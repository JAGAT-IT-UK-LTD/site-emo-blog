# APPFLOW, EarningMoneyOnline

## 1. ঢোকার পথ
1. Google search থেকে সরাসরি article এ। বেশিরভাগ visitor এভাবে আসে।
2. Social share link থেকে article এ।
3. সরাসরি homepage এ।

## 2. Route
| Route | কী |
| --- | --- |
| `/` | homepage |
| `/categories/<slug>.html` | ৮টা category |
| `/articles/<slug>.html` | 456 article |
| `/about.html`, `/contact.html` | পরিচয় |
| `/privacy/`, `/terms/`, `/affiliate-disclosure.html` | আইন |
| `/sitemap.xml`, `/feed.xml`, `/robots.txt` | crawler |
| `/preview/` | নতুন design, noindex, robots এ বন্ধ |

## 3. Flow
খোঁজা: homepage, search box এ লেখা, ফলের তালিকা, article।

ঘোরা: homepage, category tile, category page, article।

পড়া: article, short version, সূচি, মূল লেখা, verdict, source, related guide।

টাকা দেওয়ার flow নেই। Affiliate link নতুন tab এ খোলে।

## 4. অবস্থা
| Screen | Loading | খালি | Error | Offline |
| --- | --- | --- | --- | --- |
| Homepage search | "Loading guides" | "No guide matches", সাথে দুইটা উদাহরণ শব্দ | "Search could not load", category দেখতে বলে | error এর একই লেখা |
| Category | static, loading নেই | article না থাকলে "No guides yet" | 404 page | browser cache |
| Article | static | প্রযোজ্য না | 404 page | browser cache |
| ছবি | ধূসর glass ঘর | প্রযোজ্য না | ছবি না এলে glass ঘর থাকে, layout ভাঙে না | একই |
