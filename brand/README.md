# Ambiguous Games logo

The open corner: three edges of a cube meeting at a corner, plus the far left
edge of the top face, all the same length on true 30° lines. The primary
lockup sets the mark at 1.6 × the height of the name, centred on it.
Lettering is Montserrat (SIL Open Font Licence) Bold and Medium, converted to
outlines, so no font is needed to use these files.

| File | Use |
|---|---|
| `logo-silver` (.svg, .png) | Primary: silver mark, on dark backgrounds |
| `logo-on-dark` / `logo-on-light` | Flat, for dark or light backgrounds |
| `logo-black` / `logo-white` | One colour: print, stamps, embossing |
| `stacked-silver` / `stacked-on-light` | Square spaces: avatars, title pages |
| `mark-silver` / `mark-on-dark` / `mark-on-light` | The mark alone |
| `app-icon.svg`, `app-icon-1024.png` | Square app icon (iOS rounds the corners) |
| `apple-touch-icon.png`, `favicon.svg`, `favicon-tile.svg`, `favicon-32.png`, `favicon-192.png` | Website icons |

Colours: night #0F0E14, paper #F1F0F6, GAMES on dark #A3A0B2, ink #16151C,
GAMES on light #6B6878. Silver runs #FFFFFF → #B4B0C4 → #EFEDF6 → #8C88A0
from the top left to the bottom right of the mark. Keep clear space of at least
half an edge round the logo.

Rebuild: `python3 tools/make-logo.py Montserrat[wght].ttf`, then `tools/make-pngs.sh`.
