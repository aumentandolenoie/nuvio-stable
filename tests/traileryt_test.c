#include <assert.h>
#include <stdio.h>
#include <string.h>
// Unita' sotto test: anche la funzione di parsing statica.
// La risposta di rete e' simulata, nessuna richiesta esterna.
#include "../src/traileryt.c"
static int mockMode, androidCalls, iosCalls, vrCalls, byteRequests;
char *rede_postar(const char *url, int seconds, const char *const *headers, const char *body) {
  (void)url; (void)seconds; (void)headers;
  if (!mockMode) return NULL;
  if (strstr(body, "\"clientName\":\"ANDROID_VR\"")) vrCalls++;
  else if (strstr(body, "\"clientName\":\"ANDROID\"")) androidCalls++;
  else if (strstr(body, "\"clientName\":\"IOS\"")) iosCalls++;
  else assert(!"unexpected client");
  if (mockMode == 1 && androidCalls && !iosCalls)
    return strdup("{\"streamingData\":{\"formats\":[{\"itag\":18,\"mimeType\":\"video/mp4\",\"url\":\"https://rr1.googlevideo.com/videoplayback?deny=1\"}]}}");
  return strdup("{\"streamingData\":{\"formats\":[{\"itag\":18,\"mimeType\":\"video/mp4\",\"url\":\"https://rr1.googlevideo.com/videoplayback?ok=1\"}]}}");
}
char *rede_baixar_trecho64_cab(const char *url, const char *headers, int64_t start,
                               int64_t end, long *size, int64_t *total, int *status,
                               volatile int *cancelled) {
  (void)headers; (void)start; (void)end; (void)cancelled;
  byteRequests++;
  if (strstr(url, "deny=1")) {
    if (status) *status = 403;
    if (size) *size = 0;
    return NULL;
  }
  if (status) *status = 206;
  if (size) *size = 2;
  if (total) *total = 200;
  return strdup("AB");
}
char *rede_baixar(const char *url, int timeout) {
  (void)url; (void)timeout;
  return strdup("#EXTM3U\\n");
}
int main(void) {
  char url[4096];
  const char *sample =
    "{\"streamingData\":{\"formats\":["
    "{\"itag\":18,\"mimeType\":\"video/mp4; codecs=avc1\","
    "\"audioQuality\":\"AUDIO_QUALITY_LOW\","
    "\"url\":\"https://rr1---sn.googlevideo.com/videoplayback?itag=18\"},"
    "{\"itag\":22,\"mimeType\":\"video/mp4; codecs=avc1\","
    "\"audioQuality\":\"AUDIO_QUALITY_MEDIUM\","
    "\"url\":\"https://rr1---sn.googlevideo.com/videoplayback?itag=22\"}]}}";
  assert(estrai(sample, url, sizeof url) == 1);
  assert(strstr(url, "itag=22") != NULL);
  assert(!mediaUrl("https://googlevideo.com.evil.example/videoplayback"));
  assert(!mediaUrl("http://rr1.googlevideo.com/videoplayback"));
  assert(!mediaUrl("https://youtube.com/watch?v=dQw4w9WgXcQ"));
  assert(traileryt_obter("bad", url, sizeof url) == -1);
  assert(estrai("{\"streamingData\":{\"formats\":[{\"itag\":140,"
                "\"mimeType\":\"audio/mp4\",\"url\":\"https://rr1.googlevideo.com/videoplayback\"}]}}",
                url, sizeof url) == 0);
  assert(estrai("{\"streamingData\":{\"hlsManifestUrl\":\"https://rr1.googlevideo.com/"
                "api/manifest/hls_playlist/index.m3u8\"}}", url, sizeof url) == 1);
  // Un flusso TMDB rifiutato non deve essere riprovato e scambiato per Apple/IMDb.
  pthread_mutex_lock(&ytMutex);
  ytState = 1;
  snprintf(ytResolved, sizeof ytResolved, "https://rr1.googlevideo.com/videoplayback?itag=18");
  pthread_mutex_unlock(&ytMutex);
  assert(traileryt_invalidar("https://rr1.googlevideo.com/videoplayback?itag=18") == 1);
  assert(ytState == -1);
  assert(traileryt_invalidar("https://rr1.googlevideo.com/videoplayback?itag=18") == 0);
  assert(!hlsUrl("https://bad.host/p/.googlevideo.com/api/manifest/hls_playlist/index.m3u8"));
  assert(hlsUrl("https://manifest.googlevideo.com/api/manifest/hls_playlist/index.m3u8"));
  mockMode = 1; // Android CDN 403: usare il client iOS, non VR
  androidCalls = iosCalls = vrCalls = byteRequests = 0;
  assert(resolver("AbCdEfGh123", url, sizeof url) == 1);
  assert(strstr(url, "ok=1") != NULL);
  assert(androidCalls == 1 && iosCalls == 1 && vrCalls == 0);
  assert(byteRequests == 2);
  mockMode = 2; // Android CDN 206: non chiamare gli altri client
  androidCalls = iosCalls = vrCalls = byteRequests = 0;
  assert(resolver("AbCdEfGh123", url, sizeof url) == 1);
  assert(androidCalls == 1 && iosCalls == 0 && vrCalls == 0 && byteRequests == 1);
  puts("PASS: TMDB/YouTube native media URL selection and validation");
  return 0;
}
