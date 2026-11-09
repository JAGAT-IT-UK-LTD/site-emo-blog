# PLAN, EarningMoneyOnline নতুন design

## Milestone 1, design system আর header footer
কাজ: `preview/assets/glass.css`, `preview/assets/glass.js`, logo, header, footer।
নির্ভরতা: নেই।
Acceptance: 375 আর 1280 এ header আর footer ঠিক, footer এ trading name আর ঠিকানা।
R এর phone check: https://earningmoneyonline.co.uk/preview/ খুলে নিচে footer এ company লাইন দেখবেন।

## Milestone 2, homepage preview
কাজ: `preview/index.html`, search, category tile, latest, FAQ।
নির্ভরতা: Milestone 1।
Acceptance: search এ "tax" লিখলে guide আসে, tile সংখ্যা article file এর সাথে মেলে, horizontal scroll নেই।
R এর phone check: preview খুলে search এ "energy" লিখবেন, তালিকা আসবে।

## Milestone 3, category আর article preview
কাজ: `preview/categories/` এ ৮টা, `preview/articles/` এ ৫টা।
নির্ভরতা: Milestone 1।
Acceptance: article এর মূল লেখা হুবহু, table phone এ scroll হয়, সব link কাজ করে।
R এর phone check: preview এর Save Money tile, তারপর প্রথম guide।

## Milestone 4, R এর হ্যাঁ
কাজ: R preview দেখেন।
Acceptance: R chat এ হ্যাঁ বলেন, বা কী বদলাতে হবে বলেন।

## Milestone 5, সব page এ নতুন design
কাজ: generator দিয়ে homepage, ৮ category আর 456 article এ নতুন header, footer, CSS। `js/analytics.js` এর cookie consent রাখা হবে। পুরনো `css/style.css` থাকবে যতদিন না সব page বদলায়।
নির্ভরতা: Milestone 4।
Acceptance: সব 410 sitemap URL 200, canonical আর meta আগের মত, Search Console এ নতুন error নেই, 375 আর 1280 screenshot।
R এর phone check: https://earningmoneyonline.co.uk/ খুলে নতুন design দেখবেন।

অবস্থা: Milestone 5 শেষ, 9 Nov 2026। R "go on" বলার পরে সব page নতুন design এ।

## Milestone 6, content update
কাজ: তারিখ পার হওয়া article এর তালিকা (Budget 28 Oct, Bank Rate 5 Nov ইত্যাদি) আর update, `data/articles.json` হয় update নয়তো search index দিয়ে বদল।
নির্ভরতা: নেই, Milestone 5 এর সাথে চলতে পারে।
