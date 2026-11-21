"""Shared config, field helpers, category list and the calculator registry.

Every module in calcs/ does:  from core import *   and then calls calc(...) for each calculator.
"""
import icons

# ================= CONFIG =================
SITE_NAME = "CalcHub"
DOMAIN = "https://pavanvasoya08.github.io/calchub"
CONTACT_EMAIL = "yourname@gmail.com"
CUR = "₹"            # currency symbol shown in results ("$", "£", "€" ...)
LOCALE = "en-IN"     # number format: "en-IN" (1,00,000) or "en-US" (100,000)
# ==========================================

# ---------- categories (order = order on the site) ----------
CATEGORIES = [
 dict(key="finance", name="Finance & Money", page="finance-calculators", icon="wallet", short="Loans, investments, tax & stocks",
      desc=["Plan your money with calculators for loans, EMIs, savings and investments. Work out what a home, car or personal loan will cost each month, see how a SIP or fixed deposit can grow, and estimate your income tax and take-home salary.",
            "Every calculator shows the formula behind the result, so you can understand the numbers and compare options with confidence. Results are estimates; always confirm exact figures with your bank, broker or tax adviser."],
      faqs=[("Are the finance calculators accurate?", "They use standard financial formulas and update instantly. Real offers can differ because of fees, taxes and rounding, so treat the results as a close estimate."),
            ("Do you store the numbers I enter?", "No. All calculations run in your browser and nothing you type is sent to a server."),
            ("Which finance calculator should I start with?", "Most people start with the EMI calculator for loans, the SIP calculator for investing and the income tax calculator for yearly planning.")]),
 dict(key="health", name="Health & Fitness", page="health-calculators", icon="heart", short="BMI, calories, water & more",
      desc=["Check your body mass index, daily calorie needs, ideal weight, body fat and more. These calculators also help with nutrition targets such as protein, water and macros, and with planning around sleep, cycles and pregnancy.",
            "They are general guides based on well-known formulas, not medical advice. Talk to a doctor or dietitian before making big changes to your diet, exercise or health routine."],
      faqs=[("Are these health calculators medical advice?", "No. They give general estimates from standard formulas. For personal medical advice, please consult a qualified doctor."),
            ("Why do BMI and body fat results differ?", "BMI only compares weight with height. Body fat estimates use body measurements, so the two can tell different stories, especially for athletic people."),
            ("How often should I recalculate?", "Every few weeks is enough. Daily changes in weight are mostly water and are not meaningful.")]),
 dict(key="math", name="Math", page="math-calculators", icon="divide", short="Percentage, fractions, ratios & more",
      desc=["Quick answers to everyday math: percentages, averages, fractions, ratios, square roots and probability, plus a full scientific calculator for harder problems.",
            "Each page explains the method and shows a worked example, which makes these calculators useful for checking homework as well as for daily use."],
      faqs=[("Can I use these for homework?", "Yes, they are great for checking your work. The formula and example on each page also help you learn the method."),
            ("How many decimal places are shown?", "Results are rounded to a sensible number of decimal places for readability.")]),
 dict(key="education", name="Education", page="education-calculators", icon="cap", short="CGPA, GPA, marks & grades",
      desc=["Convert CGPA to percentage and back, calculate your GPA, marks percentage and the grade you need on a final exam.",
            "These calculators follow commonly used formulas. Universities and boards can use different rules, so check your institution's official method for admissions or applications."],
      faqs=[("Is the CGPA to percentage formula official?", "The multiplier 9.5 is widely used (for example by CBSE), but your university or employer may use a different one. Always check the official rule."),
            ("Can I calculate a semester GPA?", "Yes. Enter your course credits and grades in the GPA calculator.")]),
 dict(key="business", name="Business & E-commerce", page="business-calculators", icon="briefcase", short="Margins, ROI, seller fees & more",
      desc=["Price products, protect your margins and measure returns. These calculators cover profit margin, markup, break-even, GST and VAT, ROI and ROAS, and marketplace seller fees for Amazon, Flipkart and your own online store.",
            "Marketplace fees and tax rates change often, so the fee calculators let you edit every rate. Check the latest rate card on your seller dashboard before you decide."],
      faqs=[("What is the difference between margin and markup?", "Margin is profit as a share of the selling price. Markup is profit as a share of the cost. A 25% markup equals a 20% margin."),
            ("Are the seller fee calculators exact?", "They are estimates built on rates you can edit. Marketplace fee structures change, so confirm the current rates in your seller account.")]),
 dict(key="datetime", name="Date & Time", page="date-time-calculators", icon="calendar", short="Age, dates, working days & time",
      desc=["Work out ages, the days between two dates, working days, deadlines and time differences. You can add or subtract days from a date, count down to an event and convert times between time zones.",
            "All date calculations use the standard calendar, including leap years. Working-day counts exclude weekends and any holidays you enter."],
      faqs=[("Do the calculators handle leap years?", "Yes. All date maths uses the real calendar, including leap years."),
            ("Are public holidays excluded from working days?", "Only weekends are excluded automatically. You can enter the number of holidays to subtract them too.")]),
 dict(key="units", name="Unit Converters", page="unit-converters", icon="ruler", short="Length, weight, temperature & more",
      desc=["Convert between units of length, weight, temperature, area, volume and digital storage in one step. Popular conversions such as cm to feet, kg to pounds and km to miles each have their own page.",
            "Conversions use exact or internationally accepted factors and are shown with plenty of decimal places."],
      faqs=[("How accurate are the conversions?", "They use exact or standard conversion factors, so results are accurate to many decimal places."),
            ("Why is a land unit like bigha different by state?", "The size of a bigha is not standard across India, so the land converters let you pick the state or enter your own value.")]),
 dict(key="construction", name="Construction & Property", page="construction-calculators", icon="building", short="Area, materials, stamp duty & rent",
      desc=["Plan a build or a property purchase. Calculate plot and carpet areas, estimate cement, concrete, bricks, paint and tiles, and work out construction costs, stamp duty and rent.",
            "Material quantities are estimates based on common thumb rules. Actual needs depend on design, site conditions and wastage, so ask your contractor or engineer before ordering."],
      faqs=[("Are material estimates exact?", "No. They follow standard thumb rules and include an allowance for wastage. Ask your contractor to confirm quantities."),
            ("Do stamp duty rates differ by state?", "Yes. Stamp duty and registration charges vary by state, so the calculator lets you enter your own rates.")]),
 dict(key="shopping", name="Shopping & Everyday", page="shopping-calculators", icon="cart", short="Discounts, bills, fuel & travel",
      desc=["Everyday calculators for smarter spending: discounts and final prices, unit price comparisons, cashback, splitting a bill, electricity and water bills, fuel cost, mileage and trip costs.",
            "They are made for quick use on your phone while you shop, travel or manage household expenses."],
      faqs=[("How do I compare two products fairly?", "Use the unit price or price comparison calculator. It divides each price by the quantity so you can see the cheapest per unit."),
            ("Are the bill calculators exact?", "Utility tariffs differ by provider, so the calculators use rates you enter. Check your latest bill for the correct values.")]),
 dict(key="tech", name="Technology & Digital", page="technology-calculators", icon="monitor", short="Download time, data, text & converters",
      desc=["Handy tools for everyday digital tasks: estimate download and upload times, calculate data usage and storage, convert binary, decimal and hexadecimal numbers, count words and characters, change text case and generate strong passwords.",
            "Everything runs in your browser. Text you type and passwords you generate are never sent anywhere."],
      faqs=[("Is the password generator safe?", "Passwords are created in your browser using your device's secure random number generator and are never sent to or stored on a server."),
            ("Is my text private?", "Yes. Word counters and text tools run locally in your browser.")]),
]
CAT = {c["key"]: c for c in CATEGORIES}
CAT_INDEX = {c["key"]: i + 1 for i, c in enumerate(CATEGORIES)}   # 1..10 -> colour class k1..k10


# ---------- number formatting for static page text (examples) ----------
def fmt(x, d=0):
    x = round(x, d)
    s = f"{abs(x):.{d}f}"
    ip, _, fp = s.partition(".")
    if LOCALE == "en-IN" and len(ip) > 3:
        h, rest, parts = ip[-3:], ip[:-3], []
        while len(rest) > 2:
            parts.insert(0, rest[-2:]); rest = rest[:-2]
        if rest: parts.insert(0, rest)
        ip = ",".join(parts + [h])
    else:
        ip = f"{int(ip):,}"
    return ("-" if x < 0 else "") + CUR + ip + ("." + fp if fp else "")

def nf(x, d=2):
    """plain number formatting for examples (no currency symbol)."""
    s = f"{x:,.{d}f}" if LOCALE != "en-IN" else fmt(x, d)[len(CUR):]
    return s

def emi_f(P, r, y):
    i, m = r / 1200, y * 12
    return P * i * (1 + i) ** m / ((1 + i) ** m - 1)


# ---------- form field helpers ----------
def _w(when):
    return f' data-when="{when}"' if when else ""

def num(id, label, val, when=None, step="any", min="0"):
    mn = f' min="{min}"' if min != "" else ""
    return f'<div class="fld"{_w(when)}><label for="{id}">{label}</label><input type="number" id="{id}" value="{val}" step="{step}"{mn}></div>'

def sel(id, label, opts, val=None, when=None):
    o = "".join(f'<option value="{k}"{" selected" if k == val else ""}>{t}</option>' for k, t in opts)
    return f'<div class="fld"{_w(when)}><label for="{id}">{label}</label><select id="{id}">{o}</select></div>'

def dat(id, label, value="", today=False, when=None):
    """date input. ALWAYS give a default: value="YYYY-MM-DD" or today=True (today's date)."""
    v = f' value="{value}"' if value else ""
    return f'<div class="fld"{_w(when)}><label for="{id}">{label}</label><input type="date" id="{id}"{v}{" data-today" if today else ""}></div>'

def tim(id, label, value="09:00", when=None):
    return f'<div class="fld"{_w(when)}><label for="{id}">{label}</label><input type="time" id="{id}" value="{value}"></div>'

def dtl(id, label, value="", when=None):
    """date + time (datetime-local). value="YYYY-MM-DDTHH:MM"."""
    return f'<div class="fld"{_w(when)}><label for="{id}">{label}</label><input type="datetime-local" id="{id}" value="{value}"></div>'

def txt(id, label, val="", rows=6, when=None, placeholder=""):
    ph = f' placeholder="{placeholder}"' if placeholder else ""
    return f'<div class="fld wide"{_w(when)}><label for="{id}">{label}</label><textarea id="{id}" rows="{rows}"{ph}>{val}</textarea></div>'

def chk(id, label, checked=False, when=None):
    return f'<div class="fld chk"{_w(when)}><label><input type="checkbox" id="{id}"{" checked" if checked else ""}> {label}</label></div>'

def btn(label, when=None):
    """button that re-runs the calculation when clicked (use for random generators)."""
    return f'<div class="fld"{_w(when)} style="align-self:end"><button type="button" class="btn sm" data-run>{label}</button></div>'

def info(what, formula, example):
    return (f"<h2>About this calculator</h2><p>{what}</p><h2>How it is calculated</h2><p>{formula}</p>"
            f"<h2>Example</h2><p>{example}</p>")


# ---------- registry ----------
CALCS = []
_SLUGS = set()

def calc(slug, js, cat, icon, name, short, h1, lead, fields, body, faqs, title=None, head="", also=()):
    """Register a calculator.
    slug   page file name (without .html), unique
    js     name of the JS function: C.<js> in js/<category>.js (several pages may share one)
    cat    primary category key (see CATEGORIES); also= other category keys that should LIST it too
    icon   key in icons.P (use add_icons() to add new ones)
    fields list of helper-built field html strings (num/sel/dat/...); EVERY field needs a sensible default
    body   html: use info(what, formula, example)
    faqs   list of (question, answer) - at least 2
    """
    assert slug not in _SLUGS, f"duplicate slug {slug}"
    assert cat in CAT, f"unknown category {cat}"
    for a in also:
        assert a in CAT, f"unknown also-category {a}"
    assert len(faqs) >= 2, slug
    _SLUGS.add(slug)
    CALCS.append(dict(slug=slug, js=js, cat=cat, also=tuple(also), icon=icon, name=name, short=short, h1=h1, lead=lead,
                      fields="".join(fields), body=body, faqs=faqs, head=head,
                      title=title or f"{name} – Free Online Calculator"))

def add_icons(d):
    """register extra SVG icon bodies (24x24 stroke paths): add_icons({"key": '<path d="..."/>'})"""
    icons.P.update(d)
