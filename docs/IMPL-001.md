---
okf_version: "0.2"
document_id: "OKF-DOC-2026-ONTO-IMPL-001"
title: "Guida all'Implementazione Computazionale e Architettura Low-Spec per ONTO-PROBE"
framework_version: "v0.3.1"
date: "2026-10-11"
status: "Operational Engineering Specification (Patch v0.3.1)"
domain: "Mechanistic Interpretability, Multi-Agent Systems, Computational Creativity"
authors:
  - name: "Ricercatore Indipendente"
    role: "Lead Architect"
    license: "CC BY 4.0"
hardware_profile: "Consumer Desktop / Workstation Standalone (8-16GB VRAM o Zero-GPU)"
companion_documents:
  - id: "OKF-DOC-2026-ONTO-THEORY-001"
    title: "Research Framework: Indagine, Misurazione e Mitigazione dei Limiti dell'Innovazione Ontologica negli LLM"
    file: "THEORY-001.md"
  - id: "OKF-DOC-2026-ONTO-BENCH-001"
    title: "Catalogo dei Task e Specifiche del Benchmark O-Novel v0.1"
    file: "BENCH-001.md"
  - id: "OKF-DOC-2026-ONTO-EVAL-001"
    title: "Protocollo Sperimentale e Human Evaluation Runbook"
    file: "EVAL-001.md"
  - id: "OKF-DOC-2026-ONTO-META-001"
    title: "Valutazione della Suite Documentale e Mappatura dei Gap Operativi per ONTO-PROBE"
    file: "META-001.md"
---

# OKF v0.2 — Guida all'Implementazione Computazionale: ONTO-PROBE (v0.3.1)

> **Allineamento di Sistema:** Il presente documento costituisce il secondo modulo esecutivo della suite **ONTO-PROBE v0.3.1**. Esso traduce i requisiti teorici in architetture software verificabili ed eseguibili su workstation a basso costo, integrando le patch su API payloads, HMAC-Blinding e sicurezza semantica.

---

## 1. Sintesi Esecutiva (L1 — Synthesis Layer)

### 1.1 Obiettivo Ingegneristico

Questo dossier definisce l'architettura tecnica del framework, garantendo che l'indagine empirica sia realizzabile su hardware commerciale senza dipendere da cluster computazionali industriali.

L'infrastruttura governa:
1. **L'isolamento informativo assoluto** tra nodi agentici per prevenire il *diversity collapse*.
2. **L'attivazione latente mirata (CAA)** su pesi aperti per indurre spostamenti ortogonali controllati.
3. **Il sandboxing deterministico** dei verificatori logici (Z3, ProVerif).
4. **La registrazione non ripudiabile con HMAC-Blinding** per impedire la de-anonimizzazione nei test in doppio cieco.

### 1.2 Accessibilità Hardware: Profilo Reale di VRAM

La manipolazione latente non richiede cluster GPU multi-nodo:
- **Ramo White-Box (Edge/Desktop GPU):** Eseguito su modelli open-weight compatti (Llama-3.1-8B o Llama-3.2-3B) quantizzati a 4-bit (NF4). I pesi base occupano $\approx 5.5\text{ GB}$; considerando buffer di attivazione e KV-cache per $512$ token, il fabbisogno effettivo è di **$8\text{ GB}$ di VRAM minimo (12 GB raccomandato per stabilità operativa)**.
- **Ramo Black-Box (Zero-GPU locale):** Chiamate stateless a modelli commerciali (Claude 3.5 Haiku, GPT-4o-mini, Gemini 1.5 Flash). La macchina locale esegue unicamente gli script Python di orchestrazione con consumo RAM $< 200\text{ MB}$.

---

## 2. Ingegneria dei Sistemi e Workflow (L2 — Analysis Layer)

### 2.1 Modello di Esecuzione Duale

#### 2.1.1 Ramo White-Box: Contrastive Activation Addition (CAA)
Si intercetta il tensore del residual stream $\mathbf{h}^{(L)}$ al layer intermedio $L = 16$ tramite un forward pre-hook PyTorch puro, sommando il vettore direzionale ontologico estratto preventivamente:

$$\mathbf{h}^{(L)}_{\text{steered}} = \mathbf{h}^{(L)} + \alpha \cdot \mathbf{v}_{\text{onto}}, \quad \alpha \in [1.0, 2.0]$$

*(Nota metodologica: la libreria concettuale di riferimento per la CAA è `steerex`, ma l'implementazione del framework è fornita nativamente e senza dipendenze esterne in PyTorch puro al §3.3).*

#### 2.1.2 Ramo Black-Box: Generazione con Semantic Tabu
Per le chiamate API, il seed impone vincoli grammaticali e una lista di esclusione di primitive note che proibisce analogie fisiche, ingegneristiche o informatiche convenzionali.

### 2.2 Configurazione del Database Vettoriale e Modelli di Embedding

Per archiviare e confrontare i 2.000 archetipi canonici, Qdrant opera in un micro-container Docker locale.
- **Modello Locale di Default (Zero-GPU):** `bge-small-en-v1.5` (384 dimensioni). Esegue centinaia di embedding al secondo su CPU standard.
- **Modello di Validazione Incrociata:** `text-embedding-3-small` (1536 dimensioni, via API), secondo il protocollo descritto in `THEORY-001 §2.4`.
- **Configurazione Indice:** Distanza coseno, indicizzazione HNSW su disco con meno di $512\text{ MB}$ di footprint RAM.

### 2.3 Safety Layer: Constitutional Halt Gate

Il gateway di sicurezza agisce prima dell'estrazione semantica analizzando il payload rispetto a tre categorie tassative di rischio:
1. **Rischio CBRN:** Sintesi, purificazione o weaponization di agenti chimici, biologici, radiologici o nucleari.
2. **Cyber-Exploit:** Generazione di payload di iniezione zero-day, codice offuscato, shellcode polimorfico o tecniche di evasione EDR/sandbox.
3. **Manipolazione Cognitiva:** Euristiche coercitive mirate all'inganno psicologico sistematico, dark patterns persuasivi o protocolli di jailbreak conversazionale mascherati.

**Azione:** Qualora il parser lessicale/AST intercetti pattern correlati, l'esecuzione viene arrestata immediatamente (`HALT_TRIGGERED`), il payload viene scartato e l'evento viene sigillato nella catena di audit.

---

## 3. Specifiche Operative e Codice Eseguibile (L3 — Raw Dossiers)

### 3.1 Ambiente Servizi Locali: Docker Compose (`docker-compose.yml`)

```yaml
services:
  # Vector Database locale per la metrica di distanza ontologica dagli archetipi
  qdrant-archetypes:
    image: qdrant/qdrant:v1.10.0
    container_name: ontocache-qdrant
    ports:
      - "127.0.0.1:6333:6333"
    volumes:
      - ./data/qdrant_storage:/qdrant/storage
    environment:
      - QDRANT__SERVICE__ENABLE_TELEMETRY=false
    deploy:
      resources:
        limits:
          memory: 512M

  # Microservizio di sandboxing per verifica formale tramite Z3 (Binario A).
  # Rete "internal": nessuna uscita verso Internet e nessuna porta pubblicata
  # sull'host; è raggiungibile solo dai container collegati a "onto-sandbox".
  formal-verifier:
    build:
      context: ./verifier
      dockerfile: Dockerfile
    container_name: ontocache-verifier
    networks:
      - onto-sandbox
    cap_drop:
      - ALL
    read_only: true
    tmpfs:
      - /tmp:rw,noexec,nosuid,size=64m
    deploy:
      resources:
        limits:
          cpus: "1.0"
          memory: 256M

networks:
  onto-sandbox:
    internal: true
```

Per invocare il verificatore dall'host senza aprire la rete, eseguire il client in un container collegato a `onto-sandbox` (ad esempio `docker compose run --rm --network onto-sandbox ...`) oppure `docker exec ontocache-verifier python -c "..."`. Il file `verifier_service.py` va collocato in `./verifier/` accanto al `Dockerfile`.

Dockerfile del modulo verificatore (`./verifier/Dockerfile`):
```dockerfile
FROM python:3.11-slim
RUN pip install --no-cache-dir fastapi uvicorn z3-solver pydantic
WORKDIR /app
COPY verifier_service.py /app/
USER nobody
EXPOSE 8000
CMD ["uvicorn", "verifier_service:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 3.2 Microservizio di Verifica Formale (`verifier_service.py`)

```python
import time
from fastapi import FastAPI
from pydantic import BaseModel
import z3

app = FastAPI(title="Formal Verification Engine")

class SmtVerificationRequest(BaseModel):
    smt_formula: str
    expected: str = "sat"  # esito atteso del task: "sat" oppure "unsat" (es. A12: assenza di deadlock = "unsat")
    timeout_ms: int = 5000

class VerificationResponse(BaseModel):
    is_valid: bool
    status: str
    latency_ms: float

@app.post("/verify/smt", response_model=VerificationResponse)
def verify_smt(request: SmtVerificationRequest):
    start = time.time()
    solver = z3.Solver()
    solver.set("timeout", request.timeout_ms)
    
    try:
        parsed_assertions = z3.parse_smt2_string(request.smt_formula)
        solver.add(parsed_assertions)
        result = solver.check()
        
        status_str = str(result)
        if request.expected not in ("sat", "unsat"):
            raise ValueError("expected deve essere 'sat' o 'unsat'")
        # "unknown" (timeout o incompletezza del solver) non è mai valido
        valid = (status_str == request.expected)
        
        return VerificationResponse(
            is_valid=valid,
            status=status_str,
            latency_ms=(time.time() - start) * 1000
        )
    except Exception as e:
        return VerificationResponse(
            is_valid=False,
            status=f"Parse/Logic Error: {str(e)}",
            latency_ms=(time.time() - start) * 1000
        )
```

### 3.3 Modulo White-Box PyTorch a Bassa VRAM (`ontological_steerer.py`)

> **Allineamento v0.3.2:** la classe riportata è quella del collaudo `code/notebook_caa_smoke_test_v0_3_2.py` (fonte canonica). Rispetto alla bozza v0.3.1 estrae e inietta l'attivazione nello stesso punto (ingresso del layer target, via forward pre-hook), incapsula le coppie contrastive come risposta *assistant* nel chat template e isola i buffer con `.clone()`. Richiede 8 GB VRAM minimo (12 GB raccomandato).

```python
import os
from typing import List, Optional

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig

MODEL_ID = "meta-llama/Llama-3.1-8B-Instruct"
LAYER_IDX = 16
MAX_NEW_TOKENS = 256

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
```

### 3.4 Orchestratore MAS con Protocollo HMAC-Blinding (`orchestrator.py`)

```python
import os
import json
import time
import hmac
import hashlib
from typing import Dict, Any, Optional
import requests

class IsolatedOrchestrator:
    """
    Orchestratore Multi-Agente privo di sessione con separazione crittografica
    tra identificatore interno e ID cieco pubblico via HMAC.
    """
    def __init__(self, api_endpoint: str, api_key: str, hmac_secret_key: str, default_model: str = "gpt-4o-mini"):
        self.api_endpoint = api_endpoint
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        self.hmac_secret = hmac_secret_key.encode("utf-8")
        self.default_model = default_model
        self.audit_log_path = "audit_receipt_chain.jsonl"
        self.last_hash = "0" * 64

    def derive_blind_id(self, internal_sample_id: str) -> str:
        """Deriva un UUID cieco non invertibile per la valutazione in doppio cieco."""
        digest = hmac.new(self.hmac_secret, internal_sample_id.encode("utf-8"), hashlib.sha256).hexdigest()
        return f"BLIND-SAMPLE-{digest[:12]}"

    def _call_stateless_llm(self, system_prompt: str, user_prompt: str, model: Optional[str] = None) -> str:
        payload = {
            "model": model or self.default_model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt} # Corretto: ruolo standard OpenAI-compatible
            ],
            "temperature": 0.7
        }
        resp = requests.post(self.api_endpoint, headers=self.headers, json=payload, timeout=30)
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"]

    def _append_audit_block(self, internal_sample_id: str, stage: str, payload_data: Dict[str, Any]):
        timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        blind_id = self.derive_blind_id(internal_sample_id)
        payload_str = json.dumps(payload_data, sort_keys=True)
        payload_hash = hashlib.sha256(payload_str.encode("utf-8")).hexdigest()
        
        # Hash chain su 5 campi canonici concordati con THEORY-001 ed EVAL-001
        raw_to_hash = f"{self.last_hash}{internal_sample_id}{timestamp}{stage}{payload_hash}"
        block_hash = hashlib.sha256(raw_to_hash.encode("utf-8")).hexdigest()
        
        record = {
            "internal_sample_id": internal_sample_id,
            "blind_id": blind_id,
            "timestamp": timestamp,
            "stage": stage,
            "payload_hash": payload_hash,
            "prev_hash": self.last_hash,
            "block_hash": block_hash,
            "payload": payload_data
        }
        
        with open(self.audit_log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(record) + "\n")
            
        self.last_hash = block_hash

    def run_cycle(self, internal_sample_id: str, ontological_seed: str, target_problem: str) -> Dict[str, Any]:
        blind_id = self.derive_blind_id(internal_sample_id)
        
        # 1. World Builder: Conosce solo il seed
        sys_builder = "Sei un World Builder formale. Genera assiomi coerenti ma alieni basati sul vincolo dato."
        world_raw = self._call_stateless_llm(sys_builder, f"Constraint Seed: {ontological_seed}")
        self._append_audit_block(internal_sample_id, "world_builder", {"output": world_raw})

        # 2. Blind Solver: Riceve solo il mondo sintetico
        sys_solver = "Sei un risolutore astratto. Trova una configurazione di stabilità nel mondo descritto."
        solution_raw = self._call_stateless_llm(sys_solver, f"World Specs: {world_raw}")
        self._append_audit_block(internal_sample_id, "blind_solver", {"output": solution_raw})

        # 3. Extractor: Mappa le relazioni invarianti sul problema reale
        sys_extractor = "Sei un analista strutturale. Estrai le relazioni invarianti e risolvi il problema dato."
        user_extractor = f"Abstract Strategy: {solution_raw}\nTarget Problem: {target_problem}"
        final_solution = self._call_stateless_llm(sys_extractor, user_extractor)
        self._append_audit_block(internal_sample_id, "extractor", {"output": final_solution})

        return {
            "internal_sample_id": internal_sample_id,
            "blind_sample_id": blind_id,
            "world": world_raw,
            "abstract_solution": solution_raw,
            "projected_solution": final_solution,
            "chain_head": self.last_hash
        }
```

### 3.5 Matrice dei Costi e Fabbisogno Aggregato dell'Esperimento

| Componente | Ambiente di Esecuzione | Requisito Hardware Reale | Costo Unitario | Stima Benchmark Totale (50 task × 3 cond.) |
|---|---|---|---|---|
| **World & Solver MAS** | API (GPT-4o-mini / Haiku / Flash) | CPU con rete | ~€0.003 / ciclo | ~€15.00 – €30.00 (campagna completa) |
| **White-Box Steering** | Locale (Llama-3.1-8B NF4) | GPU 8–12 GB VRAM | €0 (consumo locale) | €0 |
| **Qdrant Vector DB** | Docker Locale (CPU) | 512 MB RAM | €0 | €0 |
| **Formal Verifier (Z3)** | Docker Sandbox (CPU) | 256 MB RAM | €0 | €0 |
| **LLM Judges (Binario B)** | 3 API eterogenee | CPU con rete | ~€0.01 / validazione | ~€10.00 – €15.00 |

---

## 4. SOURCES Block

- [Turner et al. 2023](https://arxiv.org/abs/2308.10248) → Activation Addition: Steering Without Optimization
- [Rimsky et al. 2024](https://aclanthology.org/2024.acl-long.657/) → Steering Llama 2 via Contrastive Activation Addition
- [steerex 2026](https://pypi.org/project/steerex/) → Conceptual framework for activation engineering (riferimento teorico)
- [de Moura & Bjørner 2008](https://doi.org/10.1007/978-3-540-78800-3_24) → Z3: An Efficient SMT Solver
- [Qdrant Team 2024](https://qdrant.tech/documentation/) → Vector Storage for Archetypal Comparison
- [Vassilev 2026](https://doi.org/10.1109/MSEC.2026.3678214) → NIST Standards: Continuous Auditing for Adversarial AI
- [OKF v0.2 Specification 2026](https://cloud.google.com/blog) → Google Open Knowledge Format Guidelines
- [ONTO-PROBE Research Framework 2026](THEORY-001.md) → OKF-DOC-2026-ONTO-THEORY-001
- [ONTO-PROBE Benchmark Catalog 2026](BENCH-001.md) → OKF-DOC-2026-ONTO-BENCH-001
- [ONTO-PROBE Evaluation Runbook 2026](EVAL-001.md) → OKF-DOC-2026-ONTO-EVAL-001
- [ONTO-PROBE Suite Analysis 2026](META-001.md) → OKF-DOC-2026-ONTO-META-001