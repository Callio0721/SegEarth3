"""Reassemble writing evidence without changing source files or rerunning inference."""
from pathlib import Path
import csv
import json

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'Astra_docs' / 'evidence'
OUT.mkdir(exist_ok=True)

def read(rel):
    with (ROOT / rel).open(newline='') as f:
        return list(csv.DictReader(f))

def write(name, rows):
    with (OUT / name).open('w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

paths = [
    'logs/joint_role_view_profile_v1_full_4b5363f/summary/joint_role_view_profiles.csv',
    'logs/uavid_joint_role_view_v1_full_f51f712/summary/joint_role_view_profiles.csv',
    'logs/isaid_joint_p0_s3_i0_v1_full_b7dae83/summary/joint_role_view_profiles.csv',
]
profiles = []
for path in paths:
    profiles.extend(dict(r, source_csv=path) for r in read(path))
write('selected_profiles.csv', profiles)
order = ['potsdam', 'vaihingen', 'loveda', 'isaid', 'openearthmap', 'uavid', 'udd5', 'vdd']
main = []
for dataset in order:
    rows = {r['profile']: r for r in profiles if r['dataset'] == dataset}
    baseline = rows['official']
    role = rows.get('role_only_best', rows['role_only'])
    joint = rows['joint_role_view_best']
    b, r, j = (float(x['miou']) for x in [baseline, role, joint])
    main.append(dict(dataset=dataset, baseline=b, role_only=r, joint=j,
                     role_gain=r-b, joint_over_role=j-r, total_gain=j-b,
                     joint_slots=joint['slots'], admission=joint['admission'],
                     operator=joint['operator'], source_csv=joint['source_csv']))
write('main_results.csv', main)

source = 'logs/role_text_completion_v1_full_99f03ff/summary/dataset_variants.csv'
source_rows = read(source)
shared = []
for dataset in order:
    rr = {r['variant']: r for r in source_rows if r['dataset'] == dataset}
    if not rr:
        continue
    baseline = float(rr['baseline']['miou'])
    for slot in range(1, 4):
        name = f'shared_semantic_s{slot}'
        shared_score = float(rr[name]['miou'])
        single = float(rr[f'combo_p0_s{slot}_i0']['miou'])
        shared.append(dict(dataset=dataset, semantic_slot=slot, baseline=baseline,
                           semantic_only=single, same_text_all_roles=shared_score,
                           shared_gain=shared_score-baseline,
                           semantic_only_minus_shared=single-shared_score,
                           source_csv=source))
write('shared_vs_role_text.csv', shared)

interactions = read('docs/论文框架/2026-09-03/matched_role_view_interactions.csv')
write('matched_interactions.csv', interactions)
macros = {k: sum(r[k] for r in main)/len(main)
          for k in ['baseline', 'role_only', 'joint', 'role_gain', 'joint_over_role', 'total_gain']}
macros['fixed_profile_role'] = sum(float(r['m10_role']) for r in interactions)/len(interactions)
macros['fixed_profile_view'] = sum(float(r['m01_view']) for r in interactions)/len(interactions)
macros['matched_interaction'] = sum(float(r['role_view_interaction']) for r in interactions)/len(interactions)
macros['shared_text_positive_cases'] = sum(r['shared_gain'] > 0 for r in shared)
macros['shared_text_total_cases'] = len(shared)
(OUT / 'statistics.json').write_text(json.dumps(macros, indent=2), encoding='utf-8')
print(json.dumps(macros, indent=2))
