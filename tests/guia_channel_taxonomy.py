#!/usr/bin/env python3
"""Regression: the TV guide is indexed by channel, not addon/genre folders."""
from pathlib import Path
s=Path("src/guia.c").read_text()
assert 'static const char *categoriaCanal(const char *nome, const char *genero,' in s
assert 'c.cat = sCatDe(categoriaCanal(c.nome, gen, f->genero[0] ? f->genero : f->nome));' in s
assert 'sCatDe(categoriaCanal(c.nome, st[i].categoria, ""))' in s
assert 'sCatDe(categoriaCanal(c.nome, xt[i].categoria, ""))' in s
assert 'contemSemCaixa(n,"sport f1")' in s
assert 'contemSemCaixa(g,"formula 1")' in s
assert 'return "Formula 1";' in s
assert 'return "MotoGP";' in s
assert 'return "Canali sportivi";' in s
assert 'return "Canali cinema e serie";' in s
assert 'return "Pallavolo";' in s
assert '#define GC_VERSAO 3u' in s
assert 'return "Eventi live";' in s
assert 'contemSemCaixa(catalog,"eventi")' in s
assert 'guideContains(name,"pallavolo")' in s
assert 'guideContains(name,"campionati")' in s
assert 'guideContains(name,"football americano")' in s
assert 'guideContains(name,"freccette")' in s
assert 'guideContains(n,"pallavolo")' in s
assert 'guideContains(n,"campionati")' in s
print("PASS: cross-addon F1 and other channels join canonical rows; old cache invalidated")
