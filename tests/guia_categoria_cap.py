#!/usr/bin/env python3
"""TV guide maintains bounded memory with two provider categories."""
from pathlib import Path
h=Path("src/guiacorte.h").read_text()
g=Path("src/guia.c").read_text()
assert '#define GUIACORTE_MAX_CANAL  900' in h
assert '#define G_GUIDE_GROUPS 2' in g
assert 'if (sNCats >= G_MAX_CAT) return -1;' in g
assert 'if (c.cat >= 0) { sCanais[sNCanais++] = c;' in g
print("PASS: capacity bound and simplified provider groups")
