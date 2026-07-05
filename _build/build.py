#!/usr/bin/env python3
"""Quoti Consulting static site builder.
Created By: iTechSmart Inc.

Usage:  python3 _build/build.py
Wraps each body in _build/pages/*.html with _build/template.html,
injecting per-page SEO meta + JSON-LD, and writes the result to the repo root.
"""
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
BASE = "https://quoticonsulting.com"

ORG = {
    "@type": "ProfessionalService",
    "@id": BASE + "/#organization",
    "name": "Quoti Consulting",
    "url": BASE + "/",
    "logo": BASE + "/assets/img/logo-mark.svg",
    "image": BASE + "/assets/img/og-image.png",
    "slogan": "Rooted in strong business foundations. Rising through strategic growth.",
    "description": "Small-business consulting firm led by a former IRS Revenue Agent: business audits, accounting system setup, compliance, business credit, funding readiness, SOPs and strategic growth planning.",
    "email": "hello@quoticonsulting.com",
    "priceRange": "$99 - $1,500+",
    "areaServed": {"@type": "Country", "name": "United States"},
    "founder": {
        "@type": "Person",
        "@id": BASE + "/about.html#shonya",
        "name": "Shonya Williams",
        "jobTitle": "Founder & Business Strategist",
        "description": "Business strategist, former IRS Revenue Agent (Small Business/Self-Employed Division), accountant, veteran and business consultant.",
        "worksFor": {"@id": BASE + "/#organization"},
    },
    "sameAs": [],
}

WEBSITE = {
    "@type": "WebSite",
    "@id": BASE + "/#website",
    "url": BASE + "/",
    "name": "Quoti Consulting",
    "publisher": {"@id": BASE + "/#organization"},
}


def offer(name, price, unit=None, description=""):
    o = {
        "@type": "Offer",
        "name": name,
        "price": price,
        "priceCurrency": "USD",
        "description": description,
        "seller": {"@id": BASE + "/#organization"},
    }
    if unit:
        o["priceSpecification"] = {
            "@type": "UnitPriceSpecification",
            "price": price,
            "priceCurrency": "USD",
            "unitText": unit,
        }
    return o


SERVICES_CATALOG = {
    "@type": "OfferCatalog",
    "name": "Quoti Consulting Services",
    "itemListElement": [
        offer("Business Overview Audit™", "99", None, "Flat-fee whole-business diagnostic with written report, foundation score and 90-day roadmap."),
        offer("Business Health Assessment™", "297", None, "Deep financial and operational health assessment with corrective action plan. Starting price."),
        offer("Business Foundation Audit™", "497", None, "Full structural audit of entity, compliance, contracts and operations. Starting price."),
        offer("Accounting System Setup", "750", None, "Accounting software configuration, chart of accounts, workflows and training. Starting price."),
        offer("Business Credit Readiness", "997", None, "Business credit profile building and tradeline strategy. Starting price."),
        offer("Funding Readiness", "1297", None, "Lender-ready financial package and funding strategy. Starting price."),
        offer("SOP Development", "997", None, "Documented standard operating procedures library. Starting price."),
        offer("Strategic Growth Planning", "1500", None, "12-month growth strategy grounded in your financials. Starting price."),
        offer("Business Coaching", "350", "MONTH", "Monthly 1:1 business coaching and accountability."),
        offer("Ascend Growth Program™", "500", "MONTH", "Flagship membership: coaching, strategy and the Quoti AOS™ operating system."),
    ],
}


def faq(pairs):
    return {
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in pairs
        ],
    }


def breadcrumbs(*items):
    return {
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": name, "item": BASE + "/" + path}
            for i, (name, path) in enumerate(items)
        ],
    }


PAGES = {
    "index.html": {
        "title": "Quoti Consulting | Business Foundations, Audits, Credit & Growth Strategy",
        "desc": "Build better businesses with Quoti Consulting: $99 Business Overview Audit™, accounting systems, compliance, business credit, funding readiness and strategic growth — led by a former IRS Revenue Agent.",
        "keywords": "business consulting, small business audit, business overview audit, former IRS revenue agent consultant, accounting system setup, business credit readiness, funding readiness, SOP development, strategic growth planning, business coaching",
        "active": "HOME",
        "jsonld": [ORG | {"hasOfferCatalog": SERVICES_CATALOG}, WEBSITE, faq([
            ("What is the $99 Business Overview Audit™?", "A flat-fee, whole-business diagnostic covering entity setup, books, compliance, credit profile and operations, delivered as a written report with a foundation score and a 90-day priority roadmap, reviewed 1:1."),
            ("Why does a former IRS Revenue Agent's perspective matter?", "Founder Shonya Williams worked in the IRS Small Business/Self-Employed Division, so client foundations are built to the standard examiners and lenders actually use."),
            ("What is Quoti AOS™?", "The Accountant Operating System — Quoti's proprietary framework of dashboards, reporting, compliance calendars, SOP libraries, client management and growth planning tools."),
            ("What industries does Quoti Consulting serve?", "Professional services, law firms, real estate, healthcare, construction, restaurants, nonprofits, government contractors, retail and service businesses."),
        ])],
    },
    "about.html": {
        "title": "About Shonya Williams — Former IRS Revenue Agent & Business Strategist | Quoti Consulting",
        "desc": "Meet Shonya Williams: founder of Quoti Consulting, business strategist, former IRS Revenue Agent (Small Business/Self-Employed Division), accountant and veteran. Mission, vision and story.",
        "keywords": "Shonya Williams, former IRS revenue agent, business strategist, veteran owned business consultant, accountant consultant, Quoti Consulting founder",
        "active": "ABOUT",
        "jsonld": [ORG, breadcrumbs(("Home", "index.html"), ("About", "about.html"))],
    },
    "services.html": {
        "title": "Services & Pricing — From the $99 Audit to Ascend Growth Program™ | Quoti Consulting",
        "desc": "Transparent consulting pricing: Business Overview Audit™ $99, Health Assessment from $297, Foundation Audit from $497, Accounting Setup from $750, Credit & Funding Readiness, SOPs, Growth Planning, Coaching and the Ascend Growth Program™ $500/mo.",
        "keywords": "business audit pricing, business health assessment, business foundation audit, accounting system setup cost, business credit readiness, funding readiness service, SOP development, strategic growth planning, business coaching pricing, Ascend Growth Program",
        "active": "SERVICES",
        "jsonld": [ORG | {"hasOfferCatalog": SERVICES_CATALOG},
                   breadcrumbs(("Home", "index.html"), ("Services", "services.html")),
                   faq([
                       ("Why do Quoti Consulting prices say 'from'?", "Scope varies with business size and complexity; listed prices are genuine starting points and every engagement gets a written quote before work begins."),
                       ("Can Quoti Consulting services be bundled?", "Yes — most clients follow the Diagnose, Build, Fund, Grow sequence and bundled roadmaps are discounted; the Ascend Growth Program™ bundles the full system for $500/month."),
                   ])],
    },
    "industries.html": {
        "title": "Industries We Serve — Law, Real Estate, Construction, Healthcare & More | Quoti Consulting",
        "desc": "Specialized business consulting for professional services, law firms, real estate, healthcare, construction, restaurants, nonprofits, government contractors, retail and service businesses.",
        "keywords": "law firm consulting, construction accounting consultant, restaurant business consultant, nonprofit consulting, government contractor accounting, real estate business consulting, healthcare practice consulting, retail business consultant",
        "active": "INDUSTRIES",
        "jsonld": [ORG, breadcrumbs(("Home", "index.html"), ("Industries", "industries.html"))],
    },
    "quoti-aos.html": {
        "title": "Quoti AOS™ — The Accountant Operating System | Quoti Consulting",
        "desc": "Quoti AOS™ is Quoti Consulting's proprietary Accountant Operating System: live dashboards, plain-English reporting, compliance calendars, SOP libraries, client management and growth planning in one system.",
        "keywords": "Quoti AOS, accountant operating system, business dashboards, compliance calendar, SOP library software, small business operating system, financial reporting system",
        "active": "AOS",
        "jsonld": [ORG, {
            "@type": "Product",
            "name": "Quoti AOS™ — Accountant Operating System",
            "brand": {"@id": BASE + "/#organization"},
            "description": "Proprietary operating system for small-business back offices: dashboards, reporting, compliance, SOPs, client management and growth planning. Included in the Ascend Growth Program™.",
            "offers": offer("Ascend Growth Program™ (includes Quoti AOS™)", "500", "MONTH"),
        }, breadcrumbs(("Home", "index.html"), ("Quoti AOS", "quoti-aos.html"))],
    },
    "quoti-live.html": {
        "title": "Quoti Live — 10,000 Free Inspirational Quotes, No Subscription | Quoti Consulting",
        "desc": "Quoti Live: 10,000 original quotes across 20 balanced categories — motivation, success, business, love, discipline and more. Quote of the day, search, favorites, shareable image cards. Free forever; optional $1 or custom donation.",
        "keywords": "free quotes, quote of the day, inspirational quotes free, motivational quotes no subscription, business quotes, daily wisdom, quote generator, Quoti Live, donation supported quotes",
        "active": "LIVE",
        "jsonld": [ORG, {
            "@type": "WebApplication",
            "name": "Quoti Live",
            "url": BASE + "/quoti-live.html",
            "applicationCategory": "LifestyleApplication",
            "operatingSystem": "Any (web)",
            "description": "Free quote platform with 10,000 original quotes in 20 balanced categories: quote of the day, random quotes, full-text search, favorites and downloadable quote image cards. No subscription — supported by optional $1 or custom donations.",
            "isAccessibleForFree": True,
            "offers": {
                "@type": "Offer",
                "price": "0",
                "priceCurrency": "USD",
                "description": "Free forever. Optional donation from $1 or a custom amount.",
            },
            "publisher": {"@id": BASE + "/#organization"},
        }, breadcrumbs(("Home", "index.html"), ("Quoti Live", "quoti-live.html")),
           faq([
               ("Is Quoti Live free?", "Yes — all 10,000 quotes, search, favorites, sharing and image downloads are free with no account or subscription. An optional donation of $1 or any custom amount supports the project."),
               ("How many quotes does Quoti Live have?", "10,000 original quotes, perfectly balanced across 20 categories — exactly 500 quotes in each category, including motivation, success, wisdom, leadership, business, money, discipline, courage, resilience, growth, happiness, love, friendship, family, health, mindfulness, creativity, time, change and gratitude."),
           ])],
    },
    "resources.html": {
        "title": "Free Business Resources — Checklists, Guides & Templates | Quoti Consulting",
        "desc": "Free small-business tools: Business Startup Checklist, Business Health Assessment, Funding Readiness Checklist, Business Credit Guide, SOP Starter Guide, Tax Checklist and Monthly Business Review template.",
        "keywords": "business startup checklist, funding readiness checklist, business credit guide, SOP template, small business tax checklist, monthly business review template, free business resources",
        "active": "RESOURCES",
        "jsonld": [ORG, breadcrumbs(("Home", "index.html"), ("Resources", "resources.html"))],
    },
    "blog.html": {
        "title": "The Quoti Growth Journal — Business Strategy, Finance & Compliance Blog | Quoti Consulting",
        "desc": "Weekly articles on business strategy, accounting, finance, compliance, leadership, business credit, funding, operations and entrepreneurship — from the team behind the $99 Business Overview Audit™.",
        "keywords": "small business blog, business strategy articles, accounting tips blog, business credit articles, funding advice, compliance blog, Quoti Growth Journal",
        "active": "BLOG",
        "jsonld": [ORG, {
            "@type": "Blog",
            "name": "The Quoti Growth Journal",
            "url": BASE + "/blog.html",
            "publisher": {"@id": BASE + "/#organization"},
            "description": "Weekly articles on business strategy, accounting, finance, compliance, leadership, business credit, funding, operations and entrepreneurship.",
        }, breadcrumbs(("Home", "index.html"), ("Blog", "blog.html"))],
    },
    "podcast.html": {
        "title": "Building Better Businesses with Shonya Williams — Podcast | Quoti Consulting",
        "desc": "Weekly podcast conversations on business foundations, financial leadership, IRS insights, business systems, funding, SOPs, leadership and entrepreneur success stories, hosted by Shonya Williams.",
        "keywords": "business podcast, Shonya Williams podcast, Building Better Businesses podcast, IRS insights podcast, small business finance podcast, entrepreneur success stories",
        "active": "PODCAST",
        "jsonld": [ORG, {
            "@type": "PodcastSeries",
            "name": "Building Better Businesses with Shonya Williams",
            "url": BASE + "/podcast.html",
            "description": "Weekly conversations about business foundations, financial leadership, IRS insights, business systems, funding, SOPs, leadership and entrepreneur success stories.",
            "publisher": {"@id": BASE + "/#organization"},
        }, breadcrumbs(("Home", "index.html"), ("Podcast", "podcast.html"))],
    },
    "client-portal.html": {
        "title": "Client Portal — Secure Documents, Messaging & Scheduling | Quoti Consulting",
        "desc": "The Quoti Consulting client portal: secure document uploads, intake forms, messaging, reports, invoices, scheduling and task tracking for active clients.",
        "keywords": "Quoti client portal, secure document upload, consulting client portal, client intake forms, consulting invoices",
        "active": "PORTAL",
        "jsonld": [ORG, breadcrumbs(("Home", "index.html"), ("Client Portal", "client-portal.html"))],
    },
    "contact.html": {
        "title": "Contact & Book a Consultation | Quoti Consulting",
        "desc": "Book a business consultation with Quoti Consulting or start your $99 Business Overview Audit™. Virtual consultations nationwide; replies within one business day.",
        "keywords": "book business consultation, contact Quoti Consulting, business audit booking, small business consultant contact",
        "active": "CONTACT",
        "jsonld": [ORG, {
            "@type": "ContactPage",
            "url": BASE + "/contact.html",
            "name": "Contact Quoti Consulting",
        }, breadcrumbs(("Home", "index.html"), ("Contact", "contact.html"))],
    },
}

NAV_KEYS = ["HOME", "ABOUT", "SERVICES", "INDUSTRIES", "AOS", "LIVE", "RESOURCES", "BLOG", "PODCAST", "PORTAL", "CONTACT"]


def build():
    template = (ROOT / "_build" / "template.html").read_text()
    for filename, meta in PAGES.items():
        body = (ROOT / "_build" / "pages" / filename).read_text()
        url = BASE + "/" + ("" if filename == "index.html" else filename)
        jsonld = json.dumps({"@context": "https://schema.org", "@graph": meta["jsonld"]},
                            ensure_ascii=False, separators=(",", ":"))
        html = (template
                .replace("{{TITLE}}", meta["title"])
                .replace("{{DESC}}", meta["desc"])
                .replace("{{KEYWORDS}}", meta["keywords"])
                .replace("{{URL}}", url)
                .replace("{{BASE}}", BASE)
                .replace("{{JSONLD}}", jsonld)
                .replace("{{CONTENT}}", body))
        for key in NAV_KEYS:
            html = html.replace("{{ACTIVE_%s}}" % key,
                                ' aria-current="page"' if meta["active"] == key else "")
        (ROOT / filename).write_text(html)
        print("built", filename)


if __name__ == "__main__":
    build()
