# -*- coding: utf-8 -*-
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

SIZE = 3000
BG = (250, 246, 236)
NAVY = (18, 42, 62)
RED = (226, 68, 42)
RED_DARK = (181, 50, 32)
MUTED = (98, 109, 116)
LINE = (220, 213, 200)
WHITE = (255, 253, 247)


def font(size, bold=False):
    candidates = [
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc" if bold else "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/opentype/noto/NotoSansCJKsc-Bold.otf" if bold else "/usr/share/fonts/opentype/noto/NotoSansCJKsc-Regular.otf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for p in candidates:
        if Path(p).exists():
            return ImageFont.truetype(p, size=size)
    return ImageFont.load_default()


def center_text(draw, xy, text, fnt, fill):
    box = draw.textbbox((0, 0), text, font=fnt)
    w = box[2] - box[0]
    draw.text((xy[0] - w / 2, xy[1]), text, font=fnt, fill=fill)


def draw_lobster(draw):
    # Head and body
    draw.ellipse((1110, 450, 1890, 1230), fill=RED, outline=RED_DARK, width=18)
    draw.ellipse((1260, 1030, 1740, 1810), fill=RED, outline=RED_DARK, width=18)
    # Eyes
    draw.ellipse((1270, 650, 1395, 775), fill=WHITE)
    draw.ellipse((1605, 650, 1730, 775), fill=WHITE)
    draw.ellipse((1315, 688, 1365, 738), fill=NAVY)
    draw.ellipse((1635, 688, 1685, 738), fill=NAVY)
    # Smile
    draw.arc((1320, 710, 1680, 1040), 20, 160, fill=NAVY, width=24)
    # Antennae
    draw.arc((1010, 210, 1480, 740), 205, 300, fill=RED_DARK, width=24)
    draw.arc((1520, 210, 1990, 740), 240, 335, fill=RED_DARK, width=24)
    # Headphones
    draw.arc((1050, 260, 1950, 1110), 190, 350, fill=NAVY, width=70)
    draw.rounded_rectangle((1035, 580, 1205, 1040), radius=70, fill=NAVY)
    draw.rounded_rectangle((1795, 580, 1965, 1040), radius=70, fill=NAVY)
    # Arms/claws
    draw.line((1280, 1180, 900, 1520), fill=RED_DARK, width=70)
    draw.line((1720, 1180, 2100, 1520), fill=RED_DARK, width=70)
    draw.ellipse((650, 1320, 1050, 1740), fill=RED, outline=RED_DARK, width=18)
    draw.pieslice((590, 1270, 1110, 1790), 305, 55, fill=BG)
    draw.ellipse((1950, 1320, 2350, 1740), fill=RED, outline=RED_DARK, width=18)
    draw.pieslice((1890, 1270, 2410, 1790), 125, 235, fill=BG)
    # Legs
    for dx in (-1, 1):
        x0 = 1500 + dx * 160
        draw.line((x0, 1610, x0 + dx * 300, 1900), fill=RED_DARK, width=38)
        draw.line((x0, 1690, x0 + dx * 430, 1760), fill=RED_DARK, width=38)


def draw_newspaper(draw):
    box = (820, 1190, 2180, 2090)
    draw.rounded_rectangle(box, radius=35, fill=WHITE, outline=NAVY, width=14)
    center_text(draw, (1500, 1260), "DAILY BRIEF", font(120, True), NAVY)
    draw.line((930, 1430, 2070, 1430), fill=LINE, width=10)
    # text columns
    for y in range(1510, 1920, 75):
        draw.line((950, y, 1300, y), fill=MUTED, width=14)
        draw.line((1700, y, 2050, y), fill=MUTED, width=14)
    # simple rising market chart
    pts = [(1350, 1840), (1470, 1700), (1580, 1760), (1690, 1530)]
    draw.line(pts, fill=RED, width=28, joint="curve")
    for x, y in pts:
        draw.ellipse((x-18, y-18, x+18, y+18), fill=RED)
    draw.line((1330, 1900, 1740, 1900), fill=NAVY, width=10)


def draw_background_icons(draw):
    # faint line chart
    draw.line([(280, 820), (540, 680), (770, 760), (940, 520)], fill=(225, 217, 202), width=20)
    for x, y in [(280,820),(540,680),(770,760),(940,520)]:
        draw.ellipse((x-25,y-25,x+25,y+25), fill=(225,217,202))
    # globe
    draw.ellipse((2220, 380, 2670, 830), outline=(215, 207, 194), width=18)
    draw.arc((2310, 390, 2580, 820), 90, 270, fill=(215, 207, 194), width=14)
    draw.arc((2310, 390, 2580, 820), 270, 90, fill=(215, 207, 194), width=14)
    draw.line((2230, 605, 2660, 605), fill=(215, 207, 194), width=14)
    # AI chip
    draw.rounded_rectangle((290, 1830, 620, 2160), radius=45, fill=(238, 231, 218), outline=(215,207,194), width=12)
    center_text(draw, (455, 1910), "AI", font(115, True), NAVY)
    for i in range(5):
        y = 1870 + i * 60
        draw.line((250, y, 290, y), fill=(215,207,194), width=12)
        draw.line((620, y, 660, y), fill=(215,207,194), width=12)


def main():
    out = Path("podcast-cover.jpg")
    im = Image.new("RGB", (SIZE, SIZE), BG)
    draw = ImageDraw.Draw(im)
    draw_background_icons(draw)
    draw_lobster(draw)
    draw_newspaper(draw)
    center_text(draw, (1500, 2200), "龙虾日报", font(285, True), NAVY)
    center_text(draw, (1500, 2580), "AI、市场、中国与世界，每日重要信息简报", font(82), MUTED)
    im.save(out, "JPEG", quality=92, optimize=True, progressive=True)
    print(f"generated {out} ({out.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
