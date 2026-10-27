"""Read existing research evidence; write only within Astra_docs."""
from pathlib import Path
import csv
import json
import re
import zipfile
import xml.etree.ElementTree as ET

from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'Astra_docs'
WORK = OUT / '_work'
WORK.mkdir(parents=True, exist_ok=True)

papers = {
    'SegEarth-OV': ('08_遥感域专门化与泛化/SegEarth-OV_2410.01768.pdf', 4),
    'TMPA': ('07_测试时适应校准与可靠性诊断/TMPA_CVPR2026.pdf', 4),
    'ReAttnCLIP': ('03_视觉语言对齐与稠密表征/ReAttnCLIP_CVPR2026.pdf', 3),
    'GLA-CLIP': ('05_场景上下文多视野与跨图证据/GLA-CLIP_CVPR2026.pdf', 2),
    'PEARL': ('03_视觉语言对齐与稠密表征/PEARL_CVPR2026.pdf', 3),
    'OV-Stitcher': ('05_场景上下文多视野与跨图证据/OV-Stitcher_CVPRF2026.pdf', 4),
    'SegEarth-OV3': ('01_基础模型与OVSS主架构/SegEarth-OV3_2512.08730v2.pdf', 2),
    'ProC-SAM3': ('02_文本概念表示与Prompt适配/ProC-SAM3_2606.21863.pdf', 2),
    'ConceptBank': ('06_检索原型记忆与外部知识/ConceptBank_2602.06333.pdf', 2),
}

paper_out = WORK / 'paper_extracts'
paper_out.mkdir(exist_ok=True)
paper_records = []
for name, (rel, render_page) in papers.items():
    path = ROOT / '参考论文' / rel
    reader = PdfReader(path)
    pages = [p.extract_text() or '' for p in reader.pages]
    (paper_out / f'{name}.txt').write_text('\n\n'.join(
        f'=== PDF PAGE {i+1} ===\n{t}' for i, t in enumerate(pages)), encoding='utf-8')
    headings = []
    for i, text in enumerate(pages[:9]):
        for line in text.splitlines():
            s = line.strip()
            if re.match(r'^(?:[1-6](?:\.[1-9])?\.?\s+[A-Z]|[IVX]+\.\s+[A-Z])', s):
                if len(s) < 115:
                    headings.append([i+1, s])
    paper_records.append(dict(name=name, source=str(path.relative_to(ROOT)),
                              pages=len(pages), headings=headings, render_page=render_page+1))
(WORK / 'paper_structure.json').write_text(json.dumps(paper_records, ensure_ascii=False, indent=2), encoding='utf-8')

profiles_paths = [
    'logs/joint_role_view_profile_v1_full_4b5363f/summary/joint_role_view_profiles.csv',
    'logs/uavid_joint_role_view_v1_full_f51f712/summary/joint_role_view_profiles.csv',
    'logs/isaid_joint_p0_s3_i0_v1_full_b7dae83/summary/joint_role_view_profiles.csv',
]
profiles = []
for rel in profiles_paths:
    with (ROOT / rel).open(newline='') as f:
        for row in csv.DictReader(f):
            row['source_csv'] = rel
            profiles.append(row)
print('PROFILE KEYS:', sorted({r['profile'] for r in profiles}))

data_dir = OUT / 'evidence'
data_dir.mkdir(exist_ok=True)
selected = [r for r in profiles if r['profile'] in {
    'official', 'role_only', 'role_only_best', 'joint_role_view_best',
    'view_only_best', 'sequential_role_view'}]
keys = sorted(set().union(*(r.keys() for r in selected)))
with (data_dir / 'selected_profiles.csv').open('w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=keys)
    w.writeheader()
    w.writerows(selected)
with (ROOT / 'docs/论文框架/2026-09-03/matched_role_view_interactions.csv').open(newline='') as f:
    interactions = list(csv.DictReader(f))
print('MATCHED INTERACTIONS:')
for r in interactions:
    print(r['dataset'], *(f'{float(r[k]):.6f}' for k in ['m00_baseline','m10_role','m01_view','m11_joint','role_view_interaction']))
print('MACRO:', {k: sum(float(r[k]) for r in interactions)/len(interactions) for k in ['m00_baseline','m10_role','m01_view','m11_joint','role_view_interaction']})
with (data_dir / 'matched_interactions.csv').open('w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=interactions[0].keys())
    w.writeheader()
    w.writerows(interactions)

deck = ROOT / 'docs/导师汇报/2026-08-23/导师汇报_研究进展_最终版.pptx'
ns = {'a':'http://schemas.openxmlformats.org/drawingml/2006/main'}
slides = []
with zipfile.ZipFile(deck) as z:
    names = sorted((n for n in z.namelist() if re.match(r'ppt/slides/slide\d+\.xml$', n)),
                   key=lambda n:int(re.search(r'slide(\d+)',n).group(1)))
    for n in names:
        node = ET.fromstring(z.read(n))
        words = [t.text for t in node.findall('.//a:t',ns) if t.text]
        slides.append(f'=== {n} ===\n'+'\n'.join(words))
(WORK / 'existing_ppt_text.txt').write_text('\n\n'.join(slides), encoding='utf-8')
print('PPT slides:', len(slides))

inventory = {}
for name in ['configs','tools','sam3','logs','docs','参考论文','tests','3d','tmp','weights','output']:
    d = ROOT/name
    counts = {}
    for p in d.rglob('*'):
        if p.is_file():
            suffix = p.suffix.lower() or '(no extension)'
            counts[suffix] = counts.get(suffix,0)+1
    inventory[name] = counts
(WORK / 'inventory.json').write_text(json.dumps(inventory,ensure_ascii=False,indent=2),encoding='utf-8')
print('Inventory file counts:',{k:sum(v.values()) for k,v in inventory.items()})

import pypdfium2 as pdfium
from PIL import Image, ImageDraw
tiles=[]
for name, (rel, page) in list(papers.items())[:6]:
    doc=pdfium.PdfDocument(str(ROOT/'参考论文'/rel))
    im=doc[page].render(scale=1.15).to_pil().convert('RGB')
    im.thumbnail((620,820))
    tile=Image.new('RGB',(650,880),'white')
    tile.paste(im,((650-im.width)//2,40))
    ImageDraw.Draw(tile).text((20,12),f'{name} | PDF p{page+1}',fill='black')
    tiles.append(tile)
sheet=Image.new('RGB',(650*3,880*2),'#eeeeee')
for i,im in enumerate(tiles):
    sheet.paste(im,((i%3)*650,(i//3)*880))
sheet.save(WORK/'cvpr_method_pages.png')
print('Paper extraction and sampled layout preview complete.')
