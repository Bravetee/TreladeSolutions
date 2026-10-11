# Prototype: Trelade Solutions (Static HTML/CSS)

This branch contains a portable static HTML/CSS prototype built from the site's existing branding.

How to preview locally:

```bash
cd prototype
python3 -m http.server 8000
# then open http://localhost:8000 in your browser
```

Notes:
- Uses Google Fonts (`Open Sans`, `Source Sans 3`) for quick prototyping. Replace with self-hosted fonts for IONOS if required.
- Colors and typography were inferred from the live site (see `colors-fonts-report.json` in the repo root).
- Branch: `prototype-static` — open a PR to merge into `main` when ready.
