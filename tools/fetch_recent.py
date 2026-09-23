#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""fetch_recent.py — this week's papers and news, into data/recent.json.

No keys. arXiv's public API for the papers; public RSS feeds for the news. A source that
does not answer is recorded under "errors" and the rest are kept, so one dead feed does
not empty the page. Titles as published, unread by a person; the hand-kept ledger is
data/developments.json.

    python3 tools/fetch_recent.py
"""
from __future__ import annotations

import json
import re
import sys
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from html import unescape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "recent.json"
UA = "factoring-site/1.0 (+https://github.com/NaNoBotCo/factoring)"

ARXIV = ("http://export.arxiv.org/api/query?search_query="
         + urllib.parse.quote('(cat:cs.CR OR cat:quant-ph OR cat:math.NT) AND (ti:factoring OR ti:factorization OR ti:"number field sieve" OR ti:"Shor" OR ti:"RSA-2048" OR ti:"discrete logarithm" OR ti:"Riemann hypothesis" OR ti:"post-quantum")')
         + "&sortBy=submittedDate&sortOrder=descending&max_results=30")

NEWS = [
    ("Google News — RSA-2048", "https://news.google.com/rss/search?q=%22RSA-2048%22+OR+%22factoring+record%22&hl=en-US&gl=US&ceid=US:en"),
    ("Google News — quantum and bitcoin", "https://news.google.com/rss/search?q=quantum+bitcoin+%28BIP-360+OR+%22post-quantum%22+OR+%22quantum+resistant%22%29&hl=en-US&gl=US&ceid=US:en"),
    ("Quanta Magazine", "https://api.quantamagazine.org/feed/"),
    ("Bitcoin Optech", "https://bitcoinops.org/feed.xml"),
]
KEEP = re.compile(r"factor|prime|RSA|quantum|Riemann|zeta|post-quantum|BIP-?36|Shor", re.I)


def get(url, timeout=40):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def strip_tags(s):
    return unescape(re.sub(r"<[^>]+>", "", s or "")).strip()


def arxiv(errors):
    try:
        root = ET.fromstring(get(ARXIV))
    except Exception as e:  # noqa: BLE001
        errors.append(f"arXiv: {e}")
        return []
    ns = {"a": "http://www.w3.org/2005/Atom"}
    out = []
    for en in root.findall("a:entry", ns):
        title = re.sub(r"\s+", " ", (en.findtext("a:title", "", ns) or "")).strip()
        link = en.findtext("a:id", "", ns)
        date = (en.findtext("a:published", "", ns) or "")[:10]
        authors = [a.findtext("a:name", "", ns) for a in en.findall("a:author", ns)]
        if len(authors) > 3:
            authors = authors[:3] + ["and others"]
        out.append({"title": title, "url": link, "date": date, "authors": ", ".join(authors)})
    return out


def rss(name, url, errors):
    try:
        root = ET.fromstring(get(url))
    except Exception as e:  # noqa: BLE001
        errors.append(f"{name}: {e}")
        return []
    out = []
    atom = "{http://www.w3.org/2005/Atom}"
    items = list(root.iter("item")) or list(root.iter(atom + "entry"))
    for it in items:
        title = strip_tags(it.findtext("title", "") or it.findtext(atom + "title", ""))
        link = (it.findtext("link", "") or "").strip()
        if not link:
            l = it.find(atom + "link")
            link = l.get("href", "") if l is not None else ""
        pub = it.findtext("pubDate", "") or it.findtext(atom + "updated", "") or ""
        desc = strip_tags(it.findtext("description", "") or it.findtext(atom + "summary", ""))
        if not KEEP.search(title + " " + desc[:300]):
            continue
        try:
            dt = datetime.strptime(pub[:25].strip(), "%a, %d %b %Y %H:%M:%S").strftime("%Y-%m-%d")
        except Exception:  # noqa: BLE001
            dt = pub[:10]
        src = name
        if name.startswith("Google News"):
            s = it.find("source")
            if s is not None and s.text:
                src = s.text
        out.append({"title": title, "url": link, "date": dt, "source": src})
    return out


def main():
    errors: list[str] = []
    papers = arxiv(errors)
    news = []
    for name, url in NEWS:
        news += rss(name, url, errors)
    seen = set()
    dedup = []
    for n in sorted(news, key=lambda n: n["date"], reverse=True):
        k = n["title"].lower()[:80]
        if k in seen:
            continue
        seen.add(k)
        dedup.append(n)
    data = {"fetched": datetime.now(timezone.utc).isoformat(timespec="seconds"), "arxiv": papers, "news": dedup[:60], "errors": errors,
            "_about": "Written by tools/fetch_recent.py. Titles as published, unread by a person. The hand-kept ledger is developments.json."}
    OUT.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{len(papers)} papers, {len(dedup)} news items, {len(errors)} sources failed" + (": " + "; ".join(errors) if errors else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
