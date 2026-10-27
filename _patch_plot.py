from pathlib import Path
import re

p = Path(r"D:\论文\9.27论文\SegEarth3-main\paper_figures_v2\tools\plot_paper_results.py")
s = p.read_text(encoding="utf-8")

read_palette = '''def _read_palette(path: Path | None, class_file: Path | None, dataset: str) -> Palette:
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

'''
s = re.sub(r"def _read_palette\(.*?\n\ndef _normalize_image", read_palette + "def _normalize_image", s, flags=re.S)

metric_funcs = '''def apply_gt_shift(labels: np.ndarray, palette: Palette) -> np.ndarray:
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
    classes = sorted(set(int(x) for x in np.unique(gt_valid)) | set(int(x) for x in np.unique(pred_valid)))
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


'''
s = re.sub(r"def apply_gt_shift\(.*?\n\ndef _present_labels", metric_funcs + "def _present_labels", s, flags=re.S)
p.write_text(s, encoding="utf-8")
print("patched plot functions")