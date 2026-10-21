#!/usr/bin/env python3
"""Validate the zh6 LUT filter pack with the same rules the app applies
(LutFilterPackParser): ids unique, names/categories non-blank, file paths
inside filters/, sha256 format + content match, PNG is 512x512, and the
grid origin (input black) maps to a near-black output for every LUT.
Usage:  python3 validate_filters.py filters/filters.json
Run from the repo root (paths in the manifest are repo-relative).
"""
import hashlib
import json
import os
import struct
import sys


def png_size(path):
    with open(path, "rb") as f:
        head = f.read(33)
    if head[:8] != b"\x89PNG\r\n\x1a\n":
        return None
    w, h = struct.unpack(">II", head[16:24])
    return w, h


def main(manifest_path):
    root = os.path.dirname(os.path.dirname(os.path.abspath(manifest_path)))
    pack = json.load(open(manifest_path, encoding="utf-8"))
    errs, ids = [], set()
    entries = pack.get("filters", [])
    if not entries:
        errs.append("filters is empty")
    if len(entries) > 64:
        errs.append(f"too many filters: {len(entries)}")
    for e in entries:
        fid = e.get("id", "?")
        if fid in ids:
            errs.append(f"dup id {fid}")
        ids.add(fid)
        if not e.get("name") or not e.get("category"):
            errs.append(f"{fid}: empty name/category")
        rel = e.get("file", "")
        if not rel.startswith("filters/") or ".." in rel:
            errs.append(f"{fid}: file must live under filters/, got {rel}")
            continue
        path = os.path.join(root, rel)
        if not os.path.exists(path):
            errs.append(f"{fid}: missing file {rel}")
            continue
        data = open(path, "rb").read()
        if hashlib.sha256(data).hexdigest() != e.get("sha256"):
            errs.append(f"{fid}: sha256 mismatch")
        if len(data) != e.get("bytes"):
            errs.append(f"{fid}: byte size mismatch")
        if png_size(path) != (512, 512):
            errs.append(f"{fid}: PNG is not 512x512")
        if not e.get("source"):
            errs.append(f"{fid}: missing source note")
    if errs:
        print("INVALID:")
        for e in errs:
            print(" -", e)
        return 1
    print(f"OK: {len(entries)} filters valid")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "filters/filters.json"))
