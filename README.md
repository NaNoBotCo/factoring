# Big Numbers, Split

Factoring, from Eratosthenes to Shor: how big numbers get split, who has split the biggest,
what the Riemann Hypothesis has to do with it, and what all of it means for a bitcoin wallet.
Plain spoken English, every number computed or sourced, nothing about money that is advice.

**Live:** https://nanobotco.github.io/factoring/

## What is on it

- **Split** — make a product of two primes at any size and watch trial division and Pollard
  rho try to get them back, with live counters; then a 2048-bit key made in the browser.
- **History** — 43 dated events from the sieve of Eratosthenes (240 BC) to RSA-260 and RSA-896
  (September 2026), in three lanes: classical, quantum, Riemann. The sieve, animated.
- **Methods** — Kraitchik's two squares on Pomerance's 1649, a box that finds them for any
  small N, and four old methods racing on numbers of different shapes.
- **Records** — every general-purpose record since 1991, the number field sieve's L(1/3) cost
  curve anchored on RSA-250, and a ruler for any key size.
- **Quantum** — Shor's period-finding you can watch (sequence and frequency view), every
  hardware claim beside what it did, the resource estimates 2012–2026, the machines, and the
  gap chart.
- **Riemann** — π(x) to ten million against x/ln x and li(x); the first 100 zeta zeros computed
  here (Euler–Maclaurin ζ, Riemann–Siegel Z, bisection, counted against Riemann–von Mangoldt);
  the explicit formula drawing the primes one zero at a time; why a proof would not touch a key.
- **Wallet** — secp256k1 explained on y² = x³ + 7 mod 97 with a hop-and-brute-force demo and a
  full-size key made in the browser; which output types expose the key; five counts of exposed
  coins; long-range and on-spend attacks; the ten-minute window estimates; every draft proposal
  (BIP 360, BIP 361, hourglass, commit-reveal, canary, SHRINCS, PACTs, P2Q); the timelines
  people sign their names to.
- **Now** — a hand-kept ledger of 41 dated rows since 2024, each with what it does not mean, and
  a weekly feed from arXiv and public RSS that nobody has read.
- **Words · Sources** — 30 terms; 124 numbered sources.

## Build

```
python3 tools/compute.py     # facts: primes, zeros, explicit formula, cost curve, examples, the toy curve
python3 tools/draw.py        # the raster pictures (numpy + Pillow): spiral, sieve, strip, curve, beat, card
python3 tools/figures.py     # the SVG charts from the data
./publish.sh                 # all of the above, checked, into docs/
python3 tools/serve.py 8837  # http://127.0.0.1:8837/factoring/
```

`publish.sh` refuses to build if a computed check fails (there are 25), if an internal link
misses, if a test fails, or if a host path leaks into the output. Python 3.9+, numpy, Pillow;
no other dependency. The browser demos are vanilla JavaScript with BigInt.

`.github/workflows/refresh.yml` runs `tools/fetch_recent.py` every Monday and commits
`data/recent.json` and `docs/`. The ledger (`data/developments.json`) is edited by hand.

## Data

Every table on the site is a JSON file in `data/` with a source id on each row, and the ids
resolve in `tools/sources.py`. The build refuses an id that is not there. `build/facts.json`
carries every computed number the pages print.

## Terms

Text, figures and data: CC BY 4.0 — credit "Nan · hongdam.net · CC BY 4.0" with a link to
https://nanobotco.github.io/factoring/. Code: MIT. See `NOTICE.txt`.

Nothing on the site is advice about money.
