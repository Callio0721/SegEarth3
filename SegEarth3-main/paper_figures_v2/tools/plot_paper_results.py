#!/usr/bin/env python
"""Create publication-quality qualitative segmentation figures.

The script reads a CSV manifest with one row per sample:

dataset,sample,image,gt,baseline,ours,palette,baseline_miou,ours_miou
LoveDA,loveda_001,/data/img.png,/data/gt.png,/data/base.npy,/data/ours.npy,/palettes/loveda.json,47.34,48.81

Notes
-----
* ``image`` may be PNG/TIF/JPG.
* ``baseline`` and ``ours`` may be .npy label maps or single-channel label images.
* If an RGB PNG/TIF mask is supplied, it is matched to the nearest palette color.
* If ``palette`` is empty, the script tries ``--palette-dir/<dataset>.json`` and
  then ``--class-dir/cls_<dataset>.txt`` for class names. A generic palette is
  used only when neither exists.
* ``gt`` is optional. Add ``--show-gt`` to display it.
* Outputs one figure per dataset, plus an optional combined figure.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

from progress_utils import progress


# A readable fallback palette. For papers, provide a dataset palette JSON so
# colors match the official benchmark/GT palette.
FALLBACK_COLORS = np.asarray([
    [255, 255, 255], [230, 25, 75], [60, 180, 75], [255, 225, 25],
    [0, 130, 200], [245, 130, 48], [145, 30, 180], [70, 240, 240],
    [240, 50, 230], [210, 245, 60], [250, 190, 190], [0, 128, 128],
    [170, 110, 40], [128, 0, 0], [0, 0, 128], [128, 128, 0],
    [0, 0, 0], [170, 255, 195], [128, 128, 128], [255, 215, 180],
], dtype=np.uint8)

TEXT = {
    "en": {
        "original": "Original",
        "gt": "Ground Truth",
        "baseline": "Baseline",
        "ours": "Ours",
        "miou": "mIoU",
        "sample": "Sample",
        "ignore": "Ignore",
    },
    "zh": {
        "original": "原图",
        "gt": "真值",
        "baseline": "Baseline",
        "ours": "我们的方法",
        "miou": "mIoU",
        "sample": "样本",
        "ignore": "忽略",
    },
}


@dataclass
class Palette:
    names: list[str]
    colors: np.ndarray
    gt_shift: int = 0
    gt_ignore_label: int | None = None
    ignore_color: np.ndarray | None = None

    @property
    def size(self) -> int:
        return int(self.colors.shape[0])


def _resolve(path: str | Path | None, base: Path) -> Path | None:
    if path is None:
        return None
    text = str(path).strip()
    if not text:
        return None
    p = Path(text)
    return p if p.is_absolute() else (base / p)


def _read_palette(path: Path | None, class_file: Path | None, dataset: str) -> Palette:
    names: list[str] = []
    colors = FALLBACK_COLORS.copy()
    gt_shift = 0
    gt_ignore_label = None
    ignore_color = np.asarray([245, 245, 245], dtype=np.uint8)

    if path is not None and path.exists():
        payload = json.loads(path.read_text(encoding="utf-8-sig"))
        names = [str(x) for x in payload.get("class_names", payload.get("names", []))]
        gt_shift = int(payload.get("gt_shift", 0))
        raw_ignore = payload.get("gt_ignore_label", None)
        gt_ignore_label = None if raw_ignore is None else int(raw_ignore)
        if "ignore_color" in payload:
            ignore_color = np.asarray(payload["ignore_color"], dtype=np.uint8)
        if "colors" in payload:
            colors = np.asarray(payload["colors"], dtype=np.uint8)
        elif "palette" in payload:
            raw = payload["palette"]
            if isinstance(raw, dict):
                colors = np.asarray(list(raw.values()), dtype=np.uint8)
                if not names:
                    names = [str(k) for k in raw.keys()]
            else:
                colors = np.asarray(raw, dtype=np.uint8)
    elif class_file is not None and class_file.exists():
        names = [line.strip() for line in class_file.read_text(encoding="utf-8-sig").splitlines() if line.strip()]

    if colors.ndim != 2 or colors.shape[1] != 3:
        raise ValueError(f"Invalid palette colors in {path}: expected N x 3 RGB values")

    n = max(len(names), int(colors.shape[0]), 1)
    if len(names) < n:
        names.extend(f"class_{i}" for i in range(len(names), n))
    if colors.shape[0] < n:
        repeat = math.ceil(n / colors.shape[0])
        colors = np.tile(colors, (repeat, 1))[:n]
    return Palette(
        names=names[:n],
        colors=colors[:n].astype(np.uint8),
        gt_shift=gt_shift,
        gt_ignore_label=gt_ignore_label,
        ignore_color=ignore_color,
    )

def _normalize_image(array: np.ndarray) -> np.ndarray:
    if array.dtype == np.uint8:
        return array
    if array.dtype == np.uint16:
        lo, hi = np.percentile(array, [1, 99])
        if hi <= lo:
            hi = lo + 1
        return np.clip((array - lo) * 255.0 / (hi - lo), 0, 255).astype(np.uint8)
    arr = np.asarray(array, dtype=np.float32)
    if np.nanmax(arr) <= 1.0:
        arr = arr * 255.0
    return np.clip(arr, 0, 255).astype(np.uint8)


def load_image(path: Path) -> np.ndarray:
    image = Image.open(path)
    if image.mode in ("RGBA", "LA"):
        image = image.convert("RGBA")
        arr = np.asarray(image)[..., :3]
    elif image.mode == "P":
        arr = np.asarray(image.convert("RGB"))
    else:
        arr = np.asarray(image)
    if arr.ndim == 2:
        arr = np.stack([arr] * 3, axis=-1)
    elif arr.ndim == 3 and arr.shape[-1] == 4:
        arr = arr[..., :3]
    return _normalize_image(arr)


def _rgb_to_labels(rgb: np.ndarray, palette: Palette) -> np.ndarray:
    flat = rgb.reshape(-1, 3).astype(np.int32)
    colors = palette.colors.astype(np.int32)
    dist = ((flat[:, None, :] - colors[None, :, :]) ** 2).sum(axis=-1)
    return dist.argmin(axis=1).reshape(rgb.shape[:2]).astype(np.int64)


def load_mask(path: Path, palette: Palette) -> np.ndarray:
    suffix = path.suffix.lower()
    if suffix == ".npy":
        arr = np.load(path)
        if arr.ndim == 3:
            if arr.shape[0] == 1:
                arr = arr[0]
            elif arr.shape[-1] == 1:
                arr = arr[..., 0]
            elif arr.shape[0] <= 64 and arr.shape[1] > 64 and arr.shape[2] > 64:
                # C x H x W logits/probabilities
                arr = arr.argmax(axis=0)
            elif arr.shape[-1] == 3:
                arr = _rgb_to_labels(arr, palette)
            else:
                arr = arr.argmax(axis=0)
        if arr.dtype.kind == "f":
            arr = (arr >= 0.5).astype(np.int64)
        return arr.astype(np.int64)

    image = Image.open(path)
    if image.mode == "P":
        return np.asarray(image).astype(np.int64)
    if image.mode in ("L", "I", "I;16"):
        arr = np.asarray(image)
        if arr.dtype.kind == "f":
            arr = (arr >= 0.5).astype(np.int64)
        return arr.astype(np.int64)
    return _rgb_to_labels(np.asarray(image.convert("RGB")), palette)


def apply_gt_shift(labels: np.ndarray, palette: Palette) -> np.ndarray:
    labels = np.asarray(labels)
    out = labels + int(palette.gt_shift)
    if palette.gt_ignore_label is not None:
        out[labels == int(palette.gt_ignore_label)] = -1
    return out


def colorize(labels: np.ndarray, palette: Palette) -> np.ndarray:
    labels = np.asarray(labels)
    ignore = palette.ignore_color if palette.ignore_color is not None else np.asarray([245, 245, 245], dtype=np.uint8)
    out = np.empty((*labels.shape, 3), dtype=np.uint8)
    out[:] = ignore
    valid = (labels >= 0) & (labels < palette.size)
    out[valid] = palette.colors[labels[valid]]
    return out


def per_image_miou(gt: np.ndarray, pred: np.ndarray, num_classes: int, ignore_value: int = -1) -> float | None:
    gt = np.asarray(gt)
    pred = np.asarray(pred)
    valid = (gt != ignore_value) & (gt >= 0)
    if not valid.any():
        return None
    gt_valid = gt[valid]
    pred_valid = pred[valid]
    classes = sorted(set(int(x) for x in np.unique(gt_valid)))
    ious = []
    for cls in classes:
        if cls < 0 or cls >= num_classes:
            continue
        gt_c = valid & (gt == cls)
        pred_c = valid & (pred == cls)
        union = np.logical_or(gt_c, pred_c).sum()
        if union == 0:
            continue
        ious.append(float(np.logical_and(gt_c, pred_c).sum()) / float(union))
    return float(np.mean(ious)) if ious else None


def _present_labels(masks: Iterable[np.ndarray], palette: Palette) -> list[int]:
    ids: set[int] = set()
    for mask in masks:
        arr = np.asarray(mask)
        values = arr[(arr >= 0) & (arr < palette.size)]
        ids.update(int(v) for v in np.unique(values))
    return sorted(ids)


def _legend_handles(ids: Sequence[int], palette: Palette):
    from matplotlib.patches import Patch
    handles = []
    for idx in ids:
        color = palette.colors[idx].astype(np.float32) / 255.0
        handles.append(Patch(facecolor=color, edgecolor="none", label=palette.names[idx]))
    return handles


def _format_metric(value: str | float | None, key: str) -> str:
    if value is None or str(value).strip() == "":
        return ""
    try:
        return f"\n{key} {float(value):.2f}"
    except ValueError:
        return f"\n{key} {value}"


def _prepare_panels(row: dict, base: Path, args, palette: Palette):
    image = load_image(_resolve(row["image"], base))
    baseline = load_mask(_resolve(row["baseline"], base), palette)
    ours = load_mask(_resolve(row["ours"], base), palette)
    gt = None
    if args.show_gt and row.get("gt"):
        gt = load_mask(_resolve(row["gt"], base), palette)
        gt = apply_gt_shift(gt, palette)

    t = TEXT[args.lang]
    baseline_title = args.baseline_name
    ours_title = args.ours_name
    if gt is not None:
        valid_gt = gt[gt >= 0]
        max_label = max(int(baseline.max()), int(ours.max()), int(valid_gt.max()) if valid_gt.size else 0)
        num_classes = max(palette.size, max_label + 1)
        baseline_score = per_image_miou(gt, baseline, num_classes=num_classes)
        ours_score = per_image_miou(gt, ours, num_classes=num_classes)
        if baseline_score is not None:
            baseline_title += f"\nImage {t['miou']} {baseline_score:.3f}"
        if ours_score is not None:
            ours_title += f"\nImage {t['miou']} {ours_score:.3f}"

    panels = [
        (t["original"], image),
        (baseline_title, colorize(baseline, palette)),
        (ours_title, colorize(ours, palette)),
    ]
    if gt is not None:
        panels.insert(1, (t["gt"], colorize(gt, palette)))
    return panels, [baseline, ours, gt]


def plot_one_dataset(row: dict, base: Path, args, out_dir: Path) -> tuple[Path, Path]:
    palette_path = _resolve(row.get("palette"), base)
    if palette_path is None and args.palette_dir:
        candidate = args.palette_dir / f"{row['dataset'].lower()}.json"
        palette_path = candidate if candidate.exists() else None
    class_file = None
    if args.class_dir:
        candidate = args.class_dir / f"cls_{row['dataset'].lower()}.txt"
        class_file = candidate if candidate.exists() else None
    palette = _read_palette(palette_path, class_file, row["dataset"])

    panels, masks = _prepare_panels(row, base, args, palette)
    ids = _present_labels([m for m in masks if m is not None], palette)
    handles = _legend_handles(ids, palette)
    if masks[2] is not None and np.any(masks[2] < 0):
        from matplotlib.patches import Patch
        ignore_color = palette.ignore_color if palette.ignore_color is not None else np.asarray([245, 245, 245], dtype=np.uint8)
        handles.append(Patch(facecolor=ignore_color.astype(np.float32) / 255.0,
                             edgecolor="none", label=TEXT[args.lang]["ignore"]))

    ncols = len(panels)
    fig, axes = plt.subplots(1, ncols, figsize=(3.15 * ncols, 3.25))
    if ncols == 1:
        axes = [axes]

    for ax, (title, data) in zip(axes, panels):
        ax.imshow(data)
        ax.set_title(title, fontsize=10.5, fontweight="bold", pad=7)
        ax.axis("off")

    sample = str(row.get("sample", "")).strip()
    title = row["dataset"] if not sample else f"{row['dataset']} | {sample}"
    fig.suptitle(title, fontsize=13, fontweight="bold", y=1.02)

    if handles:
        fig.legend(
            handles=handles,
            loc="lower center",
            ncol=min(6, len(handles)),
            frameon=False,
            fontsize=8.5,
            handlelength=1.0,
            columnspacing=1.0,
            bbox_to_anchor=(0.5, -0.01),
        )

    fig.subplots_adjust(left=0.01, right=0.99, top=0.88, bottom=0.22, wspace=0.04)
    stem = f"{row['dataset']}_{sample}" if sample else row["dataset"]
    stem = "".join(ch if ch.isalnum() or ch in "-_." else "_" for ch in stem)
    png_path = out_dir / f"{stem}.png"
    pdf_path = out_dir / f"{stem}.pdf"
    fig.savefig(png_path, dpi=args.dpi, bbox_inches="tight", facecolor="white")
    fig.savefig(pdf_path, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return png_path, pdf_path


def plot_combined(rows: list[dict], base: Path, args, out_dir: Path) -> tuple[Path, Path]:
    prepared = []
    for row in rows:
        palette_path = _resolve(row.get("palette"), base)
        if palette_path is None and args.palette_dir:
            candidate = args.palette_dir / f"{row['dataset'].lower()}.json"
            palette_path = candidate if candidate.exists() else None
        class_file = None
        if args.class_dir:
            candidate = args.class_dir / f"cls_{row['dataset'].lower()}.txt"
            class_file = candidate if candidate.exists() else None
        palette = _read_palette(palette_path, class_file, row["dataset"])
        panels, masks = _prepare_panels(row, base, args, palette)
        ids = _present_labels([m for m in masks if m is not None], palette)
        prepared.append((row, panels, palette, _legend_handles(ids, palette)))

    nrows = len(prepared)
    ncols = max(len(x[1]) for x in prepared)
    fig, axes = plt.subplots(
        nrows=nrows,
        ncols=ncols,
        figsize=(3.05 * ncols, 2.85 * nrows),
        squeeze=False,
    )

    for r, (row, panels, palette, handles) in enumerate(prepared):
        for c in range(ncols):
            ax = axes[r, c]
            ax.axis("off")
            if c < len(panels):
                title, data = panels[c]
                ax.imshow(data)
                if r == 0:
                    ax.set_title(title, fontsize=10, fontweight="bold", pad=5)
            if c == 0:
                sample = str(row.get("sample", "")).strip()
                label = row["dataset"] if not sample else f"{row['dataset']}\n{sample}"
                ax.text(-0.05, 0.5, label, transform=ax.transAxes,
                        ha="right", va="center", fontsize=10, fontweight="bold")
        if handles:
            axes[r, -1].legend(
                handles=handles,
                loc="center left",
                bbox_to_anchor=(1.01, 0.5),
                frameon=False,
                fontsize=8,
                handlelength=1.0,
                labelspacing=0.45,
            )

    fig.subplots_adjust(left=0.10, right=0.82, top=0.96, bottom=0.02, wspace=0.03, hspace=0.10)
    png_path = out_dir / "paper_results_combined.png"
    pdf_path = out_dir / "paper_results_combined.pdf"
    fig.savefig(png_path, dpi=args.dpi, bbox_inches="tight", facecolor="white")
    fig.savefig(pdf_path, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return png_path, pdf_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Plot qualitative segmentation results for papers.")
    parser.add_argument("--manifest", required=True, type=Path, help="CSV manifest, one row per dataset/sample.")
    parser.add_argument("--out-dir", type=Path, default=Path("paper_figures_v2/figures"), help="Output directory.")
    parser.add_argument("--palette-dir", type=Path, default=None, help="Directory containing <dataset>.json palettes.")
    parser.add_argument("--class-dir", type=Path, default=None, help="Directory containing cls_<dataset>.txt class files.")
    parser.add_argument("--show-gt", action="store_true", help="Insert Ground Truth as a separate panel.")
    parser.add_argument("--combined", action="store_true", help="Also create one combined grid figure.")
    parser.add_argument("--lang", choices=["en", "zh"], default="en", help="Figure text language.")
    parser.add_argument("--baseline-name", default="SegEarth-OV3", help="Baseline column title.")
    parser.add_argument("--ours-name", default="Ours", help="Ours column title.")
    parser.add_argument("--font", default=None, help="Matplotlib font family, e.g. Times New Roman or Noto Sans CJK SC.")
    parser.add_argument("--dpi", type=int, default=300, help="Raster export DPI.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.font:
        from matplotlib import font_manager
        available = {font.name for font in font_manager.fontManager.ttflist}
        candidates = [
            args.font,
            "Liberation Serif",
            "Nimbus Roman",
            "DejaVu Serif",
            "Noto Sans CJK SC",
            "DejaVu Sans",
        ]
        chosen = next((name for name in candidates if name in available), "DejaVu Sans")
        if chosen != args.font:
            print(f"[font] {args.font!r} not found; using {chosen!r}")
        matplotlib.rcParams["font.family"] = chosen
        matplotlib.rcParams["axes.unicode_minus"] = False

    manifest = args.manifest.resolve()
    base = manifest.parent
    args.out_dir.mkdir(parents=True, exist_ok=True)
    with manifest.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))

    required = {"dataset", "image", "baseline", "ours"}
    if not rows:
        raise ValueError("Manifest is empty.")
    missing = required - set(rows[0].keys())
    if missing:
        raise ValueError(f"Manifest is missing columns: {sorted(missing)}")

    for row in progress(rows, total=len(rows), desc="figures"):
        if not row.get("dataset"):
            raise ValueError("Every manifest row needs a dataset name.")
        png, pdf = plot_one_dataset(row, base, args, args.out_dir)
        print(f"[saved] {png}")
        print(f"[saved] {pdf}")

    if args.combined:
        png, pdf = plot_combined(rows, base, args, args.out_dir)
        print(f"[saved] {png}")
        print(f"[saved] {pdf}")


if __name__ == "__main__":
    main()