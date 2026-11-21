from core import *

# ---------- Percentage ----------
calc("percentage-calculator", "m_pct", "math", "percent", "Percentage Calculator", "Percent of a number, percent change and more", "Percentage Calculator",
     "Calculate percentages in seconds: percent of a number, what percent one number is of another, percentage change, and adding or subtracting a percentage.",
     [sel("m", "What do you want to find?", [("of", "X% of Y"), ("is", "X is what % of Y"), ("chg", "Percentage increase or decrease"), ("add", "Add a percentage to a value"), ("sub", "Subtract a percentage from a value")], "of"),
      num("of_p", "Percentage (%)", 20, when="m=of"), num("of_v", "Of the value", 500, when="m=of"),
      num("is_x", "Part (X)", 50, when="m=is"), num("is_y", "Total (Y)", 200, when="m=is"),
      num("ch_a", "Old value", 80, when="m=chg", min=""), num("ch_b", "New value", 100, when="m=chg", min=""),
      num("ad_v", "Value", 200, when="m=add|sub", min=""), num("ad_p", "Percentage (%)", 15, when="m=add|sub", min="")],
     info("Percentages show a part out of 100. This calculator handles the five most common percentage problems, including discounts, markups, marks and growth rates.",
          "X% of Y = X / 100 x Y. X is what % of Y = X / Y x 100. Percentage change = (new - old) / old x 100. Add a percentage: value x (1 + p/100). Subtract: value x (1 - p/100).",
          "20% of 500 is 20 / 100 x 500 = 100. Going from 80 to 100 is a 25% increase because (100 - 80) / 80 x 100 = 25. Adding 15% to 200 gives 230."),
     [("How do I calculate a percentage of a number?", "Divide the percentage by 100 and multiply by the number. For example 15% of 80 is 0.15 x 80 = 12."),
      ("What is the difference between percentage and percentage points?", "If a rate rises from 10% to 15%, it rises by 5 percentage points, which is a 50% relative increase."),
      ("How do I reverse a percentage increase?", "Divide the new value by (1 + p/100). For example, a price of 230 after a 15% increase was 230 / 1.15 = 200 before.")],
     also=("finance", "education"))

# ---------- Average ----------
calc("average-calculator", "m_avg", "math", "bars", "Average Calculator", "Mean, median, mode and range", "Average Calculator",
     "Enter a list of numbers to get their average (mean), median, mode, sum, range and more.",
     [txt("list", "Numbers (separated by commas, spaces or new lines)", "12, 18, 25, 30, 45", rows=4)],
     info("The average, or arithmetic mean, shows the central value of a set of numbers. The calculator also gives the median, mode and range.",
          "Mean = sum of values / count. Median = middle value after sorting (average of the two middle values if the count is even). Mode = most frequent value. Range = largest - smallest.",
          "For 12, 18, 25, 30 and 45 the sum is 130 and the count is 5, so the mean is 26. The median is 25 and the range is 45 - 12 = 33."),
     [("What is the difference between mean and median?", "The mean is affected by very large or small values. The median is the middle value and is less sensitive to outliers."),
      ("Can there be more than one mode?", "Yes. If several values appear equally often, all of them are modes."),
      ("How do I find a weighted average?", "Multiply each value by its weight, add the results and divide by the total of the weights.")])

# ---------- Scientific ----------
PAD_CSS = ('<style>#pad{display:grid;grid-template-columns:repeat(6,1fr);gap:8px}#pad .pk{padding:12px 4px;text-align:center}'
           '@media(max-width:520px){#pad{grid-template-columns:repeat(5,1fr)}}</style>')
calc("scientific-calculator", "m_sci", "math", "calculator", "Scientific Calculator", "Trigonometry, logs, powers and roots", "Scientific Calculator",
     "A free online scientific calculator with brackets, powers, roots, logarithms, trigonometry and factorials.",
     ['<div class="fld wide"><label for="ex">Expression</label><input type="text" id="ex" value="2*(3+4)^2" autocomplete="off" spellcheck="false"></div>',
      sel("ang", "Angle unit", [("deg", "Degrees"), ("rad", "Radians")], "deg"),
      '<div class="fld wide">' + PAD_CSS + '<div id="pad"></div></div>'],
     info("Type a full expression or use the keypad. The calculator follows the standard order of operations: brackets, powers, multiplication and division, then addition and subtraction.",
          "Supported: + - * / ^ ( ) ! %, sin cos tan asin acos atan, sqrt cbrt, log (base 10), ln, exp, abs, and the constants pi and e. Example inputs: sin(30), sqrt(144), 5!, 2^10.",
          "2*(3+4)^2 is worked out as 3 + 4 = 7, then 7^2 = 49, then 2 x 49 = 98. In degree mode sin(30) = 0.5."),
     [("Does it follow the order of operations?", "Yes. Brackets are done first, then powers, then multiplication and division, then addition and subtraction."),
      ("How do I switch between degrees and radians?", "Use the angle unit selector. Degrees are the default, which suits most school problems."),
      ("What does the ! symbol mean?", "It is the factorial. For example 5! = 5 x 4 x 3 x 2 x 1 = 120.")],
     also=("education",))

# ---------- Fraction ----------
FRIC = [num("n1", "Fraction 1: numerator", 1, step="1", min=""), num("d1", "Fraction 1: denominator", 2, step="1", min=""),
        sel("op", "Operation", [("+", "Add (+)"), ("-", "Subtract (-)"), ("*", "Multiply (x)"), ("/", "Divide (/)")], "+"),
        num("n2", "Fraction 2: numerator", 3, step="1", min=""), num("d2", "Fraction 2: denominator", 4, step="1", min="")]
calc("fraction-calculator", "m_frac", "math", "divide", "Fraction Calculator", "Add, subtract, multiply and divide fractions", "Fraction Calculator",
     "Add, subtract, multiply or divide two fractions and get the answer in simplest form, as a mixed number and as a decimal.", FRIC,
     info("This calculator works with two fractions and always reduces the answer to its simplest form.",
          "Add: a/b + c/d = (ad + cb) / bd. Subtract: (ad - cb) / bd. Multiply: ac / bd. Divide: ad / bc. The result is divided by the greatest common divisor to simplify.",
          "1/2 + 3/4 = (1 x 4 + 3 x 2) / (2 x 4) = 10/8, which simplifies to 5/4, or 1 1/4, or 1.25."),
     [("How do I add fractions with different denominators?", "Find a common denominator, convert both fractions, then add the numerators."),
      ("How do I divide fractions?", "Flip the second fraction (take its reciprocal) and multiply."),
      ("What is a mixed number?", "A whole number combined with a proper fraction, such as 1 1/4.")],
     also=("education",))

# ---------- Square root ----------
calc("square-root-calculator", "m_sqrt", "math", "triangle", "Square Root Calculator", "Square root, cube root and nth root", "Square Root Calculator",
     "Find the square root, cube root or any root of a number and check whether it is a perfect square.",
     [num("x", "Number", 50, min=""), sel("k", "Root", [("sqrt", "Square root"), ("cbrt", "Cube root"), ("nth", "Nth root")], "sqrt"), num("n", "Root index (n)", 4, when="k=nth", step="1")],
     info("The square root of a number is the value that, multiplied by itself, gives that number. The calculator also handles cube roots and nth roots.",
          "The nth root of x is x raised to the power 1/n. The square root is the case n = 2.",
          "The square root of 50 is about 7.0711 because 7.0711 x 7.0711 is about 50. It lies between the perfect squares 49 (7 x 7) and 64 (8 x 8)."),
     [("Can I take the square root of a negative number?", "Not in real numbers. Odd roots such as the cube root do work for negative numbers."),
      ("What is a perfect square?", "A whole number that is the square of another whole number, such as 16, 25 and 144."),
      ("How do I estimate a square root by hand?", "Find the two nearest perfect squares, then refine the guess by averaging and dividing.")],
     also=("education",))

# ---------- Ratio ----------
calc("ratio-calculator", "m_ratio", "math", "scale", "Ratio Calculator", "Simplify ratios and solve proportions", "Ratio Calculator",
     "Simplify a ratio to its lowest terms or find the missing value in a proportion.",
     [sel("m", "Mode", [("s", "Simplify a ratio A : B"), ("p", "Solve A : B = C : x")], "s"),
      num("s_a", "A", 24, when="m=s"), num("s_b", "B", 36, when="m=s"),
      num("p_a", "A", 2, when="m=p"), num("p_b", "B", 3, when="m=p"), num("p_c", "C", 10, when="m=p")],
     info("A ratio compares two quantities. Simplifying it to lowest terms makes it easier to read, and solving a proportion finds a missing quantity.",
          "To simplify, divide both numbers by their greatest common divisor. To solve A : B = C : x, use x = B x C / A.",
          "24 : 36 simplifies to 2 : 3 because both are divisible by 12. In 2 : 3 = 10 : x, x = 3 x 10 / 2 = 15."),
     [("What is a ratio?", "A way to compare two quantities, written as A : B or A/B."),
      ("How do I use ratios in recipes?", "Scale every ingredient by the same factor. To double a recipe, multiply each quantity by 2."),
      ("Can I use decimals?", "Yes. The calculator converts decimals to whole numbers before simplifying.")],
     also=("education",))

# ---------- Probability ----------
calc("probability-calculator", "m_prob", "math", "target", "Probability Calculator", "Chance of single and combined events", "Probability Calculator",
     "Work out the probability of one event or combine two independent events: both, either, neither or exactly one.",
     [sel("m", "Type", [("s", "Single event (favourable / total)"), ("c", "Two independent events")], "s"),
      num("s_f", "Favourable outcomes", 4, when="m=s"), num("s_t", "Total outcomes", 52, when="m=s", step="1"),
      num("c_a", "Probability of A (%)", 50, when="m=c"), num("c_b", "Probability of B (%)", 30, when="m=c")],
     info("Probability measures how likely an event is, from 0 (impossible) to 1 (certain). This calculator covers simple events and combinations of two independent events.",
          "P(event) = favourable outcomes / total outcomes. For independent events: P(A and B) = P(A) x P(B). P(A or B) = P(A) + P(B) - P(A) x P(B). P(not A) = 1 - P(A).",
          "Drawing an ace from a 52-card deck has probability 4 / 52 = 0.0769 (7.69%). If A is 50% and B is 30%, both happen 15% of the time and at least one happens 65% of the time."),
     [("What does independent mean?", "Two events are independent if one happening does not change the chance of the other, such as two separate coin tosses."),
      ("Can a probability be more than 1?", "No. Probabilities range from 0 to 1, or 0% to 100%."),
      ("What are odds?", "Odds compare favourable to unfavourable outcomes. A probability of 4/52 gives odds of 4 to 48.")],
     also=("education",))
