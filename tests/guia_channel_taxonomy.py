#!/usr/bin/env python3
"""Regression: TV guide uses provider categories and excludes StreamViX Live."""
from pathlib import Path
s = Path("src/guia.c").read_text()
assert 'c.cat = sCatDe(guiaGrupoAddon(f->base));' in s
assert 'if (!guiaCatalogoPermitido(sFontes[i].base, sFontes[i].nome, sFontes[i].id)) continue;' in s
assert 'if (contemSemCaixa(addonsCarga[i].nome, "tvvoo")) return "Tvvoo";' in s
assert 'if (contemSemCaixa(addonsCarga[i].nome, "streamvix")) return "Streamvix";' in s
assert 'contemSemCaixa(n, "streamvix live")' in s
assert 'contemSemCaixa(c, "live")' in s
assert 'contemSemCaixa(n, "streamvix eventi")' in s
assert 'if (cota > 48) cota = 48;' not in s
assert '#define GC_VERSAO 4u' in s
assert 'for (int j = i; j < sNFontes; j++)' in s
assert 'restantes++;' in s
assert 'int restantes = sNFontes - i;' not in s
assert 'sCanalPorOrigem(c.id, guiaHashBase(f->base)) < 0' in s
assert 'sCanais[i].origemHash == origem' in s
print("PASS: provider categories and per-origin channel IDs")
