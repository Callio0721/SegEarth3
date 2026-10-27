from pathlib import Path
p=Path(r'D:\论文\9.27论文\author-kit-main\sec\4_experiments.tex')
lines=p.read_text(encoding='utf-8').splitlines()
out=[]
count=0
for line in lines:
    if line.startswith(r'\captionof{table}{'):
        out.append(r'{\captionsetup{hypcap=false}')
        out.append(line)
        out.append('}')
        count+=1
    else:
        out.append(line)
p.write_text('\n'.join(out)+'\n',encoding='utf-8',newline='\n')
print('wrapped',count,'captionof calls')
