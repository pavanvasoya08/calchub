# Ask Us Anything form: Google Sheets + Apps Script setup

Everything below is free. No Formspree, no paid backend. The script has no password, API key or spreadsheet ID in it.

## 1. Create the Google Sheet
1. Go to https://sheets.google.com and create a blank sheet named **CalcHub Questions**.

## 2. Add the script
1. In the sheet: **Extensions > Apps Script**.
2. Delete the default `function myFunction() {}` and paste the full contents of `apps-script/Code.gs`.
3. At the top, check `CFG`:
   - `ALLOWED_URL_PREFIX` must match your site (`https://pavanvasoya08.github.io/calchub/`; change it when you get a custom domain).
   - `NOTIFY_EMAIL`: optional. Put your email to get a mail for every new question, or leave `''`.
4. Click **Save** (disk icon).

## 3. Create the sheet columns (run once)
1. In the function dropdown choose **setup** and click **Run**.
2. Google asks for permission: **Review permissions > choose your account > Advanced > Go to (project name) (unsafe) > Allow**. This warning is normal for your own scripts.
3. A tab named **Questions** appears with these columns: Submission ID, Submission Date, Name, Email, Question Category, Question, Calculator Name, Calculator Page URL, Status. Status has a dropdown (New, In Progress, Answered, Closed).

## 4. Deploy as a Web app
1. **Deploy > New deployment > gear icon > Web app**.
2. Description: `CalcHub form`. **Execute as: Me**. **Who has access: Anyone**.
3. **Deploy**, then copy the **Web app URL** (it ends with `/exec`).
4. Open that URL in a browser. You should see `{"ok":true,"message":"CalcHub form endpoint is running."}`.

## 5. Connect the website
Send me the Web app URL. I put it in `build.py` (`ASK_ENDPOINT`), rebuild and push.
(Or run the build yourself: `CALCHUB_ASK_URL="https://script.google.com/macros/s/XXXX/exec" python3 build.py`.)

## 6. Test
1. Open the EMI Calculator page, fill the form, wait a few seconds, click **Send question**.
2. You should see the green success message and a new row in the **Questions** tab with Status **New**.
3. Send the same question again: it is not saved twice.

## Changing the script later
Edit the code, then **Deploy > Manage deployments > pencil icon > Version: New version > Deploy**. The URL stays the same. (Saving alone does not update the live version.)

## Is it safe?
- The Web app URL is public by design (the website must call it) but it only accepts form data. It cannot read your sheet or Google account.
- The script runs as you, but it only writes rows into this one sheet. Do not share the sheet publicly.
- Protection built in: honeypot field, minimum fill time, per-email limit (3 per hour), global limit, duplicate detection, text-only cells (blocks `=formula` injection), HTML tags stripped, page URL must start with your site address.
- Google Apps Script limits for free accounts apply (about 20,000 URL calls/day for consumer accounts). That is far more than a small site needs.

## Troubleshooting
- "This form is not connected yet": the URL in `build.py` is still the placeholder.
- "The form is not set up yet": run `setup` (step 3).
- No row appears: open Apps Script > **Executions** to see errors. Make sure access is **Anyone** and you deployed a new version after editing.
