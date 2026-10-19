#!/usr/bin/env python3
"""cine-finish.py: the cinematic finish in one ffmpeg pass.

  grade (a .cube LUT at a strength) -> halation (warm glow off highlights) -> grain -> vignette
  -> frame (full 9:16, or a 4:5 / 1.37:1 / 2.39:1 picture on black inside the canvas) -> chapter cards (small red caps)

Usage:
  python3 cine-finish.py IN OUT [--lut PATH] [--strength 0.85] [--grain 6] [--halation 0.25] [--vignette 0.6]
                          [--frame full|4x5|137|239] [--res 720|1080|4k] [--cards cards.json] [--hdr]
cards.json: [{"text": "1. THE MOVE", "start": 2.0, "end": 5.0, "pos": "below|bottom|center"}, ...]
Audio is copied. Use --res 720 for the review render, --res 4k for the final (render ladder).
"""
import argparse, json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.abspath(os.path.join(HERE, ".."))
FONT = os.path.expanduser("~/.claude/skills/video-editor/presets/instagram/assets/fonts/Inter-Bold.ttf")
TONEMAP = ("zscale=t=linear:npl=100,format=gbrpf32le,zscale=p=bt709,tonemap=tonemap=hable:desat=0,"
           "zscale=t=bt709:m=bt709:r=tv,format=yuv420p")
FRAMES = {"full": None, "4x5": 4 / 5, "137": 1.37, "239": 2.39}
RES = {"720": (720, 1280), "1080": (1080, 1920), "4k": (2160, 3840)}


def probe(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                          "stream=width,height,color_transfer:stream_side_data=rotation", "-of", "json", path],
                         capture_output=True, text=True).stdout
    st = json.loads(out)["streams"][0]
    w, h = st["width"], st["height"]
    rot = next((sd.get("rotation") for sd in st.get("side_data_list", []) if "rotation" in sd), 0) or 0
    if int(round(float(rot))) % 180:
        w, h = h, w
    return w, h, st.get("color_transfer", "")


def esc(t):
    return t.replace("\\", "\\\\").replace(":", r"\:").replace("'", r"\'").replace("%", r"\%")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("inp"); ap.add_argument("out")
    ap.add_argument("--lut", default=os.path.join(SKILL, "luts", "Cine_Gawx.cube"))
    ap.add_argument("--strength", type=float, default=0.85)
    ap.add_argument("--grain", type=float, default=6)
    ap.add_argument("--halation", type=float, default=0.25)
    ap.add_argument("--vignette", type=float, default=0.6, help="0 = off, 1 = strong")
    ap.add_argument("--frame", default="full", choices=sorted(FRAMES))
    ap.add_argument("--res", default="1080", choices=sorted(RES))
    ap.add_argument("--landscape", action="store_true", help="16:9 canvas instead of 9:16")
    ap.add_argument("--cards")
    ap.add_argument("--hdr", action="store_true", help="force HLG/PQ tone map (auto-detected otherwise)")
    a = ap.parse_args()

    W, H = RES[a.res]
    if a.landscape: W, H = H, W
    sw, sh, trc = probe(a.inp)
    k = W / 1080.0 if not a.landscape else H / 1080.0
    f = []
    if a.hdr or trc in ("arib-std-b67", "smpte2084"):
        f.append(TONEMAP)
    ratio = FRAMES[a.frame]
    if ratio:                                      # the picture box inside the canvas
        bw = W if not a.landscape else int(round(H * ratio / 2) * 2)
        bh = int(round(bw / ratio / 2) * 2)
        if a.landscape: bh = H
        if bh > H: bh = H; bw = int(round(H * ratio / 2) * 2)
    else:
        bw, bh = W, H
    f.append("scale=%d:%d:force_original_aspect_ratio=increase:flags=lanczos,crop=%d:%d" % (bw, bh, bw, bh))
    f.append("format=gbrp")
    if a.lut and a.strength > 0:
        f.append("split[a][b];[b]lut3d=file='%s':interp=tetrahedral[g];[a][g]blend=all_expr='A*%.3f+B*%.3f'"
                 % (esc(a.lut), 1 - a.strength, a.strength))
    if a.halation > 0:                             # highlights -> blurred warm glow -> screen back on
        f.append("split[h0][h1];[h1]curves=all='0/0 0.62/0 1/1',gblur=sigma=%d,colorchannelmixer=rr=1:gg=0.45:bb=0.25[hg];"
                 "[h0][hg]blend=all_mode=screen:all_opacity=%.3f" % (int(18 * k), a.halation))
    f.append("format=yuv420p")
    if a.grain > 0:
        f.append("noise=alls=%d:allf=t" % int(a.grain))
    if a.vignette > 0:
        f.append("vignette=angle=%.3f" % (0.35 + 0.5 * a.vignette))
    if ratio:
        f.append("pad=%d:%d:(ow-iw)/2:(oh-ih)/2:color=black" % (W, H))
    if a.cards:
        size = int(30 * k); box_bottom = (H + bh) // 2
        for c in json.load(open(a.cards)):
            pos = c.get("pos", "below" if ratio and bh < H else "bottom")
            y = {"below": "%d" % (box_bottom + int(40 * k)), "bottom": "h-%d" % int(260 * k), "center": "(h-th)/2"}[pos]
            f.append("drawtext=fontfile='%s':text='%s':fontsize=%d:fontcolor=0xFF2A2A:x=(w-tw)/2:y=%s:"
                     "enable='between(t,%.3f,%.3f)':alpha='if(lt(t,%.3f),(t-%.3f)/0.3,if(gt(t,%.3f),(%.3f-t)/0.3,1))'"
                     % (esc(FONT), esc(c["text"].upper()), size, y, c["start"], c["end"],
                        c["start"] + 0.3, c["start"], c["end"] - 0.3, c["end"]))
    vf = ",".join(f)
    crf = "18" if a.res == "4k" else ("23" if a.res == "720" else "19")
    cmd = ["ffmpeg", "-y", "-v", "error", "-i", a.inp, "-filter_complex", "[0:v]" + vf + "[v]", "-map", "[v]",
           "-map", "0:a?", "-c:v", "libx264", "-preset", "medium", "-crf", crf, "-pix_fmt", "yuv420p",
           "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709", "-c:a", "aac", "-b:a", "256k",
           "-movflags", "+faststart", a.out]
    r = subprocess.run(cmd)
    if r.returncode: sys.exit(r.returncode)
    print("finished -> %s (%dx%d, frame %s, LUT %s @ %.0f%%)" % (a.out, W, H, a.frame, os.path.basename(a.lut), a.strength * 100))


if __name__ == "__main__":
    main()
