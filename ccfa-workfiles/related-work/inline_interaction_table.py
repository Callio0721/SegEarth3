from pathlib import Path
import re
p=Path(r"D:\论文\9.27论文\author-kit-main\sec\4_experiments.tex")
s=p.read_text(encoding='utf-8')
pat=re.compile(r'\\begin\{table\}\[!htbp\](?:(?!\\end\{table\}).)*?\\label\{tab:interaction\}.*?\\end\{table\}',re.S)
m=pat.search(s)
if not m: raise SystemExit('interaction table block not found')
block=m.group(0)
block=block.replace(r'\begin{table}[!htbp]',r'\begin{center}',1)
block=block.replace(r'\caption{',r'\captionsetup{hypcap=false}'+'\n'+r'\captionof{table}{',1)
block=block.replace(r'\label{tab:interaction}',r'\label{tab:interaction}'+'\n'+r'\captionsetup{hypcap=true}',1)
block=block.replace(r'\end{table}',r'\end{center}',1)
s=s[:m.start()]+block+s[m.end():]
p.write_text(s,encoding='utf-8')
print('interaction table now inline')
