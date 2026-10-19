#!/usr/bin/env python3
"""ig-captions.py: word-timed Instagram captions as an .ass file, plus an optional burn.

Styles (pick by the vibe; see PRESET.md "Caption styles"):
  red-white      ONE word at a time, white, tight heavy sans, soft dark halo, key word red   (the default; reference: Kallaway)
  red-black      ONE word at a time, black word on a red box                                   (loud, poppy)
  red            ONE word at a time, every word red with a soft black halo                     (dark footage, drama)
  cyan-white     white words, the key word cyan     (tech, business, clean, cool, night)
  yellow-white   white words, the key word yellow   (energy, lifestyle, warm, hype)
  doc-yellow     the whole line pale yellow, sentence case, thin outline (documentary, story, cinematic, calm)
  yellow         every word lemon yellow, bold      (loud hooks, one-word punches)

Timing comes from either:
  --edl   an engine edl.json (+ its edit/transcripts/*.json): output time = word.start - seg.start + seg offset
  --words a {"words":[{text,start,end}]} file already in OUTPUT time (a flat cut; scribe-words.py makes these)

Key words: --em "money,never,3" (case-insensitive, punctuation ignored), or --em-file JSON list of output times
(a word whose start is within 0.05 s of a listed time is the key word). Numbers are always key words.

Usage:
  python3 ig-captions.py --edl edit/edl.json --style cyan-white --em "free,today" --out edit/captions.ass
  python3 ig-captions.py --words flat-words.json --style doc-yellow --out edit/captions.ass --burn edit/final.mp4 edit/final-captioned.mp4
"""
import argparse, json, os, re, subprocess, sys

FONTS = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "fonts"))

# ASS colours are &HAABBGGRR
WHITE, CYAN, LEMON, DOC = "&H00FFFFFF", "&H00FFE500", "&H005CF2F4", "&H00A6E8F3"   # #FFFFFF #00E5FF #F4F25C #F3E8A6
RED, BLACK = "&H002A2AFF", "&H000A0A0A"                                                  # #FF2A2A #0A0A0A
# one-word styles (the Kallaway look): tight tracking, punctuation kept, each word held until the next starts, no pop.
#   border 1 = outline+shadow, 3 = opaque box (OutlineColour is the box). halo = \blur on the outline for a soft shadow.
ONE_WORD = {
    #             font             size  primary em     outline_colour  border outline spacing halo
    "red-white": ("Inter Black",     86, WHITE, RED,   "&H80000000",   1,     3.0,    -3.2,  6),
    "red-black": ("Inter Black",     76, BLACK, WHITE, RED,            3,     16.0,   -2.2,  0),
    "red":       ("Inter Black",     86, RED,   WHITE, "&H70000000",   1,     3.0,    -3.2,  6),
}
STYLES = {
    #               font                size bold  primary  em     outline shadow  words  case
    "cyan-white":   ("Montserrat ExtraBold", 86, 0, WHITE, CYAN,  4.0, 2.0, 3, "natural"),
    "yellow-white": ("Montserrat ExtraBold", 86, 0, WHITE, LEMON, 4.0, 2.0, 3, "natural"),
    "yellow":       ("Anton",               118, 0, LEMON, WHITE, 4.5, 2.0, 2, "upper"),
    "doc-yellow":   ("Inter Medium",         54, 0, DOC,   DOC,   1.6, 1.0, 7, "natural"),
}
# vertical positions (MarginV from the bottom of a 1920 frame). Instagram's caption/username/audio UI covers roughly the
# bottom 420 px and the right rail ~150 px; the top ~220 px holds the header. "lower" sits just above the UI.
POS = {"lower": 520, "middle": 680, "ref": 650, "upper": 1300}   # ref = the reference's spot, 64% down the frame
PUNCT_BREAK = set(".,!?;:")


def ts(t):
    t = max(0.0, t); cs = int(round(t * 100))
    h, cs = divmod(cs, 360000); m, cs = divmod(cs, 6000); s, cs = divmod(cs, 100)
    return "%d:%02d:%02d.%02d" % (h, m, s, cs)


def words_from_edl(edl_path):
    edl = json.load(open(edl_path)); edit = os.path.dirname(os.path.abspath(edl_path)); out, off = [], 0.0
    for r in edl["ranges"]:
        a, b = float(r["start"]), float(r["end"])
        tp = os.path.join(edit, "transcripts", r["source"] + ".json")
        if os.path.exists(tp):
            for w in json.load(open(tp)).get("words", []):
                if w.get("type", "word") != "word" or w.get("start") is None: continue
                if w["end"] <= a or w["start"] >= b: continue
                out.append({"text": w["text"].strip(), "start": max(a, w["start"]) - a + off, "end": min(b, w["end"]) - a + off})
        else:
            print("  no transcript for %s, no captions in that range" % r["source"])
        off += b - a
    return out


def chunk(words, max_words, max_s=1.6, pause=0.3):
    cues, cur = [], []
    for i, w in enumerate(words):
        cur.append(w); nxt = words[i + 1] if i + 1 < len(words) else None
        gap = (nxt["start"] - w["end"]) if nxt else 0
        if (nxt is None or w["text"][-1:] in PUNCT_BREAK or gap >= pause or len(cur) >= max_words
                or w["end"] - cur[0]["start"] >= max_s):
            cues.append(cur); cur = []
    return cues


def main():
    ap = argparse.ArgumentParser()
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--edl"); src.add_argument("--words")
    ap.add_argument("--style", default="red-white", choices=sorted(list(STYLES) + list(ONE_WORD)))
    ap.add_argument("--pos", default=None, choices=sorted(POS), help="default: lower (doc-yellow) / middle (others)")
    ap.add_argument("--em", default="", help="comma list of key words")
    ap.add_argument("--em-file", help="JSON list of output-time word starts to highlight")
    ap.add_argument("--margin-v", type=int, default=None, help="exact distance from the bottom (1920 frame); overrides --pos")
    ap.add_argument("--max-words", type=int, default=None)
    ap.add_argument("--size", type=int, default=None)
    ap.add_argument("--width", type=int, default=1080); ap.add_argument("--height", type=int, default=1920)
    ap.add_argument("--no-pop", action="store_true", help="no scale-in on each cue")
    ap.add_argument("--out", required=True)
    ap.add_argument("--burn", nargs=2, metavar=("IN", "OUT"), help="burn the captions into IN -> OUT (audio copied)")
    a = ap.parse_args()

    one = a.style in ONE_WORD
    if one:
        font, size, prim, emc, ocol, bstyle, outl, spacing, halo = ONE_WORD[a.style]
        bold, shad, mw, case = 0, 0.0, 1, "natural"
    else:
        font, size, bold, prim, emc, outl, shad, mw, case = STYLES[a.style]
        ocol, bstyle, spacing, halo = "&H00000000", 1, 0, 0
    size = a.size or size; mw = a.max_words or mw
    scale = a.height / 1920.0
    pos = a.pos or ("lower" if a.style == "doc-yellow" else "ref" if one else "middle")
    margin_v = int(POS[pos] * scale) if a.height > a.width else int(70 * scale)   # 16:9: documentary sits low
    if a.margin_v is not None: margin_v = int(a.margin_v * scale)
    words = words_from_edl(a.edl) if a.edl else [
        {"text": w["text"].strip(), "start": float(w["start"]), "end": float(w["end"])}
        for w in (lambda j: j["words"] if isinstance(j, dict) else j)(json.load(open(a.words)))]
    words = [w for w in words if w["text"]]
    if not words: sys.exit("no words to caption")

    norm = lambda t: re.sub(r"[^\w$%]", "", t.lower())
    em_words = {norm(x) for x in a.em.split(",") if x.strip()}
    em_times = json.load(open(a.em_file)) if a.em_file else []
    is_em = lambda w: (norm(w["text"]) in em_words or bool(re.search(r"\d", w["text"]))
                       or any(abs(w["start"] - t) < 0.05 for t in em_times))

    lines = ["[Script Info]", "ScriptType: v4.00+", "PlayResX: %d" % a.width, "PlayResY: %d" % a.height,
             "WrapStyle: 0", "ScaledBorderAndShadow: yes", "", "[V4+ Styles]",
             "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, "
             "Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, "
             "MarginR, MarginV, Encoding",
             "Style: Cap,%s,%d,%s,%s,%s,&H64000000,%d,0,0,0,100,100,%.1f,0,%d,%.1f,%.1f,2,%d,%d,%d,1"
             % (font, int(size * scale), prim, prim, ocol, -1 if bold else 0, spacing * scale, bstyle, outl * scale,
                shad * scale, int(90 * scale), int(170 * scale), margin_v),   # right margin clears the like/comment rail
             "", "[Events]", "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text"]
    pop = "" if (a.no_pop or one or a.style == "doc-yellow") else r"{\fscx86\fscy86\t(0,90,\fscx100\fscy100)}"
    if halo: pop = (r"{\blur%d}" % halo) + pop
    cues = chunk(words, mw)
    for i, c in enumerate(cues):
        start = c[0]["start"]
        end = max(c[-1]["end"], start + 0.35)
        if one and i + 1 < len(cues) and cues[i + 1][0]["start"] - c[-1]["end"] < 0.6:
            end = cues[i + 1][0]["start"]                       # one-word: the word stays until the next one replaces it
        elif i + 1 < len(cues): end = min(end + 0.12, cues[i + 1][0]["start"])   # hold a beat, never overlap the next cue
        parts = []
        for w in c:
            t = w["text"].upper() if case == "upper" else w["text"]
            if a.style != "doc-yellow" and not one: t = t.rstrip(",;:.") if not t.endswith("...") else t
            t = t.replace("{", "(").replace("}", ")")
            parts.append(r"{\c%s}%s{\c%s}" % (emc, t, prim) if (is_em(w) and emc != prim) else t)
        lines.append("Dialogue: 0,%s,%s,Cap,,0,0,0,,%s%s" % (ts(start), ts(end), pop, " ".join(parts)))
    open(a.out, "w").write("\n".join(lines) + "\n")
    print("captions: %d cues, style %s, %s -> %s" % (len(cues), a.style, pos, a.out))

    if a.burn:
        src_v, dst = a.burn
        esc = lambda p: p.replace("\\", "\\\\").replace(":", r"\:").replace("'", r"\'")
        vf = "ass='%s':fontsdir='%s'" % (esc(os.path.abspath(a.out)), esc(FONTS))
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", src_v, "-vf", vf, "-c:v", "libx264", "-preset", "medium",
                        "-crf", "17", "-pix_fmt", "yuv420p", "-color_primaries", "bt709", "-color_trc", "bt709",
                        "-colorspace", "bt709", "-c:a", "copy", "-movflags", "+faststart", dst], check=True)
        print("burned -> %s" % dst)


if __name__ == "__main__":
    main()
