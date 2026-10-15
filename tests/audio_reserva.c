#include "../src/audiopref.h"
#include "../src/linguas.h"
#include <assert.h>
#include <stdio.h>
#include <string.h>

static int scegli(const char *const *tracce, int n, int *riserva) {
  return nv_audiopref_trova(tracce, n, ling_audio(), ling_audio2(), ling_casa, riserva);
}

int main(void) {
  int seconda = -1;
  const char *misto[] = { "eng", "jpn", "ita", "spa" };
  const char *senzaItaliano[] = { "eng", "jpn", "spa" };
  const char *soloSconosciuto[] = { "", "und", "" };
  const char *dueItaliani[] = { "eng", "ita", "it" };

  ling_conta_audio("en");
  ling_local_audio("it");
  ling_local_audio2("es");
  assert(!strcmp(ling_audio(), "it"));
  assert(!strcmp(ling_audio2(), "es"));
  // La prima lingua ha priorita' anche se compare dopo quella di riserva.
  assert(scegli(misto, 4, &seconda) == 2 && seconda == 0);
  assert(scegli(dueItaliani, 3, &seconda) == 1 && seconda == 0);
  // Solo in assenza della prima viene scelta la seconda.
  assert(scegli(senzaItaliano, 3, &seconda) == 2 && seconda == 1);
  // Assenza di entrambe: lascia la traccia nativa (indice -1).
  assert(scegli(soloSconosciuto, 3, &seconda) == -1 && seconda == 0);
  // La lingua ISO del container puo' essere a 3 lettere (ita/eng/spa).
  ling_local_audio("en"); ling_local_audio2("it");
  assert(scegli(misto, 4, &seconda) == 0 && seconda == 0);
  ling_local_audio("*"); // principale "Tutte": la riserva puo' ancora decidere
  assert(scegli(misto, 4, &seconda) == 2 && seconda == 1);
  ling_local_audio2("*"); // scelta predefinita "Nenhuma"
  assert(scegli(misto, 4, &seconda) == -1 && seconda == 0);
  // Le lingue della account restano inalterate e la preferenza primaria
  // gia' impostata continua ad avere precedenza.
  ling_local_audio("");
  assert(!strcmp(ling_audio(), "en"));
  assert(!strcmp(ling_audio2(), ""));
  assert(scegli(misto, 4, &seconda) == 0 && seconda == 0);
  ling_local_audio2("~"); ling_definir_original("ja");
  assert(!strcmp(ling_audio2(), "ja"));
  ling_definir_original(""); assert(!strcmp(ling_audio2(), ""));
  puts("PASS: audio primary -> backup -> file default, ISO aliases, original, disabled & account preference");
  return 0;
}
