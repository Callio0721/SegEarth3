from pathlib import Path
p=Path(r'D:\论文\9.27论文\author-kit-main\sec\3_method.tex')
lines=p.read_text(encoding='utf-8').splitlines()
# Replace the single wide equation block on lines 83--88 with an aligned pair.
if lines[82].strip() != r'\begin{equation}' or lines[87].strip() != r'\end{equation}':
    raise SystemExit('unexpected equation block location')
lines[82:88] = [
    r'\begin{align}',
    r'\Psi_{\max}(L,G)&=\max(L,G), \label{eq:view-operators}\\',
    r'\Psi_{\rho,g}(L,G)&=\left((1-g)L^{\rho}+gG^{\rho}\right)^{1/\rho}. \label{eq:view-power}',
    r'\end{align}'
]
p.write_text('\n'.join(lines)+'\n',encoding='utf-8',newline='\n')
print('replaced lines')
