#!/usr/bin/env python3
"""Regression guards: title synopsis focus must not trap DOWN navigation."""
from pathlib import Path
s=Path("src/detail.c").read_text()
start=s.index("if (sinFoco && e->type == SDL_KEYDOWN")
end=s.index("if (corpoSobArte())",start)
handler=s[start:end]
assert "if (sk == SDLK_DOWN)" in handler
assert "secaoColunas(r) <= 0" in handler and "nivel = 1;" in handler
assert "foco.colunaLembrada[r]" in handler
assert "if (sk == SDLK_UP" in handler and "sinFoco = 0;" in handler
start=s.index("if (sinFoco && sin)")
end=s.index("if (sin) txt_bloco_corta",start)
draw=s[start:end]
assert "gfx_anel(" in draw and "focoAcento(&cr, &cg, &cb)" in draw
assert "gfx_cor(" not in draw and "0.02f, 0.2f, 0.35f" not in draw
print("PASS: synopsis DOWN navigation, UP return and accent-only focus outline")
