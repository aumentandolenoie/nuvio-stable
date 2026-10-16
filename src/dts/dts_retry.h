// Retry policy for the native DTS HTTP range worker.
// Keep this pure and testable: the only retries are fast transient failures.
// Slow 15s network timeouts, cancellations, and permanent HTTP errors must
// NOT produce another multi-second pause in film playback.
#ifndef NV_DTS_RETRY_H
#define NV_DTS_RETRY_H
#include <stdint.h>

#define DTS_RANGE_RETRY_FAST_NS UINT64_C(2500000000)

static inline int dts_range_retryable(int http_status, long bytes,
                                       uint64_t elapsed_ns, int cancelled) {
  if (cancelled || bytes != 0 || elapsed_ns > DTS_RANGE_RETRY_FAST_NS) return 0;
  switch (http_status) {
    case 0:   // connection failure, only when it failed promptly
    case 206: // empty partial-content response (never a valid media chunk)
    case 408: // request timeout, if immediate
    case 429: // temporary rate limit; only one bounded retry
    case 500: case 502: case 503: case 504:
      return 1;
    default: // 401, 403, 404, 416 and all other responses are not retried
      return 0;
  }
}
#endif
