from core import *
import math

SQM = 0.09290304
def sq(a): return nf(a, 2)

UNITS_L = [("ft", "Feet"), ("m", "Metres"), ("in", "Inches"), ("yd", "Yards")]
UNITS_L3 = [("ft", "Feet"), ("m", "Metres"), ("yd", "Yards")]

# ---- square feet ----
calc("square-feet-calculator", "sqft", "construction", "ruler", "Square Feet Calculator", "Room and floor area in sq ft, sq m and sq yd",
     "Square Feet Calculator", "Enter the length and width of up to four rooms to get the total area in square feet, square metres and square yards.",
     [sel("unit", "Measurement unit", UNITS_L, "ft")] + [f for i, (l, w) in enumerate([(12, 10), (10, 10), (0, 0), (0, 0)], 1) for f in (num(f"l{i}", f"Room {i} length", l), num(f"w{i}", f"Room {i} width", w))],
     info("This calculator multiplies length by width for each room, adds the areas and converts the total to square feet, square metres and square yards (gaj). Leave a room at zero to ignore it.",
          "Area = length x width. Total area = sum of all rooms. 1 sq ft = 0.092903 sq m, and 1 sq yd = 9 sq ft. Other units are first converted to feet (1 m = 3.28084 ft, 1 in = 1/12 ft, 1 yd = 3 ft).",
          f"A 12 ft x 10 ft room and a 10 ft x 10 ft room give 120 + 100 = 220 sq ft, which is {sq(220*SQM)} sq m or {sq(220/9)} sq yd."),
     [("How do I calculate square feet?", "Multiply the length in feet by the width in feet. For irregular rooms, split the space into rectangles, calculate each and add them."),
      ("How do I convert square feet to square metres?", "Multiply square feet by 0.092903. For example, 1,000 sq ft is about 92.9 sq m."),
      ("Can I enter dimensions in metres or inches?", "Yes. Pick the unit and the calculator converts everything to square feet for you.")],
     also=("math",))

# ---- land area ----
calc("land-area-calculator", "land", "construction", "triangle", "Land Area Calculator", "Area of rectangular, triangular, trapezium and circular land",
     "Land Area Calculator", "Find the area of a plot of land by shape and see it in square feet, square metres, gaj, acres and hectares.",
     [sel("shape", "Plot shape", [("rect", "Rectangle"), ("tri", "Triangle"), ("trap", "Trapezium"), ("circ", "Circle")], "rect"),
      sel("unit", "Measurement unit", UNITS_L3, "ft"),
      num("rl", "Length", 60, "shape=rect"), num("rw", "Width", 40, "shape=rect"),
      num("tb", "Base", 50, "shape=tri"), num("th", "Height", 30, "shape=tri"),
      num("pa", "Parallel side A", 50, "shape=trap"), num("pb", "Parallel side B", 70, "shape=trap"), num("ph", "Height between sides", 40, "shape=trap"),
      num("cr", "Radius", 20, "shape=circ")],
     info("Land is rarely a perfect rectangle. This calculator supports four common plot shapes and converts the area into the units used in property deals: square feet, square metres, square yards (gaj), acres and hectares.",
          "Rectangle = L x W. Triangle = 1/2 x base x height. Trapezium = (A + B) / 2 x height. Circle = pi x r^2. 1 acre = 43,560 sq ft, 1 hectare = 10,000 sq m, 1 sq yd (gaj) = 9 sq ft, 1 guntha = 1,089 sq ft.",
          f"A rectangular plot of 60 ft x 40 ft has an area of 2,400 sq ft, which is {sq(2400*SQM)} sq m, {sq(2400/9)} sq yd and {nf(2400/43560, 4)} acres."),
     [("How do I measure an irregular plot?", "Divide it into rectangles and triangles, find each area with this calculator and add the results."),
      ("How many square feet are in an acre?", "One acre equals 43,560 square feet, or about 4,047 square metres."),
      ("What is a gaj?", "Gaj is the Indian name for a square yard and equals 9 square feet.")])

# ---- carpet area ----
def carpet_ex():
    sba, load, wall = 1200, 25, 15
    b = sba / (1 + load / 100); c = b / (1 + wall / 100)
    return sba, load, wall, b, c
sba, load, wall, b, c = carpet_ex()
calc("carpet-area-calculator", "carpet", "construction", "home", "Carpet Area Calculator", "Estimate carpet area from built-up or super built-up area",
     "Carpet Area Calculator", "Convert super built-up or built-up area to the usable carpet area of a flat, using typical loading and wall percentages.",
     [sel("type", "Area you know", [("super", "Super built-up area"), ("built", "Built-up area")], "super"),
      num("area", "Area (sq ft)", 1200), num("load", "Super built-up loading (%)", 25), num("wall", "Wall thickness addition to carpet (%)", 15)],
     info("Carpet area is the floor space you can actually cover with a carpet, excluding walls, balconies and shared areas. Builders usually quote super built-up area, so this calculator works backwards using the loading percentage and wall share. Both percentages are editable because they differ by project.",
          "Built-up area = Super built-up / (1 + loading %). Carpet area = Built-up / (1 + wall %). Under RERA, the price must be quoted on carpet area, so always check the carpet area in the agreement.",
          f"A flat with {sba:,} sq ft super built-up area and {load}% loading has a built-up area of {sq(b)} sq ft. With {wall}% wall addition the carpet area is {sq(c)} sq ft, about {sq(c/sba*100)}% of the super built-up area."),
     [("What is the difference between carpet and super built-up area?", "Carpet area is the usable floor inside the walls. Super built-up area adds walls, balconies and a share of common areas such as lifts and lobbies."),
      ("What is a normal loading percentage?", "In many Indian projects loading is between 20% and 35%. Ask the builder for the exact figure in writing."),
      ("Does RERA use carpet area?", "Yes. The Real Estate (Regulation and Development) Act requires sale agreements to state the carpet area.")])

# ---- built-up area ----
c0, w0, bal, ld = 900, 12, 60, 20
bu = c0 * (1 + w0 / 100) + bal
calc("built-up-area-calculator", "builtup", "construction", "building", "Built-up Area Calculator", "Carpet area plus walls and balcony",
     "Built-up Area Calculator", "Add wall thickness and balcony to the carpet area to get the built-up area, and the super built-up area with common-area loading.",
     [num("carpet", "Carpet area (sq ft)", 900), num("wall", "Wall area as % of carpet", 12), num("bal", "Balcony / terrace area (sq ft)", 60), num("load", "Common-area loading (%)", 20)],
     info("Built-up area is the carpet area plus the area taken by walls, and usually balconies. Adding a share of common areas gives the super built-up area that builders use for pricing.",
          "Built-up area = carpet x (1 + wall %) + balcony. Super built-up area = built-up x (1 + loading %).",
          f"Carpet {c0} sq ft with {w0}% walls and a {bal} sq ft balcony gives {sq(bu)} sq ft built-up. With {ld}% loading, super built-up is {sq(bu*(1+ld/100))} sq ft."),
     [("Is a balcony part of built-up area?", "Usually yes. Balconies are counted in built-up area, though some builders count only part of them."),
      ("How thick are walls in the calculation?", "Walls typically add 10% to 15% of the carpet area, depending on wall thickness and layout."),
      ("Which area should I pay for?", "Compare prices on the carpet area, because it is the space you actually use.")])

# ---- cement ----
cv = 5 * 4 * 0.15 * 1.05
calc("cement-calculator", "cement", "construction", "beaker", "Cement Calculator", "Cement bags, sand and aggregate for concrete or mortar",
     "Cement Calculator", "Estimate cement bags, sand and aggregate for a slab, wall plaster or masonry, using the mix ratio you choose.",
     [num("l", "Length (m)", 5), num("w", "Width (m)", 4), num("d", "Thickness / depth (m)", 0.15, step="0.001"),
      sel("mix", "Mix", [("1|2|4|1.54|M15 concrete (1:2:4)", "Concrete M15 (1:2:4)"), ("1|1.5|3|1.54|M20 concrete (1:1.5:3)", "Concrete M20 (1:1.5:3)"), ("1|1|2|1.54|M25 concrete (1:1:2)", "Concrete M25 (1:1:2)"),
                          ("1|3|0|1.33|Mortar 1:3", "Mortar 1:3 (plaster)"), ("1|4|0|1.33|Mortar 1:4", "Mortar 1:4 (brickwork)"), ("1|6|0|1.33|Mortar 1:6", "Mortar 1:6 (brickwork)")], "1|1.5|3|1.54|M20 concrete (1:1.5:3)"),
      num("waste", "Wastage (%)", 5)],
     info("This calculator finds the dry volume of material needed for a given wet volume of concrete or mortar. Dry materials occupy more space than the finished mix, so a bulking factor is applied, then the volume is split in the ratio you select and cement is converted to 50 kg bags.",
          "Wet volume = L x W x D. Dry volume = wet volume x 1.54 for concrete (1.33 for mortar). Cement = dry volume x cement part / total parts. Cement bags = cement volume x 1,440 kg/m3 / 50 kg. Sand and aggregate use their own parts.",
          f"A 5 m x 4 m slab that is 0.15 m thick is 3 m3. With 5% wastage that is {sq(cv)} m3. Mix 1:1.5:3 gives {sq(cv*1.54/5.5*1440/50)} bags of cement, {sq(cv*1.54*1.5/5.5)} m3 sand and {sq(cv*1.54*3/5.5)} m3 aggregate."),
     [("How many bags of cement make 1 cubic metre of concrete?", "M20 concrete (1:1.5:3) needs about 8 bags of 50 kg per cubic metre, M15 about 6.5 bags and M25 about 11 bags."),
      ("Why is dry volume 1.54 times wet volume?", "Dry cement, sand and aggregate contain air gaps that disappear when mixed with water, so more dry material is needed than the final volume."),
      ("Should I add wastage?", "Yes. Spillage, uneven surfaces and cutting losses mean 5% to 10% extra is sensible.")],
     also=("math",))

# ---- concrete ----
calc("concrete-calculator", "conc", "construction", "weight", "Concrete Calculator", "Concrete volume and materials for slabs, beams, columns and footings",
     "Concrete Calculator", "Work out how much concrete you need and the cement, sand and aggregate to mix, for M15, M20 or M25 grade.",
     [num("l", "Length (m)", 6), num("w", "Width (m)", 4), num("t", "Depth / thickness (m)", 0.125, step="0.001"), num("n", "Number of identical members", 1),
      sel("grade", "Concrete grade", [("m15", "M15 (1:2:4)"), ("m20", "M20 (1:1.5:3)"), ("m25", "M25 (1:1:2)")], "m20"), num("waste", "Wastage (%)", 5)],
     info("Use this for slabs, beams, columns, footings and plinths: enter the size of one member, how many there are, and the grade. The calculator returns the concrete volume in cubic metres and cubic feet and the dry quantities of each material.",
          "Volume = L x W x T x number of members, plus wastage. Dry volume = volume x 1.54. Material share follows the nominal mix: M15 = 1:2:4, M20 = 1:1.5:3, M25 = 1:1:2. Cement is converted to 50 kg bags at 1,440 kg/m3.",
          f"A 6 m x 4 m slab that is 0.125 m thick holds 3 m3, or {sq(3*35.3147*1.0)} cu ft. With 5% wastage and M20 mix you need about {sq(3*1.05*1.54/5.5*1440/50)} bags of cement."),
     [("What do M15, M20 and M25 mean?", "The number is the characteristic compressive strength in N/mm2 after 28 days. M20 is common for residential slabs and beams, M25 for heavier structural work."),
      ("Does this include reinforcement steel?", "No. It covers concrete materials only. Steel quantity depends on the structural design."),
      ("Is nominal mix suitable for every job?", "Nominal mixes are fine for small residential work. Larger structures should use a design mix specified by an engineer.")])

# ---- brick ----
area = 5 * 3 - 2
calc("brick-calculator", "brick", "construction", "shapes", "Brick Calculator", "Number of bricks and mortar volume for a wall",
     "Brick Calculator", "Estimate how many standard bricks and how much mortar you need for a wall, after deducting doors and windows.",
     [num("len", "Wall length (m)", 5), num("ht", "Wall height (m)", 3), sel("th", "Wall thickness", [("1", "Half brick (90 mm)"), ("2", "One brick (190 mm)"), ("3", "One and a half brick (290 mm)")], "1"),
      num("open", "Doors and windows area (m2)", 2), num("waste", "Wastage (%)", 5)],
     info("This calculator uses the standard Indian modular brick of 190 x 90 x 90 mm. With a 10 mm mortar joint each brick occupies 200 x 100 x 100 mm, which gives 50 bricks per square metre of half-brick wall.",
          "Net wall area = length x height - openings. Bricks = net area x 50 (half brick), 100 (one brick) or 150 (one and a half brick), plus wastage. Mortar = wall volume - brick volume, where one brick is 0.001539 m3.",
          f"A 5 m x 3 m half-brick wall with 2 m2 of openings has {area} m2 net area, so {area*50} bricks, or {math.ceil(area*50*1.05)} with 5% wastage. Mortar needed is about {sq(area*0.09 - area*50*0.19*0.09*0.09)} m3."),
     [("How many bricks are needed per square metre?", "About 50 for a half-brick wall and 100 for a one-brick wall when using 190 x 90 x 90 mm bricks with 10 mm mortar joints."),
      ("How much mortar do I need?", "Mortar is roughly 15% to 25% of the wall volume. The calculator shows the wet mortar volume."),
      ("Do I need to deduct doors and windows?", "Yes. Deduct the area of every opening larger than about 0.1 m2 to avoid ordering too many bricks.")])

# ---- paint ----
pw = 2 * (5 + 4) * 3 - 2 * 1.9 - 2 * 1.2
calc("paint-calculator", "paint", "construction", "wave", "Paint Calculator", "Litres of paint needed for a room",
     "Paint Calculator", "Calculate the wall area of a room, subtract doors and windows and find the litres of paint for the number of coats you want.",
     [num("l", "Room length (m)", 5), num("w", "Room width (m)", 4), num("h", "Room height (m)", 3), num("doors", "Number of doors", 2), num("wins", "Number of windows", 2),
      chk("ceil", "Paint the ceiling too", False), num("coats", "Number of coats", 2), num("cov", "Coverage (m2 per litre)", 10)],
     info("Enter the room size and the calculator finds the paintable wall area, deducting an average door (1.9 m2) and window (1.2 m2). Multiply by the number of coats and divide by the coverage per litre to get the paint quantity.",
          "Wall area = 2 x (L + W) x H - doors x 1.9 - windows x 1.2. Ceiling area (optional) = L x W. Litres = area x coats / coverage. Most emulsions cover 9 to 12 m2 per litre per coat.",
          f"A 5 m x 4 m room with 3 m walls, 2 doors and 2 windows has {sq(pw)} m2 of wall. Two coats at 10 m2 per litre need {sq(pw*2/10)} litres."),
     [("How much area does one litre of paint cover?", "Typically 9 to 12 square metres (100 to 130 sq ft) per coat, depending on the paint and the surface."),
      ("How many coats do I need?", "Two coats are standard. A rough or dark wall may need a primer and an extra coat."),
      ("Should I buy extra?", "Add about 5% for touch-ups and uneven absorption.")])

# ---- tile ----
ta = 12 * 10
calc("tile-calculator", "tile", "construction", "shapes", "Tile Calculator", "Number of tiles and boxes for a floor or wall",
     "Tile Calculator", "Find how many tiles and boxes you need for a room, including wastage for cuts and breakage.",
     [num("l", "Room length (ft)", 12), num("w", "Room width (ft)", 10),
      sel("size", "Tile size (mm)", [("300x300", "300 x 300"), ("300x600", "300 x 600"), ("600x600", "600 x 600 (2 x 2 ft)"), ("600x1200", "600 x 1200"), ("800x800", "800 x 800"), ("1200x1200", "1200 x 1200")], "600x600"),
      num("waste", "Wastage (%)", 10), num("box", "Tiles per box", 4)],
     info("Select your tile size, enter the room dimensions and set the wastage. The calculator divides the floor area by the area of one tile, adds wastage and rounds up to full tiles and full boxes.",
          "Tiles = ceil(floor area x (1 + wastage %) / tile area). Boxes = ceil(tiles / tiles per box). A 600 x 600 mm tile covers 3.875 sq ft.",
          f"A 12 ft x 10 ft room is {ta} sq ft. A 600 x 600 mm tile covers {nf(600*600/92903.04,3)} sq ft, so you need {math.ceil(ta*1.10/(600*600/92903.04))} tiles with 10% wastage, which is {math.ceil(math.ceil(ta*1.10/(600*600/92903.04))/4)} boxes of 4."),
     [("How much wastage should I add for tiles?", "10% is usual for straight layouts and 15% for diagonal or patterned layouts."),
      ("Should I buy all tiles from the same batch?", "Yes. Colour and size can vary slightly between batches, so order everything together."),
      ("Does the calculator include grout and adhesive?", "No. It covers tiles only. Adhesive and grout are bought separately based on the tile area.")])

# ---- flooring cost ----
fa, fm, fl, fw, fo = 500, 80, 25, 10, 5000
calc("flooring-cost-calculator", "floorcost", "construction", "wallet", "Flooring Cost Calculator", "Material, labour and total cost of flooring",
     "Flooring Cost Calculator", "Estimate the total cost of new flooring from the area, material rate, labour rate and wastage.",
     [num("area", "Floor area (sq ft)", 500), num("mat", f"Material rate ({CUR} per sq ft)", 80), num("lab", f"Labour rate ({CUR} per sq ft)", 25), num("waste", "Wastage (%)", 10), num("other", f"Other costs ({CUR}, skirting, adhesive)", 5000)],
     info("Flooring cost has three parts: material (which must include wastage), labour, and extras such as skirting and adhesive. Enter your local rates to get the total and the effective rate per square foot.",
          "Material cost = area x (1 + wastage %) x material rate. Labour cost = area x labour rate. Total = material + labour + other costs.",
          f"For {fa} sq ft at {fmt(fm)} material and {fmt(fl)} labour per sq ft with {fw}% wastage and {fmt(fo)} extras: material {fmt(fa*(1+fw/100)*fm)}, labour {fmt(fa*fl)}, total {fmt(fa*(1+fw/100)*fm+fa*fl+fo)}."),
     [("Is labour charged on area with or without wastage?", "Labour is normally charged on the laid area, so wastage is not added to it."),
      ("What is a typical flooring rate?", "Rates vary widely by city and material. Get two or three local quotes and enter them here to compare."),
      ("Does this include removing old flooring?", "No. Add the removal and levelling cost under other costs.")],
     also=("finance",))

# ---- construction cost ----
cca, ccf = 1000, 1
calc("construction-cost-calculator", "cc", "construction", "building", "Construction Cost Calculator", "Estimate the cost of building a house",
     "Construction Cost Calculator", "Estimate the cost of building a house from built-up area, number of floors and quality of finish.",
     [num("area", "Built-up area per floor (sq ft)", 1000), num("floors", "Number of floors", 1),
      sel("q", "Quality of construction", [("1500", "Economy"), ("2000", "Standard"), ("2800", "Premium")], "2000"),
      num("rate", f"Your own rate ({CUR} per sq ft, 0 = use quality preset)", 0)],
     info("This is a quick budget estimate for a new house. Pick a quality level or enter your own local rate per square foot, and the calculator returns the total cost with a material and labour split and a typical breakdown by work stage.",
          "Total cost = built-up area x floors x rate per sq ft. Preset rates are Economy 1,500, Standard 2,000 and Premium 2,800 per sq ft. Material is shown at about 60% and labour at about 40% of the total.",
          f"A {cca:,} sq ft house at the standard rate of {fmt(2000)} per sq ft costs {fmt(cca*2000)}, roughly {fmt(cca*2000*0.6)} for materials and {fmt(cca*2000*0.4)} for labour."),
     [("How accurate is this estimate?", "It is a planning figure only. Actual cost depends on the city, soil, design, material brands and the contractor, so get detailed quotes."),
      ("What is not included?", "Land, approvals, interior furniture, landscaping and taxes are not included."),
      ("Which rate should I use?", "Ask local contractors for the current rate per sq ft in your area and enter it as your own rate.")],
     also=("finance",))

# ---- plot area ----
calc("plot-area-calculator", "plot", "construction", "target", "Plot Area Calculator", "Plot size in sq ft, gaj, cent, guntha and acres",
     "Plot Area Calculator", "Enter the length and width of a plot and see its area in all the units used in Indian property listings.",
     [num("l", "Plot length", 50), num("w", "Plot width", 30), sel("unit", "Measurement unit", UNITS_L3, "ft")],
     info("Plot sizes are quoted in different units across India. This calculator converts the area of a rectangular plot into square feet, square metres, square yards (gaj), cents, gunthas, acres and hectares.",
          "Area = length x width. 1 sq yd (gaj) = 9 sq ft. 1 cent = 435.6 sq ft. 1 guntha = 1,089 sq ft. 1 acre = 43,560 sq ft = 100 cents = 40 gunthas.",
          f"A 50 ft x 30 ft plot is 1,500 sq ft = {sq(1500/9)} gaj = {sq(1500/435.6)} cents = {sq(1500/1089)} gunthas = {nf(1500/43560,4)} acres."),
     [("How many square feet are in a gaj?", "One gaj (square yard) is 9 square feet."),
      ("What is a cent?", "A cent is a unit used in southern India and equals 435.6 square feet, which is 1/100 of an acre."),
      ("Does this work for irregular plots?", "It handles rectangles. For other shapes use the Land Area Calculator.")])

# ---- registration & stamp duty ----
STATES = [("Maharashtra", 5, 5, 1), ("Gujarat", 4.9, 4.9, 1), ("Karnataka", 5, 5, 1), ("Delhi", 6, 4, 1), ("Tamil Nadu", 7, 7, 2), ("Uttar Pradesh", 7, 7, 1),
          ("Rajasthan", 5, 4, 1), ("Telangana", 4, 4, 0.5), ("West Bengal", 6, 6, 1), ("Haryana", 7, 5, 0)]
def st_opts():
    return [(f"{n}|{m}|{f}|{r}", n) for n, m, f, r in STATES] + [("Custom", "Custom rates")]
val = 5000000
calc("property-registration-cost-calculator", "reg", "construction", "receipt", "Property Registration Cost Calculator", "Stamp duty plus registration fee for a property",
     "Property Registration Cost Calculator", "Estimate the total government cost of registering a property: stamp duty plus registration charges, using indicative state rates you can edit.",
     [num("val", f"Property value ({CUR})", 5000000), sel("state", "State", st_opts(), st_opts()[0][0]),
      num("cs", "Custom stamp duty (%)", 5, "state=Custom", step="0.01"), num("cr", "Custom registration fee (%)", 1, "state=Custom", step="0.01")],
     info("Registering a property involves stamp duty and a registration fee, both based on the property value or the circle rate, whichever the state treats as higher. This calculator uses indicative state rates; choose Custom to enter the exact rates your state applies.",
          "Stamp duty = property value x stamp duty %. Registration fee = property value x registration %. Total = stamp duty + registration fee. Rates here are indicative for a typical residential sale to a male buyer and change often.",
          f"For a {fmt(val)} property in Maharashtra at 5% stamp duty and 1% registration: stamp duty {fmt(val*0.05)}, registration {fmt(val*0.01)}, total {fmt(val*0.06)}. Maharashtra caps the registration fee at {fmt(30000)} in many cases, so the final figure may be lower."),
     [("Are these rates exact?", "No. They are indicative and states revise stamp duty, surcharges and caps regularly. Always confirm with the sub-registrar office or your state's official portal."),
      ("Is duty charged on the sale price or the circle rate?", "Most states charge on whichever is higher: the agreement value or the government circle rate."),
      ("Do women pay less?", "Several states give women buyers a concession on stamp duty. Use the Stamp Duty Calculator to see the difference.")],
     also=("finance",))

calc("stamp-duty-calculator", "stamp", "construction", "shield", "Stamp Duty Calculator", "Stamp duty on a property purchase",
     "Stamp Duty Calculator", "Calculate the stamp duty on a property purchase, with different rates for male and female buyers in some states.",
     [num("val", f"Property value ({CUR})", 5000000), sel("state", "State", st_opts(), st_opts()[3][0]),
      sel("buyer", "Buyer", [("m", "Male or joint buyer"), ("f", "Female buyer")], "m"),
      num("cs", "Custom stamp duty (%)", 5, "state=Custom", step="0.01")],
     info("Stamp duty is a state tax paid when a property is transferred. Some states charge a lower rate when the buyer is a woman. Pick your state, or enter your own rate, to see the duty on your purchase.",
          "Stamp duty = property value x stamp duty rate. The rate depends on the state and, in some states, on the buyer. Additional cess or surcharge, where applicable, is not included.",
          f"On a {fmt(val)} property in Delhi, a male buyer pays 6%, which is {fmt(val*0.06)}. A female buyer pays 4%, which is {fmt(val*0.04)}, saving {fmt(val*0.02)}."),
     [("Who pays stamp duty?", "The buyer pays stamp duty when the sale deed is registered."),
      ("Are the state rates up to date?", "They are indicative. States change rates and concessions often, so verify the current rate on the official state website."),
      ("Does stamp duty apply to gift or rent agreements?", "Yes, but at different rates. This calculator is meant for property purchase.")],
     also=("finance",))

# ---- rent ----
r0, inc, yrs = 20000, 5, 5
tot = sum(r0 * (1 + inc / 100) ** y * 12 for y in range(yrs))
calc("rent-calculator", "rent", "construction", "home", "Rent Calculator", "Total rent over time and HRA tax exemption",
     "Rent Calculator", "Work out your total rent with yearly increases, or estimate the HRA exemption you can claim on rent paid.",
     [sel("mode", "What do you want to calculate?", [("cost", "Total rent over the years"), ("hra", "HRA exemption")], "cost"),
      num("rent", f"Monthly rent ({CUR})", 20000, "mode=cost"), num("maint", f"Monthly maintenance ({CUR})", 1500, "mode=cost"), num("dep", f"Security deposit ({CUR})", 60000, "mode=cost"),
      num("inc", "Yearly rent increase (%)", 5, "mode=cost"), num("yrs", "Years", 5, "mode=cost", step="1", min="1"),
      num("basic", f"Basic salary per month ({CUR})", 50000, "mode=hra"), num("hra", f"HRA received per month ({CUR})", 20000, "mode=hra"),
      num("paid", f"Rent paid per month ({CUR})", 18000, "mode=hra"), sel("metro", "City", [("0.5", "Metro (Delhi, Mumbai, Kolkata, Chennai)"), ("0.4", "Non-metro")], "0.5", "mode=hra")],
     info("Use this calculator to plan what a rented home will cost you over several years, including a yearly rent increase and maintenance, or to estimate the House Rent Allowance (HRA) exemption available to salaried employees under the old tax regime.",
          "Rent in year n = rent x (1 + increase %)^(n-1). Total rent = sum of yearly rents x 12. HRA exemption per month = lowest of: HRA received, rent paid - 10% of basic salary, and 50% (metro) or 40% (non-metro) of basic salary.",
          f"Rent of {fmt(r0)} a month with a {inc}% yearly increase costs {fmt(tot)} over {yrs} years. For HRA, with basic {fmt(50000)}, HRA {fmt(20000)} and rent {fmt(18000)} in a metro, the monthly exemption is {fmt(min(20000, 18000-5000, 25000))}."),
     [("Who can claim HRA exemption?", "Salaried employees who pay rent and receive HRA, and who choose the old tax regime. The new regime does not allow HRA exemption."),
      ("What is a normal yearly rent increase?", "Many agreements use 5% to 10% a year. Your rental agreement sets the actual figure."),
      ("Is the security deposit included in total rent?", "No. It is refundable, so it is shown separately.")],
     also=("finance",))
