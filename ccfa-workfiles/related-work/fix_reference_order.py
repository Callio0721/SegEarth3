from pathlib import Path
import re
KIT=Path(r'D:\论文\9.27论文\author-kit-main')
bbl=(KIT/'main.bbl').read_text(encoding='utf-8')
start=bbl.index('\\begin{thebibliography}')
body=bbl[start:]
prefix=body[:body.index('\\bibitem')]
suffix='\\end{thebibliography}'
parts=re.split(r'(?=\\bibitem)', body[body.index('\\bibitem'):])
entries={}
for part in parts:
    if not part.startswith('\\bibitem'):
        continue
    m=re.match(r'\\bibitem(?:\[[^\]]*\])?\{([^}]+)\}', part)
    if not m:
        continue
    key=m.group(1)
    fixed=re.sub(r'^\\bibitem(?:\[[^\]]*\])?\{[^}]+\}', r'\\bibitem{'+key+'}', part, count=1)
    entries[key]=fixed.rstrip()
ordered=[]
for i in range(1,29):
    key=f'R{i:02d}'
    if key not in entries:
        raise SystemExit(f'missing bibliography entry {key}')
    ordered.append(entries[key])
refs=prefix+'\n\n'.join(ordered)+'\n'+suffix+'\n'
(KIT/'references.tex').write_text(refs,encoding='utf-8',newline='\n')

main=(KIT/'main.tex').read_text(encoding='utf-8')
main=re.sub(r'\n% Keep citation numbering.*?\n\\nocite\{[^}]+\}\n', '\n', main, flags=re.S)
main=re.sub(r'\{\n\s*\\small\n\s*\\bibliographystyle\{ieeenat_fullname\}\n\s*\\bibliography\{main\}\n\}', '\\input{references}', main)
if '\\input{references}' not in main:
    raise SystemExit('failed to replace bibliography block')
(KIT/'main.tex').write_text(main,encoding='utf-8',newline='\n')
print('wrote',KIT/'references.tex','entries',len(ordered))
