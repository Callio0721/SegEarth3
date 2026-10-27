from pathlib import Path
p=Path(r"D:\论文\9.27论文\SegEarth3-main\paper_figures_v2\tools\plot_paper_results.py")
s=p.read_text(encoding="utf-8")
s=s.replace('    classes = sorted(set(int(x) for x in np.unique(gt_valid)) | set(int(x) for x in np.unique(pred_valid)))', '    classes = sorted(set(int(x) for x in np.unique(gt_valid)))')
p.write_text(s,encoding="utf-8")
print("per-image mIoU now averages GT-present classes")