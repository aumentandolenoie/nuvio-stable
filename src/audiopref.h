// Scelta di una traccia audio: priorita assoluta alla lingua principale,
// poi a quella di riserva, infine si lascia la traccia originale del file.
// Puro, senza stato o dipendenze di piattaforma (LG / Samsung / Android).
#ifndef NV_AUDIOPREF_H
#define NV_AUDIOPREF_H
#include <string.h>

// Restituisce l'indice di una traccia con lingua dichiarata oppure -1.
// "*", "original" e preferenze vuote significano "nessuna selezione".
// Il chiamante deve rispettare la traccia scelta manualmente in precedenza.
static inline int nv_audiopref_trova(const char *const *lingue, int n,
                                     const char *principale, const char *riserva,
                                     int (*casa)(const char *, const char *),
                                     int *riserva_usata) {
  const char *preferenze[2] = { principale, riserva };
  if (riserva_usata) *riserva_usata = 0;
  if (!lingue || n < 1 || !casa) return -1;
  for (int priorita = 0; priorita < 2; priorita++) {
    const char *preferita = preferenze[priorita];
    if (!preferita || !*preferita || !strcmp(preferita, "*")) continue;
    for (int i = 0; i < n; i++) {
      if (!lingue[i] || !*lingue[i]) continue; // lingua sconosciuta mai presunta
      if (casa(lingue[i], preferita)) {
        if (riserva_usata) *riserva_usata = priorita == 1;
        return i;
      }
    }
  }
  return -1;
}
#endif
