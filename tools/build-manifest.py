#!/usr/bin/env python3
"""Rebuild the RyoStore manifest for Insei Fetch by hashing the
product folder.

Usage: build-manifest.py <product-dir>

The store folder for a fastfetch preset is flat:

    fastfetch/insei-fetch/
        config.jsonc, emblem.png   the preset and its face
        LICENSE, PROVENANCE.txt
        preview.webp                the shelf picture (not installed)
        manifest.json

Every file installs to the preset's own destination except
preview.webp. Prints the manifestSha256 the registry row must carry.
"""
import hashlib
import json
import os
import sys

root = sys.argv[1]

files = []
for name in sorted(os.listdir(root)):
    full = os.path.join(root, name)
    if name == "manifest.json" or not os.path.isfile(full):
        continue
    data = open(full, "rb").read()
    files.append({
        "source": name,
        "destination": name,
        "mode": "0644",
        "size": len(data),
        "sha256": hashlib.sha256(data).hexdigest(),
        "install": name != "preview.webp",
    })
manifest = {
    "schema": 1,
    "id": "insei-fetch",
    "category": "fastfetch",
    "version": "1.0.4",
    "destination": "ryoku/fastfetch/insei-fetch",
    "files": files,
}
out = json.dumps(manifest, indent=2, ensure_ascii=False) + "\n"
open(os.path.join(root, "manifest.json"), "w").write(out)
print(hashlib.sha256(out.encode()).hexdigest())
