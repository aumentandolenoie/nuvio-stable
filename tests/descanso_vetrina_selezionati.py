#!/usr/bin/env python3
"""Vetrina selected catalogs must not silently fall back to the clock."""
from pathlib import Path
s=Path("src/descanso.c").read_text()
assert "if (fonte == DESC_FONTE_ESCOLHIDOS) {" in s
assert "if (!eligible) { fonte = DESC_FONTE_CATALOGO; descSelMode=0; n=cat_n(); }" in s
assert "for (i = 0; i < n; i++) if (itemServe(i, fonte))" in s
assert "filaFontePedida = fonteAt;" in s
assert "filaRev != cat_revisao()" in s
print("PASS: selected-catalog Vetrina falls back to titles, not the clock")
