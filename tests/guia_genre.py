#!/usr/bin/env python3
"""Genre parameters remain valid while guide categories use providers."""
from pathlib import Path
g=Path("src/guia.c").read_text()
a=Path("src/addons.c").read_text()
assert '"/catalog/%s/%s/genre=%s&skip=%d.json"' in g
assert '"/catalog/%s/%s/genre=%s.json"' in g
assert 'requiredGenre' in a
assert 'if (!guiaCatalogoPermitido(sFontes[i].base, sFontes[i].nome, sFontes[i].id)) continue;' in g
assert 'if (cota > 48) cota = 48;' not in g
print("PASS: genre requests retained, provider filter applied")
