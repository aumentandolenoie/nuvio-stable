#!/usr/bin/env python3
"""Independent, refreshable selected screensaver catalogs contract."""
from pathlib import Path
s=Path("src/descanso.c").read_text()
assert '#define DESC_SEL_REFRESH_MS (6u * 60u * 60u * 1000u)' in s
assert "fil_chave(k)" in s and "ajustes_vetrina_catalogo_ativo(key)" in s
assert '"movie_"' in s and '"series_"' in s
assert '"/catalog/%s/%s.json"' in s
assert "rede_baixar(url,10)" in s
assert "nv_perfil_sessao_atual(w->session)" in s
assert "descSelPendingN > 0" in s
assert "descSelGeneration++" in s
assert "if (ativo && fonte == DESC_FONTE_ESCOLHIDOS)" in s
assert "cat_acrescentar(&descSelItems[atual])" in s
print("PASS: selected Vetrina independent catalogs, six-hour refresh, stale-result protection")
