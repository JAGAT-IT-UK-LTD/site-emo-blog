# BRIEF, EarningMoneyOnline (site-emo-blog)

## What it is
earningmoneyonline.co.uk, a plain HTML blog about earning money online (456 article files, 8 category pages). Income is affiliate links, no customer pays the site directly.

## Where it is live
- https://earningmoneyonline.co.uk, 200 on 6 Nov 2026. `www` also 200 (no redirect to the bare name).
- No healthz (`/healthz` 404). Live `index.html` was byte for byte the same as `main` on 6 Nov 2026. Live sitemap and repo sitemap both have 410 URLs.
- New Liquid Glass design preview: https://earningmoneyonline.co.uk/preview/ (noindex, blocked in robots.txt). Live design unchanged until R says yes.

## Content state
- Newest article is dated 8 Oct 2026. Nothing published since.
- Some articles look ahead to dates that have now passed (Budget 28 Oct 2026, Bank Rate 5 Nov 2026). They need an update.
- `data/articles.json` is stale (51 entries, 16 Aug 2026). The preview builds its own index from the article files.

## Why new articles stopped (found 9 Nov 2026)
- Articles were written by two Claude Cowork scheduled tasks (Mon, Wed, Fri daily task and a Thursday weekly task) on the old Windows computer, saved under Downloads/emo-data, then approved in the Studio and committed.
- The computer moved to the Mac on 14 Oct 2026. The files came across (now in ~/Documents/from-windows/Downloads/emo-data) but the Cowork tasks did not. No article task exists on this Mac, local or cloud. The Studio was also split out of this repo on 15 Oct.
- Only the cloud routine "Monthly trending topics" (trig_01CVoS68gMvgrzDoM2m8hHJ1) is left, and it is turned off.
- Eight finished articles from 13 Sep 2026 were never published (about 2,050 words each, in emo-data/articles-home-2026-09-13): artificial grass vs lawn, deposit deductions fair wear and tear, eco 40 60 programme, heating oil price volatility, leaky toilet on a water meter, surface water drainage rebate, washer dryer vs separate machines, Water Smart rising block tariff. Their figures need a fresh check before publishing.

## Affiliate state (from the code, 9 Nov 2026)
- Amazon Associates: tag `earningmoneyonline-21` on all 212 Amazon links in 89 articles, every link marked sponsored. Earnings are not visible from here, the Associates dashboard needs the owner login.
- Awin: one link only (eukhost), publisher id 3046515.
- Skimlinks: written about in articles, but its script is not on the site, so it earns nothing.
- GA4 id G-GQ2B6EM9YC loads only after cookie consent.

## Cloudflare cache
Cloudflare caches CSS and JS for 4 hours. The preview asset URLs carry a content hash (`?v=`) for that reason. The live `css/style.css` has no hash, so a change to it can take up to 4 hours to show.

## Design work, 6 Nov 2026
- Six docs in `docs/` (SPEC is the index). Design brief: `docs/DESIGN-BRIEF.md`, plan: `docs/PLAN.md`.
- `tools/build-preview.py` rebuilds `/preview/` from the real article and category files. Run `python3 -I tools/build-preview.py` from the repo root after any content change.
- Preview has homepage with search, 8 categories, 5 articles. Other cards link to the live article.
- 9 Nov: colour A navy to indigo is the default, B is the old green, switch in the preview badge. Articles read as a book page in Literata.

## How it deploys
Not the GitHub image pipeline, and nothing is built. Static nginx on uk-vps, box folder `/root/earningmoneyonline`, synced every 5 minutes from a git checkout `/root/emo-uk-repo` (its remote is the old owner URL, which redirects to this repo). Source: `project/project.yaml`. A push to `main` goes live within minutes.

## Money
Off. No checkout, no gateway in the code. Affiliate links only, with an affiliate disclosure page.

## RAM on the box
Not measured.

## Session
The Claude session that owns this repo is named "EarningMoneyOnline (site-emo-blog)" in the app.

## Next steps
1. R looks at `/preview/` and says yes or what to change. Then roll the design to every page (`docs/PLAN.md` milestone 5).
2. Restart article writing on this Mac or as a cloud routine (needs R yes), fact check and publish the 8 waiting articles, update the articles whose dates have passed.
3. Decide whether this site stays on the 5 minute git sync or moves to the image pipeline like the other sites.
4. Two old open PRs (3 and 4, from 3 Sep 2026) are for other projects (DriverJagat, a voice stack) and do not belong in this repo.
5. `www` should 301 to the bare name.

## Owner clicks
- Look at https://earningmoneyonline.co.uk/preview/ on the phone and say yes or what to change.
- Affiliate accounts and their payouts (owner accounts).
- Yes or no on closing the two stray PRs 3 and 4.

## Rules
Read `CLAUDE.md`, `AI.md` and `README.md` first. Rules source is JAGAT-IT-UK-LTD/ai-memory `CHARTER.md`.

Last updated: 9 Nov 2026, Claude Opus 5.5.
