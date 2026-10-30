# ambiguous.com

The Ambiguous Games website: plain HTML and one stylesheet, no build step.
Served by GitHub Pages from `main` (custom domain in `CNAME`).

- `index.html`: the studio and the three games.
- `herdwise/`, `deepwell/`, `zenolith/`: a page per game (App Store marketing URLs).
- `support/`: the support URL for every app. `privacy/`: the privacy policy URL for every app.
  Update the privacy policy, and its date, before shipping ads, purchases,
  Game Center or iCloud.
- `brand/`: the logo files (see brand/README.md); `tools/` draws them.
- `img/`: icons and screenshots (simulator, iPhone 17 Pro, JPEG, 1200 px tall).

Preview: `python3 -m http.server` here, then open http://localhost:8000.
