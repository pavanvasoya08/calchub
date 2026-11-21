from core import *
import json as _json

def _n(x, d=4):
    s = f"{x:,.{d}f}".rstrip("0").rstrip(".")
    return s

def _head(cfg):
    return "<script>window.CV=" + _json.dumps(cfg) + ";</script>"

CONV_FAQ_NOTE = "The calculator also shows the reverse conversion and a table of common values."

def conv(slug, name, short, a, b, f, icon, vals, d=4, fn="lin", alt=None, ftin=False, default=1, faq=None, lead=None, formula=None, note=""):
    """a, b = (name, symbol); f = multiplier a -> b (for lin)."""
    cfg = dict(a=a, b=b, f=f, vals=vals, d=d, fn=fn, alt=alt, ftin=ftin)
    if fn == "c2f":
        fx, rx = (lambda x: x * 9 / 5 + 32), (lambda x: (x - 32) * 5 / 9)
    elif fn == "f2c":
        fx, rx = (lambda x: (x - 32) * 5 / 9), (lambda x: x * 9 / 5 + 32)
    else:
        fx, rx = (lambda x: x * f), (lambda x: x / f)
    ex_in = default
    ex_out = fx(ex_in)
    formula = formula or f"{b[0]} = {a[0]} x {f}. To go back, divide by {f}."
    if fn == "c2f": formula = "Fahrenheit = Celsius x 9/5 + 32. To go back, Celsius = (Fahrenheit - 32) x 5/9."
    if fn == "f2c": formula = "Celsius = (Fahrenheit - 32) x 5/9. To go back, Fahrenheit = Celsius x 9/5 + 32."
    if ftin:
        fields = [num("v", "Feet", 5, step="any"), num("i", "Inches", 7, step="any")] if a[1] == "ft" else [num("v", "Centimetres (cm)", 170)]
    else:
        fields = [num("v", f"{a[0]} ({a[1]})", default, min="" if fn != "lin" else "0")]
    if ftin and a[1] == "ft":
        ex = f"5 ft 7 in is {_n((5*12+7)*2.54,2)} cm."
    elif ftin:
        tot = 170 / 2.54; ft = int(tot // 12); ins = tot - ft * 12
        ex = f"170 cm is {_n(170*0.0328084,4)} feet, which is {ft} ft {_n(ins,1)} in."
    else:
        ex = f"{_n(ex_in)} {a[1]} = {_n(ex_out, d)} {b[1]}. And {_n(ex_in)} {b[1]} = {_n(rx(ex_in), d)} {a[1]}."
    what = (lead or f"Convert {a[0].lower()} to {b[0].lower()} instantly. Type a value and the result updates as you type.") + " " + CONV_FAQ_NOTE
    faqs = faq or [
        (f"How do I convert {a[0].lower()} to {b[0].lower()}?", formula),
        (f"How many {b[0].lower()} are in one {a[0].lower().rstrip('s')}?", f"1 {a[1]} = {_n(fx(1), 6)} {b[1]}." if fn == "lin" else f"Use the formula above; for example 0 {a[1]} = {_n(fx(0), 2)} {b[1]}."),
        ("Is this converter accurate?", "It uses the exact international conversion factors and shows the result to several decimal places."),
        ("Can I convert the other way?", f"Yes. The reverse result is shown below, so you can read {b[0].lower()} to {a[0].lower()} without leaving the page."),
    ]
    calc(slug, "conv", "units", icon, name, short, name, f"Convert {a[0].lower()} to {b[0].lower()} with an instant result, the reverse conversion and a quick reference table.",
         fields, info(what + (" " + note if note else ""), formula, ex), faqs, head=_head(cfg))

conv("cm-to-feet-calculator", "CM to Feet Calculator", "Centimetres to feet and inches", ("Centimetres", "cm"), ("Feet", "ft"), 0.0328084, "ruler",
     [150, 160, 165, 170, 175, 180, 185, 190], ftin=True, lead="Convert centimetres to feet and inches, which is handy for height.",
     formula="Feet = cm / 30.48. For feet and inches, take the whole number of feet and convert the remainder: inches = remainder x 12.")
conv("feet-to-cm-calculator", "Feet to CM Calculator", "Feet and inches to centimetres", ("Feet", "ft"), ("Centimetres", "cm"), 30.48, "ruler",
     [4, 5, 5.5, 6, 6.5, 7], ftin=True, lead="Convert feet and inches to centimetres, for example to find height in cm.",
     formula="cm = (feet x 12 + inches) x 2.54, because 1 inch is exactly 2.54 cm.")
conv("kg-to-pounds-converter", "KG to Pounds Converter", "Kilograms to pounds", ("Kilograms", "kg"), ("Pounds", "lb"), 2.2046226218, "weight", [1, 5, 10, 25, 50, 60, 75, 100], default=70, d=2)
conv("pounds-to-kg-converter", "Pounds to KG Converter", "Pounds to kilograms", ("Pounds", "lb"), ("Kilograms", "kg"), 0.45359237, "weight", [1, 5, 10, 25, 50, 100, 150, 200], default=154, d=2)
conv("km-to-miles-converter", "KM to Miles Converter", "Kilometres to miles", ("Kilometres", "km"), ("Miles", "mi"), 0.6213711922, "route", [1, 5, 10, 21.1, 42.2, 50, 100, 500], default=10, d=3)
conv("miles-to-km-converter", "Miles to KM Converter", "Miles to kilometres", ("Miles", "mi"), ("Kilometres", "km"), 1.609344, "route", [1, 5, 10, 26.2, 50, 60, 100, 500], default=10, d=3)
conv("celsius-to-fahrenheit-converter", "Celsius to Fahrenheit", "Convert degrees Celsius to Fahrenheit", ("Celsius", "°C"), ("Fahrenheit", "°F"), 1, "thermo", [-40, 0, 10, 20, 25, 37, 100], fn="c2f", default=25, d=2)
conv("fahrenheit-to-celsius-converter", "Fahrenheit to Celsius", "Convert degrees Fahrenheit to Celsius", ("Fahrenheit", "°F"), ("Celsius", "°C"), 1, "thermo", [-40, 0, 32, 50, 68, 98.6, 212], fn="f2c", default=98.6, d=2)
conv("inches-to-cm-converter", "Inches to CM Converter", "Inches to centimetres", ("Inches", "in"), ("Centimetres", "cm"), 2.54, "ruler", [1, 2, 5, 6, 10, 12, 24, 36], default=10, d=2)
conv("meters-to-feet-converter", "Meters to Feet Converter", "Metres to feet", ("Metres", "m"), ("Feet", "ft"), 3.280839895, "ruler", [1, 2, 5, 10, 25, 50, 100], default=10, d=3)
conv("liters-to-gallons-converter", "Liters to Gallons Converter", "Litres to US and UK gallons", ("Litres", "L"), ("US gallons", "gal (US)"), 0.2641720524, "beaker", [1, 5, 10, 20, 40, 50, 100], default=10, d=3,
     alt=["UK (imperial) gallons", 0.2199692483],
     note="The US gallon is 3.785 litres and the UK (imperial) gallon is 4.546 litres, so both results are shown.")
conv("mb-to-gb-converter", "MB to GB Converter", "Megabytes to gigabytes (1000 and 1024)", ("Megabytes", "MB"), ("Gigabytes", "GB"), 0.001, "monitor", [100, 500, 1000, 1024, 2048, 5000, 10240], default=2048, d=4,
     alt=["Gibibytes, binary (GiB)", 1 / 1024],
     note="Storage makers use 1 GB = 1000 MB. Operating systems often use 1 GB = 1024 MB, so both are shown.")
conv("kb-to-mb-converter", "KB to MB Converter", "Kilobytes to megabytes (1000 and 1024)", ("Kilobytes", "KB"), ("Megabytes", "MB"), 0.001, "monitor", [100, 500, 1000, 1024, 2048, 5000, 10240], default=2048, d=4,
     alt=["Mebibytes, binary (MiB)", 1 / 1024],
     note="Decimal: 1 MB = 1000 KB. Binary: 1 MB (MiB) = 1024 KB.")
conv("square-feet-to-square-meter-converter", "Square Feet to Square Meter", "Sq ft to sq m", ("Square feet", "sq ft"), ("Square metres", "sq m"), 0.09290304, "shapes", [100, 250, 500, 1000, 1200, 1500, 2000], default=1000, d=3,
     lead="Convert area from square feet to square metres, which is useful for flats, plots and floor plans.")

# ---------- acre to bigha ----------
BIGHA = [("Uttar Pradesh", 27000), ("Bihar", 27220), ("Gujarat", 17427), ("Haryana", 27225), ("Himachal Pradesh", 8712), ("Jharkhand", 27211),
         ("Punjab", 9070), ("Rajasthan (pucca)", 27225), ("Rajasthan (kachha)", 17424), ("Madhya Pradesh", 12000), ("Uttarakhand", 6804),
         ("West Bengal", 14400), ("Assam", 14400)]
_cfg = dict(states=BIGHA)
calc("acre-to-bigha-converter", "bigha", "units", "shapes", "Acre to Bigha Converter", "Acres to bigha by state",
     "Acre to Bigha Converter", "Convert acres to bigha (and bigha to acres) using the bigha size used in your state.",
     [num("v", "Value", 1), sel("dir", "Convert", [("ab", "Acres to bigha"), ("ba", "Bigha to acres")], "ab"),
      sel("st", "State", [(str(i), s) for i, (s, _) in enumerate(BIGHA)], "0")],
     info("The size of a bigha is not the same across India. It changes from state to state, and sometimes between districts. Choose your state to convert acres to bigha, or bigha to acres, with the usual local size. A table shows the same value in every state.",
          "1 acre = 43,560 square feet. Bigha = acres x 43,560 / square feet per bigha (for your state). Acres = bigha x square feet per bigha / 43,560.",
          f"1 acre in Uttar Pradesh (1 bigha = 27,000 sq ft) is {_n(43560/27000,3)} bigha. In Gujarat (1 bigha = 17,427 sq ft) it is {_n(43560/17427,3)} bigha."),
     [("How many bigha are in an acre?", f"It depends on the state. In Uttar Pradesh 1 acre is about {_n(43560/27000,2)} bigha, in Gujarat about {_n(43560/17427,2)} bigha and in Punjab about {_n(43560/9070,2)} bigha."),
      ("Why does the bigha size change?", "Bigha was a traditional local measure and each region fixed its own size. Even within a state the size can differ between districts, so check your local revenue record before any transaction."),
      ("How many square feet are in one acre?", "1 acre is 43,560 square feet or about 4,047 square metres."),
      ("Is this result legally valid?", "No. It is an estimate based on commonly used sizes. For registration or sale, use the area written in your land records.")],
     head=_head(_cfg))

# ---------- general unit converter ----------
UNITS = {
 "length": ("Length", [("Millimetre", "mm", 0.001), ("Centimetre", "cm", 0.01), ("Metre", "m", 1), ("Kilometre", "km", 1000), ("Inch", "in", 0.0254), ("Foot", "ft", 0.3048), ("Yard", "yd", 0.9144), ("Mile", "mi", 1609.344)]),
 "weight": ("Weight", [("Milligram", "mg", 1e-6), ("Gram", "g", 0.001), ("Kilogram", "kg", 1), ("Tonne", "t", 1000), ("Ounce", "oz", 0.028349523125), ("Pound", "lb", 0.45359237), ("Stone", "st", 6.35029318)]),
 "temperature": ("Temperature", [("Celsius", "°C", 0), ("Fahrenheit", "°F", 0), ("Kelvin", "K", 0)]),
 "area": ("Area", [("Square metre", "sq m", 1), ("Square kilometre", "sq km", 1e6), ("Square foot", "sq ft", 0.09290304), ("Square yard", "sq yd", 0.83612736), ("Square inch", "sq in", 0.00064516), ("Acre", "acre", 4046.8564224), ("Hectare", "ha", 10000)]),
 "volume": ("Volume", [("Millilitre", "ml", 0.001), ("Litre", "L", 1), ("Cubic metre", "m3", 1000), ("US gallon", "gal (US)", 3.785411784), ("UK gallon", "gal (UK)", 4.54609), ("US cup", "cup", 0.2365882365), ("US fluid ounce", "fl oz", 0.0295735295625), ("Tablespoon (US)", "tbsp", 0.01478676478125), ("Teaspoon (US)", "tsp", 0.00492892159375)]),
 "speed": ("Speed", [("Metre per second", "m/s", 1), ("Kilometre per hour", "km/h", 1 / 3.6), ("Mile per hour", "mph", 0.44704), ("Knot", "kn", 1852 / 3600), ("Foot per second", "ft/s", 0.3048)]),
 "time": ("Time", [("Second", "s", 1), ("Minute", "min", 60), ("Hour", "h", 3600), ("Day", "day", 86400), ("Week", "week", 604800), ("Year (365.25 days)", "year", 31557600)]),
 "data": ("Data", [("Bit", "bit", 0.125), ("Byte", "B", 1), ("Kilobyte", "KB", 1000), ("Megabyte", "MB", 1e6), ("Gigabyte", "GB", 1e9), ("Terabyte", "TB", 1e12), ("Kibibyte", "KiB", 1024), ("Mebibyte", "MiB", 1048576), ("Gibibyte", "GiB", 1073741824)]),
}
_defaults = {"length": ("km", "mi"), "weight": ("kg", "lb"), "temperature": ("°C", "°F"), "area": ("sq ft", "sq m"), "volume": ("L", "gal (US)"), "speed": ("km/h", "mph"), "time": ("h", "min"), "data": ("GB", "MB")}
_fields = [sel("cat", "Category", [(k, v[0]) for k, v in UNITS.items()], "length"), num("v", "Value", 1, min="")]
for k, (nm, lst) in UNITS.items():
    opts = [(u[1], f"{u[0]} ({u[1]})") for u in lst]
    _fields.append(sel("f_" + k, "From", opts, _defaults[k][0], when=f"cat={k}"))
    _fields.append(sel("t_" + k, "To", opts, _defaults[k][1], when=f"cat={k}"))
calc("unit-converter", "uc", "units", "scale", "Unit Converter", "Length, weight, temperature, area, volume, speed, time and data",
     "Unit Converter", "Convert between common units of length, weight, temperature, area, volume, speed, time and data in one place.",
     _fields,
     info("This all-in-one unit converter handles eight categories: length, weight, temperature, area, volume, speed, time and data. Pick a category, choose the units and type a value. Use the swap button to reverse the conversion.",
          "Each value is first converted to a base unit (metre, kilogram, square metre, litre, metre per second, second or byte) and then to the target unit. Temperature uses its own formulas: F = C x 9/5 + 32 and K = C + 273.15.",
          f"10 km is {_n(10*1000/1609.344,4)} miles. 25 °C is {_n(25*9/5+32,1)} °F. 1 GB is 1,000 MB (decimal) or about 0.931 GiB (binary)."),
     [("Which unit categories are supported?", "Length, weight, temperature, area, volume, speed, time and data."),
      ("What is the difference between GB and GiB?", "1 GB is 1,000,000,000 bytes while 1 GiB is 1,073,741,824 bytes. Operating systems often show GiB but call it GB."),
      ("How is temperature converted?", "Temperature scales have different zero points, so formulas are used instead of a single multiplier: F = C x 9/5 + 32 and K = C + 273.15."),
      ("Are the conversions exact?", "Length, weight and volume factors are the exact international definitions. Results are rounded for display.")],
     head=_head(dict(units=UNITS)))
