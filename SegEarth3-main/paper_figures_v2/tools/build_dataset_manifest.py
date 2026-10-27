#!/usr/bin/env python
"""Build a manifest for ONE dataset with N image/GT pairs.

Example:
    python tools/build_dataset_manifest.py \
      --dataset LoveDA --num-samples 30 \
      --data-root /home/PengJunhao/workspace/data \
      --pred-root paper_figures_v2/preds \
      --out paper_figures_v2/manifests/loveda.csv
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

import numpy as np
from PIL import Image

from progress_utils import progress
from build_paper_manifest import (
    DATASETS,
    choose_image_and_gt,
    first_existing,
    image_files,
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", required=True)
    parser.add_argument("--data-root", type=Path, default=Path("/home/PengJunhao/workspace/data"))
    parser.add_argument("--pred-root", type=Path, default=Path("paper_figures_v2/preds"))
    parser.add_argument("--palette-dir", type=Path, default=Path("paper_figures_v2/palettes"))
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--num-samples", type=int, default=30)
    parser.add_argument("--start-index", type=int, default=0)
    parser.add_argument("--sample", default=None, help="Optional single filename/stem.")
    parser.add_argument("--select-mode", choices=["first", "diverse"], default="first")
    parser.add_argument("--candidate-limit", type=int, default=500)
    args = parser.parse_args()

    dataset = args.dataset
    if dataset not in DATASETS:
        raise ValueError(f"Unknown dataset: {dataset}")
    img_candidates, gt_candidates, baseline_miou, ours_miou = DATASETS[dataset]
    img_root = first_existing(args.data_root, img_candidates)
    gt_root = first_existing(args.data_root, gt_candidates)
    if img_root is None or gt_root is None:
        raise FileNotFoundError(
            f"{dataset}: image/gt directory not found under {args.data_root}")

    files = image_files(img_root)
    pairs = []
    if args.sample:
        image, gt = choose_image_and_gt(dataset, files, gt_root, args.sample)
        pairs.append((image, gt))
    elif args.select_mode == "first":
        for image in progress(files[args.start_index:], desc=f"{dataset}: scanning"):
            try:
                _, gt = choose_image_and_gt(dataset, [image], gt_root)
            except FileNotFoundError:
                continue
            pairs.append((image, gt))
            if len(pairs) >= args.num_samples:
                break
    else:
        candidates = []
        for image in progress(files[args.start_index:], desc=f"{dataset}: scanning"):
            try:
                _, gt = choose_image_and_gt(dataset, [image], gt_root)
            except FileNotFoundError:
                continue
            candidates.append((image, gt))
            if len(candidates) >= args.candidate_limit:
                break
        scored = []
        for image, gt in progress(candidates, total=len(candidates), desc=f"{dataset}: scoring"):
            arr = np.asarray(Image.open(gt))
            if arr.ndim == 3:
                flat = arr.reshape(-1, arr.shape[-1])
                unique = len(np.unique(flat, axis=0))
                foreground = float(np.mean(np.any(flat != 0, axis=1)))
            else:
                unique = len(np.unique(arr))
                foreground = float(np.mean(arr != 0))
            scored.append((unique, foreground, image, gt))
        scored.sort(key=lambda item: (item[0], item[1]), reverse=True)
        pairs = [(image, gt) for _, _, image, gt in scored[:args.num_samples]]

    if not pairs:
        raise FileNotFoundError(f"No image/GT pairs found for {dataset}")
    if len(pairs) < args.num_samples:
        print(f"[warn] requested {args.num_samples}, found only {len(pairs)} valid pairs")

    key = dataset.lower()
    rows = []
    for image, gt in pairs:
        stem = image.stem
        rows.append({
            "dataset": dataset,
            "sample": stem,
            "image": str(image),
            "gt": str(gt),
            "baseline": str(args.pred_root / "baseline" / key / f"{stem}.npy"),
            "ours": str(args.pred_root / "ours" / key / f"{stem}.npy"),
            "palette": str(args.palette_dir / f"{key}.json"),
            "baseline_miou": f"{baseline_miou:.3f}",
            "ours_miou": f"{ours_miou:.3f}",
        })

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