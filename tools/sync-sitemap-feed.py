#!/usr/bin/env python3
"""Keep sitemap.xml and feed.xml in step with the article files. Standard library only.

  python3 -I tools/sync-sitemap-feed.py           add missing articles to sitemap.xml, move lastmod forward
                                                  where an article was updated, rebuild feed.xml (newest 30)
  python3 -I tools/sync-sitemap-feed.py --check   change nothing, exit 1 if an article is missing from
                                                  sitemap.xml or the newest article is not in feed.xml

Safe to rerun. Existing sitemap lines are kept as they are, a lastmod only ever moves forward.
Dates come from the article's own "Published d Month yyyy" and "Updated d Month yyyy" text.
"""
import html
import os
import re
import sys
from datetime import date, datetime, timezone
from email.utils import format_datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://earningmoneyonline.co.uk"
MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August",
          "September", "October", "November", "December"]
FEED_ITEMS = 30
CAT_SLUG = {"Save Money": "save-money", "Make Money": "make-money", "Side Hustles": "side-hustles",
            "Work & Career": "work-career", "Tools & Reviews": "tools-reviews", "UK Update": "uk-update",
            "Affiliate Marketing": "affiliate-marketing", "AI Tools": "ai-tools"}


def read(rel):
    with open(os.path.join(ROOT, rel), encoding="utf-8", errors="replace") as f:
        return f.read()


def write(rel, s):
    with open(os.path.join(ROOT, rel), "w", encoding="utf-8") as f:
        f.write(s)


def text(s):
    return html.unescape(re.sub(r"<[^>]+>", "", s or "")).strip()


def when_text(s):
    m = re.search(r"<!--emo:when-->(.*?)<!--/emo:when-->", s, re.S)
    if m:
        return m.group(1)
    m = re.search(r'<div class="who">.*?<span>(.*?)</span>', s, re.S)
    return m.group(1) if m else s


def dates(s, word):
    out = []
    for d, mon, y in re.findall(word + r" ?(\d{1,2}) (\w+) (\d{4})", s):
        if mon in MONTHS:
            out.append(date(int(y), MONTHS.index(mon) + 1, int(d)))
    return out


def articles():
    out = []
    for f in sorted(os.listdir(os.path.join(ROOT, "articles"))):
        if not f.endswith(".html"):
            continue
        s = read("articles/" + f)
        w = when_text(s)
        bare = dates(" " + text(w).strip()[:20], "^ ?")  # "21 July 2026 · 6 min read" with no word in front
        pub = (dates(w, "Published") or dates(w, "Updated") or bare or [None])[0]
        upd = max([pub] + dates(w, "Updated")) if pub else None
        tag = re.search(r"<!--emo:tag-->(.*?)<!--/emo:tag-->", s, re.S) or re.search(r'<span class="tag">(.*?)</span>', s)
        h1 = re.search(r"<!--emo:h1-->(.*?)<!--/emo:h1-->", s, re.S) or re.search(r"<h1[^>]*>(.*?)</h1>", s, re.S)
        title = re.search(r"<title>(.*?)</title>", s, re.S)
        desc = re.search(r'<meta name="description" content="([^"]*)"', s)
        rt = re.search(r"(\d+) min read", w)
        out.append({"f": f, "pub": pub, "upd": upd or pub, "tag": text(tag.group(1)) if tag else "",
                    "title": text(h1.group(1)) if h1 else text(title.group(1) if title else f),
                    "desc": text(desc.group(1)) if desc else "", "rt": rt.group(1) if rt else ""})
    return out


def sync_sitemap(arts, check):
    s = read("sitemap.xml")
    have = dict(re.findall(r"<loc>([^<]+)</loc><lastmod>([^<]+)</lastmod>", s))
    missing, bumped = [], 0
    for a in arts:
        loc = "%s/articles/%s" % (SITE, a["f"])
        lm = a["upd"].isoformat() if a["upd"] else date.today().isoformat()
        if loc not in have:
            missing.append((loc, lm))
        elif have[loc] < lm:
            s = s.replace("<loc>%s</loc><lastmod>%s</lastmod>" % (loc, have[loc]),
                          "<loc>%s</loc><lastmod>%s</lastmod>" % (loc, lm))
            bumped += 1
    if check:
        for loc, _ in missing:
            print("missing from sitemap.xml:", loc)
        return not missing
    # homepage and category pages: lastmod is the newest article date they show
    newest = max(a["upd"] for a in arts if a["upd"]).isoformat()
    pages = {SITE + "/": newest}
    for tag, slug in CAT_SLUG.items():
        ds = [a["upd"] for a in arts if a["tag"] == tag and a["upd"]]
        if ds:
            pages["%s/categories/%s.html" % (SITE, slug)] = max(ds).isoformat()
    for loc, lm in pages.items():
        old = have.get(loc)
        if old and old < lm:
            s = s.replace("<loc>%s</loc><lastmod>%s</lastmod>" % (loc, old), "<loc>%s</loc><lastmod>%s</lastmod>" % (loc, lm))
    add = "".join('  <url><loc>%s</loc><lastmod>%s</lastmod><priority>0.9</priority></url>\n' % m for m in missing)
    s = s.replace("</urlset>", add + "</urlset>")
    write("sitemap.xml", s)
    print("sitemap.xml: %d added, %d lastmod moved forward" % (len(missing), bumped))
    return True


def rss_date(d):
    return format_datetime(datetime(d.year, d.month, d.day, 7, 0, tzinfo=timezone.utc))


def sync_feed(arts, check):
    dated = sorted([a for a in arts if a["pub"]], key=lambda a: (a["pub"], a["f"]), reverse=True)[:FEED_ITEMS]
    if check:
        ok = dated and ("/articles/%s<" % dated[0]["f"]) in read("feed.xml")
        if not ok:
            print("feed.xml does not have the newest article:", dated[0]["f"] if dated else "none")
        return bool(ok)
    e = html.escape
    items = []
    for a in dated:
        url = "%s/articles/%s" % (SITE, a["f"])
        items.append("  <item>\n    <title>%s</title>\n    <link>%s</link>\n    <guid isPermaLink=\"true\">%s</guid>\n"
                     "    <pubDate>%s</pubDate>\n    <category>%s</category>\n    <description>%s</description>\n  </item>\n"
                     % (e(a["title"]), url, url, rss_date(a["pub"]), e(a["tag"]), e(a["desc"])))
    s = read("feed.xml")
    head = s[:s.index("<lastBuildDate>")]
    out = (head + "<lastBuildDate>%s</lastBuildDate>\n  <ttl>1440</ttl>\n" % format_datetime(datetime.now(timezone.utc), usegmt=True)
           + "".join(items) + "</channel>\n</rss>\n")
    write("feed.xml", out)
    print("feed.xml: %d newest articles, newest %s (%s)" % (len(items), dated[0]["f"], dated[0]["pub"]))
    return True


def main():
    check = "--check" in sys.argv
    arts = articles()
    nodate = [a["f"] for a in arts if not a["pub"]]
    if nodate:
        print("no Published date found in:", ", ".join(nodate[:10]))
    ok = sync_sitemap(arts, check) & sync_feed(arts, check)
    if check:
        print("sitemap and feed in step" if ok else "sitemap or feed out of step, run tools/sync-sitemap-feed.py")
        sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
