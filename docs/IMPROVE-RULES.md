# Nightly improvement rules, EarningMoneyOnline

R asked on 9 Nov 2026: every night at 11 pm improve 10 existing articles. Better SEO and keywords, more gripping, easy to read like a book page. No new articles, no big change at once.

The order is in `data/improve-queue.json` (articles whose dates have passed first, then the ones whose figures were checked longest ago). `python3 -I tools/improve.py next 10` prints tonight's ten.

## Never
1. Never change a file name, URL or canonical. Never delete an article.
2. Never remove an affiliate link or change the Amazon tag `earningmoneyonline-21`. Keep every `rel` value.
3. Never invent a figure, a quote, a review, a reader or a statistic. Every number needs a linked official or primary source checked in this run.
4. Never touch `preview/`, `assets/`, `js/`, `tools/`, design files, other repos or the server.
5. Never write a new article. Improve only the ten in the queue.
6. No dashes and no emoji in new text. Use commas and full stops.

## Where to edit
Pages are built by the generator. Edit only inside these markers in the article file, then run `python3 -I tools/build-preview.py --live`:
1. `<!--emo:meta-->`: `<title>`, `<meta name="description">`, `og:title`, `og:description`, `twitter:title`, `twitter:description`. Keep canonical, og:url, og:image as they are.
2. `<!--emo:h1-->`: the headline on the page.
3. `<!--emo:sf-->`: the opening paragraph under the headline.
4. `<!--emo:when-->`: keep `Published ...`, add or update `Updated <d Month yyyy>` and `Figures checked <Month yyyy>`.
5. `<!--emo:body-->`: the article.

## SEO
1. Find the main search phrase: Google autocomplete (`https://suggestqueries.google.com/complete/search?client=firefox&hl=en-GB&gl=uk&q=<phrase>`) and a standard web search for the topic. Note the People Also Ask questions and what the top three UK results cover.
2. Title: main phrase near the front, 50 to 60 characters, a number or a year when it helps, says what the reader gets.
3. Description: 140 to 155 characters, the answer in short with one real figure, ends with why to click.
4. Use the main phrase in the headline, in the first 100 words, and in one H2. Use 3 to 5 related phrases naturally in H2s and text. No keyword stuffing.
5. At least 3 links to other guides on this site that a reader of this one would want next, with plain descriptive link text.
6. A `Frequently asked` H2 with 3 to 5 real questions from People Also Ask, each answered in 40 to 60 words.

## Gripping and easy to read, like a book page
1. The opening paragraph gives the answer in two or three sentences, then why it matters to this reader.
2. Paragraphs of one to three sentences. Sentences mostly under 20 words. Plain British English, UK spelling, £.
3. One idea per paragraph, one line of thought after another. Headings that read like the reader's own questions.
4. Keep or add one worked example with a named UK household and real sums. Keep `The short version` box and update it.
5. Tables for comparisons. A pull quote only for the single most surprising fact.
6. Keep the honest verdict. Say plainly when something is not worth it.

## Facts
1. Check every figure against the official source today (GOV.UK, HMRC, Ofgem, Bank of England, ONS, FCA, legislation.gov.uk, the provider's own page).
2. If a figure changed, fix it everywhere in the article, including examples, tables and the short version.
3. An article about a date that has passed (a budget, a rate decision, a deadline) must now say what actually happened, with the source.
4. Update the `Sources and further reading` list with the pages you used.

## Before merge
`python3 -I tools/improve.py check <the ten slugs>` must print `all 10 pages passed`. It fails on: changed canonical, title not 30 to 65 characters, description not 120 to 165, missing social tags, missing design markers, body shrunk below 85 percent, fewer outside source links, fewer Amazon links, new dashes, no Frequently asked section, no `Figures checked <Month> <this year>`, broken or fewer than 3 internal links. If one article cannot pass, put it back with `git checkout origin/main -- articles/<slug>`, leave it `todo`, and say why in the log.
