#!/usr/bin/env python3
"""music-cut.py: pull a ready-to-use bed from the music library.

  python3 music-cut.py --list [--context educational] [--mood upbeat]     # browse
  python3 music-cut.py educational/track --len 20 -o bed.mp3                            # from the best (most-replayed) window
  python3 music-cut.py emotional-sad/song --len 16 --at drop --lead 4 -o bed.mp3         # land the drop 4 s into the bed
  python3 music-cut.py cinematic/score --len 30 --start 41.5 -o bed.mp3               # exact start

Fades: 0.4 s in, 1.2 s out (change with --fade-in / --fade-out). Output is -16 LUFS-ish (loudnorm I=-16) so the editor
can duck it under a voice; pass --raw to skip leveling.
"""
import argparse, json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
MANIFEST = os.path.join(HERE, "manifest.json")
if not os.path.exists(MANIFEST):
    sys.exit("no music library yet: add tracks to %s, then run shared/tools/build-manifest.py music (see README.md)" % HERE)
LIB = json.load(open(MANIFEST))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("id", nargs="?")
    ap.add_argument("--list", action="store_true"); ap.add_argument("--context"); ap.add_argument("--mood")
    ap.add_argument("--len", type=float, default=20); ap.add_argument("--at", choices=["best", "drop"], default="best")
    ap.add_argument("--lead", type=float, default=0, help="with --at drop: seconds of build before the drop")
    ap.add_argument("--start", type=float); ap.add_argument("--fade-in", type=float, default=0.4)
    ap.add_argument("--fade-out", type=float, default=1.2); ap.add_argument("--raw", action="store_true"); ap.add_argument("-o")
    a = ap.parse_args()
    if a.list:
        for t in LIB:
            if a.context and a.context not in t["contexts"]: continue
            if a.mood and a.mood != t["mood"]: continue
            print("%-5s %-34s %-24s %-12s %5.0f bpm  best %5.1f-%5.1f  %s" % (t["id"], t["title"][:34], t["artist"][:24], t["mood"],
                  t["bpm"], t["best_window"][0], t["best_window"][1], ",".join(t["contexts"])))
        return
    t = next((x for x in LIB if x["id"] == a.id), None)
    if not t: sys.exit("unknown id %s (use --list)" % a.id)
    if a.start is not None: s = a.start
    elif a.at == "drop": s = max(0, t["drop_at"] - a.lead)
    else: s = t["best_window"][0]
    s = min(s, max(0, t["duration"] - a.len))
    out = a.o or "%s-%s.mp3" % (t["id"], int(s))
    af = "afade=t=in:d=%.2f,afade=t=out:st=%.2f:d=%.2f" % (a.fade_in, max(0, a.len - a.fade_out), a.fade_out)
    if not a.raw: af += ",loudnorm=I=-16:TP=-1.5:LRA=11"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", "%.2f" % s, "-t", "%.2f" % a.len, "-i", os.path.join(HERE, t["file"]),
                    "-af", af, "-ar", "48000", "-c:a", "libmp3lame", "-q:a", "2", out], check=True)
    print("%s: %s - %s, %.1f-%.1f s -> %s" % (t["id"], t["title"], t["artist"], s, s + a.len, out))


if __name__ == "__main__":
    main()
