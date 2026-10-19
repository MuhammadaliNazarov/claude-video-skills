#!/usr/bin/env python3
"""split-edits.py: J-cuts and L-cuts on an engine EDL (the picture cuts where the EDL says, the sound does not).

Add `"split": N` to a range in edl.json (seconds, applies to the cut INTO that range):
  N > 0  J-cut: this range's audio starts N s early, under the previous shot (hear it before you see it)
  N < 0  L-cut: the previous range's audio runs |N| s into this shot (keep hearing it after the cut)
The source needs N s of handle before/after the in/out points (it is taken from the source file).

Run AFTER render.py (it reuses clips_graded/ or clips_draft/ for the picture):
  python3 split-edits.py edit/edl.json --clips edit/clips_draft -o edit/review_split.mp4
Audio: per-range pieces with 30 ms fades, concatenated; total length = picture length. Loudness/captions as usual after.
Captions follow the SOUND: build them from the same split times (`--words-out` writes them).
"""
import argparse, glob, json, os, subprocess, sys, tempfile


def dur(p):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p],
                                capture_output=True, text=True).stdout.strip())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("edl"); ap.add_argument("--clips", required=True); ap.add_argument("-o", required=True)
    ap.add_argument("--words-out", help="write output-time words (following the audio) for ig-captions --words")
    a = ap.parse_args()
    edl = json.load(open(a.edl)); edit = os.path.dirname(os.path.abspath(a.edl)); R = edl["ranges"]
    segs = sorted(glob.glob(os.path.join(a.clips, "seg_*.mp4")))
    if len(segs) != len(R): sys.exit("clips (%d) do not match ranges (%d): render the EDL first" % (len(segs), len(R)))
    vd = [dur(s) for s in segs]
    d = [0.0] + [float(r.get("split", 0)) for r in R[1:]] + [0.0]          # d[i] = shift at the cut into range i
    tmp = tempfile.mkdtemp(); pieces = []; words = []; t_out = 0.0
    for i, r in enumerate(R):
        src = edl["sources"][r["source"]]; src = src if os.path.isabs(src) else os.path.join(edit, src)
        a_in = float(r["start"]) - d[i]; a_len = vd[i] + d[i] - d[i + 1]
        if a_in < 0 or a_len <= 0.06: sys.exit("range %d: split leaves no audio or needs handle before 0 s" % i)
        p = os.path.join(tmp, "a%02d.wav" % i)
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", "%.3f" % a_in, "-t", "%.3f" % a_len, "-i", src, "-vn",
                        "-af", "afade=t=in:d=0.03,afade=t=out:st=%.3f:d=0.03" % (a_len - 0.03), "-ar", "48000", "-ac", "2", p], check=True)
        pieces.append(p)
        tp = os.path.join(edit, "transcripts", r["source"] + ".json")
        if a.words_out and os.path.exists(tp):
            for w in json.load(open(tp))["words"]:
                if w.get("type", "word") != "word": continue
                if w["start"] >= a_in and w["start"] < a_in + a_len:
                    words.append({"text": w["text"], "start": round(w["start"] - a_in + t_out, 3), "end": round(min(w["end"], a_in + a_len) - a_in + t_out, 3)})
        t_out += a_len
    lst = os.path.join(tmp, "list.txt"); open(lst, "w").write("".join("file '%s'\n" % p for p in pieces))
    vlst = os.path.join(tmp, "v.txt"); open(vlst, "w").write("".join("file '%s'\n" % os.path.abspath(s) for s in segs))
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", vlst, "-f", "concat", "-safe", "0", "-i", lst,
                    "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "256k", "-shortest", "-movflags", "+faststart", a.o], check=True)
    if a.words_out: json.dump({"words": words}, open(a.words_out, "w"), indent=0)
    n = sum(1 for x in d[1:-1] if x)
    print("split edits: %d (J %d, L %d) -> %s" % (n, sum(1 for x in d if x > 0), sum(1 for x in d if x < 0), a.o))


if __name__ == "__main__":
    main()
