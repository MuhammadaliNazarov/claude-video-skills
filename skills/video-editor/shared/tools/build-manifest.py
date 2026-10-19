#!/usr/bin/env python3
"""build-manifest.py: index your own sound effects or music so the skills can use them.

  $VU_PY build-manifest.py sfx   [--dir shared/sfx]     # writes shared/sfx/manifest.json   (duration, peak_at)
  $VU_PY build-manifest.py music [--dir shared/music]   # writes shared/music/manifest.json (bpm, drop_at, best_window)

Files are found recursively (wav/mp3/m4a/aac/flac/ogg). Re-running keeps tags you edited by hand (mood, contexts,
vocals, title, artist) for files that are still there. Music `best_window` here is the loudest 15 s; replace it with
YouTube's "most replayed" window if you know it.
"""
import argparse, json, os, sys
import numpy as np
import librosa

EXT = (".wav", ".mp3", ".m4a", ".aac", ".flac", ".ogg")
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
KEEP = ("category", "mood", "contexts", "vocals", "title", "artist", "best_window", "source")


def files(d):
    for base, _, names in os.walk(d):
        for n in sorted(names):
            if n.lower().endswith(EXT):
                yield os.path.relpath(os.path.join(base, n), d)


def sfx_entry(path):
    y, sr = librosa.load(path, sr=22050, mono=True)
    return {"duration": round(len(y) / sr, 3), "peak_at": round(float(np.argmax(np.abs(y))) / sr, 3)}


def music_entry(path, win=15.0):
    y, sr = librosa.load(path, sr=22050, mono=True)
    dur = len(y) / sr
    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
    hop = 512
    rms = librosa.feature.rms(y=y, hop_length=hop)[0]
    t = librosa.frames_to_time(np.arange(len(rms)), sr=sr, hop_length=hop)
    sm = np.convolve(rms, np.ones(43) / 43, mode="same")             # ~1 s smoothing
    jump = np.diff(sm, prepend=sm[0])
    drop = float(t[int(np.argmax(jump))])
    n = max(1, int(win * sr / hop))
    if len(rms) > n:
        csum = np.convolve(rms, np.ones(n), mode="valid")
        s = float(t[int(np.argmax(csum))])
    else:
        s = 0.0
    return {"duration": round(dur, 2), "bpm": round(float(np.atleast_1d(tempo)[0]), 1), "drop_at": round(drop, 2),
            "best_window": [round(s, 2), round(min(dur, s + win), 2)]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("kind", choices=["sfx", "music"])
    ap.add_argument("--dir")
    a = ap.parse_args()
    d = os.path.abspath(a.dir or os.path.join(ROOT, a.kind))
    out = os.path.join(d, "manifest.json")
    old = {}
    if os.path.exists(out):
        prev = json.load(open(out))
        old = {e["file"]: e for e in (prev if isinstance(prev, list) else prev.get("sounds", []))}
    rows = []
    for i, rel in enumerate(files(d), 1):
        p = os.path.join(d, rel)
        try:
            e = sfx_entry(p) if a.kind == "sfx" else music_entry(p)
        except Exception as ex:  # unreadable file: report it, keep going
            print("skip %s (%s)" % (rel, ex), file=sys.stderr)
            continue
        e = {"id": os.path.splitext(rel)[0].replace(os.sep, "/"), "file": rel, **e}
        if a.kind == "sfx":
            e["category"] = os.path.dirname(rel).split(os.sep)[0] or "core"
        if a.kind == "music":
            e.update({"title": os.path.splitext(os.path.basename(rel))[0], "artist": "", "mood": "",
                      "contexts": [os.path.dirname(rel)] if os.path.dirname(rel) else [], "vocals": "unknown"})
        for k in KEEP:
            if k in old.get(rel, {}):
                e[k] = old[rel][k]
        rows.append(e)
        print("%-40s %s" % (rel, {k: e[k] for k in e if k in ("duration", "peak_at", "bpm", "drop_at")}))
    json.dump(rows, open(out, "w"), indent=1)
    print("wrote %s (%d files)" % (out, len(rows)))


if __name__ == "__main__":
    main()
