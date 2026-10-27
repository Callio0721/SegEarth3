from pathlib import Path
p=Path(r"D:\论文\9.27论文\SegEarth3-main\paper_figures_v2\tools\plot_paper_results.py")
s=p.read_text(encoding="utf-8")
s=s.replace('            baseline_title += f"\\n{t[\'miou\']} {baseline_score:.3f}"', '            baseline_title += f"\\nImage {t[\'miou\']} {baseline_score:.3f}"')
s=s.replace('            ours_title += f"\\n{t[\'miou\']} {ours_score:.3f}"', '            ours_title += f"\\nImage {t[\'miou\']} {ours_score:.3f}"')
old='    handles = _legend_handles(ids, palette)\n'
new='''    handles = _legend_handles(ids, palette)
    if masks[2] is not None and np.any(masks[2] < 0):
        from matplotlib.patches import Patch
        ignore_color = palette.ignore_color if palette.ignore_color is not None else np.asarray([245, 245, 245], dtype=np.uint8)
        handles.append(Patch(facecolor=ignore_color.astype(np.float32) / 255.0,
                             edgecolor="none", label=TEXT[args.lang]["ignore"]))
'''
s=s.replace(old,new,1)
p.write_text(s,encoding="utf-8")
print("patched title and ignore legend")