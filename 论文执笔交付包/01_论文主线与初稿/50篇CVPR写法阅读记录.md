# 50 篇 CVPR 主会论文：结构、论证与图表阅读记录

日期：2026-09-05。范围为 **CVPR 2025 主会 25 篇 + CVPR 2026 主会 25 篇**，全部以 CVF 官方 proceedings 页面核验；Findings、arXiv 和较早论文没有充当这 50 篇的计数。开放词汇分割为中心，向遥感、密集预测、跨域及局部—全局建模扩展。

阅读粒度：逐篇阅读章节结构、方法入口和关键段落、实验/消融段落、表格比较对象及图注；渲染并检查了 50 篇的代表正文页面。对 TMPA、SegEarth-OV、GLA-CLIP、PEARL 等直接相关机制另读原方法。**这是 50 篇结构与关键内容的定向学习，不声称逐句精读所有正文和补充材料。**

PDF、官方页面、官方 BibTeX 和抽取文本保存在 `../_work/cvpr50/`；`sources.csv` 给出逐篇映射。每个题目链接均为主会官方来源。下列是阅读后的分析，不是原文摘抄。

## 共同采用、而非机械照抄的写作原则

1. Related Work 按“问题与解法”归类，每段结尾解释本文差异，不按论文年份逐篇报菜名。
2. Method 先定义输入、输出与原模型机制，然后每一小节按“缺口→操作→作用对象→与下一步关系”推进。
3. 主图给整体数据流；局部放大只画新操作。不用几十个实验代号代替方法名称。
4. 主表回答竞争力；配对模块表回答归因；结构替代对照回答“为什么这样做”；类别/定性图回答何处受益与边界。
5. 理论厚度来自准确的计算对象、前置条件和作用链；不是补一些未实现的公式或借来的定理。
6. 有监督、测试时梯度、冻结推理、标注支持、配置选择需分别说明；不同论文的数字不能自动视为同协议复现。

## 逐篇记录

### C01 · CVPR 2025 · [Dual Semantic Guidance for Open Vocabulary Semantic Segmentation](https://openaccess.thecvf.com/content/CVPR2025/html/Wang_Dual_Semantic_Guidance_for_Open_Vocabulary_Semantic_Segmentation_CVPR_2025_paper.html)

- 结构定位：1. Introduction；2. Related Work；3. Dual Semantic Guidance；4. Experiments；5. Conclusion。
- 方法论证：DSGG 生成监督、DSGS 利用监督，两个模块分别回答“得到什么”和“怎样使用”。
- 图表组织：框架图先给两阶段；消融比较注意力替代策略与监督损失，而非只堆组件。
- 对本稿的采用/边界：区分补充描述的产生与角色化使用；同信息、不同用途是关键对照。
- 本地原文：[PDF](../_work/cvpr50/C01.pdf)；[文本](../_work/cvpr50/C01.txt)。

### C02 · CVPR 2025 · [Understanding Fine-tuning CLIP for Open-vocabulary Semantic Segmentation in Hyperbolic Space](https://openaccess.thecvf.com/content/CVPR2025/html/Peng_Understanding_Fine-tuning_CLIP_for_Open-vocabulary_Semantic_Segmentation_in_Hyperbolic_Space_CVPR_2025_paper.html)

- 结构定位：1. Introduction；2. Related Work；3. Preliminary Background；4. Methodology；5. Experiments；6. Conclusion。
- 方法论证：先给双曲空间预备，再从半径变化引出具体微调操作与理论分析。
- 图表组织：半径可视化与受控半径实验对应同一解释，主表区分微调范式。
- 对本稿的采用/边界：理论必须描述我们实际操作；不把几何最优性借成 mIoU 保证。
- 本地原文：[PDF](../_work/cvpr50/C02.pdf)；[文本](../_work/cvpr50/C02.txt)。

### C03 · CVPR 2025 · [LPOSS: Label Propagation Over Patches and Pixels for Open-vocabulary Semantic Segmentation](https://openaccess.thecvf.com/content/CVPR2025/html/Stojnic_LPOSS_Label_Propagation_Over_Patches_and_Pixels_for_Open-vocabulary_Semantic_CVPR_2025_paper.html)

- 结构定位：1. Introduction；2. Related work；3. Label propagation over patches and pixels；3. This is a smoothening operation, which we also per-；1. Extract features Z (wi)；2. Upsample patch-level predictions to the original window；3. Obtain per-pixel predictions by averaging predictions；4. Experiments；5. Conclusion。
- 方法论证：LPOSS 按 patch 传播、跨窗口传播、pixel 传播的处理对象展开。
- 图表组织：窗口大小/步长控制与 Boundary IoU 补充主指标；流程图标出空间还原。
- 对本稿的采用/边界：我们的 Local 必须明确 crop→grounding→坐标还原→重叠聚合。
- 本地原文：[PDF](../_work/cvpr50/C03.pdf)；[文本](../_work/cvpr50/C03.txt)。

### C04 · CVPR 2025 · [Exploring Simple Open-Vocabulary Semantic Segmentation](https://openaccess.thecvf.com/content/CVPR2025/html/Lai_Exploring_Simple_Open-Vocabulary_Semantic_Segmentation_CVPR_2025_paper.html)

- 结构定位：1. Introduction；2. Related work；3. Approach；4. Experiments；5. Conclusion。
- 方法论证：S-Seg 先定义简单图文监督路线，再解释伪掩膜与自训练。
- 图表组织：先检验自然的简单替代方案，再报主结果；背景计分协议分开列。
- 对本稿的采用/边界：不能用复杂筛查记录代替最直观的普通多提示对照。
- 本地原文：[PDF](../_work/cvpr50/C04.pdf)；[文本](../_work/cvpr50/C04.txt)。

### C05 · CVPR 2025 · [Mask-Adapter: The Devil is in the Masks for Open-Vocabulary Segmentation](https://openaccess.thecvf.com/content/CVPR2025/html/Li_Mask-Adapter_The_Devil_is_in_the_Masks_for_Open-Vocabulary_Segmentation_CVPR_2025_paper.html)

- 结构定位：1. Introduction；2. Related Work；3. Approach；4. Experiments；5. Conclusion。
- 方法论证：Mask-Adapter 从“已有好 mask 仍然分类不好”定位区域读出问题。
- 图表组织：GT mask 条件下的诊断与真实推理结果分开；主图放大 adapter。
- 对本稿的采用/边界：相关性/上界诊断用于定位，不代替最终方法的真实收益。
- 本地原文：[PDF](../_work/cvpr50/C05.pdf)；[文本](../_work/cvpr50/C05.txt)。

### C06 · CVPR 2025 · [Fine-Grained Image-Text Correspondence with Cost Aggregation for Open-Vocabulary Part Segmentation](https://openaccess.thecvf.com/content/CVPR2025/html/Choi_Fine-Grained_Image-Text_Correspondence_with_Cost_Aggregation_for_Open-Vocabulary_Part_Segmentation_CVPR_2025_paper.html)

- 结构定位：1. Introduction；2. Related Work；3. Method；4. Experiments；5. Conclusion。
- 方法论证：PartCATSeg 将 object 与 part 的粒度矛盾映射到两路 cost 与引导。
- 图表组织：结构图使用同色模块贯通输入、聚合和输出；消融比较聚合及引导来源。
- 对本稿的采用/边界：三角色是计算职责，不粗暴等同 thing/stuff 或局部/全局。
- 本地原文：[PDF](../_work/cvpr50/C06.pdf)；[文本](../_work/cvpr50/C06.txt)。

### C07 · CVPR 2025 · [Parameter-efficient Fine-tuning in Hyperspherical Space for Open-vocabulary Semantic Segmentation](https://openaccess.thecvf.com/content/CVPR2025/html/Peng_Parameter-efficient_Fine-tuning_in_Hyperspherical_Space_for_Open-vocabulary_Semantic_Segmentation_CVPR_2025_paper.html)

- 结构定位：1. Introduction；2. Related Work；3. Preliminaries；4. Methodology；5. Experiments；6. Conclusion。
- 方法论证：H-CLIP 先定义需要保存的几何关系，再给参数化及通信模块。
- 图表组织：理论对象、约束和模型插入点逐项对齐；主表分骨干。
- 对本稿的采用/边界：只陈述有界更新的实际性质，不虚构强正确性定理。
- 本地原文：[PDF](../_work/cvpr50/C07.pdf)；[文本](../_work/cvpr50/C07.txt)。

### C08 · CVPR 2025 · [DPSeg: Dual-Prompt Cost Volume Learning for Open-Vocabulary Semantic Segmentation](https://openaccess.thecvf.com/content/CVPR2025/html/Zhao_DPSeg_Dual-Prompt_Cost_Volume_Learning_for_Open-Vocabulary_Semantic_Segmentation_CVPR_2025_paper.html)

- 结构定位：1. Introduction；2. Related Work；3. Discussion and Motivation；4. Method；5. Experiments；6. Conclusion。
- 方法论证：DPSeg 显式讨论模态差距，再提出双 prompt cost 与二次细化。
- 图表组织：单一 embedding 平均、cost 平均、cost 拼接等同级替代比较。
- 对本稿的采用/边界：比较信息进入哪里；不能把它写成 SAM3 的免训练先例。
- 本地原文：[PDF](../_work/cvpr50/C08.pdf)；[文本](../_work/cvpr50/C08.txt)。

### C09 · CVPR 2025 · [Effective SAM Combination for Open-Vocabulary Semantic Segmentation](https://openaccess.thecvf.com/content/CVPR2025/html/Lee_Effective_SAM_Combination_for_Open-Vocabulary_Semantic_Segmentation_CVPR_2025_paper.html)

- 结构定位：1. Introduction；2. Related Work；3. Proposed Approach；4. Experiments；5. Conclusion。
- 方法论证：ESC-Net 将 CLIP correlation 转为伪 prompt，再复用 SAM 并进行跨模态融合。
- 图表组织：总体架构与伪提示/融合细节分图；点、框、mask 有组合消融。
- 对本稿的采用/边界：我们的模型是原生 concept grounding，不是 CLIP 生成点再提示 SAM。
- 本地原文：[PDF](../_work/cvpr50/C09.pdf)；[文本](../_work/cvpr50/C09.txt)。

### C10 · CVPR 2025 · [SegEarth-OV: Towards Training-Free Open-Vocabulary Segmentation for Remote Sensing Images](https://openaccess.thecvf.com/content/CVPR2025/html/Li_SegEarth-OV_Towards_Training-Free_Open-Vocabulary_Segmentation_for_Remote_Sensing_Images_CVPR_2025_paper.html)

- 结构定位：1. Introduction；2. Related Work；3. Preliminaries；4. Method；5. Experiments；6. Conclusion。
- 方法论证：SegEarth-OV 从分辨率不足与 global bias 两个具体矛盾引出模块。
- 图表组织：主多类表、二类任务、模块消融、可迁移性各司其职。
- 对本稿的采用/边界：主线写问题—操作—证据；背景不照搬 CLIP 到 SAM3。
- 本地原文：[PDF](../_work/cvpr50/C10.pdf)；[文本](../_work/cvpr50/C10.txt)。

### C11 · CVPR 2025 · [Distilling Spectral Graph for Object-Context Aware Open-Vocabulary Semantic Segmentation](https://openaccess.thecvf.com/content/CVPR2025/html/Kim_Distilling_Spectral_Graph_for_Object-Context_Aware_Open-Vocabulary_Semantic_Segmentation_CVPR_2025_paper.html)

- 结构定位：1. Introduction；2. Related Works；3. Method；4. Experiments；5. Conclusion。
- 方法论证：CASS 分对象级图结构与类别存在上下文，按信息来源展开。
- 图表组织：图结构的处理前后对照和多骨干支持机制；mIoU 与 pAcc 分表。
- 对本稿的采用/边界：角色互补需自己的配对证据，不借别人的注意力图解释。
- 本地原文：[PDF](../_work/cvpr50/C11.pdf)；[文本](../_work/cvpr50/C11.txt)。

### C12 · CVPR 2025 · [Semantic Library Adaptation: LoRA Retrieval and Fusion for Open-Vocabulary Semantic Segmentation](https://openaccess.thecvf.com/content/CVPR2025/html/Qorbani_Semantic_Library_Adaptation_LoRA_Retrieval_and_Fusion_for_Open-Vocabulary_Semantic_CVPR_2025_paper.html)

- 结构定位：1. Introduction；2. Related Work；3. Method and Framework；4. Experiment Setup and Results；1. For each dataset, we train an adapter on its training set.；2. When evaluating on a particular dataset, we remove its；3. We repeat the process for each dataset, ensuring that the；5. Conclusion。
- 方法论证：SemLA 将离线 LoRA 库与在线检索融合分成两个明确阶段。
- 图表组织：leave-one-domain-out 和 all-inclusive 分表，训练资源在协议中说明。
- 对本稿的采用/边界：冻结推理与配置选择是否使用标签是两个问题，设置中统一交代。
- 本地原文：[PDF](../_work/cvpr50/C12.pdf)；[文本](../_work/cvpr50/C12.txt)。

### C13 · CVPR 2025 · [DeCLIP: Decoupled Learning for Open-Vocabulary Dense Perception](https://openaccess.thecvf.com/content/CVPR2025/html/Wang_DeCLIP_Decoupled_Learning_for_Open-Vocabulary_Dense_Perception_CVPR_2025_paper.html)

- 结构定位：1. Introduction；2. Background and Motivation；3. Method；4. Experiments；5. Conclusion。
- 方法论证：DeCLIP 先展示联合监督的冲突，再分 content/context 进行蒸馏。
- 图表组织：朴素合并基线显示任务之间的损益，支撑结构设计而非只支撑总分。
- 对本稿的采用/边界：借鉴“损益随用途变化”的论证，不照搬内部解耦到 SAM3。
- 本地原文：[PDF](../_work/cvpr50/C13.pdf)；[文本](../_work/cvpr50/C13.txt)。

### C14 · CVPR 2025 · [Hybrid Global-Local Representation with Augmented Spatial Guidance for Zero-Shot Referring Image Segmentation](https://openaccess.thecvf.com/content/CVPR2025/html/Liu_Hybrid_Global-Local_Representation_with_Augmented_Spatial_Guidance_for_Zero-Shot_Referring_CVPR_2025_paper.html)

- 结构定位：1. Introduction；2. Related Work；3. Method；4. Experiments；5. Conclusion。
- 方法论证：Hybrid Global-Local RIS 区分目标局部识别与上下文空间关系。
- 图表组织：mask/crop、blur/token mask、空间关系等替代对照解释各自职责。
- 对本稿的采用/边界：可借采样互补的思路，但其 proposal 评分不等于我们的 dense 预测。
- 本地原文：[PDF](../_work/cvpr50/C14.pdf)；[文本](../_work/cvpr50/C14.txt)。

### C15 · CVPR 2025 · [SAM-REF: Introducing Image-Prompt Synergy during Interaction for Detail Enhancement in the Segment Anything Model](https://openaccess.thecvf.com/content/CVPR2025/html/Yu_SAM-REF_Introducing_Image-Prompt_Synergy_during_Interaction_for_Detail_Enhancement_in_CVPR_2025_paper.html)

- 结构定位：1. Introduction；2. Related Work；3. Method；0. If the error ratio Re is larger than a threshold θ, it indi-；4. Experiments；5. Ablation Experiments；6. Qualitative Result；7. Conclusion；8. Acknowledgement。
- 方法论证：SAM-REF 从图像与 prompt 交互位置引出 global/local refinement。
- 图表组织：比较将 local 贴回原 SAM 或 global-refined 结果，验证组合位置。
- 对本稿的采用/边界：控制组合接口比反复调强度更能证明问题。
- 本地原文：[PDF](../_work/cvpr50/C15.pdf)；[文本](../_work/cvpr50/C15.txt)。

### C16 · CVPR 2025 · [SkySense-O: Towards Open-World Remote Sensing Interpretation with Vision-Centric Visual-Language Modeling](https://openaccess.thecvf.com/content/CVPR2025/html/Zhu_SkySense-O_Towards_Open-World_Remote_Sensing_Interpretation_with_Vision-Centric_Visual-Language_Modeling_CVPR_2025_paper.html)

- 结构定位：1. Introduction；2. Related work；3. Sky-SA Dataset；4. SkySense-O Model；5. Experiment；6. Conclusion。
- 方法论证：SkySense-O 先交代数据缺口，再写数据引擎与 vision-centric 训练。
- 图表组织：数据性质表和任务结果表分开；消融区分训练数据与建模选择。
- 对本稿的采用/边界：Related Work 区分训练式遥感基础模型与我们的冻结适配。
- 本地原文：[PDF](../_work/cvpr50/C16.pdf)；[文本](../_work/cvpr50/C16.txt)。

### C17 · CVPR 2025 · [SegMAN: Omni-scale Context Modeling with State Space Models and Local Attention for Semantic Segmentation](https://openaccess.thecvf.com/content/CVPR2025/html/Fu_SegMAN_Omni-scale_Context_Modeling_with_State_Space_Models_and_Local_CVPR_2025_paper.html)

- 结构定位：1. Introduction；2. Related work；3. Method；4. Experiments；2. As shown in Table 4, SegMAN-T achieves +1.6%；5. Conclusion。
- 方法论证：SegMAN 将全局上下文、局部细节、多尺度对应 encoder/decoder 设计。
- 图表组织：总图与局部 block 同页层次清楚；encoder、decoder 分别验证。
- 对本稿的采用/边界：我们的文本作用与观察范围各有位置，但要在联合表验证连接。
- 本地原文：[PDF](../_work/cvpr50/C17.pdf)；[文本](../_work/cvpr50/C17.txt)。

### C18 · CVPR 2025 · [Mamba as a Bridge: Where Vision Foundation Models Meet Vision Language Models for Domain-Generalized Semantic Segmentation](https://openaccess.thecvf.com/content/CVPR2025/html/Zhang_Mamba_as_a_Bridge_Where_Vision_Foundation_Models_Meet_Vision_CVPR_2025_paper.html)

- 结构定位：1. Introduction；2. Related Works；3. Preliminary；4. Proposed Method；5. Experiments；6. Conclusions。
- 方法论证：MFuser 用 VFM 局部特征与 VLM 文本对齐的差异引出桥接模块。
- 图表组织：先给两种特征的例子，再做 fuser 与文本增强替代消融。
- 对本稿的采用/边界：解释互补要指向具体缺失的信息；不能仅称“两模态更丰富”。
- 本地原文：[PDF](../_work/cvpr50/C18.pdf)；[文本](../_work/cvpr50/C18.txt)。

### C19 · CVPR 2025 · [SemiDAViL: Semi-supervised Domain Adaptation with Vision-Language Guidance for Semantic Segmentation](https://openaccess.thecvf.com/content/CVPR2025/html/Basak_SemiDAViL_Semi-supervised_Domain_Adaptation_with_Vision-Language_Guidance_for_Semantic_Segmentation_CVPR_2025_paper.html)

- 结构定位：1. Introduction；1. Language-Guided SSDA Framework: We pioneer the；2. Enhanced Feature Localization: Recognizing that VL；3. Adaptive Class-Balanced Loss: To tackle class imbal-；4. State-of-the-Art Performance: Through detailed eval-；2. Related Works；3. Proposed Method；4. Experimental Results；5. Conclusion。
- 方法论证：SemiDAViL 将类别混淆和类别不平衡映射到语言引导与损失。
- 图表组织：标注量、域、监督类型分别控制；模块表和类别解释分层。
- 对本稿的采用/边界：我们的数据集平均与类别平均分别报告，避免混用统计单位。
- 本地原文：[PDF](../_work/cvpr50/C19.pdf)；[文本](../_work/cvpr50/C19.txt)。

### C20 · CVPR 2025 · [Exploring CLIP's Dense Knowledge for Weakly Supervised Semantic Segmentation](https://openaccess.thecvf.com/content/CVPR2025/html/Yang_Exploring_CLIPs_Dense_Knowledge_for_Weakly_Supervised_Semantic_Segmentation_CVPR_2025_paper.html)

- 结构定位：1. Introduction；2. Related Works；1. Have striking eyes.；2. Retractable claws.；3. Methodology；4. Experiments and Results；5. Conclusion。
- 方法论证：ExCEL 从 patch-text 对齐切入，区分文本语义与视觉校准。
- 图表组织：训练免训练结果、CAM seed 与最终 segmentation 分表。
- 对本稿的采用/边界：辅助响应增强与最终分割提升不能当成同一结果。
- 本地原文：[PDF](../_work/cvpr50/C20.pdf)；[文本](../_work/cvpr50/C20.txt)。

### C21 · CVPR 2025 · [POT: Prototypical Optimal Transport for Weakly Supervised Semantic Segmentation](https://openaccess.thecvf.com/content/CVPR2025/html/Wang_POT_Prototypical_Optimal_Transport_for_Weakly_Supervised_Semantic_Segmentation_CVPR_2025_paper.html)

- 结构定位：1. Introduction；2. Related Work；3. Methodology；4. Experiment；5. Conclusion。
- 方法论证：POT 从单 prototype 无法覆盖多模态外观引出分区、分配、激活。
- 图表组织：single/multi cluster 与 OT 单独消融，CAM 与分割分别评价。
- 对本稿的采用/边界：描述信息量与使用结构需要分开控制。
- 本地原文：[PDF](../_work/cvpr50/C21.pdf)；[文本](../_work/cvpr50/C21.txt)。

### C22 · CVPR 2025 · [Convex Combination Star Shape Prior for Data-driven Image Semantic Segmentation](https://openaccess.thecvf.com/content/CVPR2025/html/Zhao_Convex_Combination_Star_Shape_Prior_for_Data-driven_Image_Semantic_Segmentation_CVPR_2025_paper.html)

- 结构定位：1. Introduction；2. Related work；3. Method；4. Numerical experiments；5. Conclusion；6. Acknowledgements。
- 方法论证：CCS Shape 先数学定义，再推平滑约束，最后实例化到模型。
- 图表组织：模块/损失/后处理三种接口比较；形状假设有具体成立条件。
- 对本稿的采用/边界：有形式化条件才能谈结构保证；我们的 region prompt 不是拓扑保证。
- 本地原文：[PDF](../_work/cvpr50/C22.pdf)；[文本](../_work/cvpr50/C22.txt)。

### C23 · CVPR 2025 · [Weakly Supervised Semantic Segmentation via Progressive Confidence Region Expansion](https://openaccess.thecvf.com/content/CVPR2025/html/Xu_Weakly_Supervised_Semantic_Segmentation_via_Progressive_Confidence_Region_Expansion_CVPR_2025_paper.html)

- 结构定位：1. Introduction；2. Related work；3. Methods；4. Experiments；5. Conclusion。
- 方法论证：PCRE 将 over-expansion 明确为方法针对的问题。
- 图表组织：CAM、伪标签、最终结果分别列，逐步扩张示意图解释具体操作。
- 对本稿的采用/边界：不要把“覆盖更多像素”写成“必然更准确”，记录 correction/damage。
- 本地原文：[PDF](../_work/cvpr50/C23.pdf)；[文本](../_work/cvpr50/C23.txt)。

### C24 · CVPR 2025 · [DFormerv2: Geometry Self-Attention for RGBD Semantic Segmentation](https://openaccess.thecvf.com/content/CVPR2025/html/Yin_DFormerv2_Geometry_Self-Attention_for_RGBD_Semantic_Segmentation_CVPR_2025_paper.html)

- 结构定位：1. Introduction；2. Related Work；3. Methodology；4. Experiments；1024. More detailed settings for each variant of DFormerv2；5. Conclusions。
- 方法论证：DFormerv2 反问 depth 是否必须再经独立 encoder，提出几何先验 attention。
- 图表组织：旧双编码与新先验接口并排；模态控制区分语义与形状贡献。
- 对本稿的采用/边界：Related Work 比较使用机制，不只列共享关键词。
- 本地原文：[PDF](../_work/cvpr50/C24.pdf)；[文本](../_work/cvpr50/C24.txt)。

### C25 · CVPR 2025 · [Scaling up Image Segmentation across Data and Tasks](https://openaccess.thecvf.com/content/CVPR2025/html/Wang_Scaling_up_Image_Segmentation_across_Data_and_Tasks_CVPR_2025_paper.html)

- 结构定位：1. Introduction；2. Related Work；3. Method；4. Experiments；5. Conclusion。
- 方法论证：MQ-Former 按 mixed query 设计、数据/任务扩展展开。
- 图表组织：learnable/conditional/mixed query 在相同任务设置直接比较。
- 对本稿的采用/边界：角色/查询含义必须明确；主表不要混合不同任务指标。
- 本地原文：[PDF](../_work/cvpr50/C25.pdf)；[文本](../_work/cvpr50/C25.txt)。

### C26 · CVPR 2026 · [SynCLIP: Synonym-Coherent Language-Image Pretraining for Robust Open-Vocabulary Dense Perception](https://openaccess.thecvf.com/content/CVPR2026/html/Xie_SynCLIP_Synonym-Coherent_Language-Image_Pretraining_for_Robust_Open-Vocabulary_Dense_Perception_CVPR_2026_paper.html)

- 结构定位：1. Introduction；2. Related Work；3. Proposed Method；4. Experiments；5. Conclusion。
- 方法论证：SynCLIP 以同义词导致 grounding 不一致作为中心现象。
- 图表组织：同义词实例表、attention 对比、独立与联合模块消融形成闭环。
- 对本稿的采用/边界：更像人类同义的文字未必产生相同 mask，支持按功能评价提示。
- 本地原文：[PDF](../_work/cvpr50/C26.pdf)；[文本](../_work/cvpr50/C26.txt)。

### C27 · CVPR 2026 · [ReAttnCLIP: Training-Free Open-Vocabulary Remote Sensing Image Segmentation via Re-defined Attention in CLIP](https://openaccess.thecvf.com/content/CVPR2026/html/Niu_ReAttnCLIP_Training-Free_Open-Vocabulary_Remote_Sensing_Image_Segmentation_via_Re-defined_Attention_CVPR_2026_paper.html)

- 结构定位：1. Introduction；2. Related Work；3. Preliminaries；4. Method；5. Experiment；4. Computing similarity using XX ⊤ yields the most sig-；6. Conclusion。
- 方法论证：ReAttnCLIP 先展开原 attention 的贡献项，再针对不同项修正。
- 图表组织：主遥感表与单类任务分开，逐组件和替代相似度检验计算解释。
- 对本稿的采用/边界：P 对 query admission、幅度、最终分数的耦合要写清。
- 本地原文：[PDF](../_work/cvpr50/C27.pdf)；[文本](../_work/cvpr50/C27.txt)。

### C28 · CVPR 2026 · [Retrieve and Segment: Are a Few Examples Enough to Bridge the Supervision Gap in Open-Vocabulary Segmentation?](https://openaccess.thecvf.com/content/CVPR2026/html/Aravanis_Retrieve_and_Segment_Are_a_Few_Examples_Enough_to_Bridge_CVPR_2026_paper.html)

- 结构定位：1. Introduction；2. Related work；3. Method；4. Experiments；5. Conclusion。
- 方法论证：RNS 先形式化完整/缺失视觉与文本支持，再定义检索融合。
- 图表组织：有无标注、support 数量、域数据分栏；按信息可用性组织实验。
- 对本稿的采用/边界：我们的方法没有在线外部样本库，不能混称同一种 training-free 设置。
- 本地原文：[PDF](../_work/cvpr50/C28.pdf)；[文本](../_work/cvpr50/C28.txt)。

### C29 · CVPR 2026 · [Direct Segmentation without Logits Optimization for Training-Free Open-Vocabulary Semantic Segmentation](https://openaccess.thecvf.com/content/CVPR2026/html/Li_Direct_Segmentation_without_Logits_Optimization_for_Training-Free_Open-Vocabulary_Semantic_Segmentation_CVPR_2026_paper.html)

- 结构定位：1. Introduction；2. Related Works；3. Approach；4. Experiments；5. Conclusion。
- 方法论证：Direct Segmentation 先重新表述目标，再推解析操作及对应变体。
- 图表组织：常规 raw-logit baseline 与各解析步骤逐项比较。
- 对本稿的采用/边界：数学只保留帮助读者理解实际计算的部分。
- 本地原文：[PDF](../_work/cvpr50/C29.pdf)；[文本](../_work/cvpr50/C29.txt)。

### C30 · CVPR 2026 · [Mitigating Objectness Bias and Region-to-Text Misalignment for Open-Vocabulary Panoptic Segmentation](https://openaccess.thecvf.com/content/CVPR2026/html/Kormushev_Mitigating_Objectness_Bias_and_Region-to-Text_Misalignment_for_Open-Vocabulary_Panoptic_Segmentation_CVPR_2026_paper.html)

- 结构定位：1. Introduction；2. Related Work；3. OVRCOAT；4. Experiments；5. Conclusion。
- 方法论证：OVRCOAT 将 objectness 提前丢 mask 与区域文本错配分开处理。
- 图表组织：2×2 因子表之外，还有 mask 阶段与类别层分析。
- 对本稿的采用/边界：我们的 PI 耦合属于原生机制；主文不要用角色名称替代机制。
- 本地原文：[PDF](../_work/cvpr50/C30.pdf)；[文本](../_work/cvpr50/C30.txt)。

### C31 · CVPR 2026 · [HOPS: Hierarchical Open-vocabulary Part Segmentation with Attention-Aware Filtering and Affinity-Guided Enhancement](https://openaccess.thecvf.com/content/CVPR2026/html/Li_HOPS_Hierarchical_Open-vocabulary_Part_Segmentation_with_Attention-Aware_Filtering_and_Affinity-Guided_CVPR_2026_paper.html)

- 结构定位：1. Introduction；2. Related Work；3. Problem Analysis；4. Method；5. Experiments；6. Conclusion。
- 方法论证：HOPS 单列 Problem Analysis：对象过分割与部件欠分割不同。
- 图表组织：mOSI/mUSI 对应两个具体问题，非只有最终 h-IoU。
- 对本稿的采用/边界：角色结论应有用途控制；结构连通未量化时不宣称拓扑改善。
- 本地原文：[PDF](../_work/cvpr50/C31.pdf)；[文本](../_work/cvpr50/C31.txt)。

### C32 · CVPR 2026 · [Reconstructing CLIP for Open-Vocabulary Dense Perception](https://openaccess.thecvf.com/content/CVPR2026/html/Liu_Reconstructing_CLIP_for_Open-Vocabulary_Dense_Perception_CVPR_2026_paper.html)

- 结构定位：1. Introduction；2. Related Work；3. Method；4. Experiments；5. Conclusion。
- 方法论证：DenseRC 从 CLS 实际聚合了什么推出 dense feature 构造。
- 图表组织：消融 multi-value 时先关 attention 模块，以免混淆因素。
- 对本稿的采用/边界：配对消融固定角色与视图配置，不能用各自最优替代。
- 本地原文：[PDF](../_work/cvpr50/C32.pdf)；[文本](../_work/cvpr50/C32.txt)。

### C33 · CVPR 2026 · [MM-OVSeg: Multimodal Optical-SAR Fusion for Open-Vocabulary Segmentation in Remote Sensing](https://openaccess.thecvf.com/content/CVPR2026/html/Wei_MM-OVSeg_Multimodal_Optical-SAR_Fusion_for_Open-Vocabulary_Segmentation_in_Remote_Sensing_CVPR_2026_paper.html)

- 结构定位：1. Introduction；2. Related Work；3. Method；4. Experiments；5. Conclusion。
- 方法论证：MM-OVSeg 从云遮挡下光学证据缺失引出 SAR 与两阶段融合。
- 图表组织：天气、域、模态设置先用表定义，随后结果表一一对应。
- 对本稿的采用/边界：明确我们是 RGB 的不同观察，不是 Optical-SAR 多模态方法。
- 本地原文：[PDF](../_work/cvpr50/C33.pdf)；[文本](../_work/cvpr50/C33.txt)。

### C34 · CVPR 2026 · [SegEarth-R2: Towards Comprehensive Language-guided Segmentation for Remote Sensing Images](https://openaccess.thecvf.com/content/CVPR2026/html/Xin_SegEarth-R2_Towards_Comprehensive_Language-guided_Segmentation_for_Remote_Sensing_Images_CVPR_2026_paper.html)

- 结构定位：1. Introduction；2. Related works；3. LaSeRS Dataset；1. Prompt_1: single-target explicit；2. Prompt_2: single-target implicit；3. Prompt_3: multi-target explicit；4. Prompt_4: multi-target explicit；1. Prompt_1: single-target explicit；2. Prompt_2: single-target；3. Prompt_3: multi-target explicit；4. Prompt_4: multi-target explicit；1. Object recognition: Verifying the accuracy；2. Spatial description and logical consistency；3. Mask quality: Assessing if the annotated；4. Grammatical error: Checking for；4. SegEarth-R2；5. Experiment；6. Conclusion。
- 方法论证：SegEarth-R2 从复杂指令维度定义任务，再说明数据与分割 query。
- 图表组织：按粒度、多目标、推理、语言多样性分解能力。
- 对本稿的采用/边界：我们的 role prompt 是类别补充，不夸成复杂指令推理或新数据任务。
- 本地原文：[PDF](../_work/cvpr50/C34.pdf)；[文本](../_work/cvpr50/C34.txt)。

### C35 · CVPR 2026 · [PCA-Seg: Revisiting Cost Aggregation for Open-Vocabulary Semantic and Part Segmentation](https://openaccess.thecvf.com/content/CVPR2026/html/Yin_PCA-Seg_Revisiting_Cost_Aggregation_for_Open-Vocabulary_Semantic_and_Part_Segmentation_CVPR_2026_paper.html)

- 结构定位：1. Introduction；2. Related Work；3. Method；4. Experiments；5. Conclusion。
- 方法论证：PCA-Seg 从串行空间/类别聚合的干扰转向并行 cost aggregation。
- 图表组织：serial/parallel 直接对照先于专家与正交项；语义/部件协议分表。
- 对本稿的采用/边界：主动区分“角色使用”与内部特征解耦，避免仅换术语的创新陈述。
- 本地原文：[PDF](../_work/cvpr50/C35.pdf)；[文本](../_work/cvpr50/C35.txt)。

### C36 · CVPR 2026 · [Beyond Text: Visual Description Assembly by Probabilistic Model for CLIP-based Weakly Supervised Semantic Segmentation](https://openaccess.thecvf.com/content/CVPR2026/html/Qiu_Beyond_Text_Visual_Description_Assembly_by_Probabilistic_Model_for_CLIP-based_CVPR_2026_paper.html)

- 结构定位：1. Introduction；2. Related Works；3. Methodology；4. Experiments and Results；5. Conclusion。
- 方法论证：VDA 从静态文字原型不足转向视觉属性分布与组合原型。
- 图表组织：属性组件表、静态/动态融合曲线、CAM 对比解释信息进入方式。
- 对本稿的采用/边界：文本不必越长越好；我们保留类别锚点而非以自预测替换语义。
- 本地原文：[PDF](../_work/cvpr50/C36.pdf)；[文本](../_work/cvpr50/C36.txt)。

### C37 · CVPR 2026 · [Training-Free Open-Vocabulary Camouflaged Object Segmentation via Fine-Grained Object Binding and Adaptive Hybrid Prompt](https://openaccess.thecvf.com/content/CVPR2026/html/Ren_Training-Free_Open-Vocabulary_Camouflaged_Object_Segmentation_via_Fine-Grained_Object_Binding_and_CVPR_2026_paper.html)

- 结构定位：1. Introduction；2. Related Works；3. Methods；4. Experiments；5. Conclusion。
- 方法论证：FOB/AHP 从伪装对象和背景混淆切入，联结语义探针与 SAM 提示。
- 图表组织：probe、SAM、hybrid prompt 的增量与框/点删除对照。
- 对本稿的采用/边界：不把训练免训练边界与 CLIP→SAM 的额外前置条件省略。
- 本地原文：[PDF](../_work/cvpr50/C37.pdf)；[文本](../_work/cvpr50/C37.txt)。

### C38 · CVPR 2026 · [SkySense-VITA: Towards Universal In-context Segmentation of Multi-modal Remote Sensing Imagery](https://openaccess.thecvf.com/content/CVPR2026/html/Wu_SkySense-VITA_Towards_Universal_In-context_Segmentation_of_Multi-modal_Remote_Sensing_Imagery_CVPR_2026_paper.html)

- 结构定位：1. Introduction；2. Related Work；3. SkySense-VITA；4. Experiments；5. Conclusion。
- 方法论证：SkySense-VITA 将 prompt fusion 与 target decoding 两个流程分开。
- 图表组织：visual/text/fused 三种输入表与 naive fusion 对照暴露负干扰。
- 对本稿的采用/边界：组合好于较弱端点不够，还需对更好端点及单组件解释。
- 本地原文：[PDF](../_work/cvpr50/C38.pdf)；[文本](../_work/cvpr50/C38.txt)。

### C39 · CVPR 2026 · [HySeg: Learning Generative Priors for Structure-Aware Remote Sensing Segmentation](https://openaccess.thecvf.com/content/CVPR2026/html/Qiu_HySeg_Learning_Generative_Priors_for_Structure-Aware_Remote_Sensing_Segmentation_CVPR_2026_paper.html)

- 结构定位：1. Introduction；2. Related Work；3. Method；4. Experiments；5. Conclusions。
- 方法论证：HySeg 明确生成结构先验，再投影为 affinity 引导分割。
- 图表组织：除 region IoU，还用 clDice/Betti error 对齐拓扑主张。
- 对本稿的采用/边界：我们没有这些结构指标，不能把 IoU 上涨直接写成连通性证明。
- 本地原文：[PDF](../_work/cvpr50/C39.pdf)；[文本](../_work/cvpr50/C39.txt)。

### C40 · CVPR 2026 · [Open-Vocabulary Domain Generalization in Urban-Scene Segmentation](https://openaccess.thecvf.com/content/CVPR2026/html/Zhao_Open-Vocabulary_Domain_Generalization_in_Urban-Scene_Segmentation_CVPR_2026_paper.html)

- 结构定位：1. Introduction；2. Related Work；3. Methodology；4. Experiments；30. With ViT-L/14, S 2-Corr attains 55.8% on Dv-19, im-；5. Conclusion。
- 方法论证：S2-Corr 先分析 OVSS 在新域的失败，再建立 SSM baseline 和改进。
- 图表组织：训练域与测试词表大小分开，模块表在两个骨干复现。
- 对本稿的采用/边界：自然域实验是边界检查，不声称跨域配置直接迁移。
- 本地原文：[PDF](../_work/cvpr50/C40.pdf)；[文本](../_work/cvpr50/C40.txt)。

### C41 · CVPR 2026 · [The Power of Prior: Training-Free Open-Vocabulary Semantic Segmentation with LLaVA](https://openaccess.thecvf.com/content/CVPR2026/html/Zhang_The_Power_of_Prior_Training-Free_Open-Vocabulary_Semantic_Segmentation_with_LLaVA_CVPR_2026_paper.html)

- 结构定位：1. Introduction；2. Related Work；3. Methodology；4. Experiments；5. Conclusion。
- 方法论证：FSeg-LLaVA 按问答、text-visual response、mask generation 三步展开。
- 图表组织：不同问句和选层、mask 组合均有直接消融。
- 对本稿的采用/边界：prompt 表达本身是有效变量，具体描述应可回查。
- 本地原文：[PDF](../_work/cvpr50/C41.pdf)；[文本](../_work/cvpr50/C41.txt)。

### C42 · CVPR 2026 · [SPAR: Single-Pass Any-Resolution ViT for Open-vocabulary Segmentation](https://openaccess.thecvf.com/content/CVPR2026/html/Kombol_SPAR_Single-Pass_Any-Resolution_ViT_for_Open-vocabulary_Segmentation_CVPR_2026_paper.html)

- 结构定位：1. Introduction；2. Related Work；3. Method；4. Experiments；5. Conclusion。
- 方法论证：SPAR 先解释固定输入分辨率，再给任意分辨率蒸馏。
- 图表组织：single-pass 与 sliding-window 对照及不同任务验证表征收益。
- 对本稿的采用/边界：固定模型输入下分辨率/覆盖范围的取舍是事实基础，非生物学装饰。
- 本地原文：[PDF](../_work/cvpr50/C42.pdf)；[文本](../_work/cvpr50/C42.txt)。

### C43 · CVPR 2026 · [Looking Beyond the Window: Global-Local Aligned CLIP for Training-free Open-Vocabulary Semantic Segmentation](https://openaccess.thecvf.com/content/CVPR2026/html/Lee_Looking_Beyond_the_Window_Global-Local_Aligned_CLIP_for_Training-free_Open-Vocabulary_CVPR_2026_paper.html)

- 结构定位：1. Introduction；2. Related Work；3. Method；4. Experiment；5. Further Analysis；6. Conclusion & Limitation。
- 方法论证：GLA-CLIP 的 global K/V 扩展产生 locality bias，继续用 proxy 修正。
- 图表组织：跨窗口 Boundary Error Rate 与注意力稳定性对应主问题；配置声明明确。
- 对本稿的采用/边界：承认 global/local 已有先例，我们的新焦点是其与角色文本的条件互补。
- 本地原文：[PDF](../_work/cvpr50/C43.pdf)；[文本](../_work/cvpr50/C43.txt)。

### C44 · CVPR 2026 · [Test-Time Multi-Prompt Adaptation for Open-Vocabulary Remote Sensing Image Segmentation](https://openaccess.thecvf.com/content/CVPR2026/html/Yang_Test-Time_Multi-Prompt_Adaptation_for_Open-Vocabulary_Remote_Sensing_Image_Segmentation_CVPR_2026_paper.html)

- 结构定位：1. Introduction；2. Related Work；3. Method；4. Experiment；5. Conclusion。
- 方法论证：TMPA 先文本歧义，再数据集描述生成，最后低熵视觉均值引导在线 bias。
- 图表组织：dataset description、VGTA 和骨干通用性分别测试。
- 对本稿的采用/边界：借其任务适配思想，不把 CLIP embedding 的线性混合硬套到 SAM3。
- 本地原文：[PDF](../_work/cvpr50/C44.pdf)；[文本](../_work/cvpr50/C44.txt)。

### C45 · CVPR 2026 · [S2C2Seg: Semantic-Spatial Consistency and Category Optimization for Open-Vocabulary Segmentation](https://openaccess.thecvf.com/content/CVPR2026/html/Qing_S2C2Seg_Semantic-Spatial_Consistency_and_Category_Optimization_for_Open-Vocabulary_Segmentation_CVPR_2026_paper.html)

- 结构定位：1. Introduction；2. Related Work；3. Method；4. Experiments；5. Conclusion。
- 方法论证：S2C2Seg 将类别子集筛选与全局语义/局部空间组合分开。
- 图表组织：比较加、乘、学习权重等融合，并按有无背景分组。
- 对本稿的采用/边界：不能笼统声称“首次全局局部+文本”；我们的职责对象与接口须具体。
- 本地原文：[PDF](../_work/cvpr50/C45.pdf)；[文本](../_work/cvpr50/C45.txt)。

### C46 · CVPR 2026 · [PEARL: Geometry Aligns Semantics for Training-Free Open-Vocabulary Semantic Segmentation](https://openaccess.thecvf.com/content/CVPR2026/html/Pei_PEARL_Geometry_Aligns_Semantics_for_Training-Free_Open-Vocabulary_Semantic_Segmentation_CVPR_2026_paper.html)

- 结构定位：1. Introduction；2. Related Work；3. Method；4. Experiments；5. Conclusion。
- 方法论证：PEARL 将 attention 几何对齐和文本感知传播串成 align-then-propagate。
- 图表组织：PA/TLP 四格与替代策略验证各自功能。
- 对本稿的采用/边界：优先用短操作链和配对消融，不堆无关失败模块。
- 本地原文：[PDF](../_work/cvpr50/C46.pdf)；[文本](../_work/cvpr50/C46.txt)。

### C47 · CVPR 2026 · [Discriminative Perception via Anchored Description for Reasoning Segmentation](https://openaccess.thecvf.com/content/CVPR2026/html/Yang_Discriminative_Perception_via_Anchored_Description_for_Reasoning_Segmentation_CVPR_2026_paper.html)

- 结构定位：1. Introduction；2. Related Work；3. Methodology；4. Experiments；5. Conclusion。
- 方法论证：DPAD 对准推理游离目标的问题，把 grounded description 放入奖励。
- 图表组织：二值/差值/缩放奖励替代对照，而非只报完整框架。
- 对本稿的采用/边界：我们的描述不含这个 RL 工作流，不能仅因 anchor 一词就混引。
- 本地原文：[PDF](../_work/cvpr50/C47.pdf)；[文本](../_work/cvpr50/C47.txt)。

### C48 · CVPR 2026 · [Selective, Regularized, and Calibrated: Harnessing Vision Foundation Models for Cross-Domain Few-Shot Semantic Segmentation](https://openaccess.thecvf.com/content/CVPR2026/html/Ma_Selective_Regularized_and_Calibrated_Harnessing_Vision_Foundation_Models_for_Cross-Domain_CVPR_2026_paper.html)

- 结构定位：1. Introduction；2. RELA TED WORK；3. Method；4. Experiments；5. Conclusion。
- 方法论证：HERA 以层间可迁移性差异引出 select–regularize–calibrate。
- 图表组织：层规则、support-only 与最终三组件效应各有表。
- 对本稿的采用/边界：离线可解码信息不等于任意插入点有效；不要重开已停的层选择实验。
- 本地原文：[PDF](../_work/cvpr50/C48.pdf)；[文本](../_work/cvpr50/C48.txt)。

### C49 · CVPR 2026 · [F2Net: A Frequency-Fused Network for Ultra-High Resolution Remote Sensing Segmentation](https://openaccess.thecvf.com/content/CVPR2026/html/Chen_F2Net_A_Frequency-Fused_Network_for_Ultra-High_Resolution_Remote_Sensing_Segmentation_CVPR_2026_paper.html)

- 结构定位：1. Introduction；2. Related Work；3. Methodology；4. Experiment；5. Conclusion。
- 方法论证：F2Net 把 UHR 的细节/上下文矛盾对应到频率分支及组合。
- 图表组织：三分支单独、两两、完整组合表，比只写模块累加更有说服力。
- 对本稿的采用/边界：借用匹配组合表，不声称我们进行了频率分解。
- 本地原文：[PDF](../_work/cvpr50/C49.pdf)；[文本](../_work/cvpr50/C49.txt)。

### C50 · CVPR 2026 · [Vocabulary Scaling Law: Tuning Open-vocabulary Predictors for Their Openness](https://openaccess.thecvf.com/content/CVPR2026/html/Chen_Vocabulary_Scaling_Law_Tuning_Open-vocabulary_Predictors_for_Their_Openness_CVPR_2026_paper.html)

- 结构定位：1. Introduction；2. Related Work；3. Background: the Openness of CLIP；4. Vocabulary Scaling Law behind CLIP；5. Submodular-Vocabulary Fine-tuning；6. Experiments；7. Limitation and Future Work。
- 方法论证：Vocabulary Scaling Law 将 openness 定义为稳定性与扩展性后推导条件。
- 图表组织：同时报告闭集准确率、扩展、干扰类稳定性，直接检验所称能力。
- 对本稿的采用/边界：当前固定测试词表结果不足以声称未知任意词表的稳健性。
- 本地原文：[PDF](../_work/cvpr50/C50.pdf)；[文本](../_work/cvpr50/C50.txt)。

