"""Aggregazione dei giudizi, ICC(2,k) e confronto tra condizioni (solo libreria standard)."""
import random
from collections import defaultdict
from statistics import mean
from typing import Any, Dict, List, Optional, Sequence

APPROPRIATENESS_MIN = 2.5   # EVAL-001 §4: sotto questa soglia O-novelty = 0
ICC_MIN = 0.60              # Cicchetti 1994
DISAGREEMENT_RANGE = 2.0    # scarto massimo tra giudici oltre il quale il dossier va al referee umano


def icc2k(matrix: Sequence[Sequence[float]]) -> Optional[float]:
    """ICC(2,k): effetti casuali a due vie, media di k rater, accordo assoluto (Shrout & Fleiss 1979).

    matrix: n bersagli x k rater, senza valori mancanti. Restituisce None se non calcolabile.
    """
    n, k = len(matrix), len(matrix[0]) if matrix else 0
    if n < 2 or k < 2:
        return None
    grand = sum(sum(r) for r in matrix) / (n * k)
    row_means = [sum(r) / k for r in matrix]
    col_means = [sum(matrix[i][j] for i in range(n)) / n for j in range(k)]
    ssr = k * sum((m - grand) ** 2 for m in row_means)
    ssc = n * sum((m - grand) ** 2 for m in col_means)
    sst = sum((matrix[i][j] - grand) ** 2 for i in range(n) for j in range(k))
    sse = sst - ssr - ssc
    msr, msc, mse = ssr / (n - 1), ssc / (k - 1), sse / ((n - 1) * (k - 1))
    denom = msr + (msc - mse) / n
    if denom == 0:
        return None
    return (msr - mse) / denom


def aggregate_dossier(judgments: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Riassume i giudizi validi di un dossier. Il gate funzionale azzera la novità (EVAL-001 §4)."""
    ok = [j for j in judgments if "error" not in j]
    if not ok:
        return {"n_judges": 0, "valid": False, "gated_novelty": None}
    appr = mean(j["appropriateness_score"] for j in ok)
    coh = mean(j["logical_coherence_score"] for j in ok)
    nov = mean(j["structural_novelty_score"] for j in ok)
    taboo_votes = sum(1 for j in ok if j["taboo_violation_detected"])
    taboo = taboo_votes * 2 > len(ok)
    gate = appr >= APPROPRIATENESS_MIN and not taboo
    spread = max(
        max(j[k] for j in ok) - min(j[k] for j in ok)
        for k in ("appropriateness_score", "structural_novelty_score")
    )
    return {
        "n_judges": len(ok), "appropriateness": appr, "coherence": coh, "novelty": nov,
        "taboo_leak": taboo, "gate_passed": gate,
        # novità normalizzata in [0,1]; 0 se il gate non è superato
        "gated_novelty": (nov - 1.0) / 4.0 if gate else 0.0,
        "escalate_to_human": len(ok) >= 2 and spread >= DISAGREEMENT_RANGE,
        "valid": True,
    }


def icc_by_dimension(per_dossier: Dict[str, List[Dict[str, Any]]], judges: Sequence[str]) -> Dict[str, Optional[float]]:
    """ICC(2,k) per dimensione, usando solo i dossier valutati con successo da TUTTI i giudici."""
    out: Dict[str, Optional[float]] = {}
    for key in ("appropriateness_score", "logical_coherence_score", "structural_novelty_score"):
        rows = []
        for js in per_dossier.values():
            by_judge = {j["judge"]: j for j in js if "error" not in j}
            if all(j in by_judge for j in judges):
                rows.append([by_judge[j][key] for j in judges])
        out[key] = icc2k(rows)
    return out


def bootstrap_diff(a: Dict[str, float], b: Dict[str, float], n_boot: int = 5000,
                   seed: int = 0) -> Optional[Dict[str, float]]:
    """Differenza media a-b su unità appaiate (task) con IC bootstrap al 95%."""
    keys = sorted(set(a) & set(b))
    if len(keys) < 3:
        return None
    diffs = [a[k] - b[k] for k in keys]
    rng = random.Random(seed)
    boots = sorted(mean(rng.choice(diffs) for _ in diffs) for _ in range(n_boot))
    lo, hi = boots[int(0.025 * n_boot)], boots[int(0.975 * n_boot) - 1]
    return {"mean_diff": mean(diffs), "ci_low": lo, "ci_high": hi, "n_tasks": len(keys)}


def summarize(records: List[Dict[str, Any]]) -> Dict[str, Any]:
    """records: un elemento per dossier con task_id, condition, domain e l'aggregato dei giudizi."""
    valid = [r for r in records if r.get("valid")]
    by_cond: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    for r in valid:
        by_cond[r["condition"]].append(r)
    conditions = {}
    for c, rs in sorted(by_cond.items()):
        conditions[c] = {
            "n": len(rs),
            "gated_novelty_mean": mean(r["gated_novelty"] for r in rs),
            "appropriateness_mean": mean(r["appropriateness"] for r in rs),
            "novelty_raw_mean": mean(r["novelty"] for r in rs),
            "gate_pass_rate": mean(1.0 if r["gate_passed"] else 0.0 for r in rs),
            "taboo_leak_rate": mean(1.0 if r["taboo_leak"] else 0.0 for r in rs),
            "escalation_rate": mean(1.0 if r["escalate_to_human"] else 0.0 for r in rs),
        }
    per_task: Dict[str, Dict[str, List[float]]] = defaultdict(lambda: defaultdict(list))
    for r in valid:
        per_task[r["condition"]][r["task_id"]].append(r["gated_novelty"])
    task_means = {c: {t: mean(v) for t, v in d.items()} for c, d in per_task.items()}
    contrasts = {}
    for x, y in (("C3", "C1"), ("C3", "C2"), ("C2", "C1")):
        if x in task_means and y in task_means:
            contrasts[f"{x}-{y}"] = bootstrap_diff(task_means[x], task_means[y])
    return {"conditions": conditions, "contrasts": contrasts}
