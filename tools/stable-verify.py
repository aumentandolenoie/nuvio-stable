#!/usr/bin/env python3
"""Verify packaged LG webOS binary, separate identity and Homebrew metadata."""
import hashlib
import io
import json
from pathlib import Path
import subprocess
import sys
import tarfile

APP_ID = "space.nuvio.native.stable"
REPO = "aumentandolenoie/nuvio-stable"


def check(condition, detail):
    if not condition:
        raise SystemExit("FAIL: " + detail)
    print("PASS: " + detail)


def main():
    if len(sys.argv) != 3:
        raise SystemExit("usage: stable-verify.py PACKAGE.ipk HOMEBREW_DIR")
    path = Path(sys.argv[1])
    output = Path(sys.argv[2])
    check(path.is_file() and path.stat().st_size > 0, "IPK non-empty")
    expected_meta = json.loads(Path("deploy/app/appinfo.json").read_text())
    check(path.name == f"{APP_ID}_{expected_meta['version']}_arm.ipk",
          "IPK filename matches app id and version")
    data = subprocess.check_output(["ar", "p", str(path), "data.tar.gz"])
    with tarfile.open(fileobj=io.BytesIO(data), mode="r:gz") as tar:
        members = tar.getmembers()
        meta = [m for m in members if m.name.endswith("/appinfo.json")]
        executable = [m for m in members if m.name.endswith("/nuvio-proto")]
        check(len(meta) == 1 and len(executable) == 1, "exactly one packaged appinfo and binary")
        package_info = json.load(tar.extractfile(meta[0]))
        check(package_info["id"] == APP_ID and package_info["title"] == "Nuvio Stable",
              "independent packaged identity")
        check(package_info["version"] == expected_meta["version"],
              "packaged app version matches source")
        check(executable[0].mode & 0o777 == 0o755, "native executable is mode 0755")
        binary = tar.extractfile(executable[0]).read()
        check(APP_ID.encode() in binary, "native executable uses Stable app ID")
        check(b"com.webos.media.client.space.nuvio.native.stable" in binary,
              "native player uses Stable LS2 client identity")
    manifest = json.loads((output / "webosbrew.manifest.json").read_text())
    index = json.loads((output / "repo.json").read_text())
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    check(manifest["id"] == APP_ID and manifest["version"] == package_info["version"],
          "Homebrew manifest ID and version")
    check(manifest["ipkHash"]["sha256"] == digest and manifest["ipkSize"] == path.stat().st_size,
          "Homebrew SHA-256 and file size")
    check(manifest["ipkUrl"] ==
          f"https://github.com/{REPO}/releases/download/v{package_info['version']}/{path.name}",
          "Homebrew IPK URL targets the correct release asset")
    check(index["packages"][0]["manifest"] == manifest, "Homebrew index contains verified manifest")
    print("VALIDATED LG webOS Homebrew package:", path)


if __name__ == "__main__":
    main()
