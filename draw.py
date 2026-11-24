#!/usr/bin/env python3
"""Draw the 24 November 2026 world-news front page, 1024x1024 PNG.

Every element is drawn from code: no photos, no downloaded art.
Run: python3 draw.py  -> writes entry.png next to this script.
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

NAVY = (13, 27, 62)
PAPER = (250, 246, 236)
INK = (18, 18, 18)
RED = (178, 34, 34)
GOLD = (201, 162, 39)
TEAL = (0, 110, 110)
GREY = (90, 90, 90)
CARD = (255, 255, 255)
LINE = (200, 192, 175)

def font(path, size):
    return ImageFont.truetype(path, size)

def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def icon_chip(d, x, y, s, col):
    d.rounded_rectangle([x, y, x + s, y + s], radius=8, outline=col, width=5)
    d.rectangle([x + s * 0.28, y + s * 0.28, x + s * 0.72, y + s * 0.72],
                fill=col)
    for i in range(3):
        px = x + s * (0.22 + i * 0.28)
        d.line([px, y - 8, px, y], fill=col, width=4)
        d.line([px, y + s, px, y + s + 8], fill=col, width=4)
        py = y + s * (0.22 + i * 0.28)
        d.line([x - 8, py, x, py], fill=col, width=4)
        d.line([x + s, py, x + s + 8, py], fill=col, width=4)

def icon_globe(d, x, y, s, col):
    d.ellipse([x, y, x + s, y + s], outline=col, width=5)
    d.ellipse([x + s * 0.28, y, x + s * 0.72, y + s], outline=col, width=3)
    d.line([x, y + s * 0.5, x + s, y + s * 0.5], fill=col, width=3)
    d.arc([x, y + s * 0.18, x + s, y + s * 0.82], 200, 340, fill=col, width=3)
    # crack: no-deal slash
    d.line([x + s * 0.15, y + s * 0.85, x + s * 0.85, y + s * 0.15],
           fill=RED, width=6)

def icon_flame(d, x, y, s, col):
    pts = [(x + s * 0.5, y),
           (x + s * 0.78, y + s * 0.32),
           (x + s * 0.95, y + s * 0.62),
           (x + s * 0.72, y + s),
           (x + s * 0.28, y + s),
           (x + s * 0.05, y + s * 0.62),
           (x + s * 0.22, y + s * 0.32)]
    d.polygon(pts, fill=col)
    d.ellipse([x + s * 0.38, y + s * 0.55, x + s * 0.62, y + s * 0.85],
              fill=(255, 210, 63))

def icon_ship(d, x, y, s, col):
    d.polygon([(x, y + s * 0.62), (x + s, y + s * 0.62),
               (x + s * 0.82, y + s), (x + s * 0.18, y + s)], fill=col)
    d.rectangle([x + s * 0.42, y + s * 0.18, x + s * 0.58, y + s * 0.62],
                fill=col)
    d.rectangle([x + s * 0.18, y + s * 0.30, x + s * 0.82, y + s * 0.44],
                fill=col)
    # smoke / blast
    d.ellipse([x + s * 0.62, y + 2, x + s * 0.76, y + s * 0.16], fill=RED)
    d.ellipse([x + s * 0.74, y + s * 0.08, x + s * 0.90, y + s * 0.24],
              fill=(255, 140, 0))

def icon_scales(d, x, y, s, col):
    d.line([x + s * 0.5, y, x + s * 0.5, y + s * 0.85], fill=col, width=5)
    d.line([x + s * 0.08, y + s * 0.22, x + s * 0.92, y + s * 0.22],
           fill=col, width=5)
    d.polygon([(x + s * 0.08, y + s * 0.22), (x + s * 0.30, y + s * 0.62),
               (x - s * 0.02, y + s * 0.62)], outline=col, width=4)
    d.polygon([(x + s * 0.92, y + s * 0.22), (x + s * 0.70, y + s * 0.62),
               (x + s * 1.02, y + s * 0.62)], outline=col, width=4)
    d.line([x + s * 0.30, y + s * 0.85, x + s * 0.70, y + s * 0.85],
           fill=col, width=5)

def icon_ball(d, x, y, s, col):
    d.ellipse([x, y, x + s, y + s], fill=col)
    d.arc([x - s * 0.35, y + s * 0.12, x + s * 0.45, y + s * 0.88],
          270, 90, fill=(255, 255, 255), width=5)
    d.arc([x + s * 0.55, y + s * 0.12, x + s * 1.35, y + s * 0.88],
          90, 270, fill=(255, 255, 255), width=5)

ICONS = {"chip": icon_chip, "globe": icon_globe, "flame": icon_flame,
         "ship": icon_ship, "scales": icon_scales, "ball": icon_ball}

STORIES = [
    ("TECH  ·  USA", "NVIDIA BRINGS BACK HUANG",
     "Board reinstates Jensen Huang as CEO; shares jump more than 30%.",
     "chip", TEAL),
    ("CLIMATE  ·  WORLD", "COP31 ENDS WITH NO DEAL",
     "Climate talks end with no agreement; may resume next year.",
     "globe", (150, 90, 0)),
    ("DISASTER  ·  INDONESIA", "FACTORY FIRE KILLS AT LEAST 24",
     "Blaze at a candy factory; rescuers search for missing workers.",
     "flame", RED),
    ("WAR  ·  LIBYA", "UKRAINE CLAIMS WARSHIP SUNK",
     "Missile corvette reported destroyed off the port of Benghazi.",
     "ship", NAVY),
    ("JUSTICE  ·  THE HAGUE", "MYANMAR GUILTY OF GENOCIDE",
     "Top UN court rules against Myanmar over the Rohingya.",
     "scales", (90, 60, 140)),
    ("SPORT  ·  TURIN", "ALCARAZ WINS ATP FINALS",
     "First Finals title for the Spaniard, beating Zverev.",
     "ball", (60, 140, 60)),
]

def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead ----
    d.rectangle([0, 0, W, 196], fill=NAVY)
    d.rectangle([0, 196, W, 202], fill=GOLD)
    f_kicker = font(BOLD, 28)
    d.text((512, 30), "THE WORLD IN ONE DAY", font=f_kicker,
           fill=GOLD, anchor="ma")
    f_date = font(BOLD, 78)
    d.text((512, 58), "24 NOVEMBER 2026", font=f_date,
           fill=(255, 255, 255), anchor="ma")
    f_sub = font(REG, 27)
    d.text((512, 152), "TUESDAY  ·  WORLD NEWS IN ONE IMAGE",
           font=f_sub, fill=(200, 210, 230), anchor="ma")

    # ---- story grid: 2 cols x 3 rows ----
    margin, gap = 28, 18
    cw = (W - 2 * margin - gap) // 2
    ch = 232
    top = 224
    f_tag = font(BOLD, 21)
    f_head = font(BOLD, 28)
    f_body = font(REG, 24)

    for i, (tag, head, body, icon, col) in enumerate(STORIES):
        r, c = divmod(i, 2)
        x0 = margin + c * (cw + gap)
        y0 = top + r * (ch + gap)
        d.rounded_rectangle([x0, y0, x0 + cw, y0 + ch], radius=14,
                            fill=CARD, outline=LINE, width=2)
        # icon box
        ix, iy, isz = x0 + 18, y0 + 18, 64
        ICONS[icon](d, ix, iy, isz, col)
        tx = x0 + 100
        d.text((tx, y0 + 16), tag, font=f_tag, fill=col)
        head_lines = wrap(d, head, f_head, cw - 118)
        yy = y0 + 46
        for ln in head_lines[:2]:
            d.text((tx, yy), ln, font=f_head, fill=INK)
            yy += 36
        body_lines = wrap(d, body, f_body, cw - 36)
        by = y0 + 132
        for ln in body_lines[:2]:
            d.text((x0 + 18, by), ln, font=f_body, fill=(60, 60, 60))
            by += 30

    # ---- footer ----
    fy = top + 3 * ch + 2 * gap + 12
    d.line([margin, fy, W - margin, fy], fill=LINE, width=2)
    f_foot = font(REG, 20)
    d.text((512, fy + 10),
           "Sources: People · Forbes · BBC · Times of India · Naval News · UN court reports",
           font=f_foot, fill=GREY, anchor="ma")

    img.save("entry.png", optimize=True)
    print("saved entry.png", img.size)

if __name__ == "__main__":
    main()
