#!/usr/bin/env python3
"""
inspect_smoke_test_outputs.py — Strumento di Ispezione Qualitativa per CAA Smoke Test
Progetto: ONTO-PROBE (v0.3.2)

Carica i risultati prodotti da `notebook_caa_smoke_test_v0_3_2.py`, genera viste comparative
fianco a fianco, evidenzia i delta lessicali per asse ontologico e redige un dossier
analitico leggibile in formato Markdown o visualizzabile direttamente a terminale.
"""

import argparse
import sys
from pathlib import Path
from typing import List, Dict, Optional

import pandas as pd

STOPWORDS_IT = {
    "della", "delle", "dello", "degli", "questo", "questa", "questi", "queste",
    "quello", "quella", "quelli", "quelle", "sistema", "sistemi", "essere", "stato",
    "stata", "stati", "state", "anche", "tutto", "tutti", "tutta", "tutte",
    "molto", "molti", "molta", "molte", "nella", "nelle", "nello", "negli",
    "hanno", "avere", "quale", "quali", "come", "cosa", "dove", "quando",
    "perche", "perché", "sopra", "sotto", "prima", "dopo", "senza", "verso",
    "mentre", "oltre", "grazie", "tramite", "secondo", "invece", "allora",
    "quindi", "inoltre", "infatti", "oppure", "ovvero", "altri", "altra", "altre",
}

def format_dataframe_as_markdown(df: pd.DataFrame, float_digits: int = 3) -> str:
    """Formatta DataFrame come tabella Markdown pura, con float arrotondati."""
    headers = [str(c) for c in df.columns]
    lines = ["| " + " | ".join(headers) + " |"]
    lines.append("| " + " | ".join(["---"] * len(headers)) + " |")
    for _, row in df.iterrows():
        cells = []
        for c in df.columns:
            v = row[c]
            if pd.isna(v):
                cells.append("")
            elif isinstance(v, float):
                cells.append(f"{v:.{float_digits}f}")
            else:
                cells.append(str(v))
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)

def load_dataset(input_path: Path) -> pd.DataFrame:
    """Carica i dati generati, preferendo il file con metriche complete."""
    if input_path.exists():
        target = input_path
    else:
        # Priorità: CSV con metriche > Parquet con metriche > Parquet pre-metriche
        candidates = [
            input_path.parent / "results_with_metrics.csv",
            input_path.parent / "caa_smoke_test_metrics.parquet",
            input_path.parent / "caa_smoke_test_results.parquet",
        ]
        target = next((p for p in candidates if p.exists()), None)
        if target is None:
            raise FileNotFoundError(
                f"Nessun file di output trovato. Percorsi provati:\n  - {input_path}\n  - "
                + "\n  - ".join(str(p) for p in candidates)
            )

    print(f"[Loader] Lettura dati da: {target}")
    if target.suffix == ".parquet":
        return pd.read_parquet(target)
    return pd.read_csv(target)

def print_banner(title: str, width: int = 80):
    print("\n" + "=" * width)
    print(title.center(width))
    print("=" * width + "\n")


def display_dose_response_table(df: pd.DataFrame, axis_name: str):
    """Mostra la progressione all'aumentare di alpha per un singolo asse."""
    subset = df[df["asse"] == axis_name].sort_values("alpha")
    if subset.empty:
        print(f"Nessun dato per l'asse: {axis_name}")
        print(f"Assi disponibili: {sorted(a for a in df['asse'].unique() if a != 'baseline')}")
        return

    print_banner(f"PROGRESSIONE DOSE-RISPOSTA: {axis_name}")
    for _, row in subset.iterrows():
        alpha = row["alpha"]
        ppl = row.get("perplexity", "N/A")
        sim = row.get("sim_to_baseline", "N/A")
        ppl_str = f"{ppl:.2f}" if isinstance(ppl, (int, float)) else str(ppl)
        sim_str = f"{sim:.4f}" if isinstance(sim, (int, float)) else str(sim)

        print(f"--- [α = {alpha:.1f}] | PPL: {ppl_str} | Sim. Baseline: {sim_str} ---")
        text = str(row["text"]).strip()
        print(text[:400] + ("..." if len(text) > 400 else ""))
        print()

def display_cross_axis_comparison(df: pd.DataFrame, target_alpha: float = 1.5):
    """Confronta gli output dei tre assi ontologici a un valore fisso di alpha."""
    print_banner(f"CONFRONTO DIRETTO TRA ASSI ONTOLOGICI (α = {target_alpha:.1f})")

    baseline_rows = df[df["asse"] == "baseline"]
    if not baseline_rows.empty:
        print("[BASELINE NON GUIDATA (α = 0.0)]")
        print(str(baseline_rows.iloc[0]["text"])[:350] + "...\n")
        print("-" * 80)
    else:
        print("[AVVISO: Nessun output baseline (α = 0.0) disponibile nel dataset]\n")
        print("-" * 80)

    axes = sorted(a for a in df["asse"].unique() if a != "baseline")
    for axis in axes:
        row = df[(df["asse"] == axis) & (df["alpha"] == target_alpha)]
        if row.empty:
            print(f"\n[Warning] Nessun output per asse '{axis}' a α = {target_alpha}")
            continue
        record = row.iloc[0]
        ppl = record.get("perplexity", "N/A")
        sim = record.get("sim_to_baseline", "N/A")
        ppl_str = f"{ppl:.2f}" if isinstance(ppl, (int, float)) else str(ppl)
        sim_str = f"{sim:.4f}" if isinstance(sim, (int, float)) else str(sim)

        print(f"\n>>> ASSE: {axis.upper()} (PPL: {ppl_str}, Sim: {sim_str})")
        print(str(record["text"]).strip())
        print("-" * 80)


def extract_vocabulary_divergence(
    df: pd.DataFrame, target_alpha: float = 1.5
) -> Dict[str, List[str]]:
    """Estrae i termini caratterizzanti di ciascun asse rispetto al baseline."""
    baseline_rows = df[df["asse"] == "baseline"]
    baseline_words = set()
    if not baseline_rows.empty:
        baseline_words = set(str(baseline_rows.iloc[0]["text"]).lower().split())

    axes = sorted(a for a in df["asse"].unique() if a != "baseline")
    vocab_diff: Dict[str, List[str]] = {}

    for axis in axes:
        row = df[(df["asse"] == axis) & (df["alpha"] == target_alpha)]
        if row.empty:
            print(f"[Warning] Nessun dato per l'asse '{axis}' a α = {target_alpha}")
            continue
        axis_words = set(str(row.iloc[0]["text"]).lower().split())
        unique = [
            w.strip(".,;:()[]{}\"'“”«»`*")
            for w in axis_words - baseline_words
            if len(w) > 4 and w.strip(".,;:()[]{}\"'“”«»`*") not in STOPWORDS_IT
        ]
        vocab_diff[axis] = sorted(set(unique))[:15]

    return vocab_diff

def export_markdown_dossier(
    df: pd.DataFrame,
    output_file: Path,
    target_alpha: float = 1.5,
    target_axis: Optional[str] = None,
):
    """Genera un fascicolo di ispezione qualitativa in Markdown."""
    active_df = df.copy()
    if target_axis:
        active_df = active_df[active_df["asse"].isin(["baseline", target_axis])]

    md: List[str] = []
    md.append("# Dossier di Ispezione Qualitativa: CAA Smoke Test")
    md.append("\n**Framework:** ONTO-PROBE v0.3.2  ")
    md.append(f"**Data di Generazione:** {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')}  ")
    md.append(f"**Condizione di Confronto Primaria:** $\\alpha = {target_alpha}$  ")
    if target_axis:
        md.append(f"**Filtro Asse Specifico:** `{target_axis}`  ")
    md.append("\n---\n")

    md.append("## 1. Sintesi Tabellare Metriche")
    summary_cols = ["asse", "alpha", "length", "perplexity", "trigram_rep", "sim_to_baseline"]
    available_cols = [c for c in summary_cols if c in active_df.columns]
    md.append(format_dataframe_as_markdown(active_df[available_cols]))
    md.append("\n---\n")

    md.append("## 2. Termini Distintivi Introdotti dallo Steering")
    md.append(f"Parole chiave emerse a $\\alpha = {target_alpha}$ non presenti nel baseline:")
    vocab_diff = extract_vocabulary_divergence(active_df, target_alpha)
    if vocab_diff:
        for axis, words in vocab_diff.items():
            md.append(f"- **{axis}:** `{', '.join(words)}`")
    else:
        md.append("_(nessun termine distintivo rilevato o assi non disponibili)_")
    md.append("\n---\n")

    md.append("## 3. Trascrizioni Integrali degli Output")
    for _, row in active_df.iterrows():
        md.append(f"### Asse: `{row['asse']}` | $\\alpha = {row['alpha']}$")
        md.append(f"- **Perplexity:** {row.get('perplexity', 'N/A')}")
        md.append(f"- **Similarità col baseline:** {row.get('sim_to_baseline', 'N/A')}\n")
        md.append("```text")
        md.append(str(row["text"]).strip())
        md.append("```\n")

    output_file.write_text("\n".join(md), encoding="utf-8")
    print(f"[Export] Fascicolo Markdown salvato in: {output_file.resolve()}")

def main():
    parser = argparse.ArgumentParser(
        description="Strumento di ispezione e comparazione qualitativa per il CAA Smoke Test."
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=Path("./caa_smoke_test_output/results_with_metrics.csv"),
        help="Percorso al file CSV o Parquet generato dal notebook.",
    )
    parser.add_argument(
        "--alpha",
        type=float,
        default=1.5,
        help="Valore target di alpha da confrontare tra i diversi assi (default: 1.5).",
    )
    parser.add_argument(
        "--axis",
        type=str,
        default=None,
        help="Nome dell'asse specifico da analizzare in progressione dose-risposta.",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="Seme da visualizzare (default: il più basso presente). I controlli casuali compaiono come assi 'random_*'.",
    )
    parser.add_argument(
        "--export-md",
        type=Path,
        default=Path("./caa_smoke_test_output/qualitative_dossier.md"),
        help="Percorso di salvataggio per il report in formato Markdown.",
    )

    args = parser.parse_args()

    try:
        df = load_dataset(args.input)
    except FileNotFoundError as err:
        print(f"Errore: {err}", file=sys.stderr)
        sys.exit(1)

    # Validazione colonne minime
    if "asse" not in df.columns or "alpha" not in df.columns or "text" not in df.columns:
        print(
            "Errore: il dataset non contiene le colonne minime richieste "
            "('asse', 'alpha', 'text').",
            file=sys.stderr,
        )
        sys.exit(1)

    if "seed" in df.columns:
        seed = args.seed if args.seed is not None else int(df["seed"].min())
        df = df[df["seed"] == seed]
        if df.empty:
            print(f"Errore: nessun dato per il seed {seed}.", file=sys.stderr)
            sys.exit(1)
        print(f"[Seed] Visualizzazione del seed {seed}")

    if args.axis:
        display_dose_response_table(df, args.axis)
    else:
        display_cross_axis_comparison(df, target_alpha=args.alpha)

    if args.export_md:
        export_markdown_dossier(
            df, args.export_md, target_alpha=args.alpha, target_axis=args.axis
        )


if __name__ == "__main__":
    main()