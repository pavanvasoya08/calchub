from core import *

def B(slug, js, icon, name, short, lead, fields, what, formula, example, faqs, also=(), h1=None):
    calc(slug, js, "business", icon, name, short, h1 or name, lead, fields, info(what, formula, example), faqs, also=also)

# 1 profit margin
p, c = 1500, 1000
B("profit-margin-calculator", "margin", "percent", "Profit Margin Calculator", "Profit, margin % and markup %",
  "Enter your selling price and cost to see profit, profit margin and markup at once.",
  [num("price", f"Selling price ({CUR})", p), num("cost", f"Cost price ({CUR})", c)],
  "Shows how much profit you make on each sale, as an amount, as a share of the selling price (margin) and as a share of the cost (markup).",
  "Profit = selling price - cost. Margin % = profit / selling price x 100. Markup % = profit / cost x 100.",
  f"Selling for {fmt(p)} an item that costs {fmt(c)} gives a profit of {fmt(p-c)}, a margin of {nf((p-c)/p*100,1)}% and a markup of {nf((p-c)/c*100,1)}%.",
  [("What is the difference between margin and markup?", "Margin is profit as a percentage of the selling price. Markup is profit as a percentage of the cost. The same sale always has a higher markup than margin."),
   ("What is a good profit margin?", "It depends on the industry. Retail often runs 20-50% gross margin, while software can exceed 70%. Compare with businesses like yours."),
   ("Is this gross or net margin?", "It is a gross margin on one product, using only the cost you enter. Rent, salaries and other overheads are not included.")])

# 2 markup
cost, mk = 800, 40
B("markup-calculator", "markup", "trend", "Markup Calculator", "Selling price from cost and markup %",
  "Add a markup percentage to your cost to get the selling price, profit and equivalent margin.",
  [num("cost", f"Cost price ({CUR})", cost), num("mk", "Markup (%)", mk)],
  "Finds the selling price you need when you add a fixed percentage on top of your cost.",
  "Selling price = cost x (1 + markup / 100). Profit = selling price - cost. Equivalent margin = profit / selling price x 100.",
  f"A cost of {fmt(cost)} with a {mk}% markup gives a price of {fmt(cost*1.4)}, a profit of {fmt(cost*0.4)} and a margin of {nf(40/140*100,1)}%.",
  [("How do I convert markup to margin?", "Margin = markup / (100 + markup) x 100. A 25% markup equals a 20% margin."),
   ("Why is my margin lower than my markup?", "Markup uses cost as the base, margin uses the selling price. The selling price is larger, so the percentage is smaller."),
   ("Can markup be above 100%?", "Yes. A product sold for three times its cost has a 200% markup. Margin can never reach 100%.")])

# 3 selling price
cost, pct = 600, 30
B("selling-price-calculator", "selling", "tag", "Selling Price Calculator", "Price needed for your target margin or markup",
  "Work out the selling price that gives the profit margin or markup you want.",
  [num("cost", f"Cost per unit ({CUR})", cost), sel("mode", "Target type", [("margin", "Profit margin"), ("markup", "Markup")], "margin"), num("pct", "Target (%)", pct)],
  "Use it to price a product so it earns a specific margin or markup after your costs.",
  "For margin: price = cost / (1 - margin / 100). For markup: price = cost x (1 + markup / 100).",
  f"To earn a {pct}% margin on a {fmt(cost)} cost, sell at {fmt(cost/(1-pct/100),2)}. The profit is {fmt(cost/(1-pct/100)-cost,2)} per unit.",
  [("Should I price by margin or markup?", "Margin tells you what share of each sale is profit, which is easier to compare with expenses. Markup is quicker for adding a fixed percentage to cost."),
   ("Does the price include tax?", "No. Add GST or VAT separately with the GST or VAT calculator."),
   ("What costs should I include?", "Include product cost plus packaging, shipping and platform fees for an accurate price.")])

# 4 cost price
sp, pct = 1200, 20
B("cost-price-calculator", "costprice", "receipt", "Cost Price Calculator", "Find the cost from selling price and profit %",
  "Find the original cost price when you know the selling price and the profit percentage.",
  [num("sp", f"Selling price ({CUR})", sp), num("pct", "Profit (%)", pct), sel("base", "Profit % is on", [("cost", "Cost price"), ("sp", "Selling price")], "cost")],
  "Works backwards from the selling price to the cost price.",
  "If profit is on cost: cost = selling price / (1 + profit / 100). If profit is on selling price: cost = selling price x (1 - profit / 100).",
  f"Selling price {fmt(sp)} with a {pct}% profit on cost means a cost of {fmt(sp/1.2,2)} and a profit of {fmt(sp-sp/1.2,2)}.",
  [("What if I sold at a loss?", "Enter a negative profit percentage, for example -10 for a 10% loss."),
   ("Is profit usually on cost or selling price?", "In school maths, profit % is on cost. In business reports, margin is on the selling price. Pick the right base above."),
   ("Why is the cost not simply price minus percent?", "Because the percentage applies to a different base. Dividing by (1 + profit %) gives the correct cost.")])

# 5 vat
amt = 1000
B("vat-calculator", "vat", "percent", "VAT Calculator", "Add or remove VAT from a price",
  "Add VAT to a net price or remove it from a VAT-inclusive price. Default rate is 20%.",
  [num("amt", f"Amount ({CUR})", amt), num("rate", "VAT rate (%)", 20, step="0.01"), sel("mode", "Calculation", [("add", "Add VAT to price"), ("remove", "Remove VAT from price")], "add")],
  "Quickly finds the VAT amount and the price with and without VAT.",
  "Price with VAT = net price x (1 + rate / 100). Net price = gross price / (1 + rate / 100). VAT = gross - net.",
  f"Adding 20% VAT to {fmt(amt)} gives {fmt(1200)}, where VAT is {fmt(200)}. Removing 20% VAT from {fmt(1200)} gives {fmt(1000)}.",
  [("What VAT rate should I use?", "Use the standard rate for your country and product. Many countries have reduced rates for food, books or services."),
   ("Is VAT the same as GST?", "They work the same way: both tax the value added at each stage. India uses GST; many other countries use VAT."),
   ("Why can't I just subtract 20% from a VAT-inclusive price?", "Because VAT is 20% of the net price, not of the gross price. You must divide by 1.20.")])

# 6 gst incl/excl
amt = 5000
B("gst-inclusive-exclusive-calculator", "gstie", "receipt", "GST Inclusive/Exclusive Calculator", "Add or remove GST with CGST/SGST split",
  "Convert between GST-exclusive and GST-inclusive prices and see the CGST, SGST or IGST split.",
  [num("amt", f"Amount ({CUR})", amt), sel("rate", "GST rate", [("0", "0%"), ("5", "5%"), ("12", "12%"), ("18", "18%"), ("28", "28%")], "18"),
   sel("mode", "Amount is", [("excl", "GST exclusive (add GST)"), ("incl", "GST inclusive (remove GST)")], "excl"),
   sel("supply", "Supply type", [("intra", "Within state (CGST + SGST)"), ("inter", "Between states (IGST)")], "intra")],
  "Use it on invoices to get the base price, total GST and the tax split for either kind of supply.",
  "GST-exclusive to inclusive: final = base x (1 + rate / 100). Inclusive to exclusive: base = final / (1 + rate / 100). Within a state, GST splits equally into CGST and SGST; between states it is IGST.",
  f"Adding 18% GST to {fmt(amt)} gives {fmt(amt*1.18)}. The GST is {fmt(amt*0.18)}, split into {fmt(amt*0.09)} CGST and {fmt(amt*0.09)} SGST.",
  [("What is the difference between CGST, SGST and IGST?", "CGST goes to the central government and SGST to the state when a sale is within one state. IGST is charged on sales between states or imports."),
   ("Which GST rate applies to my product?", "It depends on the HSN code of the item. Check the official GST rate finder or ask your accountant."),
   ("Is there a separate GST calculator?", "Yes, the main GST Calculator in the Finance category does the same maths with a simpler form.")], also=("finance",))

# 7 break even
fixed, price, vc, tg = 50000, 250, 150, 0
B("break-even-calculator", "breakeven", "scale", "Break-Even Calculator", "Units and revenue needed to cover costs",
  "Find how many units you must sell to cover your fixed costs, and the units needed for a target profit.",
  [num("fixed", f"Fixed costs ({CUR})", fixed), num("price", f"Selling price per unit ({CUR})", price), num("vc", f"Variable cost per unit ({CUR})", vc), num("target", f"Target profit ({CUR}, optional)", tg)],
  "Shows the sales volume where your total revenue equals your total costs, so you neither gain nor lose.",
  "Contribution per unit = price - variable cost. Break-even units = fixed costs / contribution per unit (rounded up). Break-even revenue = units x price.",
  f"With fixed costs of {fmt(fixed)}, a price of {fmt(price)} and a variable cost of {fmt(vc)}, the contribution is {fmt(100)} per unit. You break even at {nf(500,0)} units, or {fmt(125000)} of revenue.",
  [("What counts as a fixed cost?", "Costs that stay the same whatever you sell, such as rent, salaries and software subscriptions."),
   ("What counts as a variable cost?", "Costs that rise with each unit sold, such as materials, packaging and per-order shipping."),
   ("How can I lower my break-even point?", "Raise the price, cut variable costs or reduce fixed costs. Each one lowers the units you need to sell.")])

# 8 revenue
price, units, disc, ret = 499, 200, 10, 5
g = price*units; d = g*disc/100; r = (g-d)*ret/100; n = g-d-r
B("revenue-calculator", "revenue", "bars", "Revenue Calculator", "Gross and net revenue from price and units",
  "Estimate gross revenue, discounts, returns and net revenue from your price and sales volume.",
  [num("price", f"Price per unit ({CUR})", price), num("units", "Units sold", units), num("disc", "Average discount (%)", disc), num("ret", "Return rate (%)", ret)],
  "Turns price and volume into revenue, after discounts and returns.",
  "Gross revenue = price x units. Discounts = gross x discount %. Returns = (gross - discounts) x return %. Net revenue = gross - discounts - returns.",
  f"Selling {units} units at {fmt(price)} gives gross revenue of {fmt(g)}. After a {disc}% discount ({fmt(d)}) and {ret}% returns ({fmt(r,2)}), net revenue is {fmt(n,2)}.",
  [("What is the difference between revenue and profit?", "Revenue is the money coming in from sales. Profit is what remains after all costs are paid."),
   ("What is net revenue?", "Sales after discounts, returns and allowances are deducted from gross sales."),
   ("Why multiply by 12?", "The last tile assumes you repeat the same volume every month for a year, as a rough yearly view.")])

# 9 commission
sales, r1 = 200000, 5
B("commission-calculator", "commission", "users", "Commission Calculator", "Flat or tiered sales commission",
  "Calculate sales commission at a flat rate or with a higher rate above a sales threshold.",
  [num("sales", f"Total sales ({CUR})", sales), sel("mode", "Commission type", [("flat", "Flat rate"), ("tier", "Tiered (two rates)")], "flat"),
   num("r1", "Commission rate (%)", r1, step="0.01"), num("limit", f"Tier threshold ({CUR})", 100000, when="mode=tier"), num("r2", "Rate above threshold (%)", 8, when="mode=tier", step="0.01")],
  "Helps sales teams, agents and marketplaces work out earned commission.",
  "Flat: commission = sales x rate. Tiered: commission = sales up to the threshold x rate 1 + sales above it x rate 2.",
  f"A flat {r1}% on {fmt(sales)} of sales earns {fmt(sales*r1/100)}. With a tier at {fmt(100000)} and 8% above it, you would earn {fmt(100000*.05+100000*.08)}.",
  [("What is the effective commission rate?", "It is total commission divided by total sales. It matters most in tiered plans."),
   ("Is commission taxable?", "Usually yes. It counts as income, and TDS may apply. Check your local tax rules."),
   ("Are commissions paid on gross or net sales?", "That is set by your agreement. Some plans exclude returns, taxes or discounts, so enter the amount your plan uses.")])

# 10 roas
spend, rev, m = 20000, 100000, 30
B("roas-calculator", "roas", "target", "ROAS Calculator", "Return on ad spend and break-even ROAS",
  "Measure how much revenue each unit of ad spend brings in and find your break-even ROAS.",
  [num("spend", f"Ad spend ({CUR})", spend), num("rev", f"Revenue from ads ({CUR})", rev), num("margin", "Profit margin (%)", m)],
  "ROAS tells you if your advertising is profitable, especially when compared with your break-even point.",
  "ROAS = ad revenue / ad spend. ACOS = ad spend / ad revenue x 100. Break-even ROAS = 1 / profit margin.",
  f"{fmt(spend)} of ads that bring {fmt(rev)} of revenue gives a ROAS of 5.00x and an ACOS of 20%. At a 30% margin the break-even ROAS is {nf(100/30,2)}x, so these ads are profitable.",
  [("What is a good ROAS?", "A common target is 4x, but the right number depends on your margin. Compare it with the break-even ROAS shown above."),
   ("What is the difference between ROAS and ROI?", "ROAS looks only at revenue per unit of ad spend. ROI looks at profit after all costs."),
   ("What is ACOS?", "Advertising cost of sales: ad spend as a percentage of ad revenue. It is the inverse of ROAS.")])

# 11 roi
cost, ret_, yrs = 100000, 150000, 3
B("roi-calculator", "roi", "trend", "ROI Calculator", "Return on investment and annualised ROI",
  "Calculate return on investment as a percentage and as an annual growth rate over time.",
  [num("cost", f"Amount invested ({CUR})", cost), num("ret", f"Final value ({CUR})", ret_), num("years", "Time period (years)", yrs, step="0.1")],
  "Compare how well different investments or projects performed.",
  "ROI = (final value - amount invested) / amount invested x 100. Annualised ROI = (final value / amount invested)^(1 / years) - 1.",
  f"Investing {fmt(cost)} and ending with {fmt(ret_)} gives a gain of {fmt(ret_-cost)}, an ROI of 50% and an annualised ROI of {nf(((ret_/cost)**(1/yrs)-1)*100,2)}% over {yrs} years.",
  [("Why does annualised ROI matter?", "A 50% gain over 3 years is not the same as 50% in one year. Annualising makes investments of different lengths comparable."),
   ("Does ROI include costs and fees?", "Only if you include them in the amount invested or the final value."),
   ("Can ROI be negative?", "Yes. If the final value is below the investment, ROI is negative and shows your loss.")], also=("finance",))

# 12 shipping
B("shipping-cost-calculator", "shipping", "route", "Shipping Cost Calculator", "Volumetric weight and courier cost estimate",
  "Find volumetric and chargeable weight for a parcel and estimate the shipping cost from slab rates.",
  [num("l", "Length (cm)", 30), num("w", "Width (cm)", 20), num("h", "Height (cm)", 15), num("wt", "Actual weight (kg)", 1.2),
   num("div", "Volumetric divisor", 5000, step="1"), num("slab", "Weight slab (kg)", 0.5), num("first", f"Rate for first slab ({CUR})", 45), num("extra", f"Rate per additional slab ({CUR})", 40)],
  "Couriers bill on the greater of actual weight and volumetric weight. This tool shows both and applies your rates.",
  "Volumetric weight (kg) = length x width x height (cm) / 5000. Chargeable weight = the higher of actual and volumetric weight. Cost = first slab rate + extra slabs x additional rate.",
  f"A 30 x 20 x 15 cm parcel has a volumetric weight of {nf(30*20*15/5000,2)} kg. At an actual weight of 1.2 kg the chargeable weight is 1.8 kg, which is 4 slabs of 0.5 kg: {fmt(45+3*40)}.",
  [("Why is the divisor 5000?", "Many Indian couriers use 5000 for cm. Some use 4000 or 6000, so check with yours and edit the field."),
   ("Are these courier rates accurate?", "No. The rates are placeholders. Enter the slab rates from your courier or aggregator."),
   ("Does it include GST or fuel surcharge?", "No. Add those separately based on your courier's rate card.")], also=("shopping",))

# 13 amazon
price, ref, cl, sh, cost = 1000, 8, 20, 60, 500
tot = (price*ref/100+cl+sh)*1.18
B("amazon-seller-fee-calculator", "amazon", "cart", "Amazon Seller Fee Calculator", "Referral, closing and shipping fees with payout",
  "Estimate Amazon fees, GST on fees, your net payout and profit per order.",
  [num("price", f"Selling price ({CUR})", price), num("ref", "Referral fee (%)", ref, step="0.01"), num("close", f"Closing fee ({CUR})", cl), num("ship", f"Shipping / FBA fee ({CUR})", sh),
   num("gst", "GST on fees (%)", 18, step="0.01"), num("cost", f"Product cost ({CUR})", cost)],
  "Shows what is left of each sale after marketplace fees. Rates are editable because they change by category and price.",
  "Fees = referral fee (price x rate) + closing fee + shipping fee. GST is charged on those fees. Net payout = price - fees - GST on fees. Profit = payout - product cost.",
  f"On a {fmt(price)} item with {ref}% referral, {fmt(cl)} closing and {fmt(sh)} shipping, total fees with 18% GST are {fmt(tot,2)}. The payout is {fmt(price-tot,2)} and the profit after a {fmt(cost)} cost is {fmt(price-tot-cost,2)}.",
  [("Where do I find the exact Amazon fees?", "On the fee schedule in Amazon Seller Central. Rates vary by category, price band and fulfilment method."),
   ("Are the default rates official?", "No, they are illustrative. Replace them with the current rates for your product."),
   ("Does the payout include TCS or TDS?", "No. Taxes collected at source and returns are not included, so your final payout may differ.")], also=("shopping",))

# 14 flipkart
price, com, fx, sh, col, cost = 1000, 10, 10, 55, 15, 500
tot = (price*com/100+fx+sh+col)*1.18
B("flipkart-seller-fee-calculator", "flipkart", "cart", "Flipkart Seller Fee Calculator", "Commission, fixed, collection and shipping fees",
  "Estimate Flipkart fees, GST on fees, your settlement amount and profit per order.",
  [num("price", f"Selling price ({CUR})", price), num("com", "Commission (%)", com, step="0.01"), num("fixed", f"Fixed fee ({CUR})", fx), num("ship", f"Shipping fee ({CUR})", sh),
   num("coll", f"Collection fee ({CUR})", col), num("gst", "GST on fees (%)", 18, step="0.01"), num("cost", f"Product cost ({CUR})", cost)],
  "Shows the settlement you receive after marketplace fees. All rates are editable because they vary by category.",
  "Fees = commission (price x rate) + fixed fee + collection fee + shipping fee. GST applies to the fees. Settlement = price - fees - GST. Profit = settlement - product cost.",
  f"On a {fmt(price)} item with {com}% commission, {fmt(fx)} fixed, {fmt(col)} collection and {fmt(sh)} shipping, fees with GST are {fmt(tot,2)}. Settlement is {fmt(price-tot,2)} and profit is {fmt(price-tot-cost,2)}.",
  [("Are Flipkart fees the same for every product?", "No. Commission and shipping vary by category, price and weight. Check the rate card in Flipkart Seller Hub."),
   ("Are the defaults official rates?", "No, they are sample values. Edit them to match your category."),
   ("Are return charges included?", "No. Add return and RTO costs in the E-commerce Profit Calculator.")], also=("shopping",))

# 15 ecom
price, cost, fee, sh, pk, ads, ret, orders = 999, 400, 12, 60, 15, 80, 10, 100
pf = price*fee/100; ok = price-cost-pf-sh-pk-ads; lost = -(sh+pk+ads); prof = .9*ok+.1*lost
B("ecommerce-profit-calculator", "ecom", "briefcase", "E-commerce Profit Calculator", "Net profit per order after fees, ads and returns",
  "Find your true profit per order after platform fees, shipping, packaging, ad cost and returns.",
  [num("price", f"Selling price ({CUR})", price), num("cost", f"Product cost ({CUR})", cost), num("fee", "Platform fee (%)", fee, step="0.01"), num("ship", f"Shipping per order ({CUR})", sh),
   num("pack", f"Packaging per order ({CUR})", pk), num("ads", f"Ad cost per sale ({CUR})", ads), num("ret", "Return rate (%)", ret), num("orders", "Orders per month", orders, step="1")],
  "Gives a realistic profit per order by counting costs that sellers often forget, including returns.",
  "Profit if delivered = price - product cost - platform fee - shipping - packaging - ad cost. A returned order loses shipping, packaging and ad cost. Expected profit = (1 - return rate) x delivered profit + return rate x returned loss.",
  f"A {fmt(price)} product with a {fmt(cost)} cost makes {fmt(ok,2)} per delivered order. With a {ret}% return rate the expected profit is {fmt(prof,2)} per order, or {fmt(prof*orders,0)} on {orders} orders.",
  [("Why include returns?", "Returns can wipe out profit, especially in fashion and electronics. Including them avoids over-estimating earnings."),
   ("What is a healthy e-commerce margin?", "Many sellers aim for at least 15-20% net margin after all costs, but it varies by category."),
   ("Do the numbers include GST?", "No. Enter the selling price and fees in the form you use for your accounts, and handle GST separately.")], also=("shopping",))
