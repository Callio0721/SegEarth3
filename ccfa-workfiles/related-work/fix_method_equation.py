from pathlib import Path
import re
p=Path(r'D:\论文\9.27论文\author-kit-main\sec\3_method.tex')
t=p.read_text(encoding='utf-8')
pattern=r'\\begin\{equation\}\s*\\Psi_\{\\max\}\(L,G\)=\\max\(L,G\),\s*\\qquad\s*\\Psi_\{\\rho,g\}\(L,G\)=\\left\(\(1-g\)L\^\{\\rho\}+gG\^\{\\rho\}\\right\)\^\{1/\\rho\},\s*\\label\{eq:view-operators\}\s*\\end\{equation\}'
rep=r'''\begin{align}
\Psi_{\max}(L,G)&=\max(L,G), \label{eq:view-operators}\\
\Psi_{\rho,g}(L,G)&=\left((1-g)L^{\rho}+gG^{\rho}\right)^{1/\rho}. \label{eq:view-power}
\end{align}'''
t2,n=re.subn(pattern,rep,t,count=1,flags=re.S)
if n!=1:
    raise SystemExit(f'replacement failed: {n}')
p.write_text(t2,encoding='utf-8',newline='\n')
print('replaced')
