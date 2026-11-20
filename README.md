# CalcHub

Free online calculators website: 45 calculators (loans & investments, tax & business, health, math & everyday, unit converters). Pure static HTML/CSS/JS. No server or database needed.

## Structure

- `site/` – the ready-to-deploy website (upload or point your host here)
- `build.py` – generates `site/` from the files below
- `content.py` – **settings and all calculator content** (domain, email, currency, fields, text, FAQs)
- `assets_js.py` – calculator logic
- `assets_css.py` – styles
- `icons.py` – SVG icon set

## Before you go live

1. Open `content.py` and set `DOMAIN`, `CONTACT_EMAIL`, and (optionally) `CUR` / `LOCALE`.
2. Run `python3 build.py` to regenerate `site/` (no dependencies needed).
3. Deploy the `site/` folder (Cloudflare Pages, Netlify or GitHub Pages).
4. Submit `https://yourdomain.com/sitemap.xml` in Google Search Console.
5. After AdSense approval, set `ADSENSE_CLIENT` and `AD_SLOT` in `build.py` and rebuild.

## Add a new calculator

1. Add a `calc(...)` block in `content.py` (fields, explanation, FAQs).
2. Add its logic as `C.<name>` in `assets_js.py`.
3. Add an icon mapping in `icons.py`, then rebuild.
