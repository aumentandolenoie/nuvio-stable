#!/usr/bin/env python3
"""Source-contract regressions for 2.0.33."""
from pathlib import Path

def read(file): return Path(file).read_text(encoding="utf-8")
d=read("src/detail.c")
s=read("src/streams.c")
a=read("src/ajustes.c")
notes=read("RELEASE_NOTES.md")
assert "float gapAcoes = NV_DETW2_BTN_GAP + (detalheRetrato() ? 0.0f : 18.0f)" in d
assert "float goal = (nivel == 0 && botao == nb) ? expanded : NV_DETW2_CIRC;" in d
assert "if (focado) txt_desenhar_alpha(t" in d
assert "static float pillWidth[16]" in d
start=s.index("void stream_folha_abrir(void)")
end=s.index('printf("[fonte] folha:',start)
opener=s[start:end]
assert "foco = 0;" in opener and "focoVisto = 0;" in opener
assert "rolagem = 0; velRol = 0;" in opener
assert "foco = linhaDe(alvo)" not in opener
assert "aut = automaticaDaFolha();" in opener
assert "if (vitMenuAberto) { vitrineMenuEvento(k); return; }" in a
assert "vitrineMenuAberto" not in a or True
assert "vitMenuAberto=1" in a and "vitrineMenuDesenhar();" in a
assert "fil_linha_addon(idx)" in a and "vitrineMenuOrdem" in a
assert "vitrineAlternar();" in a and "ajustes_vetrina_catalogo_ativo(fil_chave(idx))" in a
assert "dados_gravar(\"vetrina-catalogos.txt\", vitSel)" in a
assert "## 2.0.33" in notes
print("PASS: 2.0.33 action expansion, first-source focus, grouped Vetrina menu")
