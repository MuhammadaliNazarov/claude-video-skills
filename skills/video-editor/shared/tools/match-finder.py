#!/usr/bin/env python3
"""match-finder.py: find match-cut and cut-on-action points across clips.

  python3 match-finder.py clip1.mov clip2.mov ... [--top 8] [--fps 4] [--out matches.json]

Prints:
  GRAPHIC matches  frame pairs (end region of one clip -> any point of another) whose shapes/composition line up
                   (edge-map correlation on a 64x36 grey thumbnail; colour-histogram similarity as a tie-break)
  MOVEMENT matches pairs where the direction of motion agrees (mean optical-flow-ish shift by phase correlation)
  ACTION points    per clip, moments of peak motion = where to cut on action (cut mid-movement, continue in the next shot)
Times are in seconds of each source; read the frames (timeline_view.py) before trusting a pair.
"""
import argparse, json, os, subprocess, sys
import numpy as np


def frames(path, fps, w=64, h=36):
    tm = "zscale=t=linear:npl=100,format=gbrpf32le,zscale=p=bt709,tonemap=tonemap=hable:desat=0,zscale=t=bt709:m=bt709:r=tv,"
    trc = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=color_transfer", "-of", "csv=p=0", path],
                         capture_output=True, text=True).stdout.strip()
    vf = (tm if trc in ("arib-std-b67", "smpte2084") else "") + "fps=%g,scale=%d:%d,format=rgb24" % (fps, w, h)
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-vf", vf, "-f", "rawvideo", "-"], capture_output=True).stdout
    a = np.frombuffer(raw, np.uint8).reshape(-1, h, w, 3).astype(np.float32) / 255
    return a


def edges(g):
    gx = np.abs(np.diff(g, axis=1, prepend=g[:, :1])); gy = np.abs(np.diff(g, axis=0, prepend=g[:1, :]))
    e = gx + gy; e = e - e.mean(); return e / (np.linalg.norm(e) + 1e-9)


def hist(f):
    h = np.concatenate([np.histogram(f[..., c], bins=12, range=(0, 1))[0] for c in range(3)]).astype(np.float32)
    return h / (h.sum() + 1e-9)


def shift(a, b):
    F = np.fft.fft2(a) * np.conj(np.fft.fft2(b)); r = np.fft.ifft2(F / (np.abs(F) + 1e-9)).real
    y, x = np.unravel_index(np.argmax(r), r.shape); h, w = a.shape
    return (x if x < w / 2 else x - w), (y if y < h / 2 else y - h)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("clips", nargs="+"); ap.add_argument("--top", type=int, default=8); ap.add_argument("--fps", type=float, default=4)
    ap.add_argument("--out")
    a = ap.parse_args()
    data = {}
    for c in a.clips:
        f = frames(c, a.fps); g = f.mean(-1)
        motion = np.r_[0, np.abs(np.diff(g, axis=0)).mean((1, 2))]
        flow = [(0, 0)] + [shift(g[i], g[i - 1]) for i in range(1, len(g))]
        data[c] = {"f": f, "g": g, "e": [edges(x) for x in g], "h": [hist(x) for x in f], "motion": motion, "flow": flow}
    res = {"graphic": [], "movement": [], "action": {}}
    for A in a.clips:
        dA = data[A]; n = len(dA["g"]); tail = range(max(0, n - int(3 * a.fps)), n)    # last 3 s of A
        for B in a.clips:
            if A == B: continue
            dB = data[B]
            for i in tail:
                for j in range(len(dB["g"])):
                    s = float((dA["e"][i] * dB["e"][j]).sum()); hc = float(np.minimum(dA["h"][i], dB["h"][j]).sum())
                    res["graphic"].append((round(s * 0.8 + hc * 0.2, 3), os.path.basename(A), round(i / a.fps, 2), os.path.basename(B), round(j / a.fps, 2)))
                    fa, fb = dA["flow"][i], dB["flow"][j]
                    ma, mb = np.hypot(*fa), np.hypot(*fb)
                    if ma > 1 and mb > 1:
                        cos = (fa[0] * fb[0] + fa[1] * fb[1]) / (ma * mb)
                        res["movement"].append((round(float(cos) * min(ma, mb), 2), os.path.basename(A), round(i / a.fps, 2), os.path.basename(B), round(j / a.fps, 2)))
        m = dA["motion"]; idx = np.argsort(m)[::-1]; picks = []
        for k in idx:
            if all(abs(k - p) > a.fps * 1.5 for p in picks): picks.append(int(k))
            if len(picks) >= 4: break
        res["action"][os.path.basename(A)] = [round(p / a.fps, 2) for p in sorted(picks)]
    for key in ("graphic", "movement"):
        res[key] = sorted(res[key], reverse=True)[:a.top]
    print("GRAPHIC match candidates (score, out-clip @ t -> in-clip @ t):")
    for r in res["graphic"]: print("  %.3f  %s @ %.2f  ->  %s @ %.2f" % r)
    print("MOVEMENT match candidates (same direction of motion):")
    for r in res["movement"]: print("  %.2f  %s @ %.2f  ->  %s @ %.2f" % r)
    print("CUT-ON-ACTION points (peak motion per clip):")
    for k, v in res["action"].items(): print("  %s: %s" % (k, ", ".join("%.2f" % x for x in v)))
    if a.out: json.dump(res, open(a.out, "w"), indent=1)


if __name__ == "__main__":
    main()
