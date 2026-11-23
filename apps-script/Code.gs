/**
 * CalcHub "Ask Us Anything" form -> Google Sheets
 * Container-bound script: create it from the Google Sheet (Extensions > Apps Script).
 * No spreadsheet ID, password or API key is stored here.
 * Deploy as Web app: Execute as = Me, Who has access = Anyone.
 */
var CFG = {
  SHEET_NAME: 'Questions',
  ALLOWED_URL_PREFIX: 'https://pavanvasoya08.github.io/calchub/',  // change when you get a custom domain
  NOTIFY_EMAIL: '',               // optional: your email to get a notification for each question. Leave '' to disable.
  MIN_SECONDS: 4,                 // forms submitted faster than this are treated as bots
  MAX_PER_EMAIL_PER_HOUR: 3,
  MAX_PER_MINUTE_ALL: 30,
  DUPLICATE_WINDOW_SEC: 600,      // same email + same question within 10 minutes = duplicate
  CATEGORIES: ['Calculation help', 'Formula or result question', 'Report a problem', 'Suggest a new calculator', 'Other']
};
var HEADERS = ['Submission ID', 'Submission Date', 'Name', 'Email', 'Question Category', 'Question',
               'Calculator Name', 'Calculator Page URL', 'Status'];
var STATUSES = ['New', 'In Progress', 'Answered', 'Closed'];

/** Run this ONCE from the editor (Run > setup) to create the sheet, headers and Status dropdown. */
function setup() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var sh = ss.getSheetByName(CFG.SHEET_NAME) || ss.insertSheet(CFG.SHEET_NAME);
  sh.getRange(1, 1, 1, HEADERS.length).setValues([HEADERS]).setFontWeight('bold').setBackground('#e7f0e9');
  sh.setFrozenRows(1);
  sh.getRange(2, 1, sh.getMaxRows() - 1, HEADERS.length).setNumberFormat('@');   // plain text: stops formula injection
  sh.getRange(2, 9, sh.getMaxRows() - 1, 1).setDataValidation(
    SpreadsheetApp.newDataValidation().requireValueInList(STATUSES, true).setAllowInvalid(false).build());
  sh.setColumnWidths(1, 2, 150); sh.setColumnWidth(6, 420); sh.setColumnWidth(8, 300);
  return 'Sheet "' + CFG.SHEET_NAME + '" is ready.';
}

function doGet() { return json_({ ok: true, message: 'CalcHub form endpoint is running.' }); }

function doPost(e) {
  var lock = LockService.getScriptLock();
  try {
    var raw = e && e.postData && e.postData.contents;
    if (!raw || raw.length > 10000) return json_({ ok: false, error: 'Invalid request.' });
    var d;
    try { d = JSON.parse(raw); } catch (x) { return json_({ ok: false, error: 'Invalid request.' }); }
    if (!d || typeof d !== 'object') return json_({ ok: false, error: 'Invalid request.' });

    // --- spam checks: honeypot + too-fast submission. Bots get a normal "success" reply and nothing is stored.
    if (d.website) return json_({ ok: true, message: 'Thank you! Your question has been received.' });
    var elapsed = Number(d.elapsed);
    if (!isFinite(elapsed) || elapsed < CFG.MIN_SECONDS) return json_({ ok: false, error: 'Please take a moment to review your question and submit again.' });

    // --- validate + sanitise
    var name = clean_(d.name, 80, true), email = clean_(d.email, 254, true).toLowerCase();
    var category = clean_(d.category, 60, true), question = clean_(d.question, 1000, false);
    var calcName = clean_(d.calculator, 100, true), pageUrl = clean_(d.url, 300, true);
    var token = clean_(d.token, 64, true);
    var errors = [];
    if (name.length < 2) errors.push('Please enter your name.');
    if (!/^[^\s@<>()\[\]\\,;:"]+@[^\s@<>()\[\]\\,;:"]+\.[A-Za-z]{2,}$/.test(email)) errors.push('Please enter a valid email address.');
    if (CFG.CATEGORIES.indexOf(category) < 0) errors.push('Please choose a question category.');
    if (question.length < 10) errors.push('Please write your question (at least 10 characters).');
    if (pageUrl.indexOf(CFG.ALLOWED_URL_PREFIX) !== 0) errors.push('Invalid page.');
    if (!calcName) errors.push('Invalid page.');
    if (!/^[A-Za-z0-9-]{8,64}$/.test(token)) errors.push('Invalid request.');
    if (errors.length) return json_({ ok: false, error: errors[0] });

    if (!lock.tryLock(15000)) return json_({ ok: false, error: 'The server is busy. Please try again in a moment.' });
    var cache = CacheService.getScriptCache();

    // --- duplicate protection (same submit token, or same email + same question within the window)
    var qKey = 'q_' + hash_(email + '|' + question.toLowerCase());
    if (cache.get('t_' + token) || cache.get(qKey)) return json_({ ok: true, duplicate: true, message: 'Thank you! Your question was already received.' });

    // --- rate limits
    var eKey = 'e_' + hash_(email), eCount = Number(cache.get(eKey) || 0);
    if (eCount >= CFG.MAX_PER_EMAIL_PER_HOUR) return json_({ ok: false, error: 'You have sent several questions recently. Please try again later.' });
    var mKey = 'm_' + Math.floor(Date.now() / 60000), mCount = Number(cache.get(mKey) || 0);
    if (mCount >= CFG.MAX_PER_MINUTE_ALL) return json_({ ok: false, error: 'Too many requests right now. Please try again shortly.' });

    // --- store
    var sh = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(CFG.SHEET_NAME);
    if (!sh) return json_({ ok: false, error: 'The form is not set up yet.' });
    var now = new Date();
    var id = 'Q-' + Utilities.formatDate(now, Session.getScriptTimeZone(), 'yyyyMMdd') + '-' + Utilities.getUuid().replace(/-/g, '').slice(0, 6).toUpperCase();
    var row = [id, Utilities.formatDate(now, Session.getScriptTimeZone(), 'yyyy-MM-dd HH:mm:ss'), name, email, category, question, calcName, pageUrl, 'New'];
    var r = sh.getLastRow() + 1;
    sh.getRange(r, 1, 1, row.length).setNumberFormat('@').setValues([row]);
    cache.put('t_' + token, '1', 21600);
    cache.put(qKey, '1', CFG.DUPLICATE_WINDOW_SEC);
    cache.put(eKey, String(eCount + 1), 3600);
    cache.put(mKey, String(mCount + 1), 120);

    if (CFG.NOTIFY_EMAIL) {
      try { MailApp.sendEmail(CFG.NOTIFY_EMAIL, 'New CalcHub question ' + id, calcName + '\n' + pageUrl + '\n\n' + name + ' <' + email + '>\n' + category + '\n\n' + question); } catch (m) {}
    }
    return json_({ ok: true, id: id, message: 'Thank you! Your question has been received.' });
  } catch (err) {
    return json_({ ok: false, error: 'Something went wrong. Please try again later.' });
  } finally {
    try { lock.releaseLock(); } catch (x) {}
  }
}

function clean_(v, max, singleLine) {
  var s = String(v == null ? '' : v);
  s = s.replace(/[\u0000-\u0008\u000B\u000C\u000E-\u001F\u007F]/g, '');      // control characters
  s = s.replace(/<[^>]*>/g, '');                                           // html tags
  s = singleLine ? s.replace(/\s+/g, ' ') : s.replace(/[ \t]+/g, ' ').replace(/\n{3,}/g, '\n\n');
  return s.trim().slice(0, max);
}
function hash_(s) {
  return Utilities.computeDigest(Utilities.DigestAlgorithm.SHA_256, s)
    .map(function (b) { return ('0' + (b & 0xff).toString(16)).slice(-2); }).join('').slice(0, 32);
}
function json_(o) { return ContentService.createTextOutput(JSON.stringify(o)).setMimeType(ContentService.MimeType.JSON); }
