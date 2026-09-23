#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""figures.py — the SVG charts, drawn from the data files and build/facts.json.

    records.svg    bits of the general-purpose factoring record against the year
    cost.svg       the L[1/3] curve: core-years against key size, anchored on RSA-250
    qubits.svg     the gap: qubits the papers ask for, qubits the machines have
    pi.svg         pi(x) against x/ln x and li(x)
    zeros.svg      Z(t) along the critical line, the first zeros marked
    explicit.svg   psi(x) and the explicit formula with 0, 10, 30, 100 zeros
    exposure.svg   bitcoin in exposed-key outputs, by who counted

Every SVG carries a cc:license block and the credit in <metadata>.
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from compute import Z   # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
BUILD = ROOT / "build"
IMG = BUILD / "img"
F = json.loads((BUILD / "facts.json").read_text(encoding="utf-8"))
EXPL = json.loads((BUILD / "data" / "explicit.json").read_text(encoding="utf-8"))
RECORDS = json.loads((ROOT / "data" / "records.json").read_text(encoding="utf-8"))
EST = json.loads((ROOT / "data" / "estimates.json").read_text(encoding="utf-8"))
MACH = json.loads((ROOT / "data" / "machines.json").read_text(encoding="utf-8"))
WALLET = json.loads((ROOT / "data" / "wallet.json").read_text(encoding="utf-8"))

INK, MUTE, LINE, BG = "#f2ede3", "#9d9689", "#2c2c3a", "#0f0f18"
C0, C1, C2, VIO = "#ffb347", "#5fd3c6", "#ff7ab6", "#b79cff"
FONT = "font-family='Avenir Next, Segoe UI, system-ui, sans-serif'"
MONO = "font-family='ui-monospace, Menlo, Consolas, monospace'"
META = ('<metadata><rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" '
        'xmlns:cc="http://creativecommons.org/ns#" xmlns:dc="http://purl.org/dc/elements/1.1/">'
        '<cc:Work rdf:about=""><dc:creator>Nan, hongdam.net</dc:creator>'
        '<dc:source>https://nanobotco.github.io/factoring/</dc:source>'
        '<cc:license rdf:resource="https://creativecommons.org/licenses/by/4.0/"/></cc:Work>'
        '</rdf:RDF></metadata>')


def svg(w, h, body, title):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
            f'role="img" aria-label="{title}">{META}<title>{title}</title>'
            f'<rect width="{w}" height="{h}" rx="10" fill="{BG}"/>{body}'
            f'<text x="{w - 12}" y="{h - 8}" text-anchor="end" fill="{MUTE}" font-size="11" {FONT}>Nan · hongdam.net · CC BY 4.0</text></svg>')


def write(name, text):
    IMG.mkdir(parents=True, exist_ok=True)
    (IMG / name).write_text(text, encoding="utf-8")
    print(f"  {name}")


def axes(x0, y0, x1, y1, xt, yt, xlab, ylab, xfmt=str, yfmt=str):
    """Axis lines, ticks and labels. xt/yt are (value, position) lists."""
    b = [f'<line x1="{x0}" y1="{y1}" x2="{x1}" y2="{y1}" stroke="{LINE}"/>',
         f'<line x1="{x0}" y1="{y0}" x2="{x0}" y2="{y1}" stroke="{LINE}"/>']
    for v, px in xt:
        b.append(f'<line x1="{px:.1f}" y1="{y0}" x2="{px:.1f}" y2="{y1}" stroke="{LINE}" stroke-dasharray="2 4"/>')
        b.append(f'<text x="{px:.1f}" y="{y1 + 18}" text-anchor="middle" fill="{MUTE}" font-size="12" {MONO}>{xfmt(v)}</text>')
    for v, py in yt:
        b.append(f'<line x1="{x0}" y1="{py:.1f}" x2="{x1}" y2="{py:.1f}" stroke="{LINE}" stroke-dasharray="2 4"/>')
        b.append(f'<text x="{x0 - 8}" y="{py + 4:.1f}" text-anchor="end" fill="{MUTE}" font-size="12" {MONO}>{yfmt(v)}</text>')
    b.append(f'<text x="{(x0 + x1) / 2}" y="{y1 + 38}" text-anchor="middle" fill="{MUTE}" font-size="13" {FONT}>{xlab}</text>')
    b.append(f'<text transform="translate(16 {(y0 + y1) / 2}) rotate(-90)" text-anchor="middle" fill="{MUTE}" font-size="13" {FONT}>{ylab}</text>')
    return "".join(b)


# ------------------------------------------------------------------ records
def records():
    W, H = 960, 480
    x0, y0, x1, y1 = 70, 30, W - 30, H - 60
    rows = sorted(RECORDS["rows"], key=lambda r: r["year"])
    sx = lambda yr: x0 + (yr - 1990) / (2029 - 1990) * (x1 - x0)
    sy = lambda bits: y1 - (bits - 300) / (2100 - 300) * (y1 - y0)
    b = [axes(x0, y0, x1, y1, [(y, sx(y)) for y in range(1990, 2028, 5)], [(v, sy(v)) for v in (512, 768, 1024, 1536, 2048)],
              "year", "bits in the record number")]
    for v, lab, col in ((512, "512 — keys of the 1990s web", MUTE), (1024, "1024 — keys of the 2000s web; still open", C2), (2048, "2048 — keys of today; still open", C2)):
        b.append(f'<line x1="{x0}" y1="{sy(v)}" x2="{x1}" y2="{sy(v)}" stroke="{col}" stroke-width="1.5" stroke-dasharray="6 5"/>')
        b.append(f'<text x="{x0 + 8}" y="{sy(v) - 6}" fill="{col}" font-size="12" {FONT}>{lab}</text>')
    pts = " ".join(f"{sx(r['year']):.1f},{sy(r['bits']):.1f}" for r in rows)
    b.append(f'<polyline points="{pts}" fill="none" stroke="{C1}" stroke-width="2"/>')
    for r in rows:
        new = r["year"] > 2026
        b.append(f'<circle cx="{sx(r["year"]):.1f}" cy="{sy(r["bits"]):.1f}" r="{6 if new else 4}" fill="{C0 if new else C1}"/>')
        if r["name"] in ("RSA-129", "RSA-155", "RSA-768", "RSA-250"):
            b.append(f'<text x="{sx(r["year"]) + 8:.1f}" y="{sy(r["bits"]) + 4:.1f}" fill="{INK}" font-size="12" {MONO}>{r["name"]}</text>')
    b.append(f'<text x="{sx(2026.7) - 10:.1f}" y="{sy(896) - 12:.1f}" text-anchor="end" fill="{C0}" font-size="12" {MONO}>RSA-260 and RSA-896, Sept 2026</text>')
    b.append(f'<text x="{x1 - 8}" y="{y1 - 10}" text-anchor="end" fill="{MUTE}" font-size="12" {FONT}>general-purpose records only; the amber dots are September 2026</text>')
    write("records.svg", svg(W, H, "".join(b), "Factoring records by year, 1991 to 2026, in bits"))


# ------------------------------------------------------------------ cost
def cost():
    W, H = 960, 480
    x0, y0, x1, y1 = 80, 30, W - 30, H - 60
    rows = F["cost"]["rows"]
    L = lambda bits: (64 / 9) ** (1 / 3) * (bits * math.log(2)) ** (1 / 3) * math.log(bits * math.log(2)) ** (2 / 3) / math.log(10)
    anchor = F["cost"]["anchor"]
    cy = lambda bits: math.log10(anchor["core_years"]) + L(bits) - L(anchor["bits"])
    sx = lambda bits: x0 + (bits - 400) / (4200 - 400) * (x1 - x0)
    sy = lambda lg: y1 - (lg + 2) / (14 + 2) * (y1 - y0)
    b = [axes(x0, y0, x1, y1, [(v, sx(v)) for v in (512, 1024, 2048, 3072, 4096)], [(v, sy(v)) for v in range(-2, 15, 2)],
              "key size in bits", "core-years, powers of ten", yfmt=lambda v: f"10^{v}")]
    pts = " ".join(f"{sx(bts):.1f},{sy(cy(bts)):.1f}" for bts in range(400, 4201, 25))
    b.append(f'<polyline points="{pts}" fill="none" stroke="{C0}" stroke-width="2.5"/>')
    for r in rows:
        if r["bits"] in (512, 768, 1024, 2048, 4096):
            b.append(f'<circle cx="{sx(r["bits"]):.1f}" cy="{sy(math.log10(r["core_years"])):.1f}" r="5" fill="{C0}"/>')
            lab = f'{r["bits"]}: {r["core_years"]:.2g}'
            b.append(f'<text x="{sx(r["bits"]) + 9:.1f}" y="{sy(math.log10(r["core_years"])) + 4:.1f}" fill="{INK}" font-size="12" {MONO}>{lab}</text>')
    b.append(f'<circle cx="{sx(829):.1f}" cy="{sy(math.log10(2700)):.1f}" r="7" fill="none" stroke="{C2}" stroke-width="2"/>')
    b.append(f'<text x="{sx(829) - 10:.1f}" y="{sy(math.log10(2700)) + 22:.1f}" text-anchor="end" fill="{C2}" font-size="12" {FONT}>RSA-250, 2,700 core-years — the anchor</text>')
    b.append(f'<text x="{x0 + 8}" y="{y0 + 14}" fill="{MUTE}" font-size="12" {FONT}>exp((64/9)^(1/3) (ln N)^(1/3) (ln ln N)^(2/3)), scaled; a ruler, not a forecast</text>')
    write("cost.svg", svg(W, H, "".join(b), "The number field sieve's cost curve, core-years against bits"))


# ------------------------------------------------------------------ the gap
def qubits():
    W, H = 960, 520
    x0, y0, x1, y1 = 80, 30, W - 30, H - 60
    sx = lambda yr: x0 + (yr - 2000) / (2030 - 2000) * (x1 - x0)
    sy = lambda n: y1 - (math.log10(n) - 0) / (9.5 - 0) * (y1 - y0)
    b = [axes(x0, y0, x1, y1, [(y, sx(y)) for y in range(2000, 2031, 5)], [(10 ** k, sy(10 ** k)) for k in range(0, 10)],
              "year", "physical qubits, powers of ten", yfmt=lambda v: f"10^{round(math.log10(v))}")]
    for r in EST["rows"]:
        if not r["physical"]:
            continue
        col = C0 if r["target"] == "rsa2048" else C2
        b.append(f'<circle cx="{sx(r["year"]):.1f}" cy="{sy(r["physical"]):.1f}" r="6" fill="{col}"/>')
        right = r["target"] == "rsa2048" and r["year"] > 2024
        nudge = {"Caltech and Oratomic": 8, "Häner and others, IonQ": -4}.get(r["who"], 0)
        who = r["who"].split(",")[0].split(" and ")[0]
        if right:
            b.append(f'<text x="{sx(r["year"]) + 9:.1f}" y="{sy(r["physical"]) + 4 + nudge:.1f}" fill="{col}" font-size="11" {FONT}>{who} {r["date"][:4]}</text>')
        else:
            b.append(f'<text x="{sx(r["year"]) - 9:.1f}" y="{sy(r["physical"]) + 4 + nudge:.1f}" text-anchor="end" fill="{col}" font-size="11" {FONT}>{who} {r["date"][:4]}</text>')
    # the biggest machine so far, as a step
    best, steps = 0, []
    for m in sorted(MACH["rows"], key=lambda m: m["year"]):
        if m["physical"] > best:
            if steps:
                steps.append(f"{sx(m['year']):.1f},{sy(best):.1f}")
            best = m["physical"]
            steps.append(f"{sx(m['year']):.1f},{sy(best):.1f}")
    steps.append(f"{sx(2026.7):.1f},{sy(best):.1f}")
    b.append(f'<polyline points="{" ".join(steps)}" fill="none" stroke="{C1}" stroke-width="1.5" stroke-dasharray="5 4"/>')
    for m in MACH["rows"]:
        b.append(f'<circle cx="{sx(m["year"]):.1f}" cy="{sy(m["physical"]):.1f}" r="4" fill="{C1}"/>')
    for m in ("IBM Condor", "Google Willow", "Quantinuum Helios"):
        r = next(x for x in MACH["rows"] if x["name"] == m)
        b.append(f'<text x="{sx(r["year"]) + 8:.1f}" y="{sy(r["physical"]) + (14 if m == "Quantinuum Helios" else -6):.1f}" fill="{C1}" font-size="11" {FONT}>{m}, {r["physical"]}</text>')
    ly = y0 + 16
    b.append(f'<circle cx="{x0 + 14}" cy="{ly}" r="5" fill="{C0}"/><text x="{x0 + 24}" y="{ly + 4}" fill="{INK}" font-size="12" {FONT}>qubits a paper says would break RSA-2048</text>')
    b.append(f'<circle cx="{x0 + 14}" cy="{ly + 18}" r="5" fill="{C2}"/><text x="{x0 + 24}" y="{ly + 22}" fill="{INK}" font-size="12" {FONT}>qubits a paper says would break a 256-bit wallet key</text>')
    b.append(f'<circle cx="{x0 + 14}" cy="{ly + 36}" r="4" fill="{C1}"/><text x="{x0 + 24}" y="{ly + 40}" fill="{INK}" font-size="12" {FONT}>qubits a named machine has (dashed: the biggest so far)</text>')
    write("qubits.svg", svg(W, H, "".join(b), "The gap between qubit estimates for breaking a key and the qubits machines have, 2001 to 2026"))


# ------------------------------------------------------------------ pi(x)
def pi():
    W, H = 960, 440
    x0, y0, x1, y1 = 80, 30, W - 30, H - 60
    t = F["primes"]["table"]
    sx = lambda k: x0 + (k - 1) / 6 * (x1 - x0)
    sy = lambda v: y1 - math.log10(v) / 6 * (y1 - y0)
    b = [axes(x0, y0, x1, y1, [(10 ** k, sx(k)) for k in range(1, 8)], [(10 ** k, sy(10 ** k)) for k in range(0, 7)],
              "x", "count", xfmt=lambda v: f"10^{round(math.log10(v))}", yfmt=lambda v: f"10^{round(math.log10(v))}")]
    for key, col, lab in (("x_over_ln", C2, "x / ln x"), ("li", C1, "li(x)"), ("pi", C0, "π(x), the true count")):
        pts = " ".join(f"{sx(math.log10(r['x'])):.1f},{sy(r[key]):.1f}" for r in t)
        sw = 3 if key == "pi" else 1.5
        dash = "" if key == "pi" else "stroke-dasharray='6 4'"
        b.append(f'<polyline points="{pts}" fill="none" stroke="{col}" stroke-width="{sw}" {dash}/>')
        i = ("x_over_ln", "li", "pi").index(key)
        b.append(f'<line x1="{x1 - 230}" y1="{y1 - 60 + 18 * i}" x2="{x1 - 206}" y2="{y1 - 60 + 18 * i}" stroke="{col}" stroke-width="{sw}" {dash}/>')
        b.append(f'<text x="{x1 - 198}" y="{y1 - 56 + 18 * i}" fill="{col}" font-size="12" {FONT}>{lab}</text>')
    # the error table, inset
    ty = y0 + 20
    b.append(f'<text x="{x0 + 10}" y="{ty}" fill="{MUTE}" font-size="12" {MONO}>x         π(x)      x/ln x miss   li(x) miss</text>')
    for i, r in enumerate(t):
        lab = "10^" + str(round(math.log10(r["x"])))
        line = f"{lab:<9} {r['pi']:>8}   {r['err_ln']:>+10.0f}   {r['err_li']:>+8.1f}"
        b.append(f'<text x="{x0 + 10}" y="{ty + 16 * (i + 1)}" fill="{INK}" font-size="12" {MONO} xml:space="preserve">{line}</text>')
    write("pi.svg", svg(W, H, "".join(b), "The count of primes below x against two guesses, on log scales"))


# ------------------------------------------------------------------ Z(t)
def zeros():
    W, H = 960, 300
    x0, y0, x1, y1 = 50, 20, W - 20, H - 50
    tmax = 60.0
    sx = lambda t: x0 + t / tmax * (x1 - x0)
    sy = lambda v: (y0 + y1) / 2 - v / 4.5 * (y1 - y0) / 2
    b = [f'<line x1="{x0}" y1="{sy(0)}" x2="{x1}" y2="{sy(0)}" stroke="{LINE}"/>']
    ts = [2 + i * 0.05 for i in range(int((tmax - 2) / 0.05) + 1)]
    pts = " ".join(f"{sx(t):.1f},{sy(max(-4.5, min(4.5, Z(t)))):.1f}" for t in ts)
    b.append(f'<polyline points="{pts}" fill="none" stroke="{C1}" stroke-width="1.8"/>')
    for g in F["zeros"]["first"]:
        b.append(f'<circle cx="{sx(g):.1f}" cy="{sy(0):.1f}" r="5" fill="{C0}"/>')
        b.append(f'<text x="{sx(g):.1f}" y="{y1 + 18}" text-anchor="middle" fill="{C0}" font-size="11" {MONO}>{g:.2f}</text>')
    b.append(f'<text x="{x0 + 6}" y="{y0 + 14}" fill="{MUTE}" font-size="12" {FONT}>Z(t) along the critical line: zeta with its phase removed, so it is real, and crosses zero exactly where zeta does. The first ten crossings, computed here.</text>')
    b.append(f'<text x="{(x0 + x1) / 2}" y="{H - 8}" text-anchor="middle" fill="{MUTE}" font-size="12" {FONT}>t, the height up the line</text>')
    write("zeros.svg", svg(W, H, "".join(b), "The Riemann-Siegel Z function from t = 2 to 60, with the first ten zeros marked"))


# ------------------------------------------------------------------ the explicit formula
def explicit():
    W, H = 960, 440
    x0, y0, x1, y1 = 60, 30, W - 30, H - 50
    xs = EXPL["x"]
    sx = lambda x: x0 + (x - 2) / 98 * (x1 - x0)
    sy = lambda v: y1 - v / 100 * (y1 - y0)
    b = [axes(x0, y0, x1, y1, [(v, sx(v)) for v in range(10, 101, 10)], [(v, sy(v)) for v in range(0, 101, 20)], "x", "ψ(x)")]
    # the staircase
    path = []
    prev = None
    for x, v in zip(xs, EXPL["truth"]):
        if prev is not None and v != prev:
            path.append(f"L{sx(x):.1f},{sy(prev):.1f}")
        path.append(f"{'M' if prev is None else 'L'}{sx(x):.1f},{sy(v):.1f}")
        prev = v
    b.append(f'<path d="{" ".join(path)}" fill="none" stroke="{C1}" stroke-width="2.5"/>')
    for n, col, dash in (("0", MUTE, "6 4"), ("10", C2, "2 3"), ("30", VIO, ""), ("100", C0, "")):
        pts = " ".join(f"{sx(x):.1f},{sy(max(-5, min(105, v))):.1f}" for x, v in zip(xs, EXPL["series"][n]))
        sw = 2 if n == "100" else 1.4
        da = f"stroke-dasharray='{dash}'" if dash else ""
        b.append(f'<polyline points="{pts}" fill="none" stroke="{col}" stroke-width="{sw}" {da}/>')
    ly = y0 + 16
    for i, (n, col, lab) in enumerate((("t", C1, "ψ(x): every prime power p^k adds ln p"), ("0", MUTE, "the formula with no zeros: just x"), ("10", C2, "10 zeros"), ("30", VIO, "30 zeros"), ("100", C0, "100 zeros"))):
        b.append(f'<line x1="{x0 + 10}" y1="{ly + 16 * i}" x2="{x0 + 34}" y2="{ly + 16 * i}" stroke="{col}" stroke-width="2.5"/>')
        b.append(f'<text x="{x0 + 42}" y="{ly + 16 * i + 4}" fill="{INK}" font-size="12" {FONT}>{lab}</text>')
    write("explicit.svg", svg(W, H, "".join(b), "Chebyshev's psi function and Riemann's explicit formula with 0, 10, 30 and 100 zeros"))


# ------------------------------------------------------------------ exposure
def exposure():
    W, H = 960, 360
    x0, y0, x1, y1 = 60, 30, W - 30, H - 70
    rows = WALLET["exposure"]
    n = len(rows)
    bw = (x1 - x0) / n
    sy = lambda v: y1 - v / 8e6 * (y1 - y0)
    b = [axes(x0, y0, x1, y1, [], [(v, sy(v)) for v in (0, 2e6, 4e6, 6e6, 8e6)], "", "bitcoin in outputs whose key is on the chain", yfmt=lambda v: f"{v / 1e6:.0f}M")]
    for i, r in enumerate(rows):
        x = x0 + i * bw + bw * 0.15
        b.append(f'<rect x="{x:.1f}" y="{sy(r["btc"]):.1f}" width="{bw * 0.7:.1f}" height="{y1 - sy(r["btc"]):.1f}" fill="{C0}" rx="4"/>')
        b.append(f'<text x="{x + bw * 0.35:.1f}" y="{sy(r["btc"]) - 8:.1f}" text-anchor="middle" fill="{INK}" font-size="13" {MONO}>{r["btc"] / 1e6:.2f}M · {r["share"] * 100:.0f}%</text>')
        b.append(f'<text x="{x + bw * 0.35:.1f}" y="{y1 + 18}" text-anchor="middle" fill="{INK}" font-size="12" {FONT}>{r["who"]}</text>')
        b.append(f'<text x="{x + bw * 0.35:.1f}" y="{y1 + 34}" text-anchor="middle" fill="{MUTE}" font-size="11" {MONO}>{r["date"]}</text>')
    b.append(f'<text x="{x0 + 8}" y="{y0 + 14}" fill="{MUTE}" font-size="12" {FONT}>five counts of the same doors; CoinShares counted only the oldest kind</text>')
    write("exposure.svg", svg(W, H, "".join(b), "Bitcoin in exposed-key outputs, as counted by five sources from 2020 to 2026"))


if __name__ == "__main__":
    records()
    cost()
    qubits()
    pi()
    zeros()
    explicit()
    exposure()
