#!/usr/bin/env python3
"""Draws the Ambiguous Games logo files into brand/ (SVG, lettering as outlines).

The mark: three edges of a cube meeting at a corner plus the far left edge of
the top face, all of length L on true 30-degree lines (the "open corner").
Lettering: Montserrat (SIL OFL) Bold for AMBIGUOUS, Medium for GAMES.

Needs fonttools and uharfbuzz, and the variable Montserrat font:
  python3 tools/make-logo.py path/to/Montserrat[wght].ttf
(https://github.com/google/fonts/tree/main/ofl/montserrat). PNGs: tools/make-pngs.sh.
"""
import math, os, sys
import uharfbuzz as hb
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen

FONT = sys.argv[1]
OUT = os.path.join(os.path.dirname(__file__), '..', 'brand')
C = math.cos(math.pi / 6)

NIGHT, PAPER, GAMES_ON_DARK = '#0F0E14', '#F1F0F6', '#A3A0B2'
INK, GAMES_ON_LIGHT = '#16151C', '#6B6878'

tt = TTFont(FONT)
upem = tt['head'].unitsPerEm
blob = hb.Blob.from_file_path(FONT)
face = hb.Face(blob)

def run(text, wght, fs, track):
    """Shaped glyphs (with kerning) as (glyph name, x) at size fs; and the width without trailing tracking."""
    font = hb.Font(face)
    font.set_variations({'wght': wght})
    buf = hb.Buffer(); buf.add_str(text); buf.guess_segment_properties()
    hb.shape(font, buf, {'kern': True})
    s, x, out = fs / upem, 0.0, []
    order = tt.getGlyphOrder()
    for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
        out.append((order[info.codepoint], x + pos.x_offset * s))
        x += pos.x_advance * s + track
    # Width to the ink's right edge (the last glyph's outline, not its advance).
    gs = tt.getGlyphSet(location={'wght': wght})
    bp = BoundsPen(gs); gs[out[-1][0]].draw(bp)
    return out, out[-1][1] + bp.bounds[2] * s

def outline(glyphs, wght, fs, x0, y0):
    gs = tt.getGlyphSet(location={'wght': wght})
    s, d = fs / upem, []
    for name, x in glyphs:
        pen = SVGPathPen(gs)
        gs[name].draw(TransformPen(pen, (s, 0, 0, -s, x0 + x, y0)))
        d.append(pen.getCommands())
    return ' '.join(d)

def cap(ch, wght, fs):
    gs = tt.getGlyphSet(location={'wght': wght})
    bp = BoundsPen(gs); gs[tt.getBestCmap()[ord(ch)]].draw(bp)
    return bp.bounds[3] * fs / upem

def typeset(fs):
    t1, gfs = fs * 0.02, fs * 0.47
    t2 = gfs * 0.72
    capA, capG = cap('A', 700, fs), cap('G', 500, gfs)
    g1, w1 = run('AMBIGUOUS', 700, fs, t1)
    g2, w2 = run('GAMES', 500, gfs, t2)
    b1 = capA
    b2 = b1 + capA * 0.55 + capG
    return dict(fs=fs, gfs=gfs, capA=capA, g1=g1, w1=w1, g2=g2, w2=w2, b1=b1, b2=b2, H=b2)

def mark_d(L, x, y):
    p = lambda dx, dy: f'{x + dx * L:.2f} {y + dy * L:.2f}'
    return f'M{p(C, -0.5)} L{p(0, 0)} L{p(-C, -0.5)} L{p(0, -1)} M{p(0, 0)} L{p(0, 1)}'

def silver(L, x, y):
    return (f'<linearGradient id="silver" gradientUnits="userSpaceOnUse" x1="{x - C * L:.2f}" y1="{y - L:.2f}" x2="{x + C * L:.2f}" y2="{y + L:.2f}">'
            '<stop offset="0" stop-color="#FFFFFF"/><stop offset="0.48" stop-color="#B4B0C4"/>'
            '<stop offset="0.7" stop-color="#EFEDF6"/><stop offset="1" stop-color="#8C88A0"/></linearGradient>')

def mark_el(L, x, y, sw, colour):
    defs = ''
    if colour == 'silver':
        defs, colour = silver(L, x, y), 'url(#silver)'
    return defs, (f'<path d="{mark_d(L, x, y)}" fill="none" stroke="{colour}" stroke-width="{sw:.2f}" '
                  'stroke-linecap="round" stroke-linejoin="round"/>')

def svg(w, h, defs, body, title, bg=None, x0=0, y0=0, pad=0):
    # A little room round the ink so overshoots and anti-aliasing never clip.
    x0, y0, w, h = x0 - pad, y0 - pad, w + 2 * pad, h + 2 * pad
    rect = f'<rect x="{x0}" y="{y0}" width="{w:.2f}" height="{h:.2f}" fill="{bg}"/>' if bg else ''
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x0:.2f} {y0:.2f} {w:.2f} {h:.2f}" width="{w:.0f}" height="{h:.0f}" role="img" aria-label="{title}">'
            f'<title>{title}</title>' + (f'<defs>{defs}</defs>' if defs else '') + rect + body + '</svg>\n')

def primary(markc, word, games, fs=100):
    T = typeset(fs)
    L = T['H'] * 0.8
    sw = L / 11
    cx, cy = C * L + sw / 2, T['H'] / 2
    tx = cx + C * L + sw / 2 + T['capA'] * 0.62
    top, bot = cy - L - sw / 2, cy + L + sw / 2
    W = tx + max(T['w1'], T['w2'])
    defs, m = mark_el(L, cx, cy, sw, markc)
    body = (m + f'<path d="{outline(T["g1"], 700, fs, tx, T["b1"])}" fill="{word}"/>'
              + f'<path d="{outline(T["g2"], 500, T["gfs"], tx, T["b2"])}" fill="{games}"/>')
    return svg(W, bot - top, defs, body, 'Ambiguous Games', y0=top, pad=T['H'] * 0.05)

def stacked(markc, word, games, fs=100):
    T = typeset(fs)
    W = max(T['w1'], T['w2'])
    L = T['H'] * 0.62
    sw = L / 11
    cx, cy = W / 2, L + sw / 2
    ty = cy + L + sw / 2 + T['capA'] * 0.9
    defs, m = mark_el(L, cx, cy, sw, markc)
    body = (m + f'<path d="{outline(T["g1"], 700, fs, (W - T["w1"]) / 2, ty + T["b1"])}" fill="{word}"/>'
              + f'<path d="{outline(T["g2"], 500, T["gfs"], (W - T["w2"]) / 2, ty + T["b2"])}" fill="{games}"/>')
    return svg(W, ty + T['H'], defs, body, 'Ambiguous Games', pad=T['H'] * 0.05)

def mark_only(markc, sw_ratio=11, size=100, pad=0.0, bg=None, L_ratio=None):
    L = (L_ratio or 0.5) * size if L_ratio else None
    if L is None:
        # Tight: the mark's own box (2L tall, 2cL wide) plus half a stroke all round.
        L = 100; sw = L / sw_ratio
        w, h = 2 * C * L + sw, 2 * L + sw
        defs, m = mark_el(L, w / 2, h / 2, sw, markc)
        return svg(w, h, defs, m, 'Ambiguous Games', pad=sw)
    sw = L / sw_ratio
    defs, m = mark_el(L, size / 2, size / 2, sw, markc)
    return svg(size, size, defs, m, 'Ambiguous Games', bg=bg)

def write(name, text):
    with open(os.path.join(OUT, name), 'w') as f: f.write(text)

os.makedirs(OUT, exist_ok=True)
write('logo-silver.svg', primary('silver', PAPER, GAMES_ON_DARK))
write('logo-on-dark.svg', primary(PAPER, PAPER, GAMES_ON_DARK))
write('logo-on-light.svg', primary(INK, INK, GAMES_ON_LIGHT))
write('logo-black.svg', primary('#000000', '#000000', '#000000'))
write('logo-white.svg', primary('#FFFFFF', '#FFFFFF', '#FFFFFF'))
write('stacked-silver.svg', stacked('silver', PAPER, GAMES_ON_DARK))
write('stacked-on-light.svg', stacked(INK, INK, GAMES_ON_LIGHT))
write('mark-silver.svg', mark_only('silver'))
write('mark-on-dark.svg', mark_only(PAPER))
write('mark-on-light.svg', mark_only(INK))
# App icon: full square (iOS rounds the corners itself); mark is 25% of the side per edge.
write('app-icon.svg', mark_only('silver', size=1024, bg=NIGHT, L_ratio=0.25))
# Favicon: heavier stroke so it reads at 16 px; follows the browser's light or dark tab.
fav = mark_only(INK, sw_ratio=5.5, size=100, L_ratio=0.42)
fav = fav.replace(f'stroke="{INK}"', 'class="m" stroke="#16151C"').replace(
    '<title>', f'<style>@media (prefers-color-scheme: dark) {{ .m {{ stroke: {PAPER}; }} }}</style><title>')
write('favicon.svg', fav)
# Favicon tile (PNG fallbacks): the paper mark on a night rounded square, readable on any tab.
L = 30; tile = mark_only(PAPER, sw_ratio=4.5, size=100, L_ratio=0.3)
write('favicon-tile.svg', tile.replace('<path', '<rect width="100" height="100" rx="22" fill="%s"/><path' % NIGHT, 1))
print('wrote', sorted(os.listdir(OUT)))
