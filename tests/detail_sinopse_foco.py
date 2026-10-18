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

# Focus enlargement needs clearance between adjacent hero action pills.
actions=s[s.index("def "):] if False else Path("src/detail.c").read_text()
start=actions.index("float cyBtn = yAcoes + NV_DETW2_BTN_H * 0.5f;")
end=actions.index("// --- ILHA DE AMIGOS",start)
row=actions[start:end]
assert "float gapAcoes = NV_DETW2_BTN_GAP + (detalheRetrato() ? 0.0f : 18.0f);" in row
assert "bx += rp.w + gapAcoes;" in row
assert "bx += largura + gapAcoes;" in row
assert "NV_DETW2_CIRC+gapAcoes" in row
print("PASS: action pills retain focus-growth clearance, including expanded group")
