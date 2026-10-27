from pathlib import Path

ROOT=Path(r"D:\论文\9.27论文")
KIT=ROOT/"author-kit-main"
CN=ROOT/"中文论文"/"论文中文版.md"

en_abs=r'''\begin{abstract}
Training-free open-vocabulary semantic segmentation must assign arbitrary textual categories to dense remote-sensing imagery without updating the segmentation model. Concept-grounded segmenters such as SAM3 and SegEarth-OV3 provide a shared grounding state with distinct Presence, Semantic, and Instance readouts, but current methods typically condition all readouts with one category-level description and one visual observation. We study the resulting mismatch between shared concept grounding and heterogeneous evidence requirements. We introduce Joint Role--View Specialization (JRV), which preserves the official class anchor, grounds role-functional candidates with the complete frozen model, and applies bounded role-specific corrections while retaining the native Presence--Instance coupling. JRV then grounds spatially aligned Local and Context observations, reuses the same role profile across both views, and composes their complete class-score fields before the original class decision. On eight remote-sensing benchmarks, JRV raises the matched average mIoU from 53.56 to 57.49 and improves every dataset over the baseline. A matched Role--View factorial analysis shows positive interaction on six of eight datasets, while the natural-image evaluations show transfer of role supplementation and the dataset dependence of view composition. These results support organizing supplementary evidence by readout responsibility and observation condition rather than treating additional text or larger visual fields as uniformly beneficial.
\end{abstract}
'''

en_con=r'''\section{Conclusion}
\label{sec:conclusion}

We studied how supplementary evidence should enter a frozen concept-grounded segmentation model whose Presence, Semantic, and Instance readouts serve different functions. The central finding is that a shared concept supplies a stable category anchor but does not impose a shared evidence requirement. JRV preserves the official ontology and the native $p\max(S,I)$ path, specializes supplementary text by readout role, and composes aligned Local and Context observations after complete grounding. The eight-benchmark evaluation supports this organization: average mIoU rises from 53.56 to 57.49, every dataset improves over the matched baseline, and the fixed Role--View configuration has positive interaction on six datasets. The category and pixel analyses show that the gain reflects corrected assignments rather than a single dominant class.

The scope is equally part of the result. Dataset-level profiles are selected offline rather than predicted per image, the view operator varies with data distribution, and iSAID and UDD5 exhibit overlapping rather than complementary corrections. Cityscapes selects a Global endpoint, while the same-image Potsdam/Vaihingen control does not support an additional gain from the tested 256/512 crops. These observations position JRV as evidence organization for a frozen concept-grounded model, not as a universal claim that more prompts or larger fields improve segmentation. A natural next step is to replace offline profile selection with a validation-driven or lightweight adaptive policy while preserving the anchor and full-grounding constraints identified here.
'''

cn_abs=r'''## 摘要

免训练遥感开放词汇语义分割要求在不更新分割模型的情况下，将任意文本类别落实到稠密遥感图像中。SAM3 与 SegEarth-OV3 提供了共享概念 grounding，并从中读取 Presence、Semantic 和 Instance 三类证据；现有方法通常用同一个类别级描述和同一个视觉观察约束全部 readout。本文研究共享概念 grounding 与异质证据需求之间的这一错配，提出角色—视图联合专门化（Joint Role–View Specialization，JRV）。JRV 保留官方类别 anchor，以完整冻结模型对角色功能候选进行 grounding，并通过有界 role-specific correction 更新证据，同时保留 Presence 与 Instance 的原生耦合。随后，方法在空间对齐的 Local 与 Context 观察上分别完成 grounding，复用同一角色配置，并在原始类别决策之前组合完整类别分数场。八个遥感基准上的实验将配对平均 mIoU 从 53.56 提升到 57.49，八个数据集均超过 baseline；固定 Role–View 配置的匹配因子分析在六个数据集上呈正交互。自然图像评价进一步显示角色补充的迁移性，同时表明视图组合依赖数据分布。结果说明，补充证据应按 readout 职责和观察条件组织，而不是把更多文本或更大视野默认视为普遍有益。
'''

cn_con=r'''## 5. 结论

本文研究补充证据应如何进入一个冻结的概念定位分割模型。该模型的 Presence、Semantic 和 Instance readout 承担不同职责。核心发现是：共享概念提供稳定的类别 anchor，但不意味着三种 readout 具有相同的证据需求。JRV 保留官方 ontology 和原生 \(p\max(S,I)\) 路径，按角色组织补充文本，并在完整 grounding 之后组合对齐的 Local 与 Context 观察。八个基准上的评价支持这一组织方式：平均 mIoU 从 53.56 提升到 57.49，全部数据集超过匹配 baseline，固定 Role–View 配置在六个数据集上呈正交互。类别与像素分析表明，增益对应真实纠正，而不是由单个主导类别造成。

方法的适用范围也是结论的一部分。数据集级 profile 是离线选择的，而不是逐图预测的；视图算子会随数据分布变化；iSAID 与 UDD5 的收益表现为重叠而非互补。Cityscapes 选择 Global 单端点，Potsdam/Vaihingen 的同图 256/512 控制也未显示额外视图收益。因此，JRV 的定位是冻结概念定位模型中的证据组织方法，而不是“更多提示或更大视野必然提升分割”的普遍主张。下一步可以利用验证数据或轻量自适应策略替代离线 profile 选择，同时保留本文强调的 anchor 与完整 grounding 约束。
'''

# English abstract and conclusion
(KIT/"sec"/"0_abstract.tex").write_text(en_abs,encoding="utf-8",newline="\n")
(KIT/"sec"/"5_conclusion.tex").write_text(en_con,encoding="utf-8",newline="\n")
main=(KIT/"main.tex").read_text(encoding="utf-8")
if '\\input{sec/0_abstract}' not in main:
    main=main.replace('\\maketitle\n', '\\maketitle\n\n\\input{sec/0_abstract}\n')
if '\\input{sec/5_conclusion}' not in main:
    main=main.replace('\\input{sec/4_experiments}', '\\input{sec/4_experiments}\n\n\\input{sec/5_conclusion}')
(KIT/"main.tex").write_text(main,encoding="utf-8",newline="\n")

# Chinese abstract and conclusion
raw=CN.read_bytes(); bom=raw.startswith(b'\xef\xbb\xbf'); text=raw.decode('utf-8-sig')
text=text.replace('*Introduction、Related Work、Method、Experiments 英文初稿的独立中文对照版。当前已整理 Introduction、Related Work、Method 与 Experiments；其余章节待补。', '*Abstract、Introduction、Related Work、Method、Experiments、Conclusion 的独立中文对照版。当前各主要章节已整理。')
if '## 摘要' not in text:
    text=text.replace('## 1. 引言', cn_abs.strip()+'\n\n## 1. 引言')
else:
    s=text.index('## 摘要'); e=text.index('## 1. 引言',s); text=text[:s]+cn_abs.strip()+'\n\n'+text[e:]
if '## 5. 结论' not in text:
    text=text.rstrip()+'\n\n'+cn_con.strip()+'\n'
else:
    s=text.index('## 5. 结论'); text=text[:s]+cn_con.strip()+'\n'
CN.write_text(text,encoding='utf-8-sig' if bom else 'utf-8',newline='\n')

mapping=ROOT/'中文论文'/'中英章节对应.md'
mt=mapping.read_text(encoding='utf-8-sig')
mt=mt.replace('| `论文中文版.md` / 摘要 | `sec/0_abstract.tex` | 待撰写 |', '| `论文中文版.md` / 摘要 | `sec/0_abstract.tex` | 已完成 |')
mt=mt.replace('| `论文中文版.md` / 结论 | `sec/5_conclusion.tex` | 待整理 |', '| `论文中文版.md` / 结论 | `sec/5_conclusion.tex` | 已完成 |')
mapping.write_text(mt,encoding='utf-8',newline='\n')
print('abstract and conclusion written')
