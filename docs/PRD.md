# PRD, EarningMoneyOnline

## 1. পণ্য এক লাইনে
earningmoneyonline.co.uk, UK মানুষের জন্য টাকা আয় আর টাকা বাঁচানোর guide, প্রতিটা guide এ আসল সংখ্যা, UK নিয়ম আর সরকারি source।

## 2. সমস্যা, কার জন্য, প্রধান ৩ কাজ
সমস্যা: UK তে খরচ, tax, benefit আর side income নিয়ে বেশিরভাগ লেখা হয় বিজ্ঞাপন, নয়তো সংখ্যা ছাড়া সাধারণ কথা।

কার জন্য: UK তে থাকা সাধারণ পরিবার, নতুন freelancer, side hustle শুরু করতে চান এমন মানুষ, বাড়িওয়ালা আর ভাড়াটে।

প্রধান ৩ কাজ:
1. একটা নির্দিষ্ট প্রশ্নের guide খুঁজে পাওয়া, search বা category দিয়ে।
2. guide পড়ে আসল সংখ্যা আর করণীয় এক নজরে বোঝা, short version আর verdict দিয়ে।
3. সরকারি source এ গিয়ে নিজে যাচাই করা।

## 3. প্রতিযোগী
| নাম | দাম | link | আমাদের সুবিধা |
| --- | --- | --- | --- |
| MoneySavingExpert | পাঠকের জন্য free, affiliate আয় | https://www.moneysavingexpert.com | প্রতিটা খরচের worked example, এক বিষয়ে এক ছোট page |
| Which? | membership, দাম যাচাই হয়নি | https://www.which.co.uk | আমাদের সব guide free, paywall নেই |
| Skint Dad | free, affiliate আয় | https://www.skintdad.co.uk | প্রতিটা সংখ্যার পাশে UK সরকারি source link |

## 4. Feature
MVP, এখন live: 456 article, 8 category, cookie consent সহ GA4, sitemap, RSS feed, privacy, terms, affiliate disclosure।

এই ধাপে: নতুন Liquid Glass design, homepage এ search, লেখা কম, phone আগে।

পরে: পুরনো হয়ে যাওয়া article এর তালিকা আর update, related guide নিজে থেকে, newsletter।

## 5. আয়
সরাসরি কোনো দাম নেই, checkout নেই। আয় affiliate link থেকে, Amazon Associates আর Skimlinks। Stripe বা PayStation লাগবে না। Affiliate disclosure page আছে।

## 6. SEO
প্রধান keyword: "how much does X cost UK", "is X worth it UK", "side hustle tax UK", "energy price cap", "what you actually get UK"।

৮টা প্রধান page:
1. `/` homepage
2. `/categories/save-money.html`
3. `/categories/make-money.html`
4. `/categories/side-hustles.html`
5. `/categories/work-career.html`
6. `/categories/tools-reviews.html`
7. `/categories/uk-update.html`
8. `/categories/affiliate-marketing.html`

সাথে `/categories/ai-tools.html` আর 456 article।

## 7. KPI
1. Search Console clicks আর impressions। Site verified।
2. GA4, শুধু consent দেওয়া visitor।
3. Affiliate click আর আয়, owner এর affiliate account থেকে।
4. নতুন design এর পরে: homepage search কতবার ব্যবহার হলো, article এ কতদূর পড়া হলো।

## 8. ঝুঁকি
1. আইন: tax, benefit, energy এর সংখ্যা পুরনো হলে ভুল তথ্য। প্রতিটা page এ "general guidance, not financial advice" আছে। 8 Oct 2026 এর পরে নতুন article নেই, আর কিছু article এর তারিখ পার হয়ে গেছে, যেমন Budget 28 Oct আর Bank Rate 5 Nov।
2. Data: কোনো user data রাখা হয় না। GA4 শুধু consent এ।
3. খরচ: প্রায় শূন্য, static file, uk-vps এ।
4. ছবি Pexels থেকে সরাসরি আসে। Pexels বদলালে ছবি ভাঙবে।
