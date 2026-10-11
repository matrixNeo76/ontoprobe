#!/usr/bin/env python3
"""Genera il notebook Colab (.ipynb) da code/notebook_caa_smoke_test_v0_3_2.py.

Il file .py (formato "percent": celle separate da `# %%`) resta la fonte unica;
il .ipynb è un artefatto generato. Uso: python tools/build_notebook.py
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "code" / "notebook_caa_smoke_test_v0_3_2.py"
DST = ROOT / "code" / "notebook_caa_smoke_test_v0_3_2.ipynb"

MARKER = re.compile(r"^# %%(.*)$", re.M)


def to_source(lines):
    return [l + "\n" for l in lines[:-1]] + ([lines[-1]] if lines else [])


def build():
    text = SRC.read_text(encoding="utf-8")
    parts = MARKER.split(text)  # [pre, marker1, body1, marker2, body2, ...]
    cells = []
    for marker, body in zip(parts[1::2], parts[2::2]):
        body = body.strip("\n")
        if not body.strip():
            continue
        lines = body.split("\n")
        if "[markdown]" in marker:
            md = [re.sub(r"^# ?", "", l) for l in lines]
            cells.append({"cell_type": "markdown", "id": f"cell{len(cells):03d}", "metadata": {}, "source": to_source(md)})
        else:
            cells.append({
                "cell_type": "code", "id": f"cell{len(cells):03d}", "metadata": {}, "execution_count": None,
                "outputs": [], "source": to_source(lines),
            })
    nb = {
        "nbformat": 4,
        "nbformat_minor": 5,
        "metadata": {
            "accelerator": "GPU",
            "colab": {"gpuType": "T4", "provenance": []},
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python"},
        },
        "cells": cells,
    }
    DST.write_text(json.dumps(nb, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"Scritto {DST.relative_to(ROOT)} ({len(cells)} celle)")


if __name__ == "__main__":
    build()
