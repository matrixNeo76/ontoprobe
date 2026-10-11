#!/usr/bin/env python3
"""ONTO-PROBE black-box: esegue il Binario B via API (nessuna GPU).

Esempi (dalla radice del repository):
  python code/run_blackbox.py estimate --limit 6
  python code/run_blackbox.py all --run-id prova --limit 6 --mock        # prova a secco, offline
  export ONTO_API_KEY=...                                                 # chiave del provider
  python code/run_blackbox.py all --run-id pilot --limit 6               # pilota reale
Fasi singole: generate | judge | analyze. Le fasi sono riprendibili: rilanciando lo stesso run-id
vengono saltate le chiamate già fatte.
"""
import argparse
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from blackbox import pipeline as P  # noqa: E402
from blackbox.client import LLMClient, LLMError, MockClient  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("phase", choices=["estimate", "generate", "judge", "analyze", "all"])
    ap.add_argument("--run-id", default="run")
    ap.add_argument("--limit", type=int, default=6, help="numero di task (bilanciati sui 3 domini); 30 = benchmark completo")
    ap.add_argument("--tasks", nargs="*", help="ID espliciti (es. ONTO-B21 ONTO-B35), ha precedenza su --limit")
    ap.add_argument("--reps", type=int, default=1, help="repliche per task e condizione")
    ap.add_argument("--worlds", type=int, default=2, help="mondi sintetici per la condizione C3")
    ap.add_argument("--gen-model", default=os.environ.get("ONTO_GEN_MODEL", P.DEFAULT_GEN_MODEL))
    ap.add_argument("--judge-models", default=os.environ.get("ONTO_JUDGE_MODELS", ",".join(P.DEFAULT_JUDGES)),
                    help="elenco separato da virgole (3 giudici eterogenei raccomandati)")
    ap.add_argument("--out", default=str(ROOT / "outputs" / "blackbox"))
    ap.add_argument("--mock", action="store_true", help="client simulato, nessuna chiamata di rete")
    ap.add_argument("--price-in", type=float, default=0.3, help="USD per 1M token in ingresso (solo per la stima)")
    ap.add_argument("--price-out", type=float, default=1.2, help="USD per 1M token in uscita (solo per la stima)")
    a = ap.parse_args(argv)

    judge_models = [m.strip() for m in a.judge_models.split(",") if m.strip()]
    tasks = P.load_tasks(ids=a.tasks, limit=None if a.tasks else a.limit)
    run_dir = Path(a.out) / a.run_id

    if a.phase == "estimate":
        e = P.estimate(len(tasks), a.reps, a.worlds, len(judge_models), a.price_in, a.price_out)
        print(f"Task: {len(tasks)} · repliche: {a.reps} · giudici: {len(judge_models)}")
        print(f"Dossier: {e['dossiers']} · chiamate di generazione: {e['generation_calls']} · di giudizio: {e['judge_calls']}")
        print(f"Token stimati: {e['tokens_in']:,} in / {e['tokens_out']:,} out")
        print(f"Costo indicativo: ~{e['usd']:.2f} USD con i prezzi medi forniti ({a.price_in}/{a.price_out} per M token). "
              "Controlla i prezzi reali dei tuoi modelli.")
        return 0

    try:
        client = MockClient() if a.mock else LLMClient()
    except LLMError as e:
        print(f"Errore: {e}", file=sys.stderr)
        return 1

    if a.mock:
        run_dir.mkdir(parents=True, exist_ok=True)
        (run_dir / "MOCK").write_text("run simulato\n", encoding="utf-8")
    try:
        if a.phase in ("generate", "all"):
            n = P.generate(client, run_dir, tasks, a.gen_model, a.reps, a.worlds)
            print(f"[generate] nuove generazioni: {n}")
        if a.phase in ("judge", "all"):
            n = P.judge(client, run_dir, judge_models)
            print(f"[judge] nuovi giudizi: {n}")
        if a.phase in ("analyze", "all"):
            P.analyze(run_dir, judge_models)
            print(f"[analyze] report: {run_dir / 'report.md'}")
    except LLMError as e:
        print(f"Errore API: {e}\nRilancia lo stesso comando per riprendere da dove si è interrotto.", file=sys.stderr)
        return 2
    print(f"Chiamate: {client.calls} · token in/out: {client.tokens_in:,}/{client.tokens_out:,}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
