// TMDB restituisce ID di YouTube, non URL MP4. Il player nativo LG
// puo' ricevere una URL HTTPS di un formato progressivo (audio+video).
// Questo risolutore e' volutamente sperimentale: YouTube puo' rispondere 403,
// richiedere token di origine o fornire soltanto formati SABR. In quel caso
// il chiamante deve ripiegare sulle fonti Apple TV/IMDb gia' supportate.
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

// Accetta solo flussi media HTTPS di YouTube, mai URL arbitrarie nella resposta.
// L'URL scade e non viene scritto su disco.
static int mediaUrl(const char *s) {
  const char *host, *fim, *p;
  size_t n;
  if (!s || strncmp(s, "https://", 8)) return 0;
  host = s + 8;
  fim = strchr(host, '/');
  if (!fim) return 0;
  n = (size_t)(fim - host);
  if (n < 16 || n > 200 || !strstr(fim, "videoplayback")) return 0;
  // Per impedire redirect o host falsi, confronta il SUFFISSO del dominio.
  for (p = host; p + 16 <= fim; ++p) {
    if (p + 16 == fim && !strncmp(p, ".googlevideo.com", 16)) return 1;
  }
  return n == strlen("googlevideo.com") && !strncmp(host, "googlevideo.com", n);
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
  if (!strncmp(candidato, "https://", 8) &&
      (strstr(candidato, ".googlevideo.com/") || strstr(candidato, "googlevideo.com/"))) {
    snprintf(dest, cap, "%s", candidato);
    return 1;
  }
  return 0;
}

static int resolver(const char *id, char *url, size_t cap) {
  const char *const headersVr[] = {
    "X-YouTube-Client-Name: 28",
    "X-YouTube-Client-Version: 1.65.10",
    "Origin: https://www.youtube.com",
    "User-Agent: com.google.android.apps.youtube.vr.oculus/1.65.10 (Linux; U; Android 12L) gzip",
    NULL
  };
  const char *const headersIos[] = {
    "X-YouTube-Client-Name: 5",
    "X-YouTube-Client-Version: 20.49.6",
    "Origin: https://www.youtube.com",
    "User-Agent: com.google.ios.youtube/20.49.6 (iPhone16,2; U; CPU iOS 18_0 like Mac OS X)",
    NULL
  };
  char corpo[600];
  char *resposta;
  int ok;
  // Chiave pubblica del client YouTube (non e' una credenziale Nuvio).
  const char *api = "https://www.youtube.com/youtubei/v1/player?key=AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8";
  snprintf(corpo, sizeof corpo,
           "{\"videoId\":\"%s\",\"context\":{\"client\":{\"clientName\":\"ANDROID_VR\","
           "\"clientVersion\":\"1.65.10\",\"androidSdkVersion\":32,"
           "\"deviceMake\":\"Oculus\",\"deviceModel\":\"Quest 3\","
           "\"osName\":\"Android\",\"osVersion\":\"12L\",\"hl\":\"it\",\"gl\":\"IT\"}},"
           "\"contentCheckOk\":true,\"racyCheckOk\":true}", id);
  resposta = rede_postar(api, 7, headersVr, corpo);
  ok = estrai(resposta, url, cap);
  free(resposta);
  if (ok) return 1;
  snprintf(corpo, sizeof corpo,
           "{\"videoId\":\"%s\",\"context\":{\"client\":{\"clientName\":\"IOS\","
           "\"clientVersion\":\"20.49.6\",\"deviceModel\":\"iPhone16,2\","
           "\"osName\":\"iOS\",\"osVersion\":\"18.0\",\"hl\":\"it\",\"gl\":\"IT\"}},"
           "\"contentCheckOk\":true,\"racyCheckOk\":true}", id);
  resposta = rede_postar(api, 7, headersIos, corpo);
  ok = estrai(resposta, url, cap);
  free(resposta);
  return ok;
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
             id, ok ? "flusso disponibile" : "non disponibile, fallback Apple/IMDb");
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
