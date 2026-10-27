from pathlib import Path
ROOT=Path(r"D:\论文\9.27论文")
SRC=ROOT/'Astra_docs'/'manuscript_v1'
CN=ROOT/'中文论文'
for src,dst in [(SRC/'references.md',CN/'参考文献.md'),(SRC/'references.bib',CN/'references.bib')]:
    CN.mkdir(exist_ok=True)
    dst.write_text(src.read_text(encoding='utf-8-sig').rstrip()+'\n',encoding='utf-8',newline='\n')
p=CN/'论文中文版.md'
t=p.read_text(encoding='utf-8-sig')
t=t.replace('[参考文献](references.md)','[参考文献](参考文献.md)')
p.write_text(t.rstrip()+'\n',encoding='utf-8',newline='\n')
m=CN/'中英章节对应.md'
text=m.read_text(encoding='utf-8-sig')
text += '\n引用对应：中文稿件中的 `[1]–[28]` 按 `参考文献.md` / `references.bib` 的 `R01–R28` 顺序对应；英文模板使用 `\\cite{Rxx}`，最终编号由 BibTeX 自动生成。\n'
m.write_text(text,encoding='utf-8',newline='\n')
print('updated')
