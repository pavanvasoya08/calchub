from core import *

def Sh(slug, js, icon, name, short, lead, fields, what, formula, example, faqs, also=()):
    calc(slug, js, "shopping", icon, name, short, name, lead, fields, info(what, formula, example), faqs, also=also)

# discount percentage
Sh("discount-percentage-calculator", "discpct", "percent", "Discount Percentage Calculator", "Find the discount % or the final sale price",
   "Find the discount percentage from the original and sale price, or the sale price from a discount percentage.",
   [num("orig", f"Original price ({CUR})", 2000), sel("mode", "I know the", [("price", "Sale price"), ("percent", "Discount %")], "price"),
    num("sale", f"Sale price ({CUR})", 1500, when="mode=price"), num("pct", "Discount (%)", 25, when="mode=percent", step="0.01")],
   "Quickly check how big a sale really is, or see what a percentage discount will cost you.",
   "Discount % = (original price - sale price) / original price x 100. Sale price = original price x (1 - discount % / 100).",
   f"A {fmt(2000)} item on sale for {fmt(1500)} has a discount of {nf(25,0)}% and you save {fmt(500)}. A 30% discount on {fmt(2000)} gives a price of {fmt(1400)}.",
   [("How do I calculate a discount percentage?", "Subtract the sale price from the original price, divide by the original price and multiply by 100."),
    ("Is a 50% discount the same as half price?", "Yes. Taking 50% off means you pay half of the original price."),
    ("Does the discount include tax?", "No. Taxes are added after the discount. Use the Final Price Calculator to include tax.")], also=("finance",))

# final price
p = 5000; a = p*.8; b = a*.9; fin = b*1.18
Sh("final-price-calculator", "finalprice", "tag", "Final Price Calculator", "Price after up to three discounts and tax",
   "Apply up to three successive discounts and tax to see the final price you will pay.",
   [num("price", f"Original price ({CUR})", p), num("d1", "Discount 1 (%)", 20, step="0.01"), num("d2", "Discount 2 (%)", 10, step="0.01"), num("d3", "Discount 3 (%)", 0, step="0.01"), num("tax", "Tax (%)", 18, step="0.01")],
   "Stacked offers, such as a sale plus a coupon, apply one after the other, so the total discount is not simply the sum.",
   "Each discount is applied to the price left by the previous one. Final price = price after discounts x (1 + tax / 100).",
   f"{fmt(p)} less 20% is {fmt(a)}; less another 10% is {fmt(b)}. With 18% tax the final price is {fmt(fin)}. The effective discount is {nf((1-.8*.9)*100,0)}%, not 30%.",
   [("Why is 20% + 10% not 30%?", "The second discount applies to the already reduced price, so the total is 28%."),
    ("Can I use only one discount?", "Yes. Leave the other discount fields at zero."),
    ("Which tax rate should I enter?", "Use the GST or sales tax rate for the item, for example 18% GST. Enter 0 if the price is tax-inclusive.")])

# unit price
Sh("unit-price-calculator", "unitprice", "scale", "Unit Price Calculator", "Compare two products by price per unit",
   "Compare two packs and see which one is cheaper per gram, litre or piece.",
   [num("p1", f"Product A price ({CUR})", 120), num("q1", "Product A quantity", 500), num("p2", f"Product B price ({CUR})", 220), num("q2", "Product B quantity", 1000)],
   "Bigger packs are not always cheaper. Divide price by quantity to find the real best value.",
   "Price per unit = price / quantity. The product with the lower price per unit is the better value.",
   f"Product A costs {fmt(120)} for 500 g, which is {fmt(120/500,2)} per gram. Product B costs {fmt(220)} for 1000 g, which is {fmt(.22,2)} per gram, so B is cheaper per gram.",
   [("Do both quantities need the same unit?", "Yes. Use the same unit for both, such as grams for both or millilitres for both."),
    ("Is the cheaper unit price always the better buy?", "Not if you will not use all of it. Food that spoils or items you do not need are not savings."),
    ("Can I compare more than two products?", "Yes, use the Price Comparison Calculator to compare up to four.")])

# price comparison
Sh("price-comparison-calculator", "compare", "bars", "Price Comparison Calculator", "Compare up to four products per unit",
   "Enter up to four products with their price and quantity to rank them by price per unit.",
   [f for i, (pp, qq) in enumerate([(120, 500), (220, 1000), (95, 400), (0, 0)], 1) for f in (num(f"p{i}", f"Product {i} price ({CUR})", pp), num(f"q{i}", f"Product {i} quantity", qq))],
   "Ranks your options from cheapest to most expensive per unit, so you can see the best deal quickly.",
   "Price per unit = price / quantity for each product. Rank 1 has the lowest price per unit. Leave a product blank (0) to skip it.",
   f"Product 1: {fmt(120)} for 500 = {fmt(.24,2)} per unit. Product 2: {fmt(220)} for 1000 = {fmt(.22,2)}. Product 3: {fmt(95)} for 400 = {fmt(.2375,4)}. Product 2 has the lowest unit price.",
   [("How many products can I compare?", "Up to four. Products with a zero price or quantity are ignored."),
    ("Which units should I use?", "Any, as long as they are the same for every product."),
    ("What does saving vs dearest mean?", "How much cheaper the best product is per unit, compared with the most expensive one, as a percentage.")])

# cashback
Sh("cashback-calculator", "cashback", "gift", "Cashback Calculator", "Cashback earned and effective price",
   "Work out the cashback you earn, with an optional maximum cap, and the effective price you pay.",
   [num("amt", f"Purchase amount ({CUR})", 5000), num("pct", "Cashback (%)", 5, step="0.01"), num("cap", f"Maximum cashback ({CUR}, 0 for no cap)", 200)],
   "Credit cards and wallets often cap cashback. This shows what you actually get.",
   "Cashback = purchase amount x cashback %, limited to the cap. Effective price = purchase amount - cashback.",
   f"A {fmt(5000)} purchase at 5% cashback would give {fmt(250)}, but a {fmt(200)} cap limits it to {fmt(200)}. The effective price is {fmt(4800)}.",
   [("Is cashback taxable?", "Cashback on purchases is generally treated as a discount, not income. Check local rules for referral rewards."),
    ("What if there is no cap?", "Enter 0 in the cap field."),
    ("Is cashback better than a discount?", "A discount reduces what you pay now. Cashback arrives later and may have limits, so compare the effective price.")])

# tip
bill = 2400; t = bill*.1
Sh("tip-calculator", "tip", "utensils", "Tip Calculator", "Tip, total bill and amount per person",
   "Calculate a tip and split the total bill between any number of people.",
   [num("bill", f"Bill amount ({CUR})", bill), num("tip", "Tip (%)", 10, step="0.5"), num("people", "Number of people", 4, step="1", min="1")],
   "Helps you tip fairly and divide the bill evenly.",
   "Tip = bill x tip %. Total = bill + tip. Per person = total / number of people.",
   f"A {fmt(bill)} bill with a 10% tip is {fmt(t)}, for a total of {fmt(bill+t)}. Split between 4 people, each pays {fmt((bill+t)/4)}.",
   [("How much should I tip?", "In India 5-10% is common at restaurants when no service charge is added. In the USA 15-20% is typical."),
    ("Is a service charge the same as a tip?", "No. A service charge is added by the restaurant. A tip is optional and goes to staff."),
    ("Can I round the result?", "Yes. Many people round the total per person up to the next whole number.")])

# split bill
bill = 3600; tx = bill*.05; tp = bill*.1; tot = bill+tx+tp
Sh("split-bill-calculator", "split", "users", "Split Bill Calculator", "Divide a bill with tax and tip",
   "Split a restaurant or trip bill evenly, including tax and tip.",
   [num("bill", f"Bill before tax ({CUR})", bill), num("tax", "Tax (%)", 5, step="0.01"), num("tip", "Tip (%)", 10, step="0.5"), num("people", "Number of people", 3, step="1", min="1")],
   "Shows what everyone owes when the bill includes tax and a tip.",
   "Total = bill + bill x tax % + bill x tip %. Each person pays total / number of people.",
   f"A {fmt(bill)} bill plus 5% tax ({fmt(tx)}) and a 10% tip ({fmt(tp)}) is {fmt(tot)}. Between 3 people, each pays {fmt(tot/3)}.",
   [("What if people ordered different amounts?", "This tool splits equally. For uneven shares, calculate each person's items separately and add their share of tax and tip."),
    ("Is the tip calculated on the bill with tax?", "Here it is calculated on the pre-tax bill, which is the most common practice."),
    ("Can I split by two people?", "Yes. Set the number of people to 2.")])

# sales tax
amt = 1000
Sh("tax-calculator", "salestax", "receipt", "Tax Calculator", "Add or remove sales tax from a price",
   "Add sales tax to a price or remove it from a tax-inclusive price. This is a sales tax calculator, not an income tax tool.",
   [num("amt", f"Amount ({CUR})", amt), num("rate", "Tax rate (%)", 8, step="0.01"), sel("mode", "Calculation", [("add", "Add tax"), ("remove", "Remove tax")], "add")],
   "Works out the tax on a purchase and the price with or without tax.",
   "Price with tax = price x (1 + rate / 100). Price before tax = price with tax / (1 + rate / 100).",
   f"Adding 8% tax to {fmt(amt)} gives {fmt(1080)} (tax {fmt(80)}). Removing 8% tax from {fmt(1080)} gives {fmt(1000)}.",
   [("Is this the income tax calculator?", "No. For income tax see the Income Tax Calculator in the Finance category."),
    ("What is the difference between tax-inclusive and exclusive?", "Exclusive prices do not include tax. Inclusive prices already include it, so tax must be removed to find the base price."),
    ("Does this cover GST?", "Yes, enter the GST rate. For a CGST/SGST split use the GST Inclusive/Exclusive Calculator.")], also=("business",))

# electricity
u = 350; r1, r2, r3 = 3.5, 5, 7; l1, l2 = 100, 300; fx = 50; dty = 5
e = 100*r1 + 200*r2 + 50*r3; du = (e+fx)*dty/100; tt = e+fx+du
Sh("electricity-bill-calculator", "electricity", "bolt", "Electricity Bill Calculator", "Estimate your bill from units or appliances",
   "Estimate your electricity bill using slab rates, or work out the running cost of an appliance.",
   [sel("mode", "Calculate", [("slab", "Bill from units (slab rates)"), ("app", "Appliance running cost")], "slab"),
    num("units", "Units consumed (kWh)", u, when="mode=slab"), num("l1", "Slab 1 up to (units)", l1, when="mode=slab"), num("r1", f"Slab 1 rate ({CUR}/unit)", r1, when="mode=slab", step="0.01"),
    num("l2", "Slab 2 up to (units)", l2, when="mode=slab"), num("r2", f"Slab 2 rate ({CUR}/unit)", r2, when="mode=slab", step="0.01"), num("r3", f"Rate above slab 2 ({CUR}/unit)", r3, when="mode=slab", step="0.01"),
    num("fixed", f"Fixed charge ({CUR})", fx, when="mode=slab"), num("duty", "Duty / tax on bill (%)", dty, when="mode=slab", step="0.01"),
    num("watts", "Appliance power (watts)", 1500, when="mode=app"), num("hrs", "Hours used per day", 4, when="mode=app", step="0.1"), num("days", "Days", 30, when="mode=app"),
    num("qty", "Number of appliances", 1, when="mode=app", step="1"), num("rate", f"Rate ({CUR} per kWh)", 6, when="mode=app", step="0.01")],
   "Electricity is billed in units (kWh). Most providers charge a higher rate as consumption rises, so a slab calculation is more accurate than a single rate.",
   "1 unit = 1 kWh = 1000 watts used for 1 hour. Slab bill = units in each slab x its rate, plus fixed charge and duty. Appliance cost = watts x hours x days x quantity / 1000 x rate.",
   f"For 350 units with slabs of {fmt(r1,2)}, {fmt(r2,2)} and {fmt(r3,2)} per unit, the energy charge is {fmt(e,2)}. Adding a {fmt(fx)} fixed charge and 5% duty gives a bill of {fmt(tt,2)}. A 1500 W heater for 4 hours a day over 30 days uses 180 kWh.",
   [("Are the default rates real?", "They are sample slabs. Rates differ by state, provider and consumer type, so enter the rates printed on your bill."),
    ("How many units is my appliance?", "Multiply its watts by hours used and divide by 1000. A 1000 W appliance running for 1 hour uses 1 unit."),
    ("Why does my actual bill differ?", "Bills may include fuel adjustment charges, meter rent, subsidies or surcharges that are not in this estimate.")], also=("tech",) if False else ())

# water
kl = 25; w = 10*10 + 10*15 + 5*25; 
Sh("water-bill-calculator", "water", "beaker", "Water Bill Calculator", "Estimate a metered water and sewage bill",
   "Estimate a water bill from your usage in kilolitres using editable slab rates and a sewage charge.",
   [num("kl", "Water used (kilolitres)", kl), num("l1", "Slab 1 up to (kL)", 10), num("r1", f"Slab 1 rate ({CUR}/kL)", 10, step="0.01"), num("l2", "Slab 2 up to (kL)", 20), num("r2", f"Slab 2 rate ({CUR}/kL)", 15, step="0.01"),
    num("r3", f"Rate above slab 2 ({CUR}/kL)", 25, step="0.01"), num("sew", "Sewage charge (% of water charge)", 30, step="0.01"), num("fixed", f"Fixed charge ({CUR})", 50)],
   "Municipal water is often billed per kilolitre (1,000 litres) with higher rates for higher use.",
   "Water charge = kilolitres in each slab x slab rate. Sewage = water charge x sewage %. Total = water + sewage + fixed charge.",
   f"For 25 kL with slabs of {fmt(10)}, {fmt(15)} and {fmt(25)} per kL, the water charge is {fmt(w)}. With 30% sewage ({fmt(w*.3,2)}) and a {fmt(50)} fixed charge, the total is {fmt(w*1.3+50,2)}.",
   [("How many litres are in a kilolitre?", "1 kilolitre equals 1,000 litres, or 1 cubic metre."),
    ("Where do I find my slab rates?", "On your water bill or your municipal corporation's website. Rates vary by city."),
    ("How much water does a household use?", "A typical urban household uses about 3-6 kL a month per person, depending on habits and supply.")])

# fuel cost
d = 450; m = 18; fp = 105
Sh("fuel-cost-calculator", "fuelcost", "fuel", "Fuel Cost Calculator", "Fuel needed and cost for a trip",
   "Work out how much fuel and money a trip will need from the distance, mileage and fuel price.",
   [num("dist", "Distance (km)", d), num("mil", "Mileage (km per litre)", m, step="0.1"), num("price", f"Fuel price ({CUR} per litre)", fp, step="0.01")],
   "Plan fuel costs before a trip or compare vehicles by running cost.",
   "Fuel needed = distance / mileage. Fuel cost = fuel needed x fuel price. Cost per km = fuel cost / distance.",
   f"A {d} km trip at {m} km/l needs {nf(d/m,2)} litres. At {fmt(fp)} per litre that costs {fmt(d/m*fp,2)}, or {fmt(fp/m,2)} per km.",
   [("What mileage should I use?", "Use real-world mileage from your trip meter, not the manufacturer claim. City mileage is usually lower than highway mileage."),
    ("Does AC use more fuel?", "Yes, typically 5-10% more, depending on the vehicle and conditions."),
    ("Can I use this for diesel or CNG?", "Yes. Enter the mileage and price for the fuel you use.")])

# mileage
def mil(slug, js_name, fuel):
    Sh(slug, "mileage", "gauge", f"{fuel} Mileage Calculator", f"Find your {fuel.lower()} mileage in km/l",
       f"Calculate your {fuel.lower()} vehicle's mileage in km per litre, fuel per 100 km and running cost.",
       [num("dist", "Distance travelled (km)", 320), num("lit", f"{fuel} used (litres)", 16), num("price", f"{fuel} price ({CUR} per litre)", 105 if fuel == "Petrol" else 92, step="0.01")],
       f"Track your {fuel.lower()} efficiency with the full-tank method: fill up, drive, refill and enter the litres added.",
       "Mileage (km/l) = distance travelled / fuel used. Fuel per 100 km = 100 / mileage. Cost per km = fuel price x fuel used / distance.",
       f"Driving 320 km on 16 litres gives a mileage of 20 km/l and 5 litres per 100 km. At {fmt(105 if fuel == 'Petrol' else 92)} per litre the cost is {fmt((105 if fuel == 'Petrol' else 92)/20,2)} per km.",
       [("How do I measure mileage accurately?", "Fill the tank fully, reset the trip meter, drive normally, then refill to the same level. Use the litres added."),
        ("What affects mileage?", "Driving style, speed, tyre pressure, traffic, load and air conditioning all change it."),
        ("What is a good mileage?", "For petrol cars 15-20 km/l is good; for diesel cars 18-25 km/l is common; bikes often achieve 40-60 km/l.")])
mil("petrol-mileage-calculator", "mileage", "Petrol")
mil("diesel-mileage-calculator", "mileage", "Diesel")

# travel cost
d, mm, f_, tl, ot, pp = 600, 15, 105, 450, 300, 4
fc = d/mm*f_; tot = fc+tl+ot
Sh("travel-cost-calculator", "travel", "route", "Travel Cost Calculator", "Total road-trip cost and per-person share",
   "Estimate the total cost of a road trip, including fuel, tolls and other expenses, and split it between travellers.",
   [num("dist", "Total distance (km)", d), num("mil", "Mileage (km per litre)", mm, step="0.1"), num("price", f"Fuel price ({CUR} per litre)", f_, step="0.01"),
    num("tolls", f"Tolls and parking ({CUR})", tl), num("other", f"Other costs ({CUR})", ot), num("people", "Number of travellers", pp, step="1", min="1")],
   "Plan a trip budget and share costs fairly.",
   "Fuel cost = distance / mileage x fuel price. Total = fuel + tolls + other costs. Per person = total / travellers.",
   f"A {d} km trip at {mm} km/l and {fmt(f_)} per litre costs {fmt(fc)} in fuel. With {fmt(tl)} tolls and {fmt(ot)} other costs, the total is {fmt(tot)}, or {fmt(tot/pp)} each for {pp} people.",
   [("Should I double the distance for a return trip?", "Yes. Enter the full round-trip distance."),
    ("Does it include food and stays?", "Add them in the Other costs field."),
    ("How accurate is the fuel estimate?", "It depends on the mileage you enter. Use your real-world mileage for the type of road.")])

# cooking
Sh("cooking-measurement-calculator", "cooking", "utensils", "Cooking Measurement Calculator", "Convert cups, spoons, millilitres and grams",
   "Convert common cooking measurements between cups, tablespoons, teaspoons, millilitres, grams and ounces for popular ingredients.",
   [num("amt", "Amount", 1, step="any", min="0"),
    sel("from", "From", [("cup", "Cup"), ("tbsp", "Tablespoon"), ("tsp", "Teaspoon"), ("ml", "Millilitre"), ("g", "Gram"), ("oz", "Ounce (weight)")], "cup"),
    sel("to", "To", [("g", "Gram"), ("cup", "Cup"), ("tbsp", "Tablespoon"), ("tsp", "Teaspoon"), ("ml", "Millilitre"), ("oz", "Ounce (weight)")], "g"),
    sel("ing", "Ingredient", [("flour", "All-purpose flour"), ("sugar", "Granulated sugar"), ("rice", "Rice (uncooked)"), ("butter", "Butter"), ("milk", "Milk"), ("water", "Water"), ("oil", "Cooking oil"), ("honey", "Honey")], "flour")],
   "Recipes use cups and spoons, but kitchen scales use grams. Because ingredients have different densities, the conversion depends on what you are measuring.",
   "Volume is converted using 1 cup = 236.6 ml, 1 tablespoon = 14.8 ml and 1 teaspoon = 4.93 ml. Weight uses the ingredient's density, for example 1 cup of flour is about 125 g.",
   "1 cup of all-purpose flour is about 125 g, 1 cup of sugar about 200 g and 1 cup of water about 237 g. One tablespoon of butter is about 14 g.",
   [("Why does 1 cup of flour weigh less than 1 cup of sugar?", "Flour is lighter and more airy. Each ingredient has its own density, so grams per cup differ."),
    ("Are cup measures the same everywhere?", "No. A US cup is 236.6 ml, a metric cup is 250 ml and an Indian tea cup is often 150-200 ml. This tool uses the US cup."),
    ("How accurate are the gram values?", "They are averages. Packing flour or sugar differently changes the weight, so use a scale when precision matters.")])
