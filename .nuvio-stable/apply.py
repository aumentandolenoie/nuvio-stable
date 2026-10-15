#!/usr/bin/env python3
"""Applica modifiche piccole e verificabili al snapshot della Legacy.
Fallisce se upstream cambia le sequenze attese, senza alterare file incerti.
"""
from pathlib import Path


def replace_one(filename: str, before: str, after: str) -> None:
    path = Path(filename)
    data = path.read_text(encoding="utf-8")
    count = data.count(before)
    if count != 1:
        raise SystemExit(f"{filename}: frammento atteso trovato {count} volte, richiesto 1")
    path.write_text(data.replace(before, after, 1), encoding="utf-8")
    print(f"[stable] modificato {filename}")


# L'opzione è locale perché non esiste un suo equivalente nel profilo ufficiale.
# Sono invece già sincronizzate le preferenze condivise, tra cui
# preferExternalMetaAddonDetail (ajustes.c + sync.c).
replace_one(
    "src/app.c",
    'if (ajustes_fonte_manual() && lembrada < 0) {\n'
    '    if (!prefPendente) autoMotivo = "escolha manual: a folha abre com o que chegou";\n'
    '    return !prefPendente;\n'
    '  }',
    'if (ajustes_fonte_manual()) {\n'
    '    // Il selettore manuale non aspetta una fonte memorizzata: resta\n'
    '    // aperto mentre gli altri addon terminano di rispondere.\n'
    '    autoMotivo = "escolha manual: folha aberta com as fontes recebidas";\n'
    '    return 1;\n'
    '  }',
)
# Il collegamento VOD ricordato dalla sessione NON deve bypassare il pannello.
replace_one(
    "src/app.c",
    'if (!preparoEspera && tocarFonteGuardada()) { /* fonte guardada abriu */ }',
    'if (!ajustes_fonte_manual() && !preparoEspera && tocarFonteGuardada()) {\n'
    '          /* Apenas no modo automatico: no manual sempre pedir uma escolha. */\n'
    '        }',
)
# A scelta sempre richiesta va distinta dal precedente "riusa l'ultima scelta".
# Questo punto centralizzato copre Play, Continua a guardare, episodi e ripresa;
# il ramo precedente "if (player_id_canal()[0])" mantiene escluso Live TV.
replace_one(
    "src/app.c",
    'if (ajustes_fonte_manual() && stream_n() > 0 && lembrada < 0) {',
    'if (ajustes_fonte_manual() && stream_n() > 0) {',
)
replace_one(
    "src/app.c",
    '      // ISSUE #62: COM "ESCOLHER A FONTE AO REPRODUZIR" LIGADO, "RETOMAR"\n'
    '      // ABRIA A FOLHA DE NOVO. A pessoa ja tinha escolhido a fonte deste\n'
    '      // titulo na folha — e a escolha esta guardada (fontepref) e presente na\n'
    '      // lista de agora. Perguntar de novo e o que o relator chamou de "o bug\n'
    '      // antigo": o ajuste quer que a PESSOA escolha, e ela escolheu. So\n'
    '      // pergunta quando nao ha escolha lembrada que sirva para esta lista;\n'
    '      // trocar de fonte continua a um hold de distancia (menu do episodio,\n'
    '      // hold no botao primario).\n',
    '      // NUVIO STABLE: quando a escolha manual e ligada, abrir a folha em\n'
    '      // CADA pedido VOD, mesmo se houver fonte lembrada no fontepref.\n'
    '      // A preferida fica apenas destacada: NAO inicia o video sozinha.\n'
    '      // Isto cobre o botao Play e Continuar assistindo pelo mesmo caminho.\n'
    '      // O ramo anterior de canais permanece automatico (Guia TV).\n',
)
replace_one(
    "src/ajustes.h",
    '// 1 = ao mandar Reproduzir, ABRIR A FOLHA DE FONTES em vez de escolher\n'
    '// sozinho. Padrao 0: quem nunca entrou em Ajustes continua com a escolha\n'
    '// automatica de sempre.\n',
    '// 1 = a CADA pedido de reproducao VOD, inclusive Retomar/Continuar,\n'
    '// ABRIR A FOLHA DE FONTES, mesmo com uma fonte lembrada ou em cache.\n'
    '// Padrao 0: conserva a escolha automatica de sempre.\n',
)
# Rende la preferenza del profilo ufficiale immediatamente visibile, senza
# duplicare il campo o modificare indici/chavi di persistenza.
replace_one(
    "src/ajustes_ux_tela.inc",
    '    ROT("Dados do título"),\n'
    '      OPC(AJ_TMDB_LIGADO),\n'
    '    MAIS(),',
    '    ROT("Dados do título"),\n'
    '      OPC(AJ_DET_META_EXT), OPC(AJ_TMDB_LIGADO),\n'
    '    MAIS(),',
)
replace_one(
    "src/ajustes_ux_tela.inc",
    '      OPC(AJ_TMDB_TRAILERS), OPC(AJ_TMDB_MAIS), OPC(AJ_TMDB_COL), OPC(AJ_TMDB_CW),\n'
    '      OPC(AJ_DET_META_EXT), OPC(AJ_DET_SO_CINEMETA),',
    '      OPC(AJ_TMDB_TRAILERS), OPC(AJ_TMDB_MAIS), OPC(AJ_TMDB_COL), OPC(AJ_TMDB_CW),\n'
    '      OPC(AJ_DET_SO_CINEMETA),',
)
# Il toggle "preferExternalMetaAddonDetail", condiviso col profilo, deve
# rispettare gli addon anche quando la lingua dell'interfaccia non è inglese.
# Se il testo addon manca in parte, TMDB integra solo i campi mancanti.
replace_one(
    "src/descoberta.c",
    '// Resolve (com rede) titulo e sinopse localizados. Num idioma que nao e o\n'
    '// ingles, o TMDB primeiro e o addon quando ele nao tem (#209). Em ingles, a\n'
    '// ordem e a da preferencia:\n'
    '// com "Prefere a ficha do addon de metadados" o addon vem primeiro; sem ele, o\n'
    '// TMDB no idioma configurado, e o addon so quando o TMDB nao tem (ou esta\n'
    '// desligado). Em ingles e sem a preferencia nao ha nada a localizar.\n',
    '// Resolve titulo e sinopse localizados. Quando a conta prefere metadata\n'
    '// externa, o addon tem prioridade independentemente do idioma; TMDB so\n'
    '// completa os campos que faltarem. Sem essa preferencia, TMDB localizado\n'
    '// vem antes do addon (se o idioma nao for ingles).\n',
)
replace_one(
    "src/descoberta.c",
    '  // Com a preferencia o addon vem primeiro SO em ingles (#209): num idioma\n'
    '  // que nao e o ingles o TMDB traduz antes, como na ficha do titulo.\n'
    '  if (externo && !naoIng) {\n'
    '    ok = textoDoAddon(tipo, id, tit, nt, sin, ns, NULL);\n'
    '  } else {\n'
    '    ok = textoDoTmdb(tipo, id, tit, nt, sin, ns,\n'
    '                     naoIng ? logoTmdb : NULL, sizeof logoTmdb);\n'
    '    if (!tit[0] && !sin[0]) ok = textoDoAddon(tipo, id, tit, nt, sin, ns, NULL);\n'
    '  }',
    '  if (externo) {\n'
    '    ok = textoDoAddon(tipo, id, tit, nt, sin, ns, NULL);\n'
    '    if (!tit[0] || !sin[0]) {\n'
    '      char titTmdb[256] = "", sinTmdb[1600] = "";\n'
    '      int tmdb = textoDoTmdb(tipo, id, titTmdb, sizeof titTmdb,\n'
    '                            sinTmdb, sizeof sinTmdb,\n'
    '                            naoIng ? logoTmdb : NULL, sizeof logoTmdb);\n'
    '      if (!tit[0] && titTmdb[0]) snprintf(tit, nt, "%s", titTmdb);\n'
    '      if (!sin[0] && sinTmdb[0]) snprintf(sin, ns, "%s", sinTmdb);\n'
    '      if (tmdb) ok = 1;\n'
    '    }\n'
    '  } else {\n'
    '    ok = textoDoTmdb(tipo, id, tit, nt, sin, ns,\n'
    '                     naoIng ? logoTmdb : NULL, sizeof logoTmdb);\n'
    '    if (!tit[0] && !sin[0]) ok = textoDoAddon(tipo, id, tit, nt, sin, ns, NULL);\n'
    '  }',
)
