#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
out="$(mktemp)"
trap 'rm -f "$out"' EXIT
cc -std=gnu11 -Wall -Wextra -Werror -Isrc tests/audio_reserva.c src/linguas.c -o "$out"
"$out"
python3 - <<'PY'
from pathlib import Path
s = Path('src/ajustes.c').read_text()
v = Path('src/video.c').read_text()
t = Path('src/video_tizen.c').read_text()
a = Path('src/video_android.c').read_text()
ui = Path('src/ajustes_ux_tela.inc').read_text()
default = Path('src/ajustes_ux_padrao.inc').read_text()
assert 'AJ_AUD_LINGUA2,' in s
assert '"audioReservaIdiomaLocal"' in s
assert 'return i == AJ_CW_FONTE' in s and 'i == AJ_AUD_LINGUA2' in s
assert 'ling_local_audio2(c)' in s
assert 'OPC(AJ_AUD_LINGUA), OPC(AJ_AUD_LINGUA2)' in ui
assert 'secondary audio language: Nenhuma' in default
picker = Path('src/ajustes_ux_dados.inc').read_text()
assert 'else if (op == AJ_AUD_LINGUA2)' in picker
reserve = picker.split('else if (op == AJ_AUD_LINGUA2)', 1)[1].split('else if (op == AJ_LEG_LINGUA', 1)[0]
assert 'v == 0' in reserve and '"Nenhuma"' in reserve
assert 'v + 1' in reserve and 'ling_opcao_codigo(idx)' in reserve
assert 'ling_nome(cod)' in reserve and 'i18n(texto)' in reserve
assert 'ling_audio2(void)   { return emVigor(localAud2, ""); }' in Path('src/linguas.c').read_text()

for source in (v, t, a):
    assert 'nv_audiopref_trova(' in source
    assert 'ling_audio(), ling_audio2()' in source or 'ling_audio(),\n                                          ling_audio2()' in source
print('PASS: impostazione persistente e selettore collegati ai tre backend')
PY
