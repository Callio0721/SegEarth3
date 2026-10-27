from pathlib import Path
import re
p=Path(r"D:\论文\9.27论文\author-kit-main\sec\4_experiments.tex")
s=p.read_text(encoding='utf-8')

# Ensure the main table remains a full-width top float after 4.1.
s=s.replace(r'\captionof{table}{Remote-sensing open-vocabulary',r'\caption{Remote-sensing open-vocabulary',1)

# Convert the four single-column inline tables into real floats.
patterns=[
('tab:component-progression', r'''\begin{center}
\centering
\captionsetup{hypcap=false}
\captionof{table}{Macro component progression. Stage entries refer to the configurations defined in Section~3; Role-only is the best recorded independent role profile and is not the matched Role condition used for interaction analysis.}
\label{tab:component-progression}
\captionsetup{hypcap=true}
\small
\setlength{\tabcolsep}{3pt}
\begin{tabular}{lccc}
\toprule
Stage & Macro mIoU & $\Delta$ vs baseline & Positive \\
\midrule
Matched baseline & 53.56 & -- & -- \\
Role-Functional Text & 55.82 & +2.25 & 8/8 \\
Joint Role--View & 57.49 & +3.92 & 8/8 \\
\bottomrule
\end{tabular}
\end{center}''', r'''\begin{table}[t]
\centering
\caption{Macro component progression. Stage entries refer to the configurations defined in Section~3; Role-only is the best recorded independent role profile and is not the matched Role condition used for interaction analysis.}
\label{tab:component-progression}
\small
\setlength{\tabcolsep}{3pt}
\begin{tabular}{lccc}
\toprule
Stage & Macro mIoU & $\Delta$ vs baseline & Positive \\
\midrule
Matched baseline & 53.56 & -- & -- \\
Role-Functional Text & 55.82 & +2.25 & 8/8 \\
Joint Role--View & 57.49 & +3.92 & 8/8 \\
\bottomrule
\end{tabular}
\end{table}'''),
('tab:role-use', r'''\begin{center}
\centering
\captionsetup{hypcap=false}
\captionof{table}{The same semantic-oriented candidate used either only for Semantic supplementation or for all three roles. Both variants retain the anchor and bounded update; values are final mIoU.}
\label{tab:role-use}
\captionsetup{hypcap=true}
\small
\setlength{\tabcolsep}{2.5pt}
\begin{tabular}{llccc}
\toprule
Dataset & Candidate & Baseline & Semantic only & Shared P/S/I \\
\midrule
Potsdam & S2 & 57.87 & \textbf{58.00} & 56.63 \\
Vaihingen & S3 & 60.86 & \textbf{61.57} & 61.28 \\
LoveDA & S1 & 47.34 & \textbf{48.09} & 46.61 \\
OEM & S3 & 44.30 & \textbf{46.28} & 44.02 \\
UDD5 & S3 & 71.80 & 71.56 & \textbf{73.04} \\
VDD & S1 & 64.11 & \textbf{65.27} & 65.05 \\
\bottomrule
\end{tabular}
\end{center}''', r'''\begin{table}[t]
\centering
\caption{The same semantic-oriented candidate used either only for Semantic supplementation or for all three roles. Both variants retain the anchor and bounded update; values are final mIoU.}
\label{tab:role-use}
\small
\setlength{\tabcolsep}{2.5pt}
\begin{tabular}{llccc}
\toprule
Dataset & Candidate & Baseline & Semantic only & Shared P/S/I \\
\midrule
Potsdam & S2 & 57.87 & \textbf{58.00} & 56.63 \\
Vaihingen & S3 & 60.86 & \textbf{61.57} & 61.28 \\
LoveDA & S1 & 47.34 & \textbf{48.09} & 46.61 \\
OEM & S3 & 44.30 & \textbf{46.28} & 44.02 \\
UDD5 & S3 & 71.80 & 71.56 & \textbf{73.04} \\
VDD & S1 & 64.11 & \textbf{65.27} & 65.05 \\
\bottomrule
\end{tabular}
\end{table}'''),
('tab:interaction', r'''\begin{center}
\centering
\captionsetup{hypcap=false}
\captionof{table}{Matched Role $\times$ View ablation. The Role column uses the final joint role configuration, not an independently reselected optimum. Values are computed before rounding.}
\label{tab:interaction}
\captionsetup{hypcap=true}
\small
\setlength{\tabcolsep}{3.5pt}
\begin{tabular}{lccccc}
\toprule
Dataset & $m_{00}$ & $m_{10}$ & $m_{01}$ & $m_{11}$ & $\Gamma$ \\
\midrule
Potsdam & 57.87 & 58.59 & 62.34 & \textbf{63.18} & +0.11 \\
Vaihingen & 60.86 & 61.59 & 63.58 & \textbf{66.38} & +2.07 \\
LoveDA & 47.34 & 48.30 & 47.18 & \textbf{48.81} & +0.66 \\
iSAID & 27.64 & 28.27 & 28.73 & \textbf{29.13} & -0.23 \\
OEM & 44.30 & 50.53 & 45.17 & \textbf{53.08} & +1.68 \\
UAVid & 54.58 & 59.50 & 54.43 & \textbf{59.82} & +0.47 \\
UDD5 & 71.80 & 72.76 & 72.27 & \textbf{72.94} & -0.28 \\
VDD & 64.11 & 65.83 & 64.30 & \textbf{66.55} & +0.53 \\
\midrule
Average & 53.56 & 55.67 & 54.75 & \textbf{57.49} & +0.63 \\
\bottomrule
\end{tabular}
\end{center}''', r'''\begin{table}[t]
\centering
\caption{Matched Role $\times$ View ablation. The Role column uses the final joint role configuration, not an independently reselected optimum. Values are computed before rounding.}
\label{tab:interaction}
\small
\setlength{\tabcolsep}{3.5pt}
\begin{tabular}{lccccc}
\toprule
Dataset & $m_{00}$ & $m_{10}$ & $m_{01}$ & $m_{11}$ & $\Gamma$ \\
\midrule
Potsdam & 57.87 & 58.59 & 62.34 & \textbf{63.18} & +0.11 \\
Vaihingen & 60.86 & 61.59 & 63.58 & \textbf{66.38} & +2.07 \\
LoveDA & 47.34 & 48.30 & 47.18 & \textbf{48.81} & +0.66 \\
iSAID & 27.64 & 28.27 & 28.73 & \textbf{29.13} & -0.23 \\
OEM & 44.30 & 50.53 & 45.17 & \textbf{53.08} & +1.68 \\
UAVid & 54.58 & 59.50 & 54.43 & \textbf{59.82} & +0.47 \\
UDD5 & 71.80 & 72.76 & 72.27 & \textbf{72.94} & -0.28 \\
VDD & 64.11 & 65.83 & 64.30 & \textbf{66.55} & +0.53 \\
\midrule
Average & 53.56 & 55.67 & 54.75 & \textbf{57.49} & +0.63 \\
\bottomrule
\end{tabular}
\end{table}'''),
('tab:natural', r'''\begin{center}
\centering
\captionsetup{hypcap=false}
\captionof{table}{Natural-image evaluation (mIoU, \%). Role-only and view-only are separately selected optima; the table is not used to compute interaction. VOC20 uses the foreground vocabulary.}
\label{tab:natural}
\captionsetup{hypcap=true}
\small
\setlength{\tabcolsep}{3pt}
\begin{tabular}{lcccccc}
\toprule
Dataset & Images & Baseline & Role & View & Joint & $\Delta$ \\
\midrule
VOC20 & 1,449 & 96.89 & 97.00 & 97.00 & \textbf{97.11} & +0.22 \\
Cityscapes & 500 & 67.90 & \textbf{72.20} & 68.72 & \textbf{72.20} & +4.29 \\
\bottomrule
\end{tabular}
\end{center}''', r'''\begin{table}[t]
\centering
\caption{Natural-image evaluation (mIoU, \%). Role-only and view-only are separately selected optima; the table is not used to compute interaction. VOC20 uses the foreground vocabulary.}
\label{tab:natural}
\small
\setlength{\tabcolsep}{3pt}
\begin{tabular}{lcccccc}
\toprule
Dataset & Images & Baseline & Role & View & Joint & $\Delta$ \\
\midrule
VOC20 & 1,449 & 96.89 & 97.00 & 97.00 & \textbf{97.11} & +0.22 \\
Cityscapes & 500 & 67.90 & \textbf{72.20} & 68.72 & \textbf{72.20} & +4.29 \\
\bottomrule
\end{tabular}
\end{table}''')]
for _,a,b in patterns:
    if a not in s:
        raise AssertionError('missing block '+_)
    s=s.replace(a,b,1)
p.write_text(s,encoding='utf-8')
print('converted single-column tables to top floats')
