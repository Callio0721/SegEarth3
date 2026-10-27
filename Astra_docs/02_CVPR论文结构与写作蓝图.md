# CVPR 论文结构与写作蓝图

> 目标不是把 `state.md` 翻译成英文，而是从现有实验中提炼一个问题、两个相互连接的设计和一条可核查的证据链。

## 1. 一篇论文，而不是两套方法的拼接

建议保留工作名称 **Role–View Evidence Specialization**，先不花精力反复命名。核心叙事为：

> **A shared concept provides a category anchor, but useful supplementary evidence depends on both the readout responsibility and the visual observation.**

概念 anchor 保留“分什么”的共同基础；角色化补充表达“这个输出还需要什么信息”；互补视野提供“在什么观察条件下能读到这些信息”。两种补充都经过完整 SAM3 grounding，而不是另造一个与预训练模型脱节的判别器。

两个贡献应分别回答：

1. **What to supplement?** 按功能使用补充文本证据，而不是默认整条新描述适合替换所有角色。
2. **Under which observation?** 将补充文本的效果与视觉范围共同考虑，通过对齐视图证据获得条件互补。

第二个回答不是“每头分配一个专属视图”，因为当前代码未这样实现。它是相同角色配置在完整 Local / Global grounding 下产生的证据如何联合使用。

论文的第三条 contribution 可以是“跨八个遥感基准及自然域扩展的系统验证和机制分析”，**无需凭空添加第三个算法模块**。

## 2. 八页如何分配

按已公布的 [CVPR 2026 Author Guidelines](https://cvpr.thecvf.com/Conferences/2026/AuthorGuidelines)，正文最多八页，图表计入，参考文献可另页。以下是八页写作目标，不冒充尚未核实的下一届最终规则。

| 内容 | 预算，含所属图表 | 核心职责 |
|---|---:|---|
| Title + Abstract | 0.35 页 | 问题、方法、最重要的结果 |
| 1. Introduction | 1.15 页 | 为什么现有做法不够，为什么应研究角色与观察 |
| 2. Related Work | 0.65 页 | 确定相对最接近工作的新增位置 |
| 3. Method | 2.45 页 | 用一张主图和少量必要公式完整定义方法 |
| 4. Experiments | 3.20 页 | 主对比、模块归因、协同、作用范围与真实视觉结果 |
| 5. Conclusion / Limitations | 0.20 页 | 回扣问题、交代最重要边界 |
| **合计** | **8.00 页** | 不把参考文献算入上述预算 |

这是版面预算，不是要求每节机械占满。初稿排版时先固定图表位置，再调整段落长度，避免先写十几页再删到只剩结论。

建议页面节奏：第一页让读者理解问题；第二页完成相关工作并进入主图；第三至四页把方法讲完；第五至八页用结果回答最可能的审稿问题。不要把 SAM3 的教科书介绍铺成一整页。

## 3. Introduction：六个段落形成论证，不写研究日记

### 第 1 段：任务及其真正难点

开放词汇遥感分割需要把类别概念落实为密集地物区域。不同类别同时存在尺度、外观与空间组织差异，单纯图文整体相似度并不能直接解决定位与密集覆盖。先建立问题的重要性，引用 SegEarth-OV 等直接相关工作，不从遥感“应用广泛”开始长篇铺垫。

### 第 2 段：从图文对齐到概念 grounding 的机会

解释 SAM3/SegEarth-OV3 不再只把文本当分类原型：同一个概念条件会参与共享 grounding，并产生 existence、dense coverage、query masks 等不同输出。原生结构是本文的机会，不要先贬低 baseline。

### 第 3 段：第一处缺口及可观察事实

提示改写通常围绕“让类别描述更充分”。但在多职责输出模型中，一条描述的作用不仅取决于它说了什么，还取决于其输出被用于哪个角色。用一组同文本改变用途的对照建立动机：OEM 的 S3 只修正 Semantic 为46.28，同时修正三角色为44.02。

紧接着承认该作用不是固定规律：UDD5 同样的 S3 角色类型在共享用途下更好。由此引出的是**角色适配性需要辨别**，不是人为宣告“三头必须三种语言”。

### 第 4 段：为什么文本补充之后还需要观察补充

文本可以要求连续覆盖或区域组织，却不能恢复一次裁剪中根本看不到的结构，也不能增加缩放后消失的细节。Local / Global 提供不同视觉证据；补充描述只有在相应证据可见时才可能发挥作用。这是第二部分由第一部分自然引出的地方。

需要引用具有真实机制的上下文研究，而不是一句“人类也看全局和局部”：GLA-CLIP / OV-Stitcher 研究跨窗口上下文，HRDA 研究高分辨率局部与广域观察的联合处理。它们提供先例，不替我们证明 SAM3 中的效果。

### 第 5 段：方法总述

以官方概念为 anchor，每种补充文本完整 grounding，按角色作有界修正；两个观察分别完整计算并对齐融合；联合考虑文本配置与视图证据，保持原生 SAM3 耦合。不在这里解释全部超参数或枚举融合算子。

### 第 6 段：贡献及最有分量的结果

两条方法贡献加一条实证贡献即可。写八数据集平均57.49、相对同次 baseline +3.92、固定配置6/8正 interaction。避免在第一页同时堆 PA、AUC、oracle、若干模型缩写和所有失败方向。

### 英文开篇核心段示例

> Concept-grounded segmentation models expose several readouts under a shared textual condition, yet these readouts serve different purposes: assessing concept existence, covering dense regions, and organizing query-based masks. A richer description therefore need not be equally useful to every readout. We study how supplementary evidence should be allocated without disrupting the shared grounding that makes these outputs coherent. Our approach preserves the original category anchor, specializes supplementary textual evidence by readout responsibility, and combines aligned observations in which this evidence can be grounded differently.

这段可以作为初稿的逻辑骨架，不必照抄为最终英文。

## 4. Related Work：三条工作流，末句落到差异

### 2.1 Training-Free Open-Vocabulary Segmentation

**写什么：** CLIP 类方法如何把图文表征转换为密集预测，以及 SAM3 类方法如何利用 concept-conditioned masks。自然域与遥感域放在同一技术演进里，不分成两个重复名词清单。

代表：SegEarth-OV、ReAttnCLIP、SegEarth-OV3。每类说明一条实际流程与一个瓶颈。SegEarth-OV3 用原生 Semantic/Instance/Presence 融合，是直接 baseline，而非仅写“采用 SAM3”。

**与本文相接：** 本文不重新训练视觉语言表征，而研究冻结概念 grounding 的补充证据应怎样被不同 readout 使用。

### 2.2 Prompt and Concept Adaptation

**写什么：** TMPA 的 dataset-aware 描述与视觉引导测试时调整；ConceptBank 的 support 驱动候选概念功能评价；ProC-SAM3 的受约束扩展与 semantic-base 残差融合；CoCo-SAM3 的同义证据聚合及跨类校准。

不能把四篇混成“LLM 生成描述然后提升”。它们分别在生成约束、候选评价、输出融合、类别竞争处介入。ConceptBank 的 support GT 使用应明确；TMPA 的线性混合前提不能被当作 SAM3 潜空间已对齐的证据。

**与本文相接：** 现有这些具体机制没有等价实现本文的“完整 grounding 后按 P/S/I 角色使用补充，再与视图配置共同考虑”。但 CoCo-SAM3 已有不同信息来源分工，不能宣称首次想到“语义信息与结构信息不一样”。

### 2.3 Contextual Evidence for Dense Prediction

**写什么：** HRDA 的双分辨率观察；GLA-CLIP 的跨窗口 global K/V；OV-Stitcher 的 attention stitching 与类别偏置提示。必要时补直接遥感邻接上下文文献。

**与本文相接：** 本文不拼接或重写预训练内部 attention；不同观察各自完整 grounding，在对齐的类分数空间组合。新增主张不是“上下文有用”，而是观察的收益依赖 role-functional text，二者不能只看独立最优。

**篇幅纪律：** 三个小节合计约半页到四分之三页，每节一至两段；更详细的方法对照表放补充。本地阅读账本承担论文全文无法承载的细节。

## 5. Method：先定义真实对象，再给两个设计

推荐四个小节，避免把简单方法拆成八个模块。

### 3.1 Preliminaries and Overview

约0.35页。定义图像、类别、官方 anchor、多别名、三个角色输出及原生组合。主图第一次出现于本节附近。

用一个式子说明原生组合足够：

\[
\mathcal F(p,S,Q;a)=p\max\left(S,\max_{q:ar_q>\eta}M_qr_qp\right).
\]

图中把 Full Native Grounding 作为共享模块，不画三个互不关联的 SAM3。另用小 inset 标识 P/S/I 的职责，不复制整套 baseline 内部网络。

### 3.2 Role-Functional Textual Evidence

约0.85页。按以下顺序写：

1. 类别 anchor 不变，构造角色功能候选；正文举一类真实配置文本，完整候选表及生成约束放补充。
2. 每条候选都完整运行 grounding，获取其输出；只取指定职责证据。
3. 在概率/分数输出上进行有界修正，并保留 P→I 耦合。
4. 保留官方多别名输出；未启用补充时准确回到官方路径。

简记更新为：

\[
\mathcal R(a,b)=\operatorname{clip}_{[0,1]}
\left(a+\alpha\operatorname{clip}(b-a,-\tau,\tau)\right).
\]

使用 `p'=R(p_A,p_P)`、`S'=R(S_A,S_S)`；Instance 的 anchor/candidate maps 都先按当前 `p'` 和相应 admission 构造，再作 `R`。这一句不能删，否则公式会把已保留的原生耦合画没。

每个观察单元输出：

\[
G_v=\operatorname{clip}_{[0,1]}
\left(B_v^{official}+\mathcal F_v^{role}-\mathcal F_v^{anchor}\right).
\]

`Bofficial` 与 `Fanchor` 不强行视为相等，因为官方别名聚合和组合 anchor 是不同对象。补充给10–15行伪代码，做到别人能够按文稿复现。

### 3.3 Complementary Visual Observations

约0.60页。解释同一目标区域的两种观察：较高有效分辨率的 Local 和较大空间范围的 Global。它们不是无条件一一对应 Instance / Semantic。

写清三个步骤：构建观察→各自完整 grounding→恢复目标坐标、连续分数图重叠聚合。最终的类别图不是把已经 argmax 的整数标签直接平均。

正文主图只需显示 Aligned View Evidence Fusion。方法文字至少定义融合算子集合属于逐类、逐像素连续分数组合；完整形式进入补充：max、加权幂均值（线性是ρ=1）、加权 log-odds。具体选择列入固定配置表，不能只画“Fusion”却全文不定义它。

### 3.4 Joint Role–View Evidence Composition

约0.65页。阐明为什么独立最优文本不一定在新观察下仍最优，以及为何应联合考虑；定义：

\[
Z=\Psi\left(\mathcal A_L(G_L^{\theta}),\mathcal A_G(G_G^{\theta})\right),
\]

其中 `A` 是坐标恢复/聚合，`θ` 是同一套角色配置，`Ψ` 是固定的视图证据组合。然后使用原来的类别竞争与背景阈值。

Profile 是推理配置，不是额外学习的神经网络。正文不堆每数据集选项，但实现细节与补充必须列明固定候选、已选组合和选择依据。不要把候选筛查过程画成模型每张图自动作出的选择。

本节末尾用一个简短句子连接实验：我们用固定配置的2×2对照检验文本与视图是否存在超出独立贡献的互补，而不是预设其必然协同。

## 6. 理论如何扎实，而不是补一些听起来深刻的名词

### 6.1 角色异质性：架构事实 + 干预结果

论据一是计算对象不同：P为类别级标量、S为空间稠密场、I由query masks组织。论据二是同文本改变使用角色会改变效果。二者共同支持“补充信息应考虑用途”。

它们不推出“这些角色在数学上独立”，也不推出“同一文本永远不可能适合三个角色”。后期共享文本的正例恰好限定了命题范围。

### 6.2 Local / Global：可观察性权衡，不是泛化的生物学比喻

固定模型输入分辨率时，扩大图像范围会把更多场景关系带进观察，但缩小同一物体在输入/token网格中的尺寸；局部裁剪反过来提高细节采样，却删除一部分区域外关系。这是可直接从输入变换推导的取舍。

因此“连续地表/大区域组织”可能受益于广域，而细小实体可能需要局部细节。这个解释由 HRDA 的双分辨率设计、GLA-CLIP / OV-Stitcher 的跨窗口机制提供相关先例，但类别上的实际方向仍由本文实验验证。

SlowFast 的快慢视频分支可以启发“不同信息带宽承担互补职责”，但其时间采样与动作识别机制不等于遥感空间尺度。**不把 SlowFast 或生物视觉当作本方法成立的直接证明。**

### 6.3 Anchor：可保证的是更新边界，不是正确性

由更新定义可以直接得到：`||R(a,b)−a||∞≤ατ`（`a∈[0,1]`，非负α/τ）。它说明每次输出干预受控、零补充可回到anchor。

不能据此保证类别不漂移、最终 mIoU 不下降；query admission 与 argmax 仍含非连续变化。若正文篇幅紧，保留直观解释即可，把这个简单性质放补充，不专设“理论定理”章节。

### 6.4 两方法的协同：机制解释 + 固定配置证据

文本改变的是特定概念条件下的读出；观察改变的是该条件计算可以利用的视觉内容及其采样。故二者存在依赖是合理的：更明确的语言要求不能弥补缺失视觉证据，更多视觉内容也可能在弱文本条件下被误用。

实验使用：

\[
\Gamma=m_{11}-m_{10}-m_{01}+m_{00}.
\]

这定义的是 mIoU 上的 performance interaction。它能够检验超加性结果，但不是内部特征交互的数学分解，更不是“attention 被充分使用”的证明。

正文要同时给出 `m11−m10` 与 `Γ`：前者回答第二部分在当前方法上有没有用；后者回答是不是超过独立贡献之和。iSAID 就是前者正、后者负的例子。**既有可执行增益，也有明确适用边界，比宣称处处协同更完整。**

## 7. Experiments：用问题组织，不按实验日期组织

### 4.1 Experimental Setup

约0.35页。八遥感数据集、两自然域扩展、冻结条件、评价口径、配置方式与上下文来源。完整尺寸、类别词、版本、threshold、融合式进入补充，不占两页正文。

Potsdam / Vaihingen 说明利用同一原始场景的邻接 RGB 重建1024上下文、目标512评测、不使用邻接标签；不要写成原始大幅正射图全部一次输入。保留用户确定的57.49主结果，另报当前单图控制即可。

### 4.2 Comparison with State of the Art

约0.80页。**Table 1 应继续以 PPT p16 的多方法主表为基础**，而非退化成只对 baseline / ProC 的三行表。按 CLIP-based、SAM3-based 分组，注明引用与复现来源。尚未核对的扩展方法不凭空补结果。

正文三段足够：总体覆盖与平均表现；相对最接近强基线的优势分布；不同类别/数据条件的剩余差距。不要逐格念完表格，也不以“所有数据集 SOTA”概括当前结果。

57.49 相对于 ProC 论文56.1的名义平均差为约1.39点；它是参考主表的数值差，不等于已经作过二者完全同输入协议的配对因果比较。

### 4.3 Contribution and Conditional Complementarity

约0.80页。主文建议优先一张真正匹配配置的四格表，而不是同时摆两张容易混淆的“Role-only”表。

**可直接用于初稿的固定配置表：**

| Dataset | Baseline `m00` | Role `m10` | View `m01` | Joint `m11` | Γ |
|---|---:|---:|---:|---:|---:|
| Potsdam | 57.87 | 58.59 | 62.34 | 63.18 | +0.11 |
| Vaihingen | 60.86 | 61.59 | 63.58 | 66.38 | +2.07 |
| LoveDA | 47.34 | 48.30 | 47.18 | 48.81 | +0.66 |
| iSAID | 27.64 | 28.27 | 28.73 | 29.13 | −0.23 |
| OEM | 44.30 | 50.53 | 45.17 | 53.08 | +1.68 |
| UAVid | 54.58 | 59.50 | 54.43 | 59.82 | +0.47 |
| UDD5 | 71.80 | 72.76 | 72.27 | 72.94 | −0.28 |
| VDD | 64.11 | 65.83 | 64.30 | 66.55 | +0.53 |
| **Macro** | **53.56** | **55.67** | **54.75** | **57.49** | **+0.63** |

角色、admission和算子固定为每数据集选定的最终 Joint 配置，仅开关两项补充。数值源为本工作区 `evidence/matched_interactions.csv`。

阶段独立最优 Role55.82→Joint57.49 用一句话说明，并将完整阶段表放补充。不能把55.82填入上表再算Γ。

这一节回答三件事即可：两个部分各自作用；何时 View 在 Role 后变得更有用；联合配置相对先选 Role 再选 View 是否值得。原六数据集后者平均+0.28是补充证据，不要把它包装成新的第三模块。

### 4.4 Why These Design Choices?

约0.65页。只围绕最关键的选择安排紧凑 Table 3，必要时分(a)/(b)两个panel：

- (a) 同一补充文本的不同角色用途，以及最终文本池下的普通多提示集成对照。现有共享18组可先写；公平的最终池对照若补跑，再加入对应行。
- (b) anchor-preserving完整策略与Direct。OEM/Potsdam可展示优势，VDD保留反例；六数据集完整表在补充。标题不要写成仅clipping消融。

不要把Block23、Replay、FCRA、所有fusion算子大表都塞进正文。它们解释研究选择，但不是论文的第二条主要贡献。

### 4.5 Where Does the Improvement Come From?

约0.60页。类别分组柱图与真实定性对照共用一个图或相邻两个小图。先用量化说明覆盖范围，再用图像说明实际改变，不用热图单独证明机制。

可采用现有统计：48/63类别改善；地表覆盖、水域和建筑等分组有较明显平均提升；移动目标并非全赢。展示 `Baseline / Role / View / Joint` 的真实mask，可比只给 `Baseline / Ours` 更直接说明协同。

自然域结果若主文空间允许，增加两行小表或一段：City67.90→72.20，VOC96.89→97.11；完整自然域角色与视图分析放补充。这是适用范围验证，不要掩盖City没有额外View收益。

## 8. 图表安排：每张只承担一个论证任务

| 图表 | 要回答的问题 | 推荐内容 | 不放什么 |
|---|---|---|---|
| Fig.1 Motivation，单栏 | 为什么不应默认共享补充文本？ | 一个真实文本，两个使用范围，配对数值/局部预测；必要时一个反向案例 | 复杂最终结构、十个消融缩写 |
| Fig.2 Method，双栏 | 方法的完整数据流是什么？ | anchor+三类补充；每视图完整grounding；有界角色修正；对齐View fusion | 三个独立decoder、每头专属视图、未实现latent路由 |
| Table1 Main，双栏 | 与本领域强方法相比怎样？ | p16多模型表、八数据集、宏平均、来源脚注 | 混合不同任务的不可比数值 |
| Table2 Factorial，单/双栏 | 两部分独立和共同作用如何？ | 上述固定配置四格表，Γ与反例均保留 | 将独立最优Role当作匹配反事实 |
| Table3 Design，紧凑 | 为什么是角色用途与anchor-preserving？ | 同文本不同用途；最终池对照；完整Residual/Direct小panel | 所有失败方向的大清单 |
| Fig.3 Analysis / qualitative，双栏 | 哪些区域真的改对了？ | 类别组涨幅小图+真实mask对比，含一个边界案例 | 生成的分割结果、仅attention热图 |

总目标是**三张关键表、三张功能明确的图**，不是机械要求数量。版面紧时把Fig.1缩成Introduction中的一个小示意，把自然域移补充，优先保住主图与最关键归因对照。

## 9. 如何从记录文件转成正文

写作的最小单位应由“一个实验”改成“一个可支持的判断”：

```text
原始CSV / 固定配置
        ↓
一句有限范围的判断
        ↓
最直接的表格或图像
        ↓
解释它支持哪一个设计、排除了哪一种替代解释
        ↓
正文一段；其余细节进补充
```

例如不写：“我们先做presence，又做top2，然后试了Block23和Replay，最后发现……”

应写：“Keeping grounding intact is important: restricting candidate updates to isolated internal states degraded the tested model. We therefore specialize evidence usage after complete grounding rather than separating the pretrained computation.” 相邻引用本项目补充表，而不是用外部文献代替自己的干预结果。

另一个例子，不写：“OEM涨8.77，Potsdam涨5.31，所以方法优越。”

应写：“Role and observation improvements are condition-dependent. On LoveDA, the selected view rule slightly degrades anchor predictions, yet improves the role-conditioned model. This contrast supports composing views under the intended textual condition rather than treating visual augmentation as an independent add-on.” 随后用固定四格表支撑。

## 10. 实际写作推进顺序

1. **冻结证据与术语。** 固定57.49版本；统一baseline来源、Local/Global含义、Role/Joint称呼。使用本轮证据账本，不重复清仓审计。
2. **先写Method及一张主图。** 以实际代码为限定义输入、输出和操作；先讲得可复现，再追求修辞。
3. **写Experiments。** 填真实主表、固定四格表和现有角色控制；将尚缺一两项对照明确留位，不填推测结果。
4. **再写Introduction和Related Work。** 根据已经站得住的设计与证据设定贡献幅度，避免先写宏大贡献再找实验。
5. **补最必要的对照和真实定性图。** 不因写论文重新开启关闭方向。具体见证据清单。
6. **完成八页英文初稿与补充材料。** 主文保持论证，补充放候选描述、配置表、复现算法、完整消融和失败案例。
7. **做一次模拟审稿，再做一次定向修订。** 只围绕实际缺口改，不反复扩大实验协议。

## 11. 我的模拟审稿标准与这一版的取舍

### 必须能回答

- 新增性：与ProC/CoCo/TMPA/OV-Stitcher最接近的地方是什么，本文多证明了什么？
- 归因性：角色化带来的收益是否超越相同提示池的普通使用？
- 结构性：图中每条箭头是否有对应代码，是否把输出融合误写成内部attention？
- 完整性：零补充如何回到baseline，别名如何保留，Instance如何使用Presence？
- 有效性：整体增益、类别改进、实际mask改变能否对上？
- 适用范围：为什么City/UDD/iSAID不呈现同样协同，为什么Pots/Vai需要更广域观察？

### 本版主动放弃的写法

不把三个角色写成互斥的信息需求；不把简单数学边界写成性能保证；不把多尺度本身写成首次创新；不使用“揭示attention未充分读取”的未证实结论；不把共享文本正例和Direct反例藏掉。

这些调整不是防御性降调，而是把文章的力量集中到已有数据真正支持的发现：**补充证据的价值取决于用途和观察条件，保留原生共享计算、在证据使用层面进行专门化，是一条有效的免训练路径。**
