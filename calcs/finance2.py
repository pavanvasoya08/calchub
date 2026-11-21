from core import *

# ---- PPF ----
bal = 0
for _ in range(15):
    bal = (bal + 150000) * 1.071
calc("ppf-calculator", "ppf", "finance", "bank", "PPF Calculator", "Maturity value of your Public Provident Fund",
     "PPF Calculator", "Find the maturity value of your Public Provident Fund account with yearly deposits and compounding interest.",
     [num("dep", f"Yearly deposit ({CUR}, max 1,50,000)", 150000), num("rate", "Interest rate (% per year)", 7.1), num("yrs", "Years (minimum 15)", 15, step="1", min="15")],
     info("The Public Provident Fund is a government-backed savings scheme with a 15-year lock-in. Interest is tax-free and compounds every year, which makes it a popular long-term savings choice.",
          "Each year: Interest = (Opening balance + Deposit) x Rate. Closing balance = Opening balance + Deposit + Interest. The yearly deposit is limited to Rs 1,50,000.",
          f"Depositing {fmt(150000)} every year for 15 years at 7.1% gives a maturity value of about {fmt(bal)}, with {fmt(150000*15)} invested."),
     [("What is the PPF interest rate?", "The government announces the rate every quarter. The default here is 7.1%, but you can change it to match the current rate."),
      ("How much can I deposit in PPF each year?", "You can deposit between Rs 500 and Rs 1,50,000 in a financial year."),
      ("Can I extend PPF after 15 years?", "Yes, the account can be extended in blocks of 5 years, with or without fresh deposits. Enter a longer period to see the effect.")], also=())

# ---- GST ----
calc("gst-calculator", "gst", "finance", "receipt", "GST Calculator", "Add or remove GST from any price",
     "GST Calculator", "Add GST to a price or remove it from a GST-inclusive price, with the CGST and SGST split.",
     [sel("mode", "What do you want to do?", [("add", "Add GST to the price"), ("remove", "Remove GST from the price")], "add"),
      num("amt", f"Amount ({CUR})", 1000), sel("rate", "GST rate", [("0", "0%"), ("3", "3%"), ("5", "5%"), ("12", "12%"), ("18", "18%"), ("28", "28%")], "18")],
     info("Goods and Services Tax (GST) is added to the price of most goods and services in India. This calculator adds GST to a base price or works backwards from a price that already includes GST.",
          "Add GST: GST = Price x Rate / 100, Total = Price + GST. Remove GST: Base price = Total / (1 + Rate / 100), GST = Total - Base price.",
          f"A price of {fmt(1000)} plus 18% GST gives GST of {fmt(180)} and a total of {fmt(1180)}. A GST-inclusive price of {fmt(1180)} has a base price of {fmt(1000)}."),
     [("What are the GST rates in India?", "The common slabs are 0%, 5%, 12%, 18% and 28%, with 3% on items like gold. The slab for a product depends on its category."),
      ("What are CGST and SGST?", "For sales within a state, GST is split equally between the Centre (CGST) and the State (SGST). For interstate sales it is charged as IGST."),
      ("How do I find the price before GST?", "Choose Remove GST, enter the GST-inclusive price and select the rate. The tool divides by 1 plus the rate.")], also=("business",))

# ---- Income tax ----
calc("income-tax-calculator", "itax", "finance", "clipboard", "Income Tax Calculator", "Compare new and old tax regimes for FY 2026-27",
     "Income Tax Calculator (FY 2026-27)", "Estimate your income tax under the new and old regimes and see which one saves more.",
     [num("inc", f"Annual gross income ({CUR})", 1500000), sel("age", "Age group (old regime)", [("0", "Below 60"), ("60", "60 to 79"), ("80", "80 and above")], "0"),
      num("c80", f"80C investments ({CUR}, max 1,50,000)", 150000), num("d80", f"80D health insurance ({CUR})", 25000), num("nps", f"NPS 80CCD(1B) ({CUR}, max 50,000)", 0),
      num("hl", f"Home loan interest ({CUR}, max 2,00,000)", 0), num("hra", f"HRA exemption ({CUR})", 0), num("oth", f"Other deductions ({CUR})", 0)],
     info("This calculator compares your tax under the new regime (default) and the old regime for FY 2026-27 (AY 2027-28). Deductions in the form only apply to the old regime.",
          "New regime slabs: up to 4 lakh nil, 4-8 lakh 5%, 8-12 lakh 10%, 12-16 lakh 15%, 16-20 lakh 20%, 20-24 lakh 25%, above 24 lakh 30%. Standard deduction is Rs 75,000, and the 87A rebate makes income up to Rs 12 lakh tax-free. Old regime slabs: up to 2.5 lakh nil, 2.5-5 lakh 5%, 5-10 lakh 20%, above 10 lakh 30%, with a Rs 50,000 standard deduction. Cess of 4% is added in both.",
          "On a gross income of Rs 15,00,000 the new regime taxable income is Rs 14,25,000. Tax on slabs is Rs 90,000 (Rs 20,000 + Rs 40,000 + Rs 30,000), and with 4% cess the total is Rs 93,600."),
     [("Is income up to Rs 12 lakh really tax-free?", "Under the new regime, the 87A rebate makes tax nil when taxable income is up to Rs 12 lakh. With the Rs 75,000 standard deduction, a salaried person with an income of Rs 12.75 lakh pays no tax."),
      ("Which regime is better?", "The new regime usually wins unless your total deductions are large (for example 80C, HRA, home loan interest and health insurance together). This calculator shows both so you can compare."),
      ("Does the result include surcharge?", "No. Surcharge applies only on very high incomes, above Rs 50 lakh. Always confirm the final figure with the Income Tax Department or a tax adviser.")], also=("business",))

# ---- Salary ----
calc("salary-calculator", "salary", "finance", "wallet", "Salary Calculator", "Convert CTC into monthly in-hand salary",
     "Salary Calculator (CTC to In-hand)", "Find your monthly take-home salary from your annual CTC after PF, professional tax and income tax.",
     [num("ctc", f"Annual CTC ({CUR})", 1000000), num("basic", "Basic salary (% of CTC)", 40, step="1"), num("hra", "HRA (% of basic)", 40, step="1"), num("pt", f"Professional tax ({CUR} per month)", 200)],
     info("Your CTC (cost to company) is not what reaches your bank account. Employer PF, employee PF, professional tax and income tax are all taken out first. This tool estimates the monthly in-hand amount.",
          "Gross salary = CTC - Employer PF. PF = 12% of basic (both employer and employee). In-hand = Gross - Employee PF - Professional tax - Income tax. Income tax uses the new regime with the Rs 75,000 standard deduction.",
          "For a CTC of Rs 10,00,000 with 40% basic, the basic is Rs 4,00,000 and PF is Rs 48,000. Gross is Rs 9,52,000, income tax is nil under the 12 lakh rebate, and the monthly in-hand is about Rs 77,000 after Rs 2,400 yearly professional tax."),
     [("What is the difference between CTC and in-hand salary?", "CTC is the total yearly cost to the employer, including PF and benefits. In-hand salary is the amount credited to your account after all deductions."),
      ("Why is my actual salary different from this estimate?", "Companies structure salary differently. Bonuses, insurance, gratuity and variable pay change the actual figure. Use this as a close estimate."),
      ("Is the tax calculation exact?", "It is a simple new-regime estimate with only the standard deduction. For a full comparison use the income tax calculator.")], also=())

# ---- Inflation ----
calc("inflation-calculator", "infl", "finance", "trend", "Inflation Calculator", "See future prices and falling purchasing power",
     "Inflation Calculator", "Find how much the same goods will cost in the future and how much your money will be worth.",
     [num("amt", f"Amount today ({CUR})", 100000), num("rate", "Average inflation (% per year)", 6), num("yrs", "Years", 10, step="1")],
     info("Inflation makes prices rise over time, so the same amount of money buys less. This tool shows the future cost of something that costs a fixed amount today, and the buying power of your money.",
          "Future cost = Amount x (1 + Inflation)^Years. Buying power = Amount / (1 + Inflation)^Years.",
          f"Something that costs {fmt(100000)} today will cost about {fmt(100000*1.06**10)} after 10 years at 6% inflation. Your {fmt(100000)} will only buy goods worth {fmt(100000/1.06**10)} in today's terms."),
     [("What inflation rate should I use?", "India's long-term average is around 5% to 6% a year. Use a higher rate for education and healthcare costs."),
      ("How can I beat inflation?", "Investments that earn more than inflation after tax, such as equity funds over the long term, preserve buying power. Savings accounts often earn less than inflation."),
      ("Is inflation the same for everything?", "No. Food, fuel, rent, education and healthcare all rise at different rates. Use the rate that fits your expense.")], also=())

# ---- Profit & loss ----
calc("profit-loss-calculator", "pl", "finance", "scale", "Profit & Loss Calculator", "Profit or loss amount and percentage",
     "Profit and Loss Calculator", "Enter a cost price and a selling price to see your profit or loss as an amount and a percentage.",
     [num("cp", f"Cost price per unit ({CUR})", 800), num("sp", f"Selling price per unit ({CUR})", 1000), num("qty", "Quantity", 1, step="1", min="1")],
     info("Use this tool to check if a sale makes a profit or a loss. It gives the amount, the percentage on cost price, and the margin on selling price.",
          "Profit = Selling price - Cost price. Profit % = Profit / Cost price x 100. Margin % = Profit / Selling price x 100. If the selling price is lower than the cost price, the same formulas give a loss.",
          f"Buying at {fmt(800)} and selling at {fmt(1000)} gives a profit of {fmt(200)}, which is 25% on cost and 20% margin on selling price."),
     [("What is the difference between profit % and margin %?", "Profit % is based on cost price. Margin % is based on selling price, so it is always lower than profit % for a profitable sale."),
      ("How do I calculate loss percentage?", "Loss % = (Cost price - Selling price) / Cost price x 100. Enter the lower selling price to see it."),
      ("Does this include expenses?", "Only the prices you enter. Add shipping, packaging or other costs to the cost price for the true result.")], also=("business",))

# ---- Discount ----
calc("discount-calculator", "disc", "finance", "tag", "Discount Calculator", "Final price and savings after a discount",
     "Discount Calculator", "Find the sale price and how much you save after one or two discounts.",
     [num("price", f"Original price ({CUR})", 2000), num("d", "Discount (%)", 20), num("d2", "Extra discount (%, optional)", 0)],
     info("Enter the original price and the discount to see the price you pay and how much you save. You can add a second discount, such as a coupon on top of a sale.",
          "Savings = Price x Discount / 100. Final price = Price - Savings. For a second discount, it is applied on the already reduced price.",
          f"A {fmt(2000)} item with 20% off costs {fmt(1600)}, so you save {fmt(400)}. With an extra 10% off, the price falls to {fmt(1440)}."),
     [("How do I calculate a discount?", "Multiply the price by the discount percentage and divide by 100. Subtract the result from the price."),
      ("Is 20% + 10% the same as 30% off?", "No. The second discount is applied on the reduced price, so 20% and 10% together equal 28% off."),
      ("Can I find the discount percentage from two prices?", "Yes. Discount % = (Original price - Sale price) / Original price x 100.")], also=("shopping",))

# ---- Brokerage ----
calc("brokerage-calculator", "brk", "finance", "bars", "Brokerage Calculator", "Net profit after all share trading charges",
     "Brokerage Calculator", "Work out brokerage, STT, taxes and your breakeven price for equity delivery and intraday trades.",
     [sel("type", "Trade type", [("delivery", "Equity delivery"), ("intra", "Equity intraday")], "delivery"),
      num("buy", f"Buy price ({CUR})", 500), num("sell", f"Sell price ({CUR})", 520), num("qty", "Quantity", 100, step="1", min="1"),
      num("brk", "Brokerage (% per side)", 0.03, step="0.001"), num("cap", f"Intraday brokerage cap per order ({CUR})", 20), num("ex", "Exchange charges (%)", 0.00297, step="0.00001")],
     info("Every share trade has brokerage, STT, exchange charges, GST, SEBI fees and stamp duty. These costs reduce your profit, so this calculator shows your real net result and the breakeven selling price.",
          "Brokerage = Turnover x Rate (capped for intraday). STT is 0.1% on buy and sell for delivery and 0.025% on sell for intraday. Exchange charges and SEBI fees apply on total turnover. GST is 18% of brokerage, exchange and SEBI charges. Stamp duty is 0.015% (delivery) or 0.003% (intraday) on buy.",
          "Buying 100 shares at Rs 500 and selling at Rs 520 gives a gross profit of Rs 2,000. After brokerage, STT, exchange charges, GST, SEBI and stamp duty, the net profit is a little under Rs 1,900 for a delivery trade."),
     [("What is the breakeven price?", "It is the selling price at which your net profit after all charges is zero. Selling above it makes a profit."),
      ("Do charges differ between brokers?", "Yes. Brokerage varies by broker, while STT, stamp duty and exchange charges are set by regulators and exchanges. Edit the inputs to match your broker."),
      ("Are these figures exact?", "They are close estimates. Rates change over time, so check your contract note for the final amounts.")], also=())

# ---- Stock average ----
lots = [(100, 50), (60, 40)]
calc("stock-average-calculator", "savg", "finance", "repeat", "Stock Average Calculator", "Average buy price across your purchases",
     "Stock Average Calculator", "Find your average buying price across many purchases and see the effect of buying more shares.",
     [num("p1", f"Purchase 1 price ({CUR})", 100), num("q1", "Purchase 1 quantity", 50, step="1"), num("p2", f"Purchase 2 price ({CUR})", 80), num("q2", "Purchase 2 quantity", 40, step="1"),
      num("p3", f"Purchase 3 price ({CUR})", 0), num("q3", "Purchase 3 quantity", 0, step="1"), num("p4", f"Purchase 4 price ({CUR})", 0), num("q4", "Purchase 4 quantity", 0, step="1"),
      num("p5", f"Purchase 5 price ({CUR})", 0), num("q5", "Purchase 5 quantity", 0, step="1"), num("np", f"New purchase price ({CUR}, optional)", 70), num("nq", "New purchase quantity", 30, step="1")],
     info("When you buy the same stock at different prices, your average cost changes. Use this tool to find it and to see how buying more at a lower price brings it down.",
          "Average price = Total amount invested / Total quantity. Total amount is the sum of price x quantity for each purchase.",
          f"50 shares at {fmt(100)} and 40 shares at {fmt(80)} cost {fmt(8200)} for 90 shares, an average of {fmt(8200/90,2)}. Buying 30 more at {fmt(70)} lowers the average to {fmt(10300/120,2)}."),
     [("What is averaging down?", "Buying more shares of a stock after its price falls to lower your average cost. It reduces the break-even level but increases your exposure."),
      ("How many purchases can I enter?", "Up to five existing purchases plus one new purchase. Leave unused rows at 0."),
      ("Does it include brokerage?", "No. Add charges to the price if you want a cost-inclusive average.")], also=())

# ---- Stock profit ----
calc("stock-profit-calculator", "sprofit", "finance", "trend", "Stock Profit Calculator", "Profit or loss on a share trade",
     "Stock Profit Calculator", "Calculate your profit or loss and return percentage on a share trade, including charges.",
     [num("buy", f"Buy price ({CUR})", 250), num("sell", f"Sell price ({CUR})", 290), num("qty", "Quantity", 100, step="1", min="1"), num("ch", "Total charges (% of buy + sell value)", 0.1, step="0.01")],
     info("Enter your buy price, sell price and quantity to see the gain or loss on a trade. Add an estimate of charges to see the net result.",
          "Gross profit = (Sell price - Buy price) x Quantity. Net profit = Gross profit - Charges. Return % = Net profit / Invested amount x 100.",
          f"Buying 100 shares at {fmt(250)} and selling at {fmt(290)} gives a gross profit of {fmt(4000)}. Charges of 0.1% on {fmt(54000)} are {fmt(54)}, so the net profit is {fmt(3946)}, a return of {nf(3946/25000*100)}%."),
     [("What charges should I include?", "Brokerage, STT, exchange fees, GST, SEBI fees and stamp duty. Around 0.1% is a rough figure for delivery trades. Use the brokerage calculator for an exact split."),
      ("Is profit on shares taxed?", "Yes. Short-term and long-term capital gains tax rules apply depending on the holding period. This tool does not calculate tax."),
      ("Can I use it for losses?", "Yes. If the sell price is lower than the buy price the result shows a negative number.")], also=())

# ---- Mutual fund ----
f1 = 100000 * 1.12 ** 10
i = 1.12 ** (1 / 12) - 1
f2 = 10000 * ((1 + i) ** 120 - 1) / i * (1 + i)
calc("mutual-fund-returns-calculator", "mfr", "finance", "pie", "Mutual Fund Returns Calculator", "Lump sum, SIP and CAGR returns",
     "Mutual Fund Returns Calculator", "Estimate the future value of a lump sum or SIP, or find the CAGR of an investment you already hold.",
     [sel("mode", "Calculate", [("lump", "Lump sum maturity value"), ("sip", "SIP maturity value"), ("cagr", "CAGR of an investment")], "sip"),
      num("amt", f"Investment amount ({CUR}, lump sum or monthly SIP)", 10000, when="mode=lump|sip"), num("rate", "Expected return (% per year)", 12, when="mode=lump|sip"),
      num("inv", f"Amount invested ({CUR})", 100000, when="mode=cagr"), num("fv", f"Current value ({CUR})", 180000, when="mode=cagr"), num("yrs", "Years", 10, step="any")],
     info("Estimate how much a mutual fund investment can grow, or measure the yearly growth rate you earned. Returns from mutual funds are market-linked, so these are estimates and not guarantees.",
          "Lump sum: Future value = Amount x (1 + Rate)^Years. SIP: instalments are compounded monthly at the equivalent monthly rate. CAGR = (Final value / Invested)^(1 / Years) - 1.",
          f"A lump sum of {fmt(100000)} at 12% for 10 years grows to about {fmt(f1)}. A SIP of {fmt(10000)} a month at 12% for 10 years grows to about {fmt(f2)} on {fmt(1200000)} invested."),
     [("What is CAGR?", "Compound annual growth rate is the constant yearly rate that takes an investment from its start value to its end value over a period."),
      ("Are mutual fund returns guaranteed?", "No. Returns depend on market performance. Past returns do not guarantee future results."),
      ("What is the difference between lump sum and SIP?", "A lump sum invests the whole amount at once. A SIP invests a fixed amount every month, which spreads your purchase price over time.")], also=())
