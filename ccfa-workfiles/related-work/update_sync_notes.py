from pathlib import Path
ROOT=Path(r'D:\论文\9.27论文')
main=ROOT/'author-kit-main'/'main.tex'
t=main.read_text(encoding='utf-8')
if 'References are fixed in R01--R28 order' not in t:
    t=t.replace('% The Chinese counterpart is maintained at ../中文论文/论文中文版.md.\n', '% The Chinese counterpart is maintained at ../中文论文/论文中文版.md.\n% References are fixed in R01--R28 order in references.tex to match the Chinese manuscript.\n% Keep main.bib synchronized as source metadata.\n')
main.write_text(t,encoding='utf-8',newline='\n')
m=ROOT/'中文论文'/'中英章节对应.md'
text=m.read_text(encoding='utf-8-sig')
note='\n英文固定编号文件：`author-kit-main/references.tex`。该文件按 `R01–R28` 顺序输出 `[1]–[28]`，与中文 `参考文献.md` 一致。`author-kit-main/main.bib` 保留为元数据来源；新增参考文献时需要同时更新 BibTeX 信息和固定编号列表。\n'
if '英文固定编号文件' not in text:
    text=text.rstrip()+note
m.write_text(text,encoding='utf-8',newline='\n')
print('updated notes')
