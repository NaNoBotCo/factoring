#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""site.py — the pages, built from build/facts.json, the data files and the figures.

    SITE_URL=https://nanobotco.github.io/factoring python3 tools/site.py
"""
from __future__ import annotations

import html
import json
import os
import shutil
from datetime import date
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
import fleet                                   # noqa: E402
from css import CSS                            # noqa: E402
from sources import SOURCES, BY_ID             # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
BUILD = ROOT / "build"
SITE = BUILD / "site"
IMG = BUILD / "img"
DATA = ROOT / "data"
SITE_URL = os.environ.get("SITE_URL", "https://nanobotco.github.io/factoring").rstrip("/")
tail = SITE_URL.split("//", 1)[-1]
BASE = "/" + tail.split("/", 1)[1] + "/" if "/" in tail else "/"
SELF = "factoring"
NAME = "Big Numbers, Split"
TAG = ("Factoring, from Eratosthenes to Shor: how big numbers get split, who has split the "
       "biggest, what the Riemann Hypothesis has to do with it, and what all of it means for a "
       "bitcoin wallet.")
CREDIT = "Nan · hongdam.net · CC BY 4.0"
TODAY = date.today().isoformat()
E = html.escape

F = json.loads((BUILD / "facts.json").read_text(encoding="utf-8"))
FLEET = fleet.load(DATA / "fleet.json")
D = {k: json.loads((DATA / f"{k}.json").read_text(encoding="utf-8"))
     for k in ("timeline", "records", "claims", "estimates", "machines", "developments", "wallet", "glossary")}
RECENT = json.loads((DATA / "recent.json").read_text(encoding="utf-8")) if (DATA / "recent.json").exists() else None
AS_OF = D["developments"]["as_of"]
USED: set[str] = set()

NAV = [("split/", "Split"), ("history/", "History"), ("methods/", "Methods"), ("records/", "Records"),
       ("quantum/", "Quantum"), ("riemann/", "Riemann"), ("wallet/", "Wallet"), ("now/", "Now"),
       ("words/", "Words"), ("sources/", "Sources")]

ALT = {
    "hero.jpg": "Thousands of small amber dots on a dark ground, arranged on a square spiral so that faint diagonal lines run through them: the primes, drawn where they fall.",
    "band-sieve.jpg": "Eight coloured stripes, one per small prime, each with ticks at that prime's multiples, and a last stripe of amber ticks where the primes survive.",
    "band-zeros.jpg": "A teal field with dark wells along a rose horizontal line: the size of the zeta function across the critical strip, the zeros as the dark spots.",
    "band-curve.jpg": "A glowing amber loop and tail, an elliptic curve, with a teal line cutting it at three points and a rose vertical dropping from the third.",
    "band-wave.jpg": "A field of teal bars of varying height with a tall amber bar every so often at a steady spacing: a^x mod N repeating.",
    "card.jpg": "The site's name over the prime spiral.",
    "records.svg": "A line chart of factoring records in bits against year, rising from 330 bits in 1991 to 896 in 2026, with dashed lines at 512, 1024 and 2048.",
    "cost.svg": "A curve rising steeply from left to right: the estimated core-years to factor a key against its size in bits, marked at 512, 768, 1024, 2048 and 4096.",
    "qubits.svg": "A scatter of amber and rose dots high on a log scale, the qubits papers ask for, falling from a billion in 2012 toward a hundred thousand in 2026; and a teal step low on the chart, the qubits real machines have, reaching about a thousand.",
    "pi.svg": "Three nearly coincident lines on log axes with an inset table of misses: the count of primes, x over ln x, and li of x.",
    "zeros.svg": "A wavy teal line crossing a horizontal axis at ten marked amber points between 14 and 50.",
    "explicit.svg": "A teal staircase rising from 0 to about 94, and coloured curves that hug it more closely as more zeros are added.",
    "exposure.svg": "Five amber bars of different heights, one per source, each labelled with millions of bitcoin and a percentage.",
}


# --------------------------------------------------------------------- helpers

def cite(*ids):
    out = []
    for sid in ids:
        if sid not in SOURCES:
            raise KeyError(f"unknown source id: {sid}")
        USED.add(sid)
        n = BY_ID[sid]
        out.append(f'<a class="cite" href="{BASE}sources/#src-{n}" title="{E(SOURCES[sid][1])}">[{n}]</a>')
    return "".join(out)


def cites(ids):
    return cite(*ids)


def fig(name, caption, cls="", w=0):
    alt = ALT.get(name, caption)
    size = f' width="{w}"' if w else ""
    return (f'<figure class="fig {cls}"><img src="{BASE}img/{name}" alt="{E(alt)}" '
            f'loading="lazy" decoding="async"{size}>'
            f'<figcaption>{caption}</figcaption></figure>')


def eq(body, note=""):
    n = f'<div class="eqn">Reading it: {note}</div>' if note else ""
    return f'<div class="eq">{body}{n}</div>'


def band(img, inner):
    return (f'<section class="band" style="background-image:url({BASE}img/{img})">'
            f'<div class="in">{inner}</div></section>')


def shot(href, img, kicker, title, text):
    return (f'<a class="shot" href="{BASE}{href}"><span class="bg" style="background-image:url({BASE}img/{img})"></span>'
            f'<span class="scrim"></span><span class="sp"></span>'
            f'<span class="tx"><em>{E(kicker)}</em><b>{E(title)}</b><span>{E(text)}</span></span></a>')


def card(href, title, kicker, text):
    return (f'<a class="card" href="{BASE}{href}"><h3>{E(title)}</h3>'
            f'<p class="mute small">{E(kicker)}</p><p>{E(text)}</p></a>')


def n(x):
    return f"{x:,}"


def page(title, body, path, desc="", cur="", scripts=(), jsonld=None):
    cur_attr = ' aria-current="page"'
    nav = "".join(f'<a href="{BASE}{h}"{cur_attr if cur == h else ""}>{E(t)}</a>' for h, t in NAV)
    js = "".join(f'<script src="{BASE}js/{s}" defer></script>' for s in scripts)
    ld = f'<script type="application/ld+json">{json.dumps(jsonld)}</script>' if jsonld else ""
    canon = SITE_URL + "/" + path if path else SITE_URL + "/"
    head_title = f"{title} — {NAME}" if path else f"{NAME} — factoring, from Eratosthenes to Shor"
    out = f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{E(head_title)}</title>
<meta name="description" content="{E(desc or TAG)}">
<link rel="canonical" href="{E(canon)}">
<meta property="og:title" content="{E(head_title)}">
<meta property="og:description" content="{E(desc or TAG)}">
<meta property="og:image" content="{SITE_URL}/img/card.jpg">
<meta property="og:type" content="website">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{BASE}icon.svg" type="image/svg+xml">
<style>{CSS}</style>{ld}</head>
<body data-base="{BASE}" data-asof="{AS_OF}">
<a class="sr" href="#main">Skip to the page</a>
<header class="top"><div class="in">
<a class="brand" href="{BASE}"><i></i>Big Numbers, <b>Split</b></a>
<nav aria-label="Sections">{nav}</nav></div></header>
<main id="main">{body}</main>
<footer class="bot"><div class="in">
<p><b>{E(NAME)}</b> — {E(TAG)}</p>
<p>Text and figures {E(CREDIT)}. Code MIT. Built {E(TODAY)}; the ledger runs to {E(AS_OF)}.
Every number on these pages is computed by <code>tools/compute.py</code> or carried in a data file with its
source, in <a href="https://github.com/NaNoBotCo/{SELF}">the repository</a>. Nothing here is advice about money.</p>
{fleet.row_html(SELF, roster=FLEET)}
{fleet.support_html(roster=FLEET)}
{fleet.maker_html(roster=FLEET)}
</div></footer>{js}
<script src="{BASE}js/nav.js" defer></script>
</body></html>"""
    write(SITE / path / "index.html" if path else SITE / "index.html", out)
    return out


def write(p: Path, text: str):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")


# ----------------------------------------------------------------------- home

def home():
    c = F["cost"]["rows"]
    by = {r["bits"]: r for r in c}
    largest = D["claims"]["largest_shor_hardware"]
    expo = D["wallet"]["exposure"]
    glass = next(x for x in expo if x["who"] == "Glassnode")
    b = [f"""<h1><span class="kind">Factoring, from Eratosthenes to Shor</span>Big Numbers,<br>Split</h1>
<p class="lede">Multiply two big primes: a millisecond. Get them back out of the product: past a certain
size, nobody can. Every RSA lock on the web rests on that gap, and the lock on a bitcoin wallet is the
same gap in a different coat. This is the history of the gap, who has narrowed it, and what is left of it
as of {E(AS_OF)}.</p>

<div class="hero"><img src="{BASE}img/hero.jpg" alt="{E(ALT['hero.jpg'])}" width="2000" height="1000"></div>
<p class="small mute">The whole numbers wound into a square spiral, 1 in the middle, and every prime lit.
Stanisław Ulam drew it on a scratch pad during a dull talk in 1963. The diagonal streaks are real — primes
crowd some quadratic lines and shun others — and nobody has explained them. Drawn here from a sieve, not
copied.</p>

<div class="answer" id="wallet-answer">
<h3>If you came about the wallet</h3>
<p><b>Nobody has broken a real key.</b> The largest number ever split by Shor's algorithm on a physical
machine is {largest['number']}, in {largest['year']}, with the answer wired into the circuit
{cite('martinlopez2012', 'smolin2013')}. The largest wallet-style curve key broken on hardware is 15 bits
(April 2026), and Bitcoin developers matched that result with random coin flips within a day
{cite('qday2026', 'qday2026b')}. A wallet key is 256 bits.</p>
<p><b>The bill keeps falling, on paper.</b> Qubits said to be needed for a 2048-bit RSA key: a billion in
2012, twenty million in 2019, under a million in 2025, under a hundred thousand in February 2026 on a code
nobody has built at scale {cite('fowler2012', 'gidney2019', 'gidney2025', 'pinnacle2026')}. For a wallet
key: under half a million, in minutes, on a fast superconducting machine — Google, March 2026
{cite('babbush2026')}.</p>
<p><b>The machines are far behind the paper.</b> The biggest have a hundred to a thousand physical qubits,
and the best error-corrected count is 48 logical qubits {cite('helios2025', 'willow2024')}. The papers
want more than a thousand logical qubits running for hours.</p>
<p><b>Some coins are more exposed than others.</b> About {glass['share'] * 100:.0f}% of all bitcoin sits
in outputs whose public key is already visible on the chain — Satoshi-era coins, Taproot, and any address
that was used twice {cite('glassnode2026', 'chaincode2025')}. A hash-only address that has never spent
shows its key only for the ten minutes or so while its transaction waits to be confirmed.</p>
<p><b>The timelines people put their names to:</b> experts surveyed in 2025 put a 28–49% chance on a
one-day RSA-2048 break within ten years; NIST retires RSA-2048 and 256-bit curves after 2030 and bans them
after 2035; Google will finish its own move by 2029 {cite('gri2025', 'nist8547', 'google2029')}. Bitcoin
has proposals and no roadmap {cite('coindesk2026roadmap')}.</p>
<p><a href="{BASE}wallet/">The whole wallet page</a> — which outputs are exposed, what the proposals say,
and a lock small enough to see.</p>
</div>

<h2>The short version</h2>
<div class="prose">
<p>Take two boards and glue them face to face. Anyone can do it, and you cannot tell afterwards where the
seam is. Now hand the block to a stranger and ask them to split it back into the two boards. If the block is
small they can find the seam by tapping along it. If the block is big enough, tapping takes longer than
they have.</p>
<p>A <strong>prime</strong> is a whole number that nothing divides but 1 and itself. Glue two of them
together by multiplying and you get a <strong>semiprime</strong>. Every RSA key is one: a number of 617
digits that is exactly two primes of about 309 digits each. The public key is the block. The private key is
the two boards. The bet the whole web makes is that nobody can find the seam.</p>
<p>Tapping along the block is <strong>trial division</strong>: try 2, try 3, try 5, and so on up to the
square root. For a 20-digit number that is ten billion taps. For a 617-digit number it is a 1 with 308
zeros after it. The methods on this site are the clever ways of tapping, from a Greek librarian's sieve to a
1994 idea that needs a machine that does not exist yet. They shorten the job, a lot. None of them, on any
computer built so far, gets through a 2048-bit block.</p>
<p>A wallet key is not a semiprime. It is a hop count on a curve — start at a fixed point, hop k times,
show everyone where you landed, keep k. Finding k from the landing spot is the <strong>discrete
logarithm</strong>, and it is hard in the same way and for the same reason, and the same 1994 idea breaks
both. That is why a site about factoring is the site for the wallet question.</p>
</div>

<h2>Where to go</h2>
<div class="shots">
{shot('split/', 'band-wave.jpg', 'Make one, break one', 'Split', 'Two primes, one product, and a counter that shows the wall arriving. Then a 2048-bit key, made in your browser in a second.')}
{shot('history/', 'band-sieve.jpg', '240 BC to last week', 'History', f'{len(D["timeline"]["events"])} events: Eratosthenes, Fermat, Gauss, Riemann, the Lehmers, Pollard, RSA, Shor, and two records from this month.')}
{shot('methods/', 'band-sieve.jpg', 'Sieves', 'Methods', 'Four old methods racing, and the one trick since 1926 that every record rests on: two squares that agree.')}
{shot('quantum/', 'band-wave.jpg', 'Shor, and the bill', 'Quantum', 'Period-finding you can watch, every hardware claim beside what it did, and the gap chart: qubits asked for against qubits built.')}
{shot('riemann/', 'band-zeros.jpg', 'A hundred zeros, computed', 'Riemann', 'Where the primes are, the Hypothesis in one line, the zeros drawn, and what proving it would and would not do to a key.')}
{shot('wallet/', 'band-curve.jpg', 'The curve, the window, the proposals', 'Wallet', 'Which outputs show their key, how many coins sit in them, what a ten-minute attack needs, and every draft on the table.')}
</div>
<div class="grid">
{card('records/', 'Records', 'Every general-purpose record since 1991', 'The table, the chart, and a ruler for how far 2048 bits is from the record.')}
{card('now/', 'Now', f'The ledger to {AS_OF}', f'{len(D["developments"]["rows"])} dated rows since 2024, each with what it does not mean; and a weekly feed nobody has read.')}
{card('words/', 'Words', f'{len(D["glossary"]["words"])} terms', 'Prime, semiprime, discrete logarithm, qubit, soft fork — each in a sentence or two.')}
{card('sources/', 'Sources', f'{len(SOURCES)} numbered', 'Every citation on the site, with a link.')}
</div>

<h2>How to read this site</h2>
<div class="prose">
<p>Every number on these pages comes from one of two places. The computed ones — the count of primes, the
zeta zeros, the cost curve, the worked examples — are produced by <code>tools/compute.py</code> at build
time, and <a href="{BASE}riemann/#checks">{F['checks']['total']} checks</a> run before the site will
publish ({F['checks']['failures']} failing as of {TODAY}). The historical and recent ones live in data
files with a source on every row, and the source list is <a href="{BASE}sources/">one page</a>.</p>
<p>Where a claim reached the press, the <a href="{BASE}quantum/#claims">claims table</a> gives what was
said and what was done, side by side. Where a fact rests on a single secondary source it is marked
<span class="tag c2">unconfirmed</span>.</p>
<p>The pictures are computed too: the spiral, the sieve, the strip, the curve. No photograph, no stock.</p>
</div>"""]
    ld = {"@context": "https://schema.org", "@type": "WebSite", "name": NAME, "url": SITE_URL + "/",
          "description": TAG, "license": "https://creativecommons.org/licenses/by/4.0/",
          "author": {"@type": "Person", "name": "Nan", "url": "https://hongdam.net/"},
          "publisher": fleet.publisher_ld(FLEET), "sameAs": fleet.same_as(SELF, roster=FLEET)}
    return page("", "".join(b), "", TAG, "", jsonld=ld)


# ---------------------------------------------------------------------- split

def split():
    ex = F["examples"]
    fer = ex["fermat"]
    dens = F["primes"]["density"]
    b = [f"""<h1><span class="kind">Make one, break one</span>Split</h1>
<p class="lede">Multiplying is cheap. Splitting is the whole problem. The box below makes a product of two
primes at whatever size you like and then tries to get the primes back, with a live count of the work.
Watch the wall arrive.</p>

<div class="tool" id="split">
<h3>Make a semiprime, then split it</h3>
<div class="row"><label>digits in each prime</label>
<span class="units">
<button data-digits="3" aria-pressed="false">3</button>
<button data-digits="6" aria-pressed="true">6</button>
<button data-digits="9" aria-pressed="false">9</button>
<button data-digits="12" aria-pressed="false">12</button>
<button data-digits="16" aria-pressed="false">16</button>
<button data-digits="20" aria-pressed="false">20</button>
</span></div>
<div class="row"><button class="go" id="make">make a new one</button>
<button id="trial">split by trial division</button>
<button id="rho">split by Pollard rho</button>
<button id="stop">stop</button></div>
<div class="out" id="splitout"></div>
<p class="small mute">Trial division tries every odd number up to the square root. Pollard's rho method
(1975) walks a pseudo-random path and needs about the square root of the <i>smaller prime</i> — the square
root of the square root. At 6 digits both finish. At 12, rho finishes and trial division shows you its
projection. At 20 neither finishes, and the projection is the point.</p>
</div>

<h2>Why there are always enough primes</h2>
<div class="prose">
<p>Making a key means finding two primes of about 309 digits. That only works because primes never run
out and never get too thin. The Prime Number Theorem {cite('hadamard1896')} says that near a number x,
about one in every ln x whole numbers is prime — ln being the natural logarithm, a number that grows very
slowly. So:</p>
</div>
<div class="wrap"><table><thead><tr><th>size of the number</th><th class="n">about one prime in every</th></tr></thead><tbody>""",
         *[f'<tr><td>{d["digits"]} digits</td><td class="n">{d["one_in"]}</td></tr>' for d in dens],
         f"""</tbody></table></div>
<div class="prose">
<p>At 309 digits, one number in about {dens[-2]['one_in']} is prime — and only the odd ones need testing, so
one in {dens[-2]['one_in'] // 2}. Pick random numbers, test each with a fast test that can tell prime from
not (Miller–Rabin, 1976–1980; certain-if-the-Riemann-Hypothesis-holds in one version, almost-certain in
the one everyone uses {cite('miller1976')}), and a prime turns up in a few hundred tries. Your browser
does it below.</p>
</div>

<div class="tool">
<h3>A 2048-bit key, made here</h3>
<p class="small mute">Two 1024-bit primes, found by the same test, multiplied. This is the shape of the
key that guards most of the web.</p>
<div class="row"><button class="go" id="big">make one</button></div>
<div class="out" id="bigout"><span class="k">press the button — a second or two</span></div>
</div>

<h2>Why the two primes are kept apart</h2>
<div class="prose">
<p>Fermat noticed in 1643 {cite('fermat1643')} that any odd number is a difference of two squares, a² −
b², and that (a − b)(a + b) is then a factorisation. Walk a up from the square root of N and check whether
a² − N is a perfect square. If the two primes are close together, a starts near both of them and the walk
is short. The primes {n(fer['p'])} and {n(fer['q'])} give N = {n(fer['N'])}, and Fermat's walk finds them
in {fer['steps']} steps. Key generators keep their two primes far apart for exactly this reason, and one of
the 2024 'RSA-2048 broken' papers turned out to have chosen its numbers so that the primes differed in two
bits {cite('wang2024b')}.</p>
</div>
{fig('band-wave.jpg', 'a^x mod 143 for x from 0: the values look random until the amber bars, where the sequence comes back to 1, at a steady spacing. That spacing is the period, and reading it is the one thing a quantum computer does that a classical one cannot — see the <a href="' + BASE + 'quantum/">quantum page</a>.')}
"""]
    return page("Split — make a semiprime, then break it", "".join(b), "split/",
                "Make a product of two primes at any size and watch trial division and Pollard rho try to "
                "get them back; then make a 2048-bit key in your browser.", "split/", scripts=("split.js",))


# -------------------------------------------------------------------- history

def history():
    ev = D["timeline"]["events"]
    items = []
    for e in ev:
        items.append(f'<li class="{e["lane"]}"><span class="when">{E(e["when"])}</span>'
                     f'<span class="who">{E(e["who"])}</span><p>{e["what"]} {cites(e["src"])}</p></li>')
    lanes = {"classical": sum(1 for e in ev if e["lane"] == "classical"), "quantum": sum(1 for e in ev if e["lane"] == "quantum"), "riemann": sum(1 for e in ev if e["lane"] == "riemann")}
    b = [f"""<h1><span class="kind">240 BC to this month</span>History</h1>
<p class="lede">{len(ev)} events. Teal dots are the classical story — sieves, congruences, records. Rose
dots are the quantum one. Violet dots are Riemann's: the count of the primes, and the hypothesis that
sits under the whole subject without ever touching a key.</p>

{fig('band-sieve.jpg', 'The sieve of Eratosthenes as stripes: one row per small prime, a tick at each multiple, and the last row is what survives. Every factoring record since 1981 begins with a sieve like this one, run over a different kind of number.')}

<div class="tool">
<h3>The sieve, 240 BC</h3>
<p class="small mute">Write the numbers out. Take the first one standing, keep it, strike its multiples.
Repeat. Once the striking prime passes the square root of the last number, everything left is prime.</p>
<canvas id="sieve" width="900" height="600" aria-label="a grid of the numbers 1 to 600, primes in amber, struck numbers in the colour of the prime that struck them"></canvas>
<div class="row"><button class="go" id="sieveplay">play</button><button id="sievestep">one prime</button><button id="sievereset">reset</button></div>
<div class="out" id="sieveout"></div>
</div>

<p class="small"><span class="tag c1">classical · {lanes['classical']}</span> <span class="tag c2">quantum · {lanes['quantum']}</span> <span class="tag v">Riemann · {lanes['riemann']}</span></p>
<ul class="tl">{"".join(items)}</ul>

<h2>What the story adds up to</h2>
<div class="prose">
<p>Three things have moved the record. New mathematics: Kraitchik's two squares, Pomerance's sieve, the
number field sieve, Shor's period. More hardware: Lehmer's bicycle chain, six hundred volunteers' PCs, a
cluster, a data centre of GPUs. And the same cost curve, drawn over and over, with the same shape: each
doubling of the key's length multiplies the work by something between a hundred and a few thousand,
never by two. That is why 512 bits fell in 1999, 768 in 2009, 896 in 2026, and 2048 is still nowhere
near — on classical machines. The <a href="{BASE}records/">records page</a> draws the curve.</p>
<p>The quantum lane is a different kind of story: one idea in 1994, thirty years of estimates of what it
would cost to run, and hardware that as of {E(AS_OF)} has split the number 21. The
<a href="{BASE}quantum/">quantum page</a> puts the estimates and the machines on one chart.</p>
</div>"""]
    return page("History — factoring from Eratosthenes to this month", "".join(b), "history/",
                f"{len(ev)} dated events in the history of factoring, the Riemann Hypothesis and quantum "
                "factoring, from the sieve of Eratosthenes to the September 2026 records.", "history/",
                scripts=("sieve.js",))


# -------------------------------------------------------------------- methods

def methods():
    k = F["examples"]["kraitchik"]
    rel = k["relations"]
    r41 = rel[0]
    r43 = next(r for r in rel if r["x"] == 43)
    b = [f"""<h1><span class="kind">Sieves</span>Methods</h1>
<p class="lede">Every classical method since 1926 is the same trick with better tools: find two numbers
whose squares agree when divided by N, and the greatest common divisor does the rest. Here is the trick on
a number small enough to do by hand, and four old methods racing on numbers of different shapes.</p>

<h2>Four methods, one number</h2>
<div class="tool" id="race">
<div class="row"><label>the number</label><select id="racepick"></select><button class="go" id="racego">race</button></div>
<div class="out" id="raceout"></div>
<p class="small mute">Bars are steps taken, on a log scale. Each method gives up at three million steps.
Pick a different number and a different method wins — that is the lesson. Trial division likes a small
factor; Fermat likes two close ones; p − 1 likes a factor whose neighbour is made of small primes; rho does
not care and is slow. The number field sieve, below, is what you use when you know nothing about the
shape.</p>
</div>

<h2>Two squares that agree</h2>
<div class="prose">
<p>Fermat's idea needs N itself to be a² − b². Kraitchik's improvement {cite('kraitchik1926')} is that you
only need two numbers whose squares leave the same remainder when divided by N:</p>
{eq("x² ≡ y² (mod N)&nbsp;&nbsp;&nbsp;⇒&nbsp;&nbsp;&nbsp;N divides (x − y)(x + y)", "if x² and y² differ by a multiple of N, then N divides the product on the right — and unless x ≡ ±y, N has to share part of itself with each bracket. gcd(x − y, N) is a factor.")}
<p>Finding such a pair directly is as hard as factoring. The trick is to <em>build</em> one. Take x just
above √N, so that x² − N is small, and keep the ones that break into small primes — the
<strong>smooth</strong> ones. Then multiply a handful together so that every prime appears an even number
of times: the product is a square by construction.</p>
<p>Carl Pomerance's example {cite('pomerance1996')}, N = {k['N']}:</p>
{eq(f"{r41['x']}² = {r41['x2']} = {k['N']} + {r41['q']}, &nbsp;and {r41['q']} = 2⁵<br>{r43['x']}² = {r43['x2']} = {k['N']} + {r43['q']}, &nbsp;and {r43['q']} = 2³ · 5²", "two squares just above N whose leftovers are made of small primes")}
{eq(f"({r41['x']} · {r43['x']})² ≡ {r41['q']} · {r43['q']} = {r41['q'] * r43['q']} = {k['Y']}² (mod {k['N']})", f"multiply the two: the left is a square, and the right — 2⁸ · 5² — is a square too. So X = {r41['x']} · {r43['x']} = {r41['x'] * r43['x']} ≡ {k['X']}, Y = {k['Y']}.")}
{eq(f"gcd({k['X']} − {k['Y']}, {k['N']}) = gcd({k['X'] - k['Y']}, {k['N']}) = {k['gcd']}, &nbsp;&nbsp;{k['N']} = {k['gcd']} × {k['other']}", "Euclid's algorithm, two thousand years old, finishes the job.")}
</div>

<div class="tool" id="kra">
<h3>Try it on a number</h3>
<div class="row"><label>N</label><input type="text" id="kran" value="{k['N']}" size="12">
<button class="go" id="krago">find two squares</button>
<span class="units"><button data-n="1649">1649</button><button data-n="8051">8051</button><button data-n="10403">10403</button><button data-n="87463">87463</button><button data-n="1000009">1000009</button></span></div>
<div class="out" id="kraout"></div>
<p class="small mute">The parities column is what the linear algebra works on: a row of 0s and 1s, one
per small prime, saying whether that prime appears an odd number of times. A set of rows that adds to all
zeros (mod 2) is a square. About half the squares found are duds — X ≡ ±Y — and then you take the next.</p>
</div>

<h2>From the trick to the records</h2>
<div class="prose">
<p><strong>Dixon, 1981</strong> {cite('dixon1981')} — pick random x, keep the smooth x² mod N, do the
linear algebra. The first method with a proved sub-exponential running time.</p>
<p><strong>The quadratic sieve, 1981</strong> {cite('pomerance1985', 'pomerance1996')} — do not test each
x² − N for small factors one at a time. Notice that if p divides x² − N then it also divides (x + p)² − N,
so a prime p marks every p-th entry in the row — the sieve of Eratosthenes again, run over the values
x² − N. That is where the name comes from and why it was ten to a hundred times faster than what came
before. It set every record from 1983 to 1994, including the 129-digit number from Martin Gardner's
column {cite('atkins1995')}.</p>
<p><strong>The number field sieve, 1988–1993</strong> {cite('nfs1993', 'lenstra1993')} — the same plan,
but the smooth values are found in a larger number system than the integers, where they are far smaller
and so far more often smooth. The price is a lot of algebra to get back to ordinary integers at the end.
It is the fastest method known for numbers of no special form, and every record since 1996 is a run of it
— the 2019, 2020 and 2026 records all with the same open-source program, CADO-NFS
{cite('cadonfs', 'boudot2020', 'lu2026', 'weis2026')}.</p>
<p><strong>The elliptic curve method, 1985</strong> {cite('lenstra1987')} — a different family: its cost
depends on the size of the factor it finds, not the size of N. It is the tool for pulling a 30-digit factor
out of a 300-digit number, and it is the first place the curves of the wallet page appear in factoring.</p>
<p>What none of them do is scale kindly. The next page draws the cost curve.</p>
</div>"""]
    return page("Methods — two squares that agree, and four methods racing", "".join(b), "methods/",
                "Kraitchik's trick on Pomerance's example, a race between trial division, Fermat, Pollard "
                "rho and p−1, and how the quadratic and number field sieves grew out of it.", "methods/",
                scripts=("race.js", "kraitchik.js"))


# -------------------------------------------------------------------- records

def records():
    R = D["records"]
    c = F["cost"]
    by = {r["bits"]: r for r in c["rows"]}
    rows = []
    for r in R["rows"]:
        rows.append(f'<tr><td>{E(r["name"])}</td><td class="n">{r["digits"]}</td><td class="n">{r["bits"]}</td>'
                    f'<td class="d">{E(r["date"])}</td><td>{E(r["team"])}</td><td>{E(r["method"])}</td><td>{E(r["effort"])} {cites(r["src"])}</td></tr>')
    op = "".join(f'<tr><td>{E(r["name"])}</td><td class="n">{r["digits"]}</td><td class="n">{r["bits"]}</td><td colspan="4">{E(r["note"])} {cites(r["src"])}</td></tr>' for r in R["open"])
    sp = "".join(f'<tr><td>{E(r["name"])}</td><td class="n">{r["digits"]}</td><td class="n">{r["bits"]}</td><td class="d">{E(r["date"])}</td><td>{E(r["team"])}</td><td>{E(r["method"])}</td><td>{E(r["note"])} {cites(r["src"])}</td></tr>' for r in R["special"])
    b = [f"""<h1><span class="kind">1991 to this month</span>Records</h1>
<p class="lede">Every general-purpose factoring record since the RSA challenge list was published, the
curve they sit on, and a ruler for how far a 2048-bit key is from the biggest number anyone has split.</p>

{fig('records.svg', 'Bits in the record number against the year. The 2026 pair are the first records set on GPUs and the first set with the help of AI coding agents; both authors said the mathematics did not change ' + cite('lu2026', 'weis2026') + '.')}

<div class="wrap"><table><thead><tr><th>number</th><th class="n">digits</th><th class="n">bits</th><th>date</th><th>who</th><th>method</th><th>effort</th></tr></thead>
<tbody>{"".join(rows)}</tbody>
<tbody><tr><th colspan="7">still open</th></tr>{op}</tbody>
<tbody><tr><th colspan="7">special form — a different, easier sieve; not comparable</th></tr>{sp}</tbody></table></div>
<p class="small mute">The two 2026 rows are not on the RSA challenge list's own cadence: RSA-260 was the
next unsolved challenge number; RSA-896 was a 270-digit challenge number picked because it was a round
number of bits. Effort units change with the era — MIPS-years, Opteron-years, Xeon core-years, GPU-years
— and are not convertible without a footnote; the sources give each team's own figure.</p>

<h2>The curve</h2>
<div class="prose">
<p>The number field sieve's running time has a known shape {cite('nfs1993')}:</p>
{eq("L(N) = exp( c · (ln N)<sup>1/3</sup> · (ln ln N)<sup>2/3</sup> ),&nbsp;&nbsp; c = (64/9)<sup>1/3</sup> ≈ " + f"{c['c']:.3f}", "not exponential in the number of bits (that would be 2 to the bits), and not a fixed power of the bits either; in between, with the 1/3 doing the work. Constants and lower-order terms are missing, which is why this is a ruler and not a forecast.")}
<p>Anchor it on RSA-250 — {n(int(c['anchor']['core_years']))} core-years for {c['anchor']['bits']} bits
{cite('rsa250')} — and read off the rest:</p>
</div>
<div class="wrap"><table><thead><tr><th class="n">bits</th><th class="n">digits</th><th class="n">times RSA-250</th><th class="n">core-years, scaled</th><th>in words</th></tr></thead><tbody>""",
         *[f'<tr><td class="n">{r["bits"]}</td><td class="n">{r["digits"]}</td><td class="n">{r["relative_to_rsa250"]:.3g}</td><td class="n">{r["core_years"]:.3g}</td><td>{words(r["core_years"])}</td></tr>' for r in c["rows"]],
         f"""</tbody></table></div>
{fig('cost.svg', 'The same curve drawn. The RSA-768 team said 1024 bits was about a thousand times harder than 768; the ruler here says ' + f"{c['ratio_768_1024']:.0f}" + '×, which is the same order. The 2026 GPU runs do not move the curve; they move the price of a core-year.')}

<div class="tool">
<h3>The ruler</h3>
<div class="row"><label>key size</label><input type="range" id="bits" min="512" max="4096" step="32" value="2048"> <span class="v" id="bitsv">2048</span> bits</div>
<div class="out" id="costout"></div>
</div>

<h2>What the 2026 records changed</h2>
<div class="prose">
<p>Two things, and neither is the mathematics. Eric Lu's RSA-260 run in early September and Stephen
Weis's RSA-896 run two weeks later both ported CADO-NFS to data-centre GPUs, with AI coding agents doing
much of the port {cite('lu2026', 'weis2026')}. Weis's ran as a low-priority job on idle machines: about
thirty GPU-years in ten days, at no marginal cost to anyone. His own conclusion: the running time of the
sieve did not improve, deployed 2048-bit keys are not affected — and a 1024-bit key is now within reach
of anyone with a large GPU fleet and a slow month. Old keys do not retire themselves; in 2015 a 512-bit key
cost $75 of cloud time to break and hundreds were still in use {cite('valenta2015')}.</p>
</div>"""]
    return page("Records — every general-purpose factoring record since 1991", "".join(b), "records/",
                "The RSA challenge records from RSA-100 in 1991 to RSA-896 in September 2026, the number "
                "field sieve's cost curve, and a ruler for any key size.", "records/", scripts=("cost.js",))


def words(y):
    if y < 1 / 365:
        return f"about {y * 365 * 24:.0f} hours of one core"
    if y < 1:
        return f"about {y * 365:.0f} days of one core"
    if y < 1e4:
        return f"about {y:,.0f} core-years — a big cluster for a year"
    if y < 1e7:
        return f"about {y:,.0f} core-years — every core in a large data centre for years"
    return f"{y:.1e} core-years — more computing than has been done on Earth"


# -------------------------------------------------------------------- quantum

def quantum():
    s15, s21 = F["examples"]["shor15"], F["examples"]["shor21"]
    C = D["claims"]
    EST = D["estimates"]["rows"]
    M = D["machines"]
    crow = []
    for r in C["rows"]:
        crow.append(f'<tr><td class="d">{E(r["date"])}</td><td>{E(r["who"])}</td><td>{E(r["claimed"])}</td>'
                    f'<td>{E(r["did"])}</td><td><b>{E(r["verdict"])}</b> {cites(r["src"])}</td></tr>')
    erow = []
    for r in EST:
        erow.append(f'<tr><td class="d">{E(r["date"])}</td><td>{E(r["who"])}</td><td>{"RSA-2048" if r["target"] == "rsa2048" else "256-bit curve key"}</td>'
                    f'<td class="n">{n(r["physical"]) if r["physical"] else "—"}</td><td class="n">{n(r["logical"]) if r["logical"] else "—"}</td><td>{E(r["time"])}</td><td>{E(r["note"])} {cites(r["src"])}</td></tr>')
    mrow = "".join(f'<tr><td class="d">{m["year"]:.0f}</td><td>{E(m["name"])}</td><td class="n">{n(m["physical"])}</td><td class="n">{m["logical"] if m["logical"] else "—"}</td><td>{cites(m["src"])}</td></tr>' for m in M["rows"])
    b = [f"""<h1><span class="kind">Shor, and the bill</span>Quantum</h1>
<p class="lede">In 1994 Peter Shor showed that a quantum computer could split any number in a number of
steps that grows like a small power of its length — not the L(1/3) curve, not anything near it
{cite('shor1997')}. The quantum part of the algorithm does one thing: it finds how often a sequence
repeats. Here is that one thing, then every claim to have done it on hardware, then the bill.</p>

<h2>The period</h2>
<div class="prose">
<p>Pick a number a with no factor in common with N and write down a, a², a³, … each reduced mod N. The
sequence has to repeat, because there are only N remainders. Call the spacing r, the <strong>period</strong>.
Then, half the time or better, a<sup>r/2</sup> is a square root of 1 mod N that is not ±1, and</p>
{eq("N divides (a<sup>r/2</sup> − 1)(a<sup>r/2</sup> + 1),&nbsp;&nbsp; gcd(a<sup>r/2</sup> ± 1, N) are the factors", "the same two-squares trick as the methods page: a^(r/2) squared is 1, so a^(r/2) and 1 are two numbers whose squares agree mod N.")}
<p>For N = {s15['N']} and a = {s15['a']}: the sequence runs {", ".join(str(v) for v in s15['sequence'][:8])}, … with period
{s15['period']}; {s15['a']}<sup>{s15['period'] // 2}</sup> mod {s15['N']} = {pow(s15['a'], s15['period'] // 2, s15['N'])}, and gcd({pow(s15['a'], s15['period'] // 2, s15['N']) - 1}, {s15['N']}) = {s15['factors'][0]},
gcd({pow(s15['a'], s15['period'] // 2, s15['N']) + 1}, {s15['N']}) = {s15['factors'][1]}. That is the arithmetic the 2001 IBM experiment did {cite('vandersypen2001')}. For 21 with a = {s21['a']}
the period is {s21['period']} and the factors are {s21['factors'][0]} and {s21['factors'][1]} {cite('martinlopez2012')}.</p>
<p>Finding r classically means walking the sequence, which for a 2048-bit N is a walk as long as trial
division. A quantum register holds all the values a<sup>x</sup> at once, and the quantum Fourier transform
turns that into a set of readings that peak at multiples of Q/r — the frequency of the beat. Read one, do
a little arithmetic with continued fractions, and you have r. That is the whole quantum step.</p>
</div>

<div class="tool">
<h3>Watch the period</h3>
<div class="row"><label>N</label><select id="pN"></select><label>a</label><select id="pa"></select></div>
<canvas id="period" width="880" height="220" aria-label="the sequence a to the x mod N as bars, with the returns to 1 in amber"></canvas>
<canvas id="freq" width="880" height="150" style="margin-top:.5rem" aria-label="the frequency view: peaks at multiples of Q over r"></canvas>
<div class="out" id="periodout"></div>
<p class="small mute">Top: the sequence. Bottom: what the quantum computer reads — the Fourier transform of
the beat, computed here on 128 points the slow way. Some choices of a fail (odd period, or the trivial
root); Shor's algorithm picks another a and goes again.</p>
</div>

<h2 id="claims">Every claim, beside what was done</h2>
<div class="prose">
<p>The largest number split by Shor's algorithm on real hardware, as of {E(AS_OF)}, is
<b>{C['largest_shor_hardware']['number']}</b>, in {C['largest_shor_hardware']['year']} — and that run, like
every hardware run of Shor so far, was 'compiled' with knowledge of the answer, which Smolin, Smith and
Vargo showed lets two qubits 'factor' any number you like {cite('smolin2013')}. Everything larger in the
press was one of: an adiabatic minimisation with no known scaling advantage, a classical method with a
small quantum step bolted on, a number chosen to be easy, or a toy curve key.</p>
</div>
<div class="wrap"><table><thead><tr><th>date</th><th>who</th><th>what was said</th><th>what was done</th><th>verdict</th></tr></thead><tbody>{"".join(crow)}</tbody></table></div>

<h2>The bill</h2>
<div class="prose">
<p>Since nobody can run Shor at scale, the field publishes estimates: how many physical qubits, at what
error rate, for how long. The estimates have fallen a thousandfold in fourteen years, all on paper. Each
one assumes a physical error rate of about one in a thousand and a code that turns many noisy qubits into
one reliable one; the newest ones assume codes and wiring that do not exist yet at scale.</p>
</div>
<div class="wrap"><table><thead><tr><th>date</th><th>who</th><th>target</th><th class="n">physical qubits</th><th class="n">logical</th><th>time</th><th>note</th></tr></thead><tbody>{"".join(erow)}</tbody></table></div>

{fig('qubits.svg', 'The gap. Amber and rose dots: what a paper says would break a key. The teal step: the most physical qubits any named machine has had. Note the vertical scale — each gridline is ten times the last. The 2026 estimates and the 2026 machines are still two to three gridlines apart, before counting that the machines’ qubits are far noisier than the papers assume.')}

<h2>The machines</h2>
<div class="wrap"><table><thead><tr><th>year</th><th>machine</th><th class="n">physical qubits</th><th class="n">logical</th><th></th></tr></thead><tbody>{mrow}</tbody></table></div>
<div class="prose">
<p>Physical qubits are the noisy ones a chip has. Logical qubits are the reliable ones built from them by
error correction, and the exchange rate has been about a thousand to one for the surface code. Google's
Willow (December 2024) was the first chip clearly past the point where adding physical qubits makes the
logical one better instead of worse {cite('willow2024')}; Quantinuum's Helios (November 2025) holds 48
logical qubits, the most anywhere {cite('helios2025')}. The papers want more than a thousand logical
qubits running billions of operations. IBM's roadmap puts 200 logical qubits in 2029 {cite('ibm2025')}.</p>
<p>The <a href="{BASE}wallet/">wallet page</a> has the 2026 estimates for a curve key specifically, and
the ten-minute question.</p>
</div>"""]
    return page("Quantum — Shor's period, every hardware claim, and the bill", "".join(b), "quantum/",
                "Shor's algorithm with the period you can watch, every quantum factoring claim beside what "
                "it did, the resource estimates from 2012 to 2026, and the machines.", "quantum/",
                scripts=("period.js",))


# -------------------------------------------------------------------- riemann

def riemann():
    P = F["primes"]
    Zs = F["zeros"]
    X = F["explicit"]
    chk = F["checks"]
    trow = "".join(f'<tr><td class="n">10<sup>{len(str(r["x"])) - 1}</sup></td><td class="n">{n(r["pi"])}</td><td class="n">{r["x_over_ln"]:,.0f}</td><td class="n">{r["err_ln"]:+,.0f}</td><td class="n">{r["li"]:,.1f}</td><td class="n">{r["err_li"]:+.1f}</td></tr>' for r in P["table"])
    checks = "".join(f'<li>{"<b>ok</b>" if c["ok"] else "<b style=color:var(--c2)>BAD</b>"} {E(c["name"])}</li>' for c in chk["list"])
    b = [f"""<h1><span class="kind">A hundred zeros, computed</span>Riemann</h1>
<p class="lede">Riemann's 1859 paper is eight pages on how many primes there are below a given size
{cite('riemann1859')}. It contains a guess that has stood unproved for 167 years, a million-dollar
prize, and the reason this page exists: people keep asking whether proving it would break RSA. It would
not. Here is what it is, computed rather than described.</p>

<h2>Counting primes</h2>
<div class="prose">
<p>Write π(x) for the number of primes up to x. Gauss, at fifteen, guessed from tables that π(x) runs
like x / ln x, and later that the integral li(x) = ∫ dt / ln t does better {cite('gauss1801')}. Both
were proved right in 1896 {cite('hadamard1896')}. The sieve in <code>tools/compute.py</code> counts to ten
million:</p>
</div>
<div class="wrap"><table><thead><tr><th class="n">x</th><th class="n">π(x)</th><th class="n">x / ln x</th><th class="n">miss</th><th class="n">li(x)</th><th class="n">miss</th></tr></thead><tbody>{trow}</tbody></table></div>
{fig('pi.svg', 'On log scales the three lines are one line — that is the Prime Number Theorem. The table is the story: li(x) misses by a few hundred where x / ln x misses by tens of thousands.')}
<div class="prose">
<p>The Riemann Hypothesis is a statement about that last column. It says the miss of li(x) never grows
faster than about √x · ln x — the primes are spread as evenly as a random process could spread them, with
no long-range conspiracy in either direction. Every check ever made agrees; nobody has proved it.</p>
</div>

<h2>The zeros</h2>
<div class="prose">
<p>Riemann's function is</p>
{eq("ζ(s) = 1 + 1/2<sup>s</sup> + 1/3<sup>s</sup> + 1/4<sup>s</sup> + … = ∏<sub>p</sub> 1 / (1 − p<sup>−s</sup>)", "the sum over all whole numbers equals a product over all primes — Euler's identity, and the reason a function about the whole numbers knows where the primes are.")}
<p>Extended to complex s, it has zeros. The uninteresting ones sit at −2, −4, −6, … The interesting ones
sit in the strip where the real part of s is between 0 and 1, and Riemann observed that every one he
computed had real part exactly ½ — the <strong>critical line</strong> — and wrote that it was 'very
probable' they all do. That sentence is the Hypothesis.</p>
<p>This site computed the first {Zs['count']} of them, by Euler–Maclaurin summation of ζ along the line
and bisection on sign changes of the Riemann–Siegel Z function, and checked the count against the
Riemann–von Mangoldt formula so none was skipped. The first ten agree with Odlyzko's tables
{cite('odlyzkotables')} to {Zs['max_err_first_ten']:.0e}:</p>
</div>
<div class="wrap"><table><thead><tr><th class="n">#</th>{"".join(f'<th class="n">{i + 1}</th>' for i in range(10))}</tr></thead>
<tbody><tr><td>t</td>{"".join(f'<td class="n">{g:.6f}</td>' for g in Zs['first'])}</tr></tbody></table></div>
{fig('zeros.svg', 'Z(t) is ζ(½ + it) with its phase stripped off, so it is a real wave, and it crosses zero exactly where ζ does. The amber points are the first ten crossings.')}
{fig('band-zeros.jpg', 'The critical strip laid on its side: the real part of s runs down the picture from 1.4 at the top to −0.4 at the bottom, t runs left to right from 2 to 60, brightness is the size of ζ. The dark wells are the zeros, and every one sits on the rose line, where the real part is ½. Turing checked the first few thousand this way on the Manchester machine in 1950, hoping to find one off the line ' + cite('turing1953') + '; the count is now past ten trillion ' + cite('platt2021') + '.')}

<h2>The zeros draw the primes</h2>
<div class="prose">
<p>Here is the part that makes the Hypothesis matter. Riemann's <strong>explicit formula</strong> writes
the count of primes exactly in terms of the zeros. In the cleanest form, with ψ(x) counting each prime
power p<sup>k</sup> ≤ x with weight ln p:</p>
{eq("ψ(x) = x − Σ<sub>ρ</sub> x<sup>ρ</sup>/ρ − ln 2π − ½ ln(1 − x<sup>−2</sup>)", "the smooth guess x, minus one wave per zero ρ = ½ + iγ. Each wave has size √x and wobbles ln x · γ / 2π times per unit of ln x. Add them all and the staircase of primes comes out exactly.")}
<p>The slider adds the {Zs['count']} zeros one at a time. With none, the formula is the line x. With ten,
the big wobbles. With a hundred, the steps at every prime and prime power are there, to within
{X['rms_100']:.2f} on average between the steps.</p>
</div>
<div class="tool">
<h3>Add the zeros</h3>
<div class="row"><label>zeros</label><input type="range" id="nzeros" min="0" max="100" value="0"> <button id="zplay">play</button></div>
<canvas id="explicit" width="880" height="360" aria-label="{E(ALT['explicit.svg'])}"></canvas>
<div class="out" id="explicitout"></div>
</div>
{fig('explicit.svg', 'The same thing drawn at build time: ψ(x) as a staircase, and the formula with 0, 10, 30 and 100 zeros.')}
<div class="prose">
<p>Now the Hypothesis in one sentence: if every zero has real part ½, every wave has size exactly √x,
and the primes can never stray from their smooth count by more than about √x · ln x. If some zero had real
part ¾, its wave would have size x<sup>¾</sup>, and the primes would bunch and thin on a scale nobody has
seen. That is all it says. It is a statement about the error term.</p>
</div>

<h2>What it would and would not do to a key</h2>
<div class="prose">
<p><strong>Would not:</strong> give anyone a factoring algorithm. No method on this site — not the sieves,
not the number field sieve, not Shor — runs faster if the Hypothesis is true, because none of them uses
it. Their running times rest on how often values are smooth, and the heuristics for that are about
smooth numbers, not zeros. A proof would be one of the great events in mathematics and would change no
key size anywhere. The wallet, likewise.</p>
<p><strong>Would, a little:</strong> tidy up some proofs. Miller's 1976 primality test is fast and
<em>certain</em> if the Generalised Riemann Hypothesis holds {cite('miller1976')}; without it, Rabin's
1980 version is fast and almost certain, and that is what every key generator on Earth uses, so nothing
changes in practice. Since 2002 there has been a fast certain test with no hypothesis at all
{cite('aks2004')}. Telling prime from composite is easy. Splitting a composite is the problem, and the
Hypothesis is silent on it.</p>
<p><strong>Where the Hypothesis and quantum computing do meet</strong> is somewhere else entirely. In 1972
Hugh Montgomery showed Freeman Dyson his formula for how the zeros space themselves out, and Dyson
recognised it on the spot: it was the spacing of the energy levels of a heavy atomic nucleus, from random
matrix theory {cite('montgomery1973')}. Odlyzko's computations of millions of zeros matched it to high
precision {cite('odlyzko1987')}. The suggestion — Hilbert's and Pólya's, a century old — is that the zeros
are the energy levels of some quantum system nobody has found, and Berry and Keating have a candidate
{cite('berry1999')}. A proof might come from physics. It still would not touch a key.</p>
<p><strong>Recent:</strong> in 2024 Larry Guth and James Maynard gave the first improvement since 1940 on
how many zeros can sit off the line in a given range {cite('guth2024')} — progress on the Hypothesis, not
a proof. Yitang Zhang's 2022 preprint on the Landau–Siegel zero, a related question, has one arXiv version
and no journal {cite('zhang2022')}. Several 2025–2026 preprints claim full proofs; none has been accepted
by a journal or by the field. The problem is open, and the Clay Institute's million is unclaimed
{cite('clay')}.</p>
</div>

<h2 id="checks">The checks</h2>
<p class="small mute">{chk['total']} checks run before this site publishes; {chk['failures']} failing as of
{TODAY}.</p>
<ul class="checks">{checks}</ul>"""]
    return page("Riemann — the primes counted, a hundred zeros computed, and what the Hypothesis would do to a key", "".join(b), "riemann/",
                "The Prime Number Theorem measured to ten million, the first hundred zeta zeros computed, "
                "the explicit formula drawing the primes, and why proving the Riemann Hypothesis would not "
                "break RSA.", "riemann/", scripts=("zeros.js",))


# --------------------------------------------------------------------- wallet

def wallet():
    W = D["wallet"]
    cv = F["curve"]
    orow = "".join(f'<tr><td><b>{E(o["type"])}</b><br><span class="small mute">{E(o["since"])}</span></td><td class="d">{E(o["prefix"])}</td><td><span class="tag {"c2" if o["exposed"] == "always" else "c1"}">{E(o["exposed"])}</span></td><td>{E(o["note"])} {cites(o["src"])}</td></tr>' for o in W["outputs"])
    xrow = "".join(f'<tr><td>{E(x["who"])}</td><td class="d">{E(x["date"])}</td><td class="n">{x["btc"] / 1e6:.2f}M</td><td class="n">{x["share"] * 100:.0f}%</td><td>{E(x["method"])} {cites(x["src"])}</td></tr>' for x in W["exposure"])
    arow = "".join(f'<h3>{E(a["name"])}</h3><p>{E(a["what"])} {cites(a["src"])}</p>' for a in W["attacks"])
    wrow = "".join(f'<tr><td>{E(w["who"])}</td><td class="d">{E(w["date"])}</td><td>{E(w["ten_minutes"])}</td><td>{E(w["one_hour"] or "")}</td><td>{E(w["one_day"] or "")}</td><td>{cites(w["src"])}</td></tr>' for w in W["window"])
    prow = "".join(f'<tr><td><b>{E(p["name"])}</b><br><span class="small mute">{E(p["who"])}</span></td><td class="d">{E(p["date"])}</td><td>{E(p["what"])} {cites(p["src"])}</td></tr>' for p in W["proposals"])
    trow = "".join(f'<tr><td>{E(t["who"])}</td><td class="d">{E(t["date"])}</td><td>{E(t["what"])} {cites(t["src"])}</td></tr>' for t in W["timelines"])
    erow = "".join(f'<li><b>{E(e["chain"])}</b> — {E(e["what"])} {cites(e["src"])}</li>' for e in W["elsewhere"])
    b = [f"""<h1><span class="kind">The curve, the window, the proposals</span>Wallet</h1>
<p class="lede">A bitcoin wallet does not use RSA. Its lock is a different hard problem on a curve, broken
by the same quantum algorithm and, on paper, a little more cheaply. This page is the mechanics and the
public record as of {E(AS_OF)}: which coins show their key, what a ten-minute attack would need, and every
draft proposal on the table. It is not advice.</p>

{fig('band-curve.jpg', 'An elliptic curve over the ordinary numbers, y² = x³ − 3x + 3. Draw a line through two points on it and it crosses a third; flip that third point over the axis and you have ‘added’ the two. That rule, done over whole numbers mod a 256-bit prime instead of over a smooth picture, is a wallet.')}

<h2>The lock</h2>
<div class="prose">
<p>Bitcoin's curve is y² = x³ + 7 over the integers mod a particular 256-bit prime, a curve called
secp256k1 {cite('sec2', 'nakamoto2008')}. There is a fixed starting point G on it. Your private key is a
random 256-bit number k. Your public key is the point you reach by adding G to itself k times, written
k·G. Adding is fast, and there is a shortcut (double-and-add) so that 256 doublings get you anywhere. Going
back — given k·G, find k — is the <strong>discrete logarithm</strong>, and the best classical methods
need about 2<sup>128</sup> steps {cite('koblitz1987')}. Same shape as factoring: easy one way, no known
way back.</p>
<p>Here is the same curve over the integers mod {cv['p']} instead, small enough to draw all
{cv['points']} of its points and hop around on it.</p>
</div>
<div class="tool">
<h3>Hop</h3>
<canvas id="curve" width="560" height="560" aria-label="the points of y squared equals x cubed plus seven mod 97, as dots, with the walk from G drawn"></canvas>
<div class="row"><button class="go" id="hop">hop once</button><button id="hopplay">keep hopping</button><button id="challenge">hide k, show k·G</button><button id="brute">brute force</button></div>
<div class="out" id="curveout"></div>
<p class="small mute">G has order {cv['G_order']} here: {cv['G_order']} hops and you are back where you
started. On secp256k1 the order is about 2<sup>256</sup>, and the landing spot after k hops tells you
nothing about k that anyone knows how to read — classically.</p>
</div>
<div class="tool">
<h3>A key, made here</h3>
<p class="small mute">The same arithmetic at full size, in your browser: a random 256-bit k, then k·G on
secp256k1.</p>
<div class="row"><button class="go" id="realkey">make a key</button></div>
<div class="out" id="keyout"><span class="k">press the button</span></div>
</div>

<h2>Which coins show their key</h2>
<div class="prose">
<p>A Bitcoin <strong>address</strong> is usually not the public key. It is a hash of it — a one-way
fingerprint — and the key itself appears on the chain only inside the transaction that spends from the
address {cite('btcdev')}. That one layer is most of the story. Hashes are not broken by Shor's algorithm;
a quantum computer speeds up reversing a hash only by a square root, which a 256-bit hash absorbs. So
what matters is which outputs put the key itself on the chain:</p>
</div>
<div class="wrap"><table><thead><tr><th>output type</th><th>address looks like</th><th>key visible</th><th>note</th></tr></thead><tbody>{orow}</tbody></table></div>
<div class="prose">
<p>The counts of how many coins sit in exposed outputs come from five sources and land in the same
place: about a third of all bitcoin, once address reuse is counted, and about 1.6 to 1.7 million BTC in
the oldest kind alone — coins mined in 2009–2010 and never moved.</p>
</div>
<div class="wrap"><table><thead><tr><th>who counted</th><th>when</th><th class="n">BTC</th><th class="n">of supply</th><th>how</th></tr></thead><tbody>{xrow}</tbody></table></div>
{fig('exposure.svg', 'The five counts. CoinShares counted only the P2PK outputs; the others add reused addresses and, from 2025, Taproot.')}

<h2>The two attacks</h2>
<div class="prose">{arow}</div>

<h2>The ten-minute window</h2>
<div class="prose">
<p>For a never-reused hash address, the key is visible only between broadcast and confirmation. So the
question people ask is whether a machine could take a public key, compute the private key, and get a
competing transaction mined, in the ten minutes a block takes on average. The estimates:</p>
</div>
<div class="wrap"><table><thead><tr><th>who</th><th>when</th><th>to break one key in ten minutes</th><th>in an hour</th><th>in a day</th><th></th></tr></thead><tbody>{wrow}</tbody></table></div>
<div class="prose">
<p>The 2026 papers disagree with each other in an instructive way. Google's team says a fast
superconducting machine of under half a million qubits could do it in minutes, inside the window
{cite('babbush2026')}; the Caltech and IonQ blueprints, on atoms and ions, need ten to twenty-six days per
key, because those qubits tick a thousand times slower {cite('caltech2026', 'haner2026')}. Google
withheld its circuits and published a proof they work, and advised: migrate, do not reuse addresses,
decide what to do about abandoned coins {cite('googleblog2026')}. None of these machines exists; see the
<a href="{BASE}quantum/">gap chart</a>.</p>
</div>

<h2>The proposals</h2>
<div class="prose">
<p>Every one is a draft. None has an activation path. Bitcoin has, as of {E(AS_OF)}, no agreed roadmap,
funding or timeline for a post-quantum move {cite('coindesk2026roadmap')}.</p>
</div>
<div class="wrap"><table><thead><tr><th>proposal</th><th>when</th><th>what it does</th></tr></thead><tbody>{prow}</tbody></table></div>
<div class="prose">
<p>The hard part is not the new signature; NIST has three of those already {cite('nist2024')}. It is the
old coins. A post-quantum output type only protects coins that move to it, and the question of what
happens to coins whose owners never move them — including the 1.7 million BTC from 2009 — is a question
about freezing other people's property, which is why BIP 361's sunset schedule is the contested one
{cite('bip361')}. Migrating every output would take about 76 days of full blocks at best
{cite('chaincode2025')}.</p>
<p>Elsewhere:</p>
<ul>{erow}</ul>
</div>

<h2>The timelines people sign their names to</h2>
<div class="wrap"><table><thead><tr><th>who</th><th>when</th><th>what they said</th></tr></thead><tbody>{trow}</tbody></table></div>
<div class="prose">
<p>Nobody has a date. What exists is a policy calendar (NIST's 2030 and 2035), a corporate one (Google's
2029), an expert survey with odds per decade, and a set of resource estimates that have fallen twentyfold
twice in seven years while the machines grew tenfold once. The <a href="{BASE}now/">ledger</a> is where
each new number lands.</p>
</div>"""]
    return page("Wallet — the curve, the window, and every proposal", "".join(b), "wallet/",
                "How a bitcoin key works, which outputs expose it, how many coins sit in them, what a "
                "ten-minute quantum attack would need, and every post-quantum proposal for Bitcoin as of "
                "September 2026.", "wallet/", scripts=("curve.js",))


# ------------------------------------------------------------------------ now

def now():
    rows = D["developments"]["rows"]
    lanes = sorted({r["lane"] for r in rows})
    lrow = []
    for r in reversed(rows):
        tag = ' <span class="tag c2">unconfirmed</span>' if r["confidence"] != "confirmed" else ""
        lrow.append(f'<tr data-lane="{E(r["lane"])}"><td class="d">{E(r["date"])}</td><td>{E(r["who"])}</td>'
                    f'<td>{E(r["what"])}{tag}</td><td class="mute">{E(r["not"])} {cite(r["src"])}</td></tr>')
    buttons = f'<button data-lane="all" aria-pressed="true">all</button>' + "".join(f'<button data-lane="{E(l)}" aria-pressed="false">{E(l)}</button>' for l in lanes)
    feed = ""
    if RECENT:
        papers = "".join(f'<li><a href="{E(p["url"])}" rel="noopener">{E(p["title"])}</a> <span class="small mute">— {E(p["authors"])}, {E(p["date"])}</span></li>' for p in RECENT["arxiv"][:20])
        news = "".join(f'<li><a href="{E(x["url"])}" rel="noopener">{E(x["title"])}</a> <span class="small mute">— {E(x["source"])}, {E(x["date"])}</span></li>' for x in RECENT["news"][:30])
        errs = f'<p class="small mute">Sources that did not answer: {E("; ".join(RECENT["errors"]))}</p>' if RECENT["errors"] else ""
        feed = f"""<h2>This week's feed <small>fetched {E(RECENT['fetched'][:10])}, unread by a person</small></h2>
<div class="prose"><p>A GitHub Action fetches these every Monday from arXiv and a few public feeds and rebuilds the
page. Titles as published. Nothing here has been checked; the ledger above has.</p></div>
<h3>Papers</h3><ul class="src">{papers or '<li class="mute">none this week</li>'}</ul>
<h3>News</h3><ul class="src">{news or '<li class="mute">none this week</li>'}</ul>{errs}"""
    b = [f"""<h1><span class="kind">The ledger to {E(AS_OF)}</span>Now</h1>
<p class="lede">{len(rows)} dated rows since 2024, newest first, each with what happened and what it does
not mean. Kept by hand from the sources; a row resting on a single secondary source is marked.</p>
<div class="row" id="lanes" style="display:flex;gap:.4rem;flex-wrap:wrap;align-items:center;margin:1rem 0"><span class="units">{buttons}</span> <span class="small mute" id="lanecount">{len(rows)} rows</span></div>
<div class="wrap"><table><thead><tr><th>date</th><th>who</th><th>what happened</th><th>what it does not mean</th></tr></thead><tbody>{"".join(lrow)}</tbody></table></div>
{feed}"""]
    return page("Now — the ledger of developments to " + AS_OF, "".join(b), "now/",
                f"{len(rows)} dated developments in factoring, quantum computing, the Riemann Hypothesis and "
                "Bitcoin's post-quantum plans since 2024, each with what it does not mean.", "now/",
                scripts=("now.js",))


# ---------------------------------------------------------------------- words

def words_page():
    g = D["glossary"]["words"]
    items = "".join(f'<dt id="{E(w["term"].split(",")[0].split(" ")[0].lower())}">{E(w["term"])}</dt><dd>{E(w["def"])}</dd>' for w in g)
    b = [f"""<h1><span class="kind">{len(g)} terms</span>Words</h1>
<p class="lede">Every term used on the site, in a sentence or two, in the order you are likely to meet
them.</p>
<dl class="words">{items}</dl>"""]
    return page("Words — the terms, defined", "".join(b), "words/",
                f"{len(g)} terms from prime and semiprime to qubit and soft fork, each defined in plain words.", "words/")


# -------------------------------------------------------------------- sources

def sources_page():
    items = []
    for sid, (who, what, where, url) in SOURCES.items():
        nn = BY_ID[sid]
        used = "" if sid in USED else ' <span class="tag">listed, not cited on a page</span>'
        items.append(f'<li id="src-{nn}"><b>[{nn}]</b> {E(who)}, <a href="{E(url)}" rel="noopener">{E(what)}</a>. {E(where)}.{used}</li>')
    b = [f"""<h1><span class="kind">{len(SOURCES)} numbered</span>Sources</h1>
<p class="lede">Every citation on the site, in the order the numbers were assigned. Primary where a
primary exists; a press report where that is all there is, and the row that rests on it says so.</p>
<ul class="src">{"".join(items)}</ul>
<h2>Data files</h2>
<div class="prose"><p>The rows behind the tables, as JSON, each with its source ids:
<a href="{BASE}data/timeline.json">timeline</a> · <a href="{BASE}data/records.json">records</a> ·
<a href="{BASE}data/claims.json">claims</a> · <a href="{BASE}data/estimates.json">estimates</a> ·
<a href="{BASE}data/machines.json">machines</a> · <a href="{BASE}data/developments.json">developments</a> ·
<a href="{BASE}data/wallet.json">wallet</a> · <a href="{BASE}data/glossary.json">glossary</a> ·
<a href="{BASE}data/zeros.json">the hundred zeros</a> · <a href="{BASE}data/facts.json">every computed number</a>.
All CC BY 4.0, credit "{E(CREDIT)}".</p></div>"""]
    return page("Sources", "".join(b), "sources/", f"The {len(SOURCES)} sources cited on the site, with links.", "sources/")


def not_found():
    b = f"""<h1><span class="kind">404</span>Not here</h1>
<p class="lede">That page is not on this site. The ones that are:</p>
<div class="grid">{"".join(f'<a class="card" href="{BASE}{h}"><h3>{E(t)}</h3></a>' for h, t in NAV)}</div>
<p><a href="{BASE}">Back to the front</a>.</p>"""
    out = page("Not here", b, "404")
    shutil.move(SITE / "404" / "index.html", SITE / "404.html")
    (SITE / "404").rmdir()
    return out


# ------------------------------------------------------------------- machine files

def machine_files():
    pages = [("", "The front page")] + [(h, t) for h, t in NAV]
    urls = "".join(f"<url><loc>{SITE_URL}/{h}</loc><lastmod>{TODAY}</lastmod></url>" for h, _ in pages)
    write(SITE / "sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>'
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + urls + "</urlset>")
    write(SITE / "robots.txt", f"User-agent: *\nAllow: /\nSitemap: {SITE_URL}/sitemap.xml\n")
    P = F["primes"]["table"]
    write(SITE / "llms.txt", f"""# {NAME}

> {TAG}

{SITE_URL}/

As of {AS_OF}. Nothing here is advice about money.

## Facts this site computes
- pi(10^7) = {P[-1]['pi']}; li(x) misses by {P[-1]['err_li']:.1f}, x/ln x by {P[-1]['err_ln']:.0f}
- the first {F['zeros']['count']} zeros of zeta on the critical line, first ten to 1e-9 of Odlyzko's
- the explicit formula with 100 zeros reproduces psi(x) on [2,100] to rms {F['explicit']['rms_100']:.2f}
- NFS cost curve L[1/3] anchored on RSA-250 (2,700 core-years): 1024 bits about {F['cost']['rows'][3]['relative_to_rsa250']:.0f}x, 2048 bits about {F['cost']['rows'][5]['relative_to_rsa250']:.1e}x
- Kraitchik on 1649: 41^2 = 32, 43^2 = 200 mod N, gcd gives 17
- Shor on 15 with a = 7: period 4, factors 3 and 5
- y^2 = x^3 + 7 mod 97 has {F['curve']['points']} points, G of order {F['curve']['G_order']}
- {F['checks']['total']} checks, {F['checks']['failures']} failing

## Facts this site carries, with sources
- largest number split by Shor on hardware: 21 (2012), compiled
- largest curve key broken on hardware: 15 bits (April 2026), reproduced with random bits
- general-purpose factoring record: RSA-896, 896 bits, 19 September 2026; RSA-260 on 3 September 2026
- qubit estimates for RSA-2048: 1e9 (2012), 2e7 (2019), <1e6 (2025), <1e5 (2026, qLDPC)
- qubit estimate for a 256-bit curve key: <500,000 physical, minutes (Google, March 2026)
- biggest machines: about 100-1,100 physical qubits; 48 logical (Helios, 2025)
- bitcoin in exposed-key outputs: about 30% of supply (Glassnode May 2026, Chaincode May 2025)
- NIST: RSA-2048/P-256 deprecated after 2030, disallowed after 2035 (draft IR 8547)
- Riemann Hypothesis: open; proving it gives no factoring algorithm

## Pages
""" + "".join(f"- {SITE_URL}/{h} — {t}\n" for h, t in NAV) + f"""
## Data
- {SITE_URL}/data/facts.json — every computed number
- {SITE_URL}/data/zeros.json — the hundred zeros
- {SITE_URL}/data/developments.json — the ledger
- {SITE_URL}/data/wallet.json — outputs, exposure counts, proposals, timelines

## Terms
Text and figures: {CREDIT}, CC BY 4.0. Code: MIT.
""")
    write(SITE / "humans.txt", f"""/* the site */
Name: {NAME}
Built: {TODAY}; ledger to {AS_OF}
Source: https://github.com/NaNoBotCo/{SELF}
Terms: text and figures CC BY 4.0 ({CREDIT}); code MIT

/* the tools */
python3, numpy, Pillow. Static HTML with the stylesheet inlined; the scripts in js/ read
the same JSON the figures were drawn from. The pictures are computed, none photographed.
""")
    write(SITE / "icon.svg",
          '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">'
          '<rect width="32" height="32" rx="6" fill="#0a0a10"/>'
          '<rect x="5" y="9" width="10" height="14" rx="2" fill="#5fd3c6"/>'
          '<rect x="17" y="9" width="10" height="14" rx="2" fill="#ffb347"/>'
          '<rect x="15" y="6" width="2" height="20" fill="#0a0a10"/></svg>')
    (SITE / "data").mkdir(exist_ok=True)
    for k in ("timeline", "records", "claims", "estimates", "machines", "developments", "wallet", "glossary"):
        shutil.copy(DATA / f"{k}.json", SITE / "data" / f"{k}.json")
    shutil.copy(BUILD / "facts.json", SITE / "data" / "facts.json")


def main():
    if SITE.exists():
        shutil.rmtree(SITE)
    SITE.mkdir(parents=True)
    shutil.copytree(IMG, SITE / "img")
    shutil.copytree(BUILD / "data", SITE / "data")
    shutil.copytree(ROOT / "js", SITE / "js")
    home()
    split()
    history()
    methods()
    records()
    quantum()
    riemann()
    wallet()
    now()
    words_page()
    not_found()
    sources_page()
    machine_files()
    fleet.decorate(SITE, SELF, roster=FLEET)
    (SITE / ".basepath").write_text(BASE, encoding="utf-8")
    (SITE / ".nojekyll").write_text("", encoding="utf-8")
    unused = [s for s in SOURCES if s not in USED]
    print(f"build/site ← {len(list(SITE.rglob('index.html')))} pages; {len(USED)} of {len(SOURCES)} sources cited"
          + (f"; uncited: {', '.join(unused)}" if unused else ""))


if __name__ == "__main__":
    main()
