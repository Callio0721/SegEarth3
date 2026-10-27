from pathlib import Path
p=Path(r'D:\论文\9.27论文\author-kit-main\sec\3_method.tex')
lines=p.read_text(encoding='utf-8').splitlines()
start=None
for i,l in enumerate(lines):
    if l.strip()==r'\begin{align}':
        start=i; break
if start is None:
    raise SystemExit('align block not found')
end=None
for j in range(start,len(lines)):
    if lines[j].strip()==r'\end{align}':
        end=j; break
if end is None:
    raise SystemExit('align end not found')
lines[start:end+1]=[
    r'\begin{equation}',
    r'\begin{aligned}',
    r'\Psi_{\max}(L,G)&=\max(L,G),\\',
    r'\Psi_{\rho,g}(L,G)&=\left((1-g)L^{\rho}+gG^{\rho}\right)^{1/\rho}.',
    r'\end{aligned}',
    r'\label{eq:view-operators}',
    r'\end{equation}'
]
p.write_text('\n'.join(lines)+'\n',encoding='utf-8',newline='\n')
print('fixed aligned equation')
