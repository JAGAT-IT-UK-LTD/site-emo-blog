# Project passport: site-emo-blog

> Family: **Content / Media** · Owner: @ruhulamin0001 · Completeness: **52%** · Generated 2026-10-15
> Auto-filled from repo files only; `TBC` = unknown. **Never put secret values here.** Update after every change.

## Domain & DNS
earningmoneyonline.co.uk (VERIFIED: routed by Traefik on uk-vps (72.62.213.196, Hostinger srv1569293) 2026-10-15; TLS cert expires 2026-12-16; registrar TBC)

## Hosting/VPS & deploy
uk-vps (72.62.213.196, Hostinger srv1569293) (Traefik + Docker). Compose project `earningmoneyonline`, path `/root/earningmoneyonline (nginx static; synced from /root/emo-uk-repo by /root/deploy-emo.sh every 5 min)`. Containers: see path. Deploy remote: /root/emo-uk-repo → https://github.com/ruhulamin0001/emo-uk-site.git (OLD owner URL, redirect)

## GitHub
https://github.com/JAGAT-IT-UK-LTD/site-emo-blog (public), default branch main

## Brand
Uses design-system: https://github.com/JAGAT-IT-UK-LTD/design-system (logo/colours TBC)

## Website
https://earningmoneyonline.co.uk (HTTP 200 on 2026-10-15)

## Email
TBC

## Phone/web phone
TBC

## Apps
TBC

## Payment gateway
TBC

## Paperwork/legal
privacy page present, terms page present

## ENV (names only)
TBC

## Credentials
TBC

## Code/stack
Static HTML

## Database
TBC

## Data store/backups
No app-specific backup. Server-wide: nightly /root/ops/backup-databases.sh (every DB, keep 7) + backup-vps.sh (configs, keep 7) into /root/backups on the same disk. Off-site since 15 Oct 2026: nightly 04:30 age-encrypted archive → bd-vps `/srv/offsite/uk-vps` (14 days, sha256 + restore self-test). Cloudflare R2 third copy live since 16 Oct 2026 (encrypted, 7 days).

## Marketing
TBC

## Sales plan
TBC

## AI/agents
Claude Code, GitHub Copilot; last push 2026-10-15

## Progress
Last push 2026-10-15. Description: earningmoneyonline.co.uk custom HTML site + contentstudio. Managed via Claude Cowork.

## Competitors
TBC

## Google traffic/SEO
Google Search Console verification file present; Bing verification present; sitemap present (Search Console property / GA4 id TBC)

## Owner
@ruhulamin0001

## Risks
TBC
