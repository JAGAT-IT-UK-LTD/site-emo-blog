# BRIEF, EarningMoneyOnline (site-emo-blog)

## What it is
earningmoneyonline.co.uk, a plain HTML blog about earning money online (456 article files, 8 category pages). Income is affiliate links, no customer pays the site directly.

## Where it is live
- https://earningmoneyonline.co.uk, 200 on 6 Nov 2026. `www` also 200 (no redirect to the bare name).
- No healthz (`/healthz` 404). Live `index.html` was byte for byte the same as `main` on 6 Nov 2026. Live sitemap and repo sitemap both have 410 URLs.
- 9 Nov 2026: R said go on, so every page now uses the new design (navy indigo Liquid Glass, articles as a book page in Literata). /preview/ stays as the test bed (noindex).

## Content state
- 9 Nov 2026: the 8 September articles are published (dated 9 Nov 2026, every figure checked again that day). Biggest fix: Severn Trent bills used water on 95% of supply, so the metered rate is £4.0945 a cubic metre, not £4.1758.
- 9 Nov 2026: six articles whose dates had passed now say what happened: Budget 28 Oct 2026 (Chancellor John Healey; savings and property income tax 24/44/49% from April 2027; trading allowance £3,000; National Living Wage £13.21), Bank Rate 5 Nov 2026 (raised to 4%, vote 8 to 1, next decision 17 Dec), Bank Rate 17 Sep (held at 3.75%), two mortgage pieces, September CPI 3.5% and the April 2027 uprating. They are marked done in `data/improve-queue.json`.
- `sitemap.xml` was missing 26 older articles as well; `tools/sync-sitemap-feed.py` adds every article and rebuilds `feed.xml` (newest 30). `feed.xml` had not changed since 21 Aug.
- Older live articles still use £4.1758 for Severn Trent water (water butt, low flow shower head and others). The nightly improvement should correct them to £4.0945.
- `data/articles.json` is stale (51 entries, 16 Aug 2026). The preview builds its own index from the article files.

## Why new articles stopped (found 9 Nov 2026)
- Articles were written by two Claude Cowork scheduled tasks (Mon, Wed, Fri daily task and a Thursday weekly task) on the old Windows computer, saved under Downloads/emo-data, then approved in the Studio and committed.
- The computer moved to the Mac on 14 Oct 2026. The files came across (now in ~/Documents/from-windows/Downloads/emo-data) but the Cowork tasks did not. No article task exists on this Mac, local or cloud. The Studio was also split out of this repo on 15 Oct.
- Only the cloud routine "Monthly trending topics" (trig_01CVoS68gMvgrzDoM2m8hHJ1) is left, and it is turned off.
- Eight finished articles from 13 Sep 2026 were never published (about 2,050 words each, in emo-data/articles-home-2026-09-13): artificial grass vs lawn, deposit deductions fair wear and tear, eco 40 60 programme, heating oil price volatility, leaky toilet on a water meter, surface water drainage rebate, washer dryer vs separate machines, Water Smart rising block tariff. Their figures need a fresh check before publishing.

## Affiliate state (from the code, 9 Nov 2026)
- Amazon Associates: the account ID from Amazon's welcome email (27 Jul 2026) is `earningmon051-21`. Until 9 Nov 2026 the site used `earningmoneyonline-21`, which no Amazon email mentions, so those clicks may never have counted. All 212 links in 89 articles now carry `earningmon051-21`.
- Amazon emailed on 26 Oct 2026 that the account has no three qualified sales yet. Amazon closes an account without three qualified sales within 180 days, so around 23 Jan 2027 (counted from 27 Jul). Earnings are only visible in Associates Central (owner login).
- Awin: account approved 19 Aug 2026 (publisher 3046515). Only WebHosting UK approved the site (20 Aug). One link (eukhost) on the site, no approval email found for it. No commission emails.
- Skimlinks: written about in articles, but its script is not on the site, so it earns nothing.
- GA4 id G-GQ2B6EM9YC loads only after cookie consent.

## Affiliate next steps
See `docs/AFFILIATE-SETUP.md`: Awin shortlist of 12 checked programmes, profile text, and the Skimlinks steps. The site loads Skimlinks only after cookie consent once `data/affiliate.json` has an ID.

## Traffic, 9 Nov 2026
Search Console 28 days: 29 clicks, 7.44K impressions, average position 51.4, 325 indexed, 153 not indexed (110 discovered, 39 crawled, 2 not found). GA4 12 Oct to 8 Nov: 357 sessions, Bing 170, Yahoo UK 103, DuckDuckGo 43, Google 12.

## Cloudflare cache
Cloudflare caches CSS and JS for 4 hours. The preview asset URLs carry a content hash (`?v=`) for that reason. The live `css/style.css` has no hash, so a change to it can take up to 4 hours to show.

## Nightly improvement (from 9 Nov 2026)
- R asked: every night at 11 pm improve 10 existing articles (SEO, keywords, gripping and easy to read). No new articles.
- Scheduled task `emo-nightly-improve` on this Mac (Claude app must be open; if it is closed at 11 pm the run starts when it opens).
- Order: `data/improve-queue.json`, rules: `docs/IMPROVE-RULES.md`, log: `docs/IMPROVE-LOG.md`, helper: `tools/improve.py` (queue, next, check, done, status).
- 456 articles, 10 a night, about 46 nights. Articles whose dates have passed go first (36 of them).

## How pages are built now
- `python3 -I tools/build-preview.py --live` rebuilds homepage, 8 categories, every article and the static pages (about, contact, privacy, terms, disclosure). Page text is never touched, each page keeps its own title, description, canonical and social tags.
- Safe to rerun: a new design page is read back through `<!--emo:...-->` markers, an old template page is read the old way. So a new article written in the old template is converted on the next run. Category pages and the search index come from the article files, never edit them by hand.
- The design source is `preview/assets/glass.css` and `glass.js`; live mode copies them to `/assets/emo.css` and `/assets/emo.js`. Every asset URL, including `/js/analytics.js`, carries a content hash so Cloudflare never serves an old copy.
- Structured data (Article and BreadcrumbList, or WebSite) is written into each page. `js/analytics.js` still does cookie consent, GA4, Organization and FAQ schema; its old template DOM patches stay quiet on new pages (they check `data-root` on the html tag).
- Before and after check on 9 Nov: 471 pages, title, description, canonical, og:url, og:image and article word count unchanged; 12,096 links, none broken; all sitemap URLs exist.

## Design work, 6 Nov 2026
- Six docs in `docs/` (SPEC is the index). Design brief: `docs/DESIGN-BRIEF.md`, plan: `docs/PLAN.md`.
- `tools/build-preview.py` rebuilds `/preview/` from the real article and category files. Run `python3 -I tools/build-preview.py` from the repo root after any content change.
- Preview has homepage with search, 8 categories, 5 articles. Other cards link to the live article.
- 9 Nov: colour A navy to indigo is the default, B is the old green, switch in the preview badge. Articles read as a book page in Literata.

## New articles from the cloud (from 9 Nov 2026)
- Routine `trig_01G9cJwhUBfKYaaWwpkwoM87` (claude.ai/code/routines), Sonnet 5.5, repo JAGAT-IT-UK-LTD/site-emo-blog. The prompt is short; the real rules live in `docs/WRITE-RULES.md`, so change the rules there, not in the routine.
- Each run: pick a topic (dated UK money change in the next 2 to 8 weeks, or a buyer decision), research primary sources, copy a recent article of the same category, fill the markers, run the generator, `tools/sync-sitemap-feed.py`, `tools/improve.py check`, log, PR, merge.
- The old Cowork routine "Monthly trending topics" (`trig_01CVoS68gMvgrzDoM2m8hHJ1`) stays off; it was bound to the Windows computer.
- The routine has the account connectors attached by default (Gmail, Drive and others), but its allowed tools do not include them.

## How it deploys
Not the GitHub image pipeline, and nothing is built. Static nginx on uk-vps, box folder `/root/earningmoneyonline`, synced every 5 minutes from a git checkout `/root/emo-uk-repo` (its remote is the old owner URL, which redirects to this repo). Source: `project/project.yaml`. A push to `main` goes live within minutes.

## Money
Off. No checkout, no gateway in the code. Affiliate links only, with an affiliate disclosure page.

## RAM on the box
Not measured.

## Session
The Claude session that owns this repo is named "EarningMoneyOnline (site-emo-blog)" in the app.

## Next steps
1. Design is live on every page (9 Nov). Next design step only if R asks.
2. Nightly improvement runs 10 articles a night (Mac). New articles: cloud routine "EMO article writer (Mon Wed Fri)" `trig_01G9cJwhUBfKYaaWwpkwoM87`, 07:00 UK time, one article per run, rules `docs/WRITE-RULES.md`, log `docs/WRITE-LOG.md`. It opens a PR and merges it itself when every check is green (switch `AUTO_MERGE` in the rules). It runs in the cloud, so it does not need any computer on.
3. Decide whether this site stays on the 5 minute git sync or moves to the image pipeline like the other sites.
4. Two old open PRs (3 and 4, from 3 Sep 2026) are for other projects (DriverJagat, a voice stack) and do not belong in this repo.
5. `www` should 301 to the bare name.

## Owner clicks
- Affiliate accounts and their payouts (owner accounts).
- Yes or no on closing the two stray PRs 3 and 4.

## Rules
Read `CLAUDE.md`, `AI.md` and `README.md` first. Rules source is JAGAT-IT-UK-LTD/ai-memory `CHARTER.md`.

Last updated: 9 Nov 2026 late, Claude Opus 5.5 (article restart session).
