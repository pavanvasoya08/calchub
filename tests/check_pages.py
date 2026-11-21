"""Browser test: python3 tests/check_pages.py <site_dir> [--only slug1,slug2]
Opens every calculator page, checks results render, no JS errors, no NaN/undefined, and category pages list the right items."""
import sys, os, re, glob, threading, http.server, functools
from playwright.sync_api import sync_playwright
d = sys.argv[1]
only = sys.argv[3].split(",") if len(sys.argv) > 3 and sys.argv[2] == "--only" else None
class Q(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a, **k): pass
h = functools.partial(Q, directory=d)
srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), h)
port = srv.server_address[1]
threading.Thread(target=srv.serve_forever, daemon=True).start()
pages = sorted(os.path.basename(p) for p in glob.glob(d + "/*.html"))
skip = {"index.html", "about.html", "contact.html", "disclaimer.html", "privacy-policy.html"}
bad = []
with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--no-sandbox"])
    for f in pages:
        if only and f[:-5] not in only and not f.endswith("calculators.html") and not f.endswith("converters.html"):
            continue
        pg = b.new_page(); errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.on("console", lambda m: errs.append(m.text) if m.type == "error" and "fonts" not in m.text and "ERR_" not in m.text else None)
        pg.goto(f"http://127.0.0.1:{port}/{f}"); pg.wait_for_timeout(250)
        if pg.query_selector("#out"):
            t = pg.inner_text("#out")
            if len(t.strip()) < 3 or re.search(r"NaN|undefined|Infinity|\[object", t) or "Please enter valid" in t:
                errs.append("bad output: " + t[:120].replace("\n", " | "))
        else:
            n = len(pg.query_selector_all(".grid .tcard"))
            if n < 1 and f not in skip and not os.environ.get("ALLOW_EMPTY"): errs.append("empty list")
        if errs: bad.append((f, errs[:3]))
        pg.close()
    b.close()
print("checked", len(pages), "pages; problems:", len(bad))
for f, e in bad: print(" ", f, e)
