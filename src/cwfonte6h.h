// Regra de 6 horas para "Continuar assistindo" do Nuvio Stable.
// So um inicio REAL de video (>= 2 s tocados) arma o atalho;
// filmes e episodios tem chaves diferentes, por conta e por perfil.
#ifndef NV_CWFONTE6H_H
#define NV_CWFONTE6H_H
#define CWFONTE6H_SEGUNDOS (6LL * 60LL * 60LL)
// Identidade: id da obra (imdb/tmdb/kitsu etc), temporada e episodio.
// agoraSeg: time(NULL). Uma marca futura/sem relogio e recusada.
int cwfonte6h_recente(const char *id, int temporada, int episodio, long long agoraSeg);
// Registra somente depois da fonte provar que reproduziu (nao no clique/erro).
int cwfonte6h_registrar(const char *id, int temporada, int episodio, long long agoraSeg);
#endif
