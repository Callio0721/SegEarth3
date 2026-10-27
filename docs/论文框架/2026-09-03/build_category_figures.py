"""Local paper figures from existing full-evaluation summaries; no inference."""
import csv
import hashlib
import json
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
FIG = ROOT / 'output/pdf/category_evidence_20260903'
SOURCES = [
    ROOT / 'logs/joint_role_view_profile_v1_full_4b5363f/summary',
    ROOT / 'logs/uavid_joint_role_view_v1_full_f51f712/summary',
    ROOT / 'logs/isaid_joint_p0_s3_i0_v1_full_b7dae83/summary',
]
GROUPS = {
    'Water-related': {'water', 'swimming pool'},
    'Vegetation & land cover': {'bareland', 'barren', 'grass', 'tree', 'cropland',
                                 'forest', 'agricultural', 'vegetation'},
    'Built structures': {'building', 'facade', 'roof', 'store tank', 'bridge', 'harbor'},
    'Movable objects': {'car', 'vehicle', 'human', 'ship', 'large vehicle',
                       'small vehicle', 'helicopter', 'plane'},
    'Transport surfaces': {'road', 'pavement', 'roundabout'},
    'Sports grounds': {'baseball diamond', 'tennis court', 'basketball court',
                      'ground track field', 'soccer ball field'},
    'Background / clutter': {'background', 'clutter'},
}
PURPLE, TEAL, INK, GRAY = '#8A5AB5', '#008F91', '#16384C', '#7F8B94'


def read_csv(path):
    with path.open(newline='') as f:
        return list(csv.DictReader(f))


def save_csv(name, rows):
    with (OUT / name).open('w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)


def collect():
    records, interactions, hashes = [], [], {}
    for source in SOURCES:
        path = source / 'joint_role_view_classes.csv'
        hashes[str(path.relative_to(ROOT))] = hashlib.sha256(path.read_bytes()).hexdigest()
        classes = read_csv(path)
        profiles = read_csv(source / 'joint_role_view_profiles.csv')
        inter = read_csv(source / 'joint_role_view_interactions.csv')
        datasets = list(dict.fromkeys(r['dataset'] for r in classes))
        for ds in datasets:
            subset = [r for r in classes if r['dataset'] == ds]
            role_profile = ('role_only_best' if any(r['profile'] == 'role_only_best'
                                                   for r in subset) else 'role_only')
            by_profile = {p: {int(r['class_index']): r for r in subset if r['profile'] == p}
                          for p in ('official', role_profile, 'joint_role_view_best')}
            for k, base in by_profile['official'].items():
                role, joint = by_profile[role_profile][k], by_profile['joint_role_view_best'][k]
                group = next(g for g, names in GROUPS.items() if base['class_name'] in names)
                b, r, j = [float(x['iou']) * 100 for x in (base, role, joint)]
                records.append(dict(dataset=ds, class_index=k, class_name=base['class_name'],
                    category_group=group, baseline_iou=b, role_iou=r, joint_iou=j,
                    role_delta=r-b, joint_delta=j-b, joint_minus_role=j-r,
                    role_variant=role['variant'], joint_variant=joint['variant'],
                    source_csv=str(path.relative_to(ROOT))))
            winner = next(r for r in profiles if r['dataset'] == ds
                          and r['profile'] == 'joint_role_view_best')
            matched = [r for r in inter if r['dataset'] == ds
                       and r['candidate_id'] == winner['candidate_id']
                       and r['admission'] == winner['admission']
                       and r['operator'] == winner['operator']]
            row = dict(matched[0])
            baseline = np.mean([float(r['iou'])*100 for r in by_profile['official'].values()])
            row.update(m00_baseline=baseline,
                       m10_role=baseline+float(row['role_main_effect']),
                       m01_view=baseline+float(row['view_main_effect']),
                       m11_joint=float(row['miou']))
            row['source_csv'] = str((source / 'joint_role_view_interactions.csv').relative_to(ROOT))
            interactions.append(row)
    groups = []
    for group in GROUPS:
        rows = [r for r in records if r['category_group'] == group]
        groups.append(dict(category_group=group, n=len(rows),
            positive_joint=sum(r['joint_delta'] > 0 for r in rows),
            baseline_mean=np.mean([r['baseline_iou'] for r in rows]),
            role_delta_mean=np.mean([r['role_delta'] for r in rows]),
            joint_delta_mean=np.mean([r['joint_delta'] for r in rows]),
            joint_minus_role_mean=np.mean([r['joint_minus_role'] for r in rows]),
            joint_delta_median=np.median([r['joint_delta'] for r in rows])))
    stats = dict(n_dataset_class_pairs=len(records), n_foreground=sum(r['category_group'] !=
        'Background / clutter' for r in records), group_definitions={k: sorted(v) for k,v in GROUPS.items()},
        weighting='Equal weight per dataset-class pair; not the eight-dataset macro mIoU.',
        role_reference='Best Role-only profile in the matched source summaries.',
        view_increment='Joint minus best Role-only; not a factorial interaction.',
        interaction='Same candidate/admission/operator: m11-m10-m01+m00, copied from verified summaries.',
        source_sha256=hashes, groups=groups)
    save_csv('category_class_data.csv', records)
    save_csv('category_group_summary.csv', groups)
    save_csv('matched_role_view_interactions.csv', interactions)
    (OUT / 'category_statistics.json').write_text(json.dumps(stats, ensure_ascii=False, indent=2)+'\n')
    return records, groups


def style(ax):
    ax.spines[['top', 'right', 'left']].set_visible(False)
    ax.spines['bottom'].set_color('#CAD2D7')
    ax.tick_params(axis='both', length=0, colors=INK, labelsize=9)
    ax.xaxis.grid(True, color='#E8EDF0', linewidth=.6, zorder=0)
    ax.set_axisbelow(True)


def export(fig, stem):
    for suffix in ('pdf', 'svg', 'png'):
        fig.savefig(FIG / f'{stem}.{suffix}', dpi=500, facecolor='white', bbox_inches='tight')
    plt.close(fig)


def plot(records, groups):
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,
                         'pdf.fonttype':42,'ps.fonttype':42,'svg.fonttype':'none'})
    fig,ax=plt.subplots(figsize=(11.4,4.1))
    fig.subplots_adjust(left=.075,right=.99,bottom=.21,top=.83)
    x=np.arange(len(groups)); width=.32
    for offset,key,color,label in [(-.19,'role_delta_mean',PURPLE,'Role Text'),
            (.19,'joint_delta_mean',TEAL,'Role Text + View')]:
        values=[g[key] for g in groups]
        bars=ax.bar(x+offset,values,width,color=color,label=label,zorder=3)
        for bar,value in zip(bars,values):
            ax.text(bar.get_x()+width/2,value+(.18 if value>=0 else -.15),
                    f'{value:+.2f}',ha='center',va='bottom' if value>=0 else 'top',
                    fontsize=10,color=color,fontweight='semibold')
    ax.set_xticks(x,['Water-related','Vegetation &\nland cover','Built\nstructures',
                    'Movable\nobjects','Transport\nsurfaces','Sports\ngrounds','Background /\nclutter'])
    ax.set_ylabel('Mean IoU gain over baseline (pp)',fontsize=11,color=INK)
    ax.set_ylim(-.65,11.5);ax.set_yticks(np.arange(0,12,2))
    ax.spines[['top','right','left']].set_visible(False)
    ax.spines['bottom'].set_color('#aab5bc')
    ax.tick_params(length=0,pad=8,labelsize=10,colors=INK)
    ax.yaxis.grid(True,color='#e5e9ec',lw=.7);ax.set_axisbelow(True)
    ax.axhline(0,color='#83929c',lw=.8,zorder=2)
    ax.legend(loc='upper left',bbox_to_anchor=(0,1.22),frameon=False,ncol=2,
              fontsize=11,handlelength=1.2,columnspacing=2)
    export(fig,'category_structured_gains')


if __name__ == '__main__':
    FIG.mkdir(parents=True,exist_ok=True)
    records, groups = collect()
    plot(records, groups)
    for g in groups:
        print(g)
    print('Figure directory:',FIG)
