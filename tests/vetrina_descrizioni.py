#!/usr/bin/env python3
"""Regressions for title/episode synopsis and persistent Vetrina catalog selection."""
from pathlib import Path

def source(name):
    return Path(name).read_text(encoding="utf-8")

def check(ok, label):
    if not ok:
        raise SystemExit("FAIL Vetrina/descriptions: " + label)
    print("PASS Vetrina/descriptions: " + label)

settings = source("src/ajustes.c")
layout = source("src/ajustes_ux_tela.inc")
catalog = source("src/descanso.c")
detail = source("src/detail.c")
episodes = source("src/episodios.c")
notes = source("RELEASE_NOTES.md")

check("AJ_VITRINE_CATALOGOS" in settings and "OPC(AJ_VITRINE_CATALOGOS)" in layout,
      "separate, focusable catalogue selector in Appearance settings")
check("V_DESCANSO_FONTE, 3" in settings and "v > 2 ? 0 : v" in settings,
      "third mode retains both historic source IDs unchanged")
check('dados_gravar("vetrina-catalogos.txt", vitSel)' in settings and
      'dados_ler("vetrina-catalogos.txt")' in settings and
      'ajustes_vetrina_catalogo_ativo' in settings,
      "stable catalogue-key persistence with local read/write")
check("FIL_ORIGEM_CATALOGO" in settings and "fil_chave(idx)" in settings,
      "catalogue picker never relies on mutable row positions")
check("DESC_FONTE_ESCOLHIDOS" in catalog and
      "ajustes_vetrina_catalogo_ativo(f->chave)" in catalog and
      "i >= f->ini && i < f->ini + f->n" in catalog,
      "Vetrina filters by exact configured catalogue ranges")
check("filaFonte = fonte" in catalog and "itemServe(i, filaFonte)" in catalog,
      "effective list fallback is retained between item rotations")
check("Reservoir sampling" in catalog and "vistos++" in catalog,
      "entire eligible catalogue set participates in random session")
check("VM_DESCRICAO" in episodes and "vmDescAberta" in episodes and
      "vmDescTexto" in episodes and "Leggi descrizione completa" in episodes,
      "episode long-press menu includes full synopsis without replacing watched actions")
check("sinFoco" in detail and "sinLendo" in detail and
      "sinopseModalDesenhar" in detail,
      "title synopsis can receive focus and opens a read-only overlay")
check("## 2.0.31" in notes, "release notes describe these changes")
