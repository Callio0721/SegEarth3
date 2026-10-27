from pathlib import Path
p=Path(r'D:\论文\9.27论文\author-kit-main\sec\4_experiments.tex')
t=p.read_text(encoding='utf-8')
old=r'''\begin{strip}
\centering
\includegraphics[width=\linewidth]{fig/qualitative_placeholder.png}
\captionsetup{hypcap=false}
\captionof{figure}{Placeholder for qualitative comparison. Colored panels mark the required RGB, ground-truth, Baseline, Role-only, View-only, and Joint outputs. They are placeholders, not experimental predictions; the panels will be replaced with verified exports from the fixed profile.}
\label{fig:qualitative-placeholder}
\captionsetup{hypcap=true}
\end{strip}'''
new=r'''\begin{center}
\setlength{\fboxsep}{0pt}
\fcolorbox{InstanceOrange}{FigureTint}{%
\parbox{\dimexpr\columnwidth-2\fboxrule\relax}{%
\centering
\vspace{5pt}
{\bf Qualitative comparison placeholder}\\[3pt]
{\small RGB \quad GT \quad Baseline \quad Role-only \quad View-only \quad Joint}\\[4pt]
{\small\itshape Real masks must be exported for OEM, Vaihingen, UAVid/LoveDA.}\\[5pt]
}}
\captionsetup{hypcap=false}
\captionof{figure}{Placeholder for the qualitative comparison. No prediction or improvement is shown; the panel will be replaced with verified outputs from the fixed profile.}
\label{fig:qualitative-placeholder}
\captionsetup{hypcap=true}
\end{center}'''
if old not in t:
    raise SystemExit('qualitative strip block not found')
# Use literal colors because xcolor named colors need definitions.
new=new.replace('InstanceOrange','orange!65!black').replace('FigureTint','orange!5')
p.write_text(t.replace(old,new),encoding='utf-8',newline='\n')
print('replaced qualitative strip with inline color placeholder')
