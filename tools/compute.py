#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""compute.py — every number the site prints, computed here and written to build/facts.json.

    python3 tools/compute.py            # writes build/facts.json, build/data/*.json
    python3 tools/compute.py --check    # runs the checks only

What is in here:
  primes        a sieve to ten million; pi(x) against x/ln x and li(x)
  zeros         the first 100 zeros of the Riemann zeta function on the critical line,
                found by sign changes of the Riemann–Siegel Z function and bisection,
                counted against the Riemann–von Mangoldt formula so none is missed
  explicit      psi(x) from the explicit formula with N zeros, against the true staircase
  cost          the L[1/3] curve of the number field sieve, anchored on RSA-250
  examples      the small worked examples the demos and the prose use (Kraitchik's
                1649, Shor's 15 and 21, Fermat on a pair of close primes)
  wallet        a toy elliptic curve mod 97 with the shape of secp256k1, counted

numpy only. No mpmath, no scipy: the CI runner and this laptop both have numpy.
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
BUILD = ROOT / "build"
DATA_OUT = BUILD / "data"

CHECKS: list[tuple[str, bool]] = []


def check(name: str, ok: bool):
    CHECKS.append((name, bool(ok)))


# ------------------------------------------------------------------ primes

def sieve(n: int) -> np.ndarray:
    s = np.ones(n + 1, dtype=bool)
    s[:2] = False
    for p in range(2, int(n ** 0.5) + 1):
        if s[p]:
            s[p * p::p] = False
    return s


def li(x: float) -> float:
    """The logarithmic integral, by Ramanujan's series. Good to double precision for the
    x this site uses."""
    if x <= 1:
        return float("-inf") if x == 1 else float("nan")
    L = math.log(x)
    total = 0.0
    inner = 0.0
    for n in range(1, 200):
        if (n - 1) % 2 == 0:
            inner += 1.0 / (n)          # 1/(2k+1) for k = (n-1)/2
        term = ((-1) ** (n - 1)) * L ** n / (math.factorial(n) * 2 ** (n - 1)) * inner
        total += term
        if abs(term) < 1e-17 * abs(total) and n > 10:
            break
    return 0.5772156649015329 + math.log(L) + math.sqrt(x) * total


def primes_block():
    N = 10_000_000
    s = sieve(N)
    cum = np.cumsum(s)
    table = []
    for k in range(1, 8):
        x = 10 ** k
        pi = int(cum[x])
        table.append({"x": x, "pi": pi, "x_over_ln": x / math.log(x), "li": li(x),
                      "err_ln": pi - x / math.log(x), "err_li": pi - li(x)})
    # the sieve picture and the small demos want the first few hundred primes
    first = [int(p) for p in np.nonzero(s[:2000])[0]]
    # how far apart primes are near a given size — the 'plenty of primes' point
    density = [{"digits": d, "one_in": round(math.log(10 ** d))} for d in (2, 5, 10, 20, 50, 100, 155, 308, 617)]
    check("pi(10^6) = 78498", table[5]["pi"] == 78498)
    check("pi(10^7) = 664579", table[6]["pi"] == 664579)
    check("li beats x/ln x at 10^7", abs(table[6]["err_li"]) < abs(table[6]["err_ln"]))
    check("li(10^6) near 78627.55", abs(table[5]["li"] - 78627.549) < 0.01)
    return {"table": table, "first": first, "count_to": N, "pi_max": int(cum[N]), "density": density}, s


# ------------------------------------------------------------------ zeta zeros

BERNOULLI = [1 / 6, -1 / 30, 1 / 42, -1 / 30, 5 / 66, -691 / 2730, 7 / 6, -3617 / 510,
             43867 / 798, -174611 / 330, 854513 / 138, -236364091 / 2730]


def theta(t: float) -> float:
    """The Riemann–Siegel theta function, Stirling to three terms."""
    return (t / 2) * math.log(t / (2 * math.pi)) - t / 2 - math.pi / 8 + 1 / (48 * t) + 7 / (5760 * t ** 3)


def zeta(s: complex, N: int | None = None, m: int = 12) -> complex:
    """zeta(s) by Euler–Maclaurin summation: the first N terms by hand, the tail by the
    integral and the Bernoulli corrections. Plain and slow, and correct to about 1e-12
    for the t below 300 this site needs."""
    t = abs(s.imag)
    if N is None:
        N = int(t) + 20
    n = np.arange(1, N, dtype=float)
    total = np.sum(n ** (-s))
    total += N ** (1 - s) / (s - 1) + 0.5 * N ** (-s)
    rising = s
    for k in range(1, m + 1):
        # (s)_(2k-1) = s (s+1) ... (s+2k-2), built up two factors at a time
        if k > 1:
            rising *= (s + 2 * k - 3) * (s + 2 * k - 2)
        total += BERNOULLI[k - 1] / math.factorial(2 * k) * rising * N ** (-s - 2 * k + 1)
    return complex(total)


def Z(t: float) -> float:
    """Riemann–Siegel Z(t) = e^{i theta(t)} zeta(1/2 + it): real, and zero exactly where
    zeta is zero on the critical line."""
    z = zeta(complex(0.5, t))
    return (complex(math.cos(theta(t)), math.sin(theta(t))) * z).real


def zeros_block(count: int = 100):
    lo, hi, step = 10.0, 300.0, 0.05
    grid = np.arange(lo, hi, step)
    vals = np.array([Z(float(t)) for t in grid])
    found = []
    for i in range(len(grid) - 1):
        if vals[i] == 0 or vals[i] * vals[i + 1] < 0:
            a, b = float(grid[i]), float(grid[i + 1])
            fa = vals[i]
            for _ in range(50):
                m = (a + b) / 2
                fm = Z(m)
                if fa * fm <= 0:
                    b = m
                else:
                    a, fa = m, fm
            found.append((a + b) / 2)
            if len(found) == count:
                break
    zs = found[:count]
    T = zs[-1] + 0.5
    expected = theta(T) / math.pi + 1
    known = [14.134725141734693, 21.022039638771555, 25.010857580145688, 30.424876125859513,
             32.935061587739190, 37.586178158825671, 40.918719012147495, 43.327073280914999,
             48.005150881167159, 49.773832477672302]
    err = max(abs(z - k) for z, k in zip(zs, known))
    check("first ten zeros match Odlyzko's to 1e-6", err < 1e-6)
    check("zero count agrees with Riemann–von Mangoldt", abs(len(zs) - expected) < 0.6)
    check("zeros strictly increasing", all(b > a for a, b in zip(zs, zs[1:])))
    check("zeta(2) = pi^2/6 by the same routine", abs(zeta(complex(2, 0)).real - math.pi ** 2 / 6) < 1e-10)
    return {"gamma": zs, "count": len(zs), "max_err_first_ten": err,
            "riemann_von_mangoldt": expected,
            "method": "Euler–Maclaurin zeta on the critical line, sign changes of Z(t), bisection"}


# ------------------------------------------------------------------ the explicit formula

def psi_true(xmax: int, s: np.ndarray) -> np.ndarray:
    """Chebyshev's psi(x) = sum of ln p over prime powers p^k <= x, for x = 0..xmax."""
    out = np.zeros(xmax + 1)
    for p in np.nonzero(s[:xmax + 1])[0]:
        pk = int(p)
        while pk <= xmax:
            out[pk:] += math.log(int(p))
            pk *= int(p)
    return out


def psi_formula(x: float, gammas: list[float], n: int) -> float:
    """von Mangoldt's explicit formula, the sum over zeros cut at n pairs."""
    if x < 2:
        return 0.0
    total = x - math.log(2 * math.pi) - 0.5 * math.log(1 - x ** -2)
    lx = math.log(x)
    for g in gammas[:n]:
        rho = complex(0.5, g)
        total -= 2 * (complex(math.sqrt(x) * math.cos(g * lx), math.sqrt(x) * math.sin(g * lx)) / rho).real
    return total


def explicit_block(gammas: list[float], s: np.ndarray):
    xmax = 100
    truth = psi_true(xmax, s)
    # sample between the integers so the staircase and the smooth curve are both drawn
    xs = np.arange(2, xmax + 0.001, 0.25)
    series = {}
    for n in (0, 10, 30, 100):
        series[str(n)] = [round(psi_formula(float(x), gammas, n), 4) for x in xs]
    # the formula converges to the midpoint at a jump, so compare off the integers
    off = [x for x in xs if abs(x - round(x)) > 0.1]
    err100 = max(abs(psi_formula(float(x), gammas, 100) - truth[int(x)]) for x in off)
    err0 = max(abs(psi_formula(float(x), gammas, 0) - truth[int(x)]) for x in off)
    rms = math.sqrt(sum((psi_formula(float(x), gammas, 100) - truth[int(x)]) ** 2 for x in off) / len(off))
    check("100 zeros bring psi(x) within 3 everywhere on [2,100]", err100 < 3.0)
    check("100 zeros: root-mean-square miss under 0.8", rms < 0.8)
    check("zeros improve on x alone", err100 < err0 / 2)
    check("psi(100) = ln lcm(1..100)", abs(truth[100] - math.log(math.lcm(*range(1, 101)))) < 1e-9)
    return {"x": [float(x) for x in xs], "truth": [round(float(truth[int(x)]), 4) for x in xs],
            "series": series, "err_100": err100, "rms_100": rms, "err_0": err0, "psi_100": float(truth[100])}


# ------------------------------------------------------------------ the cost curve

def L(bits: float, c: float = (64 / 9) ** (1 / 3)) -> float:
    """log10 of L_N[1/3, c] for an N of the given size."""
    lnN = bits * math.log(2)
    return c * lnN ** (1 / 3) * math.log(lnN) ** (2 / 3) / math.log(10)


def cost_block():
    anchor_bits, anchor_years = 829, 2700.0         # RSA-250, Boudot et al. 2020
    rows = []
    for bits in (512, 768, 829, 1024, 1536, 2048, 3072, 4096):
        rel = 10 ** (L(bits) - L(anchor_bits))
        rows.append({"bits": bits, "digits": len(str(2 ** bits)), "log10_L": L(bits),
                     "relative_to_rsa250": rel, "core_years": anchor_years * rel})
    by = {r["bits"]: r for r in rows}
    check("cost curve rises", all(a["core_years"] < b["core_years"] for a, b in zip(rows, rows[1:])))
    # sanity: the curve says 768 -> 1024 is a few hundred to a few thousand times harder,
    # which is the range the RSA-768 team gave ("about a thousand times")
    ratio = by[1024]["core_years"] / by[768]["core_years"]
    check("768 -> 1024 lands between 100x and 10000x", 100 < ratio < 10000)
    return {"anchor": {"bits": anchor_bits, "core_years": anchor_years, "cpu": "2.1 GHz Xeon Gold 6130"},
            "rows": rows, "ratio_768_1024": ratio, "c": (64 / 9) ** (1 / 3)}


# ------------------------------------------------------------------ small worked examples

def kraitchik_1649():
    """Pomerance's example: 1649 = 17 x 97, found by two squares that combine to a square."""
    N = 1649
    rel = []
    for x in range(41, 60):
        q = x * x % N
        # factor q over {2, 3, 5, 7}
        f, r = {}, q
        for p in (2, 3, 5, 7):
            while r % p == 0:
                f[p] = f.get(p, 0) + 1
                r //= p
        if r == 1:
            rel.append({"x": x, "x2": x * x, "q": q, "factors": f})
    # the classic pair: 41 and 43
    a, b = rel[0], [r for r in rel if r["x"] == 43][0]
    X = a["x"] * b["x"] % N
    Y = int(math.isqrt(a["q"] * b["q"]))
    g = math.gcd(X - Y, N)
    check("Kraitchik: 41^2 = 32 mod 1649", a["q"] == 32)
    check("Kraitchik: 43^2 = 200 mod 1649", b["q"] == 200)
    check("Kraitchik: 32*200 is a square", Y * Y == a["q"] * b["q"])
    check("Kraitchik: gcd gives 17", g == 17 and N // g == 97)
    return {"N": N, "relations": rel[:6], "X": X, "Y": Y, "gcd": g, "other": N // g}


def shor_example(N: int, a: int):
    seq = [pow(a, x, N) for x in range(0, 40)]
    r = next(x for x in range(1, 40) if seq[x] == 1)
    ok = r % 2 == 0 and pow(a, r // 2, N) != N - 1
    f1 = math.gcd(pow(a, r // 2, N) - 1, N) if ok else None
    f2 = math.gcd(pow(a, r // 2, N) + 1, N) if ok else None
    return {"N": N, "a": a, "period": r, "sequence": seq[:24], "works": ok, "factors": [f1, f2]}


def fermat_example():
    p, q = 10007, 10037           # close primes: Fermat's method finds them in a few steps
    N = p * q
    a = math.isqrt(N) + 1
    steps = 0
    while True:
        b2 = a * a - N
        b = math.isqrt(b2)
        steps += 1
        if b * b == b2:
            break
        a += 1
    check("Fermat: close primes fall in a handful of steps", (a - b) * (a + b) == N and steps < 10)
    return {"p": p, "q": q, "N": N, "steps": steps, "a": a, "b": b}


def examples_block():
    s15 = shor_example(15, 7)
    s21 = shor_example(21, 2)
    check("Shor: 7 mod 15 has period 4", s15["period"] == 4)
    check("Shor: 15 splits into 3 and 5", sorted(s15["factors"]) == [3, 5])
    check("Shor: 2 mod 21 has period 6", s21["period"] == 6)
    check("Shor: 21 splits into 3 and 7", sorted(s21["factors"]) == [3, 7])
    return {"kraitchik": kraitchik_1649(), "shor15": s15, "shor21": s21, "fermat": fermat_example()}


# ------------------------------------------------------------------ the toy curve

def curve_block(p: int = 97, b: int = 7):
    """y^2 = x^3 + 7 over the integers mod p — secp256k1's equation on a field small
    enough to draw every point."""
    pts = [(x, y) for x in range(p) for y in range(p) if (y * y - (x ** 3 + b)) % p == 0]
    n = len(pts) + 1          # plus the point at infinity

    def add(P, Q):
        if P is None:
            return Q
        if Q is None:
            return P
        x1, y1 = P
        x2, y2 = Q
        if x1 == x2 and (y1 + y2) % p == 0:
            return None
        if P == Q:
            lam = (3 * x1 * x1) * pow(2 * y1, -1, p) % p
        else:
            lam = (y2 - y1) * pow(x2 - x1, -1, p) % p
        x3 = (lam * lam - x1 - x2) % p
        return (x3, (lam * (x1 - x3) - y1) % p)

    # the order of every point, to pick a generator of the largest cyclic piece
    best, best_order = None, 0
    for P in pts:
        Q, k = P, 1
        while Q is not None:
            Q = add(Q, P)
            k += 1
        if k > best_order:
            best, best_order = P, k
    G = best
    walk = []
    Q = None
    for k in range(1, best_order + 1):
        Q = add(Q, G)
        walk.append(list(Q) if Q is not None else None)
    check("toy curve: order of G divides the point count", n % best_order == 0)
    check("toy curve: the walk returns to infinity", walk[-1] is None)
    return {"p": p, "b": b, "points": len(pts), "order": n, "G": list(G), "G_order": best_order,
            "walk": walk[:-1]}


# ------------------------------------------------------------------ main

def main(check_only: bool = False) -> int:
    primes, s = primes_block()
    zeros = zeros_block()
    explicit = explicit_block(zeros["gamma"], s)
    cost = cost_block()
    examples = examples_block()
    curve = curve_block()
    fails = [n for n, ok in CHECKS if not ok]
    for n, ok in CHECKS:
        print(f"  {'ok ' if ok else 'BAD'} {n}")
    facts = {
        "primes": {k: v for k, v in primes.items() if k != "first"},
        "zeros": {"count": zeros["count"], "first": zeros["gamma"][:10],
                  "max_err_first_ten": zeros["max_err_first_ten"], "method": zeros["method"]},
        "explicit": {"err_100": explicit["err_100"], "rms_100": explicit["rms_100"], "err_0": explicit["err_0"], "psi_100": explicit["psi_100"]},
        "cost": cost,
        "examples": examples,
        "curve": {k: v for k, v in curve.items() if k != "walk"},
        "checks": {"total": len(CHECKS), "failures": len(fails),
                   "list": [{"name": n, "ok": ok} for n, ok in CHECKS]},
    }
    if check_only:
        print(f"{len(CHECKS)} checks, {len(fails)} failing")
        return 1 if fails else 0
    BUILD.mkdir(parents=True, exist_ok=True)
    DATA_OUT.mkdir(parents=True, exist_ok=True)
    (BUILD / "facts.json").write_text(json.dumps(facts, indent=1), encoding="utf-8")
    (DATA_OUT / "zeros.json").write_text(json.dumps(
        {"_about": "The first 100 zeros of zeta(1/2 + i t), t > 0, computed by tools/compute.py "
                   "(Riemann–Siegel Z, bisection). CC BY 4.0, Nan · hongdam.net.",
         "gamma": [round(g, 9) for g in zeros["gamma"]]}, indent=0), encoding="utf-8")
    (DATA_OUT / "primes.json").write_text(json.dumps(
        {"_about": "Primes below 2000 and pi(x) at powers of ten, from tools/compute.py.",
         "first": primes["first"], "table": primes["table"]}), encoding="utf-8")
    (DATA_OUT / "explicit.json").write_text(json.dumps(explicit), encoding="utf-8")
    (DATA_OUT / "curve.json").write_text(json.dumps(curve), encoding="utf-8")
    print(f"build/facts.json — {len(CHECKS)} checks, {len(fails)} failing")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main("--check" in sys.argv))
