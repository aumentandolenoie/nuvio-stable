#!/usr/bin/env python3
"""Legacy genre classifier still exists for compatibility, but is not used for addon channels."""
from pathlib import Path
s=Path("src/guia.c").read_text()
assert 'static const char *categoriaCanal(' in s
assert 'c.cat = sCatDe(guiaGrupoAddon(f->base));' in s
assert '#define G_GUIDE_GROUPS 2' in s
print("PASS: provider-based channel categories")
