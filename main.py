#!/usr/bin/env python3
"""THE MONDAY WORLD - front page for Monday 23 November 2026.

Pure Python stdlib (zlib + struct + math only). Draws a 1024x1024
newspaper front page summing up 23 November 2026 world news and
writes it to /output/entry.png. Fully deterministic: fixed layout,
fixed text, no randomness, no clock, no network.

Stories (verified 23 Nov 2026 from AFP / Reuters / AP / BBC wires):
 1 COP31 collapses in Antalya - no deal, fossil fuels dropped
 2 Russian cargo ship Sparta II ablaze off Finland after drone strike
 3 Russian drone hits Kyiv-region flats - 14 missing
 4 Java candy-factory fire - 7 body bags, about 50 missing
 5 24 civilians killed in fresh South Sudan violence
 6 Kim Jong Un: North Korea seeks security, not supremacy
 7 Nepal PM Balendra Shah meets PM Modi in New Delhi
 8 South Korea education minister quits in AI exam-cheating row
 9 India post a record 720 for 9 in the Wellington Test
10 Max Verstappen wins a chaotic Las Vegas Grand Prix
"""

import math
import os
import struct
import zlib

W, H = 1024, 1024

PAPER = (247, 243, 232)
INK = (22, 22, 22)
NAVY = (18, 36, 61)
NAVY_LT = (38, 62, 96)
RED = (178, 34, 34)
RED_DK = (140, 22, 22)
GOLD = (198, 158, 62)
SKY = (203, 226, 240)
SEA = (168, 205, 228)
LAND = (122, 158, 104)
LAND_DK = (96, 132, 84)
GREY = (120, 118, 110)
RULE = (180, 175, 160)
WHITE = (255, 255, 255)
SUN = (240, 184, 48)
FLAME = (232, 98, 28)
SMOKE = (150, 148, 142)

canvas = bytearray(W * H * 3)


def fill(c):
    row = bytes(c) * W
    for y in range(H):
        canvas[y * W * 3:(y + 1) * W * 3] = row


def px(x, y, c):
    if 0 <= x < W and 0 <= y < H:
        i = (y * W + x) * 3
        canvas[i] = c[0]
        canvas[i + 1] = c[1]
        canvas[i + 2] = c[2]


def rect(x, y, w, h, c):
    x0 = max(0, x)
    y0 = max(0, y)
    x1 = min(W, x + w)
    y1 = min(H, y + h)
    if x1 <= x0 or y1 <= y0:
        return
    row = bytes(c) * (x1 - x0)
    for yy in range(y0, y1):
        canvas[yy * W * 3 + x0 * 3:yy * W * 3 + x1 * 3] = row


def hline(x0, x1, y, c):
    if x1 < x0:
        x0, x1 = x1, x0
    rect(x0, y, x1 - x0 + 1, 1, c)


def vline(x, y0, y1, c):
    if y1 < y0:
        y0, y1 = y1, y0
    rect(x, y0, 1, y1 - y0 + 1, c)


def line(x0, y0, x1, y1, c):
    dx = abs(x1 - x0)
    dy = -abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx + dy
    while True:
        px(x0, y0, c)
        if x0 == x1 and y0 == y1:
            break
        e2 = 2 * err
        if e2 >= dy:
            err += dy
            x0 += sx
        if e2 <= dx:
            err += dx
            y0 += sy


def thick_line(x0, y0, x1, y1, t, c):
    for d in range(-(t // 2), t // 2 + 1):
        line(x0 + d, y0, x1 + d, y1, c)
        line(x0, y0 + d, x1, y1 + d, c)


def circle(cx, cy, r, c, fill=True):
    if fill:
        for dy in range(-r, r + 1):
            dx = math.isqrt(max(0, r * r - dy * dy))
            hline(cx - dx, cx + dx, cy + dy, c)
    else:
        steps = max(8, r * 6)
        for i in range(steps):
            a = 2.0 * math.pi * i / steps
            px(int(cx + r * math.cos(a)), int(cy + r * math.sin(a)), c)


def ring(cx, cy, r, t, c):
    for rr in range(r - t + 1, r + 1):
        circle(cx, cy, rr, c, fill=False)


def poly(points, c):
    if len(points) < 3:
        return
    ys = [p[1] for p in points]
    for y in range(max(0, min(ys)), min(H - 1, max(ys)) + 1):
        xs = []
        n = len(points)
        for i in range(n):
            x0, y0 = points[i]
            x1, y1 = points[(i + 1) % n]
            if (y0 <= y < y1) or (y1 <= y < y0):
                x = x0 + (y - y0) * (x1 - x0) / (y1 - y0)
                xs.append(x)
        xs.sort()
        for i in range(0, len(xs) - 1, 2):
            hline(int(xs[i]), int(xs[i + 1]), y, c)


def poly_outline(points, c):
    n = len(points)
    for i in range(n):
        x0, y0 = points[i]
        x1, y1 = points[(i + 1) % n]
        line(x0, y0, x1, y1, c)


# 5x7 bitmap font, uppercase only. '#' = on pixel.
FONT = {
    'A': ("01110", "10001", "10001", "11111", "10001", "10001", "10001"),
    'B': ("11110", "10001", "10001", "11110", "10001", "10001", "11110"),
    'C': ("01110", "10001", "10000", "10000", "10000", "10001", "01110"),
    'D': ("11110", "10001", "10001", "10001", "10001", "10001", "11110"),
    'E': ("11111", "10000", "10000", "11110", "10000", "10000", "11111"),
    'F': ("11111", "10000", "10000", "11110", "10000", "10000", "10000"),
    'G': ("01110", "10001", "10000", "10111", "10001", "10001", "01111"),
    'H': ("10001", "10001", "10001", "11111", "10001", "10001", "10001"),
    'I': ("01110", "00100", "00100", "00100", "00100", "00100", "01110"),
    'J': ("00111", "00010", "00010", "00010", "00010", "10010", "01100"),
    'K': ("10001", "10010", "10100", "11000", "10100", "10010", "10001"),
    'L': ("10000", "10000", "10000", "10000", "10000", "10000", "11111"),
    'M': ("10001", "11011", "10101", "10101", "10001", "10001", "10001"),
    'N': ("10001", "11001", "10101", "10011", "10001", "10001", "10001"),
    'O': ("01110", "10001", "10001", "10001", "10001", "10001", "01110"),
    'P': ("11110", "10001", "10001", "11110", "10000", "10000", "10000"),
    'Q': ("01110", "10001", "10001", "10001", "10101", "10010", "01101"),
    'R': ("11110", "10001", "10001", "11110", "10100", "10010", "10001"),
    'S': ("01111", "10000", "10000", "01110", "00001", "00001", "11110"),
    'T': ("11111", "00100", "00100", "00100", "00100", "00100", "00100"),
    'U': ("10001", "10001", "10001", "10001", "10001", "10001", "01110"),
    'V': ("10001", "10001", "10001", "10001", "10001", "01010", "00100"),
    'W': ("10001", "10001", "10001", "10101", "10101", "11011", "10001"),
    'X': ("10001", "10001", "01010", "00100", "01010", "10001", "10001"),
    'Y': ("10001", "10001", "01010", "00100", "00100", "00100", "00100"),
    'Z': ("11111", "00001", "00010", "00100", "01000", "10000", "11111"),
    '0': ("01110", "10001", "10011", "10101", "11001", "10001", "01110"),
    '1': ("00100", "01100", "00100", "00100", "00100", "00100", "01110"),
    '2': ("01110", "10001", "00001", "00110", "01000", "10000", "11111"),
    '3': ("11111", "00010", "00100", "00010", "00001", "10001", "01110"),
    '4': ("00010", "00110", "01010", "10010", "11111", "00010", "00010"),
    '5': ("11111", "10000", "11110", "00001", "00001", "10001", "01110"),
    '6': ("00110", "01000", "10000", "11110", "10001", "10001", "01110"),
    '7': ("11111", "00001", "00010", "00100", "01000", "01000", "01000"),
    '8': ("01110", "10001", "10001", "01110", "10001", "10001", "01110"),
    '9': ("01110", "10001", "10001", "01111", "00001", "00010", "01100"),
    ' ': ("00000", "00000", "00000", "00000", "00000", "00000", "00000"),
    '.': ("00000", "00000", "00000", "00000", "00000", "01100", "01100"),
    ',': ("00000", "00000", "00000", "00000", "00000", "01100", "00100"),
    '!': ("00100", "00100", "00100", "00100", "00100", "00000", "00100"),
    '?': ("01110", "10001", "00001", "00010", "00100", "00000", "00100"),
    '-': ("00000", "00000", "00000", "11111", "00000", "00000", "00000"),
    '/': ("00001", "00001", "00010", "00100", "01000", "10000", "10000"),
    '(': ("00010", "00100", "01000", "01000", "01000", "00100", "00010"),
    ')': ("01000", "00100", "00010", "00010", "00010", "00100", "01000"),
    ':': ("00000", "01100", "01100", "00000", "01100", "01100", "00000"),
    "'": ("00100", "00100", "01000", "00000", "00000", "00000", "00000"),
    '%': ("11001", "11010", "00010", "00100", "01000", "01011", "10011"),
    '&': ("01100", "10010", "10100", "01000", "10101", "10010", "01101"),
    '+': ("00000", "00100", "00100", "11111", "00100", "00100", "00000"),
    '=': ("00000", "00000", "11111", "00000", "11111", "00000", "00000"),
    '"': ("01010", "01010", "00000", "00000", "00000", "00000", "00000"),
    ';': ("00000", "01100", "01100", "00000", "01100", "00100", "01000"),
}


def text_w(s, scale):
    return len(s) * 6 * scale - scale


def draw_text(x, y, s, scale, c):
    cx = x
    for ch in s.upper():
        g = FONT.get(ch, FONT[' '])
        for r in range(7):
            row = g[r]
            for col in range(5):
                if row[col] == '1':
                    rect(cx + col * scale, y + r * scale, scale, scale, c)
        cx += 6 * scale
    return cx


def center_text(y, s, scale, c):
    draw_text((W - text_w(s, scale)) // 2, y, s, scale, c)


def wrap_lines(s, scale, max_w):
    max_chars = max(1, (max_w + scale) // (6 * scale))
    words = s.split(' ')
    lines = []
    cur = ''
    for word in words:
        trial = word if not cur else cur + ' ' + word
        if len(trial) <= max_chars:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


# ---------------- front page layout ----------------

STORIES = [
    # (number, headline, summary) -- stories 2..10, story 1 is the lead
    (2, "SHIP ABLAZE OFF FINLAND",
     "SPARTA II BURNS AFTER A DRONE STRIKE. ALL 16 CREW EVACUATED."),
    (3, "14 MISSING AFTER KYIV STRIKE",
     "A RUSSIAN DRONE HITS A FLAT BLOCK NEAR KYIV. ONE KILLED, 14 MISSING."),
    (4, "50 MISSING IN JAVA FACTORY FIRE",
     "SEVEN BODY BAGS RECOVERED AFTER A CANDY FACTORY BLAZE IN CIKANDE."),
    (5, "24 KILLED IN SOUTH SUDAN",
     "FRESH VIOLENCE KILLS 24 CIVILIANS, AFP REPORTS FROM JUBA."),
    (6, "KIM: SECURITY, NOT SUPREMACY",
     "NORTH KOREA SEEKS SECURITY, NOT SUPREMACY, ITS LEADER SAYS."),
    (7, "NEPAL AND INDIA TALK IN DELHI",
     "PM BALENDRA SHAH MEETS PM MODI ON A TWO-DAY STATE VISIT TO INDIA."),
    (8, "SEOUL MINISTER QUITS IN AI EXAM ROW",
     "SOUTH KOREA'S EDUCATION MINISTER RESIGNS OVER AN AI CHEATING SCANDAL."),
    (9, "INDIA SMASH RECORD 720 FOR 9",
     "INDIA POST A RECORD TOTAL IN THE WELLINGTON TEST AGAINST NEW ZEALAND."),
    (10, "VERSTAPPEN WINS IN LAS VEGAS",
     "MAX VERSTAPPEN TAKES A CHAOTIC LAS VEGAS GRAND PRIX AS THE FERRARIS CLASH."),
]

CONTINENTS = [
    [(70, 446), (150, 437), (235, 440), (255, 454), (210, 470),
     (170, 482), (120, 481), (80, 467)],                       # N America
    [(255, 430), (285, 428), (290, 440), (262, 442)],           # Greenland
    [(280, 475), (330, 470), (352, 485), (330, 515), (300, 518),
     (282, 493)],                                                # S America
    [(478, 434), (528, 431), (548, 442), (520, 449), (492, 448),
     (476, 442)],                                                # Europe
    [(486, 455), (556, 452), (576, 473), (556, 505), (520, 515),
     (494, 493), (482, 473)],                                    # Africa
    [(556, 433), (700, 428), (800, 434), (860, 448), (820, 467),
     (760, 475), (680, 473), (620, 464), (572, 452)],            # Asia
    [(790, 481), (806, 478), (812, 485), (796, 488)],            # SE Asia isles
    [(806, 490), (872, 487), (886, 500), (850, 511), (812, 505)],  # Australia
    [(838, 440), (852, 437), (856, 449), (842, 452)],            # Japan
    [(908, 505), (922, 502), (926, 514), (912, 515)],            # New Zealand
]

PINS = [
    (1, 612, 448),   # COP31, Antalya
    (2, 536, 426),   # Sparta II, Gulf of Finland
    (3, 552, 442),   # Kyiv
    (4, 800, 485),   # Java factory fire
    (5, 540, 482),   # South Sudan
    (6, 778, 440),   # North Korea
    (7, 668, 454),   # New Delhi
    (8, 806, 437),   # Seoul
    (9, 916, 509),   # Wellington
    (10, 108, 457),  # Las Vegas
]


def draw_pin(x, y, n):
    circle(x, y, 13, RED, fill=True)
    ring(x, y, 13, 2, WHITE)
    s = str(n)
    draw_text(x - text_w(s, 2) // 2, y - 7, s, 2, WHITE)


def draw_masthead():
    rect(0, 0, W, 138, NAVY)
    rect(0, 134, W, 4, GOLD)
    draw_text(132, 16, "THE MONDAY WORLD", 8, WHITE)
    draw_text(305, 88, "MONDAY 23 NOVEMBER 2026", 3, GOLD)
    rect(24, 150, 976, 2, RULE)
    center_text(160, "CLIMATE  -  WAR  -  DISASTER  -  DIPLOMACY  -  SPORT",
                2, NAVY_LT)


def draw_hero(x0, y0, x1, y1):
    """Vector illustration: globe with a crack, burning ship, sun."""
    rect(x0, y0, x1 - x0, y1 - y0, SKY)
    rect(x0, y0, x1 - x0, 3, NAVY)
    rect(x0, y1 - 3, x1 - x0, 3, NAVY)
    rect(x0, y0, 3, y1 - y0, NAVY)
    rect(x1 - 3, y0, 3, y1 - y0, NAVY)
    # sun with rays
    sx, sy = x1 - 52, y0 + 34
    for ang in range(0, 360, 30):
        a = math.radians(ang)
        line(int(sx + 20 * math.cos(a)), int(sy + 20 * math.sin(a)),
             int(sx + 30 * math.cos(a)), int(sy + 30 * math.sin(a)), SUN)
    circle(sx, sy, 17, SUN, fill=True)
    circle(sx, sy, 17, SUN, fill=False)
    # globe
    gx, gy, gr = (x0 + x1) // 2 - 30, (y0 + y1) // 2 - 8, 62
    circle(gx, gy, gr, NAVY_LT, fill=True)
    circle(gx, gy, gr - 3, SEA, fill=True)
    poly([(gx - 42, gy - 18), (gx - 18, gy - 30), (gx - 2, gy - 12),
          (gx - 26, gy + 2), (gx - 44, gy + 2)], LAND)
    poly([(gx + 8, gy - 34), (gx + 34, gy - 28), (gx + 40, gy - 6),
          (gx + 18, gy + 6), (gx + 2, gy - 12)], LAND)
    poly([(gx - 20, gy + 18), (gx + 6, gy + 14), (gx + 22, gy + 30),
          (gx - 6, gy + 40), (gx - 28, gy + 34)], LAND_DK)
    # latitude lines
    for dy, w in ((-30, 46), (0, 59), (30, 46)):
        hline(gx - w, gx + w, gy + dy, WHITE)
    # red crack across the globe
    crack = [(gx - 52, gy - 34), (gx - 30, gy - 14), (gx - 38, gy + 4),
             (gx - 12, gy + 12), (gx - 22, gy + 30), (gx + 4, gy + 44),
             (gx + 26, gy + 52)]
    for i in range(len(crack) - 1):
        thick_line(crack[i][0], crack[i][1], crack[i + 1][0],
                   crack[i + 1][1], 3, RED)
    # smoke puffs
    for cx, cy, r in ((x0 + 42, y0 + 96, 10), (x0 + 58, y0 + 84, 12),
                      (x0 + 76, y0 + 98, 9)):
        circle(cx, cy, r, SMOKE, fill=True)
    # burning ship, bottom left of the panel
    hx, hy = x0 + 30, y1 - 26
    poly([(hx, hy), (hx + 96, hy), (hx + 84, hy + 16), (hx + 12, hy + 16)],
         (90, 60, 44))
    rect(hx + 40, hy - 26, 5, 26, (90, 60, 44))
    rect(hx + 58, hy - 18, 26, 18, (120, 82, 58))
    for fx in (hx + 18, hx + 44, hx + 70):
        poly([(fx, hy - 6), (fx + 7, hy - 24), (fx + 14, hy - 6)], FLAME)
        poly([(fx + 4, hy - 6), (fx + 7, hy - 16), (fx + 10, hy - 6)], SUN)
    # waves
    for wy in (y1 - 8, y1 - 4):
        for wx in range(x0 + 8, x1 - 8, 26):
            line(wx, wy, wx + 12, wy, NAVY_LT)
            line(wx + 12, wy, wx + 18, wy - 3, NAVY_LT)


def draw_lead():
    rect(24, 184, 976, 2, INK)
    draw_text(32, 196, "1  CLIMATE - ANTALYA, TURKIYE", 2, RED)
    draw_text(32, 222, "COP31 COLLAPSES", 6, INK)
    draw_text(32, 272, "NO DEAL AS FINAL TEXT DROPS FOSSIL FUELS", 2, INK)
    body = ("NEARLY 200 NATIONS LEAVE THE LONGEST CLIMATE SUMMIT ON RECORD "
            "WITH NO AGREEMENT. THE EU REFUSED A PACT THAT NEVER NAMED "
            "COAL, OIL OR GAS.")
    y = 302
    for ln in wrap_lines(body, 2, 596):
        draw_text(32, y, ln, 2, INK)
        y += 20
    draw_hero(660, 192, 992, 360)
    draw_text(660, 366, "COP31 - BALTIC - JAVA", 2, NAVY_LT)
    rect(24, 388, 976, 2, INK)


def draw_map():
    rect(24, 400, 976, 128, (232, 240, 246))
    draw_text(36, 406, "WHERE IT HAPPENED", 2, NAVY)
    draw_text(700, 406, "TEN STORIES, ONE MONDAY", 2, GREY)
    for cont in CONTINENTS:
        poly(cont, LAND)
        poly_outline(cont, LAND_DK)
    for n, x, y in PINS:
        draw_pin(x, y, n)
    rect(24, 528, 976, 2, INK)


def draw_rows():
    y = 540
    for n, head, summ in STORIES:
        if n > 2:
            hline(82, 1000, y - 6, RULE)
        circle(52, y + 22, 17, RED, fill=True)
        ring(52, y + 22, 17, 2, WHITE)
        s = str(n)
        draw_text(52 - text_w(s, 2) // 2, y + 15, s, 2, WHITE)
        draw_text(82, y + 2, head, 2, INK)
        lines = wrap_lines(summ, 2, 918)
        draw_text(82, y + 22, lines[0] if lines else "", 2, GREY)
        y += 49
    rect(24, 972, 976, 2, INK)


def draw_footer():
    rect(0, 982, W, 42, NAVY)
    center_text(994, "SOURCES: AFP / REUTERS / AP / BBC", 2, WHITE)


# ---------------- PNG encoder ----------------

def chunk(tag, data):
    out = struct.pack(">I", len(data)) + tag + data
    out += struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)
    return out


def encode_png():
    raw = bytearray()
    for y in range(H):
        raw.append(0)
        raw += canvas[y * W * 3:(y + 1) * W * 3]
    ihdr = struct.pack(">IIBBBBB", W, H, 8, 2, 0, 0, 0)
    png = b"\x89PNG\r\n\x1a\n"
    png += chunk(b"IHDR", ihdr)
    png += chunk(b"IDAT", zlib.compress(bytes(raw), 9))
    png += chunk(b"IEND", b"")
    return png


def main():
    fill(PAPER)
    draw_masthead()
    draw_lead()
    draw_map()
    draw_rows()
    draw_footer()
    data = encode_png()
    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.png", "wb") as f:
        f.write(data)
    print("wrote /output/entry.png %d bytes" % len(data))


if __name__ == "__main__":
    main()
