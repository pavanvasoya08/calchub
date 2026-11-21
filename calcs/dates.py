from core import *
import datetime as _dt

def _fd(d):
    return d.strftime("%d %B %Y").lstrip("0")

def _f(d):
    return f"{d.day} {d.strftime('%B %Y')}"

# ---------- date-calculator ----------
_s = _dt.date(2026, 11, 20)
calc("date-calculator", "dcalc", "datetime", "calendar", "Date Calculator",
     "Add or subtract years, months and days from a date",
     "Date Calculator", "Add or subtract years, months and days from any date and see the weekday, week number and day of the year.",
     [dat("s", "Start date", today=True),
      sel("op", "Operation", [("add", "Add"), ("sub", "Subtract")], "add"),
      num("y", "Years", 0, step="1"), num("m", "Months", 1, step="1"), num("d", "Days", 15, step="1")],
     info("This date calculator moves a date forward or backward by any number of years, months and days. It also tells you which weekday the new date falls on, its ISO week number and its position in the year.",
          "Years and months are added first. If the target month is shorter than the start day (for example 31 January plus 1 month), the result is the last day of that month. Days are added after that.",
          f"{_f(_s)} plus 1 month and 15 days is {_f(_dt.date(2026,12,20)+_dt.timedelta(days=15))}, which is a {(_dt.date(2026,12,20)+_dt.timedelta(days=15)).strftime('%A')}."),
     [("How are months added when the day does not exist?", "If the new month is shorter, the calculator uses the last day of that month. For example 31 January plus 1 month gives 28 or 29 February."),
      ("What is the ISO week number?", "ISO weeks start on Monday and week 1 is the week that contains the first Thursday of the year."),
      ("Can I subtract more days than the date has?", "Yes. You can subtract any amount and the calculator moves across months and years correctly."),
      ("What is the difference between this and the Date Add/Subtract Calculator?", "This one lets you mix years, months and days in one step and shows extra details about the result date.")])

# ---------- days-between ----------
_a, _b = _dt.date(2026, 1, 1), _dt.date(2026, 11, 20)
calc("days-between-dates-calculator", "between", "datetime", "cal-check", "Days Between Dates",
     "Count the days, weeks and months between two dates",
     "Days Between Dates Calculator", "Find the exact number of days, weeks and months between any two dates.",
     [dat("a", "Start date", "2026-01-01"), dat("b", "End date", today=True), chk("inc", "Include the end date in the count")],
     info("Enter two dates to see the number of days between them, plus the same gap in weeks, months and hours. It also shows which weekday each date falls on.",
          "Days = end date minus start date. When the box is ticked, one extra day is counted so that both the start and the end date are included. The years, months and days breakdown counts full calendar months.",
          f"From {_f(_a)} to {_f(_b)} is {(_b-_a).days} days, which is {(_b-_a).days//7} weeks and {(_b-_a).days%7} days."),
     [("Does the count include the end date?", "By default no. Tick the box if you want both dates to be counted, which adds one day."),
      ("What if the end date is before the start date?", "The calculator swaps the dates for you and shows the gap as a positive number."),
      ("Are leap years handled?", "Yes. Real calendar dates are used, so 29 February is counted in leap years."),
      ("How do I find the number of working days instead?", "Use the Working Days Calculator to exclude weekends and holidays.")])

# ---------- working-days ----------
_w1, _w2 = _dt.date(2026, 11, 1), _dt.date(2026, 11, 30)
_wd = sum(1 for i in range((_w2 - _w1).days + 1) if (_w1 + _dt.timedelta(days=i)).weekday() < 5)
calc("working-days-calculator", "working", "datetime", "briefcase", "Working Days Calculator",
     "Count working days between two dates",
     "Working Days Calculator", "Count the working days between two dates. Choose which days are the weekend and subtract public holidays.",
     [dat("a", "Start date", "2026-11-01"), dat("b", "End date", "2026-11-30"),
      sel("wk", "Weekend days", [("ss", "Saturday and Sunday"), ("s", "Sunday only"), ("none", "No weekend (7-day week)")], "ss"),
      num("h", "Public holidays to subtract", 0, step="1")],
     info("The working days calculator counts the days in a date range that are not weekends and not holidays. Both the start date and the end date are included.",
          "Working days = total days in the range - weekend days - holidays. Weekend days are found by checking the weekday of every date in the range.",
          f"From {_f(_w1)} to {_f(_w2)} there are 30 days, and {_wd} of them are Monday to Friday."),
     [("Are the start and end dates included?", "Yes, both dates are counted if they are working days."),
      ("How do I handle public holidays?", "Enter the number of holidays that fall on working days in the range and they are subtracted from the result."),
      ("Can I use a six-day working week?", "Yes. Choose 'Sunday only' as the weekend."),
      ("Is this the same as business days?", "Mostly yes. The Business Days Calculator also lets you add or subtract business days from a date.")],
     also=("business",))

# ---------- business-days ----------
calc("business-days-calculator", "bizdays", "datetime", "briefcase", "Business Days Calculator",
     "Count or add business days (Monday to Friday)",
     "Business Days Calculator", "Count the business days between two dates, or add and subtract business days from a date.",
     [sel("mode", "What do you want to do?", [("between", "Count business days between dates"), ("add", "Add business days to a date"), ("sub", "Subtract business days from a date")], "between"),
      dat("a", "Start date", today=True), dat("b", "End date", "2027-01-31", when="mode=between"),
      num("n", "Number of business days", 10, when="mode=add|sub", step="1"),
      num("h", "Holidays to subtract", 0, when="mode=between", step="1")],
     info("Business days are Monday to Friday. Use this calculator to find how many business days lie between two dates, or to find the date that is a certain number of business days from today.",
          "Counting: every date in the range that is not Saturday or Sunday is counted, then holidays are subtracted. Adding: the calculator steps one day at a time and only counts weekdays until the target number is reached.",
          "Adding 10 business days to Friday 20 November 2026 gives Friday 4 December 2026 because two weekends are skipped."),
     [("Which days are business days?", "Monday to Friday. Saturdays and Sundays are skipped."),
      ("Does the count include the start date?", "When counting between dates, yes. When adding days, counting starts from the day after the start date."),
      ("Are public holidays skipped automatically?", "No. Enter the number of holidays in count mode, or add extra days yourself in add mode."),
      ("Can I subtract business days?", "Yes. Choose 'Subtract business days from a date'.")],
     also=("business",))

# ---------- countdown ----------
calc("countdown-calculator", "cd", "datetime", "hourglass", "Countdown Calculator",
     "Live countdown to any date and time",
     "Countdown Calculator", "See a live countdown in days, hours, minutes and seconds to any future date and time.",
     [dtl("t", "Target date and time", "2027-01-01T00:00")],
     info("Pick a date and time and this countdown updates every second to show how long is left. It works for birthdays, holidays, exams, launches and deadlines.",
          "Time left = target date and time minus the current time of your device. The result is split into whole days, hours, minutes and seconds. If the target is in the past, the time since it passed is shown instead.",
          "A countdown to 1 January 2027 at midnight, checked on 20 November 2026 at midnight, shows 42 days, 0 hours, 0 minutes and 0 seconds."),
     [("Does the countdown use my local time?", "Yes. The target is read in your device's time zone."),
      ("What happens when the time is over?", "The calculator shows how much time has passed since the target."),
      ("Do I need to keep the page open?", "The numbers update while the page is open. If you reload, it recalculates from the current time."),
      ("Does it count days or business days?", "It counts calendar days. For business days use the Business Days Calculator.")])

# ---------- time-duration ----------
calc("time-duration-calculator", "dur", "datetime", "clock", "Time Duration Calculator",
     "Find the time between a start and end time",
     "Time Duration Calculator", "Find the hours and minutes between a start time and an end time, even when it crosses midnight.",
     [tim("s", "Start time", "09:00"), tim("e", "End time", "17:30")],
     info("Enter a start time and an end time to see the duration in hours and minutes, in decimal hours and in total minutes.",
          "Duration = end time - start time. If the end time is earlier than the start time, the calculator assumes the end is on the next day and adds 24 hours.",
          "From 09:00 to 17:30 is 8 hours 30 minutes, which equals 8.5 decimal hours or 510 minutes."),
     [("What if the end time is after midnight?", "If the end time is earlier than the start time, it is treated as the next day."),
      ("What are decimal hours?", "Minutes divided by 60. 8 hours 30 minutes is 8.5 hours."),
      ("Can I calculate more than 24 hours?", "Use the Date Calculator or Days Between Dates Calculator for longer gaps."),
      ("Does it use 12-hour or 24-hour time?", "The input follows your device setting and the result uses hours and minutes.")])

# ---------- hours ----------
calc("hours-calculator", "hours", "datetime", "clock", "Hours Calculator",
     "Work hours, weekly total and pay",
     "Hours Calculator", "Work out your daily and weekly work hours after breaks, and your pay if you enter an hourly rate.",
     [tim("i", "Clock in", "09:00"), tim("o", "Clock out", "17:30"), num("b", "Unpaid break (minutes)", 30, step="1"),
      num("d", "Days worked per week", 5, step="1"), num("r", f"Hourly rate ({CUR}, optional)", 250)],
     info("This hours calculator works out how long you worked each day after subtracting your break, then multiplies by the days worked per week. Enter an hourly rate to see your pay.",
          "Daily hours = (clock out - clock in) - break. Weekly hours = daily hours x days per week. Pay = hours x hourly rate. If clock out is earlier than clock in, the shift is treated as overnight.",
          f"09:00 to 17:30 with a 30 minute break is 8 hours a day. Over 5 days that is 40 hours, and at {fmt(250)} an hour the weekly pay is {fmt(10000)}."),
     [("Is the break paid?", "This calculator treats the break as unpaid and subtracts it."),
      ("Can I use it for overnight shifts?", "Yes. If clock out is earlier than clock in, the shift runs into the next day."),
      ("Does it include overtime?", "No. All hours are paid at the single rate you enter."),
      ("How do I ignore pay?", "Set the hourly rate to 0 and only the hours are shown.")])

# ---------- date add/subtract ----------
calc("date-add-subtract-calculator", "addsub", "datetime", "plus-circle", "Date Add/Subtract Calculator",
     "Add or subtract days, weeks, months or years",
     "Date Add/Subtract Calculator", "Add days, weeks, months or years to a date, or subtract them, and see the new date.",
     [dat("s", "Start date", today=True), sel("op", "Operation", [("add", "Add"), ("sub", "Subtract")], "add"),
      num("n", "Amount", 90, step="1"),
      sel("u", "Unit", [("d", "Days"), ("w", "Weeks"), ("m", "Months"), ("y", "Years")], "d")],
     info("Choose a start date, then add or subtract a number of days, weeks, months or years. The new date is shown with its weekday.",
          "Days and weeks are added as 1 and 7 days each. Months and years keep the same day of the month, and use the last day of the month if it does not exist.",
          f"{_f(_s)} plus 90 days is {_f(_s+_dt.timedelta(days=90))}, a {(_s+_dt.timedelta(days=90)).strftime('%A')}."),
     [("How do I find the date 90 days from today?", "Leave the start date as today, choose Add, enter 90 and choose Days."),
      ("What happens to 31 January plus 1 month?", "It becomes the last day of February."),
      ("Can I subtract years?", "Yes. Choose Subtract and Years."),
      ("Is the weekday shown?", "Yes, the weekday of the new date is always displayed.")])

# ---------- time zone converter ----------
ZONES = [("Asia/Kolkata", "India (IST)"), ("UTC", "UTC"), ("Europe/London", "London (GMT/BST)"), ("Europe/Paris", "Central Europe (CET/CEST)"),
         ("Europe/Moscow", "Moscow"), ("Asia/Dubai", "Dubai (GST)"), ("Asia/Karachi", "Pakistan (PKT)"), ("Asia/Dhaka", "Bangladesh (BST)"),
         ("Asia/Singapore", "Singapore (SGT)"), ("Asia/Shanghai", "China (CST)"), ("Asia/Tokyo", "Japan (JST)"),
         ("Australia/Sydney", "Sydney (AEST/AEDT)"), ("Pacific/Auckland", "New Zealand (NZST/NZDT)"), ("Africa/Johannesburg", "South Africa (SAST)"),
         ("America/Sao_Paulo", "Sao Paulo (BRT)"), ("America/New_York", "New York (EST/EDT)"), ("America/Chicago", "Chicago (CST/CDT)"),
         ("America/Denver", "Denver (MST/MDT)"), ("America/Los_Angeles", "Los Angeles (PST/PDT)")]
import json as _json
calc("time-zone-converter", "tz", "datetime", "route", "Time Zone Converter",
     "Convert a time between world time zones",
     "Time Zone Converter", "Convert a date and time from one time zone to another, with daylight saving handled automatically.",
     [dat("d", "Date", today=True), tim("t", "Time", "09:00"),
      sel("f", "From time zone", ZONES, "Asia/Kolkata"), sel("to", "To time zone", ZONES, "America/New_York")],
     info("Pick a date, a time and two time zones to see what time it is in the second zone. The same moment is also shown in other major cities.",
          "The time is first converted to UTC using the offset of the source zone on that date, then shown in the target zone using its offset on that date. Daylight saving rules are applied by your browser's time zone data.",
          "9:00 AM in India (UTC+5:30) is 3:30 AM UTC. In New York that is 10:30 PM the previous day during standard time (UTC-5)."),
     [("Is daylight saving time included?", "Yes. Offsets are taken for the date you choose, so summer and winter times are correct."),
      ("What is UTC?", "Coordinated Universal Time is the global time standard that other zones are measured against."),
      ("Why does the date change?", "When the zones are far apart the converted time can fall on the previous or next day, and the result says so."),
      ("Can I convert future dates?", "Yes. Pick any date and the offsets for that date are used.")])
