import math

# ================= CONFIG =================
SITE_NAME = "CalcHub"
DOMAIN = "https://pavanvasoya08.github.io/calchub"
CONTACT_EMAIL = "yourname@gmail.com"
CUR = "₹"            # currency symbol used in calculators ("$", "£", "€" ...)
LOCALE = "en-IN"     # number format: "en-IN" (1,00,000) or "en-US" (100,000)
# ==========================================


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
    return CUR + ip + ("." + fp if fp else "")


def emi_f(P, r, y):
    i, m = r / 1200, y * 12
    return P * i * (1 + i) ** m / ((1 + i) ** m - 1)


# ---------- field builders ----------
def _w(when):
    return f' data-when="{when}"' if when else ""

def num(id, label, val, when=None, step="any"):
    return f'<div class="fld"{_w(when)}><label for="{id}">{label}</label><input type="number" id="{id}" value="{val}" step="{step}" min="0"></div>'

def sel(id, label, opts, val=None, when=None):
    o = "".join(f'<option value="{k}"{" selected" if k == val else ""}>{t}</option>' for k, t in opts)
    return f'<div class="fld"{_w(when)}><label for="{id}">{label}</label><select id="{id}">{o}</select></div>'

def dat(id, label, today=False, when=None):
    return f'<div class="fld"{_w(when)}><label for="{id}">{label}</label><input type="date" id="{id}"{" data-today" if today else ""}></div>'

def txt(id, label, val):
    return f'<div class="fld" style="grid-column:1/-1"><label for="{id}">{label}</label><textarea id="{id}">{val}</textarea></div>'

def info(what, formula, example):
    return (f"<h2>About this calculator</h2><p>{what}</p><h2>How it is calculated</h2><p>{formula}</p>"
            f"<h2>Example</h2><p>{example}</p>")


CALCS = []
def calc(slug, js, cat, icon, name, short, h1, lead, fields, body, faqs, title=None, head=""):
    CALCS.append(dict(slug=slug, js=js, cat=cat, icon=icon, name=name, short=short, h1=h1, lead=lead,
                      fields="".join(fields), body=body, faqs=faqs, head=head,
                      title=title or f"{name} – Free Online Calculator"))

FIN, TAX, HEALTH, MATH, UNIT = ("Loans & Investments", "Tax, Salary & Business", "Health & Fitness", "Math & Everyday", "Unit Converters")
CATS = [(FIN, "💹", "finance"), (TAX, "🧾", "business"), (HEALTH, "❤️", "health"), (MATH, "🧮", "math"), (UNIT, "📏", "converters")]

# =============== LOANS & INVESTMENTS ===============
e = emi_f(1000000, 9, 10)
calc("emi-calculator", "emi", FIN, "🏦", "EMI Calculator", "Home, car & personal loan EMI",
     "EMI Calculator – Calculate Your Monthly Loan EMI",
     "Find your monthly EMI, total interest and year-wise repayment schedule for a home, car or personal loan.",
     [num("p", f"Loan amount ({CUR})", 2500000), num("r", "Interest rate (% per year)", 8.75), num("y", "Loan tenure (years)", 20)],
     info("An EMI (Equated Monthly Installment) is the fixed amount you pay your lender every month until a loan is fully repaid. Each EMI has two parts, principal and interest. In the early years most of the EMI goes towards interest, and the principal share grows over time.",
          "EMI = P × r × (1 + r)<sup>n</sup> ÷ ((1 + r)<sup>n</sup> − 1), where P is the loan amount, r is the monthly interest rate (annual rate ÷ 12 ÷ 100) and n is the number of monthly payments.",
          f"For a loan of {fmt(1000000)} at 9% for 10 years, the EMI is about {fmt(e)}. Over 120 months you would pay {fmt(e*120)} in total, of which {fmt(e*120-1000000)} is interest."),
     [("Does a longer tenure reduce my EMI?", "Yes. A longer tenure lowers the monthly EMI but increases the total interest you pay over the life of the loan."),
      ("Will my bank's EMI match this result?", "It should be very close for loans on a reducing balance. Processing fees, insurance and other charges are not included, so the bank's final figure can differ slightly."),
      ("How can I reduce the interest on my loan?", "Make part-prepayments when you can, choose the shortest tenure you can afford, and compare interest rates across lenders before you sign.")],
     title="EMI Calculator – Home, Car & Personal Loan EMI (Free)")

calc("home-loan-eligibility-calculator", "elig", FIN, "🏠", "Loan Eligibility Calculator", "How much loan can you get?",
     "Loan Eligibility Calculator – How Much Loan Can You Afford?",
     "Estimate the maximum loan you may qualify for based on your income, existing EMIs and the interest rate.",
     [num("inc", f"Net monthly income ({CUR})", 100000), num("ex", f"Existing monthly EMIs ({CUR})", 10000), num("r", "Interest rate (% per year)", 8.75),
      num("y", "Loan tenure (years)", 20), num("foir", "Share of income allowed for EMIs (%)", 50)],
     info("Lenders limit the share of your income that can go towards loan repayments. This calculator works backwards from that limit to estimate the largest loan whose EMI fits within it.",
          "Maximum EMI = income × allowed % − existing EMIs. Eligible loan = maximum EMI ÷ (EMI per 1 unit of loan at your rate and tenure).",
          f"With a net income of {fmt(100000)}, existing EMIs of {fmt(10000)} and a 50% limit, you can afford an EMI of {fmt(40000)} a month. The loan that EMI supports depends on the rate and tenure you enter."),
     [("What percentage of income do banks allow for EMIs?", "Many lenders allow roughly 40% to 60% of net monthly income to go towards all EMIs combined. The exact limit depends on the lender and your profile."),
      ("Is this the amount the bank will sanction?", "No. This is an estimate. Banks also check your credit score, age, employment stability and the value of the property or asset.")])

e2 = 10000 * (((1 + 0.01) ** 120 - 1) / 0.01) * 1.01
calc("sip-calculator", "sip", FIN, "📈", "SIP Calculator", "Mutual fund SIP returns",
     "SIP Calculator – Estimate Your Mutual Fund Returns",
     "See how much a monthly SIP can grow to over time at an expected rate of return.",
     [num("p", f"Monthly investment ({CUR})", 10000), num("r", "Expected return (% per year)", 12), num("y", "Time period (years)", 15)],
     info("A Systematic Investment Plan (SIP) lets you invest a fixed amount every month in a mutual fund. Because your earlier investments keep earning returns, long periods benefit greatly from compounding.",
          "Future value = P × [((1 + i)<sup>n</sup> − 1) ÷ i] × (1 + i), where P is the monthly amount, i is the monthly rate of return and n is the number of months.",
          f"Investing {fmt(10000)} a month for 10 years at 12% a year grows to about {fmt(e2)}, while you invest {fmt(1200000)} in total."),
     [("Are SIP returns guaranteed?", "No. Mutual fund returns depend on the market. This calculator only shows an estimate based on the rate you enter."),
      ("What return rate should I use?", "Use a conservative number. Long-term equity funds have historically delivered around 10% to 12% a year in some periods, but actual returns can be much higher or lower."),
      ("Is it better to start early?", "Yes. Starting early gives your money more time to compound, which often matters more than the amount you invest.")])

calc("lumpsum-calculator", "lump", FIN, "💼", "Lumpsum Calculator", "One-time investment growth",
     "Lumpsum Calculator – Future Value of a One-Time Investment",
     "Find out what a one-time investment can grow to at an expected annual return.",
     [num("p", f"Investment amount ({CUR})", 100000), num("r", "Expected return (% per year)", 12), num("y", "Time period (years)", 10)],
     info("A lumpsum investment is a single one-time deposit that grows through compounding. This calculator shows the estimated value at the end of your chosen period.",
          "Future value = P × (1 + r)<sup>t</sup>, where P is the amount, r is the annual return as a decimal and t is the number of years.",
          f"{fmt(100000)} invested at 10% a year for 10 years grows to {fmt(100000*1.1**10)}."),
     [("What is the difference between SIP and lumpsum?", "A SIP invests a fixed amount regularly, while a lumpsum invests the whole amount at once. SIPs spread out market timing risk."),
      ("Are the returns guaranteed?", "No. Returns on market-linked investments vary. Treat this as an estimate.")])

calc("fd-calculator", "fd", FIN, "🏦", "FD Calculator", "Fixed deposit maturity amount",
     "FD Calculator – Fixed Deposit Maturity Amount & Interest",
     "Calculate the maturity amount and interest earned on a fixed deposit with quarterly, monthly or yearly compounding.",
     [num("p", f"Deposit amount ({CUR})", 100000), num("r", "Interest rate (% per year)", 7), num("y", "Period (years)", 5),
      sel("n", "Compounding", [("4", "Quarterly"), ("12", "Monthly"), ("2", "Half-yearly"), ("1", "Yearly")], "4")],
     info("A fixed deposit (FD) pays a fixed rate of interest for a fixed period. Most banks compound FD interest every quarter, so interest also earns interest.",
          "Maturity amount A = P × (1 + r ÷ (100 × n))<sup>n × t</sup>, where n is the number of compounding periods per year and t is the number of years.",
          f"{fmt(100000)} at 7% for 5 years with quarterly compounding matures to about {fmt(100000*(1+0.07/4)**20)}."),
     [("Is FD interest taxable?", "In most countries, including India, interest from fixed deposits is taxable as income. This calculator does not deduct tax."),
      ("Which compounding frequency is best?", "More frequent compounding gives slightly higher returns, but the difference is usually small.")])

calc("rd-calculator", "rd", FIN, "🐖", "RD Calculator", "Recurring deposit maturity",
     "RD Calculator – Recurring Deposit Maturity Amount",
     "Calculate the maturity value of a monthly recurring deposit with quarterly compounding.",
     [num("p", f"Monthly deposit ({CUR})", 5000), num("r", "Interest rate (% per year)", 6.5), num("y", "Period (years)", 5)],
     info("A recurring deposit (RD) lets you deposit a fixed amount every month and earn a fixed interest rate. It suits people who want to build savings gradually.",
          "This calculator uses the common bank formula with quarterly compounding: M = R × [(1 + i)<sup>n</sup> − 1] ÷ [1 − (1 + i)<sup>−1/3</sup>], where R is the monthly deposit, i is the quarterly rate and n is the number of quarters.",
          f"Depositing {fmt(5000)} a month for 5 years deposits {fmt(300000)} in total. The maturity value will be higher because of the interest earned."),
     [("What is the difference between FD and RD?", "An FD needs a lump sum at the start, while an RD lets you deposit a fixed amount every month."),
      ("Will my bank give the exact same figure?", "Banks may round or compute interest slightly differently, so small variations are normal.")])

calc("ppf-calculator", "ppf", FIN, "🏛️", "PPF Calculator", "Public Provident Fund maturity",
     "PPF Calculator – Public Provident Fund Maturity Value",
     "Estimate your PPF maturity value and yearly growth. Update the rate to match the latest announced PPF rate.",
     [num("p", f"Yearly deposit ({CUR})", 150000), num("r", "Interest rate (% per year)", 7.1), num("y", "Years", 15)],
     info("The Public Provident Fund (PPF) is a long-term, government-backed savings scheme in India. The interest rate is set by the government and reviewed regularly, so enter the current rate before you calculate.",
          "Each year: closing balance = (opening balance + yearly deposit) × (1 + rate). This assumes the deposit is made at the start of each financial year.",
          f"Depositing {fmt(150000)} every year for 15 years at 7.1% gives a maturity value of about {fmt(sum(150000*1.071**k for k in range(1,16)))}."),
     [("What is the PPF lock-in period?", "The standard PPF tenure is 15 years, and it can be extended in blocks of 5 years. Check the latest rules for partial withdrawals."),
      ("Is PPF interest taxable?", "Under current rules PPF has been treated as tax-exempt, but tax laws change. Please verify with an official source.")])

calc("compound-interest-calculator", "ci", FIN, "🔁", "Compound Interest Calculator", "Interest on interest",
     "Compound Interest Calculator – Final Amount & Interest",
     "Calculate compound interest with daily, monthly, quarterly, half-yearly or yearly compounding.",
     [num("p", f"Principal ({CUR})", 100000), num("r", "Interest rate (% per year)", 8), num("y", "Time (years)", 5),
      sel("n", "Compounding", [("1", "Yearly"), ("2", "Half-yearly"), ("4", "Quarterly"), ("12", "Monthly"), ("365", "Daily")], "1")],
     info("Compound interest is interest calculated on both the original principal and the interest already added. It makes savings and loans grow faster than simple interest.",
          "A = P × (1 + r ÷ n)<sup>n × t</sup>. Compound interest = A − P, where r is the annual rate as a decimal, n is the number of times interest compounds per year and t is the time in years.",
          f"{fmt(100000)} at 8% compounded yearly for 5 years becomes {fmt(100000*1.08**5)}, so the compound interest is {fmt(100000*1.08**5-100000)}."),
     [("What is the difference between simple and compound interest?", "Simple interest is earned only on the principal. Compound interest is earned on the principal plus the interest already accumulated."),
      ("Does more frequent compounding help?", "Yes, but only slightly. Going from yearly to monthly compounding adds a small extra amount.")])

calc("simple-interest-calculator", "si", FIN, "➕", "Simple Interest Calculator", "Interest on principal only",
     "Simple Interest Calculator – Interest & Total Amount",
     "Calculate simple interest and the total amount for any principal, rate and time.",
     [num("p", f"Principal ({CUR})", 10000), num("r", "Interest rate (% per year)", 8), num("y", "Time (years)", 3)],
     info("Simple interest is calculated only on the original principal, not on interest already earned. It is commonly used for short-term loans and basic savings schemes.",
          "Simple Interest = P × R × T ÷ 100, where P is the principal, R is the annual rate in percent and T is the time in years. Total amount = P + SI.",
          f"The simple interest on {fmt(10000)} at 8% for 3 years is {fmt(2400)}, so the total amount is {fmt(12400)}."),
     [("How do I calculate interest for months?", "Convert months to years by dividing by 12. For example, 6 months is 0.5 years."),
      ("Is simple interest cheaper than compound interest?", "For a borrower, simple interest costs less over long periods because interest does not pile up on interest.")])

calc("cagr-calculator", "cagr", FIN, "🚀", "CAGR Calculator", "Compound annual growth rate",
     "CAGR Calculator – Compound Annual Growth Rate",
     "Find the yearly growth rate of an investment between a starting and ending value.",
     [num("a", f"Initial value ({CUR})", 100000), num("b", f"Final value ({CUR})", 250000), num("y", "Number of years", 5)],
     info("CAGR (Compound Annual Growth Rate) is the steady yearly rate at which an investment would have to grow to reach its final value from its starting value. It smooths out year-to-year ups and downs.",
          "CAGR = (Final value ÷ Initial value)<sup>1 ÷ years</sup> − 1.",
          f"An investment that grows from {fmt(100000)} to {fmt(250000)} in 5 years has a CAGR of {((2.5)**(1/5)-1)*100:.2f}% a year."),
     [("Is CAGR the same as average return?", "No. Average return is a simple mean of yearly returns, while CAGR accounts for compounding, so it is usually more accurate."),
      ("Can CAGR be negative?", "Yes. If the final value is lower than the initial value, the CAGR is negative.")])

calc("swp-calculator", "swp", FIN, "🏧", "SWP Calculator", "Systematic withdrawal plan",
     "SWP Calculator – Systematic Withdrawal Plan",
     "See how long your money lasts when you withdraw a fixed amount every month from an investment.",
     [num("p", f"Total investment ({CUR})", 2000000), num("w", f"Monthly withdrawal ({CUR})", 15000), num("r", "Expected return (% per year)", 8), num("y", "Time period (years)", 15)],
     info("A Systematic Withdrawal Plan (SWP) lets you take a fixed amount out of an investment every month while the remaining balance keeps earning returns. It is often used to create regular income from savings.",
          "Each month the withdrawal is taken first, and the remaining balance grows by the monthly rate: balance = (balance − withdrawal) × (1 + monthly rate).",
          "If your withdrawals are larger than the returns your balance earns, the money will eventually run out. The calculator shows exactly when."),
     [("How do I make my money last longer?", "Withdraw less each month or hope for higher returns. A safe withdrawal is usually close to what the investment can earn."),
      ("Are SWP returns guaranteed?", "No. Market returns vary, so use a conservative rate.")])

calc("inflation-calculator", "infl", FIN, "🎈", "Inflation Calculator", "Future cost of things",
     "Inflation Calculator – Future Value of Money",
     "See how inflation changes what things cost and how much your money can buy in the future.",
     [num("a", f"Amount today ({CUR})", 100000), num("r", "Inflation rate (% per year)", 6), num("y", "Years", 10)],
     info("Inflation is the steady rise in prices over time. The same amount of money buys less each year, so it is important to plan savings and retirement with inflation in mind.",
          "Future cost = amount × (1 + inflation)<sup>years</sup>. Purchasing power of today's amount in the future = amount ÷ (1 + inflation)<sup>years</sup>.",
          f"At 6% inflation, something that costs {fmt(100000)} today will cost about {fmt(100000*1.06**10)} in 10 years."),
     [("What inflation rate should I use?", "Look at your country's long-term average. Many people use 5% to 7% for India and 2% to 3% for developed economies."),
      ("Why does inflation matter for savings?", "If your savings earn less than inflation, your money loses purchasing power even though the balance grows.")])

calc("savings-goal-calculator", "save", FIN, "🎯", "Savings Goal Calculator", "Monthly saving needed for a goal",
     "Savings Goal Calculator – How Much to Save Every Month",
     "Find the monthly amount you need to save to reach a target by a certain date.",
     [num("g", f"Goal amount ({CUR})", 1000000), num("c", f"Current savings ({CUR})", 50000), num("r", "Expected return (% per year)", 7), num("y", "Years to reach the goal", 5)],
     info("This calculator tells you how much to put aside each month to reach a financial goal such as a car, a wedding or a house down payment. It takes your current savings and expected interest into account.",
          "It finds the monthly deposit P so that your current savings plus all monthly deposits, growing at the monthly rate, equal the goal at the end of the period.",
          "Set the return to 0% if you are saving in cash. Then the monthly amount is simply the remaining goal divided by the number of months."),
     [("Does the calculator include inflation?", "No. If your goal's cost will rise with inflation, increase the goal amount to match."),
      ("What if I can't afford the monthly amount?", "Extend the time period, lower the goal or look for options with a higher return.")])

calc("roi-calculator", "roi", FIN, "💹", "ROI Calculator", "Return on investment",
     "ROI Calculator – Return on Investment & Annualized Return",
     "Calculate the return on investment, net profit and annualized return for any investment.",
     [num("a", f"Amount invested ({CUR})", 100000), num("b", f"Final value ({CUR})", 135000), num("y", "Time held (years, optional)", 3)],
     info("Return on Investment (ROI) measures how much you gained or lost on an investment compared to its cost. It is useful for comparing different investments.",
          "ROI = (Final value − Amount invested) ÷ Amount invested × 100. Annualized return = (Final value ÷ Amount invested)<sup>1 ÷ years</sup> − 1.",
          f"Buying for {fmt(100000)} and selling for {fmt(135000)} gives a profit of {fmt(35000)} and an ROI of 35%."),
     [("What is a good ROI?", "It depends on the risk and time. Compare it against the returns of safer options such as fixed deposits."),
      ("Why is annualized return useful?", "A 35% gain over 1 year is far better than over 10 years. Annualizing makes investments of different durations comparable.")])

# =============== TAX, SALARY & BUSINESS ===============
calc("gst-calculator", "gst", TAX, "🧾", "GST Calculator", "Add or remove GST / VAT",
     "GST Calculator – Add or Remove GST, VAT or Sales Tax",
     "Add tax to a price or remove it from a tax-inclusive price. Shows CGST and SGST split too.",
     [num("a", f"Amount ({CUR})", 10000, step="0.01"),
      sel("rate", "Tax rate", [("5", "5%"), ("12", "12%"), ("18", "18%"), ("28", "28%"), ("c", "Custom")], "18"),
      num("cr", "Custom rate (%)", 18, when="rate=c"),
      sel("mode", "What do you want to do?", [("add", "Add tax to the amount"), ("remove", "Remove tax from the amount")], "add")],
     info("Goods and Services Tax (GST) is an indirect tax charged on the sale of goods and services. The same method works for VAT or sales tax, just enter your local rate.",
          "To add tax: tax = amount × rate ÷ 100. To remove tax: net amount = tax-inclusive amount × 100 ÷ (100 + rate), and tax = inclusive amount − net amount.",
          f"Adding 18% GST to {fmt(1000)} gives GST of {fmt(180)} and a total of {fmt(1180)}. Removing 18% GST from {fmt(1180)} returns {fmt(1000)}."),
     [("What are CGST and SGST?", "For sales within one state, the GST is split equally between the central government (CGST) and the state government (SGST). Sales between states attract IGST."),
      ("Do GST rates change?", "Yes, rates and categories are revised from time to time. Always confirm the current rate for your product or service from an official source.")],
     title="GST Calculator India – Add or Remove GST (Free)")

calc("hra-calculator", "hra", TAX, "🏘️", "HRA Exemption Calculator", "House rent allowance tax exemption",
     "HRA Exemption Calculator – Tax-Free House Rent Allowance",
     "Find how much of your House Rent Allowance is tax-exempt under the old tax regime.",
     [num("b", f"Monthly basic salary ({CUR})", 50000), num("da", f"Monthly dearness allowance ({CUR})", 0), num("hra", f"Monthly HRA received ({CUR})", 20000),
      num("rent", f"Monthly rent paid ({CUR})", 18000), sel("city", "City type", [("50", "Metro city (Delhi, Mumbai, Kolkata, Chennai)"), ("40", "Non-metro city")], "50")],
     info("If you live in rented accommodation and receive HRA from your employer, part of it can be exempt from income tax under the old regime. The exemption is the lowest of three amounts.",
          "Exempt HRA = the least of (1) actual HRA received, (2) rent paid minus 10% of (basic + DA), and (3) 50% of (basic + DA) for metro cities or 40% for others.",
          f"With a basic of {fmt(50000)}, HRA of {fmt(20000)}, rent of {fmt(18000)} in a metro city: the three amounts are {fmt(20000)}, {fmt(13000)} and {fmt(25000)}. The exemption is {fmt(13000)} a month."),
     [("Can I claim HRA if I live with my parents?", "Yes, if you actually pay rent to them and have proof, such as rent receipts and bank transfers. Tax rules apply, so check with a tax professional."),
      ("Is HRA exemption available in the new tax regime?", "HRA exemption is generally available only under the old tax regime. Check the latest rules.")])

calc("gratuity-calculator", "grat", TAX, "🎁", "Gratuity Calculator", "Gratuity on leaving a job",
     "Gratuity Calculator – Calculate Your Gratuity Amount",
     "Estimate the gratuity you will receive from your employer based on your last drawn salary and years of service.",
     [num("sal", f"Last drawn monthly salary (Basic + DA) ({CUR})", 50000), num("yr", "Years of service", 8, step="1"), num("mo", "Extra months of service", 7, step="1")],
     info("Gratuity is a lump-sum payment from an employer to an employee for long service. In India it is covered by the Payment of Gratuity Act for employees who complete 5 years of continuous service.",
          "Gratuity = Last drawn salary (Basic + DA) × 15 ÷ 26 × years of service. A part of a year of 6 months or more is counted as a full year.",
          f"For a salary of {fmt(50000)} and 8 years 7 months of service, the service counts as 9 years: {fmt(50000)} × 15 ÷ 26 × 9 = {fmt(50000*15/26*9)}."),
     [("Is gratuity payable before 5 years?", "Usually not, except in cases such as death or disability. Check your company policy and the Act."),
      ("Is gratuity taxable?", "Gratuity up to a certain limit is tax-free. Amounts above the limit are taxable. Check the current limit.")])

calc("hourly-to-salary-calculator", "hour", TAX, "⏱️", "Hourly to Salary Calculator", "Convert hourly pay to monthly & yearly",
     "Hourly to Salary Calculator – Convert Hourly Pay to Annual Salary",
     "Convert an hourly wage into weekly, monthly and yearly pay.",
     [num("rate", f"Hourly rate ({CUR})", 500), num("hrs", "Hours per week", 40), num("wks", "Weeks per year", 52)],
     info("This calculator converts hourly pay into weekly, monthly and annual income. It is helpful when comparing a freelance or hourly job with a fixed salary.",
          "Annual pay = hourly rate × hours per week × weeks per year. Monthly pay = annual pay ÷ 12.",
          f"At {fmt(500)} an hour for 40 hours a week and 52 weeks, the annual pay is {fmt(500*40*52)}, which is about {fmt(500*40*52/12)} a month."),
     [("Should I subtract unpaid leave?", "Yes. If you take unpaid weeks off, reduce the weeks per year to get a realistic figure."),
      ("Is the result before or after tax?", "Before tax. Taxes and deductions are not included.")])

calc("discount-calculator", "disc", TAX, "🏷️", "Discount Calculator", "Final price after discount",
     "Discount Calculator – Sale Price & Savings",
     "Find the final price and your savings after one or two successive discounts.",
     [num("a", f"Original price ({CUR})", 2000), num("d1", "Discount (%)", 25), num("d2", "Additional discount (%)", 0)],
     info("This calculator shows the price you pay after a percentage discount, and how much you save. You can also add a second discount, as in a sale plus a coupon.",
          "Final price = original price × (1 − discount1 ÷ 100) × (1 − discount2 ÷ 100). Two discounts are applied one after the other, not added together.",
          f"A {fmt(2000)} item with 25% off costs {fmt(1500)}. With an extra 10% coupon it costs {fmt(1350)}, an effective discount of 32.5%."),
     [("Why isn't a 20% + 10% discount equal to 30%?", "The second discount applies to the already reduced price, so the total saving is a little smaller than the sum."),
      ("How do I find the original price?", "Divide the sale price by (1 − discount%). For example, a price of 75 after 25% off was originally 100.")])

calc("tip-calculator", "tip", TAX, "🍽️", "Tip Calculator", "Split the bill with a tip",
     "Tip Calculator – Tip Amount & Bill Split",
     "Work out the tip and split the total bill between any number of people.",
     [num("a", f"Bill amount ({CUR})", 2400), num("t", "Tip (%)", 10), num("n", "Number of people", 4, step="1")],
     info("Use this calculator at restaurants to add a tip and divide the bill fairly. Tipping customs differ by country, so choose the percentage that suits where you are.",
          "Tip = bill × tip% ÷ 100. Total = bill + tip. Each person pays total ÷ number of people.",
          f"A {fmt(2400)} bill with a 10% tip is {fmt(2640)}. Split among 4 people, each pays {fmt(660)}."),
     [("How much should I tip?", "It depends on local custom. Many places use 5% to 10%, while some countries expect 15% to 20%."),
      ("Is the service charge the same as a tip?", "Not always. A service charge is added by the restaurant, while a tip is optional. Check your bill first.")])

calc("profit-margin-calculator", "marg", TAX, "📊", "Profit Margin Calculator", "Margin and markup",
     "Profit Margin Calculator – Margin & Markup",
     "Calculate profit, profit margin and markup from your cost and selling price.",
     [num("cost", f"Cost price ({CUR})", 800), num("sp", f"Selling price ({CUR})", 1000)],
     info("Profit margin is the share of the selling price that is profit. Markup is the profit as a share of the cost. They are often confused, but they give different numbers.",
          "Profit = selling price − cost. Margin = profit ÷ selling price × 100. Markup = profit ÷ cost × 100.",
          f"If an item costs {fmt(800)} and sells for {fmt(1000)}, the profit is {fmt(200)}, the margin is 20% and the markup is 25%."),
     [("What is the difference between margin and markup?", "Margin is measured against the selling price and markup against the cost. A 25% markup equals a 20% margin."),
      ("How do I set a price for a target margin?", "Selling price = cost ÷ (1 − target margin). For a 20% margin on a cost of 800, the price is 1,000.")])

calc("break-even-calculator", "be", TAX, "⚖️", "Break-Even Calculator", "Units needed to cover costs",
     "Break-Even Calculator – Break-Even Units & Revenue",
     "Find how many units you must sell to cover all your fixed and variable costs.",
     [num("fc", f"Total fixed costs ({CUR})", 100000), num("price", f"Selling price per unit ({CUR})", 500), num("vc", f"Variable cost per unit ({CUR})", 300)],
     info("The break-even point is where your total revenue equals your total costs, so you make neither profit nor loss. Every unit sold beyond it adds to your profit.",
          "Break-even units = fixed costs ÷ (selling price − variable cost per unit). The difference between price and variable cost is called the contribution margin.",
          f"With fixed costs of {fmt(100000)}, a price of {fmt(500)} and a variable cost of {fmt(300)}, the contribution is {fmt(200)} per unit, so you must sell 500 units."),
     [("What are fixed and variable costs?", "Fixed costs, such as rent, stay the same regardless of sales. Variable costs, such as materials, change with each unit produced."),
      ("How can I lower my break-even point?", "Cut fixed costs, reduce variable costs or raise your selling price.")])

calc("commission-calculator", "comm", TAX, "🤝", "Commission Calculator", "Commission on a sale",
     "Commission Calculator – Sales Commission Amount",
     "Calculate the commission earned on a sale at any percentage rate.",
     [num("a", f"Sale amount ({CUR})", 250000), num("r", "Commission rate (%)", 5)],
     info("Commission is a fee paid to a salesperson, agent or broker, usually as a percentage of the sale value.",
          "Commission = sale amount × commission rate ÷ 100.",
          f"A 5% commission on a {fmt(250000)} sale is {fmt(12500)}."),
     [("Is commission calculated before or after tax?", "That depends on your agreement. Confirm whether the rate applies to the pre-tax or post-tax amount."),
      ("Can I use a tiered commission?", "This calculator uses a single rate. For tiers, calculate each slab separately and add the results.")])

# =============== HEALTH ===============
calc("bmi-calculator", "bmi", HEALTH, "⚖️", "BMI Calculator", "Body mass index",
     "BMI Calculator – Body Mass Index for Adults",
     "Check your Body Mass Index and see your healthy weight range. Works in kilograms/centimetres or pounds/feet.",
     [sel("u", "Units", [("m", "Metric (kg, cm)"), ("i", "Imperial (lb, ft, in)")], "m"),
      num("kg", "Weight (kg)", 70, when="u=m"), num("cm", "Height (cm)", 170, when="u=m"),
      num("lb", "Weight (lb)", 154, when="u=i"), num("ft", "Height (feet)", 5, when="u=i", step="1"), num("inch", "Height (inches)", 7, when="u=i")],
     info("Body Mass Index (BMI) compares your weight with your height. It is a quick screening tool for weight categories in adults, not a diagnosis.",
          "BMI = weight (kg) ÷ height (m)<sup>2</sup>. Adult ranges: under 18.5 underweight, 18.5 to 24.9 normal, 25 to 29.9 overweight, 30 and above obese.",
          f"A person who weighs 70 kg and is 170 cm tall has a BMI of {70/1.7**2:.1f}, which is in the normal range."),
     [("Is BMI accurate for everyone?", "No. BMI does not measure body fat or muscle, so it can be misleading for athletes, older adults and some ethnic groups."),
      ("Does this apply to children?", "No. Children and teens use age and sex-specific BMI percentiles. Ask a paediatrician.")])

calc("bmr-calculator", "bmr", HEALTH, "🔥", "BMR & Calorie Calculator", "Daily calorie needs",
     "BMR & Calorie Calculator – Daily Calorie Needs",
     "Estimate your basal metabolic rate and daily calories needed to maintain your weight.",
     [sel("sex", "Sex", [("m", "Male"), ("f", "Female")], "m"), num("age", "Age (years)", 30, step="1"), num("kg", "Weight (kg)", 70), num("cm", "Height (cm)", 170),
      sel("act", "Activity level", [("1.2", "Sedentary (little or no exercise)"), ("1.375", "Light (1–3 days a week)"), ("1.55", "Moderate (3–5 days a week)"), ("1.725", "Very active (6–7 days a week)"), ("1.9", "Extra active (hard training or physical job)")], "1.375")],
     info("Basal Metabolic Rate (BMR) is the number of calories your body burns at rest to keep you alive. Multiplying it by an activity factor gives the calories you need each day to maintain your weight.",
          "Mifflin-St Jeor: BMR = 10 × weight (kg) + 6.25 × height (cm) − 5 × age + 5 for men, or − 161 for women. Daily calories = BMR × activity factor.",
          f"A 30-year-old man who weighs 70 kg and is 170 cm tall has a BMR of {10*70+6.25*170-150+5:.0f} kcal a day."),
     [("How many calories should I eat to lose weight?", "Eating less than your maintenance calories creates a deficit. Speak to a doctor or dietitian before making big changes."),
      ("How accurate is this?", "It is an estimate. Real needs vary with muscle mass, genetics and health conditions.")])

calc("ideal-weight-calculator", "ideal", HEALTH, "🧍", "Ideal Weight Calculator", "Healthy weight for your height",
     "Ideal Weight Calculator – Healthy Weight for Your Height",
     "Estimate your ideal body weight using the Devine, Robinson and Miller formulas.",
     [sel("sex", "Sex", [("m", "Male"), ("f", "Female")], "m"), num("cm", "Height (cm)", 170)],
     info("Ideal body weight formulas give a rough target weight for a given height and sex. They were originally created to help with medicine dosing, and are only a guide.",
          "Devine: 50 kg + 2.3 kg for each inch over 5 feet for men, 45.5 kg + 2.3 kg for women. Robinson and Miller use slightly different values.",
          "A man who is 170 cm (about 5 ft 7 in) tall has a Devine ideal weight of about 66 kg."),
     [("Why do the formulas give different answers?", "Each was derived from different data, so they differ by a few kilograms. Treat the results as a range."),
      ("Is the healthy BMI range better?", "The BMI range gives a wider and often more practical target than a single number.")])

calc("body-fat-calculator", "bf", HEALTH, "📏", "Body Fat Calculator", "U.S. Navy method",
     "Body Fat Calculator – Estimate Your Body Fat Percentage",
     "Estimate your body fat percentage from simple tape measurements using the U.S. Navy method.",
     [sel("sex", "Sex", [("m", "Male"), ("f", "Female")], "m"), num("cm", "Height (cm)", 175), num("neck", "Neck circumference (cm)", 38), num("waist", "Waist circumference (cm)", 85),
      num("hip", "Hip circumference (cm)", 95, when="sex=f")],
     info("Body fat percentage tells you how much of your weight is fat. The U.S. Navy method estimates it from your height and circumference measurements, with no special equipment.",
          "For men: 495 ÷ (1.0324 − 0.19077 × log10(waist − neck) + 0.15456 × log10(height)) − 450. Women's formula also includes the hip measurement.",
          "Measure your waist at the navel, your neck below the larynx and your hips at the widest point. Use a flexible tape and keep it snug but not tight."),
     [("How accurate is the Navy method?", "It is an estimate and can differ from DEXA scans or skinfold tests by a few percentage points."),
      ("What is a healthy body fat percentage?", "Healthy ranges vary by age and sex. Generally, men range from 10% to 20% and women from 18% to 28%. Ask a professional for personal advice.")])

calc("pregnancy-due-date-calculator", "preg", HEALTH, "🤰", "Pregnancy Due Date Calculator", "Estimated delivery date",
     "Pregnancy Due Date Calculator – Estimated Due Date",
     "Estimate your due date and see how far along you are from the first day of your last period.",
     [dat("lmp", "First day of last period"), num("cyc", "Average cycle length (days)", 28, step="1")],
     info("A due date is an estimate of when your baby will arrive. It is counted from the first day of your last menstrual period, assuming a regular cycle.",
          "Naegele's rule: due date = first day of last period + 280 days (40 weeks). For cycles longer or shorter than 28 days, the date is adjusted by the difference.",
          "If your last period began on 1 January, your estimated due date is about 8 October."),
     [("How accurate is the due date?", "Only a small share of babies are born on the exact date. A birth within a few weeks either side is normal."),
      ("Will my doctor change the date?", "Possibly. A dating ultrasound can adjust the date, especially if your cycles are irregular.")])

# =============== MATH & EVERYDAY ===============
calc("percentage-calculator", "pct", MATH, "％", "Percentage Calculator", "Percent of, percent change & more",
     "Percentage Calculator – Percent of a Number, Change & More",
     "Four calculators in one: find a percent of a number, what percent one number is of another, percentage change and increase or decrease.",
     [sel("mode", "What do you want to find?", [("a", "X% of Y"), ("b", "X is what % of Y"), ("c", "Percentage change from X to Y"), ("d", "Increase / decrease Y by X%")], "a"),
      num("x", "X", 20), num("y", "Y", 250)],
     info("Percentages express a number as a part of 100. This tool handles the four most common percentage problems.",
          "X% of Y = X × Y ÷ 100. X as a percent of Y = X ÷ Y × 100. Percentage change = (Y − X) ÷ X × 100. Increasing Y by X% = Y × (1 + X ÷ 100).",
          "20% of 250 is 50. 50 is 20% of 250. A change from 80 to 100 is a 25% increase."),
     [("How do I calculate a percentage increase?", "Subtract the old value from the new value, divide by the old value and multiply by 100."),
      ("What is the difference between percentage and percentage points?", "If a rate goes from 10% to 12%, it rises by 2 percentage points, which is a 20% increase.")])

calc("average-calculator", "avg", MATH, "➗", "Average Calculator", "Mean, median, mode & range",
     "Average Calculator – Mean, Median, Mode & Range",
     "Enter a list of numbers to get their mean, median, mode, sum, minimum, maximum and range.",
     [txt("nums", "Numbers (separated by commas, spaces or new lines)", "12, 18, 25, 25, 31, 44")],
     info("The mean is the usual average. The median is the middle value when numbers are sorted. The mode is the value that appears most often. Together they describe a data set.",
          "Mean = sum ÷ count. Median = the middle value (or the mean of the two middle values). Range = maximum − minimum.",
          "For 12, 18, 25, 25, 31, 44: the sum is 155, the mean is 25.83, the median is 25, the mode is 25 and the range is 32."),
     [("When should I use the median instead of the mean?", "Use the median when extreme values would distort the mean, such as income data."),
      ("Can a data set have more than one mode?", "Yes. If several values tie for the most frequent, all are modes.")])

calc("standard-deviation-calculator", "sd", MATH, "📉", "Standard Deviation Calculator", "Population & sample SD",
     "Standard Deviation Calculator – Population & Sample",
     "Calculate the standard deviation and variance of a data set, for both population and sample.",
     [txt("nums", "Numbers (separated by commas, spaces or new lines)", "4, 8, 6, 5, 3, 7, 9, 5")],
     info("Standard deviation measures how spread out numbers are around their mean. A small value means the numbers are close together, and a large value means they are widely spread.",
          "Population SD = √(Σ(x − mean)<sup>2</sup> ÷ n). Sample SD = √(Σ(x − mean)<sup>2</sup> ÷ (n − 1)). Variance is the square of the standard deviation.",
          "For 2, 4, 4, 4, 5, 5, 7, 9 the mean is 5 and the population standard deviation is 2."),
     [("Which should I use, sample or population?", "Use the population SD if your data includes every member of the group. Use the sample SD if the data is only a sample of a larger group."),
      ("Why does the sample formula divide by n − 1?", "It corrects the bias that comes from estimating the mean from the same data.")])

calc("age-calculator", "age", MATH, "🎂", "Age Calculator", "Exact age in years, months & days",
     "Age Calculator – Calculate Your Exact Age",
     "Find your exact age in years, months and days from your date of birth. See your next birthday too.",
     [dat("dob", "Date of birth"), dat("to", "Age on this date", today=True)],
     info("This calculator gives your exact age on any date. Many job applications and exams ask for your age on a specific cut-off date, and you can enter that date in the second field.",
          "It subtracts your date of birth from the chosen date, borrowing days and months as needed. Leap years are handled automatically.",
          "Someone born on 15 May 2000 is 26 years, 6 months and 4 days old on 19 November 2026."),
     [("Can I find my age on a past or future date?", "Yes. Change the second date to any date you like."),
      ("How is the next birthday calculated?", "It counts the days from the chosen date to the next occurrence of your birth day and month.")])

calc("date-difference-calculator", "dd", MATH, "📅", "Date Difference Calculator", "Days between two dates",
     "Date Difference Calculator – Days Between Two Dates",
     "Find the number of days, weeks, months and working days between two dates.",
     [dat("s", "Start date"), dat("e", "End date", today=True)],
     info("Use this tool to find how long there is between two dates, for example the days left until a deadline or the length of a project.",
          "It counts the whole days between the two dates and also breaks the gap into years, months and days. Working days count Monday to Friday and do not include public holidays.",
          "From 1 January 2026 to 31 January 2026 is 30 days, which is 4 weeks and 2 days."),
     [("Is the end date included?", "The result counts the days between the dates. Add 1 if you want to include both the start and end dates."),
      ("Are holidays excluded from working days?", "No. Only weekends are excluded. Subtract public holidays yourself.")])

calc("cgpa-to-percentage-calculator", "cgpa", MATH, "🎓", "CGPA to Percentage Calculator", "Convert CGPA to percentage",
     "CGPA to Percentage Calculator – Convert CGPA to %",
     "Convert your CGPA to a percentage, or a percentage back to CGPA, using the common multiplier.",
     [sel("mode", "Convert", [("a", "CGPA to percentage"), ("b", "Percentage to CGPA")], "a"), num("val", "Enter your CGPA or percentage", 8.4),
      sel("mult", "Multiplier", [("9.5", "9.5 (CBSE / many universities)"), ("10", "10"), ("9.25", "9.25")], "9.5")],
     info("Many schools and universities use a 10-point CGPA. To convert it to a percentage, most apply a multiplier, and the most common one is 9.5.",
          "Percentage = CGPA × multiplier. To go the other way, CGPA = percentage ÷ multiplier.",
          "A CGPA of 8.4 with the 9.5 multiplier is 79.8%."),
     [("Which multiplier should I use?", "Use the one your board, university or employer specifies. Different institutions follow different rules."),
      ("Is this an official conversion?", "No. It is a calculator for guidance. Official conversions come from your institution.")])

calc("pythagorean-theorem-calculator", "pyth", MATH, "📐", "Pythagorean Theorem Calculator", "Right triangle sides",
     "Pythagorean Theorem Calculator – Find the Missing Side",
     "Find the hypotenuse or a missing side of a right triangle. Also get its area, perimeter and angles.",
     [sel("mode", "Find", [("h", "Hypotenuse (c)"), ("l", "A missing leg (b)")], "h"), num("a", "Side a", 3), num("b", "Side b", 4, when="mode=h"), num("c", "Hypotenuse c", 5, when="mode=l")],
     info("The Pythagorean theorem relates the three sides of a right triangle. The hypotenuse is the longest side, opposite the right angle.",
          "a<sup>2</sup> + b<sup>2</sup> = c<sup>2</sup>. To find a leg: b = √(c<sup>2</sup> − a<sup>2</sup>).",
          "If the two legs are 3 and 4, the hypotenuse is √(9 + 16) = 5."),
     [("Does this work for any triangle?", "No. It only works for right triangles, which have one 90° angle."),
      ("What is a Pythagorean triple?", "A set of three whole numbers that satisfy the theorem, such as 3-4-5, 5-12-13 and 8-15-17.")])

calc("area-calculator", "area", MATH, "🟦", "Area Calculator", "Area of common shapes",
     "Area Calculator – Area of Rectangle, Circle, Triangle & More",
     "Calculate the area of a rectangle, square, circle, triangle, parallelogram or trapezoid.",
     [sel("shape", "Shape", [("rect", "Rectangle"), ("sq", "Square"), ("circ", "Circle"), ("tri", "Triangle"), ("para", "Parallelogram"), ("trap", "Trapezoid")], "rect"),
      num("l", "Length", 10, when="shape=rect"), num("w", "Width", 5, when="shape=rect"), num("s", "Side", 6, when="shape=sq"), num("r", "Radius", 7, when="shape=circ"),
      num("tb", "Base", 8, when="shape=tri|para"), num("th", "Height", 5, when="shape=tri|para"),
      num("pa", "Parallel side a", 6, when="shape=trap"), num("pb", "Parallel side b", 10, when="shape=trap"), num("ph", "Height", 4, when="shape=trap")],
     info("Area is the amount of surface a flat shape covers. It is measured in square units, such as square metres or square feet.",
          "Rectangle: length × width. Square: side<sup>2</sup>. Circle: π × radius<sup>2</sup>. Triangle: ½ × base × height. Parallelogram: base × height. Trapezoid: ½ × (a + b) × height.",
          "A rectangle that is 10 m long and 5 m wide has an area of 50 square metres."),
     [("How do I convert square feet to square metres?", "Multiply square feet by 0.092903. You can also use our area converter."),
      ("Why must all units match?", "Mixing units, such as feet and inches, gives the wrong answer. Convert everything to one unit first.")])

calc("speed-distance-time-calculator", "sdt", MATH, "🚗", "Speed Distance Time Calculator", "Find speed, distance or time",
     "Speed, Distance & Time Calculator",
     "Find speed, distance or travel time when you know the other two values.",
     [sel("mode", "Find", [("s", "Speed"), ("d", "Distance"), ("t", "Time")], "s"), num("dist", "Distance (km)", 240, when="mode=s|t"), num("time", "Time (hours)", 4, when="mode=s|d"), num("spd", "Speed (km/h)", 60, when="mode=d|t")],
     info("Speed, distance and time are linked by one simple relationship. Know any two and you can find the third.",
          "Speed = distance ÷ time. Distance = speed × time. Time = distance ÷ speed. Keep the units consistent, for example kilometres and hours.",
          "Driving 240 km in 4 hours means an average speed of 60 km/h."),
     [("Can I use miles instead of kilometres?", "Yes. If you enter miles and hours, the speed will be in miles per hour."),
      ("Is this the average speed?", "Yes. It does not account for stops or changes in speed.")])

calc("fuel-cost-calculator", "fuel", MATH, "⛽", "Fuel Cost Calculator", "Trip fuel cost",
     "Fuel Cost Calculator – Trip Cost & Mileage",
     "Estimate the fuel needed and the cost of a trip from the distance, mileage and fuel price.",
     [num("dist", "Distance (km)", 300), num("mil", "Mileage (km per litre)", 15), num("price", f"Fuel price per litre ({CUR})", 100)],
     info("Plan your trip budget by working out how much fuel you will use and what it costs.",
          "Fuel needed = distance ÷ mileage. Cost = fuel needed × price per litre.",
          f"A 300 km trip at 15 km per litre uses 20 litres. At {fmt(100)} a litre, the fuel costs {fmt(2000)}."),
     [("How do I find my car's mileage?", "Fill the tank, note the odometer, drive, then refill. Divide the distance by the litres added."),
      ("Does driving style change mileage?", "Yes. Speed, traffic, load and AC use can change your real mileage by a lot.")])

calc("electricity-bill-calculator", "elec", MATH, "💡", "Electricity Cost Calculator", "Appliance energy cost",
     "Electricity Cost Calculator – Appliance Power Cost",
     "Work out how much electricity an appliance uses and what it costs to run.",
     [num("w", "Power rating (watts)", 1500), num("h", "Hours used per day", 3), num("days", "Number of days", 30), num("rate", f"Tariff per unit / kWh ({CUR})", 7)],
     info("Electricity is billed in units, also called kilowatt-hours (kWh). One kWh is the energy used by a 1,000-watt appliance running for one hour.",
          "Energy (kWh) = watts × hours per day × days ÷ 1,000. Cost = kWh × tariff. Note that real bills may also include fixed charges and slab rates.",
          f"A 1,500 W heater used for 3 hours a day for 30 days uses 135 kWh. At {fmt(7)} per unit, that costs {fmt(945)}."),
     [("Where can I find an appliance's wattage?", "Check the label on the appliance or its manual."),
      ("Why is my bill different?", "Your bill may include slab rates, fixed charges and taxes that this simple calculator does not include.")])

# =============== UNIT CONVERTERS ===============
UNITS = {
 "length": [("mm", "Millimeters", 0.001), ("cm", "Centimeters", 0.01), ("m", "Meters", 1), ("km", "Kilometers", 1000), ("in", "Inches", 0.0254), ("ft", "Feet", 0.3048), ("yd", "Yards", 0.9144), ("mi", "Miles", 1609.344), ("nmi", "Nautical miles", 1852)],
 "weight": [("mg", "Milligrams", 1e-6), ("g", "Grams", 0.001), ("kg", "Kilograms", 1), ("t", "Metric tonnes", 1000), ("oz", "Ounces", 0.028349523125), ("lb", "Pounds", 0.45359237), ("st", "Stone", 6.35029318)],
 "area": [("mm2", "Square millimeters", 1e-6), ("cm2", "Square centimeters", 1e-4), ("m2", "Square meters", 1), ("km2", "Square kilometers", 1e6), ("ha", "Hectares", 1e4), ("ac", "Acres", 4046.8564224), ("ft2", "Square feet", 0.09290304), ("yd2", "Square yards", 0.83612736), ("in2", "Square inches", 0.00064516)],
 "speed": [("ms", "Meters per second", 1), ("kmh", "Kilometers per hour", 1/3.6), ("mph", "Miles per hour", 0.44704), ("kn", "Knots", 1852/3600), ("fts", "Feet per second", 0.3048)],
 "volume": [("ml", "Milliliters", 0.001), ("l", "Liters", 1), ("m3", "Cubic meters", 1000), ("tsp", "Teaspoons (US)", 0.00492892159375), ("tbsp", "Tablespoons (US)", 0.01478676478125), ("cup", "Cups (US)", 0.2365882365), ("floz", "Fluid ounces (US)", 0.0295735295625), ("pt", "Pints (US)", 0.473176473), ("gal", "Gallons (US)", 3.785411784)],
}
CONV = {
 "length": ("Length Converter", "📏", "Convert between meters, kilometers, miles, feet, inches and more.", "m", "km", "A kilometer is 1,000 meters, and a mile is about 1.609 kilometers.", "1 foot = 0.3048 meters exactly. 1 inch = 2.54 centimeters exactly."),
 "weight": ("Weight Converter", "⚖️", "Convert between kilograms, grams, pounds, ounces and more.", "kg", "lb", "A kilogram is about 2.2046 pounds.", "1 pound = 0.45359237 kilograms exactly."),
 "area": ("Area Converter", "🟩", "Convert between square meters, square feet, acres, hectares and more.", "m2", "ft2", "An acre is 4,046.86 square meters, and a hectare is 10,000 square meters.", "1 square foot = 0.09290304 square meters exactly."),
 "speed": ("Speed Converter", "🏎️", "Convert between km/h, mph, meters per second and knots.", "kmh", "mph", "To change km/h to mph, divide by 1.609.", "1 mph = 0.44704 meters per second exactly."),
 "volume": ("Volume Converter", "🧪", "Convert between liters, milliliters, gallons, cups and more.", "l", "gal", "A US gallon is 3.785 liters.", "US customary units are used for gallons, cups and ounces."),
}
SHORT = {"length": "Meters, miles, feet & more", "weight": "Kg, pounds, ounces & more", "area": "Sq ft, acres, hectares & more", "speed": "km/h, mph, m/s & knots", "volume": "Liters, gallons, cups & more"}
for key, (nm, ic, lead, f0, t0, ex, fm) in CONV.items():
    opts = [(u[0], u[1]) for u in UNITS[key]]
    title_word = nm.replace(" Converter", "")
    calc(f"{key}-converter", "conv", UNIT, ic, nm, SHORT[key],
         f"{nm} – Convert {title_word} Units Online", lead,
         [num("val", "Value", 1), sel("from", "From", opts, f0), sel("to", "To", opts, t0)],
         info(f"This {nm.lower()} converts values between common units instantly. It also shows the value in every unit at once.",
              "Each unit is converted through a common base unit: value × (from-unit factor) ÷ (to-unit factor). " + fm,
              ex),
         [(f"How accurate is the {nm.lower()}?", "It uses exact or internationally accepted conversion factors, with results shown to several decimal places."),
          ("Can I convert in either direction?", "Yes. Pick any unit in the From and To lists.")],
         head=f"<script>window.UNITS={__import__('json').dumps([[u[0], u[1], u[2]] for u in UNITS[key]])};</script>")

calc("temperature-converter", "temp", UNIT, "🌡️", "Temperature Converter", "Celsius, Fahrenheit & Kelvin",
     "Temperature Converter – Celsius, Fahrenheit & Kelvin",
     "Convert temperatures between Celsius, Fahrenheit and Kelvin.",
     [num("val", "Temperature", 25), sel("from", "From", [("c", "Celsius (°C)"), ("f", "Fahrenheit (°F)"), ("k", "Kelvin (K)")], "c"), sel("to", "To", [("f", "Fahrenheit (°F)"), ("c", "Celsius (°C)"), ("k", "Kelvin (K)")], "f")],
     info("Celsius is used in most of the world, Fahrenheit in the United States and Kelvin in science. This tool converts between all three.",
          "°F = °C × 9 ÷ 5 + 32. °C = (°F − 32) × 5 ÷ 9. K = °C + 273.15.",
          "25°C is 77°F. Water freezes at 0°C (32°F) and boils at 100°C (212°F)."),
     [("What is absolute zero?", "Absolute zero is 0 K, which is −273.15°C or −459.67°F. Nothing can be colder."),
      ("How do I convert Celsius to Fahrenheit quickly?", "Double the Celsius value and add 30 for a rough answer.")])
