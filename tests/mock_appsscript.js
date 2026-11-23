// Runs the REAL apps-script/Code.gs inside Node with in-memory mocks of SpreadsheetApp/CacheService/LockService/ContentService,
// and exposes it over HTTP the way a deployed Web App behaves (POST /exec -> 302 -> JSON with CORS *).
const vm = require('vm'), fs = require('fs'), http = require('http'), crypto = require('crypto');
const rows = [], cache = {};
const sheet = { getLastRow: () => rows.length + 1, getRange: (r, c, nr, nc) => ({ setNumberFormat() { return this }, setValues(v) { rows.push(v[0]); return this } }) };
const sandbox = {
  console, JSON, Date, Math, Number, String, isFinite,
  SpreadsheetApp: { getActiveSpreadsheet: () => ({ getSheetByName: () => sheet }) },
  CacheService: { getScriptCache: () => ({ get: k => cache[k] || null, put: (k, v) => { cache[k] = v } }) },
  LockService: { getScriptLock: () => ({ tryLock: () => true, releaseLock() {} }) },
  Session: { getScriptTimeZone: () => 'Asia/Kolkata' },
  Utilities: { formatDate: (d, tz, f) => f === 'yyyyMMdd' ? d.toISOString().slice(0, 10).replace(/-/g, '') : d.toISOString().replace('T', ' ').slice(0, 19), getUuid: () => crypto.randomUUID(),
    DigestAlgorithm: { SHA_256: 'sha256' }, computeDigest: (a, s) => Array.from(crypto.createHash('sha256').update(s).digest()).map(b => b > 127 ? b - 256 : b) },
  ContentService: { MimeType: { JSON: 'json' }, createTextOutput: t => ({ t, setMimeType() { return this } }) },
  MailApp: { sendEmail() {} }
};
vm.createContext(sandbox);
vm.runInContext(fs.readFileSync(__dirname + '/../apps-script/Code.gs', 'utf8'), sandbox);
const results = {}; let n = 0;
http.createServer((req, res) => {
  const cors = { 'Access-Control-Allow-Origin': '*' };
  if (req.url.startsWith('/rows')) { res.writeHead(200, { ...cors, 'content-type': 'application/json' }); return res.end(JSON.stringify(rows)); }
  if (req.url.startsWith('/result/')) { res.writeHead(200, { ...cors, 'content-type': 'application/json' }); return res.end(results[req.url.slice(8)]); }
  if (req.method === 'POST') {
    let b = ''; req.on('data', d => b += d); req.on('end', () => {
      setTimeout(() => { const out = sandbox.doPost({ postData: { contents: b } }).t; const id = ++n; results[id] = out;
      res.writeHead(302, process.env.NO_CORS_302 ? { Location: '/result/' + id } : { ...cors, Location: '/result/' + id }); res.end(); }, +process.env.DELAY_MS || 0);
    });
  } else { res.writeHead(200, cors); res.end(sandbox.doGet().t); }
}).listen(+process.argv[2] || 8799, () => console.log('mock up'));
