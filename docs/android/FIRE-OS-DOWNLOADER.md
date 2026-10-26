# Installazione di Nuvio Stable su Amazon Fire TV (Fire OS)

**Stato:** la procedura è pronta, ma non usare il link qui sotto finché la release non contiene un APK Android di produzione firmato e verificato. Una pagina GitHub Releases non garantisce che sia disponibile un file Android.

## Downloader: prima installazione

1. Installa **Downloader (AFTVnews)** dall'Amazon Appstore.
2. Su Fire TV vai in **Impostazioni → La mia Fire TV → Opzioni sviluppatore → Installa app sconosciute** e autorizza **Downloader**. Se la sezione sviluppatore non compare, apri **La mia Fire TV → Informazioni**, seleziona il nome del dispositivo e premi **Seleziona** sette volte. I nomi possono variare a seconda di Fire OS.
3. Solo dopo la pubblicazione di una release Android firmata, apri Downloader e inserisci:
   `https://github.com/aumentandolenoie/nuvio-stable/releases/latest/download/Nuvio-VERSIONE-android.apk`
   Sostituisci VERSIONE con il numero riportato nel file della release (per esempio `2.0.41`, **solo se quell'asset esiste davvero**).
4. Completa la richiesta di installazione di Fire OS e apri Nuvio.

Evita link abbreviati non controllati: una nuova release potrebbe non contenere l'APK e generare errore 404. Non pubblicare un URL Downloader come pronto se il relativo artifact non è già presente.

## Aggiornamento successivo (senza Downloader)

Nuvio Android cerca l'asset `Nuvio-<versione>-android.apk` nella release GitHub latest, scarica il file, ne controlla l'SHA-256 e lo consegna all'installer di Fire OS tramite FileProvider. Il primo aggiornamento può richiedere di autorizzare **Nuvio** (non Downloader) sotto **Installa app sconosciute**. Il sistema richiederà comunque la conferma dell'installazione.

### Vincoli che non si possono violare

- Stesso `applicationId` Android `space.nuvio.nativelegacy` e **stessa chiave di release** per tutte le versioni. Mai installare una debug build come versione iniziale se si vogliono gli aggiornamenti release.
- Verificare con `tools/release-android.sh` il certificato atteso; custodire la keystore fuori da Git e GitHub Actions logs.
- Non pubblicare finché l'APK non contiene le librerie native richieste per entrambe le ABI, supera i controlli già esistenti e funziona su un dispositivo Fire OS reale.
- L'installazione da Downloader e gli aggiornamenti in-app non sono ancora stati validati su Fire OS reale. L'updater apre l'installer di sistema: non è un aggiornamento silenzioso.
