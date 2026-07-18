# Quoti Consulting — Website

> *Rooted in strong business foundations. Rising through strategic growth.*

Premium marketing site for **Quoti Consulting** (Shonya Williams — Business Strategist, Former IRS Revenue Agent, Accountant, Veteran).

**Created By: [Quoti Consulting (https://Quoticonsulting.com)**

## Highlights

- **11 pages** — Home, About, Services, Industries, Quoti AOS, **Quoti Live**, Resources, Blog, Podcast, Client Portal, Contact
- **Quoti Live** (`quoti-live.html`) — free quote platform, no subscription: 10,000 original quotes perfectly balanced across 20 categories (500 each), quote of the day, random quote, full-text search, favorites (localStorage), copy/share, downloadable 1080×1080 quote image cards, and an optional **$1 / $3 / $5 / custom donation** model (set your payment handle in `DONATE_URL` at the top of `assets/js/quotes-app.js`; currently a PayPal.Me placeholder). Regenerate the quote library with `python3 _build/gen_quotes.py`.
- **Quoti brand system** — five signature colors (deep navy, royal blue, rich gold, soft purple, white) applied per the brand spec: navy hero/footer/AOS/contact bands, gold CTAs with navy text, royal secondary buttons and icons, purple sub-brand for Blog/Podcast/Quoti Live, blue-to-purple gradient CTA banners, gold statistics and focus rings
- **Light & dark modes** — dark-luxe gold default, ivory light theme; toggle in the header, persisted in `localStorage`, respects `prefers-color-scheme`
- **Conversion-funnel design** — $99 Business Overview Audit™ tripwire, Ascend Growth Program™ flagship, lead-capture forms, CTA bands on every page
- **Modern motion layer** — scroll parallax (logo watermarks & orbs), word-by-word blur-reveal headings, cursor spotlight on cards, 3D tilt on pricing/quote cards, magnetic gold buttons, scroll progress bar, smart hide-on-scroll header, CSS scroll-driven animations (`animation-timeline: view()`), marquee pause-on-hover — all dependency-free and `prefers-reduced-motion` safe
- **Rebuilt vector logo** — clean transparent SVG mark (`assets/img/logo-mark.svg`) + SVG/PNG favicons + social OG image
- **SEO / AIO / GEO / LLM ready** — per-page meta + canonical + Open Graph + Twitter cards, JSON-LD (`ProfessionalService`, `OfferCatalog` with all 10 priced services, `FAQPage`, `Person`, `PodcastSeries`, `Blog`, breadcrumbs), `sitemap.xml`, `robots.txt` with AI-crawler rules, and `llms.txt`
- **Self-hosted fonts** (Fraunces, Plus Jakarta Sans, JetBrains Mono) — no third-party requests, fast and private
- **Zero dependencies** — pure static HTML/CSS/JS; deploy the repo root to any static host (GitHub Pages, Netlify, Vercel, Cloudflare Pages)

## Structure

```
├── index.html … contact.html    # built pages (deploy these)
├── assets/css|js|img|fonts      # design system, behavior, logo/icons, fonts
├── _build/
│   ├── template.html            # shared head/header/footer shell
│   ├── pages/*.html             # per-page <main> content
│   └── build.py                 # compiles pages + injects SEO/JSON-LD
├── sitemap.xml · robots.txt · llms.txt · site.webmanifest
```

## Editing

Edit content in `_build/pages/`, page titles/descriptions/structured data in `_build/build.py`, then:

```bash
python3 _build/build.py
```

The production domain is set to `https://quoti.live` in `_build/build.py` (`BASE`), `sitemap.xml`, `robots.txt` and `llms.txt` — change it there if the site ever moves.

The contact/lead forms are front-end ready (`data-quoti-form`); wire them to your form backend (Formspree, Netlify Forms, HubSpot, etc.) by adding an `action`/fetch handler in `assets/js/main.js`.

---

© Quoti Consulting. Site design & build — **Created By: [Quoti Consulting LLC.](https://Quoticonsulting.com)**
