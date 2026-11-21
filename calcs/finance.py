from core import *

def L(p, r, y):
    return emi_f(p, r, y)

LOAN_FIELDS = lambda p, r, y: [num("p", f"Loan amount ({CUR})", p), num("r", "Interest rate (% per year)", r, step="0.01"), num("y", "Loan tenure (years)", y, step="0.5")]
LOAN_FAQ = [("How is EMI calculated?", "EMI = P x i x (1+i)^n / ((1+i)^n - 1), where P is the loan amount, i is the monthly interest rate and n is the number of monthly instalments."),
            ("Does a longer tenure reduce my EMI?", "Yes, the monthly EMI falls, but you pay much more interest over the life of the loan. Choose the shortest tenure you can comfortably afford."),
            ("Does the calculator include processing fees?", "No. It shows only principal and interest. Processing fees, insurance and other charges are extra, so ask your lender for the full cost.")]

def loan_body(name, p, r, y, extra=""):
    e = L(p, r, y); t = e * y * 12
    return info(f"This {name} works out your monthly instalment, the total interest you will pay and the total repayment. A year-by-year table shows how much of your payments goes to principal and interest. {extra}",
        "EMI = P x i x (1+i)^n / ((1+i)^n - 1), where P = loan amount, i = annual rate / 12 / 100 and n = tenure in months.",
        f"A loan of {fmt(p)} at {r}% for {y} years has an EMI of {fmt(e)}. You repay {fmt(t)} in total, of which {fmt(t - p)} is interest.")

def loan(slug, name, short, p, r, y, icon, extra="", also=()):
    calc(slug, "loan", "finance", icon, name, short, name, f"Find your monthly EMI, total interest and full repayment for a {r}% loan, with a yearly breakup.",
         LOAN_FIELDS(p, r, y), loan_body(name.lower(), p, r, y, extra), LOAN_FAQ, also=also)

loan("emi-calculator", "EMI Calculator", "Monthly EMI for any loan", 1000000, 9, 10, "calculator")
loan("loan-calculator", "Loan Calculator", "EMI, interest and repayment schedule", 500000, 10.5, 5, "bank")
loan("home-loan-emi-calculator", "Home Loan EMI Calculator", "EMI and yearly breakup for a home loan", 5000000, 8.5, 20, "home",
     "Home loans run for long tenures, so the interest share is highest in the early years.", also=("construction",))
loan("personal-loan-emi-calculator", "Personal Loan EMI Calculator", "EMI for an unsecured personal loan", 300000, 12, 3, "wallet")
loan("car-loan-emi-calculator", "Car Loan EMI Calculator", "EMI for a new or used car loan", 800000, 9.5, 5, "route")
loan("bike-loan-emi-calculator", "Bike Loan EMI Calculator", "EMI for a two-wheeler loan", 120000, 11, 3, "bolt")

# eligibility
inc, ex, r_, y_, f_ = 80000, 10000, 9, 20, 50
mx = inc * f_ / 100 - ex; i_ = r_ / 1200; m_ = y_ * 12
elig = mx * (1 - (1 + i_) ** -m_) / i_
calc("loan-eligibility-calculator", "elig", "finance", "shield", "Loan Eligibility Calculator", "How much loan you can get",
     "Loan Eligibility Calculator", "Estimate the maximum loan a bank may offer based on your income and existing EMIs.",
     [num("inc", f"Monthly income ({CUR})", inc), num("emi", f"Existing monthly EMIs ({CUR})", ex),
      num("r", "Interest rate (% per year)", r_, step="0.01"), num("y", "Tenure (years)", y_, step="0.5"),
      sel("f", "Share of income lenders allow for EMIs (FOIR)", [("40", "40%"), ("45", "45%"), ("50", "50%")], "50")],
     info("Banks limit the total of all your EMIs to a share of your monthly income, called the FOIR (fixed obligations to income ratio), usually 40% to 50%. This calculator turns that limit into a maximum loan amount.",
          "Maximum new EMI = income x FOIR - existing EMIs. Eligible loan = EMI x (1 - (1+i)^-n) / i, where i is the monthly rate and n the months.",
          f"With income of {fmt(inc)}, existing EMIs of {fmt(ex)}, FOIR 50%, rate {r_}% and {y_} years, the maximum new EMI is {fmt(mx)} and the eligible loan is about {fmt(elig)}."),
     [("What is FOIR?", "FOIR is the share of your monthly income that goes to fixed obligations such as EMIs. Most lenders allow 40% to 50%, and a higher income often gets a higher limit."),
      ("Can I increase my loan eligibility?", "Yes. Clear existing loans, add a co-applicant with income, choose a longer tenure or improve your credit score."),
      ("Is this the amount the bank will approve?", "Not necessarily. It is an estimate. The final amount depends on your credit score, age, employment, and the value of the property or asset.")])

FREQ = [("1", "Yearly"), ("2", "Half-yearly"), ("4", "Quarterly"), ("12", "Monthly"), ("365", "Daily")]
def A(p, r, n, y): return p * (1 + r / (100 * n)) ** (n * y)

# interest
p_, r_, y_ = 100000, 8, 5
si = p_ * r_ * y_ / 100; ci = A(p_, r_, 1, y_) - p_
calc("interest-calculator", "interest", "finance", "percent", "Interest Calculator", "Simple or compound interest",
     "Interest Calculator", "Calculate the interest on a deposit or loan using simple or compound interest.",
     [sel("type", "Interest type", [("simple", "Simple interest"), ("compound", "Compound interest")], "simple"),
      num("p", f"Principal ({CUR})", p_), num("r", "Interest rate (% per year)", r_, step="0.01"), num("y", "Time (years)", y_, step="0.25"),
      sel("n", "Compounding", FREQ, "1", when="type=compound")],
     info("Work out how much interest an amount earns (or costs) over time. Pick simple interest, where interest is charged only on the principal, or compound interest, where interest is added to the balance and earns more interest.",
          "Simple: I = P x r x t / 100. Compound: A = P x (1 + r / (100n))^(nt), and interest = A - P, where n is the number of compounding periods per year.",
          f"On {fmt(p_)} at {r_}% for {y_} years, simple interest is {fmt(si)} while yearly compound interest is {fmt(ci, 2)}."),
     [("What is the difference between simple and compound interest?", "Simple interest is calculated only on the original principal. Compound interest is calculated on the principal plus interest already added, so it grows faster."),
      ("Which is used for savings and loans?", "Bank deposits and most loans use compound interest. Some short-term personal loans and bonds use simple interest."),
      ("Can I enter months?", "Yes. Enter the time in years as a decimal, for example 2.5 for two years and six months.")], also=("math",))

# compound
p_, r_, y_ = 100000, 8, 10
calc("compound-interest-calculator", "ci", "finance", "trend", "Compound Interest Calculator", "Growth with compounding",
     "Compound Interest Calculator", "See how your money grows when interest is added back and earns interest, with a year-by-year table.",
     [num("p", f"Principal ({CUR})", p_), num("r", "Interest rate (% per year)", r_, step="0.01"), num("y", "Time (years)", y_, step="0.25"),
      sel("n", "Compounding frequency", FREQ, "12")],
     info("Compound interest means you earn interest on your interest. The more often it compounds, and the longer you stay invested, the faster your money grows.",
          "A = P x (1 + r / (100n))^(nt), where P is the principal, r the yearly rate in percent, n the compounding periods per year and t the years. Compound interest = A - P.",
          f"{fmt(p_)} at {r_}% compounded monthly for {y_} years grows to {fmt(A(p_, r_, 12, y_), 2)}, so the interest earned is {fmt(A(p_, r_, 12, y_) - p_, 2)}."),
     [("How often should interest compound?", "More frequent compounding gives a slightly higher return. Most savings accounts compound quarterly or monthly, and fixed deposits usually compound quarterly."),
      ("What is the rule of 72?", "Divide 72 by the annual rate to estimate how many years it takes to double your money. At 8% it takes about 9 years."),
      ("Is compound interest taxable?", "Interest earned on deposits is usually taxable as income. Check the current rules or ask a tax adviser.")], also=("math",))

# simple
p_, r_, y_ = 100000, 8, 5
calc("simple-interest-calculator", "si", "finance", "percent", "Simple Interest Calculator", "Interest on the principal only",
     "Simple Interest Calculator", "Find simple interest and the total amount for any principal, rate and time.",
     [num("p", f"Principal ({CUR})", p_), num("r", "Interest rate (% per year)", r_, step="0.01"), num("y", "Time (years)", y_, step="0.25")],
     info("Simple interest is charged only on the original amount. It does not grow on itself, so the interest is the same every year.",
          "Simple interest = P x R x T / 100, and Total amount = P + Simple interest, where R is the yearly rate in percent and T is time in years.",
          f"{fmt(p_)} at {r_}% for {y_} years earns {fmt(p_ * r_ * y_ / 100)} in interest, for a total of {fmt(p_ + p_ * r_ * y_ / 100)}."),
     [("What is the simple interest formula?", "SI = P x R x T / 100. Multiply the principal by the rate and the time in years, then divide by 100."),
      ("How do I use months?", "Convert months to years by dividing by 12. For 18 months, enter 1.5."),
      ("Is simple interest lower than compound interest?", "Yes, for the same rate and time. Compound interest adds interest to the balance, so it grows faster.")], also=("math",))

# SIP
def sip(m, r, y, g=0):
    bal = 0; pay = m; i = r / 1200
    for k in range(1, y * 12 + 1):
        if k > 1 and (k - 1) % 12 == 0: pay *= 1 + g / 100
        bal = (bal + pay) * (1 + i)
    return bal
m_, r_, y_ = 10000, 12, 15
v = sip(m_, r_, y_)
calc("sip-calculator", "sip", "finance", "trend", "SIP Calculator", "Future value of monthly investing",
     "SIP Calculator", "Estimate what a monthly SIP in mutual funds could grow to, with an optional yearly step-up.",
     [num("p", f"Monthly investment ({CUR})", m_), num("r", "Expected return (% per year)", r_, step="0.1"), num("y", "Investment period (years)", y_, step="1"),
      num("step", "Yearly increase in SIP (%)", 0, step="1")],
     info("A Systematic Investment Plan (SIP) invests a fixed amount every month. This calculator estimates the future value for an expected yearly return. You can also add a yearly step-up if you plan to raise your SIP as your income grows.",
          "Future value = P x ((1+i)^n - 1) / i x (1+i), where P is the monthly amount, i = annual return / 12 / 100 and n the number of months. With a step-up, the monthly amount is raised each year and each month is compounded separately.",
          f"A SIP of {fmt(m_)} a month for {y_} years at {r_}% invests {fmt(m_ * y_ * 12)} and grows to about {fmt(v)}, so estimated returns are {fmt(v - m_ * y_ * 12)}."),
     [("Are SIP returns guaranteed?", "No. Mutual fund returns depend on the market. The calculator shows an estimate based on the return you enter."),
      ("What return should I assume?", "Equity funds have historically varied a lot. Use a modest, realistic figure and try a few values to see the range."),
      ("What is a step-up SIP?", "A step-up SIP raises your monthly amount by a fixed percentage every year. Even a 10% increase can add a lot to the final value over a long period.")],
     also=())

# SWP
calc("swp-calculator", "swp", "finance", "arrow-down", "SWP Calculator", "Systematic withdrawal plan",
     "SWP Calculator", "See how long your investment lasts and what is left when you withdraw a fixed amount every month.",
     [num("p", f"Total investment ({CUR})", 2000000), num("w", f"Monthly withdrawal ({CUR})", 15000), num("r", "Expected return (% per year)", 8, step="0.1"), num("y", "Withdrawal period (years)", 15, step="1")],
     info("A Systematic Withdrawal Plan (SWP) lets you take a fixed amount from your investment each month while the rest stays invested. This calculator shows the final balance and whether your money lasts.",
          "Every month: balance = (balance - withdrawal) x (1 + monthly return), where the monthly return is the annual return divided by 12. The process repeats for every month of the period.",
          "A corpus of " + fmt(2000000) + " with " + fmt(15000) + " withdrawn each month at 8% a year is checked month by month, and the table shows the balance at the end of every year."),
     [("What is an SWP?", "It is a facility in mutual funds that pays you a fixed amount regularly by selling some units. It is often used to create a monthly income."),
      ("How do I make my money last longer?", "Withdraw less each month, or invest for a higher return. A withdrawal rate of about 4% a year of the corpus is often used as a rough guide."),
      ("Is the withdrawal taxable?", "Gains in the amount withdrawn may be taxable as capital gains. Check the current rules or ask a tax adviser.")])

# FD
p_, r_, y_ = 100000, 7, 5
calc("fd-calculator", "fd", "finance", "bank", "FD Calculator", "Fixed deposit maturity amount",
     "FD Calculator", "Find the maturity amount and interest on a fixed deposit.",
     [num("p", f"Deposit amount ({CUR})", p_), num("r", "Interest rate (% per year)", r_, step="0.01"), num("y", "Tenure (years)", y_, step="0.25"),
      sel("n", "Compounding", [("1", "Yearly"), ("2", "Half-yearly"), ("4", "Quarterly"), ("12", "Monthly")], "4")],
     info("A fixed deposit (FD) pays a fixed rate of interest for a fixed time. Most banks compound FD interest every quarter, which is the default here.",
          "Maturity amount = P x (1 + r / (100n))^(nt), where P is the deposit, r the yearly rate, n the compounding periods per year and t the years.",
          f"A deposit of {fmt(p_)} at {r_}% compounded quarterly for {y_} years matures to {fmt(A(p_, r_, 4, y_))}, so you earn {fmt(A(p_, r_, 4, y_) - p_)} in interest."),
     [("How is FD interest calculated?", "Banks usually compound FD interest quarterly. The calculator uses the compound interest formula with the compounding frequency you choose."),
      ("Is FD interest taxable?", "Yes. FD interest is added to your income and taxed at your slab rate. Banks may deduct TDS above a limit."),
      ("Which compounding should I pick?", "Quarterly matches most banks. Check your bank's terms, since cumulative and payout FDs differ.")])

# RD
def RD(p, r, y):
    i = r / 400; n = y * 4
    return p * ((1 + i) ** n - 1) / (1 - (1 + i) ** (-1 / 3))
p_, r_, y_ = 5000, 6.5, 5
calc("rd-calculator", "rd", "finance", "repeat", "RD Calculator", "Recurring deposit maturity amount",
     "RD Calculator", "Find the maturity value of a recurring deposit with a fixed monthly instalment.",
     [num("p", f"Monthly deposit ({CUR})", p_), num("r", "Interest rate (% per year)", r_, step="0.01"), num("y", "Tenure (years)", y_, step="0.25")],
     info("A recurring deposit (RD) lets you save a fixed amount every month and earn interest like a fixed deposit. Indian banks compound RD interest quarterly.",
          "Maturity = P x ((1+i)^n - 1) / (1 - (1+i)^(-1/3)), where P is the monthly deposit, i = annual rate / 400 (the quarterly rate) and n is the number of quarters.",
          f"A monthly deposit of {fmt(p_)} at {r_}% for {y_} years totals {fmt(p_ * 12 * y_)} deposited and matures to about {fmt(RD(p_, r_, y_))}."),
     [("How is RD interest compounded?", "In India, banks usually compound RD interest every quarter. Each monthly deposit earns interest for its own remaining time."),
      ("What if I miss an instalment?", "Banks charge a small penalty for late instalments, and too many misses can close the RD early."),
      ("RD or SIP: which is better?", "An RD gives a fixed, safe return. A SIP in mutual funds can earn more over time but its returns are not guaranteed.")])
