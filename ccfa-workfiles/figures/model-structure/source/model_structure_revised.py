from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle
from matplotlib.lines import Line2D


ROOT = Path(r"D:\论文\9.27论文\中文论文\绘图")
ASSETS = ROOT / "role_functional_text_skeleton" / "assets"
OUT = Path(r"D:\论文\9.27论文\ccfa-workfiles\figures\model-structure")
BUILD = OUT / "build"
BUILD.mkdir(parents=True, exist_ok=True)

plt.rcParams.update({
    "font.family": "Times New Roman",
    "mathtext.fontset": "stix",
    "font.size": 10,
})

W, H = 2000, 900
fig = plt.figure(figsize=(20, 9), dpi=180, facecolor="white")
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, W)
ax.set_ylim(0, H)
ax.axis("off")

INK = "#18324B"
MUTED = "#607386"
LINE = "#8394A5"
BLUE = "#4E79A7"
BLUE_F = "#EDF3FA"
PURPLE = "#7655A8"
PURPLE_F = "#F2ECFB"
TEAL = "#2D8580"
TEAL_F = "#E8F6F4"
ORANGE = "#C8793C"
ORANGE_F = "#FBEDE0"
PALE = "#F7F9FB"


def rounded(x, y, w, h, fill="white", edge=LINE, lw=1.5, radius=12, z=2):
    patch = FancyBboxPatch(
        (x, y), w, h,
        boxstyle=f"round,pad=0,rounding_size={radius}",
        facecolor=fill, edgecolor=edge, linewidth=lw, zorder=z,
    )
    ax.add_patch(patch)


def label(x, y, text, size=10, color=INK, weight="normal", ha="left",
          va="center", z=6, rotation=0):
    ax.text(x, y, text, fontsize=size, color=color, fontweight=weight,
            ha=ha, va=va, zorder=z, rotation=rotation)


def arrow(x1, y1, x2, y2, color=INK, lw=1.7, dashed=False, rad=0.0, z=4):
    style = (0, (4, 3)) if dashed else "-"
    ax.add_patch(FancyArrowPatch(
        (x1, y1), (x2, y2), arrowstyle="-|>", mutation_scale=11,
        linewidth=lw, linestyle=style, color=color, zorder=z,
        connectionstyle=f"arc3,rad={rad}", shrinkA=2, shrinkB=2,
    ))


def image_thumb(path, x, y, w, h, edge=LINE):
    img = plt.imread(path)
    ax.imshow(img, extent=(x, x + w, y, y + h), aspect="auto",
              origin="upper", zorder=3)
    ax.add_patch(Rectangle((x, y), w, h, fill=False, edgecolor=edge,
                           linewidth=1.0, zorder=4))


def module(x, y, w, h, title, subtitle="", fill="white", edge=LINE,
           title_color=INK, title_size=11):
    rounded(x, y, w, h, fill=fill, edge=edge, lw=1.4, radius=10)
    label(x + 16, y + h - 20, title, size=title_size, weight="bold",
          color=title_color)
    if subtitle:
        label(x + 16, y + h - 39, subtitle, size=8.2, color=MUTED)


def role_row(y, role, text, fill, edge):
    rounded(98, y, 305, 46, fill=fill, edge=edge, lw=1.2, radius=9)
    label(116, y + 23, role, size=12, color=edge, weight="bold")
    label(154, y + 23, text, size=9.6)


def view_lane(y, title, subtitle, output, edge, fill):
    rounded(978, y, 565, 112, fill=fill, edge=edge, lw=1.4, radius=13)
    label(998, y + 87, title, size=10.5, color=edge, weight="bold")
    label(998, y + 68, subtitle, size=8.2, color=MUTED)
    rounded(1165, y + 25, 155, 55, fill="white", edge=LINE, lw=1.0, radius=8)
    label(1242, y + 61, "Frozen SAM3", size=9.2, weight="bold", ha="center")
    label(1242, y + 43, "full grounding", size=7.6, color=MUTED, ha="center")
    arrow(1320, y + 52, 1360, y + 52, color=LINE, lw=1.4)
    rounded(1360, y + 25, 160, 55, fill=BLUE_F, edge=BLUE, lw=1.0, radius=8)
    label(1440, y + 61, "Role correction", size=8.8, weight="bold", ha="center")
    label(1440, y + 43, r"$\mathcal{B}(a_A,a_\pi)$ + P$\rightarrow$I",
          size=7.8, color=MUTED, ha="center")
    arrow(1520, y + 52, 1552, y + 52, color=LINE, lw=1.4)
    rounded(1552, y + 25, 105, 55, fill="white", edge=edge, lw=1.1, radius=8)
    label(1604, y + 52, output, size=12, color=edge, weight="bold",
          ha="center")


# Figure title and reading guide.
label(70, 855, "Joint Role–View Specialization", size=23, weight="bold")
label(70, 824,
      "Frozen concept grounding with role-aware evidence correction and aligned multi-view fusion",
      size=10.5, color=MUTED)
label(1930, 855, "paper mechanism figure", size=8.5, color=MUTED, ha="right")

# Column headings: a single, clear reading path.
for x, num, text in [(70, "01", "Preserve the concept anchor"),
                      (720, "02", "Specialize evidence by readout role"),
                      (1665, "03", "Fuse aligned observations")]:
    label(x, 790, num, size=9, color=BLUE, weight="bold")
    label(x + 38, 790, text, size=11, weight="bold")
    ax.add_line(Line2D([x, x + 510], [770, 770], color="#D8E0E8",
                        linewidth=1.0, zorder=1))

# 01: anchor and role prompt inventory.
rounded(70, 205, 555, 530, fill=PALE, edge="#D5DFE8", lw=1.1, radius=16)
label(98, 700, "Official concept anchor", size=11.5, weight="bold")
label(98, 677, "The original class name and aliases remain the reference signal.",
      size=8.8, color=MUTED)
rounded(98, 610, 495, 48, fill=BLUE_F, edge=BLUE, lw=1.3, radius=9)
label(118, 634, "road + official aliases", size=10.5, weight="bold")
label(573, 634, "anchor", size=8.2, color=BLUE, weight="bold", ha="right")

label(98, 575, "Role-functional supplements", size=10.5, weight="bold")
label(98, 554, "Each candidate is fully grounded; only the assigned readout is used.",
      size=8.5, color=MUTED)
role_row(475, "P", "scene presence / visibility", PURPLE_F, PURPLE)
role_row(415, "S", "dense surface / coverage", TEAL_F, TEAL)
role_row(355, "I", "region organization / boundary", ORANGE_F, ORANGE)
label(98, 300, "P, S, I denote readout responsibilities, not three isolated models.",
      size=8.3, color=MUTED)
arrow(625, 470, 690, 470, color=BLUE, lw=2.2)

# 02: one complete grounding, then bounded composition.
rounded(690, 205, 885, 530, fill="white", edge="#D5DFE8", lw=1.1, radius=16)
label(720, 700, "Complete frozen grounding", size=11.5, weight="bold")
label(720, 677, "The shared SAM3 computation is retained; specialization occurs in evidence use.",
      size=8.8, color=MUTED)
rounded(735, 560, 330, 68, fill=BLUE_F, edge=BLUE, lw=1.5, radius=11)
label(900, 600, "Frozen SAM3", size=13, weight="bold", ha="center")
label(900, 578, r"$\Phi(X_v, t_c) \rightarrow (p,S,I)$", size=10,
      color=BLUE, ha="center")
label(900, 545, "one full multimodal grounding pass per prompt", size=8.4,
      color=MUTED, ha="center")

arrow(900, 560, 900, 510, color=LINE, lw=1.6)
rounded(735, 385, 330, 125, fill=PALE, edge=LINE, lw=1.3, radius=11)
label(900, 480, "Anchor-preserving correction", size=10.5, weight="bold",
      ha="center")
label(900, 447, r"$\tilde O^r = O_A^r + \alpha\,\mathrm{clip}(O_\pi^r-O_A^r)$",
      size=9.3, ha="center")
label(900, 421, r"$r\in\{P,S,I\}$;  $\alpha=0.5,\ \tau=0.25$",
      size=8.4, color=MUTED, ha="center")
label(900, 397, "P update is retained in native instance coupling.", size=8.1,
      color=PURPLE, ha="center")

arrow(1065, 447, 1110, 447, color=LINE, lw=1.6)
rounded(1110, 385, 405, 125, fill=PALE, edge=LINE, lw=1.3, radius=11)
label(1128, 480, "Native class evidence", size=10.5, weight="bold")
label(1128, 447, r"$F_{v,\pi}=\tilde p\,\max(\tilde S,\tilde I)$", size=10)
label(1128, 420, "official aliases and spatial aggregation are preserved",
      size=8.2, color=MUTED)
label(1128, 397, "one continuous class field per view", size=8.2, color=MUTED)

# Compact P/S/I role key, instead of a large matrix.
rounded(735, 245, 780, 95, fill="white", edge="#D5DFE8", lw=1.0, radius=10)
label(755, 315, "Selected profile  π", size=9.8, weight="bold")
for x, role, text, fill, edge in [
    (930, "P", "slot 1", PURPLE_F, PURPLE),
    (1090, "S", "slot 2", TEAL_F, TEAL),
    (1250, "I", "slot 3", ORANGE_F, ORANGE),
]:
    rounded(x, 278, 125, 31, fill=fill, edge=edge, lw=1.0, radius=7)
    label(x + 18, 293, role, size=9.5, color=edge, weight="bold")
    label(x + 55, 293, text, size=8.7, color=edge)
label(1455, 293, "0 = anchor", size=8.2, color=MUTED, ha="right")

# 03: two observations share the same profile.
rounded(1665, 205, 265, 530, fill=PALE, edge="#D5DFE8", lw=1.1, radius=16)
label(1692, 700, "Aligned view fusion", size=11.5, weight="bold")
label(1692, 677, "The same π is evaluated independently per view.",
      size=8.8, color=MUTED)

image_thumb(ASSETS / "road_input4.png", 1692, 568, 88, 63, edge=LINE)
label(1780, 598, "same target region", size=8.2, color=MUTED)
label(1736, 548, "Local / native", size=9.6, color=TEAL, weight="bold",
      ha="center")
label(1736, 530, "detail + boundary", size=8.0, color=MUTED, ha="center")
arrow(1785, 548, 1820, 548, color=TEAL, lw=1.5)
rounded(1820, 522, 88, 52, fill=TEAL_F, edge=TEAL, lw=1.0, radius=8)
label(1864, 548, r"$G_{L,\pi}$", size=12, color=TEAL, weight="bold",
      ha="center")

label(1736, 427, "Context / wider", size=9.6, color=ORANGE, weight="bold",
      ha="center")
label(1736, 409, "layout + continuity", size=8.0, color=MUTED, ha="center")
arrow(1785, 427, 1820, 427, color=ORANGE, lw=1.5)
rounded(1820, 401, 88, 52, fill=ORANGE_F, edge=ORANGE, lw=1.0, radius=8)
label(1864, 427, r"$G_{G,\pi}$", size=12, color=ORANGE, weight="bold",
      ha="center")

arrow(1864, 522, 1864, 477, color=LINE, lw=1.5)
arrow(1864, 401, 1864, 477, color=LINE, lw=1.5)
rounded(1710, 318, 198, 78, fill="white", edge=BLUE, lw=1.4, radius=10)
label(1809, 370, "Aligned composition", size=10.2, weight="bold",
      ha="center")
label(1809, 343, r"$Z=\Psi(G_{L,\pi},G_{G,\pi})$", size=10, color=BLUE,
      ha="center")
label(1809, 326, "profile-selected operator", size=7.8, color=MUTED,
      ha="center")
arrow(1809, 318, 1809, 270, color=BLUE, lw=1.8)
rounded(1692, 218, 234, 52, fill=INK, edge=INK, lw=1.2, radius=9)
label(1809, 248, "Original class decision", size=9.4, color="white",
      weight="bold", ha="center")
label(1809, 231, r"$\arg\max +$ threshold", size=8.8, color="white",
      ha="center")

# Cross-column continuation arrows and legend.
arrow(1575, 447, 1650, 447, color=BLUE, lw=2.2)
label(1612, 470, "same role profile", size=7.8, color=BLUE, ha="center")
ax.add_line(Line2D([70, 110], [105, 105], color=INK, linewidth=1.6))
ax.add_patch(FancyArrowPatch((100, 105), (110, 105), arrowstyle="-|>",
                             mutation_scale=8, color=INK, linewidth=1.6))
label(120, 105, "data / computation", size=8.1, color=MUTED)
ax.add_line(Line2D([290, 330], [105, 105], color=BLUE, linewidth=1.4,
                   linestyle=(0, (4, 3))))
label(340, 105, "shared configuration", size=8.1, color=MUTED)
label(1930, 105, "No internal head splitting; specialization is applied after complete grounding.",
      size=8.2, color=MUTED, ha="right")

fig.savefig(BUILD / "model_structure_revised.svg", bbox_inches="tight",
            pad_inches=0.08, facecolor="white")
fig.savefig(BUILD / "model_structure_revised.png", dpi=220,
            bbox_inches="tight", pad_inches=0.08, facecolor="white")
plt.close(fig)
print(BUILD / "model_structure_revised.svg")
print(BUILD / "model_structure_revised.png")
