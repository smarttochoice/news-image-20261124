#!/usr/bin/env python3
"""Render the entry image: a one-page newspaper front page summing up the
world news of Tuesday 24 November 2026. Every shape is drawn with PIL; every
word is set in DejaVu. Output: entry.png, 1024x1024, under 1 MiB."""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (250, 246, 238)
INK = (24, 24, 24)
NAVY = (16, 42, 84)
CRIMSON = (178, 34, 34)
GOLD = (184, 138, 44)
GREEN = (11, 102, 35)
TEAL = (12, 96, 92)
GREY = (96, 96, 96)
CARD = (255, 255, 255)
CREAM = (238, 231, 216)

FONTS = "/usr/share/fonts/truetype/dejavu/"


def sb(size):
    return ImageFont.truetype(FONTS + "DejaVuSerif-Bold.ttf", size)


def s(size):
    return ImageFont.truetype(FONTS + "DejaVuSerif.ttf", size)


def bb(size):
    return ImageFont.truetype(FONTS + "DejaVuSans-Bold.ttf", size)


def rg(size):
    return ImageFont.truetype(FONTS + "DejaVuSans.ttf", size)


def wrap(d, text, font, width):
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=font) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def block(d, x, y, text, font, width, fill=INK, leading=None):
    step = leading if leading else int(font.size * 1.28)
    for line in wrap(d, text, font, width):
        d.text((x, y), line, font=font, fill=fill)
        y += step
    return y


img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

# ---- masthead -----------------------------------------------------------
d.rectangle([0, 0, W, 104], fill=NAVY)
d.text((512, 8), "THE WORLD IN ONE PAGE", font=sb(48), fill=CARD, anchor="ma")
d.text((512, 62), "TUESDAY  ·  24 NOVEMBER 2026", font=bb(26), fill=GOLD,
       anchor="ma")
d.rectangle([24, 106, W - 24, 110], fill=GOLD)

# ---- hero: Nvidia / Huang ----------------------------------------------
hx, hy, hw, hh = 24, 118, W - 48, 288
d.rectangle([hx, hy, hx + hw, hy + hh], outline=INK, width=3, fill=CARD)
# chip pictogram
cx, cy, cs = 152, 262, 84
d.rectangle([cx - cs, cy - cs, cx + cs, cy + cs], fill=GREEN, outline=INK,
            width=3)
for i in range(5):
    off = -cs + 24 + i * 30
    d.rectangle([cx + off - 4, cy - cs - 16, cx + off + 4, cy - cs], fill=INK)
    d.rectangle([cx + off - 4, cy + cs, cx + off + 4, cy + cs + 16], fill=INK)
    d.rectangle([cx - cs - 16, cy + off - 4, cx - cs, cy + off + 4], fill=INK)
    d.rectangle([cx + cs, cy + off - 4, cx + cs + 16, cy + off + 4], fill=INK)
d.rectangle([cx - 52, cy - 52, cx + 52, cy + 52], outline=CARD, width=3)
d.text((cx, cy - 16), "NVDA", font=bb(30), fill=CARD, anchor="ma")
d.text((cx, cy + 18), "+31%", font=bb(30), fill=(190, 255, 190), anchor="ma")
# hero copy
tx = 320
d.text((tx, hy + 14), "TECH  •  SANTA CLARA", font=bb(21), fill=GREEN)
d.text((tx, hy + 46), "Huang is back —", font=sb(42), fill=INK)
d.text((tx, hy + 96), "Nvidia soars 31%", font=sb(42), fill=INK)
block(d, tx, hy + 162,
      "Nvidia's board unanimously reinstates Jensen Huang as chief "
      "executive after an inquiry. Shares jump more than 30%.",
      s(24), hw - (tx - hx) - 24, leading=31)
d.text((tx, hy + 250), "Biggest one-day gain since 2003.", font=bb(20),
       fill=CRIMSON)

# ---- story grid ----------------------------------------------------------
gx, gy = 24, 420
pw, ph, gap = 304, 244, 14


def card(col, row, strip, kicker, head, summ, icon):
    x = gx + col * (pw + gap)
    y = gy + row * (ph + gap)
    d.rectangle([x, y, x + pw, y + ph], outline=INK, width=2, fill=CARD)
    d.rectangle([x, y, x + pw, y + 8], fill=strip)
    d.text((x + 14, y + 18), kicker, font=bb(16), fill=strip)
    icon(x, y)
    end = block(d, x + 14, y + 96, head, sb(21), pw - 28, leading=26)
    block(d, x + 14, end + 6, summ, rg(16), pw - 28, leading=20)


def icon_globe(x, y):
    gx0, gy0, r = x + 58, y + 66, 26
    d.ellipse([gx0 - r, gy0 - r, gx0 + r, gy0 + r], fill=(66, 130, 182),
              outline=NAVY, width=2)
    d.ellipse([gx0 - 18, gy0 - 20, gx0 + 4, gy0 - 2], fill=(88, 168, 96))
    d.ellipse([gx0 - 2, gy0 + 8, gx0 + 20, gy0 + 22], fill=(88, 168, 96))
    d.line([(gx0 - 22, gy0 - 18), (gx0 - 4, gy0 + 2), (gx0 - 14, gy0 + 18)],
           fill=CRIMSON, width=4)
    d.text((x + 100, y + 52), "0 deal", font=sb(26), fill=CRIMSON)


def icon_flame(x, y):
    fx, fy = x + 52, y + 46
    d.polygon([(fx, fy + 42), (fx + 14, fy + 12), (fx + 26, fy + 26),
               (fx + 38, fy), (fx + 52, fy + 42)], fill=(230, 90, 20),
              outline=INK)
    d.polygon([(fx + 16, fy + 42), (fx + 26, fy + 22), (fx + 36, fy + 42)],
              fill=(255, 200, 40))
    d.rectangle([fx, fy + 42, fx + 52, fy + 48], fill=INK)
    d.text((x + 118, y + 52), "24 dead", font=sb(24), fill=CRIMSON)


def icon_burst(x, y):
    bx, by = x + 58, y + 66
    pts = []
    import math
    for i in range(12):
        ang = i * math.pi / 6
        rad = 30 if i % 2 == 0 else 12
        pts.append((bx + rad * math.cos(ang), by + rad * math.sin(ang)))
    d.polygon(pts, fill=(255, 190, 40), outline=INK)
    d.text((bx, by - 10), "!", font=bb(24), fill=CRIMSON, anchor="ma")
    d.text((x + 104, y + 52), "Kyiv", font=sb(26), fill=INK)


def icon_bars(x, y):
    bx, by = x + 20, y + 46
    heights = [44, 34, 24, 12]
    for i, h in enumerate(heights):
        d.rectangle([bx + i * 24, by + 44 - h, bx + i * 24 + 16, by + 44],
                    fill=CRIMSON if i > 1 else NAVY)
    d.line([(bx - 4, by + 44), (bx + 100, by + 44)], fill=INK, width=2)
    d.text((x + 130, y + 52), "$1 tn", font=sb(26), fill=CRIMSON)


def icon_ball(x, y):
    bx, by, r = x + 58, y + 66, 26
    d.ellipse([bx - r, by - r, bx + r, by + r], fill=(190, 220, 40),
              outline=INK, width=2)
    d.arc([bx - r, by - r, bx + r, by + r], 300, 60, fill=CARD, width=4)
    d.arc([bx - r, by - r, bx + r, by + r], 120, 240, fill=CARD, width=4)
    d.text((x + 100, y + 52), "No. 1", font=sb(24), fill=NAVY)


card(0, 0, TEAL, "CLIMATE  •  TÜRKIYE",
     "COP31 ends with no climate deal",
     "Two weeks of UN talks close divided over fossil fuels — no deal on "
     "phasing them out.", icon_globe)
card(1, 0, CRIMSON, "DISASTER  •  INDONESIA",
     "Factory fire kills at least 24",
     "A candy factory blaze leaves dozens missing as rescuers search the "
     "ruins.", icon_flame)
card(2, 0, NAVY, "WAR  •  UKRAINE",
     "Strikes kill in Kyiv region",
     "Russian drones hit homes near Kyiv; a Russian cargo ship burns off "
     "Finland.", icon_burst)
card(0, 1, (120, 84, 20), "MARKETS  •  USA",
     "Trump blames Democrats for $1 trillion rout",
     "Wall Street tumbles after the midterms; Trump points at the "
     "Democratic win.", icon_bars)
card(1, 1, GREEN, "SPORT  •  TURIN",
     "Alcaraz wins first ATP Finals title",
     "The Spaniard beats Zverev in Turin for his maiden season-ending "
     "crown.", icon_ball)

# ---- also today -----------------------------------------------------------
ax = gx + 2 * (pw + gap)
ay = gy + 1 * (ph + gap)
d.rectangle([ax, ay, ax + pw, ay + ph], outline=INK, width=2, fill=CREAM)
d.rectangle([ax, ay, ax + pw, ay + 8], fill=GOLD)
d.text((ax + 14, ay + 18), "ALSO TODAY", font=bb(16), fill=(120, 84, 20))
extra = [
    "Chess opens in Geneva — Gukesh defends his crown against Sindarov.",
    "India–New Zealand Test ends in a draw at Wellington.",
    "UK sanctions Myanmar generals over the Rohingya ruling.",
    "A supermoon meets the Pleiades in tonight's sky.",
]
yy = ay + 48
for item in extra:
    yy = block(d, ax + 28, yy, "•  " + item, rg(15), pw - 42, leading=18)
    yy += 5

# ---- footer ---------------------------------------------------------------
d.rectangle([24, 936, W - 24, 938], fill=GREY)
d.text((512, 946), "Six stories, one day  •  As reported 24 Nov 2026  •  "
       "BBC · Reuters · AP", font=rg(16), fill=GREY, anchor="ma")

img.save("entry.png", optimize=True)
print("saved entry.png", img.size)
