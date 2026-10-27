from pathlib import Path
ROOT=Path(r'D:\论文\9.27论文')
intro=ROOT/'author-kit-main'/'sec'/'1_intro.tex'
t=intro.read_text(encoding='utf-8')
s=t.index('\\begin{figure*}[!t]')
e=t.index('\\end{figure*}',s)+len('\\end{figure*}')
fig=t[s:e].strip()+'\n'
t=t[:s]+t[e:]
intro.write_text(t,encoding='utf-8',newline='\n')
main=ROOT/'author-kit-main'/'main.tex'
m=main.read_text(encoding='utf-8')
if 'fig/intro_teaser.png' not in m:
    m=m.replace('\\maketitle\n', '\\maketitle\n\n'+fig+'\n')
main.write_text(m,encoding='utf-8',newline='\n')
print('moved teaser to main.tex')
