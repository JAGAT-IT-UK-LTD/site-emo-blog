# TRD, EarningMoneyOnline

## 1. Stack আর কেন
Plain HTML, একটা CSS, ছোট JS। কোনো framework নেই, server এ build নেই। কারণ এটা 456 page এর content site, static সবচেয়ে দ্রুত আর সস্তা।

Design master: `web-evbattery` এর layout আর liquid glass theme। নতুন design এর CSS আর JS থাকে `preview/assets/` এ। Page বানায় `tools/build-preview.py`, শুধু Python standard library, কোনো package না। Generator চালানো হয় Mac এ, ফল commit হয়, server কিছু build করে না।

## 2. বাইরের জিনিস
| নাম | কাজ | টাকা |
| --- | --- | --- |
| images.pexels.com | ছবি | free |
| Google Analytics 4 | মাপা, consent এর পরে | free |
| cdn.jsdelivr.net, gsap 3.12.5, SRI hash সহ | animation | free |
| Amazon Associates, Skimlinks | affiliate | আয়, খরচ না |

প্রতি call এ টাকা কাটে এমন কোনো API নেই।

## 3. Hosting
uk-vps, static nginx container। Folder `/root/earningmoneyonline`, প্রতি ৫ মিনিটে `/root/emo-uk-repo` git checkout থেকে sync হয়, বিস্তারিত `project/project.yaml` এ। main এ merge মানে কয়েক মিনিটে live। এই site এ ghcr image pipeline নেই, ওটা আলাদা সিদ্ধান্ত।

## 4. Env
কোনো env নেই। কোনো secret নেই।

## 5. Constraint
2 core VPS, অনেক site একসাথে। এই site CPU প্রায় নেয় না, শুধু file দেয়। এক সময়ে এক deploy।

## 6. নিরাপত্তা
কোনো লেখা server এ যায় না। Search চলে browser এ, একটা static JSON থেকে। gitleaks আর agent-gates CI আছে। বাইরের script শুধু gsap, নির্দিষ্ট version আর SRI hash সহ। gsap না এলে page ঠিক থাকে, শুধু animation থাকে না।

## 7. Performance budget
1. LCP 2.5s এর নিচে, phone এ।
2. নিজের JS 15 KB এর নিচে। gsap প্রায় 70 KB, defer।
3. Homepage এ ছবি সর্বোচ্চ ৬টা, `loading="lazy"`, Pexels `w=640`।
4. Search index শুধু search box এ focus হলে আসে।
5. Font system stack, কোনো web font না।

## 8. আইন
JAGAT IT UK LTD, company number 17474995, ICO ZC257468। Cookie consent আছে `js/analytics.js` এ, GA শুধু Accept এর পরে চলে। Privacy `/privacy/` আর `/privacy-policy.html`, terms `/terms/`, affiliate disclosure `/affiliate-disclosure.html`। নতুন footer এ trading name লাইন আর registered office।

Preview page এ `js/analytics.js` নেই, তাই preview তে GA বা cookie চলে না। Live করার সময় ওটা আবার যোগ হবে।
