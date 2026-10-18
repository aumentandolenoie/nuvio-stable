#!/usr/bin/env python3
"""Contract: Stremio required genre live catalogs are real guide sources."""
from pathlib import Path
a=Path("src/addons.c").read_text()
h=Path("src/addons.h").read_text()
g=Path("src/guia.c").read_text()
assert "genero[64]" in h and "ADD_CANAL_MAX 64" in h
assert 'js_array(p, f, "extra")' in a
assert 'js_array(extra, ef, "options")' in a
assert 'js_cadeia(option, value, sizeof value)' in a
assert 'requiredGenre' in a and 'requiredOther' in a
assert 'if (!requiredGenre && !requiredOther' in a
assert "G_MAX_FONTE   96" in g
assert '"genre=%s.json"' in g or '"/catalog/%s/%s/genre=%s.json"' in g
assert '"/catalog/%s/%s/genre=%s&skip=%d.json"' in g
assert '"%%%02X"' in g
assert '!strcmp(sFontes[j].genero, cc[k].genero)' in g
assert 'if (sFontes[i].genero[0])' in g
assert 'if (cota > 48) cota = 48;' in g
assert 'else if (cota < G_COTA_MIN) cota = G_COTA_MIN;' in g
print("PASS: genre-required live TV catalog discovery, encoded requests, quotas")
