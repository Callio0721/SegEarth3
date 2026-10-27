#!/usr/bin/env python
"""Export baseline / ours label maps for the images listed in a manifest.

Examples:
    python tools/export_paper_predictions.py \
      --manifest tools/paper_results_manifest.server.csv \
      --mode baseline --overwrite

    python tools/export_paper_predictions.py \
      --manifest tools/paper_results_manifest.server.csv \
      --mode ours --overwrite

The script uses the frozen SAM3/SegEarth-OV3 configs. For the six fixed
datasets it runs the frozen `joint_residual` profile. For the four domain
extension datasets it runs the recorded best Role/View profile.
"""

from __future__ import annotations

import argparse
import csv
import os
import sys
from pathlib import Path

import numpy as np
import torch
from PIL import Image
from torchvision import transforms
from progress_utils import progress

# When launched as `python tools/export_paper_predictions.py`, Python puts
# `tools/` on sys.path rather than the repository root. Add the root so the
# repository-level modules and configs can be imported.
def _find_repo_root(start: Path) -> Path:
    for parent in [start, *start.parents]:
        if (parent / "segearthov3_segmentor.py").exists():
            return parent
    raise RuntimeError("Cannot locate repository root containing segearthov3_segmentor.py")

REPO_ROOT = _find_repo_root(Path(__file__).resolve().parent)
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

# Register the custom segmentor and datasets before building the model.
import segearthov3_segmentor  # noqa: F401
import custom_datasets  # noqa: F401
from mmengine.config import Config
from mmseg.registry import MODELS
from mmseg.structures import SegDataSample


DATASET_CONFIG = {
    "LoveDA": "configs/cfg_loveda.py",
    "OpenEarthMap": "configs/cfg_openearthmap.py",
    "Potsdam": "configs/cfg_potsdam.py",
    "Vaihingen": "configs/cfg_vaihingen.py",
    "iSAID": "configs/cfg_iSAID.py",
    "UAVid": "configs/cfg_uavid.py",
    "UDD5": "configs/cfg_udd5.py",
    "VDD": "configs/cfg_vdd.py",
    "VOC20": "configs/cfg_voc20.py",
    "Cityscapes": "configs/cfg_city_scapes.py",
}

DATASET_KEY = {
    "LoveDA": "loveda",
    "OpenEarthMap": "openearthmap",
    "Potsdam": "potsdam",
    "Vaihingen": "vaihingen",
    "iSAID": "isaid",
    "UAVid": "uavid",
    "UDD5": "udd5",
    "VDD": "vdd",
    "VOC20": "voc20",
    "Cityscapes": "cityscapes",
}

FIXED_JOINT_DATASETS = {"LoveDA", "OpenEarthMap", "Potsdam", "Vaihingen", "UDD5", "VDD"}

DOMAIN_PROFILE = {
    "UAVid": ("p2_s3_i1", "power4_g075"),
    "iSAID": ("p0_s3_i0", "logit_g050"),
    "VOC20": ("p1_s3_i0", "logit_g050"),
    "Cityscapes": ("p1_s2_i0", "global"),
}


def _role_options(dataset: str) -> dict:
    key = DATASET_KEY[dataset]
    if dataset in FIXED_JOINT_DATASETS:
        return {
            "use_role_prompt_tta": True,
            "dump_role_prompt_tta_stats": False,
            "role_prompt_tta_protocol": "role_functional_text_screen_v1",
            "role_prompt_tta_dataset_name": key,
            "role_prompt_tta_prompt_bank": f"configs/prompt_banks/role_functional_text_v2/{key}.json",
            "role_prompt_tta_selection_registry": "configs/experiments/role_text_selections_v1.json",
            "role_prompt_tta_visual_field_diagnosis": True,
            "role_prompt_tta_visual_field_registry": "configs/experiments/role_visual_field_v1.json",
            "role_prompt_tta_visual_field_mode": "joint_role_view_final",
            "role_prompt_tta_joint_final_registry": "configs/experiments/joint_role_view_final_v1.json",
            "role_prompt_tta_final_profile": "joint_residual",
            "role_prompt_tta_joint_role_only": False,
            "role_prompt_tta_strict_integrity": True,
            "role_prompt_tta_integrity_tolerance": 1e-5,
        }
    return {
        "use_role_prompt_tta": True,
        "dump_role_prompt_tta_stats": False,
        "role_prompt_tta_protocol": "role_functional_text_screen_v1",
        "role_prompt_tta_dataset_name": key,
        "role_prompt_tta_prompt_bank": f"configs/prompt_banks/role_functional_text_v3/{key}.json",
        "role_prompt_tta_selection_registry": "configs/experiments/role_text_domain_extension_v1.json",
        "role_prompt_tta_visual_field_diagnosis": True,
        "role_prompt_tta_visual_field_registry": "configs/experiments/role_visual_field_domain_extension_v1.json",
        "role_prompt_tta_visual_field_mode": "joint_role_view",
        "role_prompt_tta_joint_profile_registry": "configs/experiments/joint_role_view_domain_extension_v1.json",
        "role_prompt_tta_joint_role_only": False,
        "role_prompt_tta_strict_integrity": True,
        "role_prompt_tta_integrity_tolerance": 1e-5,
    }


def build_model(dataset: str, mode: str, device: str):
    if mode not in {"baseline", "ours"}:
        raise ValueError(f"Unknown mode: {mode}")
    cfg = Config.fromfile(DATASET_CONFIG[dataset])
    cfg.model["device"] = device
    if mode == "ours":
        cfg.model.update(_role_options(dataset))
    else:
        cfg.model["use_role_prompt_tta"] = False
        cfg.model["dump_role_prompt_tta_stats"] = False
    model = MODELS.build(cfg.model)
    model.eval()
    return model


def prepare_sample(image_path: Path, device: str):
    image = Image.open(image_path).convert("RGB")
    tensor = transforms.ToTensor()(image).unsqueeze(0).to(device)
    sample = SegDataSample()
    sample.set_metainfo({
        "img_path": str(image_path),
        "ori_shape": (image.height, image.width),
    })
    return image, tensor, sample


def threshold_prediction(score: torch.Tensor, prob_thd: float, bg_idx: int) -> np.ndarray:
    prediction = score.argmax(dim=0)
    prediction[score.max(dim=0)[0] < float(prob_thd)] = int(bg_idx)
    return prediction.detach().cpu().numpy().astype(np.int64)


def export_with_predict(model, image_path: Path, device: str) -> np.ndarray:
    _, tensor, sample = prepare_sample(image_path, device)
    output = model.predict(tensor, data_samples=[sample])[0]
    return output.pred_sem_seg.data.cpu().numpy().squeeze(0).astype(np.int64)


def export_domain_ours(model, image_path: Path, dataset: str, device: str) -> np.ndarray:
    image, _, _ = prepare_sample(image_path, device)
    candidate_id, operator_name = DOMAIN_PROFILE[dataset]
    official_query, bundle, metadata = model._rvf_predict_image(image, str(image_path))
    if candidate_id not in bundle["roles"]:
        available = ", ".join(bundle["roles"].keys())
        raise KeyError(f"{dataset}: candidate {candidate_id!r} not found. Available: {available}")
    endpoints = bundle["roles"][candidate_id]
    family, global_weight, rho = model._jrv_operator_spec(operator_name)
    score = model._jrv_fuse_views(
        endpoints["local"], endpoints["global_value"], family, global_weight, rho
    )
    return threshold_prediction(score, model.prob_thd, model.bg_idx)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", required=True, type=Path)
    parser.add_argument("--mode", choices=["baseline", "ours", "both"], required=True)
    parser.add_argument("--device", default="cuda")
    parser.add_argument("--datasets", nargs="*", default=None)
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument("--num-shards", type=int, default=1)
    parser.add_argument("--shard-id", type=int, default=0)
    args = parser.parse_args()

    # Config paths and SAM3 assets are relative to the repository root.
    os.chdir(REPO_ROOT)

    rows = list(csv.DictReader(args.manifest.open(encoding="utf-8-sig")))
    if args.datasets:
        wanted = {x.lower() for x in args.datasets}
        rows = [r for r in rows if r["dataset"].lower() in wanted]

    if args.num_shards < 1:
        raise ValueError("--num-shards must be >= 1")
    if not 0 <= args.shard_id < args.num_shards:
        raise ValueError("--shard-id must be in [0, num_shards)")
    rows = [row for index, row in enumerate(rows) if index % args.num_shards == args.shard_id]
    print(f"[shard] {args.shard_id}/{args.num_shards}: {len(rows)} rows")

    modes = ["baseline", "ours"] if args.mode == "both" else [args.mode]

    for mode in modes:
        # Cache one model per dataset; do not keep all SAM3 instances in memory.
        current_dataset = None
        model = None
        try:
            for row in progress(rows, total=len(rows), desc=f"{mode}"):
                dataset = row["dataset"]
                if dataset not in DATASET_CONFIG:
                    print(f"[skip] unknown dataset: {dataset}")
                    continue
                image_path = Path(row["image"])
                if not image_path.exists():
                    print(f"[skip] image not found: {image_path}")
                    continue

                if dataset != current_dataset:
                    if model is not None:
                        del model
                        torch.cuda.empty_cache()
                    print(f"[build] {dataset} / {mode}")
                    model = build_model(dataset, mode, args.device)
                    current_dataset = dataset

                out_path = Path(row[mode])
                if not args.overwrite and out_path.exists():
                    print(f"[skip] exists: {out_path}")
                    continue
                out_path.parent.mkdir(parents=True, exist_ok=True)

                if mode == "baseline":
                    mask = export_with_predict(model, image_path, args.device)
                elif dataset in FIXED_JOINT_DATASETS:
                    mask = export_with_predict(model, image_path, args.device)
                else:
                    mask = export_domain_ours(model, image_path, dataset, args.device)

                np.save(out_path, mask)
                print(f"[saved] {out_path} shape={mask.shape} classes={mask.max() + 1}")
        finally:
            if model is not None:
                del model
                torch.cuda.empty_cache()


if __name__ == "__main__":
    main()