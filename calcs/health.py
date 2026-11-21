from core import *
import math, datetime

MED = ("These calculators give general estimates and are not medical advice. Talk to a doctor or registered dietitian before changing your diet, "
       "exercise or health routine.")
SEX = [("m", "Male"), ("f", "Female")]
ACT = [("1.2", "Sedentary (little or no exercise)"), ("1.375", "Light (1-3 days a week)"), ("1.55", "Moderate (3-5 days a week)"),
       ("1.725", "Very active (6-7 days a week)"), ("1.9", "Extra active (hard training or physical job)")]
def mif(kg, cm, age, sex="m"):
    return 10 * kg + 6.25 * cm - 5 * age + (5 if sex == "m" else -161)
def body(sex_default="m", age=30, kg=70, cm=170, act=None):
    f = [sel("sex", "Sex", SEX, sex_default), num("age", "Age (years)", age), num("kg", "Weight (kg)", kg), num("cm", "Height (cm)", cm)]
    if act: f.append(sel("act", "Activity level", ACT, act))
    return f
FAQ_MED = ("Is this calculator a substitute for medical advice?", "No. It uses standard formulas to give a general estimate. Individual needs vary, so please consult a doctor or registered dietitian for personal advice.")

# ---------- BMI ----------
b = 70 / 1.7 ** 2
calc("bmi-calculator", "bmi", "health", "scale", "BMI Calculator", "Body mass index and healthy weight range", "BMI Calculator",
     "Check your body mass index and see the healthy weight range for your height.",
     [sel("u", "Units", [("m", "Metric (kg, cm)"), ("i", "Imperial (lb, ft, in)")], "m"),
      num("kg", "Weight (kg)", 70, when="u=m"), num("cm", "Height (cm)", 170, when="u=m"),
      num("lb", "Weight (lb)", 154, when="u=i"), num("ft", "Height (feet)", 5, when="u=i"), num("inch", "Height (inches)", 7, when="u=i")],
     info("Body mass index (BMI) compares your weight with your height. It is widely used to screen for underweight, overweight and obesity in adults.",
          "BMI = weight in kg / (height in metres)^2. Categories: below 18.5 underweight, 18.5 to 24.9 normal, 25 to 29.9 overweight, 30 and above obese.",
          f"A person who weighs 70 kg and is 170 cm tall has a BMI of 70 / (1.70 x 1.70) = {b:.1f}, which is in the normal range."),
     [("What is a healthy BMI?", "For most adults a BMI between 18.5 and 24.9 is considered healthy."),
      ("Is BMI accurate for athletes?", "Not always. BMI cannot tell muscle from fat, so muscular people may show a high BMI even with low body fat."),
      ("Does BMI work for children?", "Children and teenagers are assessed using BMI-for-age percentiles, so this adult calculator should not be used for them."),
      FAQ_MED])

# ---------- BMR ----------
m = mif(70, 170, 30)
calc("bmr-calculator", "bmr", "health", "flame", "BMR Calculator", "Calories your body burns at rest", "BMR Calculator",
     "Find your basal metabolic rate, the calories your body needs just to stay alive.", body(),
     info("Basal metabolic rate (BMR) is the energy your body uses at complete rest for breathing, circulation and cell repair. It is the base for working out your daily calorie needs.",
          "Mifflin-St Jeor: BMR = 10 x weight (kg) + 6.25 x height (cm) - 5 x age + 5 for men or - 161 for women. The Harris-Benedict equation is shown for comparison.",
          f"A 30-year-old man who weighs 70 kg and is 170 cm tall has a BMR of {m:.0f} kcal per day."),
     [("What is the difference between BMR and TDEE?", "BMR is what you burn at rest. TDEE adds the calories used in daily movement and exercise, so it is always higher."),
      ("Which BMR formula is most accurate?", "Mifflin-St Jeor is generally considered the most reliable for healthy adults, but all formulas are estimates."),
      FAQ_MED])

# ---------- TDEE ----------
t = m * 1.55
calc("tdee-calculator", "tdee", "health", "activity", "TDEE Calculator", "Total daily energy expenditure", "TDEE Calculator",
     "Estimate the total calories you burn in a day, including exercise.", body(act="1.55"),
     info("Total daily energy expenditure (TDEE) is the number of calories you burn in a day. Eating this amount keeps your weight steady.",
          "TDEE = BMR x activity multiplier. Multipliers: 1.2 sedentary, 1.375 light, 1.55 moderate, 1.725 very active, 1.9 extra active.",
          f"A 30-year-old man (70 kg, 170 cm) with a BMR of {m:.0f} kcal who exercises moderately has a TDEE of {m:.0f} x 1.55 = {t:.0f} kcal."),
     [("How do I choose my activity level?", "Pick the level that matches your typical week. If unsure, choose the lower one because people often overestimate activity."),
      ("How do I lose weight using TDEE?", "Eat somewhat below your TDEE. A deficit of 300 to 500 kcal a day is a common, sustainable starting point."),
      FAQ_MED])

# ---------- Ideal weight ----------
inch = 170 / 2.54; over = inch - 60; dev = 50 + 2.3 * over
calc("ideal-weight-calculator", "ideal", "health", "target", "Ideal Weight Calculator", "Target weight for your height", "Ideal Weight Calculator",
     "See your ideal body weight using four well-known formulas.",
     [sel("sex", "Sex", SEX, "m"), num("cm", "Height (cm)", 170)],
     info("Ideal body weight formulas estimate a healthy weight from your height and sex. This calculator shows four common formulas and their average.",
          "Each formula adds a fixed amount of weight for every inch of height over 5 feet. For example, Devine: men 50 kg + 2.3 kg per inch, women 45.5 kg + 2.3 kg per inch.",
          f"A man who is 170 cm tall (about {inch:.1f} inches) has a Devine ideal weight of 50 + 2.3 x {over:.1f} = {dev:.1f} kg."),
     [("Are ideal weight formulas accurate?", "They are rough guides. Frame size, muscle mass and age all matter, so use them together with BMI and waist measurements."),
      ("Why do the formulas give different answers?", "They were developed from different data sets and for different purposes, so the results differ by a few kilograms."),
      FAQ_MED])

# ---------- Body fat ----------
bf = 86.010 * math.log10(90 - 38) - 70.041 * math.log10(175) + 36.76
calc("body-fat-calculator", "bodyfat", "health", "user", "Body Fat Calculator", "Body fat percentage (US Navy method)", "Body Fat Calculator",
     "Estimate your body fat percentage from simple tape measurements using the US Navy method.",
     [sel("sex", "Sex", SEX, "m"), num("cm", "Height (cm)", 175), num("neck", "Neck circumference (cm)", 38),
      num("waist", "Waist circumference (cm)", 90), num("hip", "Hip circumference (cm)", 95, when="sex=f"), num("kg", "Body weight (kg), optional", 75)],
     info("This calculator estimates body fat from your height, neck and waist (and hip for women). It uses the US Navy circumference method, which needs only a tape measure.",
          "Men: 86.010 x log10(waist - neck) - 70.041 x log10(height) + 36.76. Women: 163.205 x log10(waist + hip - neck) - 97.684 x log10(height) - 78.387. All measures in cm. Waist is taken at the navel for men and the narrowest point for women.",
          f"A man who is 175 cm tall with a 38 cm neck and 90 cm waist has about {bf:.1f}% body fat."),
     [("How accurate is the Navy method?", "It is usually within a few percentage points of other methods, but careful, consistent measurements matter."),
      ("What is a healthy body fat percentage?", "Roughly 14 to 24% for men and 21 to 31% for women is considered average to fit, but healthy ranges vary with age."),
      FAQ_MED])

# ---------- Calorie ----------
calc("calorie-calculator", "calorie", "health", "flame", "Calorie Calculator", "Daily calories to maintain, lose or gain weight", "Calorie Calculator",
     "Find how many calories to eat each day to maintain, lose or gain weight.", body(act="1.55"),
     info("This calculator estimates your daily calorie needs and shows targets for slow and steady weight loss or gain.",
          "Maintenance = BMR (Mifflin-St Jeor) x activity multiplier. About 7,700 kcal equals 1 kg of body weight, so a 550 kcal daily deficit gives roughly 0.5 kg of loss per week.",
          f"A 30-year-old man (70 kg, 170 cm, moderately active) needs about {t:.0f} kcal to maintain weight and about {t-550:.0f} kcal to lose 0.5 kg a week."),
     [("How fast should I lose weight?", "A loss of 0.25 to 0.5 kg per week is generally considered safe and sustainable for most adults."),
      ("Can I eat less than the minimum shown?", "Very low calorie diets should only be followed under medical supervision."),
      FAQ_MED])

# ---------- Protein ----------
calc("protein-intake-calculator", "protein", "health", "weight", "Protein Intake Calculator", "Daily protein for your goal", "Protein Intake Calculator",
     "Work out how many grams of protein you need each day.",
     [num("kg", "Body weight (kg)", 70),
      sel("goal", "Goal", [("0.8", "General health (0.8 g/kg)"), ("1.2", "Active lifestyle (1.2 g/kg)"), ("1.6", "Build muscle (1.6 g/kg)"), ("2.0", "Hard training or fat loss (2.0 g/kg)")], "1.2")],
     info("Protein supports muscle repair, hormones and immune health. Your need depends on body weight and how active you are.",
          "Daily protein (g) = body weight (kg) x grams per kg. Common targets are 0.8 g/kg for general health, 1.2 to 1.6 g/kg for active people and up to 2.0 g/kg for intense training.",
          f"A 70 kg person aiming for 1.2 g/kg needs {70*1.2:.0f} g of protein a day, or about {70*1.2/4:.0f} g in each of four meals."),
     [("Is too much protein harmful?", "For healthy people, intakes within these ranges are generally safe. People with kidney disease should follow their doctor's advice."),
      ("Should I use my goal weight or current weight?", "Most guidance uses current body weight, or a healthy target weight if you are significantly overweight."),
      FAQ_MED])

# ---------- Water ----------
w = 70 * 0.033
calc("water-intake-calculator", "water", "health", "beaker", "Water Intake Calculator", "How much water to drink each day", "Water Intake Calculator",
     "Estimate your daily water need from body weight, exercise and climate.",
     [num("kg", "Body weight (kg)", 70), num("min", "Exercise per day (minutes)", 30),
      sel("clim", "Climate", [("0", "Cool or moderate"), ("0.5", "Warm"), ("1", "Hot and humid")], "0")],
     info("Staying hydrated helps energy, digestion and concentration. Your water need rises with body weight, exercise and heat.",
          "Base need = 33 ml per kg of body weight. Add about 350 ml for every 30 minutes of exercise and 0.5 to 1 litre in warm or hot weather.",
          f"A 70 kg person has a base need of {w:.1f} litres. With 30 minutes of exercise in moderate weather that becomes {w+0.35:.1f} litres a day."),
     [("Do tea, coffee and food count?", "Yes. Most drinks and water-rich foods such as fruit and soup contribute to your daily fluid intake."),
      ("How do I know if I am drinking enough?", "Pale yellow urine and rarely feeling thirsty are good signs."),
      FAQ_MED])

# ---------- Pregnancy ----------
lmp = datetime.date(2026, 10, 1); due = lmp + datetime.timedelta(days=280)
calc("pregnancy-due-date-calculator", "preg", "health", "baby", "Pregnancy Due Date Calculator", "Estimated due date and weeks pregnant", "Pregnancy Due Date Calculator",
     "Find your estimated due date and how far along you are from the first day of your last period.",
     [dat("lmp", "First day of last period", "2026-10-01"), num("cycle", "Average cycle length (days)", 28)],
     info("Your estimated due date is based on the first day of your last menstrual period (LMP). The calculator also shows how many weeks pregnant you are today.",
          "Naegele's rule: due date = LMP + 280 days (40 weeks), adjusted if your cycle is longer or shorter than 28 days.",
          f"If the last period began on 1 October 2026, the estimated due date is {due.strftime('%-d %B %Y')}."),
     [("How accurate is the due date?", "Only about 4% of babies are born on the due date. Most arrive within two weeks either side."),
      ("What if my cycle is irregular?", "An early ultrasound gives a more reliable due date. Your doctor may adjust it."),
      FAQ_MED])

# ---------- Ovulation ----------
ov = lmp + datetime.timedelta(days=14)
calc("ovulation-calculator", "ovul", "health", "calendar", "Ovulation Calculator", "Fertile window and ovulation day", "Ovulation Calculator",
     "Estimate your ovulation day and fertile window from your cycle.",
     [dat("lmp", "First day of last period", "2026-10-01"), num("cycle", "Average cycle length (days)", 28)],
     info("Ovulation usually happens about 14 days before the next period. The days just before and on ovulation are the most fertile.",
          "Ovulation day = first day of last period + (cycle length - 14). The fertile window runs from 5 days before to 1 day after ovulation.",
          f"With a 28-day cycle starting on 1 October 2026, ovulation is around {ov.strftime('%-d %B %Y')} and the fertile window is {(ov - datetime.timedelta(days=5)).strftime('%-d %B')} to {(ov + datetime.timedelta(days=1)).strftime('%-d %B')}."),
     [("Can I rely on this to avoid pregnancy?", "No. Cycles vary and this is only an estimate, so it is not a reliable method of contraception."),
      ("What if my cycle is irregular?", "Predictions are less accurate. Ovulation test kits or advice from a doctor can help."),
      FAQ_MED])

# ---------- WHtR ----------
calc("waist-to-height-ratio-calculator", "whtr", "health", "ruler", "Waist-to-Height Ratio Calculator", "Check health risk from your waist size", "Waist-to-Height Ratio Calculator",
     "Compare your waist with your height to see if your body shape raises health risk.",
     [num("cm", "Height (cm)", 170), num("waist", "Waist circumference (cm)", 82)],
     info("The waist-to-height ratio (WHtR) is a simple screening tool for fat around the middle, which is linked to heart disease and diabetes.",
          "WHtR = waist circumference / height (same units). Below 0.5 is generally healthy; 0.5 to 0.59 is increased risk; 0.6 and above is high risk.",
          f"A person who is 170 cm tall with an 82 cm waist has a ratio of 82 / 170 = {82/170:.2f}, which is healthy."),
     [("Why use WHtR instead of BMI?", "It reflects where fat is stored. Fat around the waist is more strongly linked to health risk than overall weight."),
      ("Where do I measure my waist?", "Measure halfway between the bottom of your ribs and the top of your hip bones, after breathing out normally."),
      FAQ_MED])

# ---------- Macro ----------
calc("macro-calculator", "macro", "health", "pie", "Macro Calculator", "Daily carbs, protein and fat targets", "Macro Calculator",
     "Split your daily calories into carbohydrates, protein and fat.",
     [num("cal", "Maintenance calories per day", 2200),
      sel("goal", "Goal", [("-500", "Lose weight (-500 kcal)"), ("0", "Maintain weight"), ("300", "Gain muscle (+300 kcal)")], "0"),
      sel("split", "Diet style", [("bal", "Balanced (40/30/30)"), ("low", "Lower carb (25/35/40)"), ("high", "High protein (35/40/25)"), ("keto", "Keto (5/25/70)"), ("end", "Endurance (55/20/25)")], "bal")],
     info("Macronutrients are carbohydrates, protein and fat. This calculator turns your calorie goal into daily gram targets for each.",
          "Grams = calories x share / calories per gram. Carbohydrate and protein provide 4 kcal per gram, fat provides 9 kcal per gram.",
          f"On 2,200 kcal with a balanced 40/30/30 split you need {2200*.4/4:.0f} g carbohydrates, {2200*.3/4:.0f} g protein and {2200*.3/9:.0f} g fat."),
     [("Which split is best?", "There is no single best split. Choose one you can follow consistently and make sure protein is adequate."),
      ("Where do I get my maintenance calories?", "Use our TDEE or Calorie Calculator to estimate it."),
      FAQ_MED])

# ---------- Age (datetime primary, also health) ----------
calc("age-calculator", "age", "datetime", "cal-check", "Age Calculator", "Exact age in years, months and days", "Age Calculator",
     "Find your exact age in years, months, days and total days, plus your next birthday.",
     [dat("dob", "Date of birth", "1995-06-15"), dat("on", "Age at the date of", today=True)],
     info("This calculator finds your exact age as of any date, and also shows your age in months, weeks, days and hours.",
          "Age is the difference between the two dates. Years and months are counted first, and the remaining days are shown last.",
          "Someone born on 15 June 1995 is 30 years, 5 months and 6 days old on 21 November 2025, which is 11,117 days."),
     [("How is age calculated?", "The calculator subtracts the date of birth from the chosen date, counting complete years, then months, then days."),
      ("Can I find my age on a past or future date?", "Yes. Change the second date to any date you like."),
      ("Does it handle leap years?", "Yes. Leap days are included when counting total days, weeks and hours.")],
     also=("health",))

# ---------- DOB ----------
calc("date-of-birth-calculator", "dob", "health", "calendar", "Date of Birth Calculator", "Find birth date range from age", "Date of Birth Calculator",
     "Work out the year and date range someone was born from their age.",
     [dat("on", "Date of the age", today=True), num("age", "Age in completed years", 30, step="1")],
     info("If you know a person's age on a certain date, you can narrow their birth date to a one-year window.",
          "A person aged N on a date was born between that date minus (N + 1) years plus one day, and that date minus N years.",
          "A person aged 30 on 21 November 2026 was born between 22 November 1995 and 21 November 1996."),
     [("Can this give an exact birth date?", "No. Age alone only narrows it to a one-year window. You need the month and day for an exact date."),
      ("Which age should I enter?", "Enter completed years, not the age they are turning next."),
      FAQ_MED])

# ---------- Sleep ----------
calc("sleep-calculator", "sleep", "health", "clock", "Sleep Calculator", "Best bedtime or wake-up time", "Sleep Calculator",
     "Find the best time to go to bed or wake up so you finish a full sleep cycle.",
     [sel("mode", "I want to", [("w", "Wake up at a set time (find bedtime)"), ("b", "Go to bed at a set time (find wake-up)")], "w"), tim("t", "Time", "07:00")],
     info("Sleep runs in cycles of about 90 minutes. Waking at the end of a cycle usually feels easier than waking in the middle of one.",
          "Bedtime = wake time - (cycles x 90 minutes) - 14 minutes to fall asleep. Most adults need 5 to 6 cycles, which is 7.5 to 9 hours.",
          "To wake at 7:00 AM after 5 cycles, go to bed at 11:16 PM (7:00 AM - 7.5 hours - 14 minutes)."),
     [("How many hours of sleep do I need?", "Most adults need 7 to 9 hours. Teenagers and children need more."),
      ("Why 90 minutes?", "Sleep cycles through light, deep and REM stages in about 90 minutes on average, though it varies by person."),
      FAQ_MED])
