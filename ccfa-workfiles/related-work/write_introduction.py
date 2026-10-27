from pathlib import Path

ROOT=Path(r"D:\论文\9.27论文")
KIT=ROOT/"author-kit-main"
CN=ROOT/"中文论文"/"论文中文版.md"

cn_intro=r'''## 1. 引言

开放词汇语义分割要求模型在推理时根据任意类别词表，为图像中的每个像素分配类别。早期免训练方法主要改造视觉—语言模型的稠密相似度 [1,6]。SAM3 将计算对象推进到文本概念条件下的共享 grounding：同一概念既参与类别识别，也参与稠密 mask 和 query 区域生成 [10]。SegEarth-OV3 将这一接口用于遥感开放词汇分割 [11]。共享 concept 因此不再只是一个类别模板，而是同时约束多个空间输出的条件状态。

共享带来了稳定的类别共识，但三种 readout 的职责并不相同。Presence 判断类别是否在场景中出现，Semantic 估计稠密覆盖，Instance 组织 query 生成的区域和边界。遥感图像进一步放大了这种差异：小目标、连续地表和场景级存在性往往需要不同尺度的视觉证据；已有评估也表明，SAM3 的概念存在性与定位能力并不总是同步 [24]。因此，“同一概念、同一观察足以服务所有 readout”是一个需要检验的假设。

现有方法主要从类别提示或输出融合入手。TMPA 根据图像调整 CLIP 文本嵌入 [8]；ConceptBank 用支持集评价并融合候选概念 [9]；ProC-SAM3 构造受约束提示池，并对多提示输出做残差融合 [12]；CoCo-SAM3 聚合同义证据并校准类别竞争 [13]；RSGPNet 用几何提示和一致性校验改进 SAM3 的局部定位 [25]。这些方法提升了提示覆盖、概念边界或预测组合，但通常把补充描述看作类别级的整体条件，或直接聚合完整输出。一条描述重新进入 grounding 后会同时影响多个输出；它可能改善稠密覆盖，却改变存在性判断或 query 组织。此外，替换官方类别词会改变数据集 ontology 的锚点。本文保留完整 grounding 与官方 anchor，只在输出使用层面区分不同 role 的证据。

仅有文本补充还不够。文本可以要求连续覆盖或完整区域，却不能提供当前观察中不存在的视觉内容。局部裁块保留细节，但可能切断长距离结构；更大范围提供上下文，却会降低小目标的有效采样。HRDA、GLA-CLIP、OV-Stitcher 和 ConInfer 已分别从多分辨率、跨窗口注意力、窗口拼接和场景级推断处理这一权衡 [14,15,18,26]。这些方法说明视觉观察确实提供互补信息，但通常通过修改注意力、特征或固定融合规则实现。对本文的问题而言，补充信息是否有用还取决于它需要从哪个观察中读取，以及它与当前 role 配置是否匹配。

据此，本文提出角色—视图证据专门化（Role–View Evidence Specialization，JRV）。JRV 首先保留官方类别词与别名产生的 anchor，并为 Presence、Semantic、Instance 组织角色功能候选；每条候选都完成冻结 SAM3 的完整 grounding，只将其对应 readout 的变化以有界残差写回，同时保留 Presence 对 query admission、instance 幅度和最终类别分数的原生耦合。随后，对同一目标区域构造空间对齐的 Local 与 Context 观察，每个观察分别完成完整 grounding；两个观察复用同一组角色配置，在目标坐标上组合完整类别分数场，最后沿用基线的跨类别 argmax 和背景阈值。方法不修改 SAM3 内部 attention，也不为每个 head 分配独立视觉路径。

本文的贡献包括：

- 将共享概念适配从类别级推进到 readout 级，提出保留 anchor 的 Role-Functional Text，使补充文本按 Presence、Semantic 和 Instance 的计算职责进入，而不破坏官方 ontology 或 P–I 原生耦合。
- 提出 Joint Role–View evidence specialization，在完整、冻结的 Local 与 Context grounding 之后组合对齐的类别证据，把角色文本与视觉观察作为联合条件，而非两个独立附加模块。
- 在八个遥感数据集上系统评估方法的有效性、条件互补和作用范围。配对实验的平均 mIoU 从 baseline 的 53.56 提升到 Role-only 的 55.82 和 Joint 的 57.49；全部八个数据集均超过 baseline，固定 Role×View 配置在六个数据集上呈正交互。Cityscapes 与 VOC20 的自然域评估进一步检验角色补充的迁移性，并显示视图组合仍依赖数据分布。
'''

en_intro=r'''\section{Introduction}
\label{sec:introduction}

Open-vocabulary semantic segmentation assigns every pixel a category specified at inference time. Early training-free systems adapt vision-language models to produce dense similarity fields \cite{R01,R06}. SAM3 moves the computational object further: a text concept conditions a shared grounding process that supports category recognition, dense masks, and query-based regions \cite{R10}. SegEarth-OV3 applies this interface to remote sensing \cite{R11}. A shared concept is therefore not merely a class template; it is a condition that constrains several spatial outputs at once.

Sharing this condition stabilizes category semantics, but the three readouts serve different functions. Presence decides whether the concept occurs in the scene, Semantic estimates dense extent, and Instance organizes query-generated regions and boundaries. Remote sensing exposes the difference: small objects, continuous land cover, and scene-level existence require different visual evidence, and evaluations of SAM3 in overhead imagery show that concept presence and localization do not always improve together \cite{R24}. The assumption that one concept and one observation suffice for all readouts therefore requires direct examination.

Existing methods mainly adapt class prompts or combine complete outputs. TMPA adjusts CLIP text embeddings using image evidence \cite{R08}; ConceptBank evaluates and fuses candidate concepts with a support set \cite{R09}; ProC-SAM3 constructs a constrained prompt pool and applies residual fusion to multi-prompt outputs \cite{R12}; CoCo-SAM3 aggregates synonymous evidence and calibrates competition among categories \cite{R13}; and RSGPNet uses geometric prompts with consistency verification to refine SAM3 localization \cite{R25}. These methods improve prompt coverage, concept boundaries, or prediction combination. Most treat a supplementary description as a category-level condition or aggregate complete predictions. Re-grounding a description affects several outputs simultaneously, so a phrase that improves dense coverage can alter existence estimation or query organization. Replacing the official class name also moves the ontology anchor. We retain complete grounding and the official anchor, and specialize how the resulting evidence is used by each role.

Text alone cannot resolve the second issue. A description can request continuous coverage or a complete region, but it cannot supply visual content absent from the current observation. Local crops preserve detail while potentially cutting long-range structure; a wider field exposes context while reducing the effective sampling of small objects. HRDA, GLA-CLIP, OV-Stitcher, and ConInfer address this trade-off through multi-resolution processing, cross-window attention, window stitching, and scene-level inference \cite{R14,R15,R18,R26}. Their results show that visual observations provide complementary evidence, usually through modified attention, features, or a fixed fusion rule. For role-specific supplementation, usefulness also depends on which observation contains the required evidence and how that evidence interacts with the selected role configuration.

We introduce Role--View Evidence Specialization (JRV). JRV preserves the anchor produced by official class names and aliases and organizes role-functional candidates for Presence, Semantic, and Instance. Each candidate completes a full frozen SAM3 grounding pass; only the change in its assigned readout is applied as a bounded residual. Presence continues to participate in query admission, instance amplitude, and final class scaling. The method then constructs spatially aligned Local and Context observations, grounds each observation completely, and reuses the same role configuration across both. Complete class-score fields are composed in the target coordinate system, followed by the baseline cross-category argmax and background threshold. JRV does not modify SAM3 attention or assign a separate visual path to each head.

The paper makes three contributions. First, it moves shared concept adaptation from the category level to the readout level and introduces anchor-preserving Role-Functional Text, which allocates supplementary text according to the computational roles of Presence, Semantic, and Instance while retaining the official ontology and native Presence--Instance coupling. Second, it introduces Joint Role--View evidence specialization, which composes aligned class evidence after complete frozen Local and Context grounding, treating role text and visual observation as joint conditions rather than independent add-ons. Third, it evaluates the method on eight remote-sensing datasets. The matched average mIoU increases from 53.56 at the baseline to 55.82 with Role-only and 57.49 with Joint specialization. All eight datasets improve over the baseline, and the fixed Role--View configuration has positive interaction on six. Evaluations on Cityscapes and VOC20 further probe the transfer of role supplementation and show that view composition remains distribution dependent.
'''

# English source
(KIT/"sec"/"1_intro.tex").write_text(en_intro,encoding="utf-8",newline="\n")
main=(KIT/"main.tex").read_text(encoding="utf-8")
if '\\input{sec/1_intro}' not in main:
    main=main.replace('\\input{sec/2_related_work}', '\\input{sec/1_intro}\n\n\\input{sec/2_related_work}')
else:
    # ensure introduction precedes related work exactly once
    main=main.replace('\\input{sec/2_related_work}\n\n\\input{sec/1_intro}', '\\input{sec/1_intro}\n\n\\input{sec/2_related_work}')
(KIT/"main.tex").write_text(main,encoding="utf-8",newline="\n")

# Chinese source
raw=CN.read_bytes(); bom=raw.startswith(b'\xef\xbb\xbf'); text=raw.decode('utf-8-sig')
text=text.replace('*Related Work、Method、Experiments 英文初稿的独立中文对照版。暂用 Joint Role–View Specialization（JRV）作为方法名。引用编号与[参考文献](参考文献.md)一致；“—”表示尚无结果，不是已完成实验。*', '*Introduction、Related Work、Method、Experiments 英文初稿的独立中文对照版。当前已整理 Introduction 与 Related Work；其余章节待补。暂用 Joint Role–View Specialization（JRV）作为方法名。引用编号与[参考文献](参考文献.md)一致。*')
if '## 1. 引言' not in text:
    text=text.replace('## 2. 相关工作', cn_intro.strip()+'\n\n## 2. 相关工作')
else:
    start=text.index('## 1. 引言'); end=text.index('## 2. 相关工作',start); text=text[:start]+cn_intro.strip()+'\n\n'+text[end:]
CN.write_text(text,encoding='utf-8-sig' if bom else 'utf-8',newline='\n')

# Update mapping status
mapping=ROOT/'中文论文'/'中英章节对应.md'
mt=mapping.read_text(encoding='utf-8-sig')
mt=mt.replace('| `论文中文版.md` / Introduction | `sec/1_intro.tex` | 待撰写 |', '| `论文中文版.md` / Introduction | `sec/1_intro.tex` | 已完成 |')
mapping.write_text(mt,encoding='utf-8',newline='\n')
print('written intro and updated main/mapping')
