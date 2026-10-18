#!/usr/bin/env python3
"""Regression: TV guide category budget must accommodate multi-genre addons."""
from pathlib import Path
h=Path("src/guiacorte.h").read_text()
g=Path("src/guia.c").read_text()
assert "#define GUIACORTE_MAX_CAT    128" in h
assert "#define G_MAX_CAT    GUIACORTE_MAX_CAT" in g
assert "if (sNCats >= G_MAX_CAT) return -1;" in g
assert "guideChildLine(int at)" in g
assert "guideGroupOf(linhaNome(l))" in g
assert "if (c.cat >= 0) { sCanais[sNCanais++] = c;" in g
print("PASS: LG guide has capacity for StreamViX and TVVoo genre categories")
