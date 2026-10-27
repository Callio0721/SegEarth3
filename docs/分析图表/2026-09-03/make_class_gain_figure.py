"""Reproduce the class-gain figure from returned, full-split summaries.

Local analysis artifact only; does not alter model code or predictions.
Run: python make_class_gain_figure.py --repo /path/to/SegEarth3
Requires: numpy, scipy, matplotlib.
"""
import argparse
import csv
import hashlib
import json
import os
from pathlib import Path

os.environ.setdefault('MPLCONFIGDIR', '/tmp/segearth-class-gain-mpl')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import spearmanr


SOURCES = [
    'joint_role_view_profile_v1_full_4b5363f',
    'uavid_joint_role_view_v1_full_f51f712',
    'isaid_joint_p0_s3_i0_v1_full_b7dae83',
]
DATASETS = [
    ('loveda', 'LoveDA', '#4477AA', 'o'),
    ('openearthmap', 'OpenEarthMap', '#CC6677', 's'),
    ('potsdam', 'Potsdam', '#228833', '^'),
    ('vaihingen', 'Vaihingen', '#AA3377', 'D'),
    ('uavid', 'UAVid', '#EE7733', 'v'),
    ('isaid', 'iSAID', '#66AABB', 'P'),
    ('udd5', 'UDD5', '#997700', 'X'),
    ('vdd', 'VDD', '#555555', '>'),
]


def load_data(repo):
    result, provenance = [], []
    for source in SOURCES:
        rel = f'logs/{source}/summary/joint_role_view_classes.csv'
        path = repo / rel
        with path.open(newline='', encoding='utf-8-sig') as stream:
            records = list(csv.DictReader(stream))
        base = {(r['dataset'], r['class_index']): r for r in records
                if r['profile'] == 'official'}
        for row in records:
            if row['profile'] != 'joint_role_view_best':
                continue
            original = base[row['dataset'], row['class_index']]
            b = 100.0 * float(original['iou'])
            j = 100.0 * float(row['iou'])
            result.append(dict(
                dataset=row['dataset'], class_index=int(row['class_index']),
                class_name=row['class_name'], baseline_iou=b, joint_iou=j,
                joint_delta_iou=j-b, baseline_variant=original['variant'],
                joint_variant=row['variant'], source_csv=rel,
            ))
        provenance.append(dict(path=rel, sha256=hashlib.sha256(
            path.read_bytes()).hexdigest()))
    assert len(result) == 63
    assert len({(r['dataset'], r['class_index']) for r in result}) == 63
    return result, provenance


def statistics(rows):
    x = np.array([r['baseline_iou'] for r in rows])
    y = np.array([r['joint_delta_iou'] for r in rows])
    bins = []
    for name, mask in [('below_30', x < 30),
                       ('30_to_60', (x >= 30) & (x < 60)),
                       ('60_and_above', x >= 60)]:
        bins.append(dict(name=name, count=int(mask.sum()),
                         baseline_mean=float(x[mask].mean()),
                         delta_mean=float(y[mask].mean()),
                         delta_median=float(np.median(y[mask]))))
    return dict(n=len(rows), improved=int((y > 0).sum()),
                harmed=int((y < 0).sum()), pearson=float(np.corrcoef(x, y)[0, 1]),
                spearman=float(spearmanr(x, y).statistic),
                mean_delta=float(y.mean()), bins=bins)


def make_figure(rows, stats, out):
    plt.rcParams.update({
        'font.family': 'DejaVu Sans', 'font.size': 8.5,
        'axes.labelsize': 9, 'axes.titlesize': 10,
        'axes.linewidth': 0.75, 'xtick.labelsize': 8, 'ytick.labelsize': 8,
        'pdf.fonttype': 42, 'ps.fonttype': 42, 'svg.fonttype': 'none',
        'savefig.facecolor': 'white',
    })
    fig = plt.figure(figsize=(7.6, 4.55), facecolor='white')
    grid = fig.add_gridspec(2, 2, left=.088, right=.983, bottom=.225,
                           top=.88, width_ratios=[2.32, 1],
                           height_ratios=[.60, 2.45], hspace=.08, wspace=.30)
    upper = fig.add_subplot(grid[0, 0])
    lower = fig.add_subplot(grid[1, 0], sharex=upper)
    bars = fig.add_subplot(grid[:, 1])
    upper.set_ylim(52, 64)
    lower.set_ylim(-6, 24)
    lower.set_xlim(-2, 101)
    upper.set_yticks([55, 60])
    lower.set_yticks([-5, 0, 5, 10, 15, 20])
    lower.set_xticks([0, 20, 40, 60, 80, 100])
    upper.tick_params(axis='x', which='both', bottom=False, labelbottom=False)
    for ax in (upper, lower):
        ax.spines[['right', 'top']].set_visible(False)
        ax.grid(axis='y', color='#D7DDE2', linewidth=.5, alpha=.65)
        ax.set_axisbelow(True)
        ax.axvspan(0, 30, color='#F0F7F7', zorder=0)
        ax.axvspan(30, 60, color='#F7F9FB', zorder=0)
    upper.spines['bottom'].set_visible(False)
    # A visible axis break preserves the large OEM background gain without
    # compressing the other 62 observations or deleting the outlier.
    d = .008
    for ax, y in [(upper, 0), (lower, 1)]:
        ax.plot((-d, d), (y-d, y+d), transform=ax.transAxes,
                color='#303840', lw=.9, clip_on=False)
    legend = []
    for key, label, color, marker in DATASETS:
        rs = [r for r in rows if r['dataset'] == key]
        x = [r['baseline_iou'] for r in rs]
        y = [r['joint_delta_iou'] for r in rs]
        for ax in (upper, lower):
            obj = ax.scatter(x, y, s=32, marker=marker, c=color,
                             edgecolors='white', linewidths=.5, alpha=.88,
                             zorder=4, label=label)
        legend.append(obj)
    lower.axhline(0, color='#5B6269', lw=.9, ls=(0, (4, 3)), zorder=2)
    x = np.array([r['baseline_iou'] for r in rows])
    y = np.array([r['joint_delta_iou'] for r in rows])
    fit = np.polyfit(x, y, 1)
    lower.plot([0, 100], np.polyval(fit, [0, 100]),
               color='#253B4C', lw=1.25, ls=(0, (5, 3)), zorder=3)
    lower.text(.98, .93,
               f"Pearson r = {stats['pearson']:.2f}\n"
               f"Spearman ρ = {stats['spearman']:.2f}",
               ha='right', va='top', transform=lower.transAxes,
               color='#253B4C', fontsize=8,
               bbox=dict(facecolor='white', edgecolor='none', alpha=.88, pad=2))
    oem = next(r for r in rows if r['dataset'] == 'openearthmap'
               and r['class_name'] == 'background')
    upper.annotate(f"OEM background  +{oem['joint_delta_iou']:.2f}",
                   xy=(oem['baseline_iou'], oem['joint_delta_iou']),
                   xytext=(38, 59.5), color='#943C4A', fontsize=8,
                   arrowprops=dict(arrowstyle='-', color='#943C4A', lw=.65),
                   va='center')
    upper.text(1, .0, 'y-axis break', transform=upper.transAxes,
               ha='right', va='bottom', fontsize=6.8, color='#707880')
    lower.set_xlabel('Baseline class IoU (%)', labelpad=6)
    fig.text(.017, .55, 'Joint ΔIoU (percentage points)',
             rotation=90, ha='center', va='center', fontsize=9)
    upper.set_title('(a) All 63 dataset–class pairs', loc='left', pad=12,
                    fontweight='bold')
    means = [b['delta_mean'] for b in stats['bins']]
    bar_colors = ['#008F91', '#56B0B1', '#A9D8D7']
    bars.bar(np.arange(3), means, color=bar_colors, width=.60,
             edgecolor='white', linewidth=.6, zorder=3)
    for k, (value, group) in enumerate(zip(means, stats['bins'])):
        bars.text(k, value+.18, f'+{value:.2f}', ha='center', va='bottom',
                  fontsize=10, fontweight='bold', color='#006F72')
    bars.set_xticks([0, 1, 2], [
        f"{label}\nn = {group['count']}" for label, group in
        zip(['<30', '30–60', '≥60'], stats['bins'])])
    bars.set_ylim(0, 9.4)
    bars.set_yticks([0, 2, 4, 6, 8])
    bars.spines[['right', 'top']].set_visible(False)
    bars.tick_params(axis='x', length=0, pad=5)
    bars.grid(axis='y', color='#D7DDE2', linewidth=.5, zorder=0)
    bars.set_axisbelow(True)
    bars.set_title('(b) Mean ΔIoU', loc='left', pad=12,
                   fontweight='bold')
    bars.set_xlabel('Baseline class IoU (%)', labelpad=7)
    bars.text(.5, .98, f"{stats['improved']}/63 classes improve",
              ha='center', va='top', transform=bars.transAxes,
              fontsize=8.5, color='#253B4C')
    fig.legend(handles=legend, labels=[d[1] for d in DATASETS], ncol=4,
               loc='lower center', bbox_to_anchor=(.52, .052), frameon=False,
               columnspacing=1.45, handletextpad=.45, fontsize=8)
    fig.text(.5, .023, 'Eight remote-sensing datasets · Full evaluation splits '
             '· Equal weight per dataset–class pair',
             ha='center', fontsize=7.2, color='#66747E')
    for ext in ('pdf', 'svg', 'png'):
        fig.savefig(out/f'baseline_vs_joint_class_gain.{ext}', dpi=600)
    plt.close(fig)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--repo', type=Path, default=Path(__file__).resolve().parents[3])
    args = parser.parse_args()
    out = Path(__file__).resolve().parent
    rows, provenance = load_data(args.repo)
    with (out/'class_gain_data.csv').open('w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    overall = statistics(rows)
    control = statistics([r for r in rows if not (
        r['dataset'] == 'openearthmap' and r['class_name'] == 'background')])
    foreground = statistics([r for r in rows
                             if r['class_name'] not in ('background', 'clutter')])
    result = dict(all_remote_classes=overall,
                  without_oem_background=control,
                  without_background_or_clutter=foreground,
                  sources=provenance,
                  units='IoU in percent; delta in percentage points',
                  note='Descriptive association, not a causal or significance claim. '
                       'All plotted observations retained; display uses a marked y-axis break.')
    (out/'class_gain_statistics.json').write_text(
        json.dumps(result, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    make_figure(rows, overall, out)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
