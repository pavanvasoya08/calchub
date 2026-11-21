import argparse, datetime, re
import argparse, datetime, glob, importlib, json, os, re, shutil, sys
from urllib.parse import quote
ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)
from assets_css import CSS
import core
from core import CALCS, CATEGORIES, CAT, CAT_INDEX, SITE_NAME, DOMAIN, CONTACT_EMAIL, CUR, LOCALE, fmt, emi_f
from icons import svg

# ====== AdSense (fill in after approval) ======
ADSENSE_CLIENT = ""   # e.g. "ca-pub-1234567890123456"
AD_SLOT = ""          # your ad unit slot id
# ==============================================
YEAR = 2026
FONT = ('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
        '<link href="https://fonts.googleapis.com/css2?family=Sora:wght@400;500;600;700&display=swap" rel="stylesheet">')
POPULAR = ["emi-calculator", "sip-calculator", "gst-calculator", "bmi-calculator", "percentage-calculator", "age-calculator"]


def esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def ad():
    if ADSENSE_CLIENT and AD_SLOT:
        return (f'<div class="ad live"><ins class="adsbygoogle" style="display:block" data-ad-client="{ADSENSE_CLIENT}" '
                f'data-ad-slot="{AD_SLOT}" data-ad-format="auto" data-full-width-responsive="true"></ins>'
                '<script>(adsbygoogle=window.adsbygoogle||[]).push({});</script></div>')
    return '<div class="ad">Advertisement</div>'

def in_cat(key):
    """calculators listed on a category page: primary first, then cross-listed."""
    return [c for c in CALCS if c["cat"] == key] + [c for c in CALCS if key in c["also"]]

def card(c, small=False):
    k = CAT_INDEX[c["cat"]]
    return (f'<a class="tcard{" cardsm" if small else ""}" href="{c["slug"]}.html"><div class="im k{k}"><span class="t">{esc(CAT[c["cat"]]["name"].split(" &")[0])}</span><span class="ib">{svg(c["icon"])}</span></div>'
            f'<div class="bd"><b>{esc(c["name"])}</b><small>{esc(c["short"])}</small><span class="go">Open calculator →</span></div></a>')

def nav_html(cur=""):
    def col(cats):
        return '<div class="mcol">' + "".join(f'<a href="{c["page"]}.html"{" class=on" if c["page"] + ".html" == cur else ""}>{esc(c["name"])}</a>' for c in cats) + "</div>"
    h = len(CATEGORIES) // 2
    return ('<nav class="main" aria-label="Main"><a href="index.html">Home</a><details class="dd"><summary>Categories</summary>'
            f'<div class="menu">{col(CATEGORIES[:h])}{col(CATEGORIES[h:])}</div></details>'
            '<a href="index.html#all">All calculators</a></nav>')

def page(title, desc, fname, body, calc="", head="", schema="", home=False, tail=""):
    adsense = (f'<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={ADSENSE_CLIENT}" crossorigin="anonymous"></script>'
               if ADSENSE_CLIENT else "")
    url = f"{DOMAIN}/" + ("" if fname == "index.html" else fname)
    by = {c["slug"]: c for c in CALCS}
    foot_links = "".join(f'<a href="{s}.html">{by[s]["name"]}</a>' for s in POPULAR if s in by)
    cat_links = "".join(f'<a href="{c["page"]}.html">{esc(c["name"])}</a>' for c in CATEGORIES)
    cta = (f'''<section class="cta"><div class="badge"><div>{len(CALCS)}+<small>CALCULATORS</small></div></div><div class="wrap"><h2>Make smarter decisions with {SITE_NAME}</h2>
<p>From loans and investments to health, dates and everyday conversions. Pick a calculator and get your answer in seconds.</p><a class="btn" href="#all">Browse all calculators</a></div></section>''' if home else "")
    return f'''<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="robots" content="index,follow,max-image-preview:large">
<meta name="theme-color" content="#fdf6ee">
<link rel="canonical" href="{url}">
<meta property="og:site_name" content="{SITE_NAME}"><meta property="og:locale" content="en_IN"><meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(desc)}"><meta property="og:type" content="website"><meta property="og:url" content="{url}"><meta property="og:image" content="{DOMAIN}/og-image.png"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="{SITE_NAME} - free online calculators">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{esc(title)}"><meta name="twitter:description" content="{esc(desc)}"><meta name="twitter:image" content="{DOMAIN}/og-image.png">
{FONT}<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 32 32%27%3E%3Crect width=%2732%27 height=%2732%27 rx=%276%27 fill=%27%238bb494%27/%3E%3Ctext x=%2716%27 y=%2723%27 font-size=%2720%27 font-family=%27sans-serif%27 font-weight=%27700%27 fill=%27white%27 text-anchor=%27middle%27%3EC%3C/text%3E%3C/svg%3E"><link rel="stylesheet" href="style.css">
{adsense}{head}{schema}
</head><body data-calc="{calc}" data-cur="{CUR}" data-loc="{LOCALE}">
<a class="skip" href="#main">Skip to content</a>
<header class="top"><div class="wrap"><a class="logo" href="index.html"><span class="lg">C</span>alcHub</a>
{nav_html(fname)}
<div class="hsearch"><input id="hq" type="text" placeholder="Search calculators" aria-label="Search calculators" autocomplete="off"><div class="sres hidden" id="hres"></div></div></div></header>
{body}
{cta}
<footer class="foot{'' if home else ' pt'}"><div class="wrap"><div class="fbox">
<div><a class="logo" href="index.html"><span class="lg">C</span>alcHub</a><p>Free, fast and private online calculators for money, health, math, dates, units and everyday life.</p></div>
<div><h4>Popular</h4>{foot_links}</div><div><h4>Categories</h4>{cat_links}</div>
<div><h4>Company</h4><a href="about.html">About</a><a href="contact.html">Contact</a><a href="privacy-policy.html">Privacy Policy</a><a href="disclaimer.html">Disclaimer</a></div></div>
<div class="copy">© {YEAR} {SITE_NAME}. All rights reserved.</div></div></footer>
<script src="index.js"></script><script src="app.js"></script>{tail}
</body></html>'''

def ld(*objs):
    return '<script type="application/ld+json">' + json.dumps({"@context": "https://schema.org", "@graph": list(objs)}, ensure_ascii=False, separators=(",", ":")) + "</script>"

def faq_obj(faqs):
    return {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]}

def crumb_obj(items):
    return {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": n, "name": nm, "item": u} for n, (nm, u) in enumerate(items, 1)]}

APPCAT = {"finance": "FinanceApplication", "health": "HealthApplication", "math": "EducationalApplication", "education": "EducationalApplication",
          "business": "BusinessApplication", "datetime": "UtilitiesApplication", "units": "UtilitiesApplication",
          "construction": "UtilitiesApplication", "shopping": "UtilitiesApplication", "tech": "UtilitiesApplication"}

NOTES = {
 "finance": ["Results use standard formulas and the values you enter. Banks, brokers and tax authorities may apply fees, rounding rules or different compounding, so real figures can differ.",
             "Interest rates, tax slabs and investment returns change over time. Market-linked returns (SIP, mutual funds, stocks) are not guaranteed.",
             "This tool is for estimation and learning. It is not financial, tax or investment advice."],
 "health": ["Results are general estimates based on population formulas and do not replace a medical examination.",
            "Age, genetics, muscle mass, medical conditions and medication can all change what is healthy for you.",
            "This calculator is for information only and is not medical advice. Please consult a doctor or a registered dietitian before making health decisions."],
 "math": ["The calculator follows standard mathematical definitions. Very large or very small numbers may be shown rounded.",
          "Check that your inputs use the units or format the tool asks for (for example, a percentage entered as 12, not 0.12)."],
 "education": ["Grading rules differ between boards, universities and countries. Use your institution's official conversion where one exists.",
               "Results are for guidance and do not replace an official marksheet or transcript."],
 "business": ["Results depend on the costs, prices and fee rates you enter. Marketplace fees, GST and platform rules change often, so confirm current rates with the platform or your accountant.",
              "Figures are estimates for planning and are not accounting, tax or legal advice."],
 "datetime": ["Dates use the Gregorian calendar and your device's local time zone unless the tool says otherwise.",
              "Public holidays differ by country and state, so holiday-based results only count the holidays you enter."],
 "units": ["Conversions use standard factors and are rounded for display. Use more precise figures for engineering or scientific work.",
           "Some units (such as gallons or bigha) differ by country or region. The tool states which definition it uses."],
 "construction": ["Quantities are theoretical estimates. Real projects need extra for wastage, site conditions and design changes.",
                  "Rates for materials, labour, stamp duty and registration vary by city and change often. Confirm with your contractor, engineer or the local registration office."],
 "shopping": ["Prices, taxes and tariffs differ from shop to shop and state to state. Enter the actual figures from your bill or price tag.",
              "Results are estimates for comparing options and are not a substitute for an official bill."],
 "tech": ["Real-world speeds, file sizes and compression vary from the theoretical values used here.",
          "Text and password tools run entirely in your browser. Nothing you type is uploaded or stored."],
}

def labels_of(fields):
    out = re.findall(r'<label[^>]*for="[^"]+"[^>]*>(.*?)</label>', fields)
    out += [re.sub(r"<[^>]+>", "", m).strip() for m in re.findall(r'<label>\s*<input[^>]*type="checkbox"[^>]*>(.*?)</label>', fields)]
    return [re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", l)).strip() for l in out if l.strip()]

def topic_of(name):
    return re.sub(r"\s+(Calculator|Converter)$", "", name)

def keywords(c):
    name = c["name"].lower()
    t = topic_of(c["name"]).lower()
    kind = "converter" if name.endswith("converter") else "calculator"
    sec = [f"free {name}", f"{name} online", f"{t} formula", f"how to calculate {t}" if kind == "calculator" else f"how to convert {t}",
           f"{t} with example", f"{t} step by step", f"best {name}", f"{name} no sign up"]
    if c["cat"] in ("finance", "business", "construction", "shopping"):
        sec.append(f"{name} India")
    if kind == "converter":
        sec.append(f"{t} chart")
    return name, sec

def seo_title(c):
    t = f"{c['name']} – Free Online Tool | {SITE_NAME}"
    return t if len(t) <= 62 else f"{c['name']} | {SITE_NAME}"

def seo_desc(c):
    d = f"{c['lead'].rstrip('.')}. Free online {c['name'].lower()} with instant results, formula and worked example."
    if len(d) > 158:
        d = f"{c['lead'].rstrip('.')}. Free, instant and accurate."
    return d[:158]

SHARE_PAGES = {"emi-calculator"}   # pilot: social sharing only on these calculator pages
SHARE_ICONS = {
 "wa": "M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413Z",
 "fb": "M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z",
 "x": "M18.901 1.153h3.68l-8.04 9.19L24 22.846h-7.406l-5.8-7.584-6.638 7.584H.474l8.6-9.83L0 1.154h7.594l5.243 6.932ZM17.61 20.644h2.039L6.486 3.24H4.298Z",
 "li": "M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z",
 "tg": "M11.944 0A12 12 0 0 0 0 12a12 12 0 0 0 12 12 12 12 0 0 0 12-12A12 12 0 0 0 12 0a12 12 0 0 0-.056 0zm4.962 7.224c.1-.002.321.023.465.14a.506.506 0 0 1 .171.325c.016.093.036.306.02.472-.18 1.898-.962 6.502-1.36 8.627-.168.9-.499 1.201-.82 1.23-.696.065-1.225-.46-1.9-.902-1.056-.693-1.653-1.124-2.678-1.8-1.185-.78-.417-1.21.258-1.91.177-.184 3.247-2.977 3.307-3.23.007-.032.014-.15-.056-.212s-.174-.041-.249-.024c-.106.024-1.793 1.14-5.061 3.345-.48.33-.913.49-1.302.48-.428-.008-1.252-.241-1.865-.44-.752-.245-1.349-.374-1.297-.789.027-.216.325-.437.893-.663 3.498-1.524 5.83-2.529 6.998-3.014 3.332-1.386 4.025-1.627 4.476-1.635z"}

def share_html(url, title, desc):
    u, t = quote(url, safe=""), quote(title, safe="")
    msg = quote(f"{title} {url}", safe="")
    links = [("wa", "WhatsApp", f"https://wa.me/?text={msg}"),
             ("fb", "Facebook", f"https://www.facebook.com/sharer/sharer.php?u={u}"),
             ("x", "X", f"https://twitter.com/intent/tweet?text={t}&url={u}"),
             ("li", "LinkedIn", f"https://www.linkedin.com/sharing/share-offsite/?url={u}"),
             ("tg", "Telegram", f"https://t.me/share/url?url={u}&text={t}")]
    a = "".join(f'<a class="{k}" href="{esc(h)}" target="_blank" rel="noopener noreferrer nofollow" aria-label="Share on {n}"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="{SHARE_ICONS[k]}"/></svg>{n}</a>' for k, n, h in links)
    native = '<button type="button" class="ns" hidden><svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true"><path d="M4 12v7a1 1 0 001 1h14a1 1 0 001-1v-7M16 6l-4-4-4 4M12 2v14"/></svg>Share</button>'
    cp = '<button type="button" class="cp"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M10 13a5 5 0 007.07 0l3-3a5 5 0 00-7.07-7.07l-1.5 1.5"/><path d="M14 11a5 5 0 00-7.07 0l-3 3a5 5 0 007.07 7.07l1.5-1.5"/></svg>Copy link</button>'
    return (f'<section class="share" aria-labelledby="sh-h" data-url="{esc(url)}" data-title="{esc(title)}" data-text="{esc(desc)}"><h2 id="sh-h">Share this calculator</h2>'
            f'<div class="sb">{native}{a}{cp}</div><p class="msg" role="status" aria-live="polite"></p></section>')

def calc_page(c):
    inc = in_cat(c["cat"])
    same = [x for x in inc if x["slug"] != c["slug"]]
    pos = [y["slug"] for y in inc].index(c["slug"]) if c["slug"] in [y["slug"] for y in inc] else 0
    if same:
        same = same[pos % len(same):] + same[:pos % len(same)]
    rel = "".join(f'<a href="{r["slug"]}.html">{svg(r["icon"])}{esc(r["name"])}</a>' for r in same[:8])
    faqs = list(c["faqs"]) + [(f"Is this {c['name'].lower()} free to use?", f"Yes. The {c['name'].lower()} is free, needs no sign-up and runs in your browser, so the numbers you enter are not sent to a server.")]
    faq = "".join(f"<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>" for q, a in faqs)
    cat = CAT[c["cat"]]
    k = CAT_INDEX[c["cat"]]
    labs = labels_of(c["fields"])
    shown = ", ".join(f"<b>{esc(l)}</b>" for l in labs[:6]) + (f" and {len(labs) - 6} more option(s)" if len(labs) > 6 else "")
    steps = ([f"<li>Fill in {shown}.</li>"] if labs else ["<li>Enter your values in the fields above.</li>"]) + [
        "<li>Every field starts with an example value. Replace it with your own numbers or keep it to see how the tool works.</li>",
        "<li>Read the result panel. It updates instantly as you type, so there is no button to press.</li>",
        "<li>Change one value at a time to compare scenarios. Nothing is saved or sent anywhere.</li>"]
    notes = "".join(f"<li>{esc(n)}</li>" for n in NOTES[c["cat"]])
    extra = (f'<h2>How to use the {esc(c["name"])}</h2><ol>{"".join(steps)}</ol>'
             f'<h2>Assumptions and limitations</h2><ul>{notes}</ul>')
    url = f"{DOMAIN}/{c['slug']}.html"
    title, desc = seo_title(c), seo_desc(c)
    schema = ld(
        {"@type": "WebPage", "@id": url + "#webpage", "url": url, "name": title, "description": desc, "inLanguage": "en", "isPartOf": {"@id": DOMAIN + "/#website"},
         "breadcrumb": {"@id": url + "#breadcrumb"}, "mainEntity": {"@id": url + "#app"}},
        {"@type": "WebApplication", "@id": url + "#app", "name": c["name"], "url": url, "description": desc, "applicationCategory": APPCAT[c["cat"]],
         "operatingSystem": "Any (web browser)", "browserRequirements": "Requires JavaScript", "inLanguage": "en", "isAccessibleForFree": True,
         "offers": {"@type": "Offer", "price": "0", "priceCurrency": "INR"}, "publisher": {"@id": DOMAIN + "/#org"}},
        crumb_obj([("Home", DOMAIN + "/"), (cat["name"], f"{DOMAIN}/{cat['page']}.html"), (c["name"], url)]) | {"@id": url + "#breadcrumb"},
        faq_obj(faqs))
    body = f'''<main id="main" class="wrap"><div class="main-col"><nav class="crumbs" aria-label="Breadcrumb"><a href="index.html">Home</a> › <a href="{cat["page"]}.html">{esc(cat["name"])}</a> › <span>{esc(c["name"])}</span></nav>
<div class="phead k{k}"><div class="pi">{svg(c["icon"])}</div><div><h1 class="pt">{esc(c["h1"])}</h1><p class="lead">{esc(c["lead"])}</p></div></div>
{ad()}
<section class="box" id="calc" aria-label="{esc(c["name"])}"><div class="row">{c["fields"]}</div><div class="res" id="out" aria-live="polite"></div></section>{share_html(url, c["name"] + " | " + SITE_NAME, desc) if c["slug"] in SHARE_PAGES else ""}
{ad()}
<article class="txt">{c["body"]}{extra}<h2>Frequently asked questions</h2>{faq}
<h2>Related calculators</h2><div class="chips">{rel}</div><p style="margin-top:14px"><a class="link" href="{cat["page"]}.html">View all {esc(cat["name"])} calculators →</a></p></article>
{ad()}</div></main>'''
    shared = c["slug"] in SHARE_PAGES
    return page(title, desc, c["slug"] + ".html", body, c["js"], c["head"] + ('<link rel="stylesheet" href="share.css">' if shared else ""), schema,
                tail='<script src="share.js" defer></script>' if shared else "")

def category_page(cat):
    k = CAT_INDEX[cat["key"]]
    items = in_cat(cat["key"])
    cards = "".join(card(c, True) for c in items)
    desc = "".join(f"<p>{esc(p)}</p>" for p in cat["desc"])
    faq = "".join(f"<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>" for q, a in cat["faqs"])
    others = "".join(f'<a href="{o["page"]}.html">{svg(o["icon"])}{esc(o["name"])}</a>' for o in CATEGORIES if o["key"] != cat["key"])
    body = f'''<main id="main" class="wrap"><div class="main-col wide"><nav class="crumbs" aria-label="Breadcrumb"><a href="index.html">Home</a> › <span>{esc(cat["name"])}</span></nav>
<div class="phead k{k}"><div class="pi">{svg(cat["icon"])}</div><div><h1 class="pt">Free {esc(cat["name"])} Calculators</h1><p class="lead">{len(items)} free calculators. {esc(cat["short"])}.</p></div></div>
{ad()}
<div class="catfilter"><input id="q" type="text" placeholder="Search in {esc(cat["name"])}" aria-label="Search" autocomplete="off"><div class="sres hidden" id="qres"></div></div>
<div class="grid">{cards}</div>
{ad()}
<article class="txt">{desc}<h2>Frequently asked questions</h2>{faq}<h2>Other categories</h2><div class="chips">{others}</div></article>
{ad()}</div></main>'''
    t = f"Free {cat['name']} Calculators – {SITE_NAME}"
    d = f"{len(items)} free online {cat['name'].lower()} calculators. " + cat["short"] + ". Instant, accurate and no sign-up."
    curl = f"{DOMAIN}/{cat['page']}.html"
    schema = ld({"@type": "CollectionPage", "@id": curl + "#webpage", "url": curl, "name": t, "description": d, "inLanguage": "en", "isPartOf": {"@id": DOMAIN + "/#website"}, "breadcrumb": {"@id": curl + "#breadcrumb"}},
                crumb_obj([("Home", DOMAIN + "/"), (cat["name"], curl)]) | {"@id": curl + "#breadcrumb"},
                {"@type": "ItemList", "name": cat["name"] + " calculators", "numberOfItems": len(items),
                 "itemListElement": [{"@type": "ListItem", "position": n, "name": x["name"], "url": f"{DOMAIN}/{x['slug']}.html"} for n, x in enumerate(items, 1)]},
                faq_obj(cat["faqs"]))
    return page(t, d, cat["page"] + ".html", body, schema=schema)

def home():
    e = emi_f(2500000, 8.75, 20)
    i = 0.01
    sip = 10000 * ((1 + i) ** 180 - 1) / i * (1 + i)
    by = {c["slug"]: c for c in CALCS}
    pop = "".join(card(by[s]) for s in POPULAR if s in by)
    strip = "".join(f'<a href="{by[s]["slug"]}.html">{svg(by[s]["icon"])}{esc(by[s]["name"].replace(" Calculator", ""))}</a>' for s in POPULAR if s in by)
    catcards = "".join(
        f'<a class="cat k{CAT_INDEX[c["key"]]}" href="{c["page"]}.html"><div class="ico">{svg(c["icon"])}</div><div><b>{esc(c["name"])}</b><small>{len(in_cat(c["key"]))} calculators</small></div></a>'
        for c in CATEGORIES)
    secs = ""
    for c in CATEGORIES:
        items = in_cat(c["key"])
        secs += (f'<section class="catsec" id="{c["key"]}"><div class="sh"><h3>{svg(c["icon"])}{esc(c["name"])}</h3><a class="link" href="{c["page"]}.html">View all {len(items)} →</a></div>'
                 f'<div class="grid">{"".join(card(x, True) for x in items)}</div></section>')
    feats = [("bolt", "k2", "Instant results", "Answers update as you type. No buttons, no waiting."),
             ("book", "k4", "Formulas explained", "Every calculator shows how the result is worked out, with an example."),
             ("lock", "k1", "Private by design", "Your numbers stay in your browser and are never sent to a server."),
             ("phone", "k3", "Works everywhere", "Clean layout that works on phones, tablets and computers.")]
    fh = "".join(f'<div class="feat"><div class="fi {k}">{svg(ic)}</div><b>{t}</b><p>{d}</p></div>' for ic, k, t, d in feats)
    n = len(CALCS)
    body = f'''<main id="main">
<section class="hero2"><div class="wrap hero-grid"><div class="hero-l">
<span class="pill"><svg viewBox="0 0 24 24" width="14" height="14" fill="#222"><path d="M12 2l2.2 7.8L22 12l-7.8 2.2L12 22l-2.2-7.8L2 12l7.8-2.2z"/></svg>Free · No sign-up · {n} calculators</span>
<h1>Find the right <em>calculator</em> for every decision</h1>
<p>Finance, health, math, dates, units, property and more. Get accurate answers in seconds, with the formula explained.</p>
<div class="hero-cta"><a class="btn" href="#all">Start Calculating</a><a class="link" href="emi-calculator.html">Try the EMI calculator →</a></div></div>
<div class="hero-r"><svg class="dots" viewBox="0 0 60 16" width="60" height="16" fill="none" stroke="#222" stroke-width="1.6" stroke-linecap="round"><path d="M2 2l8 8M10 2l-8 8M24 2l8 8M32 2l-8 8M46 2l8 8M54 2l-8 8"/></svg>
<div class="fc fc1"><span class="tag">EMI · Example</span><small>Monthly EMI</small><b>{fmt(e)}</b><small>{fmt(2500000)} · 8.75% · 20 years</small><div class="mini"><i style="width:62%"></i></div></div>
<div class="fc fc2"><small>BMI · Example</small><b>24.2</b><small>Normal weight</small></div>
<div class="fc fc3"><span class="tag">SIP · Example</span><small>Value after 15 years</small><b>{fmt(sip)}</b><small>{fmt(10000)} a month at 12%</small></div>
<div class="fc fc4"><small>GST · Example</small><b>{fmt(1180)}</b><small>{fmt(1000)} + 18%</small></div></div></div></section>
<div class="wrap">{('<div class="strip">' + strip + '</div>') if strip else ''}
<section class="cats"><div><h2>Explore calculator categories</h2><div class="arrows"><button id="catPrev" aria-label="Previous">←</button><button id="catNext" aria-label="Next">→</button></div></div><div class="cat-row" id="catRow">{catcards}</div></section>
<section class="demo"><h2>Try a calculator right here</h2><p>A quick EMI calculator. Change any value and see the result instantly.</p>
<div class="qe"><div class="row"><div class="fld"><label for="qp">Loan amount ({CUR})</label><input type="number" id="qp" value="1000000"></div><div class="fld"><label for="qr">Interest rate (% per year)</label><input type="number" id="qr" value="9" step="any"></div><div class="fld"><label for="qy">Tenure (years)</label><input type="number" id="qy" value="10"></div></div><div class="res" id="qout"></div></div>
<div class="panel"><div class="in"><div><h3>Fast answers, clear formulas, zero sign-ups</h3><a class="btn green" href="#all">Explore calculators</a></div>
<div><div class="nums"><div><b>{n}+</b>free calculators</div><div><b>{len(CATEGORIES)}</b>categories</div></div><span class="chip2">Every calculator explains its formula</span></div></div></div></section>
{ad()}
<section><div class="sh"><h2>Popular calculators</h2><a class="btn sm" href="#all">View all</a></div><div class="grid g3">{pop}</div></section></div>
<section class="band"><div class="wrap"><h2>Built to be simple and trustworthy</h2><p>No clutter, no confusing forms. Just the answer you need, with the working shown.</p><div class="feats">{fh}</div></div></section>
<div class="wrap"><section class="how"><div class="blobv"><div class="fc"><span class="tag">Result</span><small>Your monthly EMI</small><b>{fmt(e)}</b><small>Total interest {fmt(e*240-2500000)}</small><div class="mini"><i style="width:55%"></i></div></div></div>
<div><h2>How it works in 3 simple steps</h2>
<div class="step k4"><div class="si">1</div><div><b>Pick a calculator</b><p>Browse by category or search for the one you need.</p></div></div>
<div class="step k1"><div class="si">2</div><div><b>Enter your numbers</b><p>Fill in a few fields. Results update as you type.</p></div></div>
<div class="step k2"><div class="si">3</div><div><b>Read the answer and the formula</b><p>See the result, the breakdown and how it was worked out.</p></div></div></div></section>
<section class="all" id="all"><div class="sh"><h2>All calculators</h2><div class="search"><input id="q" type="text" placeholder="Search calculators (e.g. EMI, BMI, GST)" aria-label="Search calculators" autocomplete="off"><div class="sres hidden" id="qres"></div></div></div>{secs}</section>{ad()}</div></main>'''
    return page(f"{SITE_NAME} – Free Online Calculators for Finance, Health & More",
                f"{n} free online calculators: EMI, SIP, income tax, BMI, percentage, date difference, unit converters, construction and more. Instant, accurate, no sign-up.",
                "index.html", body, home=True, schema=ld(
        {"@type": "WebSite", "@id": DOMAIN + "/#website", "url": DOMAIN + "/", "name": SITE_NAME, "inLanguage": "en", "publisher": {"@id": DOMAIN + "/#org"}},
        {"@type": "Organization", "@id": DOMAIN + "/#org", "name": SITE_NAME, "url": DOMAIN + "/"},
        {"@type": "WebPage", "@id": DOMAIN + "/#webpage", "url": DOMAIN + "/", "name": SITE_NAME, "isPartOf": {"@id": DOMAIN + "/#website"}, "inLanguage": "en"},
        {"@type": "ItemList", "name": "Calculator categories", "numberOfItems": len(CATEGORIES),
         "itemListElement": [{"@type": "ListItem", "position": n, "name": c["name"], "url": f"{DOMAIN}/{c['page']}.html"} for n, c in enumerate(CATEGORIES, 1)]}))

def simple(slug, title, html):
    body = f'<main id="main" class="wrap"><div class="plain"><h1 class="pt" style="margin:40px 0 18px">{title}</h1><article class="txt">{html}</article></div></main>'
    desc = {"about": f"About {SITE_NAME}: free, fast and private online calculators for money, health, math, dates, units and everyday needs.",
            "contact": f"Contact {SITE_NAME} with questions, feedback or calculator requests. We read every message.",
            "disclaimer": f"{SITE_NAME} disclaimer: calculator results are estimates for information only and are not financial, tax, legal or medical advice.",
            "privacy-policy": f"{SITE_NAME} privacy policy: how calculator inputs, cookies, advertising and analytics are handled."}[slug]
    return page(f"{title} – {SITE_NAME}", desc, slug + ".html", body)

PAGES = {
 "about": ("About Us", f"<p>{SITE_NAME} is a collection of free online calculators for everyday money, health, math and conversion needs. Our goal is to give you a fast, clear answer along with the formula behind it.</p><p>All calculations run in your browser. We do not store the numbers you enter.</p><p>Spotted a mistake or have an idea for a new calculator? Please <a href=\"contact.html\"><u>contact us</u></a>.</p>"),
 "contact": ("Contact Us", f"<p>For questions, feedback or calculator requests, please email us:</p><p><b>{CONTACT_EMAIL}</b></p><p>We read every message and reply as soon as we can.</p>"),
 "disclaimer": ("Disclaimer", "<p>The calculators on this website are provided for general information and estimation only. Results for loans, investments, taxes, health and other topics may differ from figures given by banks, tax authorities, doctors or other professionals. Interest rates, tax rules and thresholds change over time, so please verify them from an official source.</p><p>Nothing on this site is financial, tax, legal or medical advice. Please consult a qualified professional before making important decisions. We are not responsible for any loss arising from the use of this website.</p>"),
 "privacy-policy": ("Privacy Policy", f"<p>Your privacy matters to us. This page explains how {SITE_NAME} handles information.</p><h2>Information you enter</h2><p>The numbers you type into our calculators are processed in your browser. They are not sent to or stored on our servers.</p><h2>Cookies and advertising</h2><p>We may show ads served by third-party vendors, including Google AdSense. These vendors may use cookies to show ads based on your previous visits to this and other websites. You can opt out of personalized advertising at <a href=\"https://adssettings.google.com\"><u>Google Ads Settings</u></a>.</p><h2>Analytics</h2><p>We may use analytics tools to collect anonymous usage information, such as pages visited, so we can improve the site.</p><h2>Contact</h2><p>For privacy questions, email {CONTACT_EMAIL}.</p><p>Last updated: {YEAR}</p>"),
}

EXTRA_CSS = r""".tcard .ib{width:62px;height:62px;border-radius:16px;background:rgba(255,255,255,.72);display:grid;place-items:center}.tcard .ib svg{width:30px;height:30px}
.cardsm .ib{width:48px;height:48px;border-radius:13px}.cardsm .ib svg{width:24px;height:24px}
.cat .ico svg{width:24px;height:24px}.feat .fi svg{width:22px;height:22px}.pi svg{width:30px;height:30px}
.strip a svg{width:22px;height:22px}.catsec h3{display:flex;align-items:center;gap:10px}.catsec h3 svg{width:22px;height:22px;color:var(--sage-d)}
.chips a{display:inline-flex;align-items:center;gap:7px}.chips a svg{width:15px;height:15px}
""" + ".foot.pt{padding-top:50px;margin-top:50px}\n.grid.g3{grid-template-columns:repeat(3,1fr)}\n.panel .in>div:first-child{text-align:left}\n.logo{gap:0}\n.dots{opacity:.7;left:40%;top:48%}.pill svg{flex:none}\n@media(max-width:600px){.hero-r{height:auto;display:grid;grid-template-columns:1fr 1fr;gap:12px}.hero-r .fc{position:static;width:auto;transform:none}.hero-r .dots{display:none}}\n@media(max-width:820px){.grid.g3{grid-template-columns:repeat(auto-fill,minmax(250px,1fr))}}\n"

def load_calcs(only):
    names = sorted(os.path.splitext(os.path.basename(p))[0] for p in glob.glob(os.path.join(ROOT, "calcs", "*.py")))
    for n in names:
        if n.startswith("_") or (only and n not in only):
            continue
        importlib.import_module("calcs." + n)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(ROOT, "docs"))
    ap.add_argument("--only", default="", help="comma separated calcs/ module names (for partial builds)")
    a = ap.parse_args()
    only = [x for x in a.only.split(",") if x]
    load_calcs(only)
    out = a.out
    if os.path.isdir(out):
        shutil.rmtree(out)
    os.makedirs(out)
    files = {"index.html": home()}
    for c in CALCS:
        files[c["slug"] + ".html"] = calc_page(c)
    for cat in CATEGORIES:
        files[cat["page"] + ".html"] = category_page(cat)
    for slug, (t, h) in PAGES.items():
        files[slug + ".html"] = simple(slug, t, h)
    files["style.css"] = CSS + EXTRA_CSS
    js = ""
    for p in sorted(glob.glob(os.path.join(ROOT, "js", "*.js"))):
        n = os.path.basename(p)
        if only and n not in ("00_head.js", "99_engine.js") and not any(n.split("_", 1)[1][:-3] == o for o in only):
            continue
        js += open(p, encoding="utf-8").read() + "\n"
    files["app.js"] = js
    idx = [[c["name"], c["slug"] + ".html", c["slug"].replace("-", " ") + " " + c["short"], CAT[c["cat"]]["name"], c["short"]] for c in CALCS]
    files["index.js"] = "window.IDX=" + json.dumps(idx, ensure_ascii=False) + ";"
    urls = [f"{DOMAIN}/"] + [f"{DOMAIN}/{k}" for k in files if k.endswith(".html") and k not in ("index.html", "404.html")]
    today = datetime.date.today().isoformat()
    cat_pages = {c["page"] + ".html" for c in CATEGORIES}
    def entry(u):
        home_ = u == f"{DOMAIN}/"
        leaf = u.rsplit("/", 1)[-1]
        legal = leaf in ("about.html", "contact.html", "disclaimer.html", "privacy-policy.html")
        pr = "1.0" if home_ else ("0.3" if legal else ("0.9" if leaf in cat_pages else "0.8"))
        return f"  <url>\n    <loc>{u}</loc>\n    <lastmod>{today}</lastmod>\n    <changefreq>{'weekly' if home_ else 'monthly'}</changefreq>\n    <priority>{pr}</priority>\n  </url>\n"
    files["sitemap.xml"] = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(entry(u) for u in urls) + "</urlset>\n"
    files["404.html"] = page(f"Page not found – {SITE_NAME}", "Sorry, the page you are looking for was not found on CalcHub. Browse our free online calculators from the home page.", "404.html",
        '<main id="main" class="wrap"><div class="plain"><h1 class="pt" style="margin:40px 0 18px">Page not found</h1><article class="txt"><p>Sorry, we could not find that page. Try the <a href="index.html"><u>home page</u></a> or pick a category from the menu.</p></article></div></main>'
    ).replace('<meta name="robots" content="index,follow,max-image-preview:large">', '<meta name="robots" content="noindex,follow">')
    files["robots.txt"] = f"User-agent: *\nAllow: /\nSitemap: {DOMAIN}/sitemap.xml\n"
    if ADSENSE_CLIENT:
        files["ads.txt"] = f"google.com, {ADSENSE_CLIENT.replace('ca-', '')}, DIRECT, f08c47fec0942fa0\n"
    kw = ["# CalcHub keyword mapping (generated by build.py)\n", "| Page | Primary keyword | Secondary / long-tail keywords |", "|---|---|---|"]
    for c in CALCS:
        p, sec = keywords(c)
        kw.append(f"| {c['slug']}.html | {p} | {'; '.join(sec)} |")
    if not only:
        with open(os.path.join(ROOT, "SEO_KEYWORDS.md"), "w", encoding="utf-8") as f:
            f.write("\n".join(kw) + "\n")
    for a_ in ("og-image.png", "share.css", "share.js"):
        with open(os.path.join(ROOT, "assets", a_), "rb") as f:
            files[a_] = f.read()
    for k, v in files.items():
        if isinstance(v, bytes):
            with open(os.path.join(out, k), "wb") as f:
                f.write(v)
            continue
        with open(os.path.join(out, k), "w", encoding="utf-8") as f:
            f.write(v)
    print(len(CALCS), "calculators,", len(files), "files ->", out)

if __name__ == "__main__":
    main()
