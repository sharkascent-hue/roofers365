# Roofers 365

Static website for roofers365.ie. No build step is needed to host it: the HTML in this folder is ready to serve.

- `build.py` regenerates every page, `sitemap.xml` and `robots.txt`. Edit copy there, then run `python3 build.py`.
- `assets/style.css` holds the design, `assets/site.js` the behaviour (menu, scroll animations, forms, gallery).
- Forms are delivered by Web3Forms. Put the access key for the Roofers 365 inbox in `WEB3FORMS_KEY` in `build.py` and rebuild. Until then the form shows a call / WhatsApp fallback.
- Service pages keep the old `/service/<name>/` URLs and county pages keep `/dublin/`, `/kildare/`, `/meath/`, `/louth/`, so existing Google rankings carry over.
