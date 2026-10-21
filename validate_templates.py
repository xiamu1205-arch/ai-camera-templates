#!/usr/bin/env python3
"""Validate templates.json with the same rules the app applies
(PoseTemplatePackParser): ids unique, points/scored/framing in range,
shoulder centre == (0,-1), hip centre == (0,0). Usage:
    python3 validate_templates.py templates.json
"""
import json, sys

def main(path):
    pack = json.load(open(path, encoding="utf-8"))
    errs, ids = [], set()
    for t in pack.get("templates", []):
        tid = t.get("id", "?")
        if tid in ids: errs.append(f"dup id {tid}")
        ids.add(tid)
        if not t.get("name") or not t.get("category"): errs.append(f"{tid}: empty name/category")
        pts = {int(k): v for k, v in t.get("points", {}).items()}
        for idx, (x, y) in pts.items():
            if not (0 <= idx <= 32): errs.append(f"{tid}: bad index {idx}")
            if not (-3.0 <= x <= 3.0 and -3.5 <= y <= 3.5): errs.append(f"{tid}: coord range {idx}")
        if not t.get("scored"): errs.append(f"{tid}: scored empty")
        for s in t.get("scored", []):
            if s not in pts: errs.append(f"{tid}: scored {s} not in points")
        if 11 in pts and 12 in pts:
            sc = ((pts[11][0]+pts[12][0])/2, (pts[11][1]+pts[12][1])/2)
            if abs(sc[0]) > 0.06 or abs(sc[1]+1.0) > 0.06: errs.append(f"{tid}: shoulder centre {sc}")
        if 23 in pts and 24 in pts:
            hc = ((pts[23][0]+pts[24][0])/2, (pts[23][1]+pts[24][1])/2)
            if abs(hc[0]) > 0.06 or abs(hc[1]) > 0.06: errs.append(f"{tid}: hip centre {hc}")
        f = t.get("framing", {})
        if not (0.2 <= f.get("hipX", -1) <= 0.8 and 0.2 <= f.get("hipY", -1) <= 0.9
                and 0.10 <= f.get("torso", -1) <= 0.60):
            errs.append(f"{tid}: framing range {f}")
    if errs:
        print("INVALID:"); [print(" -", e) for e in errs]; sys.exit(1)
    print(f"OK: {len(ids)} templates valid")

if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "templates.json")
