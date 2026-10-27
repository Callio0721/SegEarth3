"""Read CVF proceedings; cache public writing-study sources only in Astra_docs."""
from pathlib import Path
from urllib.request import urlopen, Request
from urllib.parse import urljoin
from concurrent.futures import ThreadPoolExecutor
import html
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT / '_work' / 'cvpr50'
WORK.mkdir(parents=True, exist_ok=True)

def fetch(url):
    return urlopen(Request(url, headers={'User-Agent': 'Mozilla/5.0 (academic-paper-reading)'}), timeout=60).read()

def indexes():
    rows = []
    for year in [2025, 2026]:
        path = WORK / f'CVPR{year}_index.html'
        if not path.exists():
            path.write_bytes(fetch(f'https://openaccess.thecvf.com/CVPR{year}?day=all'))
        seen = set()
        for href, title in re.findall(r'<a\s+[^>]*href=["\']([^"\']+)["\'][^>]*>(.*?)</a>', path.read_text(), re.S):
            if f'content/CVPR{year}/html/' not in href or href in seen:
                continue
            seen.add(href)
            title = html.unescape(re.sub('<[^>]+>', '', title)).strip()
            rows.append(dict(year=year, title=title, url=urljoin('https://openaccess.thecvf.com/', href)))
    (WORK / 'all_titles.json').write_text(json.dumps(rows, ensure_ascii=False, indent=2))
    selected = [r for r in rows if re.search(r'open.?vocab|remote sensing|semantic segment|segment anything|referring.*segment|reasoning.*segment',r['title'],re.I)]
    for i,r in enumerate(selected):
        print(i, r['year'], r['title'])
    (WORK / 'candidate_titles.json').write_text(json.dumps(selected,ensure_ascii=False,indent=2))
    print('TOTAL',len(rows),'CANDIDATES',len(selected))

def download():
    chosen=json.loads((WORK/'selection.json').read_text())
    def one(row):
        try:
            slug=row['id']
            page=WORK/f'{slug}.html'
            if not page.exists(): page.write_bytes(fetch(row['url']))
            data=page.read_text()
            links=re.findall(r'href=["\']([^"\']+_paper\.pdf)["\']',data)
            if not links: raise ValueError('No official PDF link')
            pdf_url=urljoin(row['url'],links[0])
            pdf=WORK/f'{slug}.pdf'
            if not pdf.exists(): pdf.write_bytes(fetch(pdf_url))
            if not pdf.read_bytes().startswith(b'%PDF'): raise ValueError('Not PDF')
            bib=re.search(r'(@InProceedings\{.*?\n\})',html.unescape(data),re.S)
            if bib: (WORK/f'{slug}.bib').write_text(bib.group(1))
            row.update(pdf_url=pdf_url, pdf=str(pdf.relative_to(ROOT)), verified=True)
            print('OK',slug,row['title'],flush=True)
        except Exception as e:
            row.update(verified=False,error=f'{type(e).__name__}: {e}')
            print('FAILED',row['id'],str(e),flush=True)
        return row
    with ThreadPoolExecutor(max_workers=5) as pool:
        result=list(pool.map(one,chosen))
    (WORK/'manifest.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))

def choose():
    candidates=json.loads((WORK/'candidate_titles.json').read_text())
    indices=[7,18,21,23,31,32,35,41,50,52,57,63,68,15,71,78,38,10,17,76,54,34,28,62,
             79,84,86,88,101,103,108,124,128,140,145,147,149,153,164,169,171,178,189,197,199,201,174,100,82]
    rows=[candidates[i].copy() for i in indices]
    all_rows=json.loads((WORK/'all_titles.json').read_text())
    rows.insert(24,next(r.copy() for r in all_rows if r['title']=='Scaling up Image Segmentation across Data and Tasks'))
    for i,r in enumerate(rows,1):r['id']=f'C{i:02d}'
    assert len(rows)==50 and len({r['url'] for r in rows})==50
    (WORK/'selection.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2))
    for r in rows:print(r['id'],r['year'],r['title'])

if __name__=='__main__':
    {'indexes':indexes,'choose':choose,'download':download}[sys.argv[1]]()
