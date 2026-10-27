from pathlib import Path
import re
p=Path(r"D:\论文\9.27论文\author-kit-main\sec\4_experiments.tex")
s=p.read_text(encoding='utf-8')
s=s.replace(r'\begin{strip}',r'\clearpage'+'\n'+r'\begin{table*}[t]',1)
s=s.replace(r'\end{strip}',r'\end{table*}',1)
# Only the first captionof belongs to the full-width main table.
s=s.replace(r'\captionof{table}{Remote-sensing open-vocabulary',r'\caption{Remote-sensing open-vocabulary',1)

# Ungroup captionof blocks so \label sees the table/figure counter.
replacements=[
(r'''{\captionsetup{hypcap=false}
\captionof{table}{Macro component progression. Stage entries refer to the configurations defined in Section~3; Role-only is the best recorded independent role profile and is not the matched Role condition used for interaction analysis.}
}
\label{tab:component-progression}''',
r'''\captionsetup{hypcap=false}
\captionof{table}{Macro component progression. Stage entries refer to the configurations defined in Section~3; Role-only is the best recorded independent role profile and is not the matched Role condition used for interaction analysis.}
\label{tab:component-progression}
\captionsetup{hypcap=true}'''),
(r'''{\captionsetup{hypcap=false}
\captionof{table}{The same semantic-oriented candidate used either only for Semantic supplementation or for all three roles. Both variants retain the anchor and bounded update; values are final mIoU.}
}
\label{tab:role-use}''',
r'''\captionsetup{hypcap=false}
\captionof{table}{The same semantic-oriented candidate used either only for Semantic supplementation or for all three roles. Both variants retain the anchor and bounded update; values are final mIoU.}
\label{tab:role-use}
\captionsetup{hypcap=true}'''),
(r'''{\captionsetup{hypcap=false}
\captionof{table}{Matched Role $\times$ View ablation. The Role column uses the final joint role configuration, not an independently reselected optimum. Values are computed before rounding.}
}
\label{tab:interaction}''',
r'''\captionsetup{hypcap=false}
\captionof{table}{Matched Role $\times$ View ablation. The Role column uses the final joint role configuration, not an independently reselected optimum. Values are computed before rounding.}
\label{tab:interaction}
\captionsetup{hypcap=true}'''),
(r'''{\captionsetup{hypcap=false}
\captionof{table}{Natural-image evaluation (mIoU, \%). Role-only and view-only are separately selected optima; the table is not used to compute interaction. VOC20 uses the foreground vocabulary.}
}
\label{tab:natural}''',
r'''\captionsetup{hypcap=false}
\captionof{table}{Natural-image evaluation (mIoU, \%). Role-only and view-only are separately selected optima; the table is not used to compute interaction. VOC20 uses the foreground vocabulary.}
\label{tab:natural}
\captionsetup{hypcap=true}''')]
for a,b in replacements:
    assert a in s, a[:80]
    s=s.replace(a,b,1)
# Figure 5 label scope.
old=r'''\captionsetup{hypcap=false}
\captionof{figure}{Placeholder for the qualitative comparison. No prediction or improvement is shown; the panel will be replaced with verified outputs from the fixed profile.}
\label{fig:qualitative-placeholder}
\captionsetup{hypcap=true}'''
new=r'''\captionsetup{hypcap=false}
\captionof{figure}{Placeholder for the qualitative comparison. No prediction or improvement is shown; the panel will be replaced with verified outputs from the fixed profile.}
\label{fig:qualitative-placeholder}
\captionsetup{hypcap=true}'''
# already ungrouped; keep idempotent
assert old in s
p.write_text(s,encoding='utf-8')
print('table float and caption label scopes fixed')
