from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

src = Path(r"C:\Users\ZHANGB~1\AppData\Local\Temp\codex-clipboard-049bebe8-6df2-40c1-8ad6-f1fd0c25d3e2.png")
out = Path(r"D:\论文\9.27论文\中文论文\绘图\role_functional_text_skeleton")
out.mkdir(parents=True, exist_ok=True)

base = Image.open(src).convert("RGBA")
W, H = base.size
overlay = Image.new("RGBA", (W, H), (255, 255, 255, 0))
d = ImageDraw.Draw(overlay)

NAVY = (22, 50, 79, 255)
SLATE = (60, 82, 104, 255)
GREY = (110, 122, 134, 255)
PURPLE = (114, 87, 163, 255)
TEAL = (49, 125, 121, 255)
ORANGE = (198, 120, 63, 255)
BLUE_F = (231, 239, 249, 238)
TEAL_F = (231, 247, 245, 238)
ORANGE_F = (255, 245, 236, 238)
PANEL_F = (255, 255, 255, 210)
WHITE = (255, 255, 255, 255)

font_path = r"C:\Windows\Fonts\times.ttf"
if not Path(font_path).exists():
    font_path = r"C:\Windows\Fonts\arial.ttf"

def font(size, bold=False):
    p = r"C:\Windows\Fonts\timesbd.ttf" if bold and Path(r"C:\Windows\Fonts\timesbd.ttf").exists() else font_path
    return ImageFont.truetype(p, size)

def rounded(box, fill, outline, width=3, radius=22, dash=False):
    if not dash:
        d.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)
    else:
        x1, y1, x2, y2 = box
        # use matplotlib-like dashed rounded border approximated by dashed long edges
        r = radius
        seg = 14
        gap = 9
        # straight edges
        for x in range(x1 + r, x2 - r, seg + gap):
            d.line((x, y1, min(x + seg, x2 - r), y1), fill=outline, width=width)
            d.line((x, y2, min(x + seg, x2 - r), y2), fill=outline, width=width)
        for y in range(y1 + r, y2 - r, seg + gap):
            d.line((x1, y, x1, min(y + seg, y2 - r)), fill=outline, width=width)
            d.line((x2, y, x2, min(y + seg, y2 - r)), fill=outline, width=width)
        d.arc((x1, y1, x1 + 2*r, y1 + 2*r), 180, 270, fill=outline, width=width)
        d.arc((x2 - 2*r, y1, x2, y1 + 2*r), 270, 360, fill=outline, width=width)
        d.arc((x1, y2 - 2*r, x1 + 2*r, y2), 90, 180, fill=outline, width=width)
        d.arc((x2 - 2*r, y2 - 2*r, x2, y2), 0, 90, fill=outline, width=width)

def text(x, y, s, size=30, fill=NAVY, anchor="la", bold=False):
    d.text((x, y), s, font=font(size, bold), fill=fill, anchor=anchor)

def arrow(start, end, fill=SLATE, width=4, head=14):
    d.line((start, end), fill=fill, width=width)
    x1, y1 = start
    x2, y2 = end
    import math
    ang = math.atan2(y2-y1, x2-x1)
    a1 = ang + math.pi*0.82
    a2 = ang - math.pi*0.82
    p1 = (x2 + head*math.cos(a1), y2 + head*math.sin(a1))
    p2 = (x2 + head*math.cos(a2), y2 + head*math.sin(a2))
    d.polygon([end, p1, p2], fill=fill)

def dashed_arrow(start, end, fill=SLATE, width=3, head=13):
    x1, y1 = start
    x2, y2 = end
    import math
    dist = math.hypot(x2-x1, y2-y1)
    if dist == 0:
        return
    ux, uy = (x2-x1)/dist, (y2-y1)/dist
    pos = 0
    dash, gap = 13, 9
    while pos < dist - 2:
        a = (x1 + ux*pos, y1 + uy*pos)
        b = (x1 + ux*min(pos+dash, dist-2), y1 + uy*min(pos+dash, dist-2))
        d.line((a, b), fill=fill, width=width)
        pos += dash + gap
    arrow((x2 - ux*head*0.2, y2 - uy*head*0.2), end, fill=fill, width=width, head=head)

# Extend the drawing into the blank right area as a new panel (c)
rounded((820, 350, 1955, 1075), PANEL_F, NAVY, width=4, radius=34, dash=True)
text(860, 365, "(c) Joint Role–View Composition", 46, fill=NAVY, bold=True)

# Role profile bus
rounded((980, 445, 1490, 525), BLUE_F, (102, 133, 166, 255), width=2, radius=20)
text(1235, 485, "Shared role profile  π = (P?, S?, I?)", 31, fill=NAVY, anchor="mm", bold=True)
# Connect the existing upper role arrows to the profile
# route profile handoff around the panel title
d.line((1735, 340, 1735, 485), fill=(102, 133, 166, 255), width=3)
d.line((1735, 485, 1490, 485), fill=(102, 133, 166, 255), width=3)
arrow((1520, 485), (1490, 485), fill=(102, 133, 166, 255), width=3, head=13)

# Local branch
rounded((880, 565, 1560, 715), TEAL_F, TEAL, width=3, radius=24)
text(915, 580, "Local / native view", 32, fill=TEAL, bold=True)
rounded((930, 620, 1120, 690), (238, 243, 248, 250), (120, 140, 158, 255), width=2, radius=14)
text(1025, 655, "Frozen SAM3", 28, fill=NAVY, anchor="mm", bold=True)
arrow((1120, 655), (1160, 655), fill=SLATE, width=4)
rounded((1160, 620, 1320, 690), (234, 242, 250, 250), (102, 133, 166, 255), width=2, radius=14)
text(1240, 655, "Rπ", 32, fill=NAVY, anchor="mm", bold=True)
arrow((1320, 655), (1360, 655), fill=SLATE, width=4)
rounded((1360, 620, 1545, 690), (245, 249, 252, 250), TEAL, width=2, radius=14)
text(1452, 655, "G_L,π", 32, fill=TEAL, anchor="mm", bold=True)
# connect existing local view to branch
dashed_arrow((716, 575), (880, 610), fill=TEAL, width=3, head=14)

# Context branch
rounded((880, 765, 1560, 915), ORANGE_F, ORANGE, width=3, radius=24)
text(915, 780, "Context / wider view", 32, fill=ORANGE, bold=True)
rounded((930, 820, 1120, 890), (238, 243, 248, 250), (120, 140, 158, 255), width=2, radius=14)
text(1025, 855, "Frozen SAM3", 28, fill=NAVY, anchor="mm", bold=True)
arrow((1120, 855), (1160, 855), fill=SLATE, width=4)
rounded((1160, 820, 1320, 890), (234, 242, 250, 250), (102, 133, 166, 255), width=2, radius=14)
text(1240, 855, "Rπ", 32, fill=NAVY, anchor="mm", bold=True)
arrow((1320, 855), (1360, 855), fill=SLATE, width=4)
rounded((1360, 820, 1545, 890), (255, 249, 244, 250), ORANGE, width=2, radius=14)
text(1452, 855, "G_G,π", 32, fill=ORANGE, anchor="mm", bold=True)
# connect existing context view to branch
dashed_arrow((716, 835), (880, 840), fill=ORANGE, width=3, head=14)

# profile to both branches
dashed_arrow((1120, 525), (1120, 565), fill=(102, 133, 166, 255), width=3, head=13)
dashed_arrow((1350, 525), (1350, 765), fill=(102, 133, 166, 255), width=3, head=13)

# fusion and decision
arrow((1545, 655), (1605, 720), fill=SLATE, width=4, head=14)
arrow((1545, 855), (1605, 800), fill=SLATE, width=4, head=14)
rounded((1605, 690, 1780, 830), TEAL_F, TEAL, width=3, radius=22)
text(1692, 735, "Aligned fusion", 28, fill=NAVY, anchor="mm", bold=True)
text(1692, 775, "Ψω", 34, fill=TEAL, anchor="mm", bold=True)
text(1692, 810, "max / power / logit", 20, fill=GREY, anchor="mm")
arrow((1780, 760), (1815, 760), fill=SLATE, width=4)
rounded((1815, 705, 1932, 815), NAVY, NAVY, width=2, radius=18)
text(1873, 740, "argmax +", 22, fill=WHITE, anchor="mm", bold=True)
text(1873, 770, "threshold", 22, fill=WHITE, anchor="mm", bold=True)
text(1873, 800, "Ŷ", 26, fill=WHITE, anchor="mm", bold=True)

# Small explanatory notes, not too verbose
text(900, 955, "same profile and role operator in both views", 24, fill=GREY)
text(900, 990, "fuse aligned class-score fields; then apply the native decision", 24, fill=GREY)

# Key: top role outputs should become one profile, not four independent paths
# arrow from old role bus area to new panel title/profile is already represented by vertical arrow at x=1235

result = Image.alpha_composite(base, overlay).convert("RGB")
result.save(out / "next_step_annotation.png", quality=95)
print(out / "next_step_annotation.png")