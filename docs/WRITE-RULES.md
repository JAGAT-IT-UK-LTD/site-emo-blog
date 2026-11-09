# New article rules, EarningMoneyOnline

R said yes on 9 Nov 2026 to start article writing again, from the cloud so it never depends on one computer. A cloud routine ("EMO article writer", Mon, Wed and Fri) writes ONE new article per run, following these rules, and opens a pull request.

Switch: `AUTO_MERGE: yes`
(yes: the run merges its own PR when every check below is green. no: it opens the PR and stops. Every build changes one line on every page, so a PR left open will clash with the nightly improvement PR; that is why the default is yes.)

## Never
1. Never edit an existing article, never change a file name, URL or canonical, never delete anything. The nightly improvement task looks after old articles (`docs/IMPROVE-RULES.md`).
2. Never invent a figure, a quote, a review, a reader, a customer count or a statistic. Every number needs a linked official or primary source fetched in this run.
3. Never touch `preview/`, `assets/`, `js/`, `tools/`, `css/`, `.github/`, other repos or the server.
4. No dashes and no emoji in the text (no em dash, no en dash, no spaced hyphen used as punctuation). Use commas and full stops.
5. Never write about a topic the site already covers with the same search intent. Two "is it worth it" pieces about different products are fine. Two pieces where the reader's next action is the same are not.
6. No affiliate link unless it is a real product the reader would buy for this decision. Amazon links use the tag `earningmon051-21` and `rel="sponsored nofollow noopener"`.

## 1. Pick the topic
1. List `articles/` and read the last 20 lines of `docs/WRITE-LOG.md` so you do not repeat a topic or a category.
2. Good topics, in this order:
   1. A UK rule, rate or deadline that changes in the next 2 to 8 weeks and touches household money (GOV.UK, HMRC, DWP, Ofgem, Bank of England, FCA announcements). Say the date in the headline.
   2. A spending decision where a UK buyer researches hard before paying real money (repair or replace, is X worth it, A versus B, what it really costs), where the answer is a sum the reader can check.
   3. A plain question many people search with no good UK answer yet (check Google autocomplete: `https://suggestqueries.google.com/complete/search?client=firefox&hl=en-GB&gl=uk&q=<phrase>`).
3. Rotate the 8 categories. Do not use the same category as the previous run. The tag must be exactly one of: `Save Money`, `Make Money`, `Side Hustles`, `Work & Career`, `Tools & Reviews`, `UK Update`, `Affiliate Marketing`, `AI Tools`.
4. Drop a topic whose key figures cannot be confirmed from a primary source. Pick another. Never soften a topic into vagueness to get it through.

## 2. Research
1. Use WebSearch and WebFetch. Primary sources first: GOV.UK, HMRC, DWP, legislation.gov.uk, Ofgem, Ofwat, Bank of England, ONS, OBR, FCA, the provider or regulator's own page, the manufacturer's own specification. Which?, MoneySavingExpert or trade sites only for price ranges, named as such.
2. Write down every figure with the URL it came from before you write a word. Today's date goes next to it.
3. Any sum you work out yourself (payback, annual cost, break even) is labelled as our own arithmetic and shows the inputs.

## 3. Write
House template, the same as every article on the site (look at two recent articles in the same category first, for example `articles/water-butt-payback-uk.html`):
1. Copy a recent article of the same category: `cp articles/<base>.html articles/<new-slug>.html`. Slug: lower case words joined by hyphens, ending `-uk`, no date unless the topic is a dated event.
2. Replace the contents of every `<!--emo:...-->` marker:
   1. `meta`: `<title>` (30 to 65 characters, main search phrase near the front), `<meta name="description">` (120 to 165 characters, the answer with one real figure), canonical and `og:url` set to `https://earningmoneyonline.co.uk/articles/<new-slug>.html`, `og:title`, `og:description`, `og:image`, `twitter:title`, `twitter:description`, `twitter:image`. Keep every tag the base had.
   2. `tag`: the category. `who`: `Ruhul Amin`. `av`: keep.
   3. `when`: `Published <d Month yyyy> &middot; <n> min read &middot; Figures checked <Month yyyy>` (n = words divided by 230, rounded).
   4. `h1`: a plain headline with the main phrase. `sf`: two or three sentences that give the answer, then why it matters.
   5. `body`, in this order: share block (every URL changed to the new slug), cover image, `The short version` box (`<div class="takeaways short-version">`, 4 to 6 bullets with the key figures), table of contents (`<div class="toc">`), 4 to 7 numbered H2 sections with ids, at least one comparison table in `<div class="tbl">`, one worked example with a named UK household and real sums, the honest verdict (`<div class="verdict" id="verdict">`), a `Frequently asked` H2 with 3 to 5 real People Also Ask questions answered in 40 to 60 words each, `Sources and further reading` (`<div class="resources">`, every source you used, `rel="noopener" target="_blank"`), `More from this site` (3 to 5 links to existing related articles, `/articles/<slug>.html`), the author box and the small grey disclaimer, both copied from the base.
3. 1,600 to 2,300 words. Paragraphs of one to three sentences. Sentences mostly under 20 words. Plain British English, UK spelling, £. Headings that read like the reader's own questions. Say plainly when something is not worth it.
4. Cover image: a real Pexels photo, `https://images.pexels.com/photos/<id>/pexels-photo-<id>.jpeg?auto=compress&cs=tinysrgb&w=1200`, found with WebSearch (`site:pexels.com <subject>`). Check it returns 200 (`curl -sI`). If you cannot check it, reuse the cover of the closest article in the same category. The `alt` text describes the photo.
5. At least 3 links to other articles inside the body text, plus the `More from this site` list.

## 4. Check, in this order
1. Fact pass: open every source URL in the article again and confirm each figure in the article matches it, including the short version, the table, the example and the FAQ. Fix or remove anything that does not match.
2. `git fetch origin main` then `python3 -I tools/build-preview.py --live` (puts the article on its category page, the homepage and the search index).
3. `python3 -I tools/sync-sitemap-feed.py` (adds the article to `sitemap.xml` and `feed.xml`).
4. `python3 -I tools/improve.py check <new-slug>.html` must print `all 1 pages passed`.
5. `python3 -I tools/sync-sitemap-feed.py --check` must print `sitemap and feed in step`.
6. `git status` shows only: the new article, pages the build rewrote, `sitemap.xml`, `feed.xml`, `assets/search.json`, `docs/WRITE-LOG.md`. Nothing else.

## 5. Log, commit, PR
1. Append one line to `docs/WRITE-LOG.md`: `<yyyy-mm-dd> | <slug> | <category> | <angle in one line> | <key figures with their source domain> | branch claude/article-<slug>`. The PR number is not known yet when you commit, so write the branch name; GitHub links the branch to its PR.
2. Branch `claude/article-<slug>`, one commit `article: <title>`, push, open a PR to `main` titled `article: <title>`. PR body: what the article answers, the list of figures with source URLs, the check output, and `Agent: Claude cloud routine EMO article writer`.
3. If `AUTO_MERGE: yes` and every check above passed and the PR's GitHub checks are green: squash merge it. If `main` moved and the PR conflicts: start a fresh branch from `origin/main`, copy the article file across, rerun step 4 and open a new PR, close the old one.
4. Live is a 5 minute git sync from `main`. Ten minutes after merging, fetch `https://earningmoneyonline.co.uk/articles/<new-slug>.html` and confirm 200. Note the result in the run summary.

## 6. Run summary
End with a short summary: topic, category, word count, PR link, merged or not, live check result, anything you could not verify.
