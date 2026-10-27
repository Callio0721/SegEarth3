from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle
from matplotlib.lines import Line2D

OUT = Path(r"D:\论文\9.27论文\中文论文\绘图\role_functional_text_skeleton")
OUT.mkdir(parents=True, exist_ok=True)

plt.rcParams.update({
    "font.family": "Times New Roman",
    "mathtext.fontset": "stix",
    "font.size": 10.5,
    "axes.linewidth": 0,
})

W, H = 1600, 900
fig = plt.figure(figsize=(16, 9), dpi=160, facecolor="white")
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, W)
ax.set_ylim(0, H)
ax.axis("off")

NAVY = "#16324F"
SLATE = "#31475D"
GREY = "#6F7B88"
LGREY = "#E9EEF3"
PURPLE = "#7257A3"
PURPLE_F = "#EEE7FA"
TEAL = "#317D79"
TEAL_F = "#DDF2EE"
ORANGE = "#C6783F"
ORANGE_F = "#FCE8D8"
BLUE_F = "#E7EEF9"
WHITE = "#FFFFFF"


def box(x, y, w, h, fc=WHITE, ec=NAVY, lw=1.6, r=10, ls="-", z=2, alpha=1.0):
    patch = FancyBboxPatch(
        (x, y), w, h,
        boxstyle=f"round,pad=0.0,rounding_size={r}",
        linewidth=lw, edgecolor=ec, facecolor=fc,
        linestyle=ls, zorder=z, alpha=alpha,
    )
    ax.add_patch(patch)
    return patch


def txt(x, y, s, size=10.5, color=NAVY, weight="normal", ha="left", va="center", z=5, **kwargs):
    ax.text(x, y, s, fontsize=size, color=color, fontweight=weight,
            ha=ha, va=va, zorder=z, **kwargs)


def arrow(x1, y1, x2, y2, color=SLATE, lw=1.8, style="-|>", ls="-", rad=0.0, z=4, mutation=12):
    a = FancyArrowPatch(
        (x1, y1), (x2, y2),
        arrowstyle=style, mutation_scale=mutation,
        linewidth=lw, color=color, linestyle=ls,
        connectionstyle=f"arc3,rad={rad}", zorder=z,
        shrinkA=2, shrinkB=2,
    )
    ax.add_patch(a)
    return a


def line(points, color=SLATE, lw=1.5, ls="-", z=4):
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    ax.add_line(Line2D(xs, ys, color=color, linewidth=lw, linestyle=ls, zorder=z,
                       solid_capstyle="round", solid_joinstyle="round"))


def pill(x, y, w, h, label, fc, ec, size=9.5, weight="normal"):
    box(x, y, w, h, fc=fc, ec=ec, lw=1.2, r=h/2, z=3)
    txt(x + w/2, y + h/2, label, size=size, color=ec, weight=weight, ha="center")


def image_placeholder(x, y, w, h, label):
    box(x, y, w, h, fc="#F4F6F8", ec="#AEB8C2", lw=1.2, r=4, z=3)
    # simple landscape glyph
    ax.plot([x+8, x+w-8], [y+h*0.38, y+h*0.62], color="#9BA9B6", lw=1.0, zorder=4)
    ax.plot([x+8, x+w-8], [y+h*0.62, y+h*0.38], color="#9BA9B6", lw=1.0, zorder=4)
    ax.plot([x+w*0.38, x+w*0.56, x+w*0.68], [y+h*0.36, y+h*0.52, y+h*0.40], color="#9BA9B6", lw=1.2, zorder=4)
    txt(x+w/2, y+10, label, size=8.5, color=GREY, ha="center")


# ============ Panel A ============
box(20, 480, 1560, 400, fc="white", ec=NAVY, lw=1.6, r=18, ls=(0, (5, 4)))
txt(50, 850, "(a) Role-Functional Text", size=18, weight="bold")

# Input group
box(45, 540, 315, 285, fc="#FBFCFD", ec="#A8B4C0", lw=1.2, r=14, ls=(0, (3, 3)), alpha=0.75)

# image + official anchor
image_placeholder(60, 737, 82, 68, "Image X")
box(158, 744, 185, 55, fc=BLUE_F, ec="#7E9AB8", lw=1.2, r=8)
txt(250, 772, "road + official aliases", size=10.2, weight="bold", ha="center")
txt(250, 753, "official ontology anchor", size=8.2, color=GREY, ha="center")

# role library
txt(60, 705, "Role candidate library", size=11, weight="bold")
roles = [
    ("P", "visible road / roadway", PURPLE_F, PURPLE, 630),
    ("S", "continuous paved road surface", TEAL_F, TEAL, 575),
    ("I", "connected road region", ORANGE_F, ORANGE, 520),
]
for role, prompt, fill, edge, y in roles:
    box(58, y, 288, 43, fc=fill, ec=edge, lw=1.2, r=9)
    txt(70, y+21.5, role, size=10.5, color=edge, weight="bold")
    txt(92, y+21.5, prompt, size=9.4, color=NAVY)
txt(215, 705, "slot 0 = anchor", size=8.0, color=GREY)

# profile chip below panel A content
box(85, 489, 235, 30, fc="#EAF1FA", ec="#6685A6", lw=1.2, r=15)
txt(202.5, 504, r"Selected profile  $\pi=(P?,S?,I?)$   →  (b)", size=8.8, color=NAVY, ha="center")

# arrows into SAM3
arrow(360, 748, 405, 748, color=SLATE, lw=2.0)
arrow(360, 700, 405, 700, color=SLATE, lw=2.0)
arrow(360, 650, 405, 650, color=SLATE, lw=2.0)
arrow(360, 600, 405, 600, color=SLATE, lw=2.0)
txt(382, 812, "image + prompts", size=8.2, color=GREY, ha="center", rotation=0)

# Frozen SAM3
box(405, 555, 295, 245, fc="#EAF0F8", ec=NAVY, lw=2.0, r=14)
txt(552.5, 764, "Frozen SAM3", size=15, weight="bold", ha="center")
txt(552.5, 738, "complete multimodal grounding", size=10, color=SLATE, ha="center")
txt(552.5, 716, "image features  +  text condition", size=9.3, color=GREY, ha="center")
pill(465, 584, 175, 26, "FROZEN  /  NO TRAINING", "#D7E1EF", NAVY, size=8.3, weight="bold")
txt(552.5, 675, "Each prompt produces", size=8.8, color=SLATE, ha="center")
txt(552.5, 649, r"$(p,\;S,\;I)$ readouts", size=11, color=NAVY, ha="center")
# small lock glyph-like mark
ax.add_patch(Rectangle((685, 772), 10, 7, facecolor=NAVY, edgecolor=NAVY, zorder=5))
ax.add_patch(FancyBboxPatch((686, 777), 8, 8, boxstyle="round,pad=0,rounding_size=3",
                            facecolor="none", edgecolor=NAVY, lw=1.2, zorder=5))

# anchor readout
box(730, 733, 225, 68, fc="#F8FAFC", ec="#8A9AAA", lw=1.2, r=10)
txt(742, 780, "Anchor readout", size=10.5, weight="bold")
for i, (lab, col) in enumerate([(r"$p_A$", NAVY), (r"$S_A$", NAVY), (r"$I_A$", NAVY)]):
    x0 = 744 + i*66
    box(x0, 742, 54, 24, fc="#E8EDF3", ec="#8A9AAA", lw=1.0, r=6)
    txt(x0+27, 754, lab, size=9.3, color=col, ha="center")

# candidate readout card
box(730, 515, 225, 194, fc="#FBFCFD", ec="#A8B4C0", lw=1.2, r=12)
txt(742, 686, "Candidate outputs", size=10.2, weight="bold")
txt(742, 668, "only aligned readout is used", size=8.1, color=GREY)
cand_rows = [
    ("P", PURPLE_F, PURPLE, 620),
    ("S", TEAL_F, TEAL, 570),
    ("I", ORANGE_F, ORANGE, 520),
]
for role, fill, edge, y in cand_rows:
    txt(742, y+12, role, size=9.5, color=edge, weight="bold")
    # three readout cells
    cell_cols = [PURPLE, TEAL, ORANGE]
    for j, col in enumerate(cell_cols):
        active = (role == "P" and j == 0) or (role == "S" and j == 1) or (role == "I" and j == 2)
        cx = 770 + j*55
        box(cx, y, 47, 23, fc=(fill if active else "#F0F2F4"),
            ec=(col if active else "#C5CCD4"), lw=(1.2 if active else 0.9), r=5, z=4)
        lab = ["p", "S", "I"][j]
        txt(cx+23.5, y+11.5, lab, size=8.8,
            color=(col if active else "#A8B0B8"), weight=("bold" if active else "normal"), ha="center")

# arrows to correction
arrow(955, 766, 1000, 766, color=SLATE, lw=1.8)
arrow(955, 620, 1000, 620, color=SLATE, lw=1.8)
arrow(955, 570, 1000, 570, color=SLATE, lw=1.8)
arrow(955, 520, 1000, 520, color=SLATE, lw=1.8)

# correction card
box(1000, 495, 280, 300, fc="#FBFCFD", ec="#A8B4C0", lw=1.3, r=14)
txt(1140, 770, "Role-aligned bounded correction", size=10.5, weight="bold", ha="center")
txt(1140, 746, r"$\mathcal{B}(a,b)=\mathrm{clip}_{[0,1]}(a+\alpha\,\mathrm{clip}(b-a,-\tau,\tau))$", size=8.1, color=SLATE, ha="center")
# role lanes
lane_y = {"P": 687, "S": 615, "I": 543}
for role, fill, edge in [("P", PURPLE_F, PURPLE), ("S", TEAL_F, TEAL), ("I", ORANGE_F, ORANGE)]:
    y = lane_y[role]
    box(1020, y-18, 240, 38, fc=fill, ec=edge, lw=1.2, r=8)
    txt(1038, y+1, role, size=10.2, color=edge, weight="bold")
    if role == "P":
        formula = r"$\tilde p=\mathcal{B}(p_A,p_{\pi P})$"
    elif role == "S":
        formula = r"$\tilde S=\mathcal{B}(S_A,S_{\pi S})$"
    else:
        formula = r"$\tilde I=\mathcal{B}(I_A,I_{\pi I})$"
    txt(1068, y+1, formula, size=9.6, color=NAVY)
# P -> I coupling
arrow(1238, 665, 1238, 566, color=PURPLE, lw=2.0, rad=0.0)
txt(1248, 615, "P→I recoupling", size=8.2, color=PURPLE, weight="bold", rotation=90, ha="center")
txt(1248, 586, "admission + amplitude", size=7.4, color=PURPLE, rotation=90, ha="center")

# fusion
arrow(1280, 645, 1320, 645, color=SLATE, lw=2.0)
box(1320, 575, 105, 145, fc="#EAF0F8", ec=NAVY, lw=1.5, r=12)
txt(1372.5, 690, "Native fusion", size=9.2, weight="bold", ha="center")
txt(1372.5, 655, r"$F_\pi=$", size=9.4, color=NAVY, ha="center")
txt(1372.5, 632, r"$\tilde p\,\max(\tilde S,\tilde I)$", size=8.7, color=NAVY, ha="center")
txt(1372.5, 598, "one class field", size=7.8, color=GREY, ha="center")

# alias compensation and output
arrow(1425, 645, 1450, 645, color=SLATE, lw=1.8)
box(1450, 580, 105, 130, fc="#F8FAFC", ec="#8A9AAA", lw=1.2, r=10)
txt(1502.5, 684, "Alias guard", size=9.2, weight="bold", ha="center")
txt(1502.5, 650, r"$\mathrm{clip}($", size=8.3, ha="center")
txt(1502.5, 630, r"$G_o+F_\pi-F_A)$", size=7.9, ha="center")
txt(1502.5, 604, r"$G_{v,\pi}$", size=10.0, ha="center")
txt(1502.5, 588, "zero slots → $G_o$", size=7.1, color=GREY, ha="center")

# ============ Panel B ============
box(20, 20, 1560, 435, fc="white", ec=NAVY, lw=1.6, r=18, ls=(0, (5, 4)))
txt(50, 425, "(b) Joint Role–View Application", size=18, weight="bold")

# shared-profile bus in panel B
box(225, 354, 860, 40, fc="#EAF1FA", ec="#6685A6", lw=1.3, r=12)
txt(655, 374, r"Same selected profile  $\pi=(P?,S?,I?)$  is applied independently to both views", size=10.5, color=NAVY, ha="center", weight="bold")

# local/context cards
box(90, 145, 650, 172, fc="#F7FBFC", ec="#7BA4A1", lw=1.3, r=14)
box(860, 145, 650, 172, fc="#FFF9F4", ec="#C99671", lw=1.3, r=14)
image_placeholder(108, 199, 82, 76, "Local image")
image_placeholder(878, 199, 82, 76, "Context image")
txt(210, 297, "Local / native view", size=12.0, weight="bold")
txt(980, 297, "Context / wider view", size=12.0, weight="bold")
# mini computation paths inside the two view cards
for x0, score, edge in [(210, r"$G_{L,\pi}$", TEAL), (980, r"$G_{G,\pi}$", ORANGE)]:
    box(x0, 207, 120, 42, fc="#EEF3F7", ec="#8194A6", lw=1.1, r=8)
    txt(x0+60, 228, "Frozen SAM3", size=9.4, weight="bold", ha="center")
    txt(x0+60, 215, "full grounding", size=7.8, color=GREY, ha="center")
    arrow(x0+120, 228, x0+145, 228, color=SLATE, lw=1.5)
    box(x0+145, 207, 92, 42, fc="#EAF1FA", ec="#6685A6", lw=1.1, r=8)
    txt(x0+191, 228, r"$\mathcal{R}_\pi$", size=12.0, color=NAVY, ha="center")
    arrow(x0+237, 228, x0+262, 228, color=SLATE, lw=1.5)
    box(x0+262, 207, 128, 42, fc="#F8FAFC", ec=edge, lw=1.2, r=8)
    txt(x0+326, 228, score, size=11.0, color=edge, ha="center", weight="bold")
    txt(x0+326, 214, "class score", size=7.6, color=GREY, ha="center")
txt(210, 168, r"same $\pi$ and the same role operator $\mathcal{R}_\pi$", size=8.2, color=GREY)
txt(980, 168, r"same $\pi$ and the same role operator $\mathcal{R}_\pi$", size=8.2, color=GREY)

# profile to view arrows
arrow(390, 354, 390, 317, color="#6685A6", lw=1.5, ls=(0, (4, 4)))
arrow(1165, 354, 1165, 317, color="#6685A6", lw=1.5, ls=(0, (4, 4)))

# view outputs to fusion (orthogonal)
line([(415, 145), (415, 124), (620, 124), (620, 112)], color=SLATE, lw=1.8)
arrow(620, 124, 620, 112, color=SLATE, lw=1.8)
line([(1185, 145), (1185, 124), (940, 124), (940, 112)], color=SLATE, lw=1.8)
arrow(940, 124, 940, 112, color=SLATE, lw=1.8)

# fusion
box(620, 47, 320, 65, fc="#E7F1F3", ec=TEAL, lw=1.5, r=12)
txt(780, 88, r"Aligned view fusion  $\Psi_\omega$", size=10.4, weight="bold", ha="center")
txt(780, 66, "max / power / logit", size=8.8, color=SLATE, ha="center")

# decision
arrow(940, 79, 985, 79, color=SLATE, lw=1.8)
box(985, 47, 320, 65, fc=NAVY, ec=NAVY, lw=1.4, r=12)
txt(1145, 88, "argmax + background threshold", size=10.2, color=WHITE, weight="bold", ha="center")
txt(1145, 64, r"$\hat{Y}(x)$", size=12.0, color=WHITE, ha="center")

# Add a compact reading-path note in unused lower-right of panel B? Keep low-key.
txt(1340, 90, "class-score-level\ncomposition", size=8.2, color=GREY, ha="center", va="center")

# Panel labels in concise form
txt(40, 55, "solid arrow: data / computation     dashed arrow: shared configuration", size=8.2, color=GREY)

fig.savefig(OUT / "role_functional_text_layout.svg", bbox_inches="tight", pad_inches=0.08, facecolor="white")
fig.savefig(OUT / "role_functional_text_layout.png", dpi=180, bbox_inches="tight", pad_inches=0.08, facecolor="white")
plt.close(fig)
print(OUT / "role_functional_text_layout.png")