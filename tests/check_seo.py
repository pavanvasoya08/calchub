"""Static SEO validation: python3 tests/check_seo.py <site_dir>"""
import sys, os, re, glob, json, collections
from html.parser import HTMLParser
d = sys.argv[1]; BASE = "https://pavanvasoya08.github.io/calchub"
files = sorted(glob.glob(d + "/*.html")); names = {os.path.basename(f) for f in files} | {"style.css","app.js","index.js","og-image.png","sitemap.xml","robots.txt"}
titles = collections.defaultdict(list); descs = collections.defaultdict(list); errs = []
class P(HTMLParser):
    def __init__(s): super().__init__(); s.h = collections.Counter(); s.links = []; s.ids = collections.Counter(); s.labels = set(); s.inputs = []; s.imgs = 0; s.noalt = 0
    def handle_starttag(s, t, a):
        a = dict(a)
        if re.fullmatch(r"h[1-6]", t): s.h[t] += 1
        if t == "a" and "href" in a: s.links.append(a["href"])
        if "id" in a: s.ids[a["id"]] += 1
        if t == "label" and "for" in a: s.labels.add(a["for"])
        if t in ("input", "select", "textarea") and a.get("type") not in ("checkbox", "hidden"): s.inputs.append((a.get("id"), a.get("aria-label")))
        if t == "img":
            s.imgs += 1
            if "alt" not in a: s.noalt += 1
for f in files:
    n = os.path.basename(f); h = open(f, encoding="utf-8").read(); p = P(); p.feed(h)
    t = re.search(r"<title>(.*?)</title>", h).group(1); titles[t].append(n)
    m = re.search(r'<meta name="description" content="(.*?)">', h); descs[m.group(1) if m else ""].append(n)
    can = re.search(r'<link rel="canonical" href="(.*?)">', h).group(1)
    exp = BASE + "/" + ("" if n == "index.html" else n)
    if can != exp and n != "404.html": errs.append((n, "canonical", can))
    robots = re.search(r'name="robots" content="(.*?)"', h).group(1)
    if "noindex" in robots and n != "404.html": errs.append((n, "noindex"))
    if p.h["h1"] != 1: errs.append((n, "h1 count", p.h["h1"]))
    if len(t) > 65: errs.append((n, "title long", len(t)))
    if not m or not (50 <= len(m.group(1)) <= 160): errs.append((n, "desc length", len(m.group(1)) if m else 0))
    for need in ('og:title', 'og:description', 'og:image', 'twitter:card', 'theme-color', 'lang="en"', 'charset', 'viewport'):
        if need not in h: errs.append((n, "missing", need))
    for k, v in p.ids.items():
        if v > 1: errs.append((n, "dup id", k))
    for i, al in p.inputs:
        if i not in p.labels and not al: errs.append((n, "unlabelled input", i))
    for l in p.links:
        if l.startswith(("http", "mailto", "data:")): continue
        tgt = l.split("#")[0]
        if tgt and tgt not in names: errs.append((n, "broken link", l))
    if p.noalt: errs.append((n, "img without alt"))
    for blk in re.findall(r'<script type="application/ld\+json">(.*?)</script>', h):
        try:
            j = json.loads(blk)
            types = [x["@type"] for x in j["@graph"]]
            if len(types) != len(set(types)): errs.append((n, "duplicate schema types", types))
            for x in j["@graph"]:
                for u in re.findall(r'"(https://pavanvasoya08[^"]*)"', json.dumps(x)):
                    pass
            if "ratingValue" in blk or "aggregateRating" in blk: errs.append((n, "invented rating"))
            if n not in ("index.html",) and not n.endswith("calculators.html") and not n.endswith("converters.html") and n not in ("about.html","contact.html","disclaimer.html","privacy-policy.html","404.html"):
                if "FAQPage" in types:
                    q = [x for x in j["@graph"] if x["@type"] == "FAQPage"][0]["mainEntity"]
                    for e in q:
                        if e["name"] not in re.sub(r"&amp;", "&", h).replace("&#x27;", "'").replace("&quot;", '"') and e["name"].replace("&", "&amp;") not in h: errs.append((n, "FAQ not visible", e["name"][:40]))
        except Exception as e: errs.append((n, "bad json-ld", str(e)[:60]))
for k, v in titles.items():
    if len(v) > 1: errs.append(("DUP TITLE", k, v[:4]))
for k, v in descs.items():
    if len(v) > 1: errs.append(("DUP DESC", k[:60], v[:4]))
sm = open(d + "/sitemap.xml").read(); locs = re.findall(r"<loc>(.*?)</loc>", sm)
exp = {BASE + "/" + ("" if os.path.basename(f) == "index.html" else os.path.basename(f)) for f in files if not f.endswith("404.html")}
if set(locs) != exp: errs.append(("sitemap mismatch", sorted(exp ^ set(locs))[:5]))
rb = open(d + "/robots.txt").read()
if "Sitemap: " + BASE + "/sitemap.xml" not in rb or "Disallow: /" in rb.replace("Disallow: /\n", "X") and False: errs.append(("robots", rb))
print("pages", len(files), "sitemap urls", len(locs), "problems", len(errs))
for e in errs[:40]: print(" ", e)
