#!/usr/bin/env python3
"""Guard complete addon URL identity for live TV playback and prefetch."""
from pathlib import Path
g=Path("src/guia.c").read_text()
f=Path("src/fontecache.c").read_text()
assert "uint64_t origemHash;" in g
assert "c.origemHash = guiaHashBase(f->base);" in g
assert 'if (base && base[0] && guiaHashBase(base) == c->origemHash)' in g
assert "static char pedidoBase[NV_ADDON_URL_MAX];" in g
assert 'snprintf(pedidoBase, sizeof pedidoBase, "%s", c->base)' not in g
assert 'snprintf(pedidoBase, sizeof pedidoBase, "%s", guiaBaseCanal(c))' in g
assert 'guiaBaseCanal(&canais[alvo])' in g
assert "guiaBaseCanal(antes)" in g and "guiaBaseCanal(depois)" in g
assert "static char   pendBase[2][NV_ADDON_URL_MAX];" in f
assert "static char   emCursoBase[NV_ADDON_URL_MAX];" in f
print("PASS: long addon identity survives guide playback, zapping and prefetch")
