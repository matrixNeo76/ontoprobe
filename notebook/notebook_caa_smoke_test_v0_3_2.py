# %% [markdown]
# # CAA Smoke Test — ONTO-PROBE v0.3.2
# 
# **Scopo:** collaudare empiricamente il modulo `LowVramOntologicalSteerer` prima di procedere al benchmark completo.
# 
# **Criteri di successo:**
# 1. Estrazione del vettore senza crash né NaN con chat template assistant-aligned.
# 2. Testo generato grammaticale e coerente per α ∈ [1.0, 2.0] con isolamento del tensore `.clone()`.
# 3. Relazione dose-risposta monotona tra α e distanza dal baseline.
# 4. Assi ontologici diversi producono output qualitativamente diversi.
# 
# **Hardware minimo:** GPU con ≥ 8 GB VRAM (o Colab T4 gratuita).

# %%
# @title Installazione dipendenze
import subprocess
import sys

def install_deps():
    pkgs = [
        "transformers>=4.44",
        "accelerate>=0.33",
        "bitsandbytes>=0.43",
        "sentence-transformers>=3.0",
        "nltk>=3.9",
        "pandas",
        "matplotlib",
        "pyarrow",
        "tabulate",
    ]
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", "--upgrade"] + pkgs)

try:
    import pyarrow
    import tabulate
except ImportError:
    install_deps()

import nltk
nltk.download("punkt", quiet=True)
nltk.download("punkt_tab", quiet=True)

# %%
# @title Configurazione globale
import os
import time
from pathlib import Path
from typing import List, Dict, Optional

import torch
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig

MODEL_ID = "meta-llama/Llama-3.1-8B-Instruct"
LAYER_IDX = 16
ALPHA_GRID = [0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0]
TARGET_PROMPT = (
    "Progetta un sistema di raffreddamento passivo per un data center "
    "modulare ad alta densità energetica. Descrivi il principio fisico "
    "e il meccanismo causale in modo dettagliato."
)
MAX_NEW_TOKENS = 256
SEED = 42

torch.manual_seed(SEED)
np.random.seed(SEED)

OUTPUT_DIR = Path("./caa_smoke_test_output")
OUTPUT_DIR.mkdir(exist_ok=True)

print(f"Modello: {MODEL_ID}")
print(f"Layer di intervento: {LAYER_IDX}")
print(f"Griglia α: {ALPHA_GRID}")
print(f"Output dir: {OUTPUT_DIR.resolve()}")

# %%
# @title Classe LowVramOntologicalSteerer (v0.3.2)
class LowVramOntologicalSteerer:
    """
    Implementazione nativa PyTorch di Contrastive Activation Addition (CAA).
    Patch v0.3.2:
      - Patch 1: Incapsulamento chat template come risposta assistant in estrazione
      - Patch 2: Pre-hook sicuro con .clone() per isolare i buffer di memoria
      - Calcolo dinamico di max_memory dalla VRAM disponibile
    """

    def __init__(self, model_id: str = MODEL_ID, layer_idx: int = LAYER_IDX):
        self.layer_idx = layer_idx
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        if self.device == "cuda":
            total_gb = torch.cuda.get_device_properties(0).total_memory / (1024 ** 3)
            gpu_budget = max(1, int(total_gb - 1.5))
            max_mem = {0: f"{gpu_budget}GiB", "cpu": "16GiB"}
            print(f"[Steerer] VRAM totale: {total_gb:.1f} GB → budget GPU: {gpu_budget} GiB")
        else:
            max_mem = None

        bnb_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_compute_dtype=torch.float16,
            bnb_4bit_quant_type="nf4",
        )

        self.tokenizer = AutoTokenizer.from_pretrained(model_id, token=os.environ.get("HF_TOKEN"))
        self.model = AutoModelForCausalLM.from_pretrained(
            model_id,
            quantization_config=bnb_config,
            device_map="auto",
            max_memory=max_mem,
            token=os.environ.get("HF_TOKEN"),
        )
        self.model.eval()

        self.steering_vector: Optional[torch.Tensor] = None
        self._inject_handle = None

    def _format_contrast_pair(self, text: str) -> str:
        """
        Incapsula il testo come messaggio assistant per allineare il punto di estrazione
        allo stato esatto che precede la generazione durante l'inferenza autoregressiva.
        """
        messages = [
            {"role": "user", "content": "Descrivi il fenomeno secondo la prospettiva richiesta."},
            {"role": "assistant", "content": text}
        ]
        return self.tokenizer.apply_chat_template(messages, tokenize=False)

    def _collect_activations(self, raw_prompts: List[str]) -> torch.Tensor:
        """
        Cattura l'hidden state in INGRESSO al layer target per l'ultimo token formattato.
        """
        activations = []
        target_layer = self.model.model.layers[self.layer_idx]

        for text in raw_prompts:
            formatted_chat = self._format_contrast_pair(text)
            inputs = self.tokenizer(formatted_chat, return_tensors="pt").to(self.device)
            captured = {"act": None}

            def pre_hook(module, args):
                captured["act"] = args[0][:, -1, :].detach().cpu()

            handle = target_layer.register_forward_pre_hook(pre_hook)
            try:
                with torch.no_grad():
                    self.model(**inputs)
            finally:
                handle.remove()

            if captured["act"] is None:
                raise RuntimeError("Hook non ha catturato alcuna attivazione.")
            activations.append(captured["act"])

        return torch.cat(activations, dim=0)

    def compute_steering_vector(self, positive_prompts: List[str], negative_prompts: List[str]):
        if not positive_prompts or not negative_prompts:
            raise ValueError("Entrambe le liste devono contenere almeno un prompt.")

        pos = self._collect_activations(positive_prompts)
        neg = self._collect_activations(negative_prompts)

        if pos.shape[0] == 0 or neg.shape[0] == 0:
            raise ValueError("Attivazioni vuote.")

        v = (pos.mean(dim=0) - neg.mean(dim=0)).to(torch.float16)

        if torch.isnan(v).any():
            raise RuntimeError("Steering vector contiene NaN.")

        self.steering_vector = v
        print(f"[Steerer] Vettore estratto — norma L2: {v.float().norm().item():.4f}")
        return v

    def attach_steering(self, strength: float = 1.5):
        if self.steering_vector is None:
            raise ValueError("Vettore non calcolato.")
        self.remove_steering()

        vec = self.steering_vector.to(self.device).to(torch.float16)
        target_layer = self.model.model.layers[self.layer_idx]

        def pre_hook(module, args):
            # Clone esplicito per evitare interferenze in-place su buffer della KV-cache
            hidden = args[0].clone()
            hidden[:, -1, :] = hidden[:, -1, :] + strength * vec
            return (hidden,) + args[1:]

        self._inject_handle = target_layer.register_forward_pre_hook(pre_hook)

    def remove_steering(self):
        if self._inject_handle is not None:
            self._inject_handle.remove()
            self._inject_handle = None

    def generate(self, prompt: str, strength: float = 0.0, max_new_tokens: int = MAX_NEW_TOKENS) -> str:
        if strength > 0.0:
            self.attach_steering(strength)
        else:
            self.remove_steering()

        try:
            messages = [{"role": "user", "content": prompt}]
            chat = self.tokenizer.apply_chat_template(
                messages, tokenize=False, add_generation_prompt=True
            )
            inputs = self.tokenizer(chat, return_tensors="pt").to(self.device)

            with torch.no_grad():
                out = self.model.generate(
                    **inputs,
                    max_new_tokens=max_new_tokens,
                    do_sample=True,
                    temperature=0.7,
                    top_p=0.9,
                    repetition_penalty=1.05,
                    pad_token_id=self.tokenizer.eos_token_id,
                )
            text = self.tokenizer.decode(
                out[0][inputs["input_ids"].shape[1]:], skip_special_tokens=True
            )
            return text.strip()
        finally:
            self.remove_steering()

    def perplexity(self, text: str) -> float:
        self.remove_steering()
        enc = self.tokenizer(text, return_tensors="pt").to(self.device)
        with torch.no_grad():
            out = self.model(**enc, labels=enc["input_ids"])
        return float(torch.exp(out.loss).item())


# %%
# @title Caricamento modello
t0 = time.time()
steerer = LowVramOntologicalSteerer()
print(f"\n[Setup] Modello caricato in {time.time() - t0:.1f}s")

if torch.cuda.is_available():
    allocated = torch.cuda.memory_allocated() / (1024 ** 3)
    reserved = torch.cuda.memory_reserved() / (1024 ** 3)
    print(f"[Setup] VRAM allocata: {allocated:.2f} GB / riservata: {reserved:.2f} GB")

# %%
# @title Coppie contrastanti per 3 assi ontologici
CONTRAST_PAIRS = {
    "asse1_sostanza_processo": {
        "positive": [
            "Describe a system as a continuous flow of transformations without discrete objects.",
            "Explain reality in terms of processes, not things.",
            "Model the world as a network of events rather than stable entities.",
            "Describe a physical phenomenon emphasizing becoming over being.",
        ],
        "negative": [
            "Describe a system as a collection of discrete, stable objects.",
            "Explain reality in terms of things, not processes.",
            "Model the world as a set of isolated entities.",
            "Describe a physical phenomenon emphasizing fixed states.",
        ],
    },
    "asse2_meccanico_sistemico": {
        "positive": [
            "Explain causality as an emergent relation between components, not a mechanical chain.",
            "Describe cause and effect as mutually constitutive within a system.",
            "Model causation through feedback and interdependence, not linear sequence.",
            "Explain how effects can precede or co-occur with causes in complex systems.",
        ],
        "negative": [
            "Explain causality as a deterministic mechanical chain of events.",
            "Describe cause and effect as strictly sequential and unidirectional.",
            "Model causation through linear input-output relations.",
            "Explain how causes produce effects through direct mechanical transmission.",
        ],
    },
    "asse3_gerarchia_eterarchia": {
        "positive": [
            "Describe an organization with no center, no levels, and no privileged nodes.",
            "Model coordination through distributed peer-to-peer relations only.",
            "Explain order arising without hierarchy or central control.",
            "Describe a structure where every node can temporarily become a hub.",
        ],
        "negative": [
            "Describe an organization with a strict pyramidal hierarchy.",
            "Model coordination through top-down commands and centralized authority.",
            "Explain order as the result of hierarchical control.",
            "Describe a structure with fixed levels and permanent roles.",
        ],
    },
}

# %%
# @title Estrazione vettori di steering
steering_vectors = {}

for name, pairs in CONTRAST_PAIRS.items():
    print(f"\n=== Estrazione asse: {name} ===")
    t0 = time.time()
    v = steerer.compute_steering_vector(pairs["positive"], pairs["negative"])
    steering_vectors[name] = v
    print(f"[{name}] Estratto in {time.time() - t0:.1f}s")

print("\n=== Similarità coseno tra vettori ===")
names = list(steering_vectors.keys())
for i, n1 in enumerate(names):
    for n2 in names[i+1:]:
        v1 = steering_vectors[n1].float()
        v2 = steering_vectors[n2].float()
        cos = torch.nn.functional.cosine_similarity(v1.unsqueeze(0), v2.unsqueeze(0)).item()
        flag = "⚠️ ALTA" if abs(cos) > 0.7 else "OK"
        print(f"  {n1} vs {n2}: cos = {cos:+.4f}  [{flag}]")

# %%
# @title Griglia di generazione (19 condizioni)
def set_steering_vector(name: str):
    steerer.steering_vector = steering_vectors[name]

results = []

# Baseline (α = 0.0)
print("\n=== Baseline (α = 0.0) ===")
t0 = time.time()
baseline_text = steerer.generate(TARGET_PROMPT, strength=0.0)
results.append({
    "asse": "baseline",
    "alpha": 0.0,
    "text": baseline_text,
    "length": len(baseline_text.split()),
    "gen_time_s": time.time() - t0,
})
print(baseline_text[:300] + "...\n")

# Assi Ontologici
for name in steering_vectors.keys():
    set_steering_vector(name)
    for alpha in ALPHA_GRID:
        if alpha == 0.0:
            continue
        print(f"\n=== {name} | α = {alpha} ===")
        t0 = time.time()
        text = steerer.generate(TARGET_PROMPT, strength=alpha)
        results.append({
            "asse": name,
            "alpha": alpha,
            "text": text,
            "length": len(text.split()),
            "gen_time_s": time.time() - t0,
        })
        print(text[:300] + "...\n")

steerer.remove_steering()
df_results = pd.DataFrame(results)
print(f"\n[Generazione] Completata: {len(df_results)} output")

# Salvataggio con fallback automatico CSV
parquet_path = OUTPUT_DIR / "caa_smoke_test_results.parquet"
csv_path = OUTPUT_DIR / "caa_smoke_test_results.csv"
try:
    df_results.to_parquet(parquet_path)
    print(f"[Export] Dati salvati in Parquet: {parquet_path.name}")
except Exception as e:
    df_results.to_csv(csv_path, index=False)
    print(f"[Export] Fallback CSV applicato ({e}): {csv_path.name}")

# %%
# @title Calcolo metriche quantitative
from sentence_transformers import SentenceTransformer
from nltk.util import ngrams
from collections import Counter

print("[Metriche] Caricamento embedder bge-small-en-v1.5...")
embedder = SentenceTransformer("BAAI/bge-small-en-v1.5", device="cpu")

def trigram_repetition(text: str) -> float:
    tokens = text.lower().split()
    if len(tokens) < 3:
        return 0.0
    trigrams = list(ngrams(tokens, 3))
    if not trigrams:
        return 0.0
    counts = Counter(trigrams)
    repeated = sum(c - 1 for c in counts.values() if c > 1)
    return repeated / len(trigrams)

def compute_metrics(df: pd.DataFrame) -> pd.DataFrame:
    print("[Metriche] Calcolo PPL...")
    df["perplexity"] = df["text"].apply(lambda t: steerer.perplexity(t))
    df["trigram_rep"] = df["text"].apply(trigram_repetition)

    print("[Metriche] Calcolo embedding semantici...")
    emb = embedder.encode(df["text"].tolist(), normalize_embeddings=True, show_progress_bar=True)
    df["_emb"] = list(emb)

    baseline_emb = df.loc[df["asse"] == "baseline", "_emb"].iloc[0]
    df["sim_to_baseline"] = df["_emb"].apply(
        lambda e: float(np.dot(e, baseline_emb))
    )
    return df

df_results = compute_metrics(df_results)

try:
    df_results.to_parquet(OUTPUT_DIR / "caa_smoke_test_metrics.parquet")
except Exception:
    pass
df_results.drop(columns=["_emb"]).to_csv(OUTPUT_DIR / "results_with_metrics.csv", index=False)

summary = df_results[["asse", "alpha", "length", "perplexity", "trigram_rep", "sim_to_baseline"]].round(3)
print("\n=== RIEPILOGO METRICHE ===")
print(summary.to_string(index=False))

# %%
# @title Valutazione criteri di successo
def evaluate_criteria(df: pd.DataFrame) -> dict:
    criteria = {}

    # Criterio 1: PPL < 200 per α ∈ [1.0, 2.0]
    mask = df["alpha"].between(1.0, 2.0) & (df["asse"] != "baseline")
    ppl_ok = (df.loc[mask, "perplexity"] < 200).all()
    criteria["PPL < 200 per α ∈ [1.0, 2.0]"] = {
        "pass": bool(ppl_ok),
        "value": float(df.loc[mask, "perplexity"].max()) if mask.any() else None,
        "threshold": 200,
    }

    # Criterio 2: ripetizione trigrammi < 50% a α = 1.5
    mask = (df["alpha"] == 1.5) & (df["asse"] != "baseline")
    rep_ok = (df.loc[mask, "trigram_rep"] < 0.5).all()
    criteria["Ripetizione trigrammi < 50% a α = 1.5"] = {
        "pass": bool(rep_ok),
        "value": float(df.loc[mask, "trigram_rep"].max()) if mask.any() else None,
        "threshold": 0.5,
    }

    # Criterio 3: variazione sim_to_baseline > 0.02
    treated = df[df["asse"] != "baseline"]
    variation = treated.groupby("asse")["sim_to_baseline"].agg(lambda s: s.max() - s.min())
    var_ok = (variation > 0.02).all()
    criteria["Variazione sim_to_baseline > 0.02"] = {
        "pass": bool(var_ok),
        "value": float(variation.min()),
        "threshold": 0.02,
    }

    # Criterio 4: divergenza tra assi > 0.05
    divergences = []
    for alpha in [1.0, 1.5, 2.0]:
        subset = df[df["alpha"] == alpha]
        embs = np.stack(subset["_emb"].tolist())
        n = len(embs)
        pairwise = []
        for i in range(n):
            for j in range(i+1, n):
                pairwise.append(float(np.dot(embs[i], embs[j])))
        if pairwise:
            divergences.append(1 - np.mean(pairwise))

    div_ok = all(d > 0.05 for d in divergences) if divergences else False
    criteria["Divergenza tra assi > 0.05"] = {
        "pass": bool(div_ok),
        "value": float(np.min(divergences)) if divergences else None,
        "threshold": 0.05,
    }

    return criteria

criteria_report = evaluate_criteria(df_results)
print("\n=== CRITERI DI SUCCESSO ===")
for name, info in criteria_report.items():
    status = "✅ PASS" if info["pass"] else "❌ FAIL"
    val = f"{info['value']:.4f}" if info['value'] is not None else "N/A"
    print(f"{status}  {name} | valore: {val} (soglia: {info['threshold']})")

overall = all(info["pass"] for info in criteria_report.values())
print(f"\n=== ESITO COMPLESSIVO: {'✅ PASS' if overall else '❌ FAIL'} ===")

# %%
# @title Report finale e visualizzazione
from datetime import datetime

report_lines = [
    "=" * 70,
    f"REPORT CAA SMOKE TEST — {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
    "=" * 70,
    f"Modello: {MODEL_ID}",
    f"Layer: {LAYER_IDX}",
    f"Griglia α: {ALPHA_GRID}",
    f"Numero output generati: {len(df_results)}",
    "",
    "--- Criteri di successo ---",
]

for name, info in criteria_report.items():
    status = "PASS" if info["pass"] else "FAIL"
    val = f"{info['value']:.4f}" if info['value'] is not None else "N/A"
    report_lines.append(f"  [{status}] {name} (valore: {val}, soglia: {info['threshold']})")

report_lines.append(f"\nESITO COMPLESSIVO: {'PASS' if overall else 'FAIL'}\n")
report_text = "\n".join(report_lines)
print(report_text)
(OUTPUT_DIR / "report.txt").write_text(report_text, encoding="utf-8")

# Grafici diagnostici
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
for name in steering_vectors.keys():
    subset = df_results[df_results["asse"] == name].sort_values("alpha")
    axes[0].plot(subset["alpha"], subset["perplexity"], marker="o", label=name)
    axes[1].plot(subset["alpha"], subset["sim_to_baseline"], marker="o", label=name)

axes[0].axhline(200, color="red", linestyle="--", label="soglia PPL")
axes[0].set_xlabel("α"); axes[0].set_ylabel("Perplexity"); axes[0].set_title("Perplexity vs α")
axes[0].legend(); axes[0].grid(True, alpha=0.3)

axes[1].axhline(0.98, color="red", linestyle="--", label="soglia inerzia")
axes[1].set_xlabel("α"); axes[1].set_ylabel("Similarità col baseline"); axes[1].set_title("Sim. col baseline vs α")
axes[1].legend(); axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(OUTPUT_DIR / "caa_smoke_test_plots.png", dpi=120)
plt.close()

print(f"\n[Fine] Tutti gli artefatti sono stati salvati in: {OUTPUT_DIR.resolve()}")