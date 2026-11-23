#!/usr/bin/env python3
"""Front page for Tuesday 24 November 2026.

Draws a 1024x1024 newspaper front page with Pillow, summarising the
day's world news from reporting published on 24 November 2026:
NATO's AWACS deployment to Poland, Moscow's 'open war' warning to
Estonia, Tajikistan leaving the ICC, India's Nepal package, the Java
factory fire, the COP31 collapse and Verstappen's Las Vegas win.

Run:  python3 draw_poster.py   -> writes entry.png beside this file.
"""

import math

from PIL import Image, ImageDraw, ImageFont

SIZE = 1024
CREAM = (248, 243, 232)
INK = (22, 22, 22)
NAVY = (18, 30, 58)
CRIMSON = (164, 22, 44)
GOLD = (196, 154, 32)
MUTED = (96, 92, 84)
RULE = (205, 197, 180)
WHITE = (255, 255, 255)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_I = "/usr/share/fonts/truetype/noto/NotoSerif-Italic.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def load(path, size):
    return ImageFont.truetype(path, size)


def split_lines(canvas, text, face, width):
    """Greedy wrap: return the lines of text that fit inside width."""
    out = []
    current = ""
    for word in text.split():
        joined = (current + " " + word).strip()
        if canvas.textlength(joined, font=face) <= width or not current:
            current = joined
        else:
            out.append(current)
            current = word
    if current:
        out.append(current)
    return out


def put_lines(canvas, x, y, lines, face, colour, gap):
    for line in lines:
        canvas.text((x, y), line, font=face, fill=colour)
        y += gap
    return y


def tag(canvas, x, y, label, colour):
    """Small filled label; returns the width it took."""
    face = load(SANS_B, 15)
    w = canvas.textlength(label, font=face) + 20
    canvas.rounded_rectangle([x, y, x + w, y + 25], radius=4, fill=colour)
    canvas.text((x + 10, y + 4), label, font=face, fill=WHITE)
    return w


def radar_panel(canvas, box):
    """Early-warning radar: concentric rings, a sweep and a plane."""
    x0, y0, x1, y1 = box
    canvas.rectangle(box, fill=NAVY)
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2 - 8
    for r in (128, 96, 64, 32):
        canvas.ellipse([cx - r, cy - r, cx + r, cy + r],
                       outline=(90, 120, 170), width=2)
    canvas.line([cx - 132, cy, cx + 132, cy], fill=(90, 120, 170), width=2)
    canvas.line([cx, cy - 132, cx, cy + 132], fill=(90, 120, 170), width=2)
    # sweep wedge: a few pale radial lines, not a solid fan
    for step in range(0, 10):
        a = math.radians(-90 + step * 7)
        px = cx + 128 * math.cos(a)
        py = cy + 128 * math.sin(a)
        canvas.line([cx, cy, px, py], fill=(110, 190, 110), width=2)
    # blips: three contacts on the scope
    for bx, by in [(cx - 78, cy - 52), (cx - 40, cy + 66), (cx + 88, cy - 30)]:
        canvas.ellipse([bx - 5, by - 5, bx + 5, by + 5], fill=(235, 90, 90))
    # simple AWACS silhouette: dome, long fuselage, wings, tail
    canvas.ellipse([cx - 12, cy - 66, cx + 12, cy - 46], fill=GOLD)
    canvas.rectangle([cx - 6, cy - 46, cx + 6, cy + 12], fill=WHITE)
    canvas.polygon([(cx - 78, cy - 34), (cx + 78, cy - 34),
                    (cx + 52, cy - 20), (cx - 52, cy - 20)], fill=WHITE)
    canvas.polygon([(cx - 6, cy + 12), (cx + 6, cy + 12),
                    (cx + 22, cy + 24), (cx - 22, cy + 24)], fill=WHITE)
    canvas.text((x0 + 14, y0 + 10), "E-3 AWACS", font=load(SANS_B, 18),
                fill=GOLD)
    canvas.text((x0 + 14, y0 + 34), "EYES OVER POLAND", font=load(SANS_B, 14),
                fill=(200, 210, 230))
    # bottom caption bar
    canvas.rectangle([x0, y1 - 40, x1, y1], fill=(12, 20, 40))
    canvas.text((x0 + 14, y1 - 32), "NATO's early-warning fleet",
                font=load(SANS_B, 16), fill=WHITE)


def story_card(canvas, box, kicker, tint, headline, body):
    x0, y0, x1, y1 = box
    canvas.rectangle(box, fill=WHITE, outline=RULE, width=2)
    canvas.rectangle([x0, y0, x0 + 6, y1], fill=tint)
    canvas.text((x0 + 18, y0 + 12), kicker, font=load(SANS_B, 14),
                fill=tint)
    head_face = load(SERIF_B, 22)
    lines = split_lines(canvas, headline, head_face, (x1 - x0) - 34)
    y = put_lines(canvas, x0 + 18, y0 + 38, lines[:2], head_face, INK, 27)
    body_face = load(SANS, 15)
    blines = split_lines(canvas, body, body_face, (x1 - x0) - 34)
    put_lines(canvas, x0 + 18, y + 6, blines[:3], body_face, (58, 56, 50), 19)


def main():
    img = Image.new("RGB", (SIZE, SIZE), CREAM)
    d = ImageDraw.Draw(img)

    # ---- masthead ----
    d.rectangle([0, 0, SIZE, 92], fill=NAVY)
    d.text((SIZE // 2, 6), "THE WORLD TODAY", font=load(SERIF_B, 58),
           fill=WHITE, anchor="ma")
    d.text((SIZE // 2, 68), "ONE DAY  \u2022  ONE PAGE  \u2022  EVERY STORY THAT MATTERED",
           font=load(SANS_B, 14), fill=GOLD, anchor="ma")

    # ---- date band ----
    d.rectangle([0, 92, SIZE, 148], fill=CRIMSON)
    d.text((SIZE // 2, 100), "TUESDAY, 24 NOVEMBER 2026",
           font=load(SERIF_B, 38), fill=WHITE, anchor="ma")
    d.line([0, 148, SIZE, 148], fill=GOLD, width=4)

    # ---- lead: art left, story right ----
    radar_panel(d, (36, 168, 420, 452))
    lx = 448
    tag(d, lx, 172, "EUROPE  \u2022  NATO", CRIMSON)
    lead_face = load(SERIF_B, 42)
    lead = "NATO sends AWACS to watch Poland's skies"
    y = put_lines(d, lx, 208,
                  split_lines(d, lead, lead_face, 540), lead_face, INK, 48)
    sub_face = load(SERIF_I, 23)
    sub = "Alliance answers the missiles that fell in Poland"
    y = put_lines(d, lx, y + 8,
                  split_lines(d, sub, sub_face, 540)[:1], sub_face, CRIMSON, 28)
    story = ("Three Russian weapons came down in south-east Poland on "
             "Friday. Warsaw invoked Article 4 and asked for more air "
             "defences; NATO is sending early-warning aircraft.")
    body_face = load(SANS, 18)
    put_lines(d, lx, y + 12,
              split_lines(d, story, body_face, 540)[:3], body_face,
              (38, 36, 32), 24)
    d.line([36, 466, 988, 466], fill=RULE, width=2)

    # ---- six stories, two rows of three ----
    stories = [
        ("BALTIC", (150, 30, 30),
         "Moscow warns Estonia of \u2018open war\u2019",
         "Russia summons Tallinn's envoy after Estonia says it will "
         "shut its border from 1 December."),
        ("JUSTICE", (60, 60, 160),
         "Tajikistan quits the ICC",
         "Dushanbe formally leaves the Rome Statute; the EU urges it "
         "to reconsider and reverse course."),
        ("ASIA", (200, 90, 0),
         "India pledges $1.6bn to Nepal",
         "Modi and Nepal's PM Shah agree a big aid package and flag "
         "off a new cross-border rail link."),
        ("INDONESIA", (0, 120, 120),
         "Java factory fire: 24 dead",
         "Rescuers keep searching for about 30 people still missing "
         "after the blaze in Banten."),
        ("CLIMATE", (30, 130, 30),
         "COP31 ends with no deal",
         "Antalya talks collapse over fossil fuels; countries leave "
         "without a consensus text."),
        ("SPORT", (160, 20, 40),
         "Verstappen wins in Las Vegas",
         "Red Bull's champion takes the Grand Prix; India and New "
         "Zealand draw the Wellington Test."),
    ]
    cw, ch, gap = 304, 168, 12
    for i, (kick, tint, head, body) in enumerate(stories):
        cx = 36 + (i % 3) * (cw + gap)
        cy = 480 + (i // 3) * (ch + gap)
        story_card(d, (cx, cy, cx + cw, cy + ch), kick, tint, head, body)

    # ---- also today ----
    ay = 840
    d.rectangle([0, ay, SIZE, 948], fill=NAVY)
    d.text((36, ay + 10), "ALSO TODAY", font=load(SANS_B, 19), fill=GOLD)
    items = ("CAS to rule on Senegal's AFCON title appeal  \u2022  Trump "
             "blames Democrats for the $1tn market slide  \u2022  Seoul "
             "names a new foreign minister  \u2022  Dhaka vows to arrest "
             "Hasina if she returns")
    a_face = load(SANS, 18)
    put_lines(d, 36, ay + 40,
              split_lines(d, items, a_face, 952), a_face, WHITE, 25)

    # ---- footer ----
    d.text((SIZE // 2, 958), "Drawn from the day\u2019s reporting  \u2022  Reuters  \u2022  AP  \u2022  AFP",
           font=load(SERIF_I, 17), fill=MUTED, anchor="ma")
    d.text((SIZE // 2, 982), "THE WORLD TODAY  \u2014  TUESDAY 24 NOVEMBER 2026",
           font=load(SANS_B, 14), fill=(58, 56, 50), anchor="ma")
    d.line([SIZE // 2 - 60, 1012, SIZE // 2 + 60, 1012], fill=GOLD, width=3)

    img.save("entry.png", optimize=True)
    print("wrote entry.png")


if __name__ == "__main__":
    main()
