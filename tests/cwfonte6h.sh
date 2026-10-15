#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
dir="$(mktemp -d)"
trap 'rm -rf "$dir"' EXIT
cc -std=gnu11 -Wall -Wextra -Werror -Isrc \
   src/cwfonte6h.c tests/cwfonte6h.c -o "$dir/cwfonte6h"
"$dir/cwfonte6h"
