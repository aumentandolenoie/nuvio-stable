#!/usr/bin/env python3
"""Verifiche statiche mirate: non simulano webOS né la build C."""
from pathlib import Path

app = Path("src/app.c").read_text(encoding="utf-8")
settings = Path("src/ajustes.c").read_text(encoding="utf-8")
ui = Path("src/ajustes_ux_tela.inc").read_text(encoding="utf-8")
meta = Path("src/descoberta.c").read_text(encoding="utf-8")
sync = Path("src/sync.c").read_text(encoding="utf-8")
header = Path("src/ajustes.h").read_text(encoding="utf-8")

def check(name, ok):
    if not ok:
        raise SystemExit(f"FAIL: {name}")
    print(f"PASS: {name}")

check("selettore manuale non dipende da fonte ricordata",
      "if (escolhaManualAgora() && stream_n() > 0) {" in app
      and "if (ajustes_fonte_manual() && stream_n() > 0 && lembrada < 0)" not in app)
check("fonte memorizzata non bypassa la scelta",
      "if (!escolhaManualAgora() && !preparoEspera && tocarFonteGuardada())" in app)
check("nessuna attesa per addon precedente per aprire la lista parziale",
      'autoMotivo = "escolha manual: folha aberta com as fontes recebidas";' in app)
check("continua a guardare passa per il dettaglio condiviso",
      "home_pediu_tocar()" in app
      and "if (tocar) { cwPedido = 1; detail_pedir_reproduzir(); }" in app
      and "if ((detail_pediu_reproduzir() || doInicio) && aguardandoFonte != 2)" in app)
play = app[app.index("// A FONTE LEMBRADA DESTE TITULO"):]
check("guida TV separata dal selettore VOD",
      "if (player_id_canal()[0])" in app
      and "if (escolhaManualAgora() && stream_n() > 0)" in play)
check("opzione manuale documentata per ogni VOD",
      "a CADA pedido de reproducao VOD" in header)
sec = ui.split('SEC("Página do título"',1)[1].split('SEC("Cartazes e trailers"',1)[0]
check("preferenza metadata visibile senza altre opzioni",
      "OPC(AJ_DET_META_EXT)" in sec.split("MAIS()",1)[0]
      and sec.count("OPC(AJ_DET_META_EXT)") == 1)
check("metadata addon prioritario anche per italiano",
      "if (externo) {\n    ok = textoDoAddon(" in meta
      and "if (!tit[0] || !sin[0])" in meta
      and 'if (externo && !naoIng)' not in meta)
check("preference metadata in sincronizzazione ufficiale",
      '"preferExternalMetaAddonDetail"' in settings
      and "sync_pull_profile_settings_blob" in sync
      and "sync_push_profile_settings_blob" in sync)
print("Contratti Nuvio Stable soddisfatti.")

# CW deve abrir a folha ANTES de criar o player. A excecao temporaria
# depende de um inicio REAL e da identidade do episodio e perfil.
cw = app[app.index('int pedidoCW = cwPedido;'):]
pre, resto = cw.split('} else {\n      marco("abrir: reproduzir pedido");', 1)
check("CW apre le fonti prima di aprire il player",
      "stream_folha_abrir(); // si riempie mentre gli addon rispondono" in pre
      and "player_abrir(" not in pre
      and "cwFolhaAntesPlayer" in pre)
check("solo CW del medesimo episodio entro 6h salta scelta",
      "cwfonte6h_recente(cwItem->imdb, cwT, cwE" in pre
      and "cwAutoRecente = 0;" in pre
      and "cwAutoRecente = 0; // il prossimo episodio" in app)
check("si memorizza solo avvio effettivo di video",
      "if (provaSeg >= 2.0)" in app
      and "cwfonte6h_registrar(ci->imdb, t, e" in app)
