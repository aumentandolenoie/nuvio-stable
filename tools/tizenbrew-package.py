#!/usr/bin/env python3
"""Prepare a TizenBrew application-module candidate from a validated Samsung WGT.

Does not publish to npm or assert that AVPlay works under TizenBrew.
"""
import json
import pathlib
import re
import sys
import zipfile

if len(sys.argv) != 3:
    sys.exit("Usage: python3 tools/tizenbrew-package.py input.wgt output-directory")
archive = pathlib.Path(sys.argv[1])
dest = pathlib.Path(sys.argv[2])
if not archive.is_file():
    sys.exit(f"Missing WGT: {archive}")
if dest.exists() and any(dest.iterdir()):
    sys.exit("Output directory must be empty (no stale build files)")
app = dest / "app"
app.mkdir(parents=True, exist_ok=True)
required = {"index.html", "index.js", "index.wasm", "decodificador.js", "icon.png"}
with zipfile.ZipFile(archive) as z:
    names = set(z.namelist())
    missing = required - names
    if missing:
        sys.exit(f"WGT is missing: {sorted(missing)}")
    for member in z.infolist():
        if member.is_dir() or member.filename == "config.xml":
            continue
        relative = pathlib.PurePosixPath(member.filename)
        if relative.is_absolute() or ".." in relative.parts:
            sys.exit("Unsafe archive path")
        out = app.joinpath(*relative.parts)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_bytes(z.read(member))
    if not (app / "index.html").stat().st_size or not (app / "index.wasm").stat().st_size:
        sys.exit("Empty application assets")
manifest_version = json.loads(pathlib.Path("deploy/app/appinfo.json").read_text())["version"]
if not re.fullmatch(r"\d+\.\d+\.\d+", manifest_version):
    sys.exit("Unexpected version string")
manifest = {
    "name": "@aumentandolenoie/nuvio-stable-tizenbrew",
    "version": manifest_version,
    "private": False,
    "description": "Nuvio Stable Samsung WebAssembly TizenBrew application module (experimental)",
    "license": "GPL-3.0-or-later",
    "repository": {"type": "git", "url": "https://github.com/aumentandolenoie/nuvio-stable.git"},
    "packageType": "app",
    "appName": "Nuvio Stable (test)",
    "appPath": "app/index.html",
    "files": ["app/**"],
}
(dest / "package.json").write_text(json.dumps(manifest, indent=2) + "\n")
print(f"TizenBrew candidate prepared: {manifest['name']}@{manifest_version}; not published")
