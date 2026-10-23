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
# Diagnostics apply only to the TizenBrew package; the standalone WGT stays intact.
html_path = app / "index.html"
html = html_path.read_text()
# Generated Emscripten HTML may change whitespace or inline diagnostic code.
# Keep the runtime unchanged and suppress only matching repetitive console messages.
diagnostic_filter = """<script>
(function () {
  var previous = console.log;
  var seenThreads = false;
  console.log = function () {
    if (arguments.length && typeof arguments[0] === 'string' && arguments[0].indexOf('[fios] livres=') === 0) {
      if (seenThreads) return;
      seenThreads = true;
    }
    return previous.apply(console, arguments);
  };
})();
</script>
"""
diagnostic = """<script>
(function () {
  var info = document.createElement('div');
  info.id = 'nuvio-brew-startup-diagnostic';
  info.style.cssText = 'position:fixed;top:0;left:0;right:0;padding:14px 22px;background:#161b28;color:#fff;font:20px monospace;z-index:2147483647;white-space:pre-wrap;pointer-events:none';
  function report() {
    var worker = typeof Worker, wasm = typeof WebAssembly, sab = typeof SharedArrayBuffer;
    var gl = 'unknown';
    try { var c = document.createElement('canvas'); gl = !!(c.getContext('webgl') || c.getContext('experimental-webgl')); } catch (e) { gl = 'error: ' + e.message; }
    info.textContent = 'Nuvio Stable / TizenBrew diagnostic\\nWebAssembly=' + wasm + ' Worker=' + worker + ' SharedArrayBuffer=' + sab + ' isolated=' + (typeof crossOriginIsolated === 'undefined' ? 'unknown' : crossOriginIsolated) + ' WebGL=' + gl + '\\nWaiting for app rendering. Photograph this panel if the screen stays black.';
  }
  document.addEventListener('DOMContentLoaded', function () { document.body.appendChild(info); report(); });
  window.addEventListener('error', function (e) { if (info.parentNode) info.textContent += '\\nJS ERROR: ' + e.message; });
  window.addEventListener('unhandledrejection', function (e) { if (info.parentNode) info.textContent += '\\nPROMISE ERROR: ' + String(e.reason); });
  // Keep diagnostics visible for this diagnostic-only release, even if an empty canvas exists.
})();
</script>
"""
if "</head>" not in html:
    sys.exit("Missing head element; cannot inject TizenBrew diagnostics")
html_path.write_text(html.replace("</head>", diagnostic_filter + diagnostic + "</head>", 1))

manifest_version = json.loads(pathlib.Path("deploy/app/appinfo.json").read_text())["version"]
if not re.fullmatch(r"\d+\.\d+\.\d+", manifest_version):
    sys.exit("Unexpected version string")
manifest = {
    "name": "@aumentandolenoie/nuvio-stable-tizenbrew",
    "version": manifest_version + "-test.1",
    "private": False,
    "description": "Nuvio Stable Samsung WebAssembly TizenBrew application module (experimental)",
    "license": "GPL-3.0-or-later",
    "repository": {"type": "git", "url": "https://github.com/aumentandolenoie/nuvio-stable.git"},
    "packageType": "app",
    "appName": "Nuvio Stable (test)",
    "appPath": "app/index.html",
    "keys": ["MediaPlay", "MediaPause", "MediaPlayPause", "MediaStop", "MediaFastForward", "MediaRewind"],
    "files": ["app/**"],
}
(dest / "package.json").write_text(json.dumps(manifest, indent=2) + "\n")
print(f"TizenBrew candidate prepared: {manifest['name']}@{manifest_version}; not published")
