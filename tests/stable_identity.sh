#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
work="$(mktemp -d)"
trap 'rm -rf "$work"' EXIT
cat > "$work/identity.c" <<'EOF'
#include "app_id.h"
#include <stdio.h>
#include <string.h>
int main(void) {
  if (strcmp(NV_APP_ID, "space.nuvio.native.stable") != 0) return 1;
  if (strcmp(NV_APP_ID, NV_APP_ID_PRODUCTION) == 0) return 2;
#ifdef NV_APP_ID_DEFAULT
#error "Stable identity must not use the production media client"
#endif
  if (strcmp(NV_LS_MEDIA_CLIENT,
             "com.webos.media.client.space.nuvio.native.stable") != 0) return 3;
  puts("PASS stable application/media-client identity");
  return 0;
}
EOF
cc -std=c11 -Isrc "$work/identity.c" -o "$work/identity"
"$work/identity"
python3 - <<'PY'
import json
from pathlib import Path
p=json.loads(Path('deploy/app/appinfo.json').read_text())
assert p['id']=='space.nuvio.native.stable'
assert p['title']=='Nuvio Stable'
s=Path('src/atualizacao.c').read_text()
assert 'https://api.github.com/repos/aumentandolenoie/nuvio-stable/releases/latest' in s
assert '#define AT_APPID  NV_APP_ID' in s
assert 'REPO="aumentandolenoie/nuvio-stable"' in Path('tools/hb-repo.sh').read_text()
print("PASS Homebrew and updater target Stable repository")
PY
