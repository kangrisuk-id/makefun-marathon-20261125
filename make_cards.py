#!/usr/bin/env python3
"""Render the README gallery cards for the One-Liner Marathon entry.

Build-time asset tool only: it runs on the author's machine (which has
Pillow) to produce card-entry.png and card-finalists.png. The grader
never runs this file — the entry itself is main.py, pure stdlib.

Palette matches cover.png: deep teal night office, warm amber light.
"""

import textwrap

from PIL import Image, ImageDraw, ImageFont

TEAL = (13, 43, 54)
TEAL_LIGHT = (21, 63, 78)
AMBER = (245, 183, 49)
PAPER = (252, 240, 214)
INK = (24, 32, 38)
MUTED = (168, 196, 204)

FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(path, size)


def wrap(draw: ImageDraw.ImageDraw, text: str, fnt, max_width: int) -> list[str]:
    words, lines, current = text.split(), [], ""
    for word in words:
        trial = f"{current} {word}".strip()
        if draw.textlength(trial, font=fnt) <= max_width:
            current = trial
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def entry_card() -> None:
    """The winning line, typeset like a calendar page for Thursday."""
    img = Image.new("RGB", (1200, 760), TEAL)
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([60, 60, 1140, 700], radius=28, fill=PAPER)
    d.rounded_rectangle([60, 60, 1140, 190], radius=28, fill=AMBER)
    d.rectangle([60, 150, 1140, 190], fill=AMBER)
    d.text((600, 125), "THURSDAY", font=font(FONT_BOLD, 64), fill=INK, anchor="mm")
    d.text((600, 235), "the winning one-liner, in full",
           font=font(FONT_REG, 30), fill=(110, 96, 60), anchor="mm")
    joke = ("The meeting could have been an email. The email could have "
            "been a shrug. The shrug is scheduled for Thursday.")
    y = 310
    for line in wrap(d, joke, font(FONT_BOLD, 47), 940):
        d.text((600, y), line, font=font(FONT_BOLD, 47), fill=INK, anchor="mm")
        y += 66
    d.text((600, 640), "109 characters  ·  gate limit 280  ·  one line, no caption needed",
           font=font(FONT_REG, 27), fill=(110, 96, 60), anchor="mm")
    img.save("card-entry.png")


FINALISTS = [
    ("WINNER — 24/25", "The meeting could have been an email. The email could have "
     "been a shrug. The shrug is scheduled for Thursday."),
    ("FINALIST — 24/25", "Some people meditate. I just sit in my car in the driveway "
     "for ten minutes, arriving home in installments."),
    ("SEMI-FINALIST — 22/25", "My therapist says I have abandonment issues, which is "
     "rich, because she's the one who keeps ending our sessions."),
    ("SEMI-FINALIST — 22/25", "The office printer knows when you're in a hurry. "
     "It isn't broken; it's savoring this."),
]


def finalists_card() -> None:
    """The tournament's last four, with their scores against the brief."""
    img = Image.new("RGB", (1200, 1060), TEAL)
    d = ImageDraw.Draw(img)
    d.text((600, 78), "THE LAST FOUR STANDING", font=font(FONT_BOLD, 46),
           fill=AMBER, anchor="mm")
    d.text((600, 128), "42 candidates entered · scored on the judge's five criteria",
           font=font(FONT_REG, 28), fill=MUTED, anchor="mm")
    y = 180
    for label, line in FINALISTS:
        d.rounded_rectangle([60, y, 1140, y + 195], radius=22, fill=TEAL_LIGHT)
        d.text((95, y + 34), label, font=font(FONT_BOLD, 27), fill=AMBER)
        ty = y + 78
        for wrapped in wrap(d, line, font(FONT_REG, 31), 1010):
            d.text((95, ty), wrapped, font=font(FONT_REG, 31), fill=PAPER)
            ty += 42
        y += 215
    img.save("card-finalists.png")


if __name__ == "__main__":
    entry_card()
    finalists_card()
    print("cards written")
