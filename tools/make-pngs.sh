#!/bin/sh
# PNGs of the logo files, rendered by a headless Chromium browser (Brave here;
# set BROWSER to another). Run after tools/make-logo.py.
set -e
cd "$(dirname "$0")/../brand"
BROWSER=${BROWSER:-"/Applications/Brave Browser.app/Contents/MacOS/Brave Browser"}
TMP="$PWD/../.render"; mkdir -p "$TMP"
png() { # svg, out, width, height
  printf '<html><body style="margin:0;background:transparent"><img src="%s" style="display:block;width:%spx;height:%spx"></body></html>' "$PWD/$1" "$3" "$4" > "$TMP/p.html"
  perl -e 'alarm 60; exec @ARGV' "$BROWSER" --headless=new --disable-gpu --hide-scrollbars --force-device-scale-factor=1 \
    --no-first-run --no-default-browser-check --default-background-color=00000000 --user-data-dir="$TMP/profile" --window-size="$3,$4" \
    --screenshot="$PWD/$2" "file://$TMP/p.html" >/dev/null 2>&1
  echo "$2"
}
# (A new browser profile's first launch can hang; warm it up once.)
perl -e 'alarm 20; exec @ARGV' "$BROWSER" --headless=new --no-first-run --user-data-dir="$TMP/profile" about:blank >/dev/null 2>&1 || true
size() { sed -E 's/.* width="([0-9]+)" height="([0-9]+)".*/\1 \2/;q' "$1"; }
scaled() { # svg, out, width
  set -- "$1" "$2" "$3" $(size "$1"); png "$1" "$2" "$3" $(( $3 * $5 / $4 ))
}
scaled logo-silver.svg logo-silver.png 2400
scaled logo-on-dark.svg logo-on-dark.png 2400
scaled logo-on-light.svg logo-on-light.png 2400
scaled stacked-silver.svg stacked-silver.png 1200
scaled stacked-on-light.svg stacked-on-light.png 1200
scaled mark-silver.svg mark-silver.png 800
png app-icon.svg app-icon-1024.png 1024 1024
png app-icon.svg apple-touch-icon.png 180 180
png favicon-tile.svg favicon-32.png 32 32
png favicon-tile.svg favicon-192.png 192 192
rm -f "$TMP/p.html"
