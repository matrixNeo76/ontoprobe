#!/usr/bin/env python3
"""Estrae i 30 task del Binario B da docs/BENCH-001.md in code/blackbox/data/tasks_b.json.

BENCH-001 resta la fonte unica; il JSON è un artefatto generato. Uso: python tools/build_tasks.py
Per i task con scheda estesa (B21, B35) il tabù è letto dalla scheda; per gli altri è ricavato
dalla frase dopo "senza"/"priva di"/"privo di" ed è vuoto se la frase non contiene un divieto
esplicito (il vincolo resta comunque nell'enunciato).
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "docs" / "BENCH-001.md"
DST = ROOT / "code" / "blackbox" / "data" / "tasks_b.json"

DOMAINS = {"21": "system_design", "31": "policy", "41": "information_theory"}
MARK = re.compile(r"\b(?:senza|priva di|privo di)\b", re.I)


def domain_of(num: int) -> str:
    return DOMAINS["21" if num < 31 else "31" if num < 41 else "41"]


def split_items(text: str):
    """Divide un elenco "a, b o c" / "a né b" rispettando le parentesi."""
    text = text.strip().rstrip(". ;")
    out, cur, depth = [], "", 0
    for tok in re.split(r"(,\s+|\s+né\s+|\s+o\s+)", text):
        if re.fullmatch(r",\s+|\s+né\s+|\s+o\s+", tok or "") and depth == 0:
            out.append(cur.strip()); cur = ""
            continue
        depth += tok.count("(") - tok.count(")")
        cur += tok
    out.append(cur.strip())
    return [o for o in out if o]


def parse():
    lines = SRC.read_text(encoding="utf-8").split("\n")
    tasks = []
    i = 0
    while i < len(lines):
        l = lines[i]
        m = re.match(r"- \*\*ONTO-B(\d+):\*\*\s*(.+)$", l)
        e = re.match(r"- \*\*ONTO-B(\d+):\s*(.+?)\*\*\s*$", l)
        if m:
            num, text = int(m.group(1)), m.group(2).strip()
            mk = MARK.search(text)
            taboo = split_items(text[mk.end():]) if mk else []
            tasks.append({"id": f"ONTO-B{num}", "domain": domain_of(num),
                          "title": text.rstrip("."), "statement": text, "taboo": taboo,
                          "feasibility_hint": ""})
        elif e:
            num, title = int(e.group(1)), e.group(2).strip().rstrip(".")
            title = re.sub(r"\(\$(.*?)\$\)", lambda m: "(" + m.group(1).replace("\\text{", "").replace("}", "").replace("^2", "²") + ")", title)
            taboo, hint, valid = [], "", ""
            j = i + 1
            while j < len(lines) and lines[j].startswith("  - "):
                body = lines[j][4:]
                if body.startswith("*Tabù Semantico:*"):
                    raw = body.split(":*", 1)[1]
                    raw = re.sub(r"^\s*Vietat[aeio]( qualsiasi)?:?\s*", "", raw)
                    taboo = [t.strip(" .") for t in raw.split(";") if t.strip(" .")]
                elif body.startswith("*Fattibilità:*"):
                    hint = body.split(":*", 1)[1].strip()
                elif body.startswith("*Validità CDAT:*"):
                    valid = body.split(":*", 1)[1].strip()
                j += 1
            tasks.append({"id": f"ONTO-B{num}", "domain": domain_of(num), "title": title,
                          "statement": title, "taboo": taboo, "feasibility_hint": hint,
                          "validity_note": valid})
            i = j - 1
        i += 1
    return sorted(tasks, key=lambda t: int(t["id"].split("B")[1]))


if __name__ == "__main__":
    tasks = parse()
    DST.parent.mkdir(parents=True, exist_ok=True)
    DST.write_text(json.dumps(tasks, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Scritti {len(tasks)} task in {DST.relative_to(ROOT)}")
