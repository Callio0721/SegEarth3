# 20 篇 CVPR 2025–2026：章节、论证与图表阅读

2026-09-03。选择 13 篇 CVPR 2025、7 篇 CVPR 2026 **正会**论文，均通过 CVF 正式页面核对题名、作者、会议及 PDF。不是把 Findings、arXiv 预印本或不同任务混称为同一类 SOTA。

阅读方式：对 20 篇进行章节、主文、图表标题及版面结构通读，对最相关的 SegEarth-OV、TMPA、ReAttnCLIP、Hybrid Global–Local 等方法精读。每篇选取一页主要方法/图表页作视觉对照；下文页码指本地 PDF 物理页。C01 使用本地 arXiv 版，分页不必与 CVF 合订页相同。正文与参考文献/补充页分开观察。

[完整来源、作者和下载位置](引用与论点对照.md)；原 20 篇机器可读元数据见 `cvpr20_sources.json`，统一 BibTeX 见 `论文引用.bib`。本轮针对性复核五篇直接写法参照，并在 §6 新增两篇 CVPR 2026 正会及一篇 Findings；不把原 20 篇都改称直接 OVSS 对手。

## 1. 先看总体规律：不是固定目录，而是固定论证任务

20 篇中反复出现的顺序是 **Introduction → Related Work → Method/Approach → Experiments → Conclusion**。Preliminaries 有的单列，有的并入 Method；Limitation 有的在实验末尾，有的单列。创新重心不同，章节分配明显不同：

- 结构改进型：先展示一个具体失败，再提出对应模块，如 Mask-Adapter、ReAttnCLIP、CASS。
- 表征/理论型：先定义可分析量，再用量导出操作，如 HyperCLIP、Direct Segmentation、M²N²。
- 数据/基础模型型：单列数据构建及多任务设置，如 SkySense-O、Scaling up Image Segmentation。
- 解释/benchmark 型：方法定义之后优先验证解释量的有效性，再研究模型问题，如 CCI。

我们的重心是第一类，辅以一个简洁分析，而不是第二类的完整理论论文或第三类的新基础模型论文。

## 2. 逐篇记录

### C01 · SegEarth-OV（CVPR 2025）

**范围：** 免训练遥感 OVSS，直接写法参照。

**章节：** §1 引言；§2 相关工作；§3 预备知识；§4 方法（约 p4–5）；§5 实验（p5–8）；结论。先定位 CLIP 稠密特征的分辨率与全局偏置问题，再解释 SimFeatUp 和全局偏置处理。

**图：** 前部用失败/特征图建立动机，方法处给模块总图，再以重建和分割可视化展示模块影响。白底、模块浅色、局部放大与同色标签让“哪里变了”容易比较。

**表：** 多类别与二分类主表分开；模块、上采样设置、即插即用性和自然域扩展分别回答不同问题。不是把主表重复缩小当消融。

**借鉴：** 我们也应先用文本作用差异提出问题，再引出模块；八遥感主表与自然域小表分开。不要照搬其 CLIP 特征问题来解释 SAM3。

### C02 · Test-Time Multi-Prompt Adaptation / TMPA（CVPR 2026）

**范围：** 遥感 OVSS 的测试时提示适应，直接相关。

**章节：** §2 相关工作；§3 方法（p4–6），从多提示构造到视觉引导文本适应；§4 实验（p6–8）先设置/SOTA，再消融。

**图：** 提示约束例子在 p4 附近，用真实文字而非“LLM box”解释新增信息；熵分析图连接低熵像素选择与视觉证据。结构图把离线描述与在线处理区分。

**表：** 八数据集、二分类分别比较；组件表、提示数量表、集成到其他方法的表各验证一项设计。

**借鉴：** 我们文本模块必须展示真实 anchor/补充例子。提示筛选、三头用途和视觉输入是不同问题，不能只写“LLM 生成 prompt 后效果提高”。

### C03 · ReAttnCLIP（CVPR 2026）

**范围：** 免训练遥感 OVSS。

**章节：** §2 按 VLM/自然 OVSS/遥感 OVSS 组织相关工作；§3 预备知识；§4 方法（p3–6）从 patch 输出分解走向 patch–patch 相似性、CLS 重建与抑制；§5 实验（p6–8）。

**图：** 架构和注意力对照在 p4，后接相似性/熵诊断；最终分割图不替代内部现象图。模块配色与分析量保持一致。

**表：** 主表先建立竞争力；组件、关系构造、层位、插件及自然域表分别验证因果环节。

**借鉴：** Method 中每个操作都应对应一个明确观察和消融。我们应解释角色残差与视图证据的进入位置，不借“attention”一词制造并不存在的内部改动。

### C04 · SkySense-O（CVPR 2025）

**范围：** 有训练的遥感视觉语言基础模型，学习论文组织，不作免训练对手。

**章节：** §2 相关工作；§3 SkySA 数据；§4 模型与预训练（p4–5）；§5 多任务实验（p6–8）。区域/像素采样与 vision-centric graph 服务整体模型目标。

**图：** p1 任务能力图，p2 发展定位，p3 数据统计，p4 总架构，之后展开采样/图结构；图的层次由“系统是什么”到“关键模块怎么做”。

**表：** 数据属性表、分割/VQA/分类结果分开，组件消融最后连接统一设计。

**借鉴：** 不应让我们的小型方法承载同样多任务叙事；可学习其总览图与模块图的详略层级。

### C05 · AVION（CVPR 2026）

**范围：** 有训练的遥感分类/检索提示蒸馏。

**章节：** §2 VLM、参数高效适应和遥感；§3 原理与 Text Prototype Enhancement/Tri-Aspect Alignment（p3–4）；§4 few-shot、base-to-novel、检索与消融（p5–8）。

**图：** 域差异散点在前；主图后紧接 LLM 提示及视觉原型筛选示意。教师到学生的箭头清楚区别生成、筛选与监督。

**表：** 多任务泛化表之外，B0–B7 设置与结果、P0–P6 原型策略分层拆解，避免“全模块加上去”一行消融。

**借鉴：** 解释文本如何形成以及被什么信息约束。不能把其蒸馏效果当作无需训练即可修正 SAM3 文本的依据。

### C06 · HyperCLIP（CVPR 2025）

**完整题名：** Understanding Fine-tuning CLIP for Open-vocabulary Semantic Segmentation in Hyperbolic Space。

**章节：** §2 OVSS/双曲表示；§3 几何预备；§4 方法（p4–5）；§5 实验（p5–8）。由 Poincaré 表示的半径现象引出调整及相关推导，再检验作用。

**图：** p1–2 几何直觉和类别半径统计，p4 架构，p8 半径干预。不是用漂亮的空间图代替真实表征统计。

**表：** 主分割及任务扩展、模块尺寸、编码器适应、几何操作的对照，围绕同一个表示问题。

**借鉴：** 理论量必须与操作、实验相连。我们使用可观察采样与类别边际即可，不引入未用于实现的新空间或“定理包装”。

### C07 · S-Seg（CVPR 2025）

**完整题名：** Exploring Simple Open-Vocabulary Semantic Segmentation。使用图文数据训练。

**章节：** §2 相关工作；§3 方法（p3–6）：MaskFormer 基础、DINO 聚类伪 mask、语言对比及可选自训练；§4 实验（p6–8）。

**图：** p3 架构配伪代码，p4 推理与伪 mask 示例，p6–8 定性和数据/自训练分析。简洁框图说明“简单方案为什么已经足够”。

**表：** 主结果区分含/不含背景；单独对照简单 mask+CLIP 方案及伪 mask 质量。

**借鉴：** 我们最需要的是“相同文本为何按角色使用优于统一使用”的简单对照，而不是再添加模块使图更复杂。

### C08 · Mask-Adapter（CVPR 2025）

**范围：** 学习 mask 语义读出的 OVSS 适配器。

**章节：** §2 两类 OVSS/VLM 适应；§3 方法（p3–5）从 mask 读出问题到激活图、匹配及一致性训练；§4 实验（p5–8）。

**图：** p1 用 GT mask 的分类结果定位瓶颈；p2 对比 crop/pool/adapter；p4 总图；p8 激活图解释读出区域。

**表：** 按 backbone 分组的主表，mask 读取、训练方式、matcher、组件设计及 SAM 接入分别比较。

**借鉴：** 先定位“mask 已有但语义读出不足”再设计方法的逻辑可借鉴；我们的历史 oracle 也只能定位上限，必须接真实可执行增益。该 adapter 本身有训练。

### C09 · Dual Semantic Guidance for Open Vocabulary Semantic Segmentation（CVPR 2025）

**范围：** 图像级监督的 OVSS，非免训练。

**章节：** §2 VFM/OVSS；§3 方法（p3–5）分为语义引导生成 DSGG 与语义引导分割 DSGS；§4 实验（p5–8）。视觉区域线索与文本名词共同形成指导，再进入分割及背景筛除。

**图：** p2 两类失败与应对；p3–4 两个模块各有图，聚类和背景现象紧邻；后部定性对照。

**表：** 主表区分背景协议，之后分别消融指导生成、注意力、两种语义信息和替代操作。

**借鉴：** 两项贡献应解决相接的问题，有完整组合及替代设计对照；不能只展示“有两个模块”。

### C10 · Scaling up Image Segmentation across Data and Tasks（CVPR 2025）

**范围：** 有训练的统一图像分割。CVF 摘要/本地 PDF 的模型称呼存在 QueryMeldNet/MQ-Former 版本差异，此处以正式论文题名标识。

**章节：** §2 相关工作；§3（p3–5）混合 learned/conditional queries、跨任务数据和合成 mask–caption；§4（p6–8）先 query 设计及规模，再跨任务主表。

**图：** p3 总图，p4 query 对比，p5 数据构造，p6 thing/stuff 示例，p7 规模曲线。

**表：** 能力比较表与多尺度 query 设计表连接统一框架；open/closed vocabulary 结果按任务分别列。

**借鉴：** 用任务职责解释不同信息形式，但不把 Instance 固定等同 things、Semantic 固定等同 stuff。我们的角色具有计算定义，不能由类别名称直接替代。

### C11 · The Power of Prior（CVPR 2026）

**完整题名：** The Power of Prior: Training-Free Open-Vocabulary Semantic Segmentation with LLaVA。

**章节：** §2 OVSS/MLLM；§3（p3–5）Question–Answer Prior、Text–Visual Response、Visual–Geometric Matching；§4（p6–8）设置、主表及消融。

**实际链路：** LLaVA 问答得到类别/描述→读取视觉文本响应与注意力→形成区域、视觉匹配和点/框→SAM 掩膜。

**图表：** p1 层位定位现象，p4 三阶段图，p5 中间结果；主表之后分别比较文本、层位、点框与区域策略，检验每一阶段。

**借鉴：** 生成文本并非完整方法，关键是如何让文字成为空间证据。旧索引的泛称“投影语言先验”已改为实际三阶段流程。

### C12 · Direct Segmentation（CVPR 2026）

**完整题名：** Direct Segmentation without Logits Optimization for Training-Free Open-Vocabulary Semantic Segmentation。

**章节：** §2 OVSS/CLIP 适应；§3（p3–5）问题形式、分布重写、最优路径与最大速度；§4（p5–8）设置、主表和消融。

**实际链路：** 相似度 logits 经过抑制/归一化，按与退化目标分布的解析差异构建分割映射，上采样后决策。

**图表：** p1 范式对比，p3 总图，p4 分布解释，p7 各阶段输出；p6 主表，p8 组件与策略替代及敏感性。

**借鉴：** 若提出数学解释，要明确解释哪个实际运算。此文不是 DLAE；后者是分类任务的 Dynamic Logits Adjustment and Exploration。

### C13 · Concept Regions Matter / CCI（CVPR 2026）

**范围：** CLIP 解释与鲁棒性 benchmark，不是 OVSS 方法。

**章节：** §2 解释/鲁棒性；§3 Cluster-Importance 方法及评价；§4 COVAR 构造；§5 实验讨论；§6 总结。以聚类区域干预引起的预测变化定义贡献。

**图表：** p2 失败类型，p3 区域聚类，p4 删除曲线，p5 解释忠实度表，p6–8 背景/结构变化与错误分类。定量结果先验证解释器，再用其解释模型。

**借鉴：** 总准确率上升不能直接证明某一种语义或背景机制。我们应将类别增益图作为现象，再配对应区域的真实 correction，而非把热图当因果证明。

### C14 · ResCLIP（CVPR 2025）

**范围：** 免训练 OVSS。

**章节：** §2 VLM/OVSS；§3（p3–5）预备、Residual Cross-correlation Self-attention（RCS）与 Semantic Feedback Refinement（SFR）；§4（p6–8）设置、主表及分析。

**图表：** p1 层间注意力现象，p2 操作与收益概览，p4 关系对照，p5 总图，p8 定性；主表区分含背景/不含背景，Table 3 是完整二模块 2×2，另有层位和强度对照。

**借鉴：** 2×2 模块表比“baseline/完整方法”更能揭示组合；我们的四路表进一步报告交互，不把 Joint−Role 当严格协同。

### C15 · Hybrid Global–Local（CVPR 2025）

**完整题名：** Hybrid Global-Local Representation with Augmented Spatial Guidance for Zero-Shot Referring Image Segmentation。免训练 referring，而非遥感 OVSS。

**章节：** §2 RIS；§3（p3–4）混合表征和空间指导；§4（p5–8）主比较、表征/指导消融。

**实际链路：** local 使用 masked image；global 模糊背景并使用目标相关 attention mask，将全局空间特征融合到局部分支；语言评分再结合关系、连贯性和位置。

**图表：** p1 三种失败，p3 双分支与空间指导总图，p7 定性；RefCOCO/PhraseCut 主表后，分别比较 local/global、weighted/L2G/G2L、开始层和空间线索。

**借鉴：** 是文本条件定位中局部与上下文互补的直接先例；其 global 不是我们的大范围缩放，不能用同名掩盖实现差别。

### C16 · CASS（CVPR 2025）

**完整题名：** Distilling Spectral Graph for Object-Context Aware Open-Vocabulary Semantic Segmentation。免训练 CLIP/DINO 组合。

**章节：** §2 相关工作；§3（p3–5）谱图对象上下文蒸馏与 presence-prior 文本调整；§4（p6–8）主比较及消融。

**图表：** p1 对象部分/语义问题；p3 蒸馏框图；p4 原始/蒸馏/低秩关系对照；p5 多 head 与文本先验；p7 定性。主 mIoU 表与 pAcc 表分开，p8 组件、外部 backbone、距离等对照。

**借鉴：** 用对象一致性和上下文解释所需信息，比笼统“多一份特征”更具体。但它的内部 attention 蒸馏不能充当我们 late view fusion 的实现证据。

### C17 · VidSeg（CVPR 2025）

**范围：** 利用扩散表示的视频分割；不是本文类别文本 OVSS 的直接排名对象。

**章节：** §2 扩散表示/视频；§3 SD 等预备；§4（p3–5）场景上下文、时间对应、masked modulation；§5（p6–8）实验；§6 局限；§7 结论。

**图表：** p1 时间连续性问题，p2 不同特征的时空切片，p4 总图、p5 模块图；主表同时看分割和时间一致性，组件表与 feature/modulation 图相接，定性含失败。

**借鉴：** 新增观察应带来可指明的信息，而非重复原表示；机制指标服务问题，但主性能指标始终明确。

### C18 · M²N²（CVPR 2025）

**完整题名：** Repurposing Stable Diffusion Attention for Training-Free Unsupervised Interactive Segmentation。交互分割，主指标为 NoC 等，不是 OVSS mIoU。

**章节：** §2 监督/无监督；§3（p3–5）截断邻域、attention 聚合、Markov map、缩放邻域；§4（p5–8）设置、消融、定性与局限。

**图表：** p1 概览，p3 attention→Markov map→分割；p5 block 与阈值函数表，p6 主 NoC 表，p7 中间图，p8 参数和难例。

**借鉴：** 数学模型解释的是算法行为，效果仍需实际结果。我们的边际分析应同样克制地解释协同可能性，而非宣称性能保证。

### C19 · Open-Vocabulary Domain Generalization in Urban-Scene Segmentation（CVPR 2026）

**范围：** 有训练的城市 OV 域泛化，方法 S²-Corr。

**章节：** §2 DGSS/OVSS；§3（p3–5）任务定义、CAT-Seg 相关性问题、选择性状态空间与相关性调整；§4（p5–8）跨域协议、主结果、消融。

**图表：** p1 对照 DG/OV/联合任务，p2 训练域表，p4 架构与域差异，p5 扫描方式；p6–7 real-to-real/synthetic-to-real 分表，p7 组件，p8 相关性与分割图。

**借鉴：** 自然图像扩展要先说明任务关系，不把“另一自然数据集有效”写成严格域泛化；我们的主体仍是遥感免训练。

### C20 · ExCEL（CVPR 2025）

**完整题名：** Exploring CLIP’s Dense Knowledge for Weakly Supervised Semantic Segmentation。完整方法是 WSSS；静态 CAM 分支与训练后分割结果不同。

**章节：** §2 WSSS/VLP；§3（p3–5）文本语义扩展、静态/可学习视觉相关性、损失；§4（p5–8）主表、消融及分析。

**图表：** p1 global/patch 对齐矛盾，p3 总图分文本/静态/学习/监督四块；p6 定性，p7 CAM 组件，p8 属性与注意力。CAM 表与最终分割表分开，组件表含 precision/recall/IoU。

**借鉴：** 中间响应改善与最终分割改善必须区分。我们不能用 semantic 激活增强直接代替最终正确像素和 IoU 增益。

## 3. 为什么这些论文这样安排章节

### Introduction：先制造必要性，再宣布方法

常见的有效四段是：任务价值与进展→具体未解决矛盾→观察与方法→贡献。Fig.1 通常不是总流程复制品，而是动机/对比/一眼可懂结果：Mask-Adapter 的 GT-mask 分类、HyperCLIP 的几何、CASS 的对象一致性都如此。

我们 Fig.1 适合展示：同一 anchor→一条补充并不均匀改善三种用途→角色补充和互补观察如何共同修复区域。真实分割例子未导出前，不制作貌似真实的 prediction。

### Related Work：按技术分界，而非“某作者提出某方法”

每段先定义一条路线，再用两三项工作说明实际操作，最后接我们的差异。正文引用应集中在任务直接相关者，20 篇写作样本不必全部塞入 Related Work。

### Method：先统一符号，再展开两个模块

公式先定义实际接口，图在接口之间画信息流。模块名应对应真实计算；冻结/学习状态用图例，数据预处理与网络运算用不同形状或线型。用具体文本与小型空间示例代替巨大装饰性 token 堆叠。

对我们：概览先于残差；残差先于视图；视图后面给条件协同解释。不能把每个历史超参数单列一节。

### Experiments：一张表回答一个问题

| 问题 | 常见图表形式 | 我们的对应 |
|---|---|---|
| 是否有竞争力 | 跨方法/跨数据集主表 | PPT p16 多模型表 |
| 哪个模块有效 | 开关组合、匹配组件表 | Baseline/Role/View/Joint |
| 设计为什么如此 | 替代操作小表 | Residual vs Direct；最终文本角色分配 |
| 是否只对特殊任务有效 | 独立的扩展表 | Cityscapes/VOC20 |
| 到底改好了什么 | 同图同色预测、区域放大 | 四路真实 mask；类别组增益柱状图 |
| 什么时候不起作用 | 失败例或机制分组 | 道路/铺装混淆、收益重合等 |

表的列不要一次包含 mIoU、所有中间量和所有超参数。主表强调比较范围，消融强调控制变量，图表相互分工。

## 4. 图表视觉标准与我们应如何用

本轮方法页对照中有效的共同点：白底、少量浅色模块、黑/深色箭头；同一信息类型跨图颜色稳定；总览与放大块分层；原图、GT、预测同坐标同颜色；数值表多采用稀疏横线与少量加粗。

**我们的建议位置：**

- p1 Fig.1 问题与方法概念，不塞所有流程。
- p3 Fig.2 跨栏主架构，真实 anchor/补充文本、完整 grounding、每视图角色组合、对齐融合。
- p5 Table 1 跨栏多模型主表。
- p6 模块表与替换小表；邻近正文解释操作必要性。
- p7 匹配交互表与类别柱状图；两者分别讲协同和收益类别。
- p8 四路定性图、自然域小表与简短结论；若拥挤，完整四路/自然域表放补充，不缩到难以辨认。

柱状图只画 Role Text 与 Role Text + View 相对 baseline 的增益。数字两位小数、轴与图例保持可读，不在同一图混合类别分布、散点回归与背景放大。

## 5. 两轮自评：从实验汇报转为论文结构

| 轮次 | 审阅发现 | 修订 |
|---|---|---|
| V1：由实验记录归纳 | 结果丰富，但主线随实验切换；理论偏类比，图包含太多统计 | 聚焦“功能语言—可观察证据”，区分模块进展与匹配交互 |
| V2：对照 20 篇结构 | 缺多模型主表、Related Work 机制不够具体、理论与实现层级容易混淆 | p16 主表 + 真实消融；三条相关路线；几何/边际解释；保留 late fusion 事实 |
| 当前可进入写作 | 方法主线、数据表、理论来源已有，真实四路图与最终文本分配对照最有补充价值 | 先形成 Method/Experiments 初稿，再据这两项证据完善；不重启方法搜索 |

这不是声称“完全照着 CVPR 写就能录用”。本轮真正获得的是可核查的章节任务、论证颗粒度和图表分工，使现有工作能以论文而非实验流水账的形式表达。

## 6. 本轮针对性复核与新增（2026-09-03）

本轮回到 SegEarth-OV、TMPA、ReAttnCLIP、ResCLIP、Mask-Adapter 原文，复核引言/章节/图表用途；已有结构判断基本成立，不重复重写。修正 ResCLIP 模块全称。新增三篇读其主文与方法，GLA-CLIP p3、OV-Stitcher p5 同时作了版面视觉核对。

### R08 · GLA-CLIP / Looking Beyond the Window（CVPR 2026 正会）

**为什么重要：** 直接研究免训练 OVSS 的独立窗口语义不一致，比仅用 SlowFast 类比更贴近我们的视觉观察问题。

**论证顺序：** p1 Fig.1 先定义窗口边界不一致现象及 Boundary Error Rate → §3.2 扩展跨窗口 K/V → §3.3 说明直接扩展仍有 window bias，引入 proxy anchor → §3.4 动态归一化 → §4 主比较 → §5 进一步分析 → §6 结论/局限。不是一次宣布三个无关模块，而是每个操作回应前一步剩下的具体问题。

**图表作用：** p3 Fig.2 用主流程和两个细节框区分三个操作；p5 Fig.3 对照干预前后的 attention；Table 2 通过结构替代比较模块；§5.3 检查高相似 token 数能否对应其使用的尺度代理，连接设计量与真实任务。主表将不同推理设置分组，不把所有数字混在一个默认设置下。

**对我们：** 强化“观察包含何种证据”的动机，并把角色补充与视图的作用写成相接问题。但 GLA-CLIP 是 VFM/CLIP 跨窗口 feature attention，不是我们两种完整 SAM3 observation 的输出融合；其 BER 发现不能直接称为我们已经测得的 SAM3 缺陷。

### R09 · PEARL（CVPR 2026 正会）

**论证顺序：** 引言提出“形成 attention 的几何”和“语义在空间传播”的两处问题 → §3.1 定义基座接口 → §3.2 Procrustes 对齐 → §3.3 文本引导 Laplacian 传播 → §4 主比较/两模块消融/扩展 → §5 结论。方法使用 **align-then-propagate** 组织两个操作，而不是仅取两个模块名称并列。

**图表作用：** p4 Fig.2 总链路清楚标出 PA 在最后 attention block、TLP 在 logits 上；p7 Table 3 保留四种模块开关，Table 4 检查传播模块接到其他基座后的作用。写法把“输出从哪里来”和“接下来如何处理”讲清楚。

**对我们：** 可借鉴职责动词组织：role supplementation → grounded observations → evidence composition。两模块都有效、完整方法最好，不自动意味着数值上的超加性；我们的交互结论继续使用匹配四路 Γ，不从别人的“synergy”措辞照搬。PEARL 不提供 SAM3 的三头适配结论。

### R10 · OV-Stitcher（CVPR 2026 Findings，单列）

**论证顺序：** §3.2 分析独立子图的表示断裂 → §3.3 在末层 attention 前拼接窗口 Q/K/V → §3.4 指出区域一致性增强也可能扩大错误类别，补充 class-biased prompts → §4 实验。它已经将全局上下文与新文本组合，必须纳入邻近工作，而不能继续声称二者结合本身是空白。

**图表作用：** p4 Fig.3 用表示和预测并排定位问题；p5 Fig.4 说明 feature stitching 与文本支路位置；p8 Table 2 四路开关和无后处理对照区分模块效果与额外处理。其双模块转折来自第一个操作留下的语义问题，叙事连贯。

**对我们：** 当前区别应明确为 SAM3 的 P/S/I 角色功能补充、anchor 保护、完整 grounding 与对齐视图证据组合。不能仅写“文本更丰富、上下文更大”，也不因此回头改成已经失败的内部 Replay。

### 复核后的取舍

- **保留：** 三条 Related Work、基座→角色补充→视图组合的 Method 顺序、真实主表与模块/替换/四路交互表。
- **只改：** 补齐同任务上下文文献；把宽泛创新落到角色职责；边际推导移入补充材料候选；将单图观察对照加入现有待办。
- **不增加：** 新的 feature fusion 模块、代理量、海量参数实验或新的主表数值。新增文献用于定位和写作，不等于批准复现其算法。
