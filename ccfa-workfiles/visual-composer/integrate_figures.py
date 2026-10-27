from pathlib import Path
ROOT=Path(r"D:\论文\9.27论文")

# English intro
p=ROOT/'author-kit-main'/'sec'/'1_intro.tex'
t=p.read_text(encoding='utf-8')
needle='The assumption that one concept and one observation suffice for all readouts therefore requires direct examination.'
if needle in t and 'fig:motivation' not in t:
    t=t.replace(needle, needle+' Figure~\\ref{fig:motivation} summarizes this evidence-allocation question.')
    fig=r'''
\begin{figure*}[!t]
\centering
\includegraphics[width=\linewidth]{fig/intro_teaser.png}
\caption{Motivation. A shared concept anchor conditions three readouts with different evidence needs. The same selected role profile is evaluated under aligned Local and Context observations. The aerial image is illustrative.}
\label{fig:motivation}
\end{figure*}
'''
    # insert immediately after P2
    pos=t.index(needle)+len(needle)
    t=t[:pos]+'\n'+fig+'\n'+t[pos:]
p.write_text(t,encoding='utf-8',newline='\n')

# English method
p=ROOT/'author-kit-main'/'sec'/'3_method.tex'
t=p.read_text(encoding='utf-8')
needle='We denote the resulting single-observation class-score map by $G^{\\mathrm{o}}$.'
if needle in t and 'fig:method-overview' not in t:
    t=t.replace(needle, needle+' Figure~\\ref{fig:method-overview} summarizes the complete evidence path.')
    fig=r'''
\begin{figure*}[!t]
\centering
\includegraphics[width=\linewidth]{fig/method_overview.png}
\caption{Overview of Joint Role--View Specialization. Each required prompt is fully grounded by the frozen model. The same selected role profile is applied in Local and Context observations, and complete class-score fields are fused before the original class decision.}
\label{fig:method-overview}
\end{figure*}
'''
    pos=t.index(needle)+len(needle)
    t=t[:pos]+'\n'+fig+'\n'+t[pos:]
needle2='The operator family is a profile choice, not a new learned attention module. Combining complete class-score fields preserves the native cross-category decision after role and view composition.'
if needle2 in t and 'fig:method-detail' not in t:
    t=t.replace(needle2, needle2+' Figure~\\ref{fig:method-detail} isolates the two evidence interactions.')
    fig2=r'''
\begin{figure*}[!t]
\centering
\includegraphics[width=\linewidth]{fig/method_detail.png}
\caption{Method details. (a) Role-functional evidence keeps the official anchor, applies bounded role updates, rebuilds Instance after the Presence update, and restores the official map through alias compensation. (b) Local and Context observations reuse the same profile and are fused after complete class-score composition.}
\label{fig:method-detail}
\end{figure*}
'''
    pos=t.index(needle2)+len(needle2)
    t=t[:pos]+'\n'+fig2+'\n'+t[pos:]
p.write_text(t,encoding='utf-8',newline='\n')

# English experiments: replace category table with figure, add qualitative placeholder
p=ROOT/'author-kit-main'/'sec'/'4_experiments.tex'
t=p.read_text(encoding='utf-8')
cap='Category-group improvements over the matched baseline.'
if cap in t and 'fig:category-gain' not in t:
    ci=t.index(cap)
    start=t.rfind('\\begin{center}',0,ci)
    end=t.index('\\end{center}',ci)+len('\\end{center}')
    block=t[start:end]
    figure=r'''
\begin{figure}[t]
\centering
\includegraphics[width=\columnwidth]{fig/category_gain.png}
\caption{Category-group improvements over the matched baseline. The background/clutter mean is influenced by OEM and is shown separately.}
\label{fig:category-gain}
\end{figure}
'''
    t=t[:start]+figure+t[end:]
# insert qualitative placeholder before natural-image subsection
marker='\\subsection{Natural-Image Evaluation and Scope}'
if marker in t and 'fig:qualitative-placeholder' not in t:
    qual=r'''
\begin{figure*}[!t]
\centering
\includegraphics[width=\linewidth]{fig/qualitative_placeholder.png}
\caption{Placeholder for qualitative comparison. Colored panels mark the required RGB, ground-truth, Baseline, Role-only, View-only, and Joint outputs. They are placeholders, not experimental predictions; the panels will be replaced with verified exports from the fixed profile.}
\label{fig:qualitative-placeholder}
\end{figure*}
'''
    t=t.replace(marker, qual+'\n'+marker)
# Add a textual pointer before the category figure
needle='JRV improves 48 of 63 dataset--class pairs, including 41 of 55 foreground pairs.'
if 'fig:category-gain' in t and 'Figure~\\ref{fig:category-gain}' not in t:
    t=t.replace(needle, 'Figure~\\ref{fig:category-gain} summarizes the group-level pattern. '+needle)
p.write_text(t,encoding='utf-8',newline='\n')

# Chinese manuscript
p=ROOT/'中文论文'/'论文中文版.md'
raw=p.read_bytes(); bom=raw.startswith(b'\xef\xbb\xbf'); t=raw.decode('utf-8-sig')
# intro figure
needle='因此，“同一概念、同一观察足以服务所有 readout”是一个需要检验的假设。'
if needle in t and '图 1：动机示意' not in t:
    t=t.replace(needle, needle+' 图 1 概括了这一证据分配问题。')
    fig='''

![图 1：动机示意](../author-kit-main/fig/intro_teaser.png)

*图 1：共享概念 anchor 同时服务于不同 readout；同一角色配置在 Local 与 Context 观察下评价。*
'''
    pos=t.index(needle)+len(needle); t=t[:pos]+fig+t[pos:]
# method figures
needle='记这一单观察类别分数图为 \\(G^{\\mathrm{o}}\\)。'
if needle in t and '图 2：方法总览' not in t:
    t=t.replace(needle, needle+' 图 2 概括了完整的证据路径。')
    fig='''

![图 2：方法总览](../author-kit-main/fig/method_overview.png)

*图 2：所有需要的候选文本都经过冻结 SAM3 的完整 grounding；同一角色配置用于 Local 与 Context，最终在类别分数层融合。*
'''
    pos=t.index(needle)+len(needle); t=t[:pos]+fig+t[pos:]
needle2='算子族是数据集 profile 的一部分，不是新的学习式 attention 模块。组合发生在完整类别分数场层面，因此角色和视图组合之后仍沿用原生跨类别决策。'
if needle2 in t and '图 3：方法细节' not in t:
    t=t.replace(needle2, needle2+' 图 3 展示了两个关键证据交互。')
    fig='''

![图 3：方法细节](../author-kit-main/fig/method_detail.png)

*图 3：(a) 角色功能证据；(b) Local 与 Context 的同一角色配置与类别分数融合。*
'''
    pos=t.index(needle2)+len(needle2); t=t[:pos]+fig+t[pos:]
# replace Chinese category table with figure
old_table='''| 类别组 | 类别对 | 正提升 | Role ΔIoU | Joint ΔIoU |
|---|---:|---:|---:|---:|
| 水体相关 | 4 | 3 | +3.15 | +5.65 |
| 植被与土地覆盖 | 15 | 14 | +2.83 | +4.95 |
| 建筑结构 | 11 | 7 | +1.59 | +2.48 |
| 可移动目标 | 11 | 7 | −0.02 | +1.49 |
| 交通地表 | 9 | 6 | +1.43 | +1.26 |
| 体育场地 | 5 | 4 | +0.34 | +0.79 |
| 背景 / 杂项 | 8 | 7 | +6.64 | +10.22 |'''
if old_table in t:
    t=t.replace(old_table, '''![图 4：类别组增益](../author-kit-main/fig/category_gain.png)

*图 4：七个类别组相对匹配 baseline 的 Joint ΔIoU；背景/杂项受 OEM 影响，单独标注。*''')
# insert qualitative placeholder before 4.6
marker='### 4.6 自然域评价与范围'
if marker in t and '图 5：定性占位' not in t:
    qual='''![图 5：定性对比占位](../author-kit-main/fig/qualitative_placeholder.png)

*图 5：定性对比布局占位。色块表示需要替换的真实 RGB、GT、Baseline、Role-only、View-only 与 Joint 输出；当前不是实验预测。*

'''
    t=t.replace(marker, qual+marker)
# add reference to figure 4 in text
needle3='JRV 在 63 个数据集—类别对中提升 48 个，在 55 个前景对中提升 41 个。'
if needle3 in t and '图 4' not in t.split('JRV 在 63')[1][:80]:
    t=t.replace(needle3, '图 4 汇总了类别组层面的结果。'+needle3)
p.write_text(t,encoding='utf-8-sig' if bom else 'utf-8',newline='\n')
print('figures integrated')
