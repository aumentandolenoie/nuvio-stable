#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
cc -D_GNU_SOURCE -std=c11 -O0 -Wall -Wextra -pthread -I src \
  tests/traileryt_test.c src/js.c -lm -o /tmp/nuvio-traileryt-test
/tmp/nuvio-traileryt-test
