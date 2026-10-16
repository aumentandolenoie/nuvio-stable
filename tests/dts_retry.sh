#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT
cc -std=c11 -O2 -Wall -Wextra -Werror -Isrc tests/dts_retry.c -o "$tmp/dts_retry"
"$tmp/dts_retry"
