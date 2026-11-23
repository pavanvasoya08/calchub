from playwright.sync_api import sync_playwright
import threading,http.server,functools,json,urllib.request,sys
class Q(http.server.SimpleHTTPRequestHandler):
    def log_message(s,*a):pass
def serve(d):
    s=http.server.ThreadingHTTPServer(("127.0.0.1",0),functools.partial(Q,directory=d));threading.Thread(target=s.serve_forever,daemon=True).start();return s.server_address[1]
P=serve("/tmp/site_ask");P2=serve("/tmp/site_ask2")
rows=lambda port=8799:json.load(urllib.request.urlopen(f"http://127.0.0.1:{port}/rows"))
def fill(pg,name="Asha Patel",email="asha@example.com",cat="Calculation help",q="How is the EMI worked out for a 20 year loan?"):
    pg.fill('#ask-name',name);pg.fill('#ask-email',email);pg.select_option('#ask-cat',cat);pg.fill('#ask-question',q)
msg=lambda pg:pg.inner_text('#ask-msg').strip()
S='#ask-form button[type=submit]'
def fresh(ctx,port,wait=4300):
    pg=ctx.new_page();pg.goto(f"http://127.0.0.1:{port}/emi-calculator.html");pg.wait_for_timeout(wait);return pg
def ok(label,cond,extra=""):print(("PASS " if cond else "FAIL ")+label,extra)
with sync_playwright() as p:
    b=p.chromium.launch(executable_path="/usr/bin/google-chrome",args=["--no-sandbox"]);ctx=b.new_context(viewport={'width':1280,'height':900})
    errs=[]
    # too fast
    pg=fresh(ctx,P,300);pg.on("pageerror",lambda e:errs.append(str(e)));fill(pg);pg.click(S);pg.wait_for_timeout(700)
    ok("too-fast submit rejected, nothing stored",len(rows())==0 and "take a moment" in msg(pg),msg(pg))
    # success + sanitisation + loading
    pg=fresh(ctx,P);fill(pg,name="<b>Asha</b>  Patel",q="=HYPERLINK(\"http://evil\") <script>alert(1)</script> Is the EMI formula exact?");pg.click(S)
    ok("loading state shown",pg.is_disabled(S) and pg.inner_text(S)=="Sending...")
    pg.wait_for_timeout(900);r=rows()
    ok("success message",msg(pg).startswith("Thank you"),msg(pg));ok("one row stored",len(r)==1)
    row=r[0];print("   row:",row)
    ok("9 columns, status New",len(row)==9 and row[8]=="New");ok("ID format Q-YYYYMMDD-XXXXXX",__import__('re').fullmatch(r"Q-\d{8}-[0-9A-F]{6}",row[0]) is not None)
    ok("name/question sanitised (no tags)","<" not in row[2] and "<script" not in row[5],f"{row[2]!r} | {row[5]!r}")
    ok("calculator name + page URL stored",row[6]=="EMI Calculator" and row[7].endswith("/emi-calculator.html"))
    ok("form reset",pg.input_value('#ask-name')=="")
    # duplicate (same email + question, new page load / new token)
    pg=fresh(ctx,P);fill(pg,name="Asha",q="=HYPERLINK(\"http://evil\") <script>alert(1)</script> Is the EMI formula exact?");pg.click(S);pg.wait_for_timeout(900)
    ok("duplicate content not stored twice",len(rows())==1,msg(pg))
    # double click
    pg=fresh(ctx,P);fill(pg,email="rahul@example.com",name="Rahul",q="What is the difference between flat and reducing rate?");pg.dblclick(S);pg.wait_for_timeout(1000)
    ok("double click -> single row",len(rows())==2)
    # honeypot
    pg=fresh(ctx,P);fill(pg,email="bot@example.com",name="Bot",q="Buy cheap pills now at my website");pg.evaluate("document.getElementById('ask-web').value='http://spam'");pg.click(S);pg.wait_for_timeout(900)
    ok("honeypot: looks like success but not stored",len(rows())==2 and msg(pg).startswith("Thank you"))
    # rate limit: asha has 1 stored; 2 more ok, 4th blocked
    res=[]
    for i in range(3):
        pg=fresh(ctx,P);fill(pg,q=f"Rate limit test question number {i} here");pg.click(S);pg.wait_for_timeout(900);res.append(msg(pg)[:40])
    print("   rate limit replies:",res);ok("4th question from same email within the hour blocked",len(rows())==4 and "several questions" in res[2])
    # CORS-less redirect -> fallback path, still exactly one row
    pg=fresh(ctx,P2);fill(pg,email="fallback@example.com",name="Fallback",q="Testing the fallback when the reply cannot be read");pg.click(S);pg.wait_for_timeout(1500)
    ok("fallback path shows success, one row",msg(pg).startswith("Thank you") and len(rows(8798))==1 and len(rows(8798)[0])==9,msg(pg))
    # unreachable server
    pg=ctx.new_page();pg.route("**/exec",lambda r:r.abort());pg.goto(f"http://127.0.0.1:{P}/emi-calculator.html");pg.wait_for_timeout(4300);fill(pg,email="z@example.com",q="Network failure test question here");pg.click(S);pg.wait_for_timeout(1500)
    ok("network failure shows error and re-enables button","Could not send" in msg(pg) and not pg.is_disabled(S),msg(pg))
    o=fresh(ctx,P,100);o.goto(f"http://127.0.0.1:{P}/sip-calculator.html");ok("other calculator pages have no form",o.query_selector('#ask-form') is None)
    m=b.new_context(viewport={'width':375,'height':800});mp=fresh(m,P,300);ok("mobile: no horizontal overflow",not mp.evaluate("document.documentElement.scrollWidth>document.documentElement.clientWidth"))
    fill(mp);mp.locator('#ask').scroll_into_view_if_needed();mp.wait_for_timeout(4000);mp.click(S);mp.wait_for_timeout(1000);mp.locator('#ask').screenshot(path='/tmp/ask_m.png')
    d=fresh(ctx,P,300);d.locator('#ask').scroll_into_view_if_needed();d.locator('#ask').screenshot(path='/tmp/ask_d.png')
    ok("no JS errors",not errs,errs);b.close()
