#!/usr/bin/env python
"""Write per-dataset palette JSON files from registered dataset metainfo.

Example:
    python tools/make_dataset_palettes.py --out-dir tools/palettes
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import custom_datasets  # noqa: F401
import segearthov3_segmentor  # noqa: F401
from mmseg.registry import DATASETS

try:
    import mmseg.datasets  # noqa: F401
except Exception:
    pass


CLASS_FILES = {
    "LoveDA": "configs/cls_loveda.txt",
    "OpenEarthMap": "configs/cls_openearthmap.txt",
    "Potsdam": "configs/cls_potsdam.txt",
    "Vaihingen": "configs/cls_vaihingen.txt",
    "iSAID": "configs/cls_iSAID.txt",
    "UAVid": "configs/cls_uavid.txt",
    "UDD5": "configs/cls_udd5.txt",
    "VDD": "configs/cls_vdd.txt",
    "VOC20": "configs/cls_voc20.txt",
    "Cityscapes": "configs/cls_city_scapes.txt",
}


DATASET_CLASSES = {
    "LoveDA": "LoveDADataset",
    "OpenEarthMap": "OpenEarthMapDataset",
    "Potsdam": "PotsdamDataset",
    "Vaihingen": "ISPRSDataset",
    "iSAID": "iSAIDDataset",
    "UAVid": "UAVidDataset",
    "UDD5": "UDD5Dataset",
    "VDD": "VDDDataset",
    "VOC20": "PascalVOC20Dataset",
    "Cityscapes": "CityscapesDataset",
}

# Dataset-specific fallbacks only when a registered METAINFO has no palette.
FALLBACK = {
    "LoveDA": (
        ["background", "building", "road", "water", "barren", "forest", "agriculture"],
        [[255, 255, 255], [255, 0, 0], [255, 255, 0], [0, 0, 255],
         [159, 129, 183], [0, 255, 0], [0, 255, 255]],
    ),
    "Potsdam": (
        ["road", "building", "grass", "tree", "car", "clutter"],
        [[255, 255, 255], [0, 0, 255], [0, 255, 0], [0, 255, 255],
         [255, 255, 0], [255, 0, 0]],
    ),
    "Vaihingen": (
        ["road", "building", "grass", "tree", "car", "clutter"],
        [[255, 255, 255], [0, 0, 255], [0, 255, 0], [0, 255, 255],
         [255, 255, 0], [255, 0, 0]],
    ),
    "VDD": (
        ["other", "wall", "road", "vegetation", "vehicle", "roof", "water"],
        [[0, 0, 0], [192, 0, 0], [128, 64, 128], [0, 128, 0],
         [0, 0, 142], [192, 0, 192], [0, 128, 255]],
    ),
}

GT_SHIFT = {
    "VOC20": -1,
}
GT_IGNORE = {
    "VOC20": 0,
}


def fallback_colors(n: int) -> list[list[int]]:
    base = np.asarray([
        [255, 255, 255], [230, 25, 75], [60, 180, 75], [255, 225, 25],
        [0, 130, 200], [245, 130, 48], [145, 30, 180], [70, 240, 240],
        [240, 50, 230], [210, 245, 60], [250, 190, 190], [0, 128, 128],
        [170, 110, 40], [128, 0, 0], [0, 0, 128], [128, 128, 0],
        [0, 0, 0], [170, 255, 195], [128, 128, 128], [255, 215, 180],
    ], dtype=np.uint8)
    repeat = (n + len(base) - 1) // len(base)
    return np.tile(base, (repeat, 1))[:n].tolist()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out-dir", type=Path, default=Path("paper_figures_v2/palettes"))
    args = parser.parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=True)

    for dataset, class_name in DATASET_CLASSES.items():
        names = None
        colors = None
        try:
            cls = DATASETS.get(class_name)
            meta = getattr(cls, "METAINFO", {})
            names = [str(x) for x in meta.get("classes", [])]
            colors = meta.get("palette")
        except Exception as exc:
            print(f"[warn] {dataset}: cannot read {class_name} metainfo: {exc}")

        if not names:
            class_path = REPO_ROOT / CLASS_FILES[dataset]
            if class_path.exists():
                names = [line.strip() for line in class_path.read_text(encoding="utf-8-sig").splitlines() if line.strip()]
        if not names:
            if dataset in FALLBACK:
                names, colors = FALLBACK[dataset]
            else:
                names = [f"class_{i}" for i in range(20)]
        if not colors:
            if dataset in FALLBACK:
                names, colors = FALLBACK[dataset]
            else:
                colors = fallback_colors(len(names))

        colors = np.asarray(colors, dtype=np.uint8).tolist()
        payload = {
            "class_names": names,
            "colors": colors,
            "gt_shift": int(GT_SHIFT.get(dataset, 0)),
            "gt_ignore_label": GT_IGNORE.get(dataset),
        }
        key = dataset.lower()
        path = args.out_dir / f"{key}.json"
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"[saved] {path} ({len(names)} classes)")


if __name__ == "__main__":
    main()