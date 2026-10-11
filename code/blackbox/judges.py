"""Giudici LLM del Binario B: prompt e schema da EVAL-001 §3.1, con parsing e validazione."""
import json
import re
from typing import Any, Dict, Optional

from .conditions import problem_block

JUDGE_SYSTEM = """Sei un arbitro scientifico indipendente specializzato in epistemologia e teoria dei sistemi.
Valuta la proposta concettuale candidata rispetto al problema assegnato e agli archetipi tabù.
Valuta l'output con il massimo rigore. Non premiare l'oscurità lessicale o il gergo non funzionale.

FORMATO DI RISPOSTA RICHIESTO (STRETTAMENTE JSON, nessun testo fuori dal JSON):
{
  "appropriateness_score": <float da 1.0 a 5.0>,
  "logical_coherence_score": <float da 1.0 a 5.0>,
  "structural_novelty_score": <float da 1.0 a 5.0>,
  "taboo_violation_detected": <true/false>,
  "identified_known_archetypes": [<stringhe di eventuali modelli noti rilevati>],
  "reasoning_summary": "<massimo 150 parole>"
}

RUBRICA DI ANCORAGGIO:
Appropriateness (Validità Funzionale):
 1.0 = Completamente incoerente o dannoso per il contesto.
 2.0 = Non risolve il problema o ignora vincoli fisici/logici basilari.
 3.0 = Risolve parzialmente il problema, con lacune operative gravi.
 4.0 = Soluzione plausibile, implementabile e priva di contraddizioni.
 5.0 = Soluzione eccellente, efficiente e pienamente coerente.

Structural Novelty (Divergenza Ontologica):
 1.0 = Banale riscrittura di modelli noti (anche se espressa con neologismi).
 2.0 = Range extension o combinazione standard di due nozioni diffuse.
 3.0 = Adattamento metaforico di un modello consolidato da un altro settore.
 4.0 = Ristrutturazione causale non convenzionale, dipendenze atipiche.
 5.0 = Nuova ontologia relazionale non riconducibile ai framework noti."""

SCORE_KEYS = ("appropriateness_score", "logical_coherence_score", "structural_novelty_score")


class JudgeParseError(ValueError):
    pass


def parse_judgment(raw: str) -> Dict[str, Any]:
    """Estrae e valida il JSON del giudice; solleva JudgeParseError se non conforme."""
    start, end = raw.find("{"), raw.rfind("}")
    if start < 0 or end <= start:
        raise JudgeParseError("nessun oggetto JSON nella risposta")
    try:
        data = json.loads(raw[start:end + 1])
    except json.JSONDecodeError as e:
        raise JudgeParseError(f"JSON non valido: {e}")
    out: Dict[str, Any] = {}
    for k in SCORE_KEYS:
        try:
            v = float(data[k])
        except (KeyError, TypeError, ValueError):
            raise JudgeParseError(f"campo mancante o non numerico: {k}")
        if not 1.0 <= v <= 5.0:
            raise JudgeParseError(f"{k} fuori scala [1,5]: {v}")
        out[k] = v
    tv = data.get("taboo_violation_detected")
    if isinstance(tv, str):
        tv = tv.strip().lower() == "true"
    if not isinstance(tv, bool):
        raise JudgeParseError("taboo_violation_detected non booleano")
    out["taboo_violation_detected"] = tv
    arche = data.get("identified_known_archetypes", [])
    out["identified_known_archetypes"] = [str(a) for a in arche] if isinstance(arche, list) else []
    out["reasoning_summary"] = str(data.get("reasoning_summary", ""))[:1500]
    return out


def judge_one(client, model: str, task: Dict[str, Any], candidate: str,
              retries: int = 1) -> Optional[Dict[str, Any]]:
    """Il giudice vede solo problema, tabù e testo candidato (nessun ruolo, condizione o modello)."""
    user = f"{problem_block(task)}\n\nPROPOSTA CANDIDATA:\n<<<\n{candidate.strip()}\n>>>"
    last = ""
    for attempt in range(retries + 1):
        prompt = user if attempt == 0 else user + "\n\nLa risposta precedente non era JSON valido: rispondi SOLO con il JSON richiesto."
        raw = client.chat(model, JUDGE_SYSTEM, prompt, temperature=0.0, max_tokens=700)
        try:
            return parse_judgment(raw)
        except JudgeParseError as e:
            last = str(e)
    return {"error": last}
