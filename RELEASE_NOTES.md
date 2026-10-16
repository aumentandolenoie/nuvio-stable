# Nuvio Stable — note di rilascio

Le note descrivono le differenze della singola versione rispetto alla precedente. Le versioni storiche sono state ricostruite dai commit pubblicati; non implicano prove manuali su TV quando non documentate.

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
