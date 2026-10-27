from pathlib import Path
p=Path(r'D:\论文\9.27论文\author-kit-main\sec\4_experiments.tex')
t=p.read_text(encoding='utf-8')
old=r'''\begin{figure*}[!t]
\centering
\includegraphics[width=\linewidth]{fig/qualitative_placeholder.png}
\caption{Placeholder for qualitative comparison. Colored panels mark the required RGB, ground-truth, Baseline, Role-only, View-only, and Joint outputs. They are placeholders, not experimental predictions; the panels will be replaced with verified exports from the fixed profile.}
\label{fig:qualitative-placeholder}
\end{figure*}'''
new=r'''\begin{strip}
\centering
\includegraphics[width=\linewidth]{fig/qualitative_placeholder.png}
\captionsetup{hypcap=false}
\captionof{figure}{Placeholder for qualitative comparison. Colored panels mark the required RGB, ground-truth, Baseline, Role-only, View-only, and Joint outputs. They are placeholders, not experimental predictions; the panels will be replaced with verified exports from the fixed profile.}
\label{fig:qualitative-placeholder}
\captionsetup{hypcap=true}
\end{strip}'''
if old not in t:
    raise SystemExit('qualitative figure block not found')
p.write_text(t.replace(old,new),encoding='utf-8',newline='\n')
print('qualitative placeholder fixed in strip')
