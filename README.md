# Quoti Consulting — Website

> *Rooted in strong business foundations. Rising through strategic growth.*

Premium marketing site for **Quoti Consulting** (Shonya Williams — Business Strategist, Former IRS Revenue Agent, Accountant, Veteran).

**Created By: iTechSmart Inc.**

## Highlights

- **10 pages** — Home, About, Services, Industries, Quoti AOS, Resources, Blog, Podcast, Client Portal, Contact
- **Light & dark modes** — dark-luxe gold default, ivory light theme; toggle in the header, persisted in `localStorage`, respects `prefers-color-scheme`
- **Conversion-funnel design** — $99 Business Overview Audit™ tripwire, Ascend Growth Program™ flagship, lead-capture forms, CTA bands on every page
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

Set your production domain in `_build/build.py` (`BASE`), `sitemap.xml`, `robots.txt` and `llms.txt` before launch (currently `https://quoticonsulting.com`).

The contact/lead forms are front-end ready (`data-quoti-form`); wire them to your form backend (Formspree, Netlify Forms, HubSpot, etc.) by adding an `action`/fetch handler in `assets/js/main.js`.

---

© Quoti Consulting. Site design & build — **Created By: iTechSmart Inc.**
