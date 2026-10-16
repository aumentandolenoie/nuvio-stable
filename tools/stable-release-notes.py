#!/usr/bin/env python3
"""Estrae note per singola versione dal changelog verificato della fork Stable.

Uso:
    python3 tools/stable-release-notes.py --check
    python3 tools/stable-release-notes.py 2.0.17 > release-notes.md
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HISTORY = ROOT / "RELEASE_NOTES.md"
HEADER = re.compile(r"^## (\d+\.\d+\.\d+) — (.+)$", re.M)


def release_notes():
    body = HISTORY.read_text(encoding="utf-8")
    headers = list(HEADER.finditer(body))
    if not headers:
        raise ValueError("RELEASE_NOTES.md: nessuna versione")
    result = {}
    for i, match in enumerate(headers):
        version, title = match.group(1), match.group(2)
        end = headers[i + 1].start() if i + 1 < len(headers) else len(body)
        details = body[match.end():end].strip()
        if version in result:
            raise ValueError(f"Versione duplicata: {version}")
        if not details or details.count("- ") < 1 or "TODO" in details or "TBD" in details:
            raise ValueError(f"Note assenti o incomplete: {version}")
        result[version] = f"# Nuvio Stable {version} — {title}\n\n{details}\n"
    return result


def validate(items):
    manifest = json.loads((ROOT / "deploy/app/appinfo.json").read_text())
    version = manifest["version"]
    if manifest["id"] != "space.nuvio.native.stable":
        raise ValueError("Identita Stable inattesa")
    xml = (ROOT / "tools/tizen-config.xml").read_text()
    if not re.search(r'<widget[^>]*version="' + re.escape(version) + r'"', xml, re.S):
        raise ValueError("Versione del manifest Tizen diversa dal webOS")
    if version not in items:
        raise ValueError(f"RELEASE_NOTES.md: manca la versione {version}")
    for patch in range(5, 17):
        if f"2.0.{patch}" not in items:
            raise ValueError(f"Mancano le note storiche 2.0.{patch}")
    newest = max(items, key=lambda v: tuple(map(int, v.split("."))))
    if newest != version:
        raise ValueError(f"Ultime release notes {newest} non corrispondono alla versione app {version}")
    print(f"PASS: release notes dedicate alla versione {version}, storico {len(items)} release")


def main():
    notes = release_notes()
    if len(sys.argv) == 2 and sys.argv[1] == "--check":
        validate(notes)
    elif len(sys.argv) == 2 and sys.argv[1] in notes:
        sys.stdout.write(notes[sys.argv[1]])
    else:
        raise SystemExit("Uso: stable-release-notes.py --check | VERSIONE")


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError, KeyError) as exc:
        raise SystemExit(f"ERRORE release notes: {exc}")
