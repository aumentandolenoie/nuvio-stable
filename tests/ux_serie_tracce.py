#!/usr/bin/env python3
"""Regression contract: initial series focus, read-only incompatible audio, language-first subtitles."""
from pathlib import Path

def content(p):
    return Path(p).read_text(encoding="utf-8")

def check(condition, message):
    if not condition:
        raise SystemExit("FAIL ux serie/tracce: " + message)
    print("PASS ux serie/tracce:", message)

detail = content("src/detail.c")
faixas = content("src/faixas.c")
video = content("src/video.c")
legendas = content("src/legendasui.c")
test = content("tests/legendasui.c")
vhead = content("src/video.h")

check("epAutoPendente = 1;" in detail and "proximoNuvioNoDetalhe(ciAuto, &tt, &ee)" in detail,
      "on series opening use same Nuvio Sync next-episode resolver")
check("foco.colunaLembrada[SEC_TEMPORADAS] = temporada;" in detail and
      "foco.colunaLembrada[SEC_EPISODIOS] = trovata;" in detail and
      "if (foco.fileira == SEC_EPISODIOS) foco.coluna = trovata;" in detail,
      "update season and episode focus, not primary Play")
check("epAutoPendente = 0;" in detail and "foco.fileira == SEC_TEMPORADAS" in detail,
      "manual season/episode focus takes precedence")
check("video_audio_omessa(int i);" in vhead and "video_audio_noncompatibile(int i);" in vhead and
      "originali > nAudio" in video and 'strncmp(m->codec, "A_DTS", 5)' in video and
      "__atomic_store_n(&nAudioOmesse, 0, __ATOMIC_RELEASE)" in video,
      "missing DTS tracks come from MKV, reset each source, never use native index")
check("if (foco[0] >= video_n_audio() || video_audio_noncompatibile(foco[0])) return;" in faixas and
      "video_n_audio() + video_n_audio_omesse()" in faixas and
      'i18n("Fonte audio non compatibile")' in faixas,
      "incompatible tracks displayed and cannot reach audio selection")
check("else video_sondar_mkv_agora();" in faixas,
      "audio page requests missing MKV metadata only on open")
check("LR_IDIOMA" in legendas and "if (mais && !ver)" in legendas and
      "ver = 1; alvo = 0;" in legendas and
      "if (ver) { ver = 0;" in legendas,
      "subtitles choose language first, then filtered tracks and back")
check('linhaDe("ling|pt")' in test and 'linhaDe("ling|en")' in test and
      "assert(ver && !strcmp(verIdioma, \"en\")" in test,
      "language-first subtitle view has regression tests")
