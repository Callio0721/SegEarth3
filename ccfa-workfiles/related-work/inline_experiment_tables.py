from pathlib import Path
p=Path(r'D:\论文\9.27论文\author-kit-main\sec\4_experiments.tex')
t=p.read_text(encoding='utf-8')
out=[]; i=0
needle=r'\begin{table}[!htbp]'
while True:
    s=t.find(needle,i)
    if s<0:
        out.append(t[i:]); break
    out.append(t[i:s])
    e=t.find(r'\end{table}',s)
    if e<0: raise SystemExit('missing end table')
    block=t[s:e+len(r'\end{table}')]
    block=block.replace(needle,r'\begin{center}',1)
    block=block.replace(r'\end{table}',r'\end{center}',1)
    block=block.replace(r'\caption{',r'\captionof{table}{',1)
    out.append(block)
    i=e+len(r'\end{table}')
t=''.join(out)
p.write_text(t,encoding='utf-8',newline='\n')
print('converted',t.count(r'\captionof{table}{'),'single-column tables to inline layout')
