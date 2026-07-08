# Calculate My Hours — Project Handoff

**Site:** timespancalculator.com  
**Date:** July 1, 2026  

---

## What Was Built

A two-tool, ad-supported, fully client-side web utility for calculating time durations:

- **Bulk Spreadsheet Calculator** (`index.html`) — upload an .xlsx, .xls, .ods, or .csv file, map your start/end columns, and get four metrics appended as new columns in a downloaded file
- **Single Timespan Calculator** (`calculator.html`) — enter a start/end date and time manually and get instant results in the browser

Both tools produce four metrics: **Total Hours**, **Business Hours**, **Weekend Hours**, and **Weekday Hours** — each configurable (custom weekend days, custom business hour window).

Supporting pages: `about.html`, `contact.html`, `privacy-policy.html`, `sitemap.xml`, `favicon.svg`, `og-image.png`.

---

## Technical Stack

- **Zero backend.** Pure HTML + inline React (CDN) + SheetJS. No Node, no build step, no server.
- **SheetJS** handles all spreadsheet read/write in the browser.
- **Google Tag Manager** (GTM-KHFL7GXX) + GA4 (G-Z34JNQVYD2) for analytics.
- **Google AdSense** (ca-pub-4664800783455318) for monetization — leaderboard top, sidebars, and bottom strip.
- **Fonts:** Space Grotesk (display), Inter (body), JetBrains Mono (numbers).
- Structured data (JSON-LD WebApplication/AboutPage/ContactPage) on every page.

---

## Lessons Learned

**Static-first is the right call for a free ad-supported tool.** No hosting costs beyond a domain, no server maintenance, nothing to break. The entire app fits in a few HTML files.

**Two separate pages = two SEO entry points.** `index.html` targets "excel hours calculator / bulk spreadsheet" queries; `calculator.html` targets "hours between two dates" queries. Splitting them was the right call — each page can rank for a distinct intent.

**Flexible time input reduces abandonment.** Accepting 9:30, 21:30, and 2130 (military) with an AM/PM toggle that auto-detects format lowers friction significantly. Users paste times in whatever format they have them.

**Three-column ad layout works but sidebars are thin.** The 180px left sidebar is narrow enough that AdSense can struggle to fill it with quality ads. Desktop layouts monetize well; mobile collapses sidebars correctly (no wasted space).

**SheetJS date serialization is a gotcha.** Excel stores dates as numeric serials. When reading timestamps from uploaded files, you need to explicitly convert with SheetJS's `SSF.parse_date_code` or `XLSX.SSF` — raw cell values are not JS Date objects.

**Configurable options (weekend days, business hours window) are a differentiator.** Most competitors assume Mon–Fri, 9–5. Letting users set their own window makes the tool more universally useful and reduces edge-case complaints.

---

## Potential Next Steps

### High Impact, Low Effort

**Timezone selector on the single calculator.** Right now both tools assume local time. A simple UTC offset picker (or `Intl.supportedValuesOf('timeZone')` dropdown) would make the tool useful for teams working across time zones. This is probably the #1 user request type.

**Holidays exclusion from business hours.** Let users select a country/region and automatically exclude public holidays from business hour calculations. Even a hardcoded US federal holidays list would cover a large portion of users.

**Copy-to-clipboard on the single calculator.** Add a copy button next to each result so users can paste into Slack, email, etc. without typing the number.

**Permalink/shareable URL for single calculations.** Encode start/end/config into the URL hash so users can share a pre-filled calculation. No backend needed.

### New Features

**More calculators to broaden the site.** The brand ("Calculate My Hours") can support related tools — a shift duration calculator, a countdown timer, a payroll hours calculator by employee. Each new page = new SEO surface area.

**CSV/text export from the single calculator.** Let users download a single-row result file from the single calculator — useful when they need to paste into a report template.

**EU date format support.** DD/MM/YYYY input is common outside the US. Right now the tool may confuse formats. Auto-detecting separator order or offering a format toggle would reduce international friction.

**"How to use" demo.** A short embedded GIF or a 3-step visual guide on `index.html` would lower the learning curve for the spreadsheet tool, which has more steps (upload → map columns → download).

### SEO / Content

**A blog or resource section.** Articles like "How to calculate business hours in Excel" or "What counts as business hours in different countries" would pull long-tail search traffic and link to the tools as the solution. Even 4–5 articles would meaningfully expand organic reach.

**Google Search Console monitoring.** Set up GSC if not already done to track which queries are actually sending traffic. The two-page split may be surfacing unexpected keyword opportunities worth doubling down on.

**FAQ schema on calculator pages.** Adding FAQ structured data (common questions like "does this include holidays?" or "what time zones are supported?") can capture featured snippet positions.

### Tech Debt / Maintenance

**Lazy-load SheetJS on the single calculator.** The single calculator (`calculator.html`) doesn't need SheetJS at all — it's pure date math. Removing or deferring that dependency would improve page load on mobile.

**Consolidate shared HTML.** Header, footer, nav, and font preloads are copy-pasted across all four pages. If the site grows, a simple templating script (or even a build step with Vite) would make updates less error-prone.

**Ad slot audit.** There are currently ~3 AdSense placements per page. Once traffic grows, test Auto Ads to see if Google finds better placements than the hardcoded slots.

---

## Key Files Reference

| File | Purpose |
|------|---------|
| `index.html` | Bulk spreadsheet calculator (main tool) |
| `calculator.html` | Single timespan calculator |
| `about.html` | About page with ad layout |
| `contact.html` | Contact page |
| `privacy-policy.html` | Privacy policy page |
| `sitemap.xml` | Search engine sitemap (auto-generated by `generate_sitemap.py`) |
| `favicon.svg` | SVG favicon (bar chart motif) |
| `og-image.png` | Social share image (1200×630) |
