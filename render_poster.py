#!/usr/bin/env python3
"""Render the front page for Sunday 22 November 2026 as a 1024x1024 PNG.

A broadsheet-style poster summing up the day's world news: one lead story
on the Gulf escalation, secondary stories on Europe and the APEC summit in
Shenzhen, and a round-up box for the rest of the day. Deterministic output:
fixed fonts, fixed layout, no timestamps, no network.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

PAPER = (247, 243, 232)
INK = (18, 18, 18)
RED = (158, 24, 24)
GREY = (90, 86, 76)
RULE = (40, 40, 40)
BOX_BG = (238, 232, 214)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, text, fnt, max_w, leading, fill=INK):
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def rule(draw, x0, y, x1, width=2):
    draw.line([(x0, y), (x1, y)], fill=RULE, width=width)


def label(draw, x, y, text):
    f = font(SANS_B, 15)
    draw.text((x, y), text, font=f, fill=RED)
    return y + 22


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    mx = 44  # side margin

    # ---- Masthead -------------------------------------------------------
    rule(d, mx, 26, W - mx, 4)
    d.text((W // 2, 44), "THE WORLD TODAY", font=font(SERIF_B, 74),
           fill=INK, anchor="ma")
    rule(d, mx, 138, W - mx, 2)
    d.text((W // 2, 152), "SUNDAY 22 NOVEMBER 2026  |  ONE IMAGE, THE DAY'S WORLD NEWS",
           font=font(SANS_B, 17), fill=INK, anchor="ma")
    rule(d, mx, 184, W - mx, 4)

    # ---- Lead story -----------------------------------------------------
    y = 206
    y = label(d, mx, y, "LEAD  \u2014  THE GULF")
    y = para(d, mx, y, "Iran strikes US base in Kuwait as Gulf crisis deepens",
             font(SERIF_B, 46), W - 2 * mx, 50)
    y += 6
    y = para(d, mx, y,
             "Iran hit a United States air base in Kuwait and targeted Bahrain, "
             "while several tankers were struck off the coast of Oman as naval "
             "tensions between Iran and the US escalated. Bahrain is investigating "
             "a Patriot interceptor crash amid reports of Iranian drone attacks.",
             font(SERIF, 20), W - 2 * mx, 26)
    y += 10
    rule(d, mx, y, W - mx, 2)
    y += 14

    # ---- Graphic motif: a simple globe with the day's flashpoints -------
    gx, gy, gw, gh = mx, y, 260, 170
    d.ellipse([gx, gy, gx + gw, gy + gh], outline=INK, width=3)
    d.ellipse([gx + 52, gy + 8, gx + gw - 52, gy + gh - 8], outline=GREY, width=1)
    d.line([(gx, gy + gh // 2), (gx + gw, gy + gh // 2)], fill=GREY, width=1)
    d.line([(gx + gw // 2, gy), (gx + gw // 2, gy + gh)], fill=GREY, width=1)
    spots = [(gx + 146, gy + 74), (gx + 84, gy + 42), (gx + 196, gy + 64),
             (gx + 182, gy + 112), (gx + 52, gy + 114)]
    for sx, sy in spots:
        d.ellipse([sx - 6, sy - 6, sx + 6, sy + 6], fill=RED, outline=INK, width=1)
    cy = gy + gh + 10
    for line in wrap(d, "FLASHPOINTS: GULF \u2022 POLAND \u2022 UKRAINE \u2022 SHENZHEN \u2022 PERU",
                     font(SANS_B, 12), gw):
        d.text((gx, cy), line, font=font(SANS_B, 12), fill=GREY)
        cy += 16

    # ---- Secondary stories, right of the globe -------------------------
    tx = mx + gw + 28
    tw = W - mx - tx
    y2 = y
    y2 = label(d, tx, y2, "EUROPE")
    y2 = para(d, tx, y2,
              "Russian missiles and a drone crash in Poland; Warsaw calls it a "
              "provocation. Russia hit Ukraine with 400 drones and 110 missiles "
              "in one of the war's largest attacks. Drones struck a Russian cargo "
              "ship in the Baltic; Finland tightens security.",
              font(SERIF_B, 20), tw, 25)
    y2 += 12
    y2 = label(d, tx, y2, "ASIA-PACIFIC")
    y2 = para(d, tx, y2,
              "Trump reaches Shenzhen for the APEC summit; a trilateral meeting "
              "with Xi and Putin is planned. He calls China's nuclear buildup "
              "\u201crapid and concerning\u201d. Zelensky calls Putin a "
              "\u201ckiller\u201d; Melania Trump pushes for ceasefires before "
              "Christmas.",
              font(SERIF, 19), tw, 24)

    # ---- Also today: two-column round-up --------------------------------
    y = max(y + gh + 34, y2 + 14)
    rule(d, mx, y, W - mx, 2)
    y += 12
    y = label(d, mx, y, "ALSO TODAY")

    def news_item(x, yy, w, tag, text):
        d.text((x, yy), tag, font=font(SANS_B, 16), fill=RED)
        yy += 20
        return para(d, x, yy, text, font(SERIF, 18), w, 21) + 6

    left_items = [
        ("PERU", "A magnitude 6.9 earthquake shakes the Andes."),
        ("MYANMAR", "France seeks UN Security Council action after Myanmar "
                    "rejects the ICJ genocide ruling."),
        ("CLIMATE", "COP31 talks deadlocked over fossil fuels; US stocks slide "
                    "into correction."),
    ]
    right_items = [
        ("EUROPE", "Estonia to close its border with Russia; Denmark accuses "
                   "Russia of plotting to assassinate a US-Ukrainian rapper."),
        ("MEXICO", "A cartel leader's arrest sparks deadly violence in "
                   "Sinaloa; 11 killed."),
    ]
    ly = y
    for tag, text in left_items:
        ly = news_item(mx, ly, 448, tag, text)
    ry = y
    for tag, text in right_items:
        ry = news_item(mx + 472, ry, 460, tag, text)

    # ---- Footer ----------------------------------------------------------
    rule(d, mx, H - 56, W - mx, 2)
    d.text((W // 2, H - 44), "Compiled from wire reports  \u2022  Sunday 22 November 2026",
           font=font(SANS, 15), fill=GREY, anchor="ma")

    img.save(OUT, format="PNG", optimize=True)
    print("wrote", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
