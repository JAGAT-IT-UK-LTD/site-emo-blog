# Affiliate setup, EarningMoneyOnline (9 Nov 2026)

## Where things stand
1. Amazon Associates: account ID `earningmon051-21`, now on all 212 Amazon links. Amazon wrote on 26 Oct 2026 that there are no three qualified sales yet. Without three sales within 180 days of 27 Jul 2026 the account closes, so around 23 Jan 2027.
2. Awin: publisher 3046515 approved 19 Aug 2026. Only WebHosting UK approved the site. Cloudways and 20i said the site was not relevant, RAC said the profile was incomplete.
3. Skimlinks: no account. The site is ready for it, see below.

## Traffic to quote in applications (checked 9 Nov 2026)
1. Google Search Console, last 28 days: 29 clicks, 7.44K impressions, 325 pages indexed.
2. GA4, 12 Oct to 8 Nov 2026: 357 sessions, 94 percent from search (Bing 170, Yahoo UK 103, DuckDuckGo 43, Google 12), 67 percent engaged, 54 seconds average.
3. GA4 counts only visitors who accept cookies, so real visits are higher.

## Awin profile text (R pastes it after logging in, Account, Promotional space)
Site: https://earningmoneyonline.co.uk

Description: EarningMoneyOnline is an independent UK money guide site with 456 original guides on cutting household bills, switching energy and broadband, cashback, insurance, home improvement costs, side income and UK tax rules. Every guide uses real UK figures checked against official sources such as GOV.UK, HMRC and Ofgem, with a worked example and an honest verdict. Readers are UK households comparing costs before they spend.

Promotional type: Content, editorial and reviews. Audience: United Kingdom, adults 25 to 60. Traffic: search, mainly Bing, Yahoo UK, DuckDuckGo and Google.

## Awin programmes to apply to (each profile checked live on 9 Nov 2026)
| Advertiser | Awin profile | Public commission | Fits |
| --- | --- | --- | --- |
| Quidco UK New Member CPL | https://ui.awin.com/merchant-profile/15819 | per new member, no figure | cashback cards |
| TopCashback | https://ui.awin.com/merchant-profile/2459 | per new member, no figure | cashback |
| MoneySupermarket Energy | https://ui.awin.com/merchant-profile/22713 | £4.01 per switch | energy bills |
| MoneySupermarket Insurance | https://ui.awin.com/merchant-profile/12049 | car £4.20, home £3.50 | insurance |
| Mymoneycomparison | https://ui.awin.com/merchant-profile/22605 | not published | insurance |
| Zen Internet | https://ui.awin.com/merchant-profile/119927 | agreed per publisher | broadband |
| Paybacker | https://ui.awin.com/merchant-profile/125502 | per switch, no figure | bills switching |
| HyperJar UK | https://ui.awin.com/merchant-profile/23943 | £6 per card order | savings app |
| ManoMano UK | https://ui.awin.com/merchant-profile/17964 | not published | DIY and home |
| Home Fixtures | https://ui.awin.com/merchant-profile/130489 | not published | bathroom and kitchen |
| Building Materials | https://ui.awin.com/merchant-profile/23859 | 3 percent of sale | home improvement |
| Names.co.uk | https://ui.awin.com/merchant-profile/897 | not published | websites and domains |

Not available on Awin: Etsy (moved to Rakuten), Uswitch (closed), Compare the Market (FlexOffers only).

## Skimlinks, when R has an account
1. R signs up at skimlinks.com with ruhulsedu001@gmail.com and the site URL. Applications are reviewed by hand. 456 original UK guides should meet their bar.
2. After approval: Publisher Hub, Settings, Install shows an ID like `123456X1234567`.
3. Put that ID in `data/affiliate.json` as `skimlinks_id`, run `python3 -I tools/build-preview.py --live`, open a PR, merge.
4. The site then loads `https://s.skimresources.com/js/<ID>.skimlinks.js` only after a visitor accepts cookies, and the cookie banner says so.
5. Add Skimlinks to the privacy policy cookie list in the same PR.
