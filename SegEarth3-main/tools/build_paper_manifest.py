#!/usr/bin/env python
"""Build a paper-results manifest by scanning the actual dataset directories.

Run this on the server, not on a machine that only has the repository:

    python tools/build_paper_manifest.py \
      --data-root /home/PengJunhao/workspace/data \
      --pred-root paper_figures_v2/preds \
      --out tools/paper_results_manifest.server.csv

It selects the first sorted image from each dataset unless --sample is given:

    --sample LoveDA=2522.png
    --sample iSAID=P0003_0_896_0_896.png
    --sample Potsdam=5_15_0_0_512_512.png

The manifest can then be edited in Excel; this script only generates the paths.
"""

from __future__ import annotations

import argparse
import csv
from collections import OrderedDict
from pathlib import Path

IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".tif", ".tiff", ".bmp"}

# dataset: (possible image dirs, possible gt dirs, baseline mIoU, ours mIoU)
DATASETS = OrderedDict([
    ("LoveDA", (["LoveDA/img_dir/val", "loveDA/img_dir/val"], ["LoveDA/ann_dir/val", "loveDA/ann_dir/val"], 47.342, 48.806)),
    ("OpenEarthMap", (["OpenEarthMap/img_dir/val"], ["OpenEarthMap/ann_dir/val"], 44.303, 53.075)),
    ("Potsdam", (["potsdam/img_dir/val"], ["potsdam/ann_dir/val"], 57.867, 63.181)),
    ("Vaihingen", (["vaihingen/img_dir/val"], ["vaihingen/ann_dir/val"], 60.860, 66.384)),
    ("iSAID", (["iSAID/img_dir/val"], ["iSAID/ann_dir/val"], 27.643, 29.126)),
    ("UAVid", (["UAVid/img_dir/test"], ["UAVid/ann_dir/test"], 54.585, 59.822)),
    ("UDD5", (["UDD5/val/src"], ["UDD5/val/gt"], 71.804, 72.944)),
    ("VDD", (["VDD/test/src"], ["VDD/test/gt"], 64.107, 66.555)),
    ("VOC20", (["VOC2012/JPEGImages", "VOCdevkit/VOC2012/JPEGImages", "voc2012/JPEGImages"], ["VOC2012/SegmentationClass", "VOCdevkit/VOC2012/SegmentationClass", "voc2012/SegmentationClass"], 96.890, 97.108)),
    ("Cityscapes", (["cityscapes/leftImg8bit/val", "CityScapes/leftImg8bit/val"], ["cityscapes/gtFine/val", "CityScapes/gtFine/val"], 67.903, 72.195)),
])


def first_existing(root: Path, candidates: list[str]) -> Path | None:
    for rel in candidates:
        p = root / rel
        if p.exists():
            return p
    return None


def image_files(root: Path) -> list[Path]:
    if not root.exists():
        return []
    return sorted(
        p for p in root.rglob("*")
        if p.is_file() and p.suffix.lower() in IMAGE_EXTS
    )


def index_by_stem(root: Path) -> dict[str, Path]:
    out: dict[str, Path] = {}
    for p in image_files(root):
        out.setdefault(p.stem, p)
    return out


def choose_image(files: list[Path], query: str | None) -> Path:
    if not files:
        raise FileNotFoundError("No image files found.")
    if not query:
        return files[0]
    q = query.replace("\\", "/")
    for p in files:
        if p.name == q or p.stem == q or str(p).replace("\\", "/").endswith(q):
            return p
    raise FileNotFoundError(f"Cannot find sample {query!r}.")


def find_gt(dataset: str, image: Path, gt_root: Path) -> Path:
    gt_index = index_by_stem(gt_root)
    stem = image.stem
    if dataset == "iSAID":
        candidates = [stem + "_instance_color_RGB"]
    elif dataset == "Cityscapes":
        base = stem.replace("_leftImg8bit", "")
        candidates = [
            base + "_gtFine_labelTrainIds",
            base + "_gtFine_labelIds",
            base + "_gtFine_labelTrainIds",
        ]
    else:
        candidates = [stem]

    for key in candidates:
        if key in gt_index:
            return gt_index[key]

    # Last-resort matching for converted datasets with a suffix.
    for key, path in gt_index.items():
        if key == stem or key.startswith(stem + "_"):
            return path

    raise FileNotFoundError(
        f"No GT found for {dataset}: image={image}, gt_root={gt_root}"
    )


def choose_image_and_gt(dataset: str, files: list[Path], gt_root: Path, query: str | None = None) -> tuple[Path, Path]:
    if query:
        image = choose_image(files, query)
        return image, find_gt(dataset, image, gt_root)
    for image in files:
        try:
            return image, find_gt(dataset, image, gt_root)
        except FileNotFoundError:
            continue
    raise FileNotFoundError(f"No image with GT found for {dataset} under {gt_root}")


def parse_samples(values: list[str]) -> dict[str, str]:
    out: dict[str, str] = {}
    for item in values:
        if "=" not in item:
            raise ValueError(f"--sample must be DATASET=NAME, got {item!r}")
        key, value = item.split("=", 1)
        out[key] = value
    return out


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-root", type=Path, default=Path("/home/PengJunhao/workspace/data"))
    parser.add_argument("--pred-root", type=Path, default=Path("paper_figures_v2/preds"))
    parser.add_argument("--palette-dir", type=Path, default=Path("paper_figures_v2/palettes"))
    parser.add_argument("--out", type=Path, default=Path("paper_figures_v2/manifests/all_datasets.csv"))
    parser.add_argument("--datasets", nargs="*", default=list(DATASETS.keys()))
    parser.add_argument("--sample", action="append", default=[], help="DATASET=filename_or_stem")
    parser.add_argument("--check", action="store_true", help="Warn when baseline/ours .npy files are missing.")
    args = parser.parse_args()

    samples = parse_samples(args.sample)
    rows = []

    for dataset in args.datasets:
        if dataset not in DATASETS:
            raise ValueError(f"Unknown dataset: {dataset}")
        img_candidates, gt_candidates, baseline_miou, ours_miou = DATASETS[dataset]
        img_root = first_existing(args.data_root, img_candidates)
        gt_root = first_existing(args.data_root, gt_candidates)
        if img_root is None or gt_root is None:
            print(f"[skip] {dataset}: image/gt directory not found under {args.data_root}")
            continue

        files = image_files(img_root)
        image, gt = choose_image_and_gt(
            dataset, files, gt_root, samples.get(dataset))
        stem = image.stem
        key = dataset.lower()
        palette = args.palette_dir / f"{key}.json"
        baseline = args.pred_root / "baseline" / key / f"{stem}.npy"
        ours = args.pred_root / "ours" / key / f"{stem}.npy"

        if args.check:
            if not baseline.exists():
                print(f"[missing] baseline: {baseline}")
            if not ours.exists():
                print(f"[missing] ours: {ours}")

        rows.append({
            "dataset": dataset,
            "sample": stem,
            "image": str(image),
            "gt": str(gt),
            "baseline": str(baseline),
            "ours": str(ours),
            "palette": str(palette) if palette.exists() else "",
            "baseline_miou": f"{baseline_miou:.3f}",
            "ours_miou": f"{ours_miou:.3f}",
        })
        print(f"[ok] {dataset}: {image.name} -> {gt.name}")

    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=[
            "dataset", "sample", "image", "gt", "baseline", "ours",
            "palette", "baseline_miou", "ours_miou",
        ])
        writer.writeheader()
        writer.writerows(rows)
    print(f"[saved] {args.out} ({len(rows)} rows)")


if __name__ == "__main__":
    main()