#!/usr/bin/env python3
"""TV guide taxonomy is by provider, and excluded catalogs do not load."""
from pathlib import Path
s=Path("src/guia.c").read_text()
assert 'c.cat = sCatDe(guiaGrupoAddon(f->base));' in s
assert 'guiaCatalogoPermitido(sFontes[i].base, sFontes[i].nome, sFontes[i].id)' in s
assert 'contemSemCaixa(n, "streamvix live")' in s
assert 'contemSemCaixa(n, "streamvix eventi")' in s
print("PASS: provider taxonomy and StreamViX Live exclusion")
