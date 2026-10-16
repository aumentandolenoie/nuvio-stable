// TMDB restituisce ID di YouTube, non URL MP4. Il player nativo LG
// puo' ricevere una URL HTTPS di un formato progressivo (audio+video).
// Questo risolutore e' volutamente sperimentale: YouTube puo' rispondere 403,
// richiedere token di origine o fornire soltanto formati SABR. In quel caso
// la fonte TMDB mostra un errore e non ripiega silenziosamente su Apple/IMDb.
// Nessuna dipendenza da browser, applicazioni esterne o servizi di terze parti.
#include "traileryt.h"
#include "rede.h"
#include "js.h"
#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#define YT_URL_CAP 4096
#define YT_WAIT_FAILURE 90
#define YT_WAIT_SUCCESS 1200

static pthread_mutex_t ytMutex = PTHREAD_MUTEX_INITIALIZER;
static pthread_cond_t ytCond = PTHREAD_COND_INITIALIZER;
static pthread_t ytThread;
static int ytThreadCreated, ytState; // 0 attesa, 1 pronto, -1 fallito
static unsigned ytRequest, ytProcessed;
static char ytWanted[16], ytResolved[YT_URL_CAP];
static time_t ytFinishedAt;

static int valido(const char *s) {
  int i;
  if (!s || strlen(s) != 11) return 0;
  for (i = 0; i < 11; ++i)
    if (!((s[i] >= 'A' && s[i] <= 'Z') ||
          (s[i] >= 'a' && s[i] <= 'z') ||
          (s[i] >= '0' && s[i] <= '9') || s[i] == '_' || s[i] == '-'))
      return 0;
  return 1;
}

// Accetta soltanto host Googlevideo reali e HTTPS: le risposte remote
// non possono indurre la TV a richiedere URL arbitrarie nella LAN.
static int googleVideoHost(const char *s) {
  const char *host, *fine;
  size_t n, suffix = strlen(".googlevideo.com");
  if (!s || strncmp(s, "https://", 8)) return 0;
  host = s + 8;
  fine = strchr(host, '/');
  if (!fine) return 0;
  n = (size_t)(fine - host);
  if (!n || n > 200 || memchr(host, ':', n) || memchr(host, '@', n)) return 0;
  if (n == strlen("googlevideo.com") && !strncmp(host, "googlevideo.com", n)) return 1;
  return n > suffix && !strncmp(fine - suffix, ".googlevideo.com", suffix);
}
static int mediaUrl(const char *s) {
  return googleVideoHost(s) && strstr(strchr(s + 8, '/'), "/videoplayback") != NULL;
}
static int hlsUrl(const char *s) {
  return googleVideoHost(s) &&
         strstr(strchr(s + 8, '/'), "/api/manifest/hls_playlist/") != NULL;
}

// Prima di pubblicare il flusso al decoder uMS, verifica che la TV possa
// leggerne i primi byte con la SUA connessione. Molte URL Android VR sono
// ancora restituite dall'API ma rispondono HTTP 403 sul CDN (agosto 2026).
static int provaDiretta(const char *url) {
  long n = 0;
  int status = 0;
  int64_t total = -1;
  char *primi;
  if (hlsUrl(url)) {
    char *indice = rede_baixar(url, 6);
    int ok = indice && !strncmp(indice, "#EXTM3U", 7);
    free(indice);
    return ok;
  }
  if (!mediaUrl(url)) return 0;
  primi = rede_baixar_trecho64_cab(url, NULL, 0, 1, &n, &total, &status, NULL);
  free(primi);
  return status == 206 && n == 2;
}

static int estrai(const char *corpo, char *dest, size_t cap) {
  const char *p, *fim;
  int migliore = -1;
  char candidato[YT_URL_CAP] = "";
  if (!corpo) return 0;
  // Soltanto formats[]: adaptiveFormats[] ha audio e video separati.
  p = js_array(corpo, NULL, "formats");
  while (p) {
    char mime[180] = "", url[YT_URL_CAP] = "", audio[50] = "";
    int itag, punti = -1;
    fim = js_fim(p);
    if (!fim) break;
    js_texto(p, fim, "mimeType", mime, sizeof mime);
    js_texto(p, fim, "audioQuality", audio, sizeof audio);
    itag = (int)js_num(p, fim, "itag", 0);
    if (strstr(mime, "video/mp4") && (audio[0] || itag == 18 || itag == 22) &&
        js_texto(p, fim, "url", url, sizeof url) && mediaUrl(url)) {
      punti = itag == 22 ? 300 : itag == 18 ? 200 : 100;
      if (punti > migliore) {
        migliore = punti;
        snprintf(candidato, sizeof candidato, "%s", url);
      }
    }
    p = js_prox(fim);
  }
  if (migliore >= 0) {
    snprintf(dest, cap, "%s", candidato);
    return 1;
  }
  // Alternativa iOS: manifest HLS direttamente leggibile dal decoder webOS.
  js_texto(corpo, NULL, "hlsManifestUrl", candidato, sizeof candidato);
  if (hlsUrl(candidato)) {
    snprintf(dest, cap, "%s", candidato);
    return 1;
  }
  return 0;
}

static int tentaCliente(const char *api, const char *id, const char *nome,
                         const char *version, const char *os, const char *osVersion, const char *model,
                         const char *const *headers, char *url, size_t cap) {
  char corpo[620];
  char candidato[YT_URL_CAP] = "";
  char *resposta, status[40] = "";
  int got, validoUrl;
  snprintf(corpo, sizeof corpo,
           "{\"videoId\":\"%s\",\"context\":{\"client\":{\"clientName\":\"%s\","
           "\"clientVersion\":\"%s\",\"osName\":\"%s\",\"osVersion\":\"%s\","
           "\"deviceModel\":\"%s\",\"hl\":\"it\",\"gl\":\"IT\"}},"
           "\"contentCheckOk\":true,\"racyCheckOk\":true}",
           id, nome, version, os, osVersion, model);
  resposta = rede_postar(api, 6, headers, corpo);
  if (resposta)
    js_texto(resposta, NULL, "status", status, sizeof status);
  got = estrai(resposta, candidato, sizeof candidato);
  free(resposta);
  validoUrl = got && provaDiretta(candidato);
  // Logga soltanto lo stato (mai URL firmate o corpo della resposta).
  printf("[trailer] TMDB stream client=%s status=%s candidate=%d accessible=%d\n",
         nome, status[0] ? status : "network", got, validoUrl);
  fflush(stdout);
  if (!validoUrl) return 0;
  snprintf(url, cap, "%s", candidato);
  return 1;
}

static int resolver(const char *id, char *url, size_t cap) {
  // La versione ANDROID_VR 1.65.10 e' soggetta a 403 sistematici dal
  // 17 agosto 2026. Prima proviamo ANDROID, poi iOS (HLS), infine VR,
  // verificando sul dispositivo la resposta HTTP reale prima del play.
  const char *const hAndroid[] = {
    "X-YouTube-Client-Name: 3",
    "X-YouTube-Client-Version: 21.03.36",
    "Origin: https://www.youtube.com",
    "User-Agent: com.google.android.youtube/21.03.36 (Linux; U; Android 14) gzip",
    NULL
  };
  const char *const hIos[] = {
    "X-YouTube-Client-Name: 5",
    "X-YouTube-Client-Version: 21.03.2",
    "Origin: https://www.youtube.com",
    "User-Agent: com.google.ios.youtube/21.03.2 (iPhone16,2; U; CPU iOS 18_0 like Mac OS X)",
    NULL
  };
  const char *api = "https://www.youtube.com/youtubei/v1/player?key=AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8";
  if (tentaCliente(api,id,"ANDROID","21.03.36","Android","14","Pixel 8",hAndroid,url,cap)) return 1;
  if (tentaCliente(api,id,"IOS","21.03.2","iOS","18.0","iPhone16,2",hIos,url,cap)) return 1;
  return 0;
}

static void *ytWorker(void *unused) {
  (void)unused;
  for (;;) {
    char id[16], url[YT_URL_CAP] = "";
    unsigned generation;
    int ok;
    pthread_mutex_lock(&ytMutex);
    while (ytProcessed == ytRequest)
      pthread_cond_wait(&ytCond, &ytMutex);
    generation = ytRequest;
    ytProcessed = generation;
    snprintf(id, sizeof id, "%s", ytWanted);
    pthread_mutex_unlock(&ytMutex);
    ok = resolver(id, url, sizeof url);
    pthread_mutex_lock(&ytMutex);
    if (ytRequest == generation && !strcmp(ytWanted, id)) {
      ytState = ok ? 1 : -1;
      snprintf(ytResolved, sizeof ytResolved, "%s", ok ? url : "");
      ytFinishedAt = time(NULL);
      printf("[trailer] TMDB interno: %s (risoluzione %s)\n",
             id, ok ? "flusso verificato" : "nessun flusso accessibile");
      fflush(stdout);
    }
    pthread_mutex_unlock(&ytMutex);
  }
  return NULL;
}

int traileryt_obter(const char *youtube_id, char *url, size_t url_cap) {
  int status;
  time_t now;
  if (url && url_cap) url[0] = 0;
  if (!url || url_cap < 1024 || !valido(youtube_id)) return -1;
  pthread_mutex_lock(&ytMutex);
  now = time(NULL);
  if (strcmp(youtube_id, ytWanted) ||
      (ytState && ytFinishedAt && now - ytFinishedAt >
       (ytState > 0 ? YT_WAIT_SUCCESS : YT_WAIT_FAILURE))) {
    snprintf(ytWanted, sizeof ytWanted, "%s", youtube_id);
    ytResolved[0] = 0;
    ytState = 0;
    ++ytRequest;
    if (!ytThreadCreated) {
      if (pthread_create(&ytThread, NULL, ytWorker, NULL) == 0) {
        pthread_detach(ytThread);
        ytThreadCreated = 1;
      } else {
        ytState = -1;
        ytFinishedAt = now;
        ytProcessed = ytRequest;
      }
    }
    if (ytThreadCreated) pthread_cond_signal(&ytCond);
  }
  status = ytState;
  if (status > 0) snprintf(url, url_cap, "%s", ytResolved);
  pthread_mutex_unlock(&ytMutex);
  return status;
}

int traileryt_invalidar(const char *url) {
  int tmdb = 0;
  if (!url || !url[0]) return 0;
  pthread_mutex_lock(&ytMutex);
  if (ytState == 1 && !strcmp(ytResolved, url)) {
    tmdb = 1;
    ytState = -1;
    ytResolved[0] = 0;
    ytFinishedAt = time(NULL);
    printf("[trailer] TMDB interno: flusso rifiutato, nessun fallback nascosto\n");
    fflush(stdout);
  }
  pthread_mutex_unlock(&ytMutex);
  return tmdb;
}
