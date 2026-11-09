#!/usr/bin/env python3
"""Build earningmoneyonline.co.uk in the Liquid Glass design.

Two modes, standard library only, run from the repo root:

  python3 -I tools/build-preview.py           preview: writes /preview/ only (noindex, A or B colour switch)
  python3 -I tools/build-preview.py --live    live: rewrites the real pages (homepage, 8 categories,
                                              every article, about, contact, privacy, terms, disclosure)

The page text is never edited. Only the shell around it changes. Each page keeps its own title,
description, canonical and social tags. Running it again is safe: a page already in the new
design is read back through the <!--emo:...--> markers, and an old template page is read the old way,
so a new article written in the old template is converted on the next run.

The design lives in preview/assets/glass.css and glass.js. Live mode copies them to /assets/.
"""
import hashlib
import html
import json
import os
import posixpath
import re
import shutil
import sys
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LIVE = "--live" in sys.argv
BASE = "/" if LIVE else "/preview/"
OUT = ROOT if LIVE else os.path.join(ROOT, "preview")
SRC_ASSETS = os.path.join(ROOT, "preview", "assets")
CSS_NAME, JS_NAME = ("emo.css", "emo.js") if LIVE else ("glass.css", "glass.js")

# preview only: articles rebuilt in the new design, every other link goes to the live page
PREVIEW_ARTICLES = [
    "energy-price-cap-october-2026.html",
    "marriage-allowance-252-a-year-who-can-claim-uk.html",
    "warm-home-discount-150-who-gets-it-automatically-uk.html",
    "side-hustle-tax-rules-uk.html",
    "skilled-worker-visa-modern-slavery-rule-uk.html",
]
STATIC_PAGES = ["about.html", "contact.html", "privacy-policy.html", "affiliate-disclosure.html",
                "privacy/index.html", "terms/index.html"]

CATS = [  # (tag on the article, slug, short name, icon, page title, one line)
    ("Save Money", "save-money", "Save Money", "wallet", "Save Money",
     "Cut bills, use cashback and spend smarter every month."),
    ("Make Money", "make-money", "Make Money", "trend", "Make Money Online",
     "Etsy, print on demand, YouTube, freelancing and every real way to earn online from the UK."),
    ("Side Hustles", "side-hustles", "Side Hustles", "case", "Side Hustles",
     "Turn a hobby you already love into a real income, with UK rules and real numbers."),
    ("Work & Career", "work-career", "Work & Career", "badge", "Work and Career",
     "Remote jobs, better pay and skills that earn more."),
    ("Tools & Reviews", "tools-reviews", "Tools & Reviews", "wrench", "Tools and Reviews",
     "Honest reviews of the tools that help you earn."),
    ("UK Update", "uk-update", "UK Update", "bank", "UK Immigration Update",
     "Rule changes, deadlines and official figures that affect your money and your right to work in the UK."),
    ("Affiliate Marketing", "affiliate-marketing", "Affiliate", "link", "Affiliate Marketing",
     "Amazon Associates and the networks explained without the hype, with the honest arithmetic of what it earns."),
    ("AI Tools", "ai-tools", "AI Tools", "spark", "AI Tools",
     "How people really earn with AI in the UK, what it costs to try, and when it does not pay."),
]
TAG2SLUG = {c[0]: c[1] for c in CATS}

ICONS = {
    "wallet": '<path d="M3 7h15a3 3 0 0 1 3 3v7a3 3 0 0 1-3 3H6a3 3 0 0 1-3-3V7z"/><path d="M3 7l12-3v3"/><circle cx="16.5" cy="13.5" r="1.2"/>',
    "trend": '<path d="M3 17l6-6 4 4 8-8"/><path d="M15 7h6v6"/>',
    "case": '<rect x="3" y="7" width="18" height="13" rx="2.5"/><path d="M9 7V5a2 2 0 0 1 2-2h2a2 2 0 0 1 2 2v2M3 13h18"/>',
    "badge": '<circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0 1 16 0"/>',
    "wrench": '<path d="M14.7 6.3a4 4 0 0 0 5 5L21 13l-8 8-2-2 1.3-1.3a4 4 0 0 0-5-5L3 9l3-3 2.3 2.3"/><path d="M9 15l-2 2"/>',
    "bank": '<path d="M3 10l9-6 9 6"/><path d="M5 10v8M9.5 10v8M14.5 10v8M19 10v8M3 21h18"/>',
    "link": '<path d="M10 14a4 4 0 0 0 5.7 0l3-3a4 4 0 0 0-5.7-5.7l-1 1"/><path d="M14 10a4 4 0 0 0-5.7 0l-3 3a4 4 0 0 0 5.7 5.7l1-1"/>',
    "spark": '<path d="M12 3l1.8 5.2L19 10l-5.2 1.8L12 17l-1.8-5.2L5 10l5.2-1.8z"/><path d="M19 16l.8 2.2L22 19l-2.2.8L19 22l-.8-2.2L16 19l2.2-.8z"/>',
}

MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August",
          "September", "October", "November", "December"]
GSAP = ('<script src="https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/gsap.min.js" '
        'integrity="sha384-g4NTh/Iv5PPU4xPyhEWqPcwtNXOvdaDI8LLnyYfyNZOjKJeYQyjzQ9X5275eBjpt" '
        'crossorigin="anonymous" defer></script>')
FONT = ('<link rel="preconnect" href="https://fonts.googleapis.com">\n'
        '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
        '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Literata:ital,opsz,wght@'
        '0,7..72,400;0,7..72,700;1,7..72,400&display=swap">\n')
TRADING = ("EarningMoneyOnline is a trading name of JAGAT IT UK LTD, registered in England and Wales, "
           "company number 17474995. Registered office: 164 High Street, London Colney, St Albans, "
           "Hertfordshire, England, AL2 1QF.")

E = html.escape


# ---------------------------------------------------------------- helpers
def text(fragment):
    return html.unescape(re.sub(r"<[^>]+>", "", fragment or "")).strip()


def grab(pattern, s, flags=re.S | re.I):
    m = re.search(pattern, s, flags)
    return m.group(1) if m else ""


def mark(name, s):
    """Content between <!--emo:name--> and <!--/emo:name-->, or None when the page has no such marker."""
    m = re.search(r"<!--emo:%s-->(.*?)<!--/emo:%s-->" % (name, name), s, re.S)
    return m.group(1) if m else None


def wrap(name, content):
    return "<!--emo:%s-->%s<!--/emo:%s-->" % (name, content, name)


def read(rel):
    with open(os.path.join(ROOT, rel), encoding="utf-8", errors="replace") as f:
        return f.read()


def write(rel, content):
    path = os.path.join(OUT, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def asset_path(name):
    return os.path.join(OUT, "assets", name)


def ver(name):
    """Short content hash, so Cloudflare never serves an old copy after a change."""
    with open(asset_path(name), "rb") as f:
        return hashlib.sha1(f.read()).hexdigest()[:10]


def fmt_date(d):
    if not d:
        return ""
    y, m, dd = d.split("-")
    return "%d %s %s" % (int(dd), MONTHS[int(m) - 1][:3], y)


def art_href(slug):
    if LIVE or slug in PREVIEW_ARTICLES:
        return BASE + "articles/" + slug
    return "/articles/" + slug


DROP_HEAD = re.compile(
    r'^\s*(<meta charset|<meta name="viewport"|<meta name="robots"|<meta name="theme-color"|'
    r'<link rel="stylesheet"|<link rel="preconnect"|<link rel="icon"|<script)', re.I)


def head_meta(s):
    """The page's own SEO lines (title, description, canonical, og, twitter, verification)."""
    m = mark("meta", s)
    if m is not None:
        return m.strip("\n")
    inner = grab(r"<head>(.*?)</head>", s)
    keep = [l for l in inner.split("\n") if l.strip() and not DROP_HEAD.match(l)]
    return "\n".join(keep)


# ---------------------------------------------------------------- reading a page, old or new template
def parse_page(s):
    """Fields of an article style page. Works on the old template and on pages this script wrote."""
    if mark("body", s) is not None:
        return {"tag": text(mark("tag", s) or ""), "h1": mark("h1", s) or "", "standfirst": mark("sf", s) or "",
                "avatar": html.unescape(mark("av", s) or ""), "who": html.unescape(mark("who", s) or ""),
                "when": mark("when", s) or "", "body": mark("body", s), "meta": head_meta(s)}
    headsec = grab(r'<section class="article-head">(.*?)</section>', s)
    start = s.find('<div class="article-body">')
    end = s.rfind("<footer")
    inner = s[start + len('<div class="article-body">'):end]
    inner = inner[:inner.rfind("</div>")]
    when = grab(r'<div class="who">.*?<span>(.*?)</span>', headsec) or grab(r'<p class="meta">(.*?)</p>', headsec)
    return {"tag": text(grab(r'<span class="tag">(.*?)</span>', headsec)),
            "h1": grab(r"<h1[^>]*>(.*?)</h1>", headsec).strip(),
            "standfirst": grab(r'<p class="standfirst">(.*?)</p>', headsec),
            "avatar": html.unescape(grab(r'<div class="byline">\s*<img src="([^"]+)"', headsec)),
            "who": text(grab(r'<div class="who">\s*<b>(.*?)</b>', headsec)),
            "when": when.strip(), "body": inner, "meta": head_meta(s)}


# ---------------------------------------------------------------- index of all articles
def build_index():
    out = []
    for f in sorted(os.listdir(os.path.join(ROOT, "articles"))):
        if not f.endswith(".html"):
            continue
        s = read("articles/" + f)
        p = parse_page(s)
        title = text(p["h1"]) or text(grab(r"<title>(.*?)</title>", s))
        desc = text(grab(r'<meta name="description" content="([^"]*)"', s))
        img = grab(r'<img[^>]*class="cover"[^>]*src="([^"]+)"', s) or grab(r'<img class="cover" src="([^"]+)"', s) \
            or grab(r'property="og:image" content="([^"]+)"', s)
        img = re.sub(r"w=\d+", "w=640", html.unescape(img)) if img else ""
        m = re.search(r"(?:Published|Updated) (\d{1,2}) (\w+) (\d{4})", p["when"] or s)
        d = ""
        if m and m.group(2) in MONTHS:
            d = "%s-%02d-%02d" % (m.group(3), MONTHS.index(m.group(2)) + 1, int(m.group(1)))
        rt = grab(r"(\d+) min read", p["when"] or s)
        out.append({"u": f, "t": title, "c": p["tag"], "d": d, "i": img, "x": desc[:160],
                    "r": int(rt) if rt.isdigit() else None})
    out.sort(key=lambda a: a["d"] or "0000", reverse=True)
    return out


# ---------------------------------------------------------------- shell
LOGO = ('<svg width="30" height="30" viewBox="0 0 32 32" aria-hidden="true"><defs>'
        '<linearGradient id="lg" x1="0" y1="0" x2="1" y2="1"><stop class="lg1" offset="0"/>'
        '<stop offset="1" stop-color="#f0bd3a"/></linearGradient></defs>'
        '<circle cx="16" cy="16" r="14.5" fill="url(#lg)" stroke="rgba(255,255,255,.7)"/>'
        '<circle cx="16" cy="16" r="11" fill="none" stroke="rgba(5,7,13,.25)" stroke-dasharray="2 2.4"/>'
        '<text x="16" y="22" text-anchor="middle" font-family="system-ui,Arial" font-weight="800" '
        'font-size="17" fill="#05070d">&#163;</text></svg>')


def icon(name, size=22):
    return ('<svg width="%d" height="%d" viewBox="0 0 24 24" fill="none" stroke-width="1.8" '
            'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">%s</svg>' % (size, size, ICONS[name]))


SITE = "https://earningmoneyonline.co.uk"


def ld_json(meta, p=None, rel=""):
    """Structured data in the page itself (analytics.js skips its own copy when this exists)."""
    desc = html.unescape(grab(r'<meta name="description" content="([^"]*)"', meta))
    publisher = {"@type": "Organization", "name": "EarningMoneyOnline.co.uk", "url": SITE}
    canon = grab(r'<link rel="canonical" href="([^"]*)"', meta) or SITE + "/" + rel
    if p is None or not rel.startswith("articles/"):
        blocks = [{"@context": "https://schema.org", "@type": "WebSite", "name": "EarningMoneyOnline.co.uk",
                   "url": SITE, "description": desc, "publisher": publisher}]
    else:
        title = text(p["h1"])[:110]
        img = html.unescape(grab(r'<img[^>]*class="cover"[^>]*src="([^"]+)"', p["body"]) or grab(r'<img class="cover" src="([^"]+)"', p["body"]))
        art = {"@context": "https://schema.org", "@type": "Article", "headline": title, "description": desc,
               "image": [img or SITE + "/images/cover.jpg"], "author": {"@type": "Person", "name": "Ruhul Amin", "url": SITE},
               "publisher": publisher, "mainEntityOfPage": {"@type": "WebPage", "@id": canon}}
        if p["tag"]:
            art["articleSection"] = p["tag"]
        m = re.search(r"(\d{1,2})\s+([A-Za-z]+)\s+(\d{4})", text(p["when"]))
        if m and m.group(2) in MONTHS:
            iso = "%s-%02d-%02d" % (m.group(3), MONTHS.index(m.group(2)) + 1, int(m.group(1)))
            art["datePublished"] = iso
            art["dateModified"] = iso
        crumbs = [{"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"}]
        if p["tag"] in TAG2SLUG:
            crumbs.append({"@type": "ListItem", "position": 2, "name": p["tag"],
                           "item": SITE + "/categories/" + TAG2SLUG[p["tag"]] + ".html"})
        crumbs.append({"@type": "ListItem", "position": len(crumbs) + 1, "name": title, "item": canon})
        blocks = [art, {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": crumbs}]
    return "".join('<script type="application/ld+json">%s</script>\n' % json.dumps(b, ensure_ascii=False).replace("</", "<\\/")
                   for b in blocks)


def icons():
    """Favicon links for every browser, each with a content hash."""
    def h(name):
        with open(os.path.join(ROOT, name), "rb") as f:
            return hashlib.sha1(f.read()).hexdigest()[:10]
    return ('<link rel="icon" href="/favicon.ico?v=%s" sizes="any">\n'
            '<link rel="icon" href="/favicon.svg?v=%s" type="image/svg+xml">\n'
            '<link rel="icon" href="/favicon-32x32.png?v=%s" type="image/png" sizes="32x32">\n'
            '<link rel="apple-touch-icon" href="/apple-touch-icon.png?v=%s">\n'
            '<link rel="manifest" href="/site.webmanifest">\n'
            % (h("favicon.ico"), h("favicon.svg"), h("favicon-32x32.png"), h("apple-touch-icon.png")))


def head(meta, extra=""):
    if LIVE:
        theme = ' data-theme="indigo"'
        try:
            skim = json.load(open(os.path.join(ROOT, "data", "affiliate.json"), encoding="utf-8")).get("skimlinks_id", "")
        except (OSError, ValueError):
            skim = ""
        if re.match(r"^[0-9]+X[0-9]+$", skim or ""):
            theme += ' data-skim="%s"' % skim
        top = ""
        with open(os.path.join(ROOT, "js", "analytics.js"), "rb") as f:
            av = hashlib.sha1(f.read()).hexdigest()[:10]
        tail = '<script defer src="/js/analytics.js?v=%s"></script>\n<script>window.__EMO_PREVIEW={};</script>\n' % av
    else:
        theme = ""
        top = '<meta name="robots" content="noindex,nofollow">\n'
        tail = ('<script>window.__EMO_PREVIEW=%s;(function(){var t="indigo";try{t=localStorage.getItem("emoTheme")||t}'
                'catch(e){}if(t==="indigo")document.documentElement.setAttribute("data-theme","indigo")})();</script>\n'
                % json.dumps({s: 1 for s in PREVIEW_ARTICLES}))
    return """<!doctype html>
<html lang="en-GB" data-root="%s" data-sv="%s"%s>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
%s<meta name="theme-color" content="#0b1440">
%s
%s<link rel="stylesheet" href="%sassets/%s?v=%s">
%s%s
<script defer src="%sassets/%s?v=%s"></script>
%s</head>
<body>
<div class="sky" aria-hidden="true"><i class="b1"></i><i class="b2"></i><i class="b3"></i></div>
""" % (BASE, ver("search.json"), theme, top, wrap("meta", "\n" + meta + "\n"), icons(), BASE, CSS_NAME, ver(CSS_NAME),
       extra, GSAP, BASE, JS_NAME, ver(JS_NAME), tail)


def header(active=""):
    chips = "".join('<a class="chip" href="%scategories/%s.html"%s>%s</a>' % (
        BASE, slug, ' aria-current="page"' if slug == active else "", E(short))
        for _, slug, short, _, _, _ in CATS)
    return """<header class="top"><div class="w">
<a class="logo" href="%s" aria-label="EarningMoneyOnline home">%s<span>Earning<b>Money</b>Online</span></a>
<nav class="nav" aria-label="Categories">%s</nav>
</div></header>
""" % (BASE, LOGO, chips)


def footer():
    badge = "" if LIVE else (
        '<div class="pv" role="note"><b>Preview</b> &middot; <a href="/">live site</a> &middot; colour'
        '<button type="button" data-t="indigo" aria-pressed="false">A</button>'
        '<button type="button" data-t="green" aria-pressed="false">B</button></div>\n')
    return """<footer class="ft%s"><div class="w">
<nav aria-label="Site"><a href="/about.html">About</a><a href="/contact.html">Contact</a><a href="/privacy/">Privacy</a><a href="/terms/">Terms</a><a href="/affiliate-disclosure.html">Affiliate disclosure</a></nav>
<p>%s</p>
<p>General guidance, not financial advice. &copy; %d</p>
</div></footer>
%s</body>
</html>
""" % (" live" if LIVE else "", E(TRADING), date.today().year, badge)


def card(a):
    meta = " &middot; ".join(x for x in [E(fmt_date(a["d"])), ("%d min read" % a["r"]) if a["r"] else ""] if x)
    return ('<a class="card lit" href="%s"><div class="im"><img src="%s" alt="" loading="lazy" decoding="async" '
            'width="640" height="360"></div><div class="bd"><span class="tg">%s</span><h3>%s</h3>'
            '<span class="mt">%s</span></div></a>') % (art_href(a["u"]), E(a["i"]), E(a["c"]), E(a["t"]), meta)


# ---------------------------------------------------------------- homepage
def homepage(idx):
    counts = {c[1]: 0 for c in CATS}
    for a in idx:
        if a["c"] in TAG2SLUG:
            counts[TAG2SLUG[a["c"]]] += 1
    n = len(idx)
    tiles = "".join('<a class="tile lit" href="%scategories/%s.html"><span class="ic">%s</span><b>%s</b>'
                    '<span>%d guides</span></a>' % (BASE, slug, icon(ic), E(short), counts[slug])
                    for _, slug, short, ic, _, _ in CATS)
    latest = "".join(card(a) for a in idx[:6])
    stage = """<div class="stage">
<svg viewBox="0 0 420 260" role="img" aria-label="A coin above a rising savings line">
<defs>
<linearGradient id="emoLine" x1="0" x2="1"><stop class="s1" offset="0"/><stop class="s2" offset="1"/></linearGradient>
<linearGradient id="emoArea" x1="0" y1="0" x2="0" y2="1"><stop class="a1" offset="0"/><stop class="a2" offset="1"/></linearGradient>
<radialGradient id="emoCoin" cx=".35" cy=".3" r=".8"><stop offset="0" stop-color="#fff1b8"/><stop offset=".45" stop-color="#f0bd3a"/><stop offset="1" stop-color="#b8860b"/></radialGradient>
</defs>
<path class="ax" d="M20 240H400M20 180H400M20 120H400M20 60H400"/>
<path class="ar" d="M20 222C80 214 112 200 150 190S222 166 262 134S332 82 400 52L400 240L20 240Z"/>
<path class="ln" d="M20 222C80 214 112 200 150 190S222 166 262 134S332 82 400 52"/>
<circle class="dot" cx="400" cy="52" r="5"/>
<g class="coin"><circle class="coin-face" cx="205" cy="92" r="46"/><circle class="coin-rim" cx="205" cy="92" r="37"/>
<text class="coin-sym" x="205" y="108" text-anchor="middle">&#163;</text></g>
</svg>
<a class="fc f1" href="%s"><b>&#163;1,723</b><span>Energy price cap</span></a>
<a class="fc f2" href="%s"><b>&#163;252</b><span>Marriage Allowance</span></a>
<a class="fc f3" href="%s"><b>&#163;150</b><span>Warm Home Discount</span></a>
</div>""" % (art_href("energy-price-cap-october-2026.html"),
             art_href("marriage-allowance-252-a-year-who-can-claim-uk.html"),
             art_href("warm-home-discount-150-who-gets-it-automatically-uk.html"))
    faq = [
        ("Who writes these guides?", "Ruhul Amin, based in Hertfordshire. Every guide is written with the actual UK figures and the rules that apply."),
        ("How are the numbers checked?", "Against official sources such as GOV.UK, HMRC, Ofgem and the Bank of England. Each guide lists its sources at the end and says when the figures were checked."),
        ("How does the site make money?", 'Some links are affiliate links. If you buy through one, the site may earn a small commission at no extra cost to you. <a href="/affiliate-disclosure.html">Affiliate disclosure</a>.'),
        ("Is this financial advice?", "No. It is general guidance. Rates and rules change, so check the linked source before you act."),
    ]
    faq_html = "".join("<details><summary>%s</summary><p>%s</p></details>" % (E(q), a) for q, a in faq)
    body = """%s<main>
<section class="hero"><div class="w">
<p class="eyebrow">UK money guides</p>
<h1>Make more.<br><span class="gr">Spend less.</span></h1>
<p class="lead">%d UK money guides. Real numbers, checked against GOV.UK and Ofgem.</p>
%s
<div class="srch" role="search">
<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="M20 20l-3.5-3.5"/></svg>
<label class="sr" for="q">Search guides</label>
<input id="q" type="search" placeholder="Search %d guides" autocomplete="off" role="combobox" aria-expanded="false" aria-controls="res" aria-autocomplete="list">
<span class="kbd" aria-hidden="true">/</span>
<div class="res" id="res" role="listbox" hidden></div>
</div>
<p class="hint">Popular: <a href="%s">price cap</a> &middot; <a href="%s">side hustle tax</a> &middot; <a href="%s">Marriage Allowance</a></p>
</div></section>
<section class="c"><div class="w">
<h2>Pick a topic</h2>
<p class="sub">Eight shelves. Every guide is on one.</p>
<div class="tiles">%s</div>
</div></section>
<section class="c"><div class="w">
<h2>Latest guides</h2>
<p class="sub">Newest first.</p>
<div class="cards">%s</div>
<div class="more"><a class="btn gh" href="%scategories/save-money.html">Browse all guides</a></div>
</div></section>
<section class="faq c"><div class="w">
<h2>Questions</h2>
<p class="sub">The short answers.</p>
%s
</div></section>
</main>
""" % (header(), n, stage, n,
       art_href("energy-price-cap-october-2026.html"), art_href("side-hustle-tax-rules-uk.html"),
       art_href("marriage-allowance-252-a-year-who-can-claim-uk.html"),
       tiles, latest, BASE, faq_html)
    if LIVE:
        meta = head_meta(read("index.html"))
        write("index.html", head(meta, ld_json(meta)) + body + footer())
        return
    else:
        meta = ('<title>Earning Money Online UK | Make more, spend less</title>\n'
                '<meta name="description" content="%d practical UK money guides with real numbers, checked against official sources.">\n'
                '<link rel="canonical" href="https://earningmoneyonline.co.uk/">' % n)
    write("index.html", head(meta) + body + footer())


# ---------------------------------------------------------------- categories
def categories(idx):
    for tag, slug, short, ic, name, desc in CATS:
        items = [a for a in idx if a["c"] == tag]
        cards = "".join(card(a) for a in items) or '<p class="empty">No guides yet.</p>'
        body = """%s<main>
<section class="ph"><div class="w">
<p class="crumb"><a href="%s">Home</a> &middot; %s</p>
<span class="pill">%d guides</span>
<h1>%s</h1>
<p class="lead">%s</p>
</div></section>
<section class="c" style="padding-top:20px"><div class="w"><div class="cards list">%s</div></div></section>
</main>
""" % (header(slug), BASE, E(short), len(items), E(name), E(desc), cards)
        if LIVE:
            meta = head_meta(read("categories/%s.html" % slug))
            write("categories/%s.html" % slug, head(meta, ld_json(meta)) + body + footer())
            continue
        else:
            meta = ('<title>%s | EarningMoneyOnline</title>\n<meta name="description" content="%s">\n'
                    '<link rel="canonical" href="https://earningmoneyonline.co.uk/categories/%s.html">' % (E(name), E(desc), slug))
        write("categories/%s.html" % slug, head(meta) + body + footer())


# ---------------------------------------------------------------- article style pages
def fix_href(h, page_dir):
    """Make a link absolute, so it works wherever the page is written."""
    if not h or h.startswith(("http:", "https:", "#", "mailto:", "tel:", "/", "data:", "javascript:")):
        return h
    path, _, frag = h.partition("#")
    p = posixpath.normpath(posixpath.join(page_dir, path))
    if not LIVE:
        if p.startswith("/articles/") and posixpath.basename(p) in PREVIEW_ARTICLES:
            p = BASE + "articles/" + posixpath.basename(p)
        elif p.startswith("/categories/"):
            p = BASE.rstrip("/") + p
    return p + ("#" + frag if frag else "")


def page(rel):
    """Rebuild one article style page (an article or a static page like about.html)."""
    s = read(rel)
    p = parse_page(s)
    page_dir = "/" + posixpath.dirname(rel) + "/" if "/" in rel else "/"
    inner = p["body"]
    if mark("body", s) is None:  # old template: tidy once, then the markers keep it as it is
        inner = re.sub(r'href="([^"]*)"', lambda m: 'href="%s"' % fix_href(m.group(1), page_dir), inner)
        inner = re.sub(r"(<table\b.*?</table>)", r'<div class="tbl">\1</div>', inner, flags=re.S | re.I)
        inner = re.sub(r'<img(?![^>]*class="cover")(?![^>]*loading=)', '<img loading="lazy"', inner)
    tag = p["tag"]
    cslug = TAG2SLUG.get(tag, "")
    short = next((c[2] for c in CATS if c[1] == cslug), tag)
    crumb = ('<a href="%s">Home</a> &middot; <a href="%scategories/%s.html">%s</a>' % (BASE, BASE, cslug, E(short))
             if cslug else '<a href="%s">Home</a>' % BASE)
    by = ""
    if p["who"] or p["when"]:
        av_img = ('<img src="%s" alt="">' % E(p["avatar"])) if p["avatar"] else ""
        who = ("<b>%s</b> &middot; " % wrap("who", E(p["who"]))) if p["who"] else ""
        by = '<div class="by">%s<span>%s%s</span></div>' % (av_img, who, wrap("when", p["when"]))
    av_mark = ('<span hidden>%s</span>' % wrap("av", E(p["avatar"]))) if p["avatar"] else ""
    sf = ('<p class="standfirst">%s</p>' % wrap("sf", p["standfirst"])) if p["standfirst"] else ""
    body = """%s<main>
<section class="ph ah"><div class="w">
<p class="crumb">%s</p>
%s
<h1>%s</h1>
%s%s
</div></section>
<article class="ab">
%s
%s
</article>
</main>
""" % (header(cslug), crumb, ('<span class="pill">%s</span>' % wrap("tag", E(tag))) if tag else "",
       wrap("h1", p["h1"]), by, av_mark, sf, wrap("body", inner))
    write(rel, head(p["meta"], FONT + (ld_json(p["meta"], p, rel) if LIVE else "")) + body + footer())


def main():
    os.makedirs(os.path.join(OUT, "assets"), exist_ok=True)
    if LIVE:
        shutil.copyfile(os.path.join(SRC_ASSETS, "glass.css"), asset_path(CSS_NAME))
        shutil.copyfile(os.path.join(SRC_ASSETS, "glass.js"), asset_path(JS_NAME))
    idx = build_index()
    search = [{"u": a["u"], "t": a["t"], "c": a["c"], "d": a["d"], "x": a["x"]} for a in idx]
    with open(asset_path("search.json"), "w", encoding="utf-8") as f:
        json.dump(search, f, ensure_ascii=False, separators=(",", ":"))
    if LIVE:  # live: every article and static page; preview: the five sample articles only
        for f in sorted(os.listdir(os.path.join(ROOT, "articles"))):
            if f.endswith(".html"):
                page("articles/" + f)
        for rel in STATIC_PAGES:
            if os.path.exists(os.path.join(ROOT, rel)):
                page(rel)
    else:
        for slug in PREVIEW_ARTICLES:
            page("articles/" + slug)  # reads the real article, writes under /preview/
    homepage(idx)
    categories(idx)
    print("%s built: %d articles indexed, %d categories" % ("live" if LIVE else "preview", len(idx), len(CATS)))


if __name__ == "__main__":
    main()
