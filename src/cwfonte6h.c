#include "cwfonte6h.h"
#include "dados.h"
#include "perfis.h"
#include "progresso.h"
#include "sessao.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

// Local, nao sincronizado: lastWatchedMs do progresso pode vir da nuvem e
// indica a ULTIMA POSICAO salva, nao a hora do INICIO neste aparelho.
// Nao guardar URLs nem tokens nem identidade de conta em claro.
#define CW6_ARQ "cw-fonte-inicios.txt"
#define CW6_MAX 80
typedef struct {
  char conta[17]; // FNV-1a de sessao_usuario(), nao o identificador em claro
  int perfil;
  char chave[48]; // prog_chave: filme ttX, episodio ttX_s2e3
  long long inicio;
} Cw6Entrada;

static void contaChave(char saida[17]) {
  uint64_t h = UINT64_C(14695981039346656037);
  const unsigned char *p = (const unsigned char *)sessao_usuario();
  if (!p || !*p) { saida[0] = 0; return; }
  while (*p) { h ^= *p++; h *= UINT64_C(1099511628211); }
  snprintf(saida, 17, "%016llx", (unsigned long long)h);
}

static int preparar(const char *id, int t, int e,
                    char conta[17], char chave[48]) {
  if (!id || !*id) return 0;
  contaChave(conta);
  if (!conta[0]) return 0;
  prog_chave(chave, 48, id, t, e);
  return chave[0] != 0;
}

static int dentro(long long inicio, long long agora) {
  // No limite exato das seis ore torna obrigatoria a scelta.
  return inicio > 0 && agora >= inicio && agora - inicio < CWFONTE6H_SEGUNDOS;
}

static int ler(Cw6Entrada *destino, int max) {
  char *buf = dados_ler(CW6_ARQ), *linha, *ctx;
  int n = 0;
  if (!buf) return 0;
  for (linha = strtok_r(buf, "\n", &ctx); linha && n < max;
       linha = strtok_r(NULL, "\n", &ctx)) {
    Cw6Entrada r;
    char extra;
    if (sscanf(linha, "%16[0-9a-f]\t%d\t%47[^\t]\t%lld%c",
               r.conta, &r.perfil, r.chave, &r.inicio, &extra) != 4) continue;
    if (strlen(r.conta) != 16 || r.inicio <= 0 || r.perfil < 0) continue;
    destino[n++] = r;
  }
  free(buf);
  return n;
}

int cwfonte6h_recente(const char *id, int t, int e, long long agora) {
  Cw6Entrada r[CW6_MAX];
  char conta[17], chave[48];
  int n, i, perfil;
  if (!preparar(id, t, e, conta, chave) || agora <= 0) return 0;
  perfil = perfis_ativo();
  n = ler(r, CW6_MAX);
  for (i = 0; i < n; i++) {
    if (r[i].perfil == perfil && !strcmp(r[i].conta, conta) &&
        !strcmp(r[i].chave, chave) && dentro(r[i].inicio, agora))
      return 1;
  }
  return 0;
}

int cwfonte6h_registrar(const char *id, int t, int e, long long agora) {
  Cw6Entrada r[CW6_MAX], novo;
  char texto[CW6_MAX * 100 + 32], *p = texto;
  int n, i, total = 0, perfil;
  size_t rest = sizeof texto;
  if (!preparar(id, t, e, novo.conta, novo.chave) || agora <= 0) return 0;
  perfil = perfis_ativo();
  novo.perfil = perfil;
  novo.inicio = agora;
  n = ler(r, CW6_MAX);
  // Remover marcas vencidas e duplicatas. Manter as 79 mais recentes
  // entre todos os perfis; o registro nuovo prende sempre posto.
  for (i = 0; i < n; i++) {
    if (!dentro(r[i].inicio, agora)) continue;
    if (r[i].perfil == perfil && !strcmp(r[i].conta, novo.conta) &&
        !strcmp(r[i].chave, novo.chave)) continue;
    r[total++] = r[i];
  }
  if (total >= CW6_MAX) {
    int velho = 0;
    for (i = 1; i < total; i++)
      if (r[i].inicio < r[velho].inicio) velho = i;
    r[velho] = r[--total];
  }
  r[total++] = novo;
  for (i = 0; i < total; i++) {
    int k = snprintf(p, rest, "%s\t%d\t%s\t%lld\n",
                     r[i].conta, r[i].perfil, r[i].chave, r[i].inicio);
    if (k < 0 || (size_t)k >= rest) return 0;
    p += k; rest -= (size_t)k;
  }
  return dados_gravar(CW6_ARQ, texto);
}
