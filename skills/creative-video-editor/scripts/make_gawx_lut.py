#!/usr/bin/env python3
"""make_gawx_lut.py: builds Cine_Gawx.cube and AppleLog_Cine_Gawx.cube into ../luts/ (the Gawx Art film look).

Reuses the curve helpers and the Apple Log decode from the video-editor skill's shared/luts/make_luts.py (read-only).
Run: ~/.claude/skills/video-editor/.venv/bin/python make_gawx_lut.py
"""
import os, sys
import numpy as np
_here = os.path.dirname(os.path.abspath(__file__))
for _p in (os.path.join(_here, "..", "..", "video-editor", "shared", "luts"),
           os.path.expanduser("~/.claude/skills/video-editor/shared/luts")):
    if os.path.exists(os.path.join(_p, "make_luts.py")):
        sys.path.insert(0, os.path.abspath(_p)); break
import make_luts as m
from make_luts import scurve, luma, skin_mask, grid, applelog_to_rec709

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "luts")
# ---- "Cine_Gawx": the Gawx Art "Perfect Imperfection." look (measured 2026-10-13, references/ref02) -------------------
# Low-key film print: dark mids (median luma .14), highlights rolled off to ~.85, deep blacks; cream yellow-green
# highlights, faintly green mids, faintly warm shadows; reds kept rich, greens pushed to teal, yellows toward orange.

def _hsv(rgb):
    mx = rgb.max(-1); mn = rgb.min(-1); d = mx - mn
    r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    h = np.where(d < 1e-9, 0, np.where(mx == r, ((g - b) / np.maximum(d, 1e-9)) % 6,
        np.where(mx == g, (b - r) / np.maximum(d, 1e-9) + 2, (r - g) / np.maximum(d, 1e-9) + 4))) / 6.0
    s = np.where(mx < 1e-9, 0, d / np.maximum(mx, 1e-9))
    return h, s, mx


def _rgb(h, s, v):
    h6 = (h % 1.0) * 6; i = np.floor(h6).astype(int) % 6; f = h6 - np.floor(h6)
    p, q, t = v * (1 - s), v * (1 - s * f), v * (1 - s * (1 - f))
    out = np.choose(i[..., None] * np.ones(3, int), [np.stack(x, -1) for x in
          [(v, t, p), (q, v, p), (p, v, t), (p, q, v), (t, p, v), (v, p, q)]])
    return out


def _band(hdeg, center, width):
    d = np.abs(((hdeg - center) + 180) % 360 - 180)
    return np.clip(1 - d / width, 0, 1) ** 1.5


def look_gawx(rgb, strength=1.0):
    src = rgb
    x = np.clip(rgb, 0, 1) ** 1.38                                   # darker mids (low-key)
    x = scurve(x, 0.22)
    x = 0.008 + x * 0.992
    knee = 0.68                                                       # film shoulder: highlights roll off to ~.86
    x = np.where(x > knee, knee + (1 - np.exp(-(x - knee) / 0.2)) * 0.18, x)
    h, s, v = _hsv(np.clip(x, 0, 1)); hd = h * 360
    g = _band(hd, 110, 50); y = _band(hd, 58, 22); bl = _band(hd, 220, 35); rd = _band(hd, 0, 25)
    hd = hd + g * (172 - 110) * 0.85 + y * (-16) + bl * (-18)        # greens -> teal, yellows -> orange, blues -> cyan
    s = s * (1 - 0.30 * g) * (1 - 0.22 * y) * (1 + 0.10 * rd) * 0.74
    x = _rgb((hd / 360) % 1, np.clip(s, 0, 1), v)
    L = luma(x)[..., None]; sh = np.clip(1 - L / 0.25, 0, 1); hl = np.clip((L - 0.45) / 0.4, 0, 1)
    md = np.clip(1 - np.abs(L - 0.4) / 0.25, 0, 1)
    tint = sh * np.array([0.004, 0.006, 0.010]) + md * np.array([-0.008, 0.008, -0.004]) \
         + hl * np.array([-0.004, 0.012, -0.060])
    skin = skin_mask(src)[..., None]
    x = x + tint * (1 - 0.5 * skin)
    x = np.clip(x, 0, 1)
    return src + (x - src) * strength


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    m.HERE = os.path.abspath(OUT)
    G = grid()
    m.write("Cine_Gawx", look_gawx(G), "Cine_Gawx (Gawx Art film look)")
    m.write("AppleLog_Cine_Gawx", look_gawx(applelog_to_rec709(G)), "Apple Log to Cine_Gawx")
