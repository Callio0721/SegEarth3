"""Produce bounded, source-linked reading packets and visual previews."""
from pathlib import Path
import json
import re
import sys
import html
from pypdf import PdfReader

ROOT=Path(__file__).resolve().parents[1]
WORK=ROOT/'_work'/'cvpr50'

def flat(t):return re.sub(r'\s+',' ',t).strip()

def prepare():
    rows=json.loads((WORK/'manifest.json').read_text())
    out=[]
    for row in rows:
        if not row.get('verified'):continue
        pdf=PdfReader(WORK/f"{row['id']}.pdf")
        pages=[(p.extract_text() or '').encode('utf-8','replace').decode('utf-8') for p in pdf.pages]
        (WORK/f"{row['id']}.txt").write_text('\n\n'.join(f'=== PAGE {i+1} ===\n{t}' for i,t in enumerate(pages)))
        text='\n'.join(pages[:8])
        heads=[]
        for i,p in enumerate(pages[:8]):
            for line in p.splitlines():
                if re.match(r'^\d+\.(?:\d+\.?\s*|\s+)[A-Za-z]',line) and len(line)<115:
                    heads.append([i+1,line.strip()])
        pagehtml=(WORK/f"{row['id']}.html").read_text()
        abs_match=re.search(r'<div id="abstract"[^>]*>(.*?)</div>',pagehtml,re.S)
        abstract=flat(html.unescape(re.sub('<[^>]+>',' ',abs_match.group(1)))) if abs_match else ''
        def snippet(pattern,n):
            m=re.search(pattern,text,re.M|re.I)
            return flat(text[m.start():m.start()+n]) if m else '[heading not extracted]'
        related=snippet(r'^\d+\.\s*Related\s*Work',700)
        method=snippet(r'^\d+\.\s*(?:Our\s+)?(?:Method|Approach|Framework|Proposed)',1500)
        ablation=snippet(r'^.*(?:Ablation\s+(?:Study|Studies)|Component\s+Analysis).*$',800)
        captions=[]
        for m in re.finditer(r'^(?:Table|Figure)\s*\d+[.:]',text,re.M):
            captions.append(flat(text[m.start():m.start()+450]))
        chosen=captions[:2]+captions[-2:] if len(captions)>4 else captions
        record=dict(row,pages=len(pages),headings=heads,abstract=abstract,related=related,method=method,ablation=ablation,captions=chosen)
        out.append(record)
    (WORK/'reading_packets.json').write_text(json.dumps(out,ensure_ascii=False,indent=2))
    print('Prepared',len(out),'papers')

def show(start,end):
    rows=json.loads((WORK/'reading_packets.json').read_text())
    for r in rows[start-1:end]:
        print('\n###',r['id'],r['year'],r['title'])
        print('STRUCTURE',r['headings'])
        print('ABSTRACT',r['abstract'][:600])
        print('RELATED',r['related'][:450])
        raw=(WORK/f"{r['id']}.txt").read_text()
        method=r['method']
        if method.startswith('[heading'):
            m=re.search(r'^3\.\s+[A-Za-z]',raw,re.M)
            method=flat(raw[m.start():m.start()+1200]) if m else method
        print('METHOD',method[:1150])
        m=re.search(r'^\d+\.\d+\.?\s+(?:Ablation|Ablative|Component).*$',raw,re.M)
        ablation=flat(raw[m.start():m.start()+700]) if m else r['ablation'][:650]
        print('ABLATION',ablation)
        captions=[flat(raw[m.start():m.start()+330]) for m in re.finditer(r'^Table\s*\d+[.:]',raw,re.M)]
        print('TABLES','\n'.join(captions[:2]+captions[-1:]))
        print('FIGURE',r['captions'][0][:300] if r['captions'] else '')

def render(start,end):
    import pypdfium2 as pdfium
    from PIL import Image,ImageDraw
    rows=json.loads((WORK/'reading_packets.json').read_text())[start-1:end]
    sheet=Image.new('RGB',(1700,1160*((len(rows)+2)//3)),'#d5d5d5')
    for i,row in enumerate(rows):
        heads=row['headings']
        method_page=next((p for p,s in heads if re.match(r'^\d+\.\s*(?:Our\s+)?(?:Method|Approach|Framework|Proposed)',s,re.I)),3)
        page=min(method_page,len(PdfReader(WORK/f"{row['id']}.pdf").pages)-1)
        doc=pdfium.PdfDocument(str(WORK/f"{row['id']}.pdf"))
        im=doc[page].render(scale=1.4).to_pil().convert('RGB')
        im.thumbnail((550,1100))
        x=(i%3)*565;y=(i//3)*1160
        sheet.paste(im,(x,y+45))
        ImageDraw.Draw(sheet).text((x+5,y+10),f"{row['id']} | {row['year']} | PDF page {page+1}",fill='black')
    path=WORK/f'layout_{start:02d}_{end:02d}.png';sheet.save(path)
    print(path)

if __name__=='__main__':
    mode=sys.argv[1]
    if mode=='prepare':prepare()
    elif mode=='show':show(int(sys.argv[2]),int(sys.argv[3]))
    elif mode=='render':render(int(sys.argv[2]),int(sys.argv[3]))
