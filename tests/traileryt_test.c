#include <assert.h>
#include <stdio.h>
#include <string.h>
// Unita' sotto test: anche la funzione di parsing statica.
// La risposta di rete e' simulata, nessuna richiesta esterna.
#include "../src/traileryt.c"
char *rede_postar(const char *url, int seconds, const char *const *headers, const char *body) {
  (void)url; (void)seconds; (void)headers; (void)body;
  return NULL;
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
  puts("PASS: TMDB/YouTube native media URL selection and validation");
  return 0;
}
