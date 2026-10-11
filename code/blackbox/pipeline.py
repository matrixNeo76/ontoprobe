"""Orchestrazione: selezione task, generazione, giudizio, analisi. Tutto riprendibile (resume)."""
import json
import math
import random
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

from . import judges as J
from .audit import AuditChain, blind_id, load_or_create_key
from .conditions import CONDITIONS, calls_for
from .stats import aggregate_dossier, icc_by_dimension, summarize

DATA = Path(__file__).parent / "data" / "tasks_b.json"
DEFAULT_GEN_MODEL = "openai/gpt-4o-mini"
DEFAULT_JUDGES = ["anthropic/claude-3.5-haiku", "openai/gpt-4o-mini", "google/gemini-2.0-flash-001"]


def load_tasks(ids: Optional[Iterable[str]] = None, limit: Optional[int] = None) -> List[Dict[str, Any]]:
    tasks = json.loads(DATA.read_text(encoding="utf-8"))
    if ids:
        wanted = set(ids)
        tasks = [t for t in tasks if t["id"] in wanted]
    elif limit is not None:
        # selezione bilanciata tra i 3 domini del Binario B (round-robin)
        by_dom: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
        for t in tasks:
            by_dom[t["domain"]].append(t)
        picked: List[Dict[str, Any]] = []
        i = 0
        while len(picked) < limit and any(i < len(v) for v in by_dom.values()):
            for v in by_dom.values():
                if i < len(v) and len(picked) < limit:
                    picked.append(v[i])
            i += 1
        tasks = picked
    return tasks


def estimate(n_tasks: int, reps: int, n_worlds: int, n_judges: int,
             price_in: float, price_out: float) -> Dict[str, Any]:
    """Stima indicativa di chiamate e costo. I prezzi (USD per milione di token) sono parametri tuoi."""
    dossiers = n_tasks * reps * len(CONDITIONS)
    gen_calls = n_tasks * reps * sum(calls_for(c, n_worlds) for c in CONDITIONS)
    judge_calls = dossiers * n_judges
    tin = gen_calls * 700 + judge_calls * 1500
    tout = gen_calls * 450 + judge_calls * 250
    return {"dossiers": dossiers, "generation_calls": gen_calls, "judge_calls": judge_calls,
            "tokens_in": tin, "tokens_out": tout,
            "usd": tin / 1e6 * price_in + tout / 1e6 * price_out}


def _read_jsonl(path: Path) -> List[Dict[str, Any]]:
    if not path.exists():
        return []
    with path.open(encoding="utf-8") as f:
        return [json.loads(l) for l in f if l.strip()]


def _append_jsonl(path: Path, rec: Dict[str, Any]) -> None:
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")


def generate(client, run_dir: Path, tasks: List[Dict[str, Any]], gen_model: str, reps: int,
             n_worlds: int, log=print) -> int:
    run_dir.mkdir(parents=True, exist_ok=True)
    gen_path, audit = run_dir / "generations.jsonl", AuditChain(run_dir / "audit.jsonl")
    key = load_or_create_key(run_dir / ".hmac_key")
    done = {(r["task_id"], r["condition"], r["rep"]) for r in _read_jsonl(gen_path)}
    new = 0
    for task in tasks:
        for rep in range(reps):
            for cond, fn in CONDITIONS.items():
                if (task["id"], cond, rep) in done:
                    continue
                internal = f"{task['id']}|{cond}|{rep}"
                kwargs = {"n_worlds": n_worlds} if cond == "C3" else {}
                out = fn(client, gen_model, task, **kwargs)
                rec = {"internal_id": internal, "blind_id": blind_id(key, internal),
                       "task_id": task["id"], "domain": task["domain"], "condition": cond,
                       "rep": rep, "model": gen_model, "final": out["final"], "trace": out["trace"]}
                _append_jsonl(gen_path, rec)
                audit.append(internal, "generation", {"final": out["final"]})
                new += 1
                log(f"[gen {new}] {internal}")
    return new


def judge(client, run_dir: Path, judge_models: List[str], seed: int = 0, log=print) -> int:
    gens = _read_jsonl(run_dir / "generations.jsonl")
    tasks = {t["id"]: t for t in load_tasks()}
    j_path, audit = run_dir / "judgments.jsonl", AuditChain(run_dir / "audit.jsonl")
    done = {(r["blind_id"], r["judge"]) for r in _read_jsonl(j_path)}
    order = list(gens)
    random.Random(seed).shuffle(order)  # ordine di somministrazione randomizzato
    # dossier anonimi per eventuali referee umani (L3): solo ID cieco, problema e testo
    with (run_dir / "blind_dossiers.jsonl").open("w", encoding="utf-8") as f:
        for g in order:
            f.write(json.dumps({"blind_id": g["blind_id"], "problem": tasks[g["task_id"]]["statement"],
                                "taboo": tasks[g["task_id"]]["taboo"], "text": g["final"]},
                               ensure_ascii=False) + "\n")
    new = 0
    for g in order:
        for jm in judge_models:
            if (g["blind_id"], jm) in done:
                continue
            res = J.judge_one(client, jm, tasks[g["task_id"]], g["final"])
            _append_jsonl(j_path, {"blind_id": g["blind_id"], "judge": jm, **res})
            audit.append(g["internal_id"], "judgment", {"judge": jm, **res})
            new += 1
            log(f"[judge {new}] {g['blind_id']} <- {jm}" + (" ERRORE" if "error" in res else ""))
    return new


def analyze(run_dir: Path, judge_models: List[str]) -> Dict[str, Any]:
    gens = {g["blind_id"]: g for g in _read_jsonl(run_dir / "generations.jsonl")}
    per_dossier: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    for j in _read_jsonl(run_dir / "judgments.jsonl"):
        per_dossier[j["blind_id"]].append(j)
    records = []
    for bid, js in per_dossier.items():
        g = gens.get(bid)
        if not g:
            continue
        agg = aggregate_dossier(js)
        agg.update({"blind_id": bid, "task_id": g["task_id"], "condition": g["condition"], "domain": g["domain"]})
        records.append(agg)
    summary = summarize(records)
    summary["icc"] = icc_by_dimension(per_dossier, judge_models)
    summary["n_dossiers"] = len(gens)
    summary["n_judged"] = sum(1 for r in records if r.get("valid"))
    summary["n_judge_errors"] = sum(1 for js in per_dossier.values() for j in js if "error" in j)
    summary["judges"] = judge_models
    (run_dir / "report.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    (run_dir / "report.md").write_text(banner_if_mock(run_dir, render_report(summary)), encoding="utf-8")
    return summary


def _f(x: Optional[float], d: int = 3) -> str:
    return "n/d" if x is None or (isinstance(x, float) and math.isnan(x)) else f"{x:.{d}f}"


def render_report(s: Dict[str, Any]) -> str:
    L = ["# ONTO-PROBE — report black-box", "",
         f"Dossier generati: {s['n_dossiers']} · giudicati: {s['n_judged']} · errori dei giudici: {s['n_judge_errors']}",
         f"Giudici: {', '.join(s['judges'])}", "",
         "## Risultati per condizione", "",
         "| Condizione | N | Novità (gated, 0–1) | Appropriatezza (1–5) | Novità grezza (1–5) | Gate superato | Violazione tabù | Da escalare a umano |",
         "|---|---|---|---|---|---|---|---|"]
    for c, v in s["conditions"].items():
        L.append(f"| {c} | {v['n']} | {_f(v['gated_novelty_mean'])} | {_f(v['appropriateness_mean'], 2)} | "
                 f"{_f(v['novelty_raw_mean'], 2)} | {v['gate_pass_rate']:.0%} | {v['taboo_leak_rate']:.0%} | {v['escalation_rate']:.0%} |")
    L += ["", "C1 = singolo agente · C2 = multi-agente con memoria condivisa · C3 = ONTO-PROBE (isolato + seed).", "",
          "## Contrasti sulla novità gated (differenza media per task, IC 95% bootstrap)", ""]
    if s["contrasts"]:
        for k, v in s["contrasts"].items():
            L.append(f"- **{k}**: " + ("dati insufficienti (servono ≥ 3 task con entrambe le condizioni)" if v is None else
                     f"{v['mean_diff']:+.3f} [{v['ci_low']:+.3f}, {v['ci_high']:+.3f}] su {v['n_tasks']} task"))
    else:
        L.append("- nessun contrasto calcolabile")
    L += ["", "## Accordo tra giudici — ICC(2,k)", ""]
    for k, v in s["icc"].items():
        flag = "" if v is None else (" ✅ ≥ 0.60" if v >= 0.60 else " ⚠️ < 0.60: scala al referee umano")
        L.append(f"- {k}: {_f(v)}{flag}")
    L += ["", "## Come leggere questo report", "",
          "- La novità è giudicata da LLM: misura la **novità percepita dai giudici**, non una novità ontologica dimostrata.",
          "- Il gate azzera la novità se l'appropriatezza media è < 2.5 o se la maggioranza dei giudici rileva un tabù violato.",
          "- Un intervallo di confidenza che include 0 significa che la differenza non è distinguibile dal rumore.",
          "- Manca ancora la distanza di embedding dagli archetipi (database da 2.000 voci non costruito): "
          "questo report non la usa.",
          "- Il modello generatore compare spesso anche tra i giudici: possibile favoritismo verso il proprio stile.",
          "- Con pochi task gli intervalli sono larghi: è una prova pilota, non una conferma dell'ipotesi."]
    return "\n".join(L) + "\n"


def banner_if_mock(run_dir: Path, text: str) -> str:
    if (run_dir / "MOCK").exists():
        return ("> ⚠️ **RUN SIMULATO (--mock): i testi e i punteggi sono casuali. "
                "Serve solo a verificare che la pipeline funzioni; non interpretare i numeri.**\n\n") + text
    return text
