#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""draw.py — the raster pictures, computed. No photographs, no stock.

    hero.jpg         the Ulam spiral: the whole numbers wound into a square spiral, the primes lit
    band-sieve.jpg   Eratosthenes as stripes — each small prime's multiples in its own colour
    band-zeros.jpg   the critical strip, |zeta(s)| as brightness, the zeros as dark wells
    band-curve.jpg   an elliptic curve over the reals, with a chord and a tangent
    band-wave.jpg    a^x mod N as a bar field, the period showing as a beat
    card.jpg         the share card, 1200×630

    python3 tools/draw.py            # all, into build/img/
    python3 tools/draw.py hero       # one
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

sys.path.insert(0, str(Path(__file__).resolve().parent))
from compute import sieve, zeta   # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "build" / "img"

NAVY = np.array([0.04, 0.04, 0.07])
AMBER = np.array([1.00, 0.70, 0.28])
TEAL = np.array([0.37, 0.83, 0.78])
ROSE = np.array([1.00, 0.48, 0.71])
VIOLET = np.array([0.72, 0.61, 1.00])
CREAM = np.array([0.95, 0.93, 0.89])


def save(img, name, quality=86):
    OUT.mkdir(parents=True, exist_ok=True)
    arr = (np.clip(img, 0, 1) * 255).astype(np.uint8)
    Image.fromarray(arr).save(OUT / name, quality=quality, optimize=True, progressive=True)
    print(f"  {name}  {arr.shape[1]}×{arr.shape[0]}")


def vignette(w, h, strength=0.5):
    yy, xx = np.mgrid[0:h, 0:w]
    r = np.hypot((xx - w / 2) / (w / 2), (yy - h / 2) / (h / 2))
    return 1 - strength * np.clip(r - 0.4, 0, 1) ** 1.5


def glow(mask, sigma):
    """A soft halo around a boolean mask, via PIL's blur."""
    im = Image.fromarray((mask * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(sigma))
    return np.asarray(im, dtype=np.float32) / 255


# ------------------------------------------------------------------ hero: the Ulam spiral
def ulam(cols, rows):
    """Number the cells of a cols×rows grid along a square spiral from the centre; return
    the array of numbers."""
    grid = np.zeros((rows, cols), dtype=np.int64)
    cx, cy = cols // 2, rows // 2
    x, y, n = cx, cy, 1
    grid[y, x] = n
    step = 1
    dirs = [(1, 0), (0, -1), (-1, 0), (0, 1)]
    d = 0
    total = cols * rows
    while n < total * 3:
        for _ in range(2):
            dx, dy = dirs[d % 4]
            for _ in range(step):
                x += dx
                y += dy
                n += 1
                if 0 <= x < cols and 0 <= y < rows:
                    grid[y, x] = n
            d += 1
        step += 1
        if abs(x - cx) > cols and abs(y - cy) > rows:
            break
    return grid


def hero(w=2000, h=1000, cell=4):
    cols, rows = w // cell, h // cell
    grid = ulam(cols, rows)
    s = sieve(int(grid.max()) + 1)
    prime = s[grid]
    img = np.tile(NAVY.astype(np.float32) * 0.9, (h, w, 1))
    mask = np.kron(prime.astype(np.float32), np.ones((cell, cell), np.float32))[:h, :w]
    # a dot per prime, slightly inset, plus a halo so the diagonals read from across the room
    dots = np.kron(prime.astype(np.float32), np.pad(np.ones((cell - 1, cell - 1), np.float32), ((0, 1), (0, 1))))[:h, :w]
    halo = glow(mask > 0, 9)
    img += halo[..., None] * (AMBER * 0.35)
    img += dots[..., None] * (AMBER * 0.85 + CREAM * 0.15)
    # a faint teal wash toward the edges so the middle is the brightest place
    img *= vignette(w, h, 0.55)[..., None]
    return img


# ------------------------------------------------------------------ the sieve as stripes
def band_sieve(w=2000, h=700):
    img = np.tile(NAVY.astype(np.float32), (h, w, 1))
    primes = [2, 3, 5, 7, 11, 13, 17, 19]
    colours = [AMBER, TEAL, ROSE, VIOLET, AMBER * 0.7 + TEAL * 0.3, TEAL * 0.5 + ROSE * 0.5, VIOLET * 0.6 + AMBER * 0.4, CREAM * 0.8]
    N = 420
    colw = w / N
    rowh = h / (len(primes) + 1)
    yy, xx = np.mgrid[0:h, 0:w]
    n = (xx / colw).astype(int) + 1
    for i, (p, c) in enumerate(zip(primes, colours)):
        band = (yy >= i * rowh + rowh * 0.12) & (yy < (i + 1) * rowh - rowh * 0.12)
        hit = band & (n % p == 0) & (n != p)
        img[hit] = img[hit] * 0.3 + c * 0.55
        own = band & (n == p)
        img[own] = CREAM
    # the last row: what survives
    s = sieve(N + 1)
    band = yy >= len(primes) * rowh + rowh * 0.12
    left = band & s[np.clip(n, 0, N)]
    img[left] = img[left] * 0.2 + AMBER * 0.9
    img *= vignette(w, h, 0.35)[..., None]
    return img


# ------------------------------------------------------------------ the critical strip
def band_zeros(w=2000, h=700):
    # sigma across the width (from -0.5 to 1.5), t up the height (from 0 to 60)
    tmax = 60.0
    sig = np.linspace(-0.4, 1.4, 360)
    ts = np.linspace(2.0, tmax, 700)
    mag = np.zeros((len(ts), len(sig)), np.float32)
    for j, sg in enumerate(sig):
        for i, t in enumerate(ts):
            mag[i, j] = abs(zeta(complex(sg, t), N=90, m=10))
    v = np.log10(mag + 1e-6)
    v = (v - v.min()) / (v.max() - v.min())
    # sit the strip sideways so t runs along the band
    v = v.T[::-1]                      # sigma down the height, t across the width
    v = np.asarray(Image.fromarray((v * 255).astype(np.uint8)).resize((w, h), Image.BILINEAR), np.float32) / 255
    img = np.zeros((h, w, 3), np.float32)
    # dark where zeta is small (the zeros), amber where it is large
    img += NAVY * (1 - v)[..., None] * 1.2
    img += (TEAL * 0.6 + NAVY * 0.4)[None, None, :] * (v ** 1.6)[..., None]
    img += AMBER[None, None, :] * (np.clip(v - 0.72, 0, 1) * 2.2)[..., None]
    # the critical line sigma = 1/2
    row = int((1.4 - 0.5) / 1.8 * h)
    img[row - 1:row + 2, :] = img[row - 1:row + 2, :] * 0.4 + ROSE * 0.6
    img *= vignette(w, h, 0.3)[..., None]
    return img


# ------------------------------------------------------------------ an elliptic curve
def band_curve(w=2000, h=700):
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    x = (xx - w * 0.5) / (w * 0.13)
    y = -(yy - h * 0.5) / (h * 0.16)
    a, b = -3.0, 3.0
    f = y * y - (x ** 3 + a * x + b)
    grad = np.hypot(2 * y, 3 * x * x + a) + 1e-3
    dist = np.abs(f) / grad
    line = np.exp(-(dist / 0.04) ** 2)
    halo = np.exp(-(dist / 0.35) ** 2) * 0.25
    img = np.tile(NAVY.astype(np.float32), (h, w, 1))
    img += (halo + line)[..., None] * AMBER
    # a chord through two points on the curve and its third crossing
    def ycurve(px, sign=1):
        return sign * math.sqrt(max(px ** 3 + a * px + b, 0))
    P = (-1.6, ycurve(-1.6))
    Q = (0.4, ycurve(0.4))
    m = (Q[1] - P[1]) / (Q[0] - P[0])
    c = P[1] - m * P[0]
    d = np.abs(y - (m * x + c)) / math.sqrt(1 + m * m)
    img += (np.exp(-(d / 0.03) ** 2) * ((x > -2.6) & (x < 3.2)))[..., None] * TEAL * 0.9
    x3 = m * m - P[0] - Q[0]
    y3 = m * x3 + c
    for (px, py, col) in ((P[0], P[1], AMBER), (Q[0], Q[1], AMBER), (x3, y3, ROSE), (x3, -y3, ROSE)):
        r = np.hypot(x - px, y - py)
        img += np.exp(-(r / 0.09) ** 2)[..., None] * col
    # the vertical flip
    d2 = np.abs(x - x3)
    img += (np.exp(-(d2 / 0.02) ** 2) * ((y > -abs(y3) - 0.1) & (y < abs(y3) + 0.1)))[..., None] * ROSE * 0.6
    img *= vignette(w, h, 0.35)[..., None]
    return img


# ------------------------------------------------------------------ the period as a beat
def band_wave(w=2000, h=700):
    N, a = 143, 3          # 11 × 13; 3 has order 30 mod 143... any order shows as a beat
    seq = []
    v = 1
    for _ in range(160):
        seq.append(v)
        v = v * a % N
    img = np.tile(NAVY.astype(np.float32), (h, w, 1))
    bw = w / len(seq)
    yy, xx = np.mgrid[0:h, 0:w]
    k = (xx / bw).astype(int)
    vals = np.array(seq)[np.clip(k, 0, len(seq) - 1)]
    height = vals / N * (h * 0.8)
    bar = (yy > h - height - h * 0.1) & (yy < h * 0.9) & ((xx % bw) > 1.5)
    ones = vals == 1
    col = np.where(ones[..., None], AMBER, TEAL * 0.75)
    img[bar] = img[bar] * 0.3 + col[bar] * 0.8
    halo = glow(bar & ones, 12)
    img += halo[..., None] * AMBER * 0.5
    img *= vignette(w, h, 0.35)[..., None]
    return img


# ------------------------------------------------------------------ the share card
def fonts():
    """The display face on this machine, or the nearest thing the runner has."""
    tries = [("/System/Library/Fonts/Avenir Next Condensed.ttc", 8, 2),
             ("/System/Library/Fonts/Supplemental/Arial Black.ttf", 0, 0),
             ("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 0, 0)]
    for path, ib, ismall in tries:
        try:
            return (ImageFont.truetype(path, 150, index=ib), ImageFont.truetype(path, 36, index=ismall))
        except Exception:  # noqa: BLE001
            continue
    return ImageFont.load_default(), ImageFont.load_default()


def card():
    base = Image.open(OUT / "hero.jpg").convert("RGB")
    W, H = 1200, 630
    im = base.resize((W, int(W * base.height / base.width)), Image.LANCZOS)
    top = (im.height - H) // 2
    im = im.crop((0, top, W, top + H))
    scrim = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(scrim)
    for y in range(H):
        a = int(210 * max(0.0, (y - H * 0.25) / (H * 0.75)) ** 1.1)
        d.line([(0, y), (W, y)], fill=(6, 6, 12, a))
    im = Image.alpha_composite(im.convert("RGBA"), scrim).convert("RGB")
    d = ImageDraw.Draw(im)
    big, small = fonts()
    d.text((56, 250), "BIG NUMBERS,", font=big, fill=(243, 239, 230))
    d.text((56, 382), "SPLIT", font=big, fill=(255, 179, 71))
    d.text((60, 556), "factoring, from Eratosthenes to Shor — and what it means for a wallet", font=small, fill=(200, 194, 180))
    d.text((W - 60, 28), "Nan · hongdam.net · CC BY 4.0", font=small, fill=(160, 154, 140), anchor="ra")
    OUT.mkdir(parents=True, exist_ok=True)
    im.save(OUT / "card.jpg", quality=88, optimize=True, progressive=True)
    print(f"  card.jpg  {W}×{H}")


ALL = {"hero": lambda: save(hero(), "hero.jpg"),
       "sieve": lambda: save(band_sieve(), "band-sieve.jpg"),
       "zeros": lambda: save(band_zeros(), "band-zeros.jpg"),
       "curve": lambda: save(band_curve(), "band-curve.jpg"),
       "wave": lambda: save(band_wave(), "band-wave.jpg"),
       "card": card}

if __name__ == "__main__":
    want = sys.argv[1:] or list(ALL)
    for k in want:
        ALL[k]()
