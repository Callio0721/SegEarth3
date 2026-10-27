from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle, PathPatch
from matplotlib.path import Path as MPath
from matplotlib.lines import Line2D

ROOT = Path(r"D:\论文\9.27论文\中文论文\绘图")
ASSETS = ROOT / "role_functional_text_skeleton" / "assets"
OUT = ROOT / "model_structure_v1"
OUT.mkdir(parents=True, exist_ok=True)

plt.rcParams.update({
    "font.family": "Times New Roman",
    "mathtext.fontset": "stix",
    "font.size": 10,
})

W, H = 1900, 1000
fig = plt.figure(figsize=(19, 10), dpi=150, facecolor="white")
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, W)
ax.set_ylim(0, H)
ax.axis("off")

NAVY = "#17324D"
SLATE = "#40566B"
GREY = "#6F7C89"
PURPLE = "#7256A3"
PURPLE_F = "#F0E8FB"
TEAL = "#2E7D78"
TEAL_F = "#DDF3EF"
ORANGE = "#C8783E"
ORANGE_F = "#FDE9D9"
BLUE_F = "#E7EFF9"
PALE_BLUE = "#F5F8FC"
WHITE = "#FFFFFF"


def box(x, y, w, h, fc=WHITE, ec=NAVY, lw=1.5, r=12, ls="-", z=2, alpha=1.0):
    p = FancyBboxPatch((x, y), w, h,
                       boxstyle=f"round,pad=0,rounding_size={r}",
                       linewidth=lw, edgecolor=ec, facecolor=fc,
                       linestyle=ls, zorder=z, alpha=alpha)
    ax.add_patch(p)


def txt(x, y, s, size=10, color=NAVY, weight="normal", ha="left", va="center", z=6, rotation=0):
    ax.text(x, y, s, fontsize=size, color=color, fontweight=weight,
            ha=ha, va=va, zorder=z, rotation=rotation)


def arrow(x1, y1, x2, y2, color=SLATE, lw=1.6, ls="-", z=4, rad=0.0, mutation=11):
    a = FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>",
                        mutation_scale=mutation, linewidth=lw,
                        color=color, linestyle=ls, zorder=z,
                        connectionstyle=f"arc3,rad={rad}",
                        shrinkA=1, shrinkB=1)
    ax.add_patch(a)


def polyline(points, color=SLATE, lw=1.4, ls="-", z=4):
    xs, ys = zip(*points)
    ax.add_line(Line2D(xs, ys, color=color, linewidth=lw, linestyle=ls,
                       zorder=z, solid_capstyle="round", solid_joinstyle="round"))


def pill(x, y, w, h, s, fc, ec, size=8.5, weight="normal"):
    box(x, y, w, h, fc=fc, ec=ec, lw=1.0, r=h/2, z=3)
    txt(x+w/2, y+h/2, s, size=size, color=ec, weight=weight, ha="center")


def image_thumb(path, x, y, w, h, ec="#AAB6C2", lw=1.0):
    img = plt.imread(path)
    ax.imshow(img, extent=(x, x+w, y, y+h), aspect="auto", origin="upper", zorder=3)
    ax.add_patch(Rectangle((x, y), w, h, fill=False, edgecolor=ec, linewidth=lw, zorder=4))


def role_icon(role, x, y, w=54, h=30):
    if role == "P":
        pts = [(x+5, y+10), (x+18, y+22), (x+32, y+10), (x+46, y+22), (x+52, y+12)]
        for a, b in zip(pts[:-1], pts[1:]):
            ax.plot([a[0], b[0]], [a[1], b[1]], color=PURPLE, lw=1.5, zorder=5)
        for px, py in pts:
            ax.scatter([px], [py], s=26, color=PURPLE, zorder=6)
    elif role == "S":
        verts = [(x+2, y+8), (x+18, y+26), (x+34, y+26), (x+52, y+8)]
        codes = [MPath.MOVETO, MPath.CURVE4, MPath.CURVE4, MPath.CURVE4]
        path = MPath(verts, codes)
        ax.add_patch(PathPatch(path, fill=False, lw=6, edgecolor=TEAL, zorder=4))
        ax.add_patch(PathPatch(path, fill=False, lw=2.2, edgecolor="#D9D27B", linestyle=(0, (5, 4)), zorder=5))
    else:
        verts1 = [(x+2, y+14), (x+20, y+21), (x+24, y+12)]
        verts2 = [(x+31, y+10), (x+38, y+20), (x+52, y+26)]
        ax.add_patch(PathPatch(MPath(verts1, [MPath.MOVETO, MPath.CURVE3, MPath.CURVE3]),
                               fill=False, lw=6, edgecolor=ORANGE, zorder=4))
        ax.add_patch(PathPatch(MPath(verts2, [MPath.MOVETO, MPath.CURVE3, MPath.CURVE3]),
                               fill=False, lw=6, edgecolor=ORANGE, zorder=4))
        ax.plot([x+27.5, x+27.5], [y+3, y+28], color=SLATE, lw=1.2, linestyle=(0, (4, 3)), zorder=5)


# ==================== Panel (a) ====================
box(20, 510, 1860, 470, fc="white", ec=NAVY, lw=1.6, r=22, ls=(0, (5, 4)))
txt(50, 948, "(a) Role-Functional Text", size=20, weight="bold")

# Selected role profile
txt(55, 906, "Selected role profile", size=13, weight="bold")
txt(55, 885, "one configuration shared by every view", size=9, color=GREY)

# anchor card
box(55, 828, 360, 46, fc=BLUE_F, ec="#7996B4", lw=1.2, r=9)
txt(72, 851, "Official anchor", size=9, color=SLATE, weight="bold")
txt(178, 851, r"road + official aliases", size=10.2, weight="bold")

role_rows = [
    ("P", "slot 1", "visible road / roadway", PURPLE_F, PURPLE, 757),
    ("S", "slot 2", "continuous paved road surface", TEAL_F, TEAL, 686),
    ("I", "slot 3", "connected road region", ORANGE_F, ORANGE, 615),
]
for role, slot, prompt, fill, edge, y in role_rows:
    box(55, y, 360, 46, fc=fill, ec=edge, lw=1.2, r=9)
    txt(72, y+23, role, size=11, color=edge, weight="bold")
    txt(94, y+23, slot, size=8.3, color=edge, weight="bold")
    txt(146, y+23, prompt, size=9.5, color=NAVY)
    role_icon(role, 356, y+8)

txt(55, 580, "slot 0 = anchor;  1/2/3 = selected candidate", size=8.4, color=GREY)
# small view input, abstract one view
image_thumb(ASSETS / "road_input4.png", 455, 548, 82, 55, ec="#AAB6C2")
txt(496, 530, r"view $X_v$", size=8.8, color=GREY, ha="center")
arrow(496, 603, 496, 640, color=SLATE, lw=1.5)

# prompt arrows into SAM3
for y in [851, 780, 709, 638]:
    arrow(415, y, 445, y, color=SLATE, lw=1.3, mutation=9)

# SAM3 grounding
box(445, 640, 300, 260, fc="#EAF0F8", ec=NAVY, lw=1.8, r=14)
txt(595, 875, "Frozen SAM3", size=16, weight="bold", ha="center")
txt(595, 847, "complete multimodal grounding", size=9.4, color=SLATE, ha="center")
txt(595, 823, "image features + text condition", size=8.5, color=GREY, ha="center")
txt(595, 790, "anchor and each selected prompt", size=8.8, color=SLATE, ha="center")
txt(595, 767, "produce their own (p, S, I)", size=8.8, color=SLATE, ha="center")
pill(505, 720, 180, 24, "frozen / no training", "#D6E1EF", NAVY, size=8.2, weight="bold")
txt(595, 686, "each prompt → one grounding pass", size=8.0, color=GREY, ha="center")
# lock
ax.add_patch(Rectangle((723, 884), 10, 7, facecolor=NAVY, edgecolor=NAVY, zorder=6))
ax.add_patch(FancyBboxPatch((724, 889), 8, 8, boxstyle="round,pad=0,rounding_size=3",
                            facecolor="none", edgecolor=NAVY, lw=1.2, zorder=6))

# readouts
box(790, 835, 265, 65, fc="#F8FAFC", ec="#8B9BAA", lw=1.1, r=10)
txt(804, 880, "Anchor readout", size=9.7, weight="bold")
for i, lab in enumerate([r"$p_A$", r"$S_A$", r"$I_A$"]):
    x0 = 808 + i*78
    box(x0, 844, 62, 23, fc="#E8EDF3", ec="#8B9BAA", lw=0.9, r=5)
    txt(x0+31, 855.5, lab, size=8.8, ha="center")

box(790, 610, 265, 205, fc="#FBFCFD", ec="#A9B5C0", lw=1.1, r=12)
txt(804, 792, "Candidate readouts", size=9.7, weight="bold")
txt(804, 775, "only the aligned role is used", size=8.0, color=GREY)
cand_y = {"P": 721, "S": 670, "I": 619}
for role, fill, edge, y in [(r[0], r[3], r[4], cand_y[r[0]]) for r in role_rows]:
    txt(806, y+11, role, size=9.4, color=edge, weight="bold")
    cols = [PURPLE, TEAL, ORANGE]
    for j, col in enumerate(cols):
        active = (role == "P" and j == 0) or (role == "S" and j == 1) or (role == "I" and j == 2)
        cx = 832 + j*59
        box(cx, y, 50, 22, fc=(fill if active else "#F1F3F5"),
            ec=(col if active else "#C8CFD6"), lw=(1.1 if active else 0.8), r=5, z=4)
        txt(cx+25, y+11, ["p", "S", "I"][j], size=8.4,
            color=(col if active else "#A6AFB8"), weight=("bold" if active else "normal"), ha="center")

# arrows from grounding to readout blocks
arrow(745, 867, 790, 867, color=SLATE, lw=1.4, mutation=9)
arrow(745, 720, 790, 720, color=SLATE, lw=1.4, mutation=9)
arrow(745, 670, 790, 670, color=SLATE, lw=1.4, mutation=9)
arrow(745, 620, 790, 620, color=SLATE, lw=1.4, mutation=9)

# bounded correction
box(1080, 570, 310, 350, fc="#FBFCFD", ec="#A9B5C0", lw=1.3, r=14)
txt(1235, 892, "Bounded role correction", size=11.2, weight="bold", ha="center")
txt(1235, 868, r"$\mathcal{B}(a_A,a_\pi)=\mathrm{clip}_{[0,1]}(a_A+\alpha\,\mathrm{clip}(a_\pi-a_A,-\tau,\tau))$", size=7.8, color=SLATE, ha="center")
txt(1235, 847, r"$\alpha=0.5,\ \tau=0.25$   →   max change $\alpha\tau=0.125$", size=8.2, color=GREY, ha="center")

lane_specs = [
    ("P", 800, r"$\tilde p=\mathcal{B}(p_A,p_{\pi P})$", PURPLE_F, PURPLE),
    ("S", 735, r"$\tilde S=\mathcal{B}(S_A,S_{\pi S})$", TEAL_F, TEAL),
    ("I", 670, r"$\tilde I=\mathcal{B}(I_A^{\tilde p},I_{\pi I}^{\tilde p})$", ORANGE_F, ORANGE),
]
for role, y, formula, fill, edge in lane_specs:
    box(1100, y-20, 270, 42, fc=fill, ec=edge, lw=1.1, r=8)
    txt(1115, y+1, role, size=10, color=edge, weight="bold")
    txt(1142, y+1, formula, size=9.0, color=NAVY)
# P -> I recoupling
arrow(1350, 796, 1350, 678, color=PURPLE, lw=2.0, rad=0.0)
txt(1362, 744, "P→I", size=8.0, color=PURPLE, weight="bold", rotation=90, ha="center")
txt(1362, 734, "rebuild", size=7.2, color=PURPLE, rotation=90, ha="center")
txt(1235, 610, "query admission + instance amplitude", size=8.0, color=PURPLE, ha="center")
# arrows from readouts to correction lanes
arrow(1055, 720, 1100, 800, color=SLATE, lw=1.2, rad=-0.2, mutation=8)
arrow(1055, 670, 1100, 735, color=SLATE, lw=1.2, mutation=8)
arrow(1055, 619, 1100, 670, color=SLATE, lw=1.2, rad=0.2, mutation=8)

# fusion and alias guard
arrow(1390, 735, 1425, 735, color=SLATE, lw=1.7)
box(1425, 690, 165, 130, fc="#EAF0F8", ec=NAVY, lw=1.4, r=12)
txt(1507, 792, "Native fusion", size=9.4, weight="bold", ha="center")
txt(1507, 758, r"$F_\pi=\tilde p\,\max(\tilde S,\tilde I)$", size=9.0, color=NAVY, ha="center")
txt(1507, 722, "one class field", size=8.0, color=GREY, ha="center")
arrow(1590, 735, 1615, 735, color=SLATE, lw=1.4)
box(1615, 680, 230, 150, fc="#F8FAFC", ec="#8B9BAA", lw=1.2, r=10)
txt(1730, 803, "Official alias guard", size=9.5, weight="bold", ha="center")
txt(1730, 772, r"$G_{v,\pi}=\mathrm{clip}(G_o+F_\pi-F_A)$", size=8.2, ha="center")
txt(1730, 733, r"$G_{v,\pi}$", size=13, color=NAVY, ha="center")
txt(1730, 706, "zero slots → $G_o$", size=7.5, color=GREY, ha="center")

# ==================== Panel (b) ====================
box(20, 20, 1860, 470, fc="white", ec=NAVY, lw=1.6, r=22, ls=(0, (5, 4)))
txt(50, 455, "(b) Joint Role–View application on Local and Context observations", size=18, weight="bold")

# Input image and view construction
image_thumb(ASSETS / "road_input4.png", 55, 247, 105, 78, ec="#96A6B4")
txt(107, 228, "Input image", size=9.5, color=SLATE, ha="center")

box(205, 318, 300, 100, fc="#F5FBFC", ec=TEAL, lw=1.2, r=12)
image_thumb(ASSETS / "road_local4.png", 220, 333, 122, 70, ec="#8BA4A0")
txt(362, 382, "Local / native view", size=11, weight="bold")
txt(362, 359, "higher sampling density", size=8.0, color=GREY)

box(205, 165, 300, 100, fc="#FFF9F4", ec=ORANGE, lw=1.2, r=12)
image_thumb(ASSETS / "road_context4.png", 220, 180, 122, 70, ec="#C7A17F")
txt(362, 229, "Context / wider view", size=11, weight="bold")
txt(362, 206, "larger spatial layout", size=8.0, color=GREY)

# branch input
polyline([(160, 286), (183, 286), (183, 368), (205, 368)], color=SLATE, lw=1.5)
arrow(183, 368, 205, 368, color=SLATE, lw=1.5)
polyline([(160, 286), (183, 286), (183, 215), (205, 215)], color=SLATE, lw=1.5)
arrow(183, 215, 205, 215, color=SLATE, lw=1.5)

# shared role profile strip
box(610, 402, 780, 38, fc="#E9F1FA", ec="#6685A6", lw=1.2, r=12)
txt(1000, 421, r"shared profile $\pi$:  P = slot 1   |   S = slot 2   |   I = slot 3      (0 = anchor)", size=9.4, color=NAVY, ha="center", weight="bold")
# dashed profile fanout: local
arrow(1000, 402, 1000, 390, color="#6685A6", lw=1.3, ls=(0, (3, 3)), mutation=9)
# dashed profile fanout: context, routed around the left
polyline([(1390, 421), (1420, 421), (1420, 245), (1400, 245)], color="#6685A6", lw=1.3, ls=(0, (3, 3)))
arrow(1420, 245, 1400, 245, color="#6685A6", lw=1.3, ls=(0, (3, 3)), mutation=9)

# local lane
box(620, 295, 780, 95, fc="#F4FBFA", ec=TEAL, lw=1.2, r=12)
text_y = 342
box(638, 316, 175, 52, fc="#EEF3F7", ec="#8194A6", lw=1.0, r=8)
txt(725, 350, "Frozen SAM3", size=10, weight="bold", ha="center")
txt(725, 332, "full grounding", size=7.3, color=GREY, ha="center")
arrow(813, text_y, 850, text_y, color=SLATE, lw=1.3, mutation=9)
box(850, 312, 220, 60, fc="#EAF1FA", ec="#6685A6", lw=1.0, r=8)
txt(960, 350, r"bounded correction $\mathcal{R}_\pi$", size=9.5, weight="bold", ha="center")
txt(960, 332, r"$\mathcal{B}(a_A,a_\pi)$ + P→I", size=8.5, color=SLATE, ha="center")
arrow(1070, text_y, 1108, text_y, color=SLATE, lw=1.3, mutation=9)
box(1108, 316, 160, 52, fc="#F8FAFC", ec=TEAL, lw=1.0, r=8)
txt(1188, 342, r"$G_{L,\pi}$", size=11, color=TEAL, ha="center", weight="bold")
arrow(480, 368, 620, 368, color=SLATE, lw=1.3, mutation=9)

# context lane
box(620, 150, 780, 95, fc="#FFF8F3", ec=ORANGE, lw=1.2, r=12)
text_y2 = 197
box(638, 171, 175, 52, fc="#EEF3F7", ec="#8194A6", lw=1.0, r=8)
txt(725, 205, "Frozen SAM3", size=10, weight="bold", ha="center")
txt(725, 187, "full grounding", size=7.3, color=GREY, ha="center")
arrow(813, text_y2, 850, text_y2, color=SLATE, lw=1.3, mutation=9)
box(850, 167, 220, 60, fc="#EAF1FA", ec="#6685A6", lw=1.0, r=8)
txt(960, 205, r"bounded correction $\mathcal{R}_\pi$", size=9.5, weight="bold", ha="center")
txt(960, 187, r"$\mathcal{B}(a_A,a_\pi)$ + P→I", size=8.5, color=SLATE, ha="center")
arrow(1070, text_y2, 1108, text_y2, color=SLATE, lw=1.3, mutation=9)
box(1108, 171, 160, 52, fc="#F8FAFC", ec=ORANGE, lw=1.0, r=8)
txt(1188, 197, r"$G_{G,\pi}$", size=11, color=ORANGE, ha="center", weight="bold")
arrow(480, 215, 620, 215, color=SLATE, lw=1.3, mutation=9)

# fusion / decision
arrow(1268, 342, 1440, 290, color=SLATE, lw=1.5)
arrow(1268, 197, 1440, 248, color=SLATE, lw=1.5)
box(1440, 205, 170, 130, fc="#E8F4F3", ec=TEAL, lw=1.3, r=12)
txt(1525, 300, "Aligned fusion", size=9.5, weight="bold", ha="center")
txt(1525, 266, r"$\Psi_\omega$", size=13, color=TEAL, ha="center")
txt(1525, 232, "max / power / logit", size=7.6, color=SLATE, ha="center")
arrow(1610, 270, 1645, 270, color=SLATE, lw=1.5)
box(1645, 235, 190, 70, fc=NAVY, ec=NAVY, lw=1.2, r=12)
txt(1740, 280, "argmax + threshold", size=9.0, color=WHITE, weight="bold", ha="center")
txt(1740, 253, r"$\hat{Y}(x)$", size=11.5, color=WHITE, ha="center")

# legend
ax.add_line(Line2D([55, 95], [55, 55], color=SLATE, lw=1.5, zorder=5))
ax.add_patch(FancyArrowPatch((85, 55), (95, 55), arrowstyle="-|>", mutation_scale=8, lw=1.5, color=SLATE, zorder=5))
txt(105, 55, "data / computation", size=8.0, color=GREY)
ax.add_line(Line2D([255, 295], [55, 55], color="#6685A6", lw=1.3, linestyle=(0, (3, 3)), zorder=5))
ax.add_patch(FancyArrowPatch((285, 55), (295, 55), arrowstyle="-|>", mutation_scale=8, lw=1.3, color="#6685A6", zorder=5))
txt(305, 55, "shared configuration", size=8.0, color=GREY)
txt(1540, 55, "same profile; evidence computed separately per view", size=8.5, color=GREY)

fig.savefig(OUT / "model_structure_v1.svg", bbox_inches="tight", pad_inches=0.08, facecolor="white")
fig.savefig(OUT / "model_structure_v1.png", dpi=180, bbox_inches="tight", pad_inches=0.08, facecolor="white")
plt.close(fig)
print(OUT / "model_structure_v1.png")