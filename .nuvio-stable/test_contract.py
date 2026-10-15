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
      "if (ajustes_fonte_manual() && stream_n() > 0) {" in app
      and "if (ajustes_fonte_manual() && stream_n() > 0 && lembrada < 0)" not in app)
check("fonte memorizzata non bypassa la scelta",
      "if (!ajustes_fonte_manual() && !preparoEspera && tocarFonteGuardada())" in app)
check("nessuna attesa per addon precedente per aprire la lista parziale",
      'autoMotivo = "escolha manual: folha aberta com as fontes recebidas";' in app)
check("continua a guardare passa per il dettaglio condiviso",
      "home_pediu_tocar()" in app
      and "if (tocar) detail_pedir_reproduzir();" in app
      and "if ((detail_pediu_reproduzir() || doInicio) && aguardandoFonte != 2)" in app)
play = app[app.index("// A FONTE LEMBRADA DESTE TITULO"):]
check("guida TV separata dal selettore VOD",
      "if (player_id_canal()[0])" in app
      and "if (ajustes_fonte_manual() && stream_n() > 0)" in play)
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
