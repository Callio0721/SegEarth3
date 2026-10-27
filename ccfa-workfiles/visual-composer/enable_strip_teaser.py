from pathlib import Path
ROOT=Path(r'D:\论文\9.27论文')
pre=ROOT/'author-kit-main'/'preamble.tex'
t=pre.read_text(encoding='utf-8').replace('% \\usepackage{cuted}','\\usepackage{cuted}')
pre.write_text(t,encoding='utf-8',newline='\n')
main=ROOT/'author-kit-main'/'main.tex'
m=main.read_text(encoding='utf-8')
old=r'''\begin{figure*}[!t]
\centering
\includegraphics[width=\linewidth]{fig/intro_teaser.png}
\caption{Motivation. A shared concept anchor conditions three readouts with different evidence needs. The same selected role profile is evaluated under aligned Local and Context observations. The aerial image is illustrative.}
\label{fig:motivation}
\end{figure*}'''
new=r'''\begin{strip}
\centering
\includegraphics[width=\linewidth]{fig/intro_teaser.png}
\captionsetup{hypcap=false}
\captionof{figure}{Motivation. A shared concept anchor conditions three readouts with different evidence needs. The same selected role profile is evaluated under aligned Local and Context observations. The aerial image is illustrative.}
\label{fig:motivation}
\captionsetup{hypcap=true}
\end{strip}'''
if old not in m:
    raise SystemExit('teaser block not found')
m=m.replace(old,new)
main.write_text(m,encoding='utf-8',newline='\n')
print('enabled strip teaser')
