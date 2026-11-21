from core import *

MULT_FAQ = ("Which multiplier should I use?", "CBSE uses 9.5. Many universities use 10 or their own formula, so check your institution's rules before submitting the result anywhere official.")

# ---------- CGPA ----------
calc("cgpa-calculator", "e_cgpa", "education", "cap", "CGPA Calculator", "Cumulative grade point average from semesters", "CGPA Calculator",
     "Enter your semester grade points (SGPA) to get your CGPA and its percentage equivalent.",
     [txt("sg", "SGPA of each semester (separated by commas)", "8.2, 8.5, 7.9, 8.8", rows=2),
      txt("cr", "Credits of each semester (optional, leave empty for a simple average)", "", rows=2, placeholder="e.g. 22, 24, 22, 24"),
      num("mult", "Percentage multiplier", 9.5, step="0.01"), num("scale", "Grading scale (maximum grade point)", 10, step="1")],
     info("Cumulative grade point average (CGPA) combines your results from all semesters into one number. You can use a simple average or weight each semester by its credits.",
          "Simple CGPA = sum of SGPAs / number of semesters. Weighted CGPA = sum of (SGPA x credits) / total credits. Percentage = CGPA x multiplier (9.5 for CBSE).",
          "For SGPAs of 8.2, 8.5, 7.9 and 8.8 the CGPA is 33.4 / 4 = 8.35. With the 9.5 multiplier this is about 79.3%."),
     [("What is the difference between SGPA and CGPA?", "SGPA is the grade point average for one semester. CGPA is the average across all completed semesters."),
      MULT_FAQ,
      ("Should I use credits?", "If your university weights semesters by credits, enter them. Otherwise the simple average is fine.")])

# ---------- CGPA to % ----------
calc("cgpa-to-percentage-calculator", "e_cgpap", "education", "percent", "CGPA to Percentage Calculator", "Convert CGPA to percentage", "CGPA to Percentage Calculator",
     "Convert your CGPA on a 10-point scale to a percentage using the CBSE multiplier of 9.5 or your own.",
     [num("cgpa", "CGPA (out of 10)", 8.5, step="0.01"), num("mult", "Multiplier", 9.5, step="0.01")],
     info("Many schools and universities convert CGPA to a percentage by multiplying by a fixed number. CBSE uses 9.5.",
          "Percentage = CGPA x multiplier.",
          "A CGPA of 8.5 with the 9.5 multiplier gives 8.5 x 9.5 = 80.75%."),
     [("What is the CBSE formula?", "Multiply the CGPA by 9.5 to get an approximate percentage."), MULT_FAQ,
      ("Is the converted percentage official?", "No. It is an approximation. Use the percentage on your official marksheet where one is provided.")])

# ---------- % to CGPA ----------
calc("percentage-to-cgpa-calculator", "e_pcgpa", "education", "divide", "Percentage to CGPA Calculator", "Convert percentage to CGPA", "Percentage to CGPA Calculator",
     "Convert your percentage into a CGPA on a 10-point scale.",
     [num("pct", "Percentage (%)", 76, step="0.01"), num("mult", "Divisor", 9.5, step="0.01")],
     info("To convert a percentage back to CGPA, divide it by the same multiplier that your board or university uses.",
          "CGPA = percentage / multiplier. For CBSE the multiplier is 9.5.",
          "A percentage of 76 divided by 9.5 gives a CGPA of 8.0."),
     [("How do I convert percentage to CGPA for CBSE?", "Divide the percentage by 9.5."), MULT_FAQ,
      ("Can the CGPA be more than 10?", "No. If the result exceeds 10, check the percentage and multiplier.")])

# ---------- GPA ----------
GR = [("4", "A (4.0)"), ("3.7", "A- (3.7)"), ("3.3", "B+ (3.3)"), ("3", "B (3.0)"), ("2.7", "B- (2.7)"), ("2.3", "C+ (2.3)"), ("2", "C (2.0)"), ("1.7", "C- (1.7)"), ("1", "D (1.0)"), ("0", "F (0.0)"), ("x", "Not used")]
defaults = [("4", 4), ("3.7", 3), ("3.3", 4), ("3", 3), ("x", 3), ("x", 3)]
gf = []
for i, (g, c) in enumerate(defaults, 1):
    gf += [sel(f"g{i}", f"Course {i} grade", GR, g), num(f"c{i}", f"Course {i} credits", c, step="0.5")]
calc("gpa-calculator", "e_gpa", "education", "book", "GPA Calculator", "Grade point average on the 4.0 scale", "GPA Calculator",
     "Add your courses, grades and credit hours to calculate your semester or cumulative GPA.", gf,
     info("Grade point average (GPA) is the weighted average of your course grades on a 4.0 scale. Courses with more credit hours count more.",
          "GPA = sum of (grade points x credits) / total credits. A = 4.0, A- = 3.7, B+ = 3.3, B = 3.0, and so on.",
          "Courses: A (4 credits), A- (3 credits), B+ (4 credits), B (3 credits). Quality points = 16 + 11.1 + 13.2 + 9 = 49.3 over 14 credits, so GPA = 3.52."),
     [("How is GPA calculated?", "Multiply each grade point by the course credits, add them up and divide by total credits."),
      ("What is a good GPA?", "3.0 or higher is generally considered good, and 3.5 or higher is strong, though expectations differ by program."),
      ("Can I include courses I want to estimate?", "Yes. Enter the grade you expect and see how it changes your GPA.")])

# ---------- Marks ----------
mf = []
for i, (o, m) in enumerate([(78, 100), (85, 100), (92, 100), (67, 100), (74, 100), (0, 0)], 1):
    mf += [num(f"o{i}", f"Subject {i}: marks obtained", o), num(f"m{i}", f"Subject {i}: maximum marks", m)]
calc("marks-percentage-calculator", "e_marks", "education", "clipboard", "Marks Percentage Calculator", "Total marks and percentage", "Marks Percentage Calculator",
     "Enter marks for up to six subjects to get your total, percentage, grade and division.", mf,
     info("This calculator adds your marks across subjects and shows your overall percentage, grade and division. Leave maximum marks at 0 for subjects you do not need.",
          "Percentage = total marks obtained / total maximum marks x 100.",
          "Marks of 78, 85, 92, 67 and 74 out of 100 each total 396 out of 500, which is 79.2% (grade B, first division)."),
     [("How do I calculate percentage from marks?", "Divide your total marks by the maximum marks and multiply by 100."),
      ("Can subjects have different maximum marks?", "Yes. Each subject has its own maximum, and the calculator uses the totals."),
      ("What is first division?", "Commonly 60% and above, second division 45% to 59%, third division 33% to 44%. Boards differ.")])

# ---------- Grade ----------
calc("grade-calculator", "e_grade", "education", "target", "Grade Calculator", "Letter grade and score needed on the final exam", "Grade Calculator",
     "Convert a percentage to a letter grade, and find the score you need on your final exam to reach a target grade.",
     [num("pct", "Your percentage (%)", 78), num("cur", "Current course grade (%)", 70), num("w", "Weight of final exam (%)", 40), num("tgt", "Target course grade (%)", 80)],
     info("Enter a percentage to see its letter grade. Use the second part to find the score you need in your final exam to reach a target overall grade.",
          "Needed score = (target - current x (1 - weight)) / weight, where weight is the final exam's share as a decimal.",
          "With a current grade of 70%, a final exam worth 40% and a target of 80%, you need (80 - 70 x 0.6) / 0.4 = 95% on the final exam. A percentage of 78 is a grade B."),
     [("How do I calculate the grade I need?", "Use the formula above, or enter your current grade, the exam weight and your target."),
      ("Why does my school give different grades?", "Grade bands differ between schools and boards. The bands shown here are a common default."),
      ("What if the needed score is over 100%?", "The target is not reachable with that exam alone, so aim for a lower target or look for extra credit.")])

# ---------- Age difference ----------
calc("age-difference-calculator", "e_agediff", "education", "users", "Age Difference Calculator", "Gap between two people's ages", "Age Difference Calculator",
     "Find the exact age difference between two people in years, months and days.",
     [dat("d1", "Person 1 date of birth", "1990-03-12"), dat("d2", "Person 2 date of birth", "1994-08-25")],
     info("This calculator finds the exact gap between two dates of birth and shows who is older.",
          "The earlier date is subtracted from the later one, counting complete years, then months, then days.",
          "For 12 March 1990 and 25 August 1994 the age difference is 4 years, 5 months and 13 days. Person 1 is older."),
     [("How is age difference calculated?", "By subtracting the earlier birth date from the later one."),
      ("Can I compare dates of any two events?", "Yes. It works for any two dates. See our Date Difference Calculator for more detail."),
      ("Does it handle leap years?", "Yes. Leap days are counted in the total days.")])

# ---------- Date difference ----------
calc("date-difference-calculator", "e_datediff", "education", "calendar", "Date Difference Calculator", "Time between two dates", "Date Difference Calculator",
     "Find the exact number of years, months, weeks and days between any two dates.",
     [dat("d1", "Start date", "2026-01-01"), dat("d2", "End date", today=True), chk("inc", "Include the end date in the count")],
     info("This calculator measures the time between two dates in years, months, days, weeks and hours.",
          "The earlier date is subtracted from the later one. Years and months are counted first, with the remaining days shown last. Tick the option to count both the start and end day.",
          "From 1 January 2026 to 21 November 2026 is 10 months and 20 days, which is 324 days or 46 weeks and 2 days."),
     [("Does the calculator include the end date?", "Not by default. Tick the option if you want to count both the first and last day."),
      ("What if my start date is after the end date?", "The calculator swaps them so you always get a positive difference."),
      ("Can I use it for deadlines?", "Yes. Enter today as the start date and the deadline as the end date.")],
     also=("datetime",))

# ---------- Time ----------
calc("time-calculator", "e_time", "education", "clock", "Time Calculator", "Add or subtract hours, minutes and seconds", "Time Calculator",
     "Add or subtract two times given in hours, minutes and seconds.",
     [num("h1", "Time 1: hours", 2, step="1"), num("m1", "Time 1: minutes", 45, step="1"), num("s1", "Time 1: seconds", 30, step="1"),
      sel("op", "Operation", [("+", "Add (+)"), ("-", "Subtract (-)")], "+"),
      num("h2", "Time 2: hours", 1, step="1"), num("m2", "Time 2: minutes", 30, step="1"), num("s2", "Time 2: seconds", 45, step="1")],
     info("Use this calculator to add or subtract durations, for example total work time or video length. The result is shown as hours, minutes and seconds, as well as decimal hours.",
          "Convert each time to seconds (hours x 3600 + minutes x 60 + seconds), add or subtract, then convert back.",
          "2:45:30 + 1:30:45 = 9,930 + 5,445 = 15,375 seconds, which is 4 hours 16 minutes 15 seconds (4.2708 decimal hours)."),
     [("How do I add times?", "Add seconds first, carry over to minutes every 60, then add minutes and carry over to hours."),
      ("Can I get decimal hours?", "Yes. The result also shows decimal hours, which is useful for pay calculations."),
      ("What if the result is negative?", "That means the second time is larger than the first. The result is shown with a minus sign.")],
     also=("datetime",))
