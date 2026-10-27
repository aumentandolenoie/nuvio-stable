# Fire TV Stick 2ª generazione — esperimento API 22

Amazon identifica Fire TV Stick 2nd Gen come AFTT: Fire OS 5, Android 5.1/API 22, solo ARM 32 bit, 1 GB RAM.

La build Android standard di Nuvio ha minSdk 24. La proprietà Gradle `-Pnuvio.fireOs5=true` consente **soltanto in una build sperimentale** di impostare minSdk 22, senza cambiare il requisito predefinito. Non è un certificato di compatibilità: i manifest delle dipendenze, il codice Media3, FFmpeg e le API native devono ancora passare una compilazione reale e una prova sul dispositivo.

Esempio di argomento Gradle quando l'ambiente Android e le librerie native sono predisposti: `-Pnuvio.fireOs5=true`. Lo script `tools/android.sh` non espone ancora questa proprietà: non pubblicare un APK dichiarato Fire OS 5 usando semplicemente la build standard.

Verifiche obbligatorie prima di una prima installazione tramite Downloader:
- Gradle deve risolvere dipendenze con minSdk <= 22 (senza forzare `tools:overrideLibrary`).
- APK firmato con la keystore Android già prevista, stesso applicationId e firma per gli aggiornamenti successivi.
- Controllo sulle librerie `armeabi-v7a`, login, memoria durante guida TV, navigazione col telecomando, HLS, player e sottotitoli.
- Test di aggiornamento dall'app, con consenso tramite l'installer Fire OS.

Non pubblicare questa variante in `releases/latest` né sostituire gli artifact LG/Samsung fino a esito positivo.

## Media3 1.8.0: compatibilità ancora da confermare

**Correzione della valutazione precedente:** l'aumento del minimo ufficiale di Media3 a API 23 avviene dalla versione 1.9.0 (release notes ufficiali: https://developer.android.com/jetpack/androidx/releases/media3). La nostra fork usa ancora Media3 **1.8.0**. Pertanto non è corretto affermare che la libreria attuale sia già incompatibile con API 22.

Occorre compilare l'intero grafo delle dipendenze con minSdk 22, senza forzare manifest override, e poi effettuare test reali di playback sulla Fire Stick. Soltanto se la build fallisce o il player non riproduce correttamente HLS/VOD si valuta un backend alternativo.

## Aggiornamenti in-app: canale da separare

L'updater Android corrente cerca la release latest e l'asset `-android.apk` standard (API 24). La variante Fire OS 5 non deve scaricarlo automaticamente. Prima della distribuzione occorre aggiungere un asset Fire OS 5 dedicato, selezionarlo nella logica di aggiornamento della variante e verificare l'installazione con la stessa firma. Il semplice nome diverso dell'APK sperimentale non risolve da solo il problema.
