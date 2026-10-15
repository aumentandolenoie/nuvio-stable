// Link this against src/cwfonte6h.c: fake storage, clock and identity.
// No video, network, TV or authenticated session needed.
#include "../src/cwfonte6h.h"
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int profilo = 1;
static const char *utente = "user-A";
static char archivio[20000];
int perfis_ativo(void) { return profilo; }
const char *sessao_usuario(void) { return utente; }
char *dados_ler(const char *name) {
  assert(strcmp(name, "cw-fonte-inicios.txt") == 0);
  if (!archivio[0]) return NULL;
  char *s = malloc(strlen(archivio)+1);
  assert(s);
  strcpy(s, archivio);
  return s;
}
int dados_gravar(const char *name, const char *content) {
  assert(strcmp(name, "cw-fonte-inicios.txt") == 0);
  assert(strlen(content) < sizeof archivio);
  strcpy(archivio, content);
  return 1;
}
void prog_chave(char *out, unsigned n, const char *id, int t, int e) {
  if (e > 0) snprintf(out,n,"%s_s%de%d",id,t,e);
  else snprintf(out,n,"%s",id);
}
int main(void) {
  long long now = 1792095000;
  assert(!cwfonte6h_recente("tt-film",0,0,now));
  assert(cwfonte6h_registrar("tt-film",0,0,now));
  assert(cwfonte6h_recente("tt-film",0,0,now));
  assert(cwfonte6h_recente("tt-film",0,0,now+CWFONTE6H_SEGUNDOS-1));
  assert(!cwfonte6h_recente("tt-film",0,0,now+CWFONTE6H_SEGUNDOS));
  assert(!cwfonte6h_recente("tt-film",0,0,now-1));
  assert(!cwfonte6h_recente("tt-other",0,0,now));
  assert(cwfonte6h_registrar("tt-serie",2,3,now));
  assert(cwfonte6h_recente("tt-serie",2,3,now+300));
  assert(!cwfonte6h_recente("tt-serie",2,4,now+300));
  assert(!cwfonte6h_recente("tt-serie",1,3,now+300));
  profilo=2;
  assert(!cwfonte6h_recente("tt-serie",2,3,now));
  profilo=1; utente="user-B";
  assert(!cwfonte6h_recente("tt-serie",2,3,now));
  utente="user-A";
  assert(cwfonte6h_recente("tt-serie",2,3,now+200));
  // A failed source never calls register; old observations cannot stay recent.
  assert(!cwfonte6h_recente("tt-serie",2,3,now+CWFONTE6H_SEGUNDOS+20));
  assert(cwfonte6h_registrar("tt-serie",2,3,now+CWFONTE6H_SEGUNDOS+20));
  assert(cwfonte6h_recente("tt-serie",2,3,now+CWFONTE6H_SEGUNDOS+20));
  printf("PASS: six-hour expiry, movie/episode separation, profile/account isolation and restart persistence\n");
  return 0;
}
