"""Responsive test: python3 tests/check_mobile.py <site_dir> [widths...] -> horizontal overflow, clipped/overlapping bits, small touch targets."""
import sys, os, glob, threading, http.server, functools, json
from playwright.sync_api import sync_playwright
d = sys.argv[1]; W = [int(x) for x in sys.argv[2:]] or [320,360,375,390,414,768,1024,1280,1440]
class Q(http.server.SimpleHTTPRequestHandler):
    def log_message(self,*a): pass
srv = http.server.ThreadingHTTPServer(("127.0.0.1",0),functools.partial(Q,directory=d)); port = srv.server_address[1]
threading.Thread(target=srv.serve_forever,daemon=True).start()
pages = sorted(os.path.basename(p) for p in glob.glob(d+"/*.html") if not p.endswith("404.html"))
JS = """()=>{const de=document.documentElement,vw=de.clientWidth,r=[];
if(de.scrollWidth>vw+1)r.push('page overflow '+de.scrollWidth+'>'+vw);
const bad=[];document.querySelectorAll('body *').forEach(e=>{const b=e.getBoundingClientRect();if(!b.width)return;
 if(b.right>vw+1&&!e.closest('.cat-row,.tblwrap,.sres,.menu,textarea,pre,.hidden,details.dd')){const cs=getComputedStyle(e);if(cs.position!=='fixed'&&bad.length<3)bad.push((e.className||e.tagName)+':'+Math.round(b.right))}});
if(bad.length)r.push('wide: '+bad.join(', '));
document.querySelectorAll('.tblwrap').forEach(t=>{if(t.scrollWidth>t.clientWidth&&getComputedStyle(t).overflowX==='visible')r.push('table not scrollable')});
if(vw<=480){document.querySelectorAll('.btn,input:not([type=checkbox]),select,.fld.chk label').forEach(e=>{if(e.closest('.hidden')||!e.offsetParent)return;const b=e.getBoundingClientRect();if(b.height<30&&r.length<6&&!e.classList.contains('sm'))r.push('small target '+(e.id||e.className))})}
const fs=getComputedStyle(document.body).fontSize;if(parseFloat(fs)<14)r.push('body font '+fs);
return r}"""
bad = {}
with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/usr/bin/google-chrome",args=["--no-sandbox"])
    for w in W:
        pg = b.new_page(viewport={"width":w,"height":800})
        for f in pages:
            pg.goto(f"http://127.0.0.1:{port}/{f}"); pg.wait_for_timeout(60)
            r = pg.evaluate(JS)
            if r: bad.setdefault(w,[]).append((f,r))
        pg.close()
    b.close()
print("widths",W,"pages",len(pages))
for w,v in bad.items():
    print(w,"->",len(v),"pages with issues")
    for f,r in v[:8]: print("  ",f,r)
if not bad: print("no issues")
