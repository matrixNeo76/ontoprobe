"""Le tre condizioni sperimentali del Binario B (EVAL-001 §2.1), in versione black-box via API.

C1  Single-agent standard prompting.
C2  Multi-agent conversazionale con memoria condivisa (proponente, critico, sintetizzatore).
C3  ONTO-PROBE: seed sintattico-relazionale (THEORY-001 §3.2.2) + World Builder / Blind Solver
    isolati e stateless + rilevatore di invarianti cross-world + Extractor che mappa sul problema.

Tutte le condizioni ricevono lo stesso enunciato e gli stessi tabù: cambia solo la procedura.
"""
from typing import Any, Dict, List

SEED_GRAMMAR = """VINCOLO DI GENERAZIONE ASSIOMATICA:
1. È vietato l'uso di predicati di causalità meccanica nota o transmodale.
2. Il sistema NON può essere formulato come flusso di particelle o scambio di pacchetti.
3. Le relazioni causali devono essere descritte unicamente secondo la sintassi:
   «Lo stato di X determina la suscettibilità di transizione di Y attraverso l'inerzia di Z».
4. Qualsiasi richiamo a metafore fisiche, biologiche o computazionali standard
   comporta l'invalidazione immediata dell'output."""

FINAL_FORMAT = (
    "Rispondi in italiano, in massimo 350 parole, con: (1) principio di funzionamento, "
    "(2) meccanismo causale, (3) perché soddisfa i vincoli, (4) limiti noti."
)


def problem_block(task: Dict[str, Any]) -> str:
    lines = [f"PROBLEMA: {task['statement']}"]
    if task.get("feasibility_hint"):
        lines.append(f"INDICAZIONI DI FATTIBILITÀ (non vincolanti): {task['feasibility_hint']}")
    if task.get("validity_note"):
        lines.append(f"CRITERIO DI VALIDITÀ: {task['validity_note']}")
    if task.get("taboo"):
        lines.append("TABÙ (vietati, anche in forma travestita): " + "; ".join(task["taboo"]))
    return "\n".join(lines)


def _step(trace: List[Dict[str, str]], role: str, text: str) -> str:
    trace.append({"role": role, "output": text})
    return text


def run_c1(client, model: str, task: Dict[str, Any], temperature: float = 0.7) -> Dict[str, Any]:
    trace: List[Dict[str, str]] = []
    system = "Sei un esperto interdisciplinare. Proponi soluzioni concettuali originali e rigorose."
    out = client.chat(model, system, f"{problem_block(task)}\n\n{FINAL_FORMAT}", temperature)
    _step(trace, "single_agent", out)
    return {"final": out, "trace": trace}


def run_c2(client, model: str, task: Dict[str, Any], temperature: float = 0.7) -> Dict[str, Any]:
    """Tre agenti che leggono la stessa trascrizione (memoria condivisa)."""
    trace: List[Dict[str, str]] = []
    pb = problem_block(task)
    prop = client.chat(model, "Sei il PROPONENTE in una discussione tra esperti. Proponi una soluzione originale.",
                       f"{pb}\n\nPresenta la tua proposta in massimo 250 parole.", temperature)
    _step(trace, "proponente", prop)
    crit = client.chat(model, "Sei il CRITICO. Individua falle, violazioni dei tabù e punti banali della proposta.",
                       f"{pb}\n\nTRASCRIZIONE:\n[Proponente]: {prop}\n\nScrivi la tua critica in massimo 200 parole.",
                       temperature)
    _step(trace, "critico", crit)
    final = client.chat(model, "Sei il SINTETIZZATORE. Produci la soluzione finale tenendo conto di tutta la discussione.",
                        f"{pb}\n\nTRASCRIZIONE:\n[Proponente]: {prop}\n[Critico]: {crit}\n\n{FINAL_FORMAT}",
                        temperature)
    _step(trace, "sintetizzatore", final)
    return {"final": final, "trace": trace}


def run_c3(client, model: str, task: Dict[str, Any], temperature: float = 0.7,
           n_worlds: int = 2) -> Dict[str, Any]:
    """Pipeline isolata: ogni nodo vede solo il proprio input (stateless message passing)."""
    trace: List[Dict[str, str]] = []
    solutions = []
    for i in range(n_worlds):
        world = client.chat(
            model,
            "Sei un World Builder formale. Genera assiomi coerenti ma alieni basati sul vincolo dato. "
            "Non conosci alcun problema reale: descrivi solo un mondo sintetico autonomo.",
            f"Constraint Seed:\n{SEED_GRAMMAR}\n\nVariante del mondo n. {i + 1}: scegli entità e dinamiche "
            "diverse dalle varianti precedenti. Massimo 250 parole.", temperature)
        _step(trace, f"world_builder_{i + 1}", world)
        sol = client.chat(
            model,
            "Sei un risolutore astratto. Trova una configurazione di stabilità nel mondo descritto "
            "usando solo le sue leggi.",
            f"World Specs:\n{world}\n\nDescrivi la configurazione stabile e le relazioni che la mantengono. "
            "Massimo 200 parole.", temperature)
        _step(trace, f"blind_solver_{i + 1}", sol)
        solutions.append(sol)
    joined = "\n\n".join(f"[Mondo {i + 1}] {s}" for i, s in enumerate(solutions))
    invariants = client.chat(
        model,
        "Sei un rilevatore di isomorfismi. Estrai le relazioni strutturali che si conservano tra mondi "
        "indipendenti, ignorando i dettagli superficiali.",
        f"Soluzioni astratte:\n{joined}\n\nElenca le relazioni invarianti in forma astratta. Massimo 150 parole.",
        temperature)
    _step(trace, "isomorphism_detector", invariants)
    final = client.chat(
        model,
        "Sei un analista strutturale. Mappa le relazioni invarianti sul problema reale e risolvilo rispettando i tabù.",
        f"Strategia astratta (relazioni invarianti):\n{invariants}\n\n{problem_block(task)}\n\n{FINAL_FORMAT}",
        temperature)
    _step(trace, "extractor", final)
    return {"final": final, "trace": trace}


CONDITIONS = {"C1": run_c1, "C2": run_c2, "C3": run_c3}
CALLS_PER_CONDITION = {"C1": 1, "C2": 3, "C3": None}  # C3 = 2 * n_worlds + 2


def calls_for(condition: str, n_worlds: int = 2) -> int:
    return 2 * n_worlds + 2 if condition == "C3" else CALLS_PER_CONDITION[condition]
