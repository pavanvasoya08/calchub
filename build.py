import json, os, shutil, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from assets_css import CSS
from assets_js import JS
import content as K
from content import CALCS, CATS, SITE_NAME, DOMAIN, CONTACT_EMAIL, CUR, LOCALE, fmt
from icons import svg, SLUG as ICON_SLUG, CAT as ICON_CAT

# ====== AdSense (approval ke baad bharein) ======
ADSENSE_CLIENT = ""   # e.g. "ca-pub-1234567890123456"
AD_SLOT = ""          # your ad unit slot id
# ================================================
YEAR = 2026
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "docs")
CATIDX = {name: i + 1 for i, (name, _, _) in enumerate(CATS)}
CATSHORT = {K.FIN: "Loans", K.TAX: "Business", K.HEALTH: "Health", K.MATH: "Math", K.UNIT: "Units"}
FONT = ('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
        '<link href="https://fonts.googleapis.com/css2?family=Sora:wght@400;500;600;700&display=swap" rel="stylesheet">')


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def ad():
    if ADSENSE_CLIENT and AD_SLOT:
        return (f'<div class="ad live"><ins class="adsbygoogle" style="display:block" data-ad-client="{ADSENSE_CLIENT}" '
                f'data-ad-slot="{AD_SLOT}" data-ad-format="auto" data-full-width-responsive="true"></ins>'
                '<script>(adsbygoogle=window.adsbygoogle||[]).push({});</script></div>')
    return '<div class="ad">Advertisement</div>'

def card(c, small=False):
    k = CATIDX[c["cat"]]
    return (f'<a class="tcard{" cardsm" if small else ""}" href="{c["slug"]}.html"><div class="im k{k}"><span class="t">{CATSHORT[c["cat"]]}</span><span class="ib">{svg(ICON_SLUG[c["slug"]])}</span></div>'
            f'<div class="bd"><b>{esc(c["name"])}</b><small>{esc(c["short"])}</small><span class="go">Open calculator →</span></div></a>')

def page(title, desc, fname, body, calc="", head="", schema="", home=False):
    adsense = (f'<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={ADSENSE_CLIENT}" crossorigin="anonymous"></script>'
               if ADSENSE_CLIENT else "")
    url = f"{DOMAIN}/" + ("" if fname == "index.html" else fname)
    foot_links = "".join(f'<a href="{s}.html">{n}</a>' for s, n in [("emi-calculator", "EMI Calculator"), ("sip-calculator", "SIP Calculator"), ("gst-calculator", "GST Calculator"), ("bmi-calculator", "BMI Calculator"), ("percentage-calculator", "Percentage Calculator")])
    cat_links = "".join(f'<a href="index.html#{a}">{n}</a>' for n, _, a in CATS)
    cta = (f'''<section class="cta"><div class="badge"><div>{len(CALCS)}+<small>CALCULATORS</small></div></div><div class="wrap"><h2>Make smarter decisions with {SITE_NAME}</h2>
<p>From loans and investments to health and everyday math. Pick a calculator and get your answer in seconds.</p><a class="btn" href="#all">Browse all calculators</a></div></section>''' if home else "")
    return f'''<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{url}">
<meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(desc)}"><meta property="og:type" content="website"><meta property="og:url" content="{url}">
{FONT}<link rel="stylesheet" href="style.css">
{adsense}{head}{schema}
</head><body data-calc="{calc}" data-cur="{CUR}" data-loc="{LOCALE}">
<header class="top"><div class="wrap"><a class="logo" href="index.html"><span class="lg">C</span>alcHub</a>
<nav class="main"><a href="index.html">Home</a><a href="index.html#finance">Loans</a><a href="index.html#health">Health</a><a href="index.html#math">Math</a><a href="index.html#converters">Converters</a></nav>
<a class="btn sm" href="index.html#all">All calculators</a></div></header>
{body}
{cta}
<footer class="foot{'' if home else ' pt'}"><div class="wrap"><div class="fbox">
<div><a class="logo" href="index.html"><span class="lg">C</span>alcHub</a><p>Free, fast and private online calculators for money, health, math and everyday conversions.</p></div>
<div><h4>Popular</h4>{foot_links}</div><div><h4>Categories</h4>{cat_links}</div>
<div><h4>Company</h4><a href="about.html">About</a><a href="contact.html">Contact</a><a href="privacy-policy.html">Privacy Policy</a><a href="disclaimer.html">Disclaimer</a></div></div>
<div class="copy">© {YEAR} {SITE_NAME}. All rights reserved.</div></div></footer>
<script src="app.js"></script>
</body></html>'''

def calc_page(c):
    same = [x for x in CALCS if x["cat"] == c["cat"] and x["slug"] != c["slug"]]
    pos = [y["slug"] for y in CALCS if y["cat"] == c["cat"]].index(c["slug"])
    if same:
        same = same[pos % len(same):] + same[:pos % len(same)]
    rel = "".join(f'<a href="{r["slug"]}.html">{svg(ICON_SLUG[r["slug"]])}{esc(r["name"])}</a>' for r in same[:6])
    faq = "".join(f"<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>" for q, a in c["faqs"])
    schema = '<script type="application/ld+json">' + json.dumps({
        "@context": "https://schema.org", "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in c["faqs"]]},
        ensure_ascii=False) + "</script>"
    k = CATIDX[c["cat"]]
    anchor = next(a for n, _, a in CATS if n == c["cat"])
    body = f'''<main class="wrap"><div class="main-col"><div class="crumbs"><a href="index.html">Home</a> › <a href="index.html#{anchor}">{esc(c["cat"])}</a> › {esc(c["name"])}</div>
<div class="phead k{k}"><div class="pi">{svg(ICON_SLUG[c["slug"]])}</div><div><h1 class="pt">{esc(c["h1"])}</h1><p class="lead">{esc(c["lead"])}</p></div></div>
{ad()}
<section class="box" id="calc"><div class="row">{c["fields"]}</div><div class="res" id="out"></div></section>
{ad()}
<article class="txt">{c["body"]}<h2>Frequently asked questions</h2>{faq}
<h2>More calculators</h2><div class="chips">{rel}</div></article>
{ad()}</div></main>'''
    return page(c["title"], c["lead"], c["slug"] + ".html", body, c["js"], c["head"], schema)

def home():
    e = K.emi_f(2500000, 8.75, 20)
    i = 0.01
    sip = 10000 * ((1 + i) ** 180 - 1) / i * (1 + i)
    popular = ["emi-calculator", "sip-calculator", "gst-calculator", "bmi-calculator", "percentage-calculator", "compound-interest-calculator"]
    by = {c["slug"]: c for c in CALCS}
    pop = "".join(card(by[s]) for s in popular)
    strip = "".join(f'<a href="{s}.html">{svg(ICON_SLUG[s])}{n}</a>' for s, n in [("emi-calculator", "EMI"), ("sip-calculator", "SIP"), ("gst-calculator", "GST"), ("bmi-calculator", "BMI"), ("percentage-calculator", "Percentage"), ("age-calculator", "Age")])
    catcards = "".join(
        f'<a class="cat k{n}" href="#{a}"><div class="ico">{svg(ICON_CAT[name])}</div><div><b>{esc(name)}</b><small>{sum(1 for c in CALCS if c["cat"] == name)} calculators</small></div></a>'
        for n, (name, ic, a) in enumerate(CATS, 1))
    secs = ""
    for n, (name, ic, a) in enumerate(CATS, 1):
        items = "".join(card(c, True) for c in CALCS if c["cat"] == name)
        secs += f'<section class="catsec" id="{a}"><h3>{svg(ICON_CAT[name])}{esc(name)}</h3><div class="grid">{items}</div></section>'
    feats = [("bolt", "k2", "Instant results", "Answers update as you type. No buttons, no waiting."),
             ("book", "k4", "Formulas explained", "Every calculator shows how the result is worked out, with an example."),
             ("lock", "k1", "Private by design", "Your numbers stay in your browser and are never sent to a server."),
             ("phone", "k3", "Works everywhere", "Clean layout that works on phones, tablets and computers.")]
    fh = "".join(f'<div class="feat"><div class="fi {k}">{svg(ic)}</div><b>{t}</b><p>{d}</p></div>' for ic, k, t, d in feats)
    body = f'''<main>
<section class="hero2"><div class="wrap hero-grid"><div class="hero-l">
<span class="pill"><svg viewBox="0 0 24 24" width="14" height="14" fill="#222"><path d="M12 2l2.2 7.8L22 12l-7.8 2.2L12 22l-2.2-7.8L2 12l7.8-2.2z"/></svg>Free · No sign-up · {len(CALCS)} calculators</span>
<h1>Find the right <em>calculator</em> for every decision</h1>
<p>Loans, investments, tax, health, math and unit conversion. Get accurate answers in seconds, with the formula explained.</p>
<div class="hero-cta"><a class="btn" href="#all">Start Calculating</a><a class="link" href="emi-calculator.html">Try the EMI calculator →</a></div></div>
<div class="hero-r"><svg class="dots" viewBox="0 0 60 16" width="60" height="16" fill="none" stroke="#222" stroke-width="1.6" stroke-linecap="round"><path d="M2 2l8 8M10 2l-8 8M24 2l8 8M32 2l-8 8M46 2l8 8M54 2l-8 8"/></svg>
<div class="fc fc1"><span class="tag">EMI · Example</span><small>Monthly EMI</small><b>{fmt(e)}</b><small>{fmt(2500000)} · 8.75% · 20 years</small><div class="mini"><i style="width:62%"></i></div></div>
<div class="fc fc2"><small>BMI · Example</small><b>24.2</b><small>Normal weight</small></div>
<div class="fc fc3"><span class="tag">SIP · Example</span><small>Value after 15 years</small><b>{fmt(sip)}</b><small>{fmt(10000)} a month at 12%</small></div>
<div class="fc fc4"><small>GST · Example</small><b>{fmt(1180)}</b><small>{fmt(1000)} + 18%</small></div></div></div></section>
<div class="wrap"><div class="strip">{strip}</div>
<section class="cats"><div><h2>Explore calculator categories</h2><div class="arrows"><button id="catPrev" aria-label="Previous">←</button><button id="catNext" aria-label="Next">→</button></div></div><div class="cat-row" id="catRow">{catcards}</div></section>
<section class="demo"><h2>Try a calculator right here</h2><p>A quick EMI calculator. Change any value and see the result instantly.</p>
<div class="qe"><div class="row"><div class="fld"><label for="qp">Loan amount ({CUR})</label><input type="number" id="qp" value="1000000"></div><div class="fld"><label for="qr">Interest rate (% per year)</label><input type="number" id="qr" value="9" step="any"></div><div class="fld"><label for="qy">Tenure (years)</label><input type="number" id="qy" value="10"></div></div><div class="res" id="qout"></div></div>
<div class="panel"><div class="in"><div><h3>Fast answers, clear formulas, zero sign-ups</h3><a class="btn green" href="#all">Explore calculators</a></div>
<div><div class="nums"><div><b>{len(CALCS)}+</b>free calculators</div><div><b>0</b>sign-ups needed</div></div><span class="chip2">Every calculator explains its formula</span></div></div></div></section>
{ad()}
<section><div class="sh"><h2>Popular calculators</h2><a class="btn sm" href="#all">View all</a></div><div class="grid g3">{pop}</div></section></div>
<section class="band"><div class="wrap"><h2>Built to be simple and trustworthy</h2><p>No clutter, no confusing forms. Just the answer you need, with the working shown.</p><div class="feats">{fh}</div></div></section>
<div class="wrap"><section class="how"><div class="blobv"><div class="fc"><span class="tag">Result</span><small>Your monthly EMI</small><b>{fmt(e)}</b><small>Total interest {fmt(e*240-2500000)}</small><div class="mini"><i style="width:55%"></i></div></div></div>
<div><h2>How it works in 3 simple steps</h2>
<div class="step k4"><div class="si">1</div><div><b>Pick a calculator</b><p>Browse by category or search for the one you need.</p></div></div>
<div class="step k1"><div class="si">2</div><div><b>Enter your numbers</b><p>Fill in a few fields. Results update as you type.</p></div></div>
<div class="step k2"><div class="si">3</div><div><b>Read the answer and the formula</b><p>See the result, the breakdown and how it was worked out.</p></div></div></div></section>
<section class="all" id="all"><div class="sh"><h2>All calculators</h2><div class="search"><input id="q" type="text" placeholder="Search calculators… (e.g. EMI, BMI, GST)" aria-label="Search calculators"></div></div>{secs}</section>{ad()}</div></main>'''
    return page(f"{SITE_NAME} – Free Online Calculators: EMI, SIP, GST, BMI & More",
                f"Free online calculators: EMI, SIP, FD, GST, BMI, percentage, age, unit converters and more. {len(CALCS)} instant, accurate tools with no sign-up.",
                "index.html", body, home=True)

def simple(slug, title, html):
    body = f'<main class="wrap"><div class="plain"><h1 class="pt" style="margin:40px 0 18px">{title}</h1><article class="txt">{html}</article></div></main>'
    return page(f"{title} – {SITE_NAME}", title, slug + ".html", body)

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

def main():
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)
    files = {"index.html": home()}
    for c in CALCS:
        files[c["slug"] + ".html"] = calc_page(c)
    for slug, (t, h) in PAGES.items():
        files[slug + ".html"] = simple(slug, t, h)
    files["style.css"] = CSS + EXTRA_CSS
    files["app.js"] = JS
    urls = [f"{DOMAIN}/"] + [f"{DOMAIN}/{k}" for k in files if k.endswith(".html") and k != "index.html"]
    import datetime
    today = datetime.date.today().isoformat()
    def entry(u):
        home_ = u == f"{DOMAIN}/"
        legal = any(u.endswith(x) for x in ("about.html", "contact.html", "disclaimer.html", "privacy-policy.html"))
        pr = "1.0" if home_ else ("0.3" if legal else "0.8")
        return f"  <url>\n    <loc>{u}</loc>\n    <lastmod>{today}</lastmod>\n    <changefreq>{'weekly' if home_ else 'monthly'}</changefreq>\n    <priority>{pr}</priority>\n  </url>\n"
    files["sitemap.xml"] = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(entry(u) for u in urls) + "</urlset>\n"
    files["robots.txt"] = f"User-agent: *\nAllow: /\nSitemap: {DOMAIN}/sitemap.xml\n"
    if ADSENSE_CLIENT:
        files["ads.txt"] = f"google.com, {ADSENSE_CLIENT.replace('ca-', '')}, DIRECT, f08c47fec0942fa0\n"
    for k, v in files.items():
        with open(os.path.join(OUT, k), "w", encoding="utf-8") as f:
            f.write(v)
    print(len(CALCS), "calculators,", len(files), "files ->", OUT)

if __name__ == "__main__":
    main()
