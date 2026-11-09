#!/usr/bin/env python3
"""Nightly article improvement helper for earningmoneyonline.co.uk. Standard library only.

  python3 -I tools/improve.py queue            build or refresh data/improve-queue.json (keeps done marks)
  python3 -I tools/improve.py next 10          print the next 10 slugs to improve
  python3 -I tools/improve.py check a.html ... compare each page with origin/main and fail on any broken rule
  python3 -I tools/improve.py done a.html ...  mark done today and set the sitemap lastmod to today
  python3 -I tools/improve.py status           how many done, how many left

The rules the checks enforce are in docs/IMPROVE-RULES.md.
"""
import html
import json
import os
import re
import subprocess
import sys
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
QUEUE = os.path.join(ROOT, "data", "improve-queue.json")
MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August",
          "September", "October", "November", "December"]
TODAY = date.today()


def read(rel):
    with open(os.path.join(ROOT, rel), encoding="utf-8", errors="replace") as f:
        return f.read()


def grab(p, s):
    m = re.search(p, s, re.S | re.I)
    return m.group(1) if m else ""


def text(s):
    return html.unescape(re.sub(r"<[^>]+>", " ", s or "")).strip()


def body_of(s):
    m = re.search(r"<!--emo:body-->(.*?)<!--/emo:body-->", s, re.S)
    if m:
        return m.group(1)
    m = re.search(r'<div class="article-body">(.*)<footer', s, re.S)
    return m.group(1) if m else ""


def dates_in(t):
    """Every 'd Month yyyy' or 'Month yyyy' date in a string, as date objects."""
    out = []
    for d, mo, y in re.findall(r"(?:(\d{1,2})[ -])?(January|February|March|April|May|June|July|August|September|October|November|December)[ -](\d{4})", t, re.I):
        mi = [m.lower() for m in MONTHS].index(mo.lower()) + 1
        try:
            out.append(date(int(y), mi, int(d) if d else 28))
        except ValueError:  # "300 September 2026" style numbers that are not a day
            out.append(date(int(y), mi, 28))
    return out


# ---------------------------------------------------------------- queue
def build_queue():
    old = {}
    if os.path.exists(QUEUE):
        old = {q["slug"]: q for q in json.load(open(QUEUE, encoding="utf-8"))["items"]}
    items = []
    for f in sorted(os.listdir(os.path.join(ROOT, "articles"))):
        if not f.endswith(".html"):
            continue
        s = read("articles/" + f)
        title = text(grab(r"<h1[^>]*>(.*?)</h1>", s))
        slug_words = f.replace("-", " ").replace(".html", "")
        passed = [d for d in dates_in(title + " " + slug_words) if d < TODAY]
        checked = grab(r"(?:Figures|Rules|Rates|Prices|Facts) checked ([A-Z][a-z]+ \d{4})", s)
        cd = dates_in(checked)
        pub = dates_in(grab(r"(?:Published|Updated) (\d{1,2} [A-Z][a-z]+ \d{4})", s))
        # lower score goes first
        score = (0 if passed else 1,
                 cd[0].isoformat() if cd else "0000",
                 pub[0].isoformat() if pub else "0000")
        q = old.get(f, {"slug": f, "status": "todo", "done": ""})
        q.update({"title": title, "reason": "date passed" if passed else ("checked " + checked if checked else "no check date"),
                  "_score": list(score)})
        items.append(q)
    items.sort(key=lambda q: q["_score"])
    for i, q in enumerate(items, 1):
        q["order"] = i
        q.pop("_score", None)
    os.makedirs(os.path.dirname(QUEUE), exist_ok=True)
    with open(QUEUE, "w", encoding="utf-8") as f:
        json.dump({"updated": TODAY.isoformat(), "per_night": 10, "items": items}, f, ensure_ascii=False, indent=1)
    print("queue: %d articles, %d done, first: %s" % (len(items), sum(q["status"] == "done" for q in items), items[0]["slug"]))


def load():
    return json.load(open(QUEUE, encoding="utf-8"))


def nxt(n):
    for q in [q for q in load()["items"] if q["status"] != "done"][:n]:
        print(q["slug"])


def status():
    items = load()["items"]
    d = sum(q["status"] == "done" for q in items)
    print("done %d of %d, left %d, nights left at 10 a night: %d" % (d, len(items), len(items) - d, -(-(len(items) - d) // 10)))


def done(slugs):
    data = load()
    for q in data["items"]:
        if q["slug"] in slugs:
            q["status"], q["done"] = "done", TODAY.isoformat()
    with open(QUEUE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
    sm = read("sitemap.xml")
    for s in slugs:
        url = re.escape("https://earningmoneyonline.co.uk/articles/" + s)
        sm, k = re.subn(r"(<loc>%s</loc>)<lastmod>[^<]*</lastmod>" % url, r"\g<1><lastmod>%s</lastmod>" % TODAY.isoformat(), sm)
        if not k:
            sm = re.sub(r"(<loc>%s</loc>)" % url, r"\g<1><lastmod>%s</lastmod>" % TODAY.isoformat(), sm)
    with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(sm)
    print("marked done and lastmod set:", len(slugs))


# ---------------------------------------------------------------- checks
def before(rel):
    r = subprocess.run(["git", "show", "origin/main:" + rel], cwd=ROOT, capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else ""


def check(slugs):
    bad = 0
    for slug in slugs:
        rel = "articles/" + slug
        problems = []
        if not os.path.exists(os.path.join(ROOT, rel)):
            print("FAIL %s: file missing" % slug)
            bad += 1
            continue
        new, old = read(rel), before(rel)
        title = html.unescape(grab(r"<title>(.*?)</title>", new))
        desc = html.unescape(grab(r'<meta name="description" content="([^"]*)"', new))
        canon = grab(r'<link rel="canonical" href="([^"]*)"', new)
        if canon != "https://earningmoneyonline.co.uk/articles/" + slug:
            problems.append("canonical changed or missing: " + canon)
        if not 30 <= len(title) <= 65:
            problems.append("title length %d, want 30 to 65" % len(title))
        if not 120 <= len(desc) <= 165:
            problems.append("description length %d, want 120 to 165" % len(desc))
        for tag in ("og:title", "og:description", "twitter:title", "twitter:description"):
            if not re.search(r'(property|name)="%s" content="[^"]+"' % tag, new):
                problems.append(tag + " missing")
        if "<!--emo:body-->" not in new or "<!--emo:h1-->" not in new:
            problems.append("design markers missing, run the generator with --live")
        b_new, b_old = body_of(new), body_of(old)
        w_new, w_old = len(text(b_new).split()), len(text(b_old).split())
        if old and w_new < 0.85 * w_old:
            problems.append("body shrank from %d to %d words" % (w_old, w_new))
        src_new = len(re.findall(r'href="https?://(?!earningmoneyonline)', b_new))
        src_old = len(re.findall(r'href="https?://(?!earningmoneyonline)', b_old))
        if old and src_new < src_old:
            problems.append("outside source links dropped from %d to %d" % (src_old, src_new))
        amz = r'href="https?://(?:www\.)?amazon\.co\.uk[^"]*"'
        if old and len(re.findall(amz, b_new)) < len(re.findall(amz, b_old)):
            problems.append("Amazon affiliate links dropped")
        if re.search(r'href="https?://(?:www\.)?amazon\.co\.uk[^"]*"', b_new) and any("tag=earningmon051-21" not in h for h in re.findall(amz, b_new)):
            problems.append("an Amazon link without the account tag earningmon051-21")
        dash_new = text(b_new).count("—") + text(b_new).count("–")
        dash_old = text(b_old).count("—") + text(b_old).count("–")
        if dash_new > dash_old:
            problems.append("new dashes added in the text")
        if not re.search(r"<h2[^>]*>\s*(Frequently asked|FAQ|Questions)", b_new, re.I):
            problems.append("no Frequently asked section")
        if not re.search(r"(?:Figures|Rules|Rates|Prices|Facts) checked (%s) %d" % ("|".join(MONTHS), TODAY.year), new):
            problems.append("no 'Figures checked <Month> %d' line" % TODAY.year)
        internal = set(re.findall(r'href="(/articles/[^"#]+|[a-z0-9-]+\.html)"', b_new))
        for h in internal:
            p = h if h.startswith("/") else "/articles/" + h
            if not os.path.exists(os.path.join(ROOT, p.lstrip("/"))):
                problems.append("broken internal link " + h)
        if len([h for h in internal if h.rstrip("/") != "/articles/" + slug]) < 3:
            problems.append("fewer than 3 internal links to other guides")
        if problems:
            bad += 1
            print("FAIL %s" % slug)
            for p in problems:
                print("   - " + p)
        else:
            print("ok   %s  (%d words, title %d, description %d)" % (slug, w_new, len(title), len(desc)))
    if bad:
        print("%d of %d pages failed. Do not merge." % (bad, len(slugs)))
        sys.exit(1)
    print("all %d pages passed" % len(slugs))


if __name__ == "__main__":
    cmd, args = (sys.argv[1] if len(sys.argv) > 1 else "status"), sys.argv[2:]
    if cmd == "queue":
        build_queue()
    elif cmd == "next":
        nxt(int(args[0]) if args else 10)
    elif cmd == "check":
        check(args)
    elif cmd == "done":
        done(args)
    else:
        status()
