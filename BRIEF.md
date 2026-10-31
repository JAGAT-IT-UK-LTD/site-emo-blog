# BRIEF, EarningMoneyOnline (site-emo-blog)

## What it is
earningmoneyonline.co.uk, a plain HTML blog about earning money online (456 article files, 5 category pages). Income is affiliate links, no customer pays the site directly.

## Where it is live
- https://earningmoneyonline.co.uk, 200 on 31 Oct 2026. `www` also 200 (no redirect to the bare name).
- No healthz (`/healthz` 404). Live `index.html` is byte for byte the same as `main` today. Live sitemap and repo sitemap both have 410 URLs.

## How it deploys
Not the GitHub image pipeline, and nothing is built. Static nginx on uk-vps, box folder `/root/earningmoneyonline`, synced every 5 minutes from a git checkout `/root/emo-uk-repo` (its remote is the old owner URL, which redirects to this repo). Source: `project/project.yaml`. A push to `main` goes live within minutes.

## Money
Off. No checkout, no gateway in the code. Affiliate links only, with an affiliate disclosure page.

## RAM on the box
Not measured.

## Session
The Claude session that owns this repo is named "EarningMoneyOnline (site-emo-blog)" in the app.

## Next steps
No `docs/PLAN.md` and no six docs yet. Write the six docs before any big change.
1. Decide whether this site stays on the 5 minute git sync or moves to the image pipeline like the other sites.
2. Two old open PRs (3 and 4, from 3 Sep 2026) are for other projects (DriverJagat, a voice stack) and do not belong in this repo.
3. `www` should 301 to the bare name.

## Owner clicks
- Affiliate accounts and their payouts (owner accounts).
- Yes or no on closing the two stray PRs 3 and 4.

## Rules
Read `CLAUDE.md`, `AI.md` and `README.md` first. Rules source is JAGAT-IT-UK-LTD/ai-memory `CHARTER.md`.

Last updated: 31 Oct 2026.
