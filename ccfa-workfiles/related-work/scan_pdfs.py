import hashlib, json, re
from pathlib import Path
from pypdf import PdfReader
ROOT = Path(r"D:\论文\9.27论文")
OUT = ROOT / "ccfa-workfiles" / "related-work" / "pdf-inventory.json"
rows=[]; errors=[]
terms=["open-vocabulary","open vocabulary","segmentation","remote sensing","sam 3","sam3","clip","prompt","grounding","context","global","local","concept"]
for path in ROOT.rglob("*.pdf"):
    if any(part in {".git",".obsidian","__pycache__"} for part in path.parts) or path.name.startswith("._"):
        continue
    rel=str(path.relative_to(ROOT))
    try:
        reader=PdfReader(str(path))
        pages=[]
        for page in reader.pages:
            try: pages.append(page.extract_text() or "")
            except Exception: pages.append("")
        text="\n".join(pages)
        lower=text.lower()
        first=" ".join(text.split())[:800]
        meta=reader.metadata or {}
        row={"path":rel,"bytes":path.stat().st_size,"pages":len(reader.pages),"chars":len(text),"metadata_title":str(meta.get('/Title','')),"first_text":first,"terms":{t:lower.count(t) for t in terms}}
    except Exception as exc:
        row={"path":rel,"bytes":path.stat().st_size,"error":repr(exc)}; errors.append(row)
    rows.append(row)
OUT.write_text(json.dumps({"count":len(rows),"errors":errors,"files":rows},ensure_ascii=False,indent=2),encoding="utf-8")
print(json.dumps({"output":str(OUT),"count":len(rows),"errors":len(errors),"total_pages":sum(r.get('pages',0) or 0 for r in rows),"total_text_chars":sum(r.get('chars',0) or 0 for r in rows)},ensure_ascii=False,indent=2))
