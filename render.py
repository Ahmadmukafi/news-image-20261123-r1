#!/usr/bin/env python3
"""Render the news-image-20261123 r1 front page: THE WORLD TODAY.

Build-time only. Draws a 1024x1024 broadsheet front page with PIL and writes
entry.png next to this script. Every headline is real news of Monday
23 November 2026, verified against live sources before drawing.
"""
import math
import textwrap

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (246, 241, 231)
INK = (17, 17, 17)
NAVY = (12, 35, 64)
NAVY2 = (18, 52, 92)
RED = (179, 39, 30)
GOLD = (198, 156, 58)
TEAL = (14, 74, 78)
GREY = (90, 86, 78)
ORANGE = (232, 122, 34)
FLAME = (245, 176, 65)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap to a pixel width."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, text, fnt, width, fill=INK, leading=None):
    """Draw wrapped paragraph, return y after last line."""
    if leading is None:
        leading = int(fnt.size * 1.28)
    for line in wrap(draw, text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def rule(draw, x0, y, x1, color=INK, width=2):
    draw.line([(x0, y), (x1, y)], fill=color, width=width)


def draw_lead_art(d, x0, y0, x1, y1):
    """Night scene over the Gulf: sky, sea, tankers, missile arcs, flame."""
    d.rectangle([x0, y0, x1, y1], fill=(10, 22, 44))
    # sky bands getting lighter toward the horizon
    horizon = y0 + int((y1 - y0) * 0.62)
    for i in range(6):
        yy = y0 + i * (horizon - y0) // 6
        shade = 10 + i * 5
        d.rectangle([x0, yy, x1, yy + (horizon - y0) // 6 + 1],
                    fill=(shade, 22 + i * 4, 44 + i * 6))
    # stars
    stars = [(40, 18), (120, 40), (210, 14), (300, 34), (380, 16),
             (470, 42), (540, 20), (90, 64), (250, 58), (430, 66),
             (580, 52), (170, 30), (340, 60), (510, 70)]
    for sx, sy in stars:
        d.ellipse([x0 + sx - 2, y0 + sy - 2, x0 + sx + 2, y0 + sy + 2],
                  fill=(235, 230, 210))
    # moon
    d.ellipse([x1 - 90, y0 + 22, x1 - 46, y0 + 66], fill=(240, 232, 200))
    d.ellipse([x1 - 82, y0 + 28, x1 - 46, y0 + 66], fill=(16, 30, 54))
    # distant skyline (Bahrain) on the horizon
    base = horizon
    skyline = [(0, 46), (52, 46), (52, 26), (74, 26), (74, 46), (110, 46),
               (110, 18), (128, 18), (128, 46), (170, 46), (170, 30),
               (196, 30), (196, 46), (240, 46), (240, 12), (258, 12),
               (258, 46), (300, 46), (300, 34), (330, 34), (330, 46)]
    pts = [(x0 + px, base - py) for px, py in skyline]
    pts += [(x0 + 330, base), (x0, base)]
    d.polygon(pts, fill=(6, 14, 30))
    # flame over the skyline (factory ablaze on Sitra Island)
    fx, fy = x0 + 250, base - 12
    d.polygon([(fx - 16, fy), (fx - 6, fy - 26), (fx, fy - 40),
               (fx + 7, fy - 24), (fx + 16, fy)], fill=ORANGE)
    d.polygon([(fx - 9, fy), (fx - 3, fy - 16), (fx + 2, fy - 24),
               (fx + 5, fy - 12), (fx + 9, fy)], fill=FLAME)
    # sea
    d.rectangle([x0, horizon, x1, y1], fill=(13, 42, 66))
    for i in range(5):
        yy = horizon + 14 + i * 16
        d.line([(x0 + 8, yy), (x1 - 8, yy)], fill=(28, 74, 104), width=2)
    # two tanker silhouettes with glowing decks
    for tx, tw in [(x0 + 60, 150), (x0 + 330, 120)]:
        ty = y1 - 66
        d.polygon([(tx, ty), (tx + 18, ty - 26), (tx + tw - 18, ty - 26),
                   (tx + tw, ty), (tx + tw, ty + 12), (tx, ty + 12)],
                  fill=(5, 12, 26))
        d.rectangle([tx + 22, ty - 40, tx + 44, ty - 26], fill=(5, 12, 26))
        d.rectangle([tx + 26, ty - 52, tx + 34, ty - 40], fill=(5, 12, 26))
        d.rectangle([tx + 10, ty - 22, tx + tw - 10, ty - 18],
                    fill=(232, 122, 34))
    # missile arcs: bright streaks with glowing heads
    arcs = [((x0 + 90, y0 + 150), (x0 + 300, y0 + 30), (x0 + 470, y0 + 96)),
            ((x0 + 180, y0 + 170), (x0 + 380, y0 + 70), (x0 + 540, y0 + 130))]
    for p0, p1, p2 in arcs:
        steps = 40
        prev = None
        for i in range(steps + 1):
            t = i / steps
            mx = (1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t * t * p2[0]
            my = (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t * t * p2[1]
            if prev is not None:
                d.line([prev, (mx, my)], fill=(245, 176, 65), width=3)
            prev = (mx, my)
        d.ellipse([p2[0] - 7, p2[1] - 7, p2[0] + 7, p2[1] + 7],
                  fill=(255, 214, 120))
        d.ellipse([p2[0] - 3, p2[1] - 3, p2[0] + 3, p2[1] + 3],
                  fill=(255, 240, 200))
    # caption tag on the art
    d.rectangle([x0, y1 - 30, x0 + 300, y1], fill=RED)
    d.text((x0 + 12, y1 - 25), "BAHRAIN  •  STRAIT OF HORMUZ",
           font=font(SANS_B, 15), fill=(255, 255, 255))


def draw_cop_art(d, x0, y0, x1, y1):
    """COP31 panel: a globe split by a red crack, on teal."""
    d.rectangle([x0, y0, x1, y1], fill=TEAL)
    cx, cy, r = (x0 + x1) // 2, y0 + 92, 62
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(36, 120, 110))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(220, 235, 225),
              width=3)
    # land blobs
    d.ellipse([cx - 42, cy - 34, cx - 8, cy - 6], fill=(96, 168, 92))
    d.ellipse([cx + 2, cy + 4, cx + 38, cy + 34], fill=(96, 168, 92))
    d.ellipse([cx - 14, cy - 48, cx + 16, cy - 26], fill=(120, 186, 110))
    # latitude lines (flattened arcs across the globe)
    for dy, ry in ((-30, 16), (0, 26), (30, 16)):
        d.arc([cx - r + 8, cy + dy - ry, cx + r - 8, cy + dy + ry],
              200, 340, fill=(220, 235, 225), width=2)
    # red crack across the globe
    d.line([(cx - 58, cy - 44), (cx - 12, cy - 6), (cx + 10, cy + 8),
            (cx + 52, cy + 46)], fill=RED, width=7)
    d.line([(cx - 58, cy - 44), (cx - 12, cy - 6), (cx + 10, cy + 8),
            (cx + 52, cy + 46)], fill=(255, 120, 100), width=3)
    d.text((x0 + 12, y1 - 30), "ANTALYA, TURKEY", font=font(SANS_B, 15),
           fill=(255, 255, 255))


def icon_burst(d, cx, cy, r, color):
    pts = []
    for i in range(16):
        ang = 3.14159 * i / 8
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(ang),
                    cy + rr * math.sin(ang)))
    d.polygon(pts, fill=color)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead ----
    d.rectangle([0, 0, W, 96], fill=NAVY)
    d.text((W // 2, 12), "THE WORLD TODAY", font=font(SERIF_B, 58),
           fill=(255, 255, 255), anchor="ma")
    d.rectangle([0, 96, W, 100], fill=GOLD)
    d.text((24, 108), "MONDAY, 23 NOVEMBER 2026",
           font=font(SANS_B, 22), fill=RED)
    d.text((1000, 108), "ONE DAY  •  ONE PICTURE",
           font=font(SANS_B, 22), fill=GREY, anchor="ra")
    rule(d, 24, 140, 1000, color=INK, width=3)

    # ---- lead: art + headline (left) ----
    draw_lead_art(d, 24, 152, 640, 380)
    y = 392
    d.text((24, y), "THE GULF WAR SPREADS",
           font=font(SANS_B, 20), fill=RED)
    y += 30
    y = para(d, 24, y, "IRAN STRIKES U.S. BASES IN BAHRAIN",
             font(SERIF_B, 40), 616, leading=46)
    y += 6
    y = para(d, 24, y,
             "Missiles and drones hit American positions; two tankers "
             "struck in the Strait of Hormuz as the war reaches Saudi "
             "Arabia. Tehran claims two Patriot radars hit; Bahrain "
             "reports a factory ablaze and two people hurt.",
             font(SANS, 18), 616, leading=23)

    # ---- COP31 (right column) ----
    draw_cop_art(d, 664, 152, 1000, 330)
    y = 346
    d.text((664, y), "CLIMATE", font=font(SANS_B, 20), fill=RED)
    y += 30
    y = para(d, 664, y, "COP31 COLLAPSES IN ANTALYA",
             font(SERIF_B, 34), 336, leading=40)
    y += 6
    y = para(d, 664, y,
             "Nearly 200 nations fail to agree. The EU walks out over a "
             "draft that never mentions fossil fuels, ending the longest "
             "climate summit ever with no deal.",
             font(SANS, 17), 336, leading=22)

    # ---- also today ----
    rule(d, 24, 622, 1000, color=INK, width=2)
    d.text((24, 630), "ALSO TODAY", font=font(SANS_B, 20), fill=RED)
    rule(d, 24, 660, 1000, color=GREY, width=1)

    stories = [
        ("UKRAINE", "Russian drone hits Kyiv supermarket",
         "At least 3 killed, 15 hurt; 14 missing after a strike on a "
         "block of flats in the Kyiv region.", RED),
        ("UNITED STATES", "Democrats clinch 258 House seats",
         "Their largest majority since 1992, sealed by a win in North "
         "Carolina on Sunday.", NAVY2),
        ("ASIA", "Nepal PM meets Modi in Delhi",
         "Balendra Shah's state visit. Seoul's education minister quits "
         "over an AI cheating scandal.", TEAL),
        ("INDONESIA", "Factory fire leaves dozens missing",
         "Rescuers search a burned candy factory as bodies are recovered "
         "and families wait for news.", ORANGE),
    ]
    col_w, gap = 238, 8
    for i, (kicker, head, deck, color) in enumerate(stories):
        x = 24 + i * (col_w + gap)
        if i:
            d.line([(x - 5, 676), (x - 5, 896)], fill=(200, 194, 180),
                   width=1)
        icon_burst(d, x + 16, 694, 14, color)
        d.text((x + 38, 682), kicker, font=font(SANS_B, 17), fill=color)
        yy = para(d, x, 716, head, font(SERIF_B, 24), col_w, leading=29)
        para(d, x, yy + 4, deck, font(SANS, 16), col_w, leading=21)

    # ---- bottom ticker: sport ----
    d.rectangle([0, 908, W, H], fill=NAVY)
    d.rectangle([0, 908, W, 912], fill=GOLD)
    d.text((24, 926), "SPORT", font=font(SANS_B, 20), fill=GOLD)
    d.text((120, 926),
           "INDIA 720/9d — A RECORD TOTAL AT WELLINGTON",
           font=font(SANS_B, 20), fill=(255, 255, 255))
    d.text((24, 962),
           "LIVERPOOL THRASH 10-MAN MAN UTD  •  THE WORLD TODAY, MONDAY 23 NOVEMBER 2026",
           font=font(SANS, 17), fill=(200, 210, 225))

    img.save("entry.png", optimize=True)
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    main()
