#!/usr/bin/env python3
"""transition-join.py: join clips with a fade, dissolve or smash cut (picture AND sound handled together).

  python3 transition-join.py A.mp4 B.mp4 [C.mp4 ...] --type dissolve --dur 0.8 -o out.mp4
  --type cut | dissolve | fadeblack | fadewhite | smash | wipeleft | slideup | circleopen (any ffmpeg xfade name)
  --types dissolve,cut,fadeblack   one per join instead of one for all
  --head-fade 1.0 / --tail-fade 1.5   fade the whole piece in from / out to black (story start / end)

Meanings (from the cut-types reference): dissolve = time passes / a soft link; fadeblack = a chapter or story ends;
fadewhite = a dream, a memory, a flash; smash = abrupt contrast (loud -> quiet, chaos -> calm): hard picture cut AND the
outgoing sound stops dead (no crossfade), so the silence lands. All inputs must share size and frame rate.
"""
import argparse, json, subprocess, sys


def probe(p):
    j = json.loads(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration:stream=codec_type,r_frame_rate",
                                   "-of", "json", p], capture_output=True, text=True).stdout)
    d = float(j["format"]["duration"]); has_a = any(s["codec_type"] == "audio" for s in j["streams"])
    return d, has_a


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("clips", nargs="+"); ap.add_argument("-o", required=True)
    ap.add_argument("--type", default="dissolve"); ap.add_argument("--types"); ap.add_argument("--dur", type=float, default=0.8)
    ap.add_argument("--head-fade", type=float, default=0); ap.add_argument("--tail-fade", type=float, default=0)
    a = ap.parse_args()
    n = len(a.clips)
    if n < 2 and not (a.head_fade or a.tail_fade): sys.exit("need two or more clips")
    types = a.types.split(",") if a.types else [a.type] * (n - 1)
    if len(types) != n - 1: sys.exit("--types needs %d entries" % (n - 1))
    info = [probe(c) for c in a.clips]
    ins = sum([["-i", c] for c in a.clips], [])
    fv, fa = [], []; vlab, alab = "[0:v]", "[0:a]"; t = info[0][0]
    for i in range(1, n):
        ty = types[i - 1]; D = 0.04 if ty in ("cut", "smash") else a.dur
        xt = "fade" if ty in ("cut", "smash") else ty
        off = t - D
        fv.append("%s[%d:v]xfade=transition=%s:duration=%.3f:offset=%.3f[v%d]" % (vlab, i, xt, D, off, i)); vlab = "[v%d]" % i
        if ty == "smash":                                     # outgoing sound stops dead, incoming starts clean
            fa.append("%s[%d:a]acrossfade=d=0.01:c1=nofade:c2=nofade[a%d]" % (alab, i, i))
        else:
            fa.append("%s[%d:a]acrossfade=d=%.3f:c1=tri:c2=tri[a%d]" % (alab, i, D, i))
        alab = "[a%d]" % i; t = t + info[i][0] - D
    post_v, post_a = [], []
    if a.head_fade: post_v.append("fade=t=in:st=0:d=%.2f" % a.head_fade); post_a.append("afade=t=in:st=0:d=%.2f" % a.head_fade)
    if a.tail_fade: post_v.append("fade=t=out:st=%.3f:d=%.2f" % (t - a.tail_fade, a.tail_fade)); post_a.append("afade=t=out:st=%.3f:d=%.2f" % (t - a.tail_fade, a.tail_fade))
    if post_v: fv.append("%s%s[vf]" % (vlab, ",".join(post_v))); vlab = "[vf]"
    if post_a: fa.append("%s%s[af]" % (alab, ",".join(post_a))); alab = "[af]"
    fc = ";".join(fv + fa) if n > 1 else ";".join(["[0:v]" + ",".join(post_v) + "[vf]", "[0:a]" + ",".join(post_a) + "[af]"])
    if n == 1: vlab, alab = "[vf]", "[af]"
    subprocess.run(["ffmpeg", "-y", "-v", "error", *ins, "-filter_complex", fc, "-map", vlab, "-map", alab, "-c:v", "libx264",
                    "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "256k", "-movflags", "+faststart", a.o], check=True)
    print("joined %d clips (%s) -> %s, %.2f s" % (n, ",".join(types), a.o, t))


if __name__ == "__main__":
    main()
