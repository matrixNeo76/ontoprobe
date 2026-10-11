#!/usr/bin/env python3
"""
inspect_smoke_test_outputs.py — Strumento di ispezione qualitativa per CAA Smoke Test
"""

import argparse
import sys
from pathlib import Path
from typing import Dict, List, Optional

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


def load_dataset(input_path: Path) -> pd.DataFrame:
    if input_path.exists():
        target = input_path
    else:
        candidates = [
            input_path.parent / "results_with_metrics.csv",
            input_path.parent / "caa_smoke_test_metrics.parquet",
            input_path.parent / "caa_smoke_test_results.parquet",
        ]
        target = next((p for p in candidates if p.exists()), None)
        if target is None:
            raise FileNotFoundError(f"Nessun file di output trovato in {input_path.parent}.")

    print(f"[Loader] Lettura dati da: {target}")
    if target.suffix == ".parquet":
        return pd.read_parquet(target)
    return pd.read_csv(target)


def display_cross_axis_comparison(df: pd.DataFrame, target_alpha: float = 1.5):
    print("\n=== CONFRONTO DIRETTO TRA ASSI ONTOLOGICI ===")
    baseline_rows = df[df["asse"] == "baseline"]
    if not baseline_rows.empty:
        print("[BASELINE]")
        print(str(baseline_rows.iloc[0]["text"])[:350] + "...\n")

    axes = sorted(a for a in df["asse"].unique() if a != "baseline")
    for axis in axes:
        row = df[(df["asse"] == axis) & (df["alpha"] == target_alpha)]
        if row.empty:
            print(f"[Warning] Nessun output per asse '{axis}' a α = {target_alpha}")
            continue
        record = row.iloc[0]
        print(f"\n>>> ASSE: {axis.upper()}")
        print(str(record["text"]).strip())
        print("-" * 80)


def extract_vocabulary_divergence(df: pd.DataFrame, target_alpha: float = 1.5) -> Dict[str, List[str]]:
    baseline_rows = df[df["asse"] == "baseline"]
    baseline_words = set()
    if not baseline_rows.empty:
        baseline_words = set(str(baseline_rows.iloc[0]["text"]).lower().split())

    axes = sorted(a for a in df["asse"].unique() if a != "baseline")
    vocab_diff: Dict[str, List[str]] = {}
    for axis in axes:
        row = df[(df["asse"] == axis) & (df["alpha"] == target_alpha)]
        if row.empty:
            continue
        axis_words = set(str(row.iloc[0]["text"]).lower().split())
        unique = [
            w.strip(".,;:()[]{}\"'“”«»`*")
            for w in axis_words - baseline_words
            if len(w) > 4 and w.strip(".,;:()[]{}\"'“”«»`*") not in STOPWORDS_IT
        ]
        vocab_diff[axis] = sorted(set(unique))[:15]
    return vocab_diff


def main():
    parser = argparse.ArgumentParser(description="Strumento di ispezione qualitativa del CAA Smoke Test.")
    parser.add_argument("--input", type=Path, default=Path("./outputs/results_with_metrics.csv"))
    parser.add_argument("--alpha", type=float, default=1.5)
    parser.add_argument("--export-md", type=Path, default=Path("./outputs/qualitative_dossier.md"))
    args = parser.parse_args()

    try:
        df = load_dataset(args.input)
    except FileNotFoundError as err:
        print(f"Errore: {err}", file=sys.stderr)
        sys.exit(1)

    if "asse" not in df.columns or "alpha" not in df.columns or "text" not in df.columns:
        print("Errore: dataset senza colonne richieste ('asse', 'alpha', 'text').", file=sys.stderr)
        sys.exit(1)

    display_cross_axis_comparison(df, target_alpha=args.alpha)
    vocab = extract_vocabulary_divergence(df, target_alpha=args.alpha)
    if vocab:
        print("\n=== VOCABULARY DIFFERENCE ===")
        for axis, words in vocab.items():
            print(f"{axis}: {', '.join(words)}")

    if args.export_md:
        args.export_md.parent.mkdir(parents=True, exist_ok=True)
        payload = ["# Dossier di ispezione qualitativa", ""]
        for _, row in df.iterrows():
            payload.append(f"## {row['asse']} | α = {row['alpha']}")
            payload.append(str(row["text"]).strip())
            payload.append("")
        args.export_md.write_text("\n".join(payload), encoding="utf-8")
        print(f"\n[Export] Dossier Markdown salvato in: {args.export_md.resolve()}")


if __name__ == "__main__":
    main()
