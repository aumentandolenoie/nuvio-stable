// Risolutore sperimentale dei trailer TMDB/YouTube nel lettore nativo webOS.
// Non avvia applicazioni esterne e non blocca mai il thread grafico.
#ifndef NV_TRAILERYT_H
#define NV_TRAILERYT_H
#include <stddef.h>
// 1=URL pronto; 0=in caricamento; -1=nessun flusso diretto disponibile.
// Solo ID YouTube validi; l'URL restituito ha durata limitata.
int traileryt_obter(const char *youtube_id, char *url, size_t url_cap);
#endif
