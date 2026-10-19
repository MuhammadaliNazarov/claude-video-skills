#!/usr/bin/env python3
"""make_luts.py: builds the .cube LUTs in this folder (33-point, input/output 0..1 RGB).

Technical:
  AppleLog_to_Rec709.cube   Apple Log (Rec.2020 primaries, Apple's published log curve) -> Rec.709 / BT.1886 display,
                            with a soft filmic shoulder instead of a hard clip. Built from the Apple Log Profile white
                            paper constants, not Apple's own LUT file.
Looks (for normal Rec.709 footage, i.e. after the render's HDR->SDR tone map):
  Cine_TealOrange.cube      the classic: cool teal shadows, warm highlights, gentle S-curve, skin protected
  Cine_Film.cube            documentary film: lifted blacks, softer contrast, warm cream highlights, muted greens
  Cine_Moody.cube           dark and cool: deeper mids, blue-teal shadows, low saturation, skin kept warm
Combined (Apple Log straight to a look, one interpolation):
  AppleLog_Cine_TealOrange.cube, AppleLog_Cine_Film.cube, AppleLog_Cine_Moody.cube

Run: ~/.claude/skills/video-editor/.venv/bin/python make_luts.py   (needs numpy)
"""
import os
import numpy as np

N = 33
HERE = os.path.dirname(os.path.abspath(__file__))

# ---- Apple Log decode (Apple Log Profile white paper) ------------------------------------------------
R0, RT, C = -0.05641088, 0.01, 47.28711236
BETA, GAMMA, DELTA = 0.00964052, 0.08550479, 0.69336945
PT = C * (RT - R0) ** 2


def applelog_to_linear(p):
    p = np.asarray(p, dtype=np.float64)
    lo = np.sqrt(np.clip(p, 0, None) / C) + R0
    hi = 2.0 ** ((p - DELTA) / GAMMA) - BETA
    return np.where(p < PT, np.where(p <= 0, R0, lo), hi)


def linear_to_applelog(r):
    r = np.asarray(r, dtype=np.float64)
    lo = C * (np.clip(r, R0, None) - R0) ** 2
    hi = GAMMA * np.log2(np.clip(r, RT, None) + BETA) + DELTA
    return np.where(r < RT, np.where(r < R0, 0.0, lo), hi)


M2020_TO_709 = np.array([[1.660491, -0.587641, -0.072850],
                         [-0.124550, 1.132900, -0.008349],
                         [-0.018151, -0.100579, 1.118730]])


def filmic(x):
    """Narkowicz ACES fit: toe + soft shoulder, 0..inf -> 0..1."""
    x = np.clip(x, 0, None)
    return np.clip((x * (2.51 * x + 0.03)) / (x * (2.43 * x + 0.59) + 0.14), 0, 1)


def applelog_to_rec709(rgb, exposure=0.80):
    lin2020 = applelog_to_linear(rgb)
    lin709 = lin2020 @ M2020_TO_709.T
    # soft gamut compression: pull negative (out of 709) components toward the pixel's luminance
    y = lin709 @ np.array([0.2126, 0.7152, 0.0722])
    mn = lin709.min(axis=-1)
    k = np.where(mn < 0, y / np.maximum(y - mn, 1e-6), 1.0)[..., None]
    lin709 = y[..., None] + (lin709 - y[..., None]) * np.clip(k, 0, 1)
    disp = filmic(np.clip(lin709, 0, None) * exposure)
    return np.clip(disp, 0, 1) ** (1 / 2.4)            # BT.1886 display encoding


# ---- look helpers (display-referred 0..1 RGB) ---------------------------------------------------------
LUMA = np.array([0.2126, 0.7152, 0.0722])


def luma(rgb):
    return rgb @ LUMA


def hue_sat(rgb):
    mx, mn = rgb.max(-1), rgb.min(-1); d = mx - mn
    r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    h = np.where(d < 1e-6, 0,
        np.where(mx == r, ((g - b) / np.maximum(d, 1e-6)) % 6,
        np.where(mx == g, (b - r) / np.maximum(d, 1e-6) + 2, (r - g) / np.maximum(d, 1e-6) + 4))) * 60
    s = np.where(mx < 1e-6, 0, d / np.maximum(mx, 1e-6))
    return h, s


def skin_mask(rgb):
    """1 on skin tones (hue ~5-50 deg, moderate saturation), soft edges."""
    h, s = hue_sat(rgb)
    hm = np.clip(1 - np.abs(h - 25) / 28, 0, 1)
    sm = np.clip((s - 0.08) / 0.12, 0, 1) * np.clip((0.75 - s) / 0.2, 0, 1)
    return hm * sm


def scurve(x, strength, pivot=0.45):
    """Contrast around a pivot with smooth ends (no clipping)."""
    t = np.clip(x, 0, 1)
    lo = pivot * (t / pivot) ** (1 + strength)
    hi = 1 - (1 - pivot) * ((1 - t) / (1 - pivot)) ** (1 + strength)
    return np.where(t < pivot, lo, hi)


def saturate(rgb, amt):
    y = luma(rgb)[..., None]
    return y + (rgb - y) * amt


def hue_band(h, center, width):
    d = np.abs(((h - center) + 180) % 360 - 180)
    return np.clip(1 - d / width, 0, 1)


def look(rgb, contrast, lift, roll, shadow_tint, high_tint, sat, green_sat, skin_keep, gamma=1.0, warm=0.0):
    skin = skin_mask(rgb)[..., None]
    h, _ = hue_sat(rgb)
    x = rgb ** gamma
    x = scurve(x, contrast)
    x = lift + x * (roll - lift)                                # lifted blacks, rolled-off whites
    L = luma(x)[..., None]
    sh = (1 - L) ** 2; hl = L ** 2
    tint = sh * np.array(shadow_tint) + hl * np.array(high_tint) + np.array([warm, warm * 0.4, -warm])
    x = x + tint * (1 - skin * skin_keep)
    g = hue_band(h, 115, 55)[..., None]                       # greens / foliage
    x = saturate(x, sat * (1 - skin * (1 - 1 / max(sat, 1e-3)) * 0.5))
    x = saturate(x, 1 - g * (1 - green_sat))
    return np.clip(x, 0, 1)


LOOKS = {
    "Cine_TealOrange": dict(contrast=0.45, lift=0.015, roll=0.97, shadow_tint=(-0.055, 0.020, 0.070),
                            high_tint=(0.060, 0.018, -0.060), sat=0.90, green_sat=0.62, skin_keep=0.7),
    "Cine_Film":       dict(contrast=0.18, lift=0.055, roll=0.955, shadow_tint=(-0.010, 0.010, 0.022),
                            high_tint=(0.045, 0.030, -0.045), sat=0.82, green_sat=0.70, skin_keep=0.6, warm=0.010),
    "Cine_Moody":      dict(contrast=0.48, lift=0.020, roll=0.93, shadow_tint=(-0.045, 0.012, 0.075),
                            high_tint=(0.010, 0.004, -0.012), sat=0.78, green_sat=0.60, skin_keep=0.8, gamma=1.12),
}


def grid():
    a = np.linspace(0, 1, N)
    b, g, r = np.meshgrid(a, a, a, indexing="ij")              # .cube order: red fastest
    return np.stack([r, g, b], -1).reshape(-1, 3)


def write(name, rgb, title):
    path = os.path.join(HERE, name + ".cube")
    with open(path, "w") as f:
        f.write('TITLE "%s"\n# made by make_luts.py (video-editor)\nLUT_3D_SIZE %d\nDOMAIN_MIN 0 0 0\nDOMAIN_MAX 1 1 1\n' % (title, N))
        for p in rgb:
            f.write("%.6f %.6f %.6f\n" % tuple(p))
    print("wrote", path)


if __name__ == "__main__":
    G = grid()
    tech = applelog_to_rec709(G)
    write("AppleLog_to_Rec709", tech, "Apple Log to Rec.709 (filmic)")
    for name, kw in LOOKS.items():
        write(name, look(G, **kw), name)
        write("AppleLog_" + name, look(tech, **kw), "Apple Log to " + name)
