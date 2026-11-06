# DESIGN-BRIEF, EarningMoneyOnline

## 1. Style
Liquid Glass, dark। এটাই প্রথম পছন্দ। Spatial UI আর Skeuomorphism এই ধাপে নেই, দরকার হলে `/preview/<style>/` এ আলাদা।

## 2. Glass এর মাপ
1. পটভূমি `#05070d`।
2. Glass: `backdrop-filter: blur(22px) saturate(170%)`, সাদা gradient `.14` থেকে `.04`, border সাদা `.18`, উপরে inset আলো `inset 0 1px 0 rgba(255,255,255,.22)`।
3. পেছনে তিনটা রঙিন blob, GSAP দিয়ে ধীরে চলে: সবুজ `#0fae7e`, সোনালি `#e8b021`, নীল `#3d7bff`। সবুজ আর সোনালি পুরনো brand এর রঙ, তাই চেনা থাকে।
4. Pointer যেখানে, card এর উপর সেখানে নরম আলো।

## 3. Layout, web-evbattery এর মত
Homepage উপর থেকে নিচে:
1. Logo, glass coin এর SVG icon আর ছোট wordmark।
2. Category chip এর এক সারি। Phone এ পাশে scroll হয়।
3. ছোট headline: "Make more. Spend less."
4. এক লাইন: "456 UK money guides. Real numbers, checked against GOV.UK and Ofgem."
5. কাজের animation: একটা glass coin, নিচে savings এর রেখা আঁকা হয়, পাশে তিনটা আসল সংখ্যার chip (price cap £1,723, Marriage Allowance £252, Warm Home Discount £150), প্রতিটা নিজের article এ যায়।
6. মূল input: search box, "Search 456 guides"।
7. ৮টা category tile, নাম আর guide সংখ্যা শুধু।
8. Latest, নতুন ৬টা guide।
9. খোলা যায় এমন FAQ, ৪টা প্রশ্ন।
10. ছোট footer।

Check site না, platform site ও না, এটা content site। তাই প্রথম পাতায় price card নেই।

## 4. লেখা
Homepage এ লেখা প্রায় ৮০ শতাংশ কম। পুরনো homepage 270 KB, 383টা card। নতুনটায় ৬টা card আর search। এক typeface, system stack। ছোট text scale: 13, 15, 17, 22, তারপর heading এর জন্য clamp।

## 5. সাজানো
1. Heading, card, chip মাঝখানে।
2. Article এর মূল লেখা বামে, 70ch column এ।
3. Table phone এ পাশে scroll হয়, page ভাঙে না।

## 6. Phone আগে
375 এ: header আর chip সারি 110px এর মধ্যে, headline আর animation 450px এর মধ্যে শুরু, search box প্রথম screen এর একটু নিচে, tile ২ কলাম।
1280 এ: মাঝে 1080px এর column, tile ৪ কলাম, latest ৩ কলাম, article column 70ch।

## 7. Login
এই site এ login নেই।

## 8. Animation আর accessibility
1. এই site এর নিজের animation: coin আর savings রেখা। অন্য কোনো site এ এটা নেই।
2. `prefers-reduced-motion` হলে blob, coin আর রেখা থেমে থাকে।
3. লেখা আর পটভূমির contrast 4.5:1 এর বেশি, মূল লেখা `#e9eef6`।
4. Tap target কমপক্ষে 44px।
5. প্রতিটা link আর button এ keyboard focus এর দাগ।

## 9. Footer
"EarningMoneyOnline is a trading name of JAGAT IT UK LTD, registered in England and Wales, company number 17474995. Registered office: 164 High Street, London Colney, St Albans, Hertfordshire, England, AL2 1QF." ঠিকানা web-evbattery এর approve হওয়া footer থেকে নেওয়া।

## 10. Preview link
https://earningmoneyonline.co.uk/preview/

সেখান থেকে ৮টা category আর ৫টা article এর preview খোলা যায়। Preview noindex, robots এ বন্ধ, live design এ কোনো বদল নেই।
