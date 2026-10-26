# Fire OS / Fire TV Stick — preparazione sperimentale

Questa piattaforma usa il progetto Android nativo già presente nel repository; non usa i pacchetti webOS `.ipk` o Tizen `.tpk`.

## Stato verificato dal codice
- `android/app/src/main/AndroidManifest.xml`: launcher TV (LEANBACK), rete, OpenGL ES 2.0, touchscreen non richiesto.
- `android/app/build.gradle.kts`: Android minSdk 24, ABI arm64-v8a e armeabi-v7a; Media3 / ExoPlayer e FFmpeg.
- `tools/android.sh`: build debug e release firmata opzionale; controlli su librerie, asset, credenziali e compatibilità pagine native.
- La presenza del codice non dimostra la compatibilità effettiva con ogni modello Fire OS.

## Precondizioni prima di produrre APK installabili
1. Test automatici della configurazione di base: `tools/env.sh --require-core`, verificando che nessun segreto personale finisca nel pacchetto.
2. Ambiente Android con JDK 17, Android SDK 35, NDK 27.2.12479018, CMake 3.22.1.
3. Dependences native libcurl per **entrambe** le ABI in `~/.cache/nuvio-android/prefix/<abi>/lib/libcurl.so`. Non usare `NUVIO_SEM_CURL=1` per una release: potrebbe compromettere immagini e richieste.
4. Preparazione FFmpeg, SDL2 e motore P2P tramite gli script già esistenti, senza introdurre versioni alternative non verificate.
5. Firma release Android persistente e protetta: `NUVIO_KEYSTORE`, `NUVIO_KEYSTORE_PASS`, `NUVIO_KEY_ALIAS`, `NUVIO_KEY_PASS`. **Non pubblicare un debug come release.**
6. `bash tools/android.sh` e verifica dell'APK tramite il controllo finale già incluso nello script.
7. Installazione di prova su una Fire TV Stick Fire OS; verificare launcher, navigazione D-pad, login, cataloghi, guida TV, proxy addon, HLS, ripresa, DTS/FFmpeg, sottotitoli, cambi fonte e uscita dal player.

## Politica di pubblicazione
- Non modificare i workflow di LG o Samsung per abilitare Android.
- Non aggiungere automaticamente un APK nelle release pubbliche prima di un test su Fire OS.
- Una futura build firmata dovrebbe produrre `Nuvio-<version>-android.apk` insieme agli artifact esistenti **solo** dopo i controlli di integrità e firma, mantenendo una versione comune.
- Non modificare l'applicationId `space.nuvio.nativelegacy` dopo l'installazione, per mantenere l'aggiornabilità.

## Aggiornamenti direttamente dalla Fire TV Stick (APK sideload)
Il codice Android ha già un updater integrato (`src/atualizacao.c` + `NuvioActivity.instalarApk`):
- verifica le release GitHub del repository, cerca soltanto un asset che termina con `-android.apk`;
- scarica l'APK e ne controlla l'hash SHA-256 dichiarato nella release; in caso di differenza non lo installa;
- consegna l'APK all'installer Fire OS mediante un `FileProvider` limitato a `dados/atualizacao/`;
- su Fire OS 8/Android 8+ può richiedere inizialmente il permesso di installare app da questa fonte, e ogni aggiornamento richiede la conferma dell'installer di sistema.

**Contratto irrinunciabile per gli aggiornamenti:** stessa `applicationId` e stessa firma di release dell'APK iniziale. `tools/release-android.sh` verifica esplicitamente l'impronta del certificato con `apksigner`; NON distribuire né usare come prima installazione un APK di debug, né rigenerare la keystore di release. Aggiungere ogni futuro APK firmato come `Nuvio-<versione>-android.apk` alla stessa release GitHub già usata dagli altri target, con relativo digest. Conservare in modo sicuro keystore e credenziali: non committarle e non stamparle nei log.

Il sistema è **verificato a livello di sorgenti, non ancora su Fire OS reale**. Per il test del primo aggiornamento servono due APK consecutivi firmati con la stessa chiave e una Fire TV Stick: installazione da APK, verifica della versione nuova, conferma del prompt di permesso, conferma installazione, preservazione dei dati e riavvio. Non abilitare la pubblicazione automatica finché non è superato.
