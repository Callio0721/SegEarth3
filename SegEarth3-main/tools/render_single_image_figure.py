#!/usr/bin/env python
"""Single-image qualitative figure for Joint Role--View (paper use).

One audit-mode forward pass yields the official baseline map and every
registered profile map from the same evidence bank, so the baseline and our
method come from one run and are directly comparable.

Example:
    python tools/render_single_image_figure.py --img /path/to/openearthmap_val_0007.tif --dataset openearthmap --out paper_figs/qualitative_oem

Writes <out>.pdf, <out>.svg and <out>.png next to each other.
"""
import argparse
import os

import numpy as np
import torch
import torch.nn.functional as F
from PIL import Image
import sys

# Allow `python tools/render_single_image_figure.py` from the repository root:
# the script lives in tools/, so the project modules are not on sys.path by default.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from mmengine.config import Config
from mmseg.registry import DATASETS, MODELS

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

import custom_datasets  # noqa: F401  registers the custom datasets
import segearthov3_segmentor  # noqa: F401  registers the segmentor


DATASET_TYPES = {
    'openearthmap': 'OpenEarthMapDataset',
    'udd5': 'UDD5Dataset',
    'vdd': 'VDDDataset',
    'vaihingen': 'ISPRSDataset',
    'potsdam': 'PotsdamDataset',
    'loveda': 'LoveDADataset',
}
SCREEN_CONFIG = 'configs/experiments/cfg_{dataset}_role_functional_text_screen.py'
PROMPT_BANK = 'configs/prompt_banks/role_functional_text_v2/{dataset}.json'
SELECTION_REGISTRY = 'configs/experiments/role_text_selections_v1.json'
VISUAL_FIELD_REGISTRY = 'configs/experiments/role_visual_field_v1.json'
FINAL_REGISTRY = 'configs/experiments/joint_role_view_final_v1.json'


def parse_args():
    parser = argparse.ArgumentParser(
        description='Render one qualitative Joint Role--View figure.')
    parser.add_argument('--img', required=True, help='input image path')
    parser.add_argument('--dataset', required=True, choices=sorted(DATASET_TYPES),
                        help='dataset whose frozen registries the image belongs to')
    parser.add_argument('--out', default='paper_figs/qualitative',
                        help='output stem; .pdf/.svg/.png are appended')
    parser.add_argument('--profile', default='joint_residual',
                        help="profile to show as ours (default: primary 'joint_residual')")
    parser.add_argument('--gt', default=None,
                        help='optional ground-truth label map (.tif/.png, integer ids)')
    parser.add_argument('--device', default='cuda')
    parser.add_argument('--max-side', type=int, default=1600,
                        help='downscale only for display; 0 keeps full resolution')
    parser.add_argument('--no-baseline', action='store_true',
                        help='omit the official baseline panel')
    return parser.parse_args()


def build_model(dataset, device):
    """Build the segmentor in audit mode: one forward, all profiles."""
    cfg = Config.fromfile(SCREEN_CONFIG.format(dataset=dataset))
    cfg.model.update(dict(
        device=device,
        role_prompt_tta_prompt_bank=PROMPT_BANK.format(dataset=dataset),
        role_prompt_tta_selection_registry=SELECTION_REGISTRY,
        role_prompt_tta_visual_field_diagnosis=True,
        role_prompt_tta_visual_field_mode='joint_role_view_final',
        role_prompt_tta_visual_field_registry=VISUAL_FIELD_REGISTRY,
        role_prompt_tta_joint_final_registry=FINAL_REGISTRY,
        role_prompt_tta_final_profile='audit',
        dump_role_prompt_tta_stats=False,
        role_prompt_tta_save_npz=False,
    ))
    model = MODELS.build(cfg.model)
    model.eval()
    return model


def to_label(class_logits, prob_thd, bg_idx=0):
    score, label = class_logits.max(dim=0)
    label = label.clone()
    label[score < float(prob_thd)] = int(bg_idx)
    return label.cpu().numpy()


def colorize(label, palette):
    pal = np.asarray(palette, dtype=np.uint8)
    return pal[np.clip(label.astype(np.int64), 0, len(pal) - 1)]


def fit(image, max_side):
    if max_side and max(image.size) > max_side:
        scale = max_side / float(max(image.size))
        return image.resize(
            (max(1, int(image.width * scale)), max(1, int(image.height * scale))),
            Image.NEAREST)
    return image


def main():
    args = parse_args()
    os.makedirs(os.path.dirname(os.path.abspath(args.out)) or '.', exist_ok=True)

    model = build_model(args.dataset, args.device)
    image = Image.open(args.img).convert('RGB')
    image_path = os.path.abspath(args.img)

    with torch.no_grad():
        official_query, bundle, metadata = model._rvf_predict_image(image, image_path)
        class_logits = model._aggregate_query_logits_to_classes(official_query)
        original_shape = (image.height, image.width)
        if tuple(class_logits.shape[-2:]) != original_shape:
            class_logits = F.interpolate(
                class_logits.unsqueeze(0), size=original_shape,
                mode='bilinear', align_corners=False).squeeze(0)
            bundle = model._rvf_resize_variants(bundle, original_shape)

    profiles = bundle['profiles']
    if args.profile not in profiles:
        raise SystemExit(
            'profile %r not available; choices: %s'
            % (args.profile, ', '.join(profiles)))

    prob_thd = float(getattr(model, 'prob_thd', 0.1))
    bg_idx = int(getattr(model, 'bg_idx', 0))
    baseline = to_label(class_logits, prob_thd, bg_idx)
    ours = to_label(profiles[args.profile], prob_thd, bg_idx)

    changed = float((baseline != ours).mean()) * 100.0
    print('[profile] %s' % args.profile)
    print('[available] %s' % ', '.join(profiles))
    print('[identity] reference vs official max abs = %.3e'
          % metadata.get('reference_identity_max_abs', float('nan')))
    print('[changed] baseline vs ours = %.2f%% of pixels' % changed)

    meta = DATASETS.get(DATASET_TYPES[args.dataset]).METAINFO
    palette = meta.get('palette')
    classes = list(meta.get('classes', []))
    if not palette:
        raise SystemExit('no palette registered for %s' % args.dataset)

    gt = None
    if args.gt:
        gt = np.asarray(Image.open(args.gt)).astype(np.int64)

    panels = [('Input', np.asarray(image.convert('RGB')))]
    if not args.no_baseline:
        panels.append(('Baseline (SegEarth-OV3)', colorize(baseline, palette)))
    panels.append(('Ours (%s)' % args.profile, colorize(ours, palette)))
    if gt is not None:
        panels.append(('Ground truth', colorize(gt, palette)))

    fig, axes = plt.subplots(1, len(panels), figsize=(3.1 * len(panels), 3.6),
                             dpi=200)
    for ax, (title, canvas) in zip(np.atleast_1d(axes), panels):
        ax.imshow(fit(Image.fromarray(np.asarray(canvas)), args.max_side))
        ax.set_title(title, fontsize=11)
        ax.set_xticks([])
        ax.set_yticks([])
        for spine in ax.spines.values():
            spine.set_visible(False)
    handles = [Patch(facecolor=np.asarray(palette, dtype=np.uint8)[i] / 255.0,
                     edgecolor='none', label=name)
               for i, name in enumerate(classes) if i < len(palette)]
    fig.legend(handles=handles, loc='lower center', ncol=min(len(handles), 6),
               frameon=False, fontsize=9)
    fig.tight_layout(rect=(0, 0.10, 1, 1))

    stem = args.out[:-4] if args.out.lower().endswith('.png') else args.out
    for suffix in ('pdf', 'svg', 'png'):
        fig.savefig('%s.%s' % (stem, suffix), bbox_inches='tight')
    plt.close(fig)
    print('[saved] %s.{pdf,svg,png}' % stem)


if __name__ == '__main__':
    main()
