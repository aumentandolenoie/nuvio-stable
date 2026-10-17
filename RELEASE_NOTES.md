# Nuvio Stable — note di rilascio

Le note descrivono le differenze della singola versione rispetto alla precedente. Le versioni storiche sono state ricostruite dai commit pubblicati; non implicano prove manuali su TV quando non documentate.

## 2.0.24 — Diagnostica sincronizzazione visti

### Novità
- Log di sola lettura delle pagine della cronologia account Nuvio, dei film, delle serie e degli episodi ricevuti.
- Diagnostica mirata ai film Jojo Rabbit e Veloce come il vento: corrispondenza tra identificativi della libreria e della cronologia e stato del catalogo.
- Nessuna modifica ai dati remoti, alle marcature viste o ai meccanismi di sincronizzazione.

### Verifiche
- Compilazione e controlli automatizzati via GitHub Actions; confronto effettivo su TV ancora necessario.

## 2.0.23 — Badge delle fonti con formatter addon

### Correzioni
- Quando e attiva la descrizione fornita dall'addon (per esempio AIOStreams), la riga della fonte mostra anche i badge del pacchetto o quelli integrati.
- Testo, icone, ordine delle informazioni e comportamento del formatter addon restano invariati; la riga si adatta all'altezza dei badge.
- Nessuna modifica alla selezione delle fonti o al player video/audio.

### Verifiche
- Contratti automatici e compilazione nel workflow; conferma grafica su TV ancora necessaria.

## 2.0.22 — Diagnostica riutilizzo URL video

### Novità
- La schermata errore indica se l'indirizzo passato al player è identico, diverso o il primo osservato rispetto all'apertura precedente nella stessa sessione Nuvio.
- Il confronto usa una firma volatile soltanto in memoria: non mostra URL, token o credenziali e non introduce richieste di rete.
- Il confronto non prova che l'addon abbia rigenerato una fonte, né verifica validità o risposta HTTP.

### Verifiche
- Test automatici e compilazione attraverso GitHub Actions; verifica sul televisore ancora necessaria.

## 2.0.21 — Diagnostica della fase di apertura

### Novità
- Errore di apertura: fase del player LG, eventuale precedente tentativo DTS, ritorno nativo e numero di retry della riconnessione.
- Lo stato HTTP viene dichiarato ignoto quando il backend LG non fornisce un codice HTTP. Il codice 300 resta identificato correttamente come errore del player, non come risposta HTTP.
- Nessuna richiesta di rete aggiuntiva e nessuna modifica alle procedure di apertura, conversione DTS, selezione audio o recupero.

### Verifiche
- Controlli di compilazione e contratti tramite workflow; conferma reale su TV ancora necessaria.

## 2.0.20 — Diagnostica errori e cambio audio

### Novità
- Messaggio di errore fonte con codice del player, stato DTS, disponibilità del video e indice audio.
- Traccia diagnostica della richiesta di cambio audio (codec, indice e posizione), senza registrare URL o credenziali.
- Nessuna modifica al funzionamento del decoder, alla conversione DTS o alla strategia di rete.

### Verifiche
- Verifiche statiche dei percorsi; test su LG reale necessari per riprodurre e diagnosticare l'errore 300 e la traccia inglese.

## 2.0.19 — Diagnostica di apertura delle fonti

### Novità
- Il riquadro di errore delle fonti mostra il dettaglio tecnico del player, quando disponibile, oppure indica che il backend non ha restituito un codice.
- Nessun cambiamento a conversione DTS→AAC, decoder, fonti o timeout.

### Verifiche
- Controllo statico della modifica; riproduzione reale su LG da verificare.

## 2.0.18 — Episodi, tracce audio e sottotitoli per lingua

### Novità
- **Serie TV:** all'apertura della scheda, stagione e carosello degli episodi vengono posizionati sull'episodio da riprendere oppure sul successivo, in base ai progressi di **Nuvio Sync**. La navigazione manuale ha sempre precedenza.
- **Menu audio:** le tracce DTS e TrueHD che risultano presenti nel MKV ma non sono offerte dal decoder LG vengono mostrate in grigio con l'avviso «Fonte audio non compatibile». Non si possono selezionare come tracce native.
- **Sottotitoli:** prima si sceglie la lingua, poi una delle tracce disponibili in quella lingua; il tasto Indietro torna all'elenco delle lingue. Restano disponibili la gestione primaria/secondaria, lo stile e AutoSync.
- **Conversione DTS→AAC:** riconoscimento della traccia DTS nel file MKV anche quando LG espone soltanto un'altra traccia compatibile. La scelta è vincolata alle preferenze audio e al flag predefinito del MKV, con verifica di unicità e identificazione dell'indice originale tramite demultiplexer.
- **DTS-ES:** il confronto delle tracce non rifiuta più una traccia identificata univocamente per una discrepanza tra 6 e 7 canali segnalati dai diversi decoder. Preservata la possibilità di conversione con video Dolby Vision Profile 8.1.
- **Prestazioni e sicurezza:** il percorso informativo riutilizza la sonda MKV già presente senza ulteriori download; gli indici nativi non sono alterati e il motore DTS→AAC non è stato ricodificato.

### Verifiche
- Controlli dei contratti UI e DTS, compilazione nativa LG webOS ARMv7, verifica del pacchetto IPK e manifest Homebrew tramite GitHub Actions.
- **Da confermare su TV reale:** conversione e sincronizzazione del DTS-ES italiano di *WALL·E* (offset audio sorgente di 800 ms), oltre alla visualizzazione delle nuove interfacce. Il test automatico non sostituisce la riproduzione sul televisore.

## 2.0.17 — Riproduzione delle serie e Nuvio Sync

### Correzioni
- **Riproduci nella pagina di una serie:** dopo aver completato un episodio, apre quello successivo in base agli episodi visti su **Nuvio Sync** e al completamento locale. Esempio: *The Office* T2E12 → T2E13, anziché T1E1.
- La ripresa di un episodio **interrotto a metà** conserva l'episodio e la posizione precedenti; le scelte esplicite di un episodio restano prioritarie.
- All'apertura di una serie già vista, il pulsante aspetta brevemente i metadati degli episodi anziché cercare subito le fonti della prima puntata. Nessuna attesa aggiuntiva per la ripresa parziale o l'avvio esplicito da «Continua a guardare».
- Eliminazione delle **fonti residue dell'episodio precedente** nel passaggio «Episodio successivo» e quando il dettaglio passa a un altro episodio; le fonti precaricate corrette restano riutilizzabili.
- Sincronizzazione della schermata degli episodi completati: il prossimo episodio può essere ricavato dal completamento locale verificato, anche prima del successivo aggiornamento da Nuvio Sync.
- «**Continua a guardare**»: ordinamento per **ultima attività effettiva di visione** in tutte e tre le modalità, includendo le serie il cui prossimo episodio è ancora allo 0%.
- Selezione del prossimo episodio: gestione del cambio di stagione, puntate già viste o duplicate e puntate non ancora trasmesse. Un semplice salto al 100% non equivale a un episodio visto.

### Verifiche
- Test di progressi e visti Nuvio Sync, selezione episodio e priorità temporali; controllo dei contratti esistenti.
- Compilazione ARMv7 e creazione del pacchetto LG webOS verificati dal workflow automatico.
- **La prova su TV reale resta distinta dai test automatici.**

## 2.0.16 — Affidabilità DTS e controlli del player

- Conversione **DTS → AAC**: singolo tentativo aggiuntivo controllato per alcuni errori HTTP Range temporanei, senza creare thread o attese prolungate.
- Rispetto delle risposte HTTP **429** e delle esclusioni per errori permanenti.
- Annullamento di una richiesta pendente di trailer TMDb a schermo intero quando cambia il titolo.
- Ampliati i test di riproduzione DTS, sincronizzazione automatica dei sottotitoli e controllo delle regressioni.

## 2.0.15 — Riproducibilità dei trailer TMDb

- Risoluzione dei trailer da YouTube con tentativi sui client Android e iOS, evitando il client Android VR noto per gli errori HTTP 403.
- Verifica degli URL CDN firmati e del relativo stato HTTP prima della riproduzione.
- Avvisi per i trailer più compatti e leggibili sull'interfaccia LG webOS; indicazione del caricamento durante la verifica.
- Test di accessibilità CDN, fallback fra client e rifiuto di risposte HTTP 403 e host non validi.

## 2.0.14 — Lingua reale dei trailer TMDb

- Conservazione della lingua dichiarata per ogni video TMDb, distinta dalla lingua del titolo tradotto.
- Visualizzazione della lingua del trailer selezionato e di eventuali errori di riproduzione.
- Rimossa la sostituzione silenziosa con trailer Apple/IMDb in inglese quando la sorgente TMDb scelta non è riproducibile.

## 2.0.13 — Sorgente sperimentale trailer TMDb

- Aggiunta un'opzione per i **trailer TMDb nel player nativo LG**.
- Risoluzione asincrona dei video YouTube in flussi multimediali diretti, con convalida degli URL.
- Gestione dell'attesa per la riproduzione a schermo intero e protezioni sui flussi non validi.
- Aggiunti test specifici del resolver e build di verifica nelle pull request.

## 2.0.12 — Navigazione e preferenze TMDb

- Ricerca: riduzione della larghezza delle locandine e correzione dello spostamento orizzontale di un solo elemento.
- Eliminazione della vecchia navigazione a triplo passo con il telecomando.
- Preferenza della lingua dei trailer TMDb configurata dall'utente e rispetto delle opzioni di arricchimento dei metadati.
- Riutilizzo delle librerie P2P ARMv7 compilate nel workflow per ridurre le ricompilazioni inutili.

## 2.0.11 — Nuova interfaccia di ricerca TV

- Tastiera TV nativa integrata nella ricerca.
- Campo di ricerca centrato e risultati degli addon con locandine più grandi e layout esteso.
- Allineamento delle versioni dei manifest per il pacchetto webOS.

## 2.0.10 — Correzione tastiera QWERTY

- Tastiera con righe QWERTY effettive da 10/9/7 tasti e corrispondenza corretta tra focus e carattere selezionato.
- Migliorato il riutilizzo dei livelli SDK ARM per le build e il controllo preventivo delle versioni dei manifest.

## 2.0.9 — Ricerca tramite addon e lingua audio

- Corrette le etichette delle lingue audio di riserva nel selettore.
- Ricerca TV con tastiera QWERTY e risultati provenienti dagli **addon**, eliminando i risultati mischiati del catalogo integrato e i suggerimenti popolari non richiesti.
- Allineata la versione dichiarata nel manifest Tizen.

## 2.0.8 — Traduzioni e documentazione

- Completamento e allineamento dei cataloghi linguistici per la seconda preferenza audio.
- Aggiornamento della documentazione Homebrew.
- Verifica unificata delle traduzioni nel workflow di pubblicazione.

## 2.0.7 — Seconda lingua audio preferita

- Nuova lingua audio secondaria configurabile per profilo.
- Priorità di selezione: **lingua principale → lingua di riserva → traccia predefinita del file**.
- Applicazione coerente delle preferenze audio sui player supportati; nuove traduzioni e controlli di regressione.

## 2.0.6 — Scelta delle fonti e riproduzioni recenti

- In «Continua a guardare» il selettore delle fonti appare **prima del player** quando la scelta manuale è attiva.
- Eccezione di **6 ore** solo per lo stesso film o episodio effettivamente avviato su quel profilo e dispositivo.
- I clip di avviso dei servizi debrid non contano come riproduzioni valide per l'eccezione.
- Evitata la visualizzazione delle fonti appartenenti all'episodio precedente; test del comportamento per film, episodi e profili.

## 2.0.5 — Stabilità della build

- Adeguamento del workflow per non bloccare il pacchetto Stable con un test upstream non più applicabile a opzioni dell'interfaccia volutamente nascoste.
- Base Stable per LG webOS con identità applicativa separata dalla versione Legacy.
