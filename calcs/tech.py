from core import *
import math

def hms(sec):
    sec = round(sec); h, r = divmod(sec, 3600); m, s = divmod(r, 60)
    return (f"{h} h " if h else "") + (f"{m} min " if m or h else "") + f"{s} s"

# ---- speed & transfer ----
SPEED_U = [("1e6", "Mbps (megabits per second)"), ("8e6", "MB/s (megabytes per second)"), ("1e9", "Gbps (gigabits per second)"), ("1e3", "Kbps")]
calc("internet-speed-calculator", "inet", "tech", "gauge", "Internet Speed Calculator", "Convert Mbps to MB/s and see real download times",
     "Internet Speed Calculator", "Convert your internet speed between Mbps, MB/s and Gbps and see how long common downloads will take.",
     [num("speed", "Internet speed", 100), sel("u", "Speed unit", SPEED_U, "1e6"), num("eff", "Real-world efficiency (%)", 90)],
     info("Internet plans are sold in megabits per second (Mbps) but files are measured in megabytes (MB). This calculator converts between them and estimates the time to download typical files, after allowing for protocol overhead.",
          "1 byte = 8 bits, so MB/s = Mbps / 8. Download time = file size in bits / (speed in bits per second x efficiency).",
          f"A 100 Mbps connection is 12.5 MB/s. At 90% efficiency, a 1 GB file takes {hms(8e9/(100e6*0.9))} to download."),
     [("Why is my download slower than my plan speed?", "Wi-Fi quality, server speed, network congestion and protocol overhead all reduce real speed. 85% to 95% of the plan speed is typical."),
      ("What is the difference between Mbps and MB/s?", "Mbps is megabits per second and MB/s is megabytes per second. One megabyte is 8 megabits."),
      ("Is 100 Mbps fast enough?", "For most homes, yes. It handles several HD streams, video calls and large downloads at the same time.")])

def xfer_body(word, other):
    return info(f"Enter the size of the file and your connection speed to see how long a {word} will take. The calculator allows for overhead, because real-world speeds are always a little lower than the advertised speed.",
                "Time = file size in bits / (speed in bits per second x efficiency). File sizes use decimal units: 1 GB = 1,000 MB = 8,000 megabits.",
                f"A 5 GB file at 50 Mbps with 90% efficiency takes {hms(5*8e9/(50e6*0.9))}.")
XF = [num("size", "File size", 5), sel("su", "Size unit", [("1", "MB"), ("1e3", "GB"), ("1e6", "TB")], "1e3"), num("speed", "Speed", 50), sel("u", "Speed unit", SPEED_U, "1e6"), num("eff", "Efficiency (%)", 90)]
calc("download-time-calculator", "xfer", "tech", "arrow-down", "Download Time Calculator", "How long a download will take", "Download Time Calculator",
     "Find out how long it will take to download a file at your connection speed.", XF, xfer_body("download", "upload"),
     [("How is download time calculated?", "Divide the file size in bits by the speed in bits per second. This calculator also applies an efficiency factor for overhead."),
      ("Why does the real time differ?", "Server limits, Wi-Fi, congestion and the number of devices sharing your connection can slow the download."),
      ("Does file size use 1,000 or 1,024?", "This calculator uses decimal units (1 GB = 1,000 MB), the same as internet providers.")])
calc("upload-time-calculator", "xfer", "tech", "arrow-up", "Upload Time Calculator", "How long an upload will take", "Upload Time Calculator",
     "Find out how long it will take to upload a file, using your upload speed rather than your download speed.",
     [num("size", "File size", 2), sel("su", "Size unit", [("1", "MB"), ("1e3", "GB"), ("1e6", "TB")], "1e3"), num("speed", "Upload speed", 20), sel("u", "Speed unit", SPEED_U, "1e6"), num("eff", "Efficiency (%)", 90)],
     info("Upload speeds are usually much lower than download speeds, so large uploads such as videos or backups can take a while. Enter your upload speed from a speed test to get a realistic estimate.",
          "Time = file size in bits / (upload speed in bits per second x efficiency).",
          f"A 2 GB video at 20 Mbps upload with 90% efficiency takes {hms(2*8e9/(20e6*0.9))}."),
     [("Why is upload speed lower than download speed?", "Most home plans are asymmetric and give far more bandwidth to downloads than uploads. Fibre plans are often symmetric."),
      ("How do I find my upload speed?", "Run an online speed test and use the upload figure it reports."),
      ("Can I speed up uploads?", "Use a wired connection, pause other uploads and compress the file before sending.")])

# ---- data usage ----
calc("data-usage-calculator", "data", "tech", "pie", "Data Usage Calculator", "Monthly internet data used by streaming, calls and browsing",
     "Data Usage Calculator", "Estimate how many gigabytes you use each month from your daily habits, and choose the right data plan.",
     [num("h1", "Video streaming (hours per day)", 2, step="0.25"), num("g1", "GB per hour of video", 1.5, step="0.1"),
      num("h2", "Video calls (hours per day)", 1, step="0.25"), num("g2", "GB per hour of calls", 0.8, step="0.1"),
      num("h3", "Music streaming (hours per day)", 2, step="0.25"), num("g3", "GB per hour of music", 0.1, step="0.01"),
      num("h4", "Browsing and social media (hours per day)", 2, step="0.25"), num("g4", "GB per hour of browsing", 0.15, step="0.01"),
      num("days", "Days", 30)],
     info("Enter how many hours a day you spend on each activity and how much data each hour uses. The defaults are typical values: HD video uses about 1.5 GB an hour, video calls about 0.8 GB, music about 0.1 GB and browsing about 0.15 GB.",
          "Monthly data = sum of (hours per day x GB per hour) x number of days.",
          f"2 h of video, 1 h of calls, 2 h of music and 2 h of browsing a day use {nf((2*1.5+0.8+2*0.1+2*0.15),2)} GB a day, or {nf((2*1.5+0.8+2*0.1+2*0.15)*30,1)} GB over 30 days."),
     [("How much data does streaming use?", "Standard definition uses about 0.7 GB an hour, HD about 1.5 to 3 GB and 4K about 7 GB."),
      ("How can I use less data?", "Lower the video quality, download content over Wi-Fi and turn off auto-play."),
      ("Are the defaults accurate?", "They are averages. Edit the GB per hour fields if you know your own usage from your phone settings.")])

# ---- storage ----
calc("storage-calculator", "stor", "tech", "bars", "Storage Calculator", "How many photos, songs and videos fit on a drive",
     "Storage Calculator", "Enter the capacity of a drive and see how many photos, songs, videos or files of your own size it can hold.",
     [num("cap", "Drive capacity", 256), sel("cu", "Capacity unit", [("1", "GB"), ("2", "TB")], "1"),
      sel("mode", "Unit system", [("1000", "Decimal (1 GB = 1,000 MB)"), ("1024", "Binary (1 GB = 1,024 MB)")], "1000"), num("custom", "Your own file size (MB)", 10)],
     info("Storage makers use decimal units (1 GB = 1,000 MB), while many operating systems report binary units (1 GiB = 1,024 MiB). That is why a 256 GB drive shows as about 238 GB in Windows. This calculator shows how much fits either way.",
          "Capacity in MB = capacity x (1,000 or 1,024) for GB, and x another 1,000 or 1,024 for TB. Number of files = capacity / file size. Typical sizes: photo 4 MB, song 5 MB, one hour of HD video 3,000 MB.",
          f"A 256 GB drive holds about {nf(256000/4,0)} photos of 4 MB or {nf(256000/3000,0)} hours of HD video in decimal units. In the OS it appears as {nf(256e9/2**30,1)} GB."),
     [("Why does my drive show less space than advertised?", "Manufacturers count 1 GB as 1 billion bytes, while the operating system counts 1 GB as 1,073,741,824 bytes. Some space is also used by the file system."),
      ("How many photos fit in 128 GB?", "About 32,000 photos at 4 MB each."),
      ("Which unit system should I choose?", "Use decimal to match the drive's label. Use binary to match what your computer reports.")])

# ---- number bases ----
calc("binary-to-decimal-converter", "b2d", "tech", "repeat", "Binary to Decimal Converter", "Convert binary numbers to decimal, hex and octal",
     "Binary to Decimal Converter", "Type a binary number and get its decimal, hexadecimal and octal value instantly, with the place values shown.",
     [txt("val", "Binary number", "101101", rows=1, placeholder="Only 0 and 1")],
     info("Binary is base 2: every digit is a 0 or a 1 and each position is worth a power of two. This converter turns any binary number into decimal, hexadecimal and octal.",
          "Decimal = sum of (digit x 2^position), counting positions from 0 on the right.",
          "101101 in binary = 1x32 + 0x16 + 1x8 + 1x4 + 0x2 + 1x1 = 45 in decimal, which is 2D in hexadecimal and 55 in octal."),
     [("How do I convert binary to decimal by hand?", "Write the place values 1, 2, 4, 8, 16... from the right, then add the values where the digit is 1."),
      ("Can I enter spaces?", "Yes. Spaces and underscores are ignored, so 1011 0101 works."),
      ("Does it handle large numbers?", "Yes. Very long binary numbers are converted exactly.")])
calc("decimal-to-binary-converter", "d2b", "tech", "repeat", "Decimal to Binary Converter", "Convert decimal numbers to binary, hex and octal",
     "Decimal to Binary Converter", "Enter a whole number and see it in binary, hexadecimal and octal, with the division steps for smaller numbers.",
     [txt("val", "Decimal number", "45", rows=1, placeholder="Whole number")],
     info("To write a decimal number in binary, repeatedly divide by 2 and record the remainders. Reading them from last to first gives the binary number. This converter does it instantly and shows the steps.",
          "Divide the number by 2, note the remainder, and repeat with the quotient until it reaches 0. The remainders read in reverse order form the binary value.",
          "45 / 2 = 22 r1, 22 / 2 = 11 r0, 11 / 2 = 5 r1, 5 / 2 = 2 r1, 2 / 2 = 1 r0, 1 / 2 = 0 r1. Reading the remainders backwards gives 101101."),
     [("How many bits do I need for a number?", "A number n needs floor(log2(n)) + 1 bits. For example, 45 needs 6 bits."),
      ("Can I convert negative numbers?", "Yes, a minus sign is kept and the binary result is shown with a minus sign. Two's complement is not used."),
      ("What about decimals like 2.5?", "This tool converts whole numbers only.")])
calc("hexadecimal-converter", "hexc", "tech", "shapes", "Hexadecimal Converter", "Convert between hex, decimal, binary and octal",
     "Hexadecimal Converter", "Convert a number between hexadecimal, decimal, binary and octal by choosing the base you are starting from.",
     [sel("from", "Convert from", [("16", "Hexadecimal"), ("10", "Decimal"), ("2", "Binary"), ("8", "Octal")], "16"), txt("val", "Number", "FF", rows=1)],
     info("Hexadecimal (base 16) uses the digits 0-9 and A-F. It is widely used for colours, memory addresses and byte values because one hex digit is exactly four bits.",
          "Decimal = sum of (digit value x 16^position). Hex digits A to F stand for 10 to 15.",
          "FF in hex = 15x16 + 15 = 255 in decimal = 11111111 in binary = 377 in octal."),
     [("What does 0x mean?", "The prefix 0x marks a hexadecimal number in many programming languages. You can type it or leave it out."),
      ("Is the input case-sensitive?", "No. ff and FF are the same value."),
      ("Why is hex used for colours?", "A colour channel has 256 levels, which is exactly two hex digits, so a colour needs six digits such as #FF8800.")])

# ---- password ----
calc("password-generator", "pw", "tech", "lock", "Password Generator", "Create strong random passwords",
     "Password Generator", "Generate a strong random password with the length and characters you choose. It is created in your browser and never sent anywhere.",
     [num("len", "Length (4 to 128)", 16, step="1", min="4"), chk("up", "Uppercase letters (A-Z)", True), chk("lo", "Lowercase letters (a-z)", True), chk("di", "Numbers (0-9)", True), chk("sy", "Symbols (!@#$...)", True),
      btn("Generate new password")],
     info("This tool builds a random password using your browser's cryptographic random number generator. Nothing is stored or transmitted. Longer passwords with more character types are exponentially harder to guess.",
          "Entropy in bits = length x log2(pool size). With 94 printable characters, a 16-character password has 16 x log2(94), about 105 bits of entropy. Each extra bit doubles the guesses needed.",
          f"A 16-character password using all four types draws from 94 characters and has about {nf(16*math.log2(94),0)} bits of entropy, which is very strong."),
     [("How long should a password be?", "At least 12 characters for normal accounts and 16 or more for email, banking and password managers."),
      ("Is this generator safe?", "Yes. It uses the browser's secure random generator and the password is created on your device only."),
      ("Should I reuse passwords?", "No. Use a different password for every account and store them in a password manager.")])

# ---- text tools ----
SAMPLE = "CalcHub offers free online calculators for everyday use. Type or paste your own text here to see the counts update instantly.\n\nThis second paragraph shows how paragraphs and sentences are counted. Try changing it!"
calc("word-counter", "words", "tech", "book", "Word Counter", "Count words, characters, sentences and paragraphs",
     "Word Counter", "Paste your text to count words, characters, sentences and paragraphs, and see the reading and speaking time.",
     [txt("t", "Your text", SAMPLE, rows=8)],
     info("Type or paste text into the box and the counts update as you type. It is useful for essays, social posts, meta descriptions and any text with a word limit.",
          "Words are groups of characters separated by spaces or line breaks. Sentences end with a full stop, question mark or exclamation mark. Paragraphs are separated by blank lines. Reading time uses 200 words per minute and speaking time 130.",
          "The sample text has 33 words and 2 paragraphs, so it takes about 10 seconds to read."),
     [("How are words counted?", "Any run of characters separated by whitespace counts as one word."),
      ("Is my text saved?", "No. The counting happens in your browser and the text is never uploaded."),
      ("How long does 1,000 words take to read?", "About 5 minutes at 200 words per minute.")])
calc("character-counter", "chars", "tech", "clipboard", "Character Counter", "Count characters with and without spaces",
     "Character Counter", "Count the characters in your text with and without spaces, plus letters, digits, lines and the most common letters.",
     [txt("t", "Your text", "Check the length of your tweet, SMS or meta description here. 160 characters fit in one SMS.", rows=6)],
     info("Character limits are everywhere: SMS messages, tweets, meta descriptions and form fields. Paste your text to see the exact count, with and without spaces.",
          "Characters with spaces counts every character including spaces and line breaks. Characters without spaces ignores all whitespace. Letters and digits are counted separately.",
          "The sample sentence is 90 characters with spaces."),
     [("How many characters fit in a tweet?", "A standard post allows 280 characters."),
      ("What is the ideal meta description length?", "Around 150 to 160 characters so it is not cut off in search results."),
      ("Do emojis count as one character?", "They can count as more than one in some systems, so leave a small safety margin.")])
calc("reading-time-calculator", "read", "tech", "clock", "Reading Time Calculator", "How long a text takes to read",
     "Reading Time Calculator", "Paste your text or enter a word count to find out how long it takes to read silently and aloud.",
     [txt("t", "Your text (optional)", SAMPLE, rows=6), num("wc", "Or enter a word count (0 = use the text)", 0), num("wpm", "Reading speed (words per minute)", 200)],
     info("Average adults read about 200 to 250 words per minute silently and speak at around 130 words per minute. Enter your own reading speed for a personal estimate.",
          "Reading time = words / words per minute. Speaking time = words / 130.",
          "A 1,500-word article takes 7.5 minutes to read at 200 words per minute."),
     [("What is the average reading speed?", "About 200 to 250 words per minute for adults."),
      ("How do blogs show reading time?", "Most divide the word count by 200 or 238 and round to the nearest minute."),
      ("Should I count images?", "Not in this calculator. Add a few seconds for each image if you want to be precise.")])
calc("text-case-converter", "tcase", "tech", "tag", "Text Case Converter", "UPPER, lower, Title, camelCase, snake_case and more",
     "Text Case Converter", "Convert text to uppercase, lowercase, title case, sentence case, camelCase, snake_case and kebab-case in one go.",
     [txt("t", "Your text", "convert this Text to any case style", rows=4)],
     info("Paste any text and get it in every common case style. Each result can be copied with one click, which is handy for headings, code identifiers and URLs.",
          "Title case capitalises the first letter of each word. Sentence case capitalises the first letter of each sentence. camelCase, PascalCase, snake_case, kebab-case and CONSTANT_CASE join the words without spaces.",
          "\"convert this Text\" becomes CONVERT THIS TEXT, Convert This Text, convertThisText and convert_this_text."),
     [("What is camelCase?", "A style where words are joined and each word after the first starts with a capital letter, such as myVariableName."),
      ("When should I use kebab-case?", "It is common for URLs and CSS class names, for example my-page-title."),
      ("Does it change my original text?", "No. The original stays in the box and the converted versions appear below.")])

# ---- images & screens ----
calc("image-size-calculator", "img", "tech", "monitor", "Image Size Calculator", "Megapixels, file size and print size of an image",
     "Image Size Calculator", "Enter the pixel dimensions of an image to get its megapixels, uncompressed size, aspect ratio and print size at your chosen DPI.",
     [num("w", "Width (pixels)", 4000), num("h", "Height (pixels)", 3000), sel("bpp", "Colour depth", [("24", "24-bit colour (RGB)"), ("32", "32-bit colour (RGBA)"), ("8", "8-bit grey")], "24"), num("dpi", "Print resolution (DPI)", 300)],
     info("Pixel dimensions tell you the quality of an image. This calculator converts them into megapixels, the uncompressed memory size, the aspect ratio and the largest print size at a given DPI. Compressed formats such as JPEG are much smaller than the uncompressed size.",
          "Megapixels = width x height / 1,000,000. Uncompressed size = width x height x bits per pixel / 8. Print size in inches = pixels / DPI.",
          f"A 4000 x 3000 photo is 12 megapixels, {nf(4000*3000*3/1e6,1)} MB uncompressed at 24-bit, and prints at {nf(4000/300,1)} x {nf(3000/300,1)} inches at 300 DPI."),
     [("How many megapixels do I need for printing?", "At 300 DPI, an A4 print (8.3 x 11.7 inches) needs about 2,500 x 3,500 pixels, roughly 9 megapixels."),
      ("Why is the real file smaller?", "JPEG and other formats compress the data, usually to a tenth or less of the uncompressed size."),
      ("What DPI should I use?", "300 DPI is standard for quality prints and 72 to 150 is fine for screens.")])
calc("screen-resolution-calculator", "screen", "tech", "monitor", "Screen Resolution Calculator", "Aspect ratio, megapixels and pixel density (PPI)",
     "Screen Resolution Calculator", "Find the aspect ratio, megapixels and pixels per inch of a screen from its resolution and diagonal size.",
     [sel("pre", "Preset", [("custom", "Custom size"), ("1280x720", "HD 1280 x 720"), ("1920x1080", "Full HD 1920 x 1080"), ("2560x1440", "QHD 2560 x 1440"), ("3840x2160", "4K UHD 3840 x 2160"), ("7680x4320", "8K 7680 x 4320")], "1920x1080"),
      num("w", "Width (pixels)", 1920, "pre=custom"), num("h", "Height (pixels)", 1080, "pre=custom"), num("diag", "Screen diagonal (inches)", 24)],
     info("Pixel density (PPI) tells you how sharp a screen looks. Pick a preset or enter your own resolution and screen size to see the aspect ratio, total megapixels, PPI and the physical width and height.",
          "Aspect ratio = width : height reduced by their greatest common divisor. PPI = sqrt(width^2 + height^2) / diagonal. Physical width = diagonal x width / sqrt(width^2 + height^2).",
          f"A 24 inch Full HD screen has {nf(math.hypot(1920,1080)/24,1)} PPI, a 16:9 aspect ratio and {nf(1920*1080/1e6,2)} megapixels."),
     [("What PPI is good?", "Around 100 PPI is comfortable at desktop distance. Phones usually exceed 400 PPI."),
      ("What is 16:9?", "It means the screen is 16 units wide for every 9 units tall. It is the standard for most monitors and TVs."),
      ("Does higher resolution always look sharper?", "Only if the screen is large enough or close enough. PPI combines resolution and size.")])
