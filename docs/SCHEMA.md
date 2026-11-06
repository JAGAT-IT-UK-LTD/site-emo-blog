# SCHEMA, EarningMoneyOnline

Database নেই। সব তথ্য repo র file এ।

| Entity | কোথায় | Field |
| --- | --- | --- |
| Article | `articles/<slug>.html` | title (h1), category (`span.tag`), published date (byline), cover ছবি, description (meta), পড়ার মিনিট |
| Category | `categories/<slug>.html` | নাম, এক লাইনের বর্ণনা, article card এর তালিকা |
| Search index | `preview/assets/search.json`, বানায় `tools/build-preview.py` | u file, t title, c category, d তারিখ, i ছবি, x ছোট বর্ণনা, r মিনিট |
| পুরনো registry | `data/articles.json` | পুরনো, 51টা article, 16 Aug 2026 এর পরে update হয়নি |

সম্পর্ক: একটা article এর একটা category। এখনকার category page এ তালিকা হাতে লেখা। নতুন design এ তালিকা আসে article file থেকে, তাই কোনো article বাদ পড়ে না।

ক্রম: search index আর category তালিকা তারিখ ধরে নতুন থেকে পুরনো।

Migration: নতুন design live এর সময় generator সব page এর header, footer আর CSS বদলাবে। Article এর মূল লেখা হুবহু থাকবে, URL একই থাকবে।

কতদিন রাখা: সবসময়, git history সহ।

ব্যক্তিগত তথ্য: নেই। GA4 এর data Google এ, consent সহ।
