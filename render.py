#!/usr/bin/env python3
"""Draw the 20 November 2026 world-news front page (1024x1024 PNG).

Six stories first reported on Friday 20 November 2026, each checked
against at least two independent outlets (see README.md). Layout: a
newspaper front page -- masthead, one lead story, five panels, and a
"day in numbers" box. Every letter is drawn by this code with DejaVu
fonts, so no text can come out garbled. No network, no image model,
no randomness: the same bytes come out on every run.
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 36
PAPER = (253, 244, 224)
INK = (23, 32, 66)
WHITE = (255, 255, 255)
RED = (198, 40, 40)
TEAL = (0, 121, 107)
GOLD = (214, 158, 24)
BLUE = (30, 90, 160)
GREY = (90, 96, 110)
LIGHT = (238, 232, 214)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

def font(path, size):
    return ImageFont.truetype(path, size)

def wrap(draw, text, fnt, width):
    """Greedy word wrap to the given pixel width."""
    lines, cur = [], ""
    for word in text.split():
        trial = f"{cur} {word}".strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines

def centred(draw, text, fnt, y, colour, cx=W // 2):
    draw.text((cx - draw.textlength(text, font=fnt) / 2, y), text,
              font=fnt, fill=colour)

def rule(draw, y, colour=INK, width=3):
    draw.line([(MARGIN, y), (W - MARGIN, y)], fill=colour, width=width)

# --- small drawn icons, each in its own box -------------------------------

def icon_hourglass(d, x, y, s, colour):
    d.polygon([(x, y), (x + s, y), (x + s // 2, y + s // 2)], outline=colour, width=4)
    d.polygon([(x, y + s), (x + s, y + s), (x + s // 2, y + s // 2)], outline=colour, width=4)
    d.line([(x, y), (x + s, y)], fill=colour, width=5)
    d.line([(x, y + s), (x + s, y + s)], fill=colour, width=5)
    d.ellipse([x + s // 2 - 4, y + s // 2 - 4, x + s // 2 + 4, y + s // 2 + 4], fill=colour)

def icon_cyclone(d, x, y, s, colour):
    cx, cy = x + s // 2, y + s // 2
    for r in (10, 20, 30, 40):
        d.arc([cx - r, cy - r, cx + r, cy + r], start=20, end=300,
              fill=colour, width=5)
    d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=colour)
    for dx in (-34, -12, 12, 34):
        d.line([(x + s // 2 + dx, y + s - 4), (x + s // 2 + dx - 5, y + s + 12)],
               fill=colour, width=4)

def icon_voyager(d, x, y, s, colour):
    for sx, sy in [(x + 8, y + 6), (x + s - 10, y + 18), (x + 20, y + s - 8),
                   (x + s - 22, y + s - 16)]:
        d.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=colour)
    d.line([(x + 10, y + s - 10), (x + s - 14, y + 14)], fill=colour, width=3)
    d.ellipse([x + s - 34, y + 6, x + s - 6, y + 34], outline=colour, width=4)
    d.line([(x + s - 20, y + 34), (x + s - 20, y + s - 22)], fill=colour, width=4)
    d.rectangle([x + s - 30, y + s - 22, x + s - 10, y + s - 8], fill=colour)

def icon_probe(d, x, y, s, colour):
    d.rectangle([x + s // 2 - 16, y + 16, x + s // 2 + 16, y + 48], fill=colour)
    d.rectangle([x + 6, y + 24, x + s // 2 - 20, y + 40], outline=colour, width=4)
    d.rectangle([x + s // 2 + 20, y + 24, x + s - 6, y + 40], outline=colour, width=4)
    d.line([(x + s // 2, y + 16), (x + s // 2, y + 4)], fill=colour, width=3)
    d.ellipse([x + s // 2 - 3, y + 1, x + s // 2 + 3, y + 7], fill=colour)
    d.ellipse([x + 2, y + s - 34, x + 34, y + s - 2], fill=GREY)
    d.line([(x + 2, y + s - 34), (x + 34, y + s - 2)], fill=RED, width=6)
    d.line([(x + 34, y + s - 34), (x + 2, y + s - 2)], fill=RED, width=6)

def icon_skyline(d, x, y, s, colour):
    d.ellipse([x + s - 34, y + 2, x + s - 4, y + 32], fill=GOLD)
    base = y + s - 6
    heights = [44, 62, 34, 56, 40]
    bw = s // 5
    for i, hgt in enumerate(heights):
        d.rectangle([x + i * bw + 2, base - hgt, x + (i + 1) * bw - 2, base],
                    fill=colour)
    d.line([(x, base), (x + s, base)], fill=colour, width=4)

def icon_talks(d, x, y, s, colour):
    d.rounded_rectangle([x + 4, y + 8, x + s // 2 + 16, y + 44], radius=10,
                        outline=colour, width=4)
    d.polygon([(x + 16, y + 44), (x + 30, y + 44), (x + 16, y + 58)],
              fill=colour)
    d.rounded_rectangle([x + s // 2 - 6, y + 30, x + s - 4, y + 66], radius=10,
                        outline=TEAL, width=4)
    d.polygon([(x + s - 30, y + 66), (x + s - 16, y + 66), (x + s - 30, y + 80)],
              fill=TEAL)
    for yy in (20, 30):
        d.line([(x + 14, y + yy), (x + s // 2 + 4, y + yy)], fill=colour, width=3)

ICONS = {
    "hourglass": icon_hourglass,
    "cyclone": icon_cyclone,
    "voyager": icon_voyager,
    "probe": icon_probe,
    "skyline": icon_skyline,
    "talks": icon_talks,
}

# --- the six stories --------------------------------------------------------

LEAD = {
    "kicker": "LEAD  ·  WASHINGTON",
    "headline": "TRUMP PUTS IRAN WAR DECISION OFF TO 2027",
    "body": ("The US president says there is no rush on Iran: he will "
             "\u201csee what happens\u201d after 1 January, pushing any "
             "decision into next year."),
    "icon": "hourglass",
    "colour": RED,
}

PANELS = [
    {
        "kicker": "INDIA  ·  WEATHER",
        "headline": "CYCLONE AKVAN: 300,000 EVACUATED",
        "body": ("Odisha moves three lakh people to safety and deploys 423 "
                 "rescue teams as the severe storm closes on the coast."),
        "icon": "cyclone",
        "colour": BLUE,
    },
    {
        "kicker": "SPACE  ·  NASA",
        "headline": "VOYAGER 1 PASSES ONE LIGHT-DAY OUT",
        "body": ("The farthest human-made object crosses a new milestone: "
                 "its signals now take a full day to reach Earth."),
        "icon": "voyager",
        "colour": INK,
    },
    {
        "kicker": "SPACE  ·  JAPAN",
        "headline": "HAYABUSA2 DROPS ITS ASTEROID LANDING",
        "body": ("Engine trouble forces JAXA to scrap the planned touchdown "
                 "and rewrite the mission."),
        "icon": "probe",
        "colour": TEAL,
    },
    {
        "kicker": "BUSINESS  ·  GAMES",
        "headline": "GTA 6 SALES PASS $1.8 BILLION",
        "body": ("One day after launch, Grand Theft Auto VI has already "
                 "outsold the whole global run of The Odyssey."),
        "icon": "skyline",
        "colour": GOLD,
    },
    {
        "kicker": "EUROPE  ·  UKRAINE",
        "headline": "EUROPE READY TO TALK PEACE WITH RUSSIA",
        "body": ("European leaders say they are ready for talks to end the "
                 "war, as Russian strikes hit two embassies in Kyiv."),
        "icon": "talks",
        "colour": RED,
    },
]

NUMBERS = [
    ("300,000", "people evacuated\nfrom Cyclone Akvan"),
    ("1 light-day", "Voyager 1\u2019s distance\nfrom Earth"),
    ("$1.8bn", "GTA 6 sales in\nits first day"),
]

# --- drawing ---------------------------------------------------------------

def draw_panel(d, box, story):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=WHITE, outline=INK, width=3)
    d.rectangle([x0, y0, x1, y0 + 8], fill=story["colour"])
    pad = 16
    tx = x0 + pad
    ty = y0 + 22
    d.text((tx, ty), story["kicker"], font=font(SANS_B, 15), fill=story["colour"])
    ty += 24
    for line in wrap(d, story["headline"], font(SANS_B, 21), x1 - x0 - 2 * pad):
        d.text((tx, ty), line, font=font(SANS_B, 21), fill=INK)
        ty += 26
    ty += 6
    icon_size = 78
    ICONS[story["icon"]](d, tx, ty, icon_size, story["colour"])
    body_x = tx + icon_size + 14
    body_w = x1 - body_x - pad
    by = ty + 2
    for line in wrap(d, story["body"], font(SANS, 15), body_w):
        d.text((body_x, by), line, font=font(SANS, 15), fill=(52, 52, 66))
        by += 20

def draw_numbers(d, box):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=INK, outline=INK, width=3)
    d.text((x0 + 16, y0 + 14), "THE DAY IN NUMBERS",
           font=font(SANS_B, 15), fill=GOLD)
    y = y0 + 44
    small_x = x0 + 168
    small_w = x1 - small_x - 14
    for big, small in NUMBERS:
        d.text((x0 + 16, y), big, font=font(SANS_B, 23), fill=WHITE)
        ly = y + 2
        for line in wrap(d, small.replace("\n", " "), font(SANS, 14), small_w):
            d.text((small_x, ly), line, font=font(SANS, 14), fill=(210, 210, 220))
            ly += 18
        y += 62

def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # masthead
    rule(d, 44, width=4)
    centred(d, "THE WORLD IN ONE DAY", font(SERIF_B, 56), 58, INK)
    centred(d, "FRIDAY  ·  20 NOVEMBER 2026", font(SANS_B, 24), 132, RED)
    centred(d, "SIX STORIES  ·  ONE DAY  ·  CHECKED AGAINST TWO SOURCES EACH",
            font(SANS, 15), 166, GREY)
    rule(d, 192, width=4)
    rule(d, 198, width=2)

    # lead story
    lx0, ly0, lx1, ly1 = MARGIN, 214, W - MARGIN, 404
    d.rectangle([lx0, ly0, lx1, ly1], fill=WHITE, outline=INK, width=3)
    d.rectangle([lx0, ly0, lx1, ly0 + 8], fill=RED)
    icon_box = 120
    ICONS["hourglass"](d, lx0 + 22, ly0 + 44, icon_box, RED)
    tx = lx0 + 22 + icon_box + 26
    d.text((tx, ly0 + 26), LEAD["kicker"], font=font(SANS_B, 16), fill=RED)
    ty = ly0 + 52
    for line in wrap(d, LEAD["headline"], font(SANS_B, 33), lx1 - tx - 22):
        d.text((tx, ty), line, font=font(SANS_B, 33), fill=INK)
        ty += 40
    ty += 8
    for line in wrap(d, LEAD["body"], font(SANS, 18), lx1 - tx - 22):
        d.text((tx, ty), line, font=font(SANS, 18), fill=(52, 52, 66))
        ty += 24

    # five panels + numbers box in a 3 x 2 grid
    grid_top, grid_bottom = 420, 940
    gap = 16
    cw = (W - 2 * MARGIN - 2 * gap) // 3
    ch = (grid_bottom - grid_top - gap) // 2
    cells = []
    for row in range(2):
        for col in range(3):
            x0 = MARGIN + col * (cw + gap)
            y0 = grid_top + row * (ch + gap)
            cells.append((x0, y0, x0 + cw, y0 + ch))
    for cell, story in zip(cells[:5], PANELS):
        draw_panel(d, cell, story)
    draw_numbers(d, cells[5])

    # footer
    rule(d, 956, width=2)
    d.text((MARGIN, 966),
           "Sources: Reuters · The Times of India · The Hindu · NASA · JAXA · BBC · Space",
           font=font(SANS, 14), fill=GREY)
    d.text((MARGIN, 986),
           "An entry for make.fun news-image-20261120  ·  Drawn by code, no photographs",
           font=font(SANS, 14), fill=GREY)

    img.save("entry.png", optimize=True)
    print("wrote entry.png", img.size)

if __name__ == "__main__":
    main()
