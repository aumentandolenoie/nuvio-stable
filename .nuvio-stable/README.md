# Patch Nuvio Stable (webOS nativo)

**Base bloccata**: https://github.com/iqui27/nuvio-native-legacy, commit
\`e3e21a590120ca283bcf7a96df1813ff5041eb66\` (15 ottobre 2026).

La pipeline \`.github/workflows/bootstrap.yml\` scarica lo snapshot e copia nel
repository tutte le sorgenti, tranne la cartella \`.git\` del progetto originale
e i workflow upstream (la nostra pipeline rimane quindi indipendente).
Esegue \`python3 .nuvio-stable/apply.py\`, verifica i contratti col test
\`python3 .nuvio-stable/test_contract.py\` e fa il commit su \`main\` con
\`GITHUB_TOKEN\`. Richiede GitHub Actions attivo e permesso di scrittura sui
contenuti (dichiarato nel job). Può essere rilanciata manualmente.

## Modifiche

1. **Preferenze del profilo**: non sostituiamo il motore Legacy già esistente.
   \`src/sync.c\` scarica e riallinea \`settings_json\` del profilo tramite le
   RPC \`sync_pull_profile_settings_blob\` / \`sync_push_profile_settings_blob\`;
   \`src/ajustes.c\` associa le chiavi compatibili con la web app ufficiale.
   Le opzioni specifiche di player/UI webOS, inclusa l'apertura manuale del
   selettore fonti, restano **locali**. Non è possibile sincronizzare
   automaticamente opzioni che Nuvio ufficiale non conserva sul profilo.
   La disposizione esistente delle impostazioni viene mantenuta per non
   alterare gli indici e le chiavi dei dati salvati.
2. **Metadati**: \`preferExternalMetaAddonDetail\` è già un'impostazione
   sincronizzata. La relativa riga viene mostrata senza aprire «Altre opzioni».
   Con la preferenza attiva la ricerca del testo tenta l'addon per primo
   anche in italiano, poi usa TMDB soltanto per i campi mancanti.
   Il comportamento dipende da quali metadati gli addon effettivamente
   restituiscono.
3. **Fonti**: se «Scegliere la fonte alla riproduzione» è attivo, per i VOD
   viene aperta la lista a ogni richiesta (pulsante Riproduci, ripresa dal
   dettaglio, scheda Continua a guardare). Una fonte ricordata resta
   evidenziata ma non salta più il selettore; nemmeno il collegamento
   conservato in cache può avviare direttamente il film. Il ramo di
   riproduzione dei canali dalla guida resta invariato.

## Verifiche

- \`python3 .nuvio-stable/test_contract.py\`: verifica i percorsi principali.
- Suite nativa upstream: \`bash tests/ajustes_secoes.sh\`,
  \`bash tests/ajustes_perfil.sh\`, \`bash tests/metaprov.sh\`
  (richiedono le dipendenze di compilazione upstream, da eseguire in CI o su
  un ambiente Linux preparato).
- Test indispensabile su LG webOS: avvio di un film con e senza preferenza,
  secondo avvio dello stesso film, ripresa da Continua a guardare, serie
  TV ed episodi, cambio profilo, confronto metadati esterni e guida TV.

Il test di contratto è statico: non sostituisce una compilazione C né una
prova sul televisore. Eventuali errori della pipeline bloccano il commit.

Questa fork conserva la **GPL-3.0** del progetto upstream.
