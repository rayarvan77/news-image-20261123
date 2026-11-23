#!/usr/bin/env python3
"""Draw the 23 November 2026 world-news broadsheet poster.

A single 1024x1024 PNG, painted with Pillow primitives only: no photos,
no network, no randomness, so the output bytes are fully deterministic.
Run:  python3 draw_poster.py [output-path]
"""
import sys

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = sys.argv[1] if len(sys.argv) > 1 else "entry.png"

PAPER = (245, 239, 227)
INK = (26, 26, 26)
NAVY = (22, 35, 63)
NAVY_DARK = (16, 25, 45)
RED = (179, 39, 30)
TILE_BG = (255, 253, 247)
TILE_EDGE = (216, 208, 190)
GREY = (90, 90, 86)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_BOOK = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def fit_lines(draw, text, path, start_size, max_w, max_lines, min_size=14):
    """Shrink the font until the wrapped text fits width and line count."""
    size = start_size
    while size > min_size:
        fnt = font(path, size)
        lines = wrap(draw, text, fnt, max_w)
        if len(lines) <= max_lines and all(
            draw.textlength(ln, font=fnt) <= max_w for ln in lines
        ):
            return fnt, lines
        size -= 1
    fnt = font(path, min_size)
    return fnt, wrap(draw, text, fnt, max_w)[:max_lines]


def draw_text_block(draw, lines, fnt, x, y, color, leading):
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=color)
        y += leading
    return y


# ---------------------------------------------------------------- masthead
img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

# double outer frame
d.rectangle([10, 10, W - 11, H - 11], outline=INK, width=3)
d.rectangle([18, 18, W - 19, H - 19], outline=INK, width=1)

# navy masthead band
d.rectangle([24, 24, W - 25, 128], fill=NAVY)
d.rectangle([24, 128, W - 25, 132], fill=RED)
mast = font(SERIF, 62)
title = "THE WORLD TODAY"
tw = d.textlength(title, font=mast)
d.text(((W - tw) / 2, 44), title, font=mast, fill=(255, 255, 255))

# dateline strip with side rules
date_fnt = font(SANS_BOLD, 21)
date = "MONDAY, 23 NOVEMBER 2026"
dw = d.textlength(date, font=date_fnt)
cx = W // 2
d.line([150, 152, cx - dw / 2 - 18, 152], fill=RED, width=3)
d.line([cx + dw / 2 + 18, 152, W - 150, 152], fill=RED, width=3)
d.text((cx - dw / 2, 140), date, font=date_fnt, fill=NAVY)

# ---------------------------------------------------------------- lead art
AX, AY, AW, AH = 24, 170, 552, 386
# dusk sky gradient
top, bottom = (35, 47, 78), (96, 118, 152)
for i in range(AH):
    t = i / max(AH - 1, 1)
    col = tuple(int(top[c] + (bottom[c] - top[c]) * t) for c in range(3))
    d.line([(AX, AY + i), (AX + AW - 1, AY + i)], fill=col)
d.rectangle([AX, AY, AX + AW - 1, AY + AH - 1], outline=INK, width=2)

art = Image.new("RGBA", (AW, AH), (0, 0, 0, 0))
a = ImageDraw.Draw(art)

# far skyline
for bx, bw, bh in [(18, 52, 66), (84, 40, 88), (138, 60, 58), (470, 64, 74)]:
    a.rectangle([bx, AH - 118 - bh, bx + bw, AH - 118], fill=(26, 36, 56, 255))

# standing part of the five-storey block
BX, BY, BW, BH = 78, 150, 218, 178
a.rectangle([BX, BY, BX + BW, BY + BH], fill=(122, 130, 142, 255))
a.rectangle([BX, BY, BX + BW, BY + 12], fill=(94, 100, 112, 255))
for r in range(5):
    for c in range(5):
        wx, wy = BX + 14 + c * 40, BY + 24 + r * 30
        lit = (r + c) % 4 == 0
        a.rectangle([wx, wy, wx + 22, wy + 16],
                    fill=(232, 190, 90, 255) if lit else (52, 58, 70, 255))
# collapsed wing: jagged broken slabs leaning right
a.polygon([(BX + BW, BY + 40), (BX + BW + 118, BY + 96), (BX + BW + 96, BY + 190),
           (BX + BW + 30, BY + 150)], fill=(150, 158, 168, 255))
a.polygon([(BX + BW + 40, BY + 150), (BX + BW + 150, BY + 210),
           (BX + BW + 120, BY + 262), (BX + BW + 10, BY + 210)],
          fill=(116, 122, 134, 255))
# broken window frames on the fallen slabs
for wx, wy in [(BX + BW + 52, BY + 96), (BX + BW + 84, BY + 128),
               (BX + BW + 66, BY + 178)]:
    a.rectangle([wx, wy, wx + 18, wy + 12], fill=(52, 58, 70, 255))
# rubble mound
for (px, py, s, col) in [(300, 300, 52, (74, 79, 87)), (340, 312, 64, (96, 102, 112)),
                         (392, 306, 58, (60, 65, 74)), (440, 318, 44, (122, 130, 142)),
                         (318, 326, 40, (52, 57, 66))]:
    a.polygon([(px - s, py + 18), (px, py - s // 2), (px + s, py + 18)], fill=col + (255,))
# rescue crane, far right
a.rectangle([500, 96, 512, 330], fill=(20, 24, 31, 255))
a.polygon([(506, 96), (512, 108), (388, 128), (388, 116)], fill=(20, 24, 31, 255))
a.line([(400, 122), (400, 210)], fill=(20, 24, 31, 255), width=3)
a.rectangle([392, 210, 410, 226], fill=(224, 120, 48, 255))
# searchlight beams
a.polygon([(150, 330), (96, 130), (128, 130)], fill=(255, 255, 240, 46))
a.polygon([(330, 330), (300, 150), (330, 150)], fill=(255, 255, 240, 36))
# smoke wisps
for (sx, sy, rx, ry) in [(330, 96, 46, 16), (362, 74, 58, 18), (396, 52, 44, 14)]:
    a.ellipse([sx - rx, sy - ry, sx + rx, sy + ry], fill=(200, 205, 212, 90))
# ground
a.rectangle([0, AH - 56, AW, AH], fill=(24, 28, 38, 255))
# three rescuers in orange helmets, standing on the ground line (y = AH-56)
for fx in (286, 316, 348):
    a.ellipse([fx - 6, AH - 90, fx + 6, AH - 78], fill=(224, 120, 48, 255))
    a.rectangle([fx - 5, AH - 78, fx + 5, AH - 64], fill=(224, 120, 48, 255))
    a.rectangle([fx - 5, AH - 64, fx - 2, AH - 56], fill=(30, 30, 30, 255))
    a.rectangle([fx + 2, AH - 64, fx + 5, AH - 56], fill=(30, 30, 30, 255))
img.paste(Image.alpha_composite(Image.new("RGBA", (AW, AH), (0, 0, 0, 0)), art),
          (AX, AY), art)

# caption bar over the foot of the art panel
d.rectangle([AX, AY + AH - 34, AX + AW - 1, AY + AH - 1], fill=(16, 20, 28))
cap = font(SANS_BOLD, 14)
d.text((AX + 12, AY + AH - 27),
       "DYMER, KYIV REGION — RESCUERS DIG THROUGH THE RUBBLE",
       font=cap, fill=(255, 255, 255))

# ---------------------------------------------------------------- lead text
TX, TW = 600, 400
y = 176
kick = font(SANS_BOLD, 17)
d.text((TX, y), "UKRAINE  •  WAR IN EUROPE", font=kick, fill=RED)
y += 30
d.line([(TX, y), (TX + 64, y)], fill=RED, width=4)
y += 16
head_fnt, head_lines = fit_lines(d, "AT LEAST 15 KILLED IN KYIV REGION STRIKES",
                                 SERIF, 42, TW, 3)
y = draw_text_block(d, head_lines, head_fnt, TX, y, INK, 50)
y += 8
deck_fnt, deck_lines = fit_lines(
    d,
    "A Russian drone strike brought down part of a five-storey block of flats "
    "in Dymer, north of Kyiv. Rescuers dug through the rubble for survivors — "
    "a supermarket strike in Vyshneve and a hit on a home in Bila Tserkva "
    "added to the toll.",
    SANS, 19, TW, 6)
y = draw_text_block(d, deck_lines, deck_fnt, TX, y, (58, 58, 54), 26)
y += 12
stat = font(SANS_BOLD, 15)
stat_text = "11 IN DYMER  •  3 IN VYSHNEVE  •  1 IN BILA TSERKVA"
while stat.size > 11 and d.textlength(stat_text, font=stat) > TW:
    stat = font(SANS_BOLD, stat.size - 1)
d.text((TX, y), stat_text, font=stat, fill=RED)

# divider between lead and grid
d.line([24, 566, W - 25, 566], fill=INK, width=2)

# ---------------------------------------------------------------- tiles
def icon_globe(dr, x, y, s):
    dr.ellipse([x, y, x + s, y + s], outline=(255, 255, 255), width=3)
    dr.ellipse([x + s * 0.28, y + s * 0.08, x + s * 0.72, y + s * 0.92],
               outline=(255, 255, 255), width=2)
    dr.line([(x, y + s / 2), (x + s, y + s / 2)], fill=(255, 255, 255), width=2)
    dr.line([(x + s * 0.62, y + s * 0.1), (x + s * 0.45, y + s * 0.45),
             (x + s * 0.66, y + s * 0.62), (x + s * 0.5, y + s * 0.95)],
            fill=(255, 255, 255), width=2)


def icon_ship(dr, x, y, s):
    dr.polygon([(x, y + s * 0.55), (x + s, y + s * 0.55), (x + s * 0.82, y + s * 0.9),
                (x + s * 0.18, y + s * 0.9)], fill=(255, 255, 255))
    dr.line([(x + s * 0.2, y + s * 0.55), (x + s * 0.2, y + s * 0.12)],
            fill=(255, 255, 255), width=3)
    dr.line([(x + s * 0.2, y + s * 0.14), (x + s * 0.62, y + s * 0.34),
             (x + s * 0.2, y + s * 0.38)], fill=(255, 255, 255), width=2)
    for wy in (y + s * 0.97,):
        dr.arc([x, wy - 4, x + s * 0.4, wy + 4], 0, 180, fill=(255, 255, 255), width=2)


def icon_chart(dr, x, y, s):
    dr.line([(x, y + s * 0.25), (x + s * 0.35, y + s * 0.45),
             (x + s * 0.55, y + s * 0.3), (x + s * 0.9, y + s * 0.8)],
            fill=(255, 255, 255), width=3)
    dr.polygon([(x + s * 0.9, y + s * 0.8), (x + s * 0.62, y + s * 0.72),
                (x + s * 0.82, y + s * 0.52)], fill=(255, 255, 255))


def icon_cuffs(dr, x, y, s):
    dr.ellipse([x, y + s * 0.3, x + s * 0.42, y + s * 0.72],
               outline=(255, 255, 255), width=3)
    dr.ellipse([x + s * 0.58, y + s * 0.3, x + s, y + s * 0.72],
               outline=(255, 255, 255), width=3)
    dr.line([(x + s * 0.42, y + s * 0.5), (x + s * 0.58, y + s * 0.5)],
            fill=(255, 255, 255), width=3)


def icon_ball(dr, x, y, s):
    dr.ellipse([x, y, x + s, y + s], outline=(255, 255, 255), width=3)
    dr.arc([x - s * 0.3, y + s * 0.12, x + s * 0.5, y + s * 0.88], -70, 70,
           fill=(255, 255, 255), width=2)
    dr.arc([x + s * 0.5, y + s * 0.12, x + s * 1.3, y + s * 0.88], 110, 250,
           fill=(255, 255, 255), width=2)


def icon_trade(dr, x, y, s):
    dr.line([(x, y + s * 0.3), (x + s * 0.8, y + s * 0.3)], fill=(255, 255, 255), width=3)
    dr.polygon([(x + s * 0.8, y + s * 0.3), (x + s * 0.6, y + s * 0.16),
                (x + s * 0.6, y + s * 0.44)], fill=(255, 255, 255))
    dr.line([(x + s * 0.2, y + s * 0.7), (x + s, y + s * 0.7)],
            fill=(255, 255, 255), width=3)
    dr.polygon([(x + s * 0.2, y + s * 0.7), (x + s * 0.4, y + s * 0.56),
                (x + s * 0.4, y + s * 0.84)], fill=(255, 255, 255))


TILES = [
    ("CLIMATE", (15, 118, 110), icon_globe,
     "COP31 COLLAPSES WITH NO DEAL",
     "The longest UN climate summit ends in Antalya after a fossil-fuel rift "
     "splits nearly 200 nations."),
    ("LIBYA", (30, 58, 95), icon_ship,
     "UKRAINE SINKS RUSSIAN WARSHIP",
     "Sea drones sink the corvette Merkury in Benghazi port and hit a cargo "
     "ship, 2,400 km from the front."),
    ("MARKETS", (179, 39, 30), icon_chart,
     "ASIAN STOCKS SLIDE ON AI FEARS",
     "Nikkei falls 5% and Kospi slides as doubts over the AI boom spread; "
     "Bitcoin steadies off a two-year low."),
    ("MEXICO", (138, 90, 0), icon_cuffs,
     "MORE ARRESTS AFTER CARTEL BOSS HELD",
     "Follow-up raids in Sinaloa after the capture of Fausto Isidro Meza "
     "Flores, known as \u201cEl Chapo Isidro\u201d."),
    ("SPORT", (47, 107, 47), icon_ball,
     "ALCARAZ WINS FIRST ATP FINALS",
     "Carlos Alcaraz beats world No. 1 Alexander Zverev 6\u20132, 7\u20136 "
     "in the final in Turin."),
    ("TRADE", (91, 74, 138), icon_trade,
     "EU AND INDONESIA SIGN TRADE DEAL",
     "A decade in the making, the pact scraps most tariffs \u2014 98.5% "
     "on EU goods."),
]

GX, GY, GAP = 24, 578, 16
CW = (W - 2 * GX - 2 * GAP) // 3
CH = 182
for i, (tag, color, icon, headline, deck) in enumerate(TILES):
    tx = GX + (i % 3) * (CW + GAP)
    ty = GY + (i // 3) * (CH + GAP)
    d.rectangle([tx, ty, tx + CW - 1, ty + CH - 1], fill=TILE_BG, outline=TILE_EDGE, width=1)
    d.rectangle([tx, ty, tx + CW - 1, ty + 30], fill=color)
    tag_fnt = font(SANS_BOLD, 15)
    d.text((tx + 12, ty + 7), tag, font=tag_fnt, fill=(255, 255, 255))
    icon(d, tx + CW - 34, ty + 4, 24)
    hy = ty + 42
    h_fnt, h_lines = fit_lines(d, headline, SANS_BOLD, 20, CW - 24, 2)
    hy = draw_text_block(d, h_lines, h_fnt, tx + 12, hy, INK, 24)
    hy += 4
    deck_fnt2, deck_lines2 = fit_lines(d, deck, SANS, 15, CW - 24, 3)
    draw_text_block(d, deck_lines2, deck_fnt2, tx + 12, hy, GREY, 20)

# ---------------------------------------------------------------- footer
foot = font(SANS, 14)
msg = "Every story above was reported on Monday, 23 November 2026  •  Drawn entirely in code — no photographs"
fw = d.textlength(msg, font=foot)
d.text(((W - fw) / 2, 972), msg, font=foot, fill=GREY)

img.save(OUT, format="PNG", optimize=True, compress_level=9)
print("wrote", OUT)
