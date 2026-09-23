#!/usr/bin/env python3
"""What the built site says, checked against what compute.py computed and the data carries."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import sources  # noqa: E402

fails = []


def check(name, ok):
    print(f"  {'ok ' if ok else 'BAD'} {name}")
    if not ok:
        fails.append(name)


facts = json.loads((ROOT / "build" / "facts.json").read_text())
check("facts: zero failing checks", facts["checks"]["failures"] == 0)
check("facts: pi(10^7) = 664579", facts["primes"]["table"][6]["pi"] == 664579)
check("facts: first zero 14.134725", abs(facts["zeros"]["first"][0] - 14.134725141734693) < 1e-9)
check("facts: 100 zeros", facts["zeros"]["count"] == 100)
check("facts: Shor 15 → 3, 5", sorted(facts["examples"]["shor15"]["factors"]) == [3, 5])
check("facts: Kraitchik 1649 → 17", facts["examples"]["kraitchik"]["gcd"] == 17)
check("facts: cost ratio 768→1024 is a few hundred to a few thousand", 100 < facts["cost"]["ratio_768_1024"] < 10000)
check("facts: toy curve has a point count", facts["curve"]["points"] > 50)

# every source id in the data exists
ids = set(sources.SOURCES)
missing = []
for f in ("timeline", "records", "claims", "estimates", "machines", "developments", "wallet"):
    d = json.loads((ROOT / "data" / f"{f}.json").read_text())

    def walk(o):
        if isinstance(o, dict):
            for k, v in o.items():
                if k == "src":
                    for s in ([v] if isinstance(v, str) else v):
                        if s not in ids:
                            missing.append((f, s))
                else:
                    walk(v)
        elif isinstance(o, list):
            for x in o:
                walk(x)
    walk(d)
check("data: every source id exists", not missing)
dev = json.loads((ROOT / "data" / "developments.json").read_text())
check("ledger: rows are dated and ordered", all(a["date"] <= b["date"] for a, b in zip(dev["rows"], dev["rows"][1:])))
check("ledger: every row says what it does not mean", all(r["not"] for r in dev["rows"]))

site = ROOT / "build" / "site"
pages = ["index.html", "split/index.html", "history/index.html", "methods/index.html", "records/index.html",
         "quantum/index.html", "riemann/index.html", "wallet/index.html", "now/index.html", "words/index.html",
         "sources/index.html", "404.html"]
for p in pages:
    check(f"page {p}", (site / p).exists())
for m in ("robots.txt", "sitemap.xml", "llms.txt", "humans.txt", "icon.svg", "fleet.json",
          "data/facts.json", "data/zeros.json", "data/curve.json", "data/developments.json", "data/wallet.json",
          "img/hero.jpg", "img/card.jpg", "img/records.svg", "img/qubits.svg", "img/explicit.svg", "img/exposure.svg"):
    check(f"file {m}", (site / m).exists())
for j in ("split.js", "race.js", "sieve.js", "kraitchik.js", "period.js", "zeros.js", "curve.js", "cost.js", "now.js", "nav.js"):
    check(f"script {j}", (site / "js" / j).exists())

home = (site / "index.html").read_text(encoding="utf-8")
for must in ("CC BY 4.0", "hongdam", "img/card.jpg", "Shor", "wallet", "21", "15 bits", "advice about money"):
    check(f"front page names {must}", must in home)
wallet = (site / "wallet" / "index.html").read_text(encoding="utf-8")
for must in ("P2PK", "Taproot", "BIP 360", "BIP 361", "ten-minute", "secp256k1", "Glassnode"):
    check(f"wallet page names {must}", must in wallet)
riemann = (site / "riemann" / "index.html").read_text(encoding="utf-8")
check("riemann page says a proof gives no algorithm", "give anyone a factoring algorithm" in riemann)
check("riemann page prints the first zero", "14.134725" in riemann)
quantum = (site / "quantum" / "index.html").read_text(encoding="utf-8")
check("quantum page carries the claims table", "cargo cult" in quantum.lower() or "Cargo cult" in quantum)
records = (site / "records" / "index.html").read_text(encoding="utf-8")
check("records page has RSA-896", "RSA-896" in records)
for p in pages:
    t = (site / p).read_text(encoding="utf-8")
    if "/Users/" in t:
        check(f"no host path in {p}", False)
    if "' + fig(" in t or "' + cite(" in t:
        check(f"no leaked concatenation in {p}", False)
for w in ("hillbilly", "hillbillies"):
    check(f"the word '{w}' is nowhere in the site", not any(w in (site / p).read_text(encoding="utf-8").lower() for p in pages))

if fails:
    print(f"FAILED: {fails}")
    sys.exit(1)
print("tests pass")
