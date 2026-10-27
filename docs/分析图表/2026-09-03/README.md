# 类别增益图、最新相关工作与主链路核查

> **历史分析记录，不是当前论文图入口。** 散点图的数据、描述统计与代码核查保留；正文现采用[类别组增益柱状图](../../论文框架/2026-09-03/README.md)。本页的代码映射对应核查时版本，后续单图观察对照等状态以根目录 state.md 为准。

核查日期：2026-09-03。代码版本：`1b3b1d3`。本次只制作本地分析图、核查资料与修正文档；没有改变模型、配置或服务器实验流程。

## 1. 可直接使用的图

- [PDF：论文排版](baseline_vs_joint_class_gain.pdf)
- [SVG：可编辑矢量图](baseline_vs_joint_class_gain.svg)
- [PNG：600 dpi，适合 PPT](baseline_vs_joint_class_gain.png)
- [63 个点的原始数据与来源](class_gain_data.csv)
- [统计与敏感性检查](class_gain_statistics.json)

横轴为同次完整评估中 `official` 的类别 IoU，纵轴为 `joint_role_view_best − official`，单位均为百分数/百分点。使用八个遥感数据集的全部 **63 个 dataset–class pairs**，包括背景与负增益类别；不包含 VOC20/Cityscapes，不使用类别 oracle。相同类别名在不同数据集中分别计数。UAVid 使用其已运行的 test 协议，因此图中写的是 full evaluation splits，而不是全部 validation。

| Baseline class IoU | 类别数 | Joint 平均 ΔIoU | 中位数 |
|---|---:|---:|---:|
| <30% | 17 | +7.03 | +1.63 |
| 30–60% | 22 | +3.82 | +2.35 |
| ≥60% | 24 | +1.41 | +0.86 |

共有 **48/63** 类提升，Pearson `−0.229`，Spearman `−0.177`。图中明确保留 OEM background 的 `+60.29`，以标注的纵轴断点避免压缩其余 62 个点。

这个结果支持：**收益并非只来自原本已经分得很好的类别；基线弱/中等类别获得了更大的平均收益。** 不支持“越弱的每个类别一定提升越大”。移除 OEM background 后，三个分组均值为 `+3.70/+3.82/+1.41`，Pearson `−0.193`；移除所有 background/clutter 后为 `+3.02/+4.25/+1.49`。因此最稳妥的是“弱/中等类别优于强类的平均收益”，不是严格单调关系。IoU 上界以及横轴与差值共享 baseline 也会影响相关性，散点图不单独证明因果机制。

建议英文图注：

> **Class-wise improvements across eight remote-sensing benchmarks.** Each marker denotes a dataset–class pair, plotting baseline IoU against the gain of Joint Role–View. The method improves 48 of 63 pairs, with larger mean gains for low- and medium-baseline groups than for already strong categories. All classes are retained; the marked axis break displays the large OpenEarthMap background gain. The dashed line summarizes the descriptive linear trend.

数据来源：

1. `logs/joint_role_view_profile_v1_full_4b5363f/summary/joint_role_view_classes.csv`
2. `logs/uavid_joint_role_view_v1_full_f51f712/summary/joint_role_view_classes.csv`
3. `logs/isaid_joint_p0_s3_i0_v1_full_b7dae83/summary/joint_role_view_classes.csv`

所有 baseline 与 joint 均按 `(dataset, class_index)` 配对，CSV 内保存具体 variant；JSON 保存输入文件 SHA-256。63 类均值 `+3.769` 不等于八数据集 macro gain `+3.923`，两者权重不同。

## 2. 最新文献：新近发表与此次补漏分开

检索截止 2026-09-03。此前未保存精确的检索日期/覆盖清单，因此本次以当前本地参考库为增量基准，不把“此次新找到”都称为“上次以后新发表”。

| 论文 | arXiv 首发 | 实际方法 | 与当前方法的关系 |
|---|---|---|---|
| DinoSplat-OV：Standalone DINOv3 for Remote Sensing Training-Free Open-Vocabulary Semantic Segmentation | 2026-08-04 | DINOv3/DINO.txt；文本感知的图传播、RGB 引导 Gaussian splatting 上采样、全局支持的滑窗处理；上采样有单图测试时优化 | 文本与视觉结构/全局局部的宏观交集；不是 SAM3 P/S/I 角色补充机制 |
| GeoSeg-OV: Bridging Geospatial Gaps with Structural Guidance for Open-Vocabulary Remote Sensing Segmentation | 2026-08-11 | 多旋转 CLIP cost volume；冻结 VFM 提供结构偏置；SGA 聚合、CAD 解码；训练 CLIP 部分参数及聚合/解码模块 | 语义与结构各司其职，但**不是免训练**，也不是三头角色文本+双视图输出融合 |
| RSGPNet: Geometric Prompting for Remote Sensing Open-Vocabulary Semantic Segmentation | 2026-06-25（此次补漏） | SAM3 文本粗分割 → 从粗 mask 生成 box → 几何重提示 → 粗细一致性校验 | 同属免训练 SAM3 遥感 OVSS；与我们早期 self-box 风险直接相关，但它增加一致性约束，不能以我们的失败替代评价该论文 |

三篇均核对 arXiv 原文并下载了 PDF。官方来源：[DinoSplat-OV](https://arxiv.org/abs/2608.03023)、[GeoSeg-OV](https://arxiv.org/abs/2608.10426)、[RSGPNet](https://arxiv.org/abs/2606.28410)。DinoSplat-OV 的网页元数据与 PDF 标题词序略不同，本表采用 PDF 标题。

### ProC-SAM3 是否仍是主要 SOTA 对照？

**在本次找到并核实、且有相近八数据集免训练结果的公开工作中，仍以 ProC-SAM3 为最重要的强对照。没有查到足以替换这一比较位置的新八数据集结果。** 这不等于每个数据集都由 ProC 最优。

- ProC-SAM3 最新 arXiv 为 2026-07-22 的 v2，已标注 GRSL 录用，八数据集平均 **56.1**；本地现有 PDF 已是 v2，无需重复下载。[论文](https://arxiv.org/abs/2606.21863)
- RSGPNet 的四数据集 mIoU 为 LoveDA **47.8**、Potsdam **59.7**、Vaihingen **61.1**、UDD5 **71.0**，平均 **59.9**。ProC 在同名四数据集上为 **46.1/58.8/64.5/73.4**，平均 **60.7**。RSGP 在前两个数据集更高，但并未整体超过 ProC；四数据集平均也不能直接和八数据集 56.1 比。[RSGP 原文 Table II/IV](https://arxiv.org/html/2606.28410v1)
- DinoSplat-OV Table 1 的 UDD5/DOTA/LoveDA/Vaihingen 为 **42.9/28.6/36.3/42.3**，未提供当前八数据集完整比较，也未直接比较 ProC。DOTA 不能当作 iSAID。[原文](https://arxiv.org/html/2608.03023v1)
- 另补查了 2 月的 *Enabling Training-Free Text-Based Remote Sensing Segmentation*：CLIP 语义选择 SAM 网格 masks，八数据集平均 **41.3**，不是新的 SAM3 对手。[原文 Table 1](https://arxiv.org/html/2602.17799v1)
- *Training-Free Entity-Level Few-Shot Segmentation ... with Advection Refinement*（2026-07-31）用 SAM3 实体、support 前景/背景原型和文本势场；属于 few-shot 协议，不并入我们的无 support 主表。[arXiv](https://arxiv.org/abs/2607.29278)

这两篇补查工作的 PDF 也已保存到本地参考库；ELFSS-AR 当前只完成摘要层方法/协议核验，未将其未分析的结果当作排名证据。本轮共补入 5 篇 PDF，详细分类见 `参考论文/索引.md`。

这轮未发现与“**保留共享 grounding + 按 P/S/I 分配补充文本残差 + 联合选择 Role 与对齐视图分数融合**”高度同构的新增遥感论文。已有方法仍覆盖其中若干部件，不能据此声明所有组成技术首次提出。

## 3. 理论—代码：主链一致，修正过度简写

本次查看了 baseline 论文 §3.1–3.2/Eq.1–3、当前模型入口、角色组合、视图复原/融合、配置与实际汇总链。GitNexus 图谱对应 `1b3b1d3`，用于定位；最终结论依据实际源码及回传日志。没有做全仓库审计，也没有重跑 SAM3。

### 3.1 真实主流程

```text
                   official anchor + role supplementary texts
                                     │
              ┌──────────────────────┴──────────────────────┐
              │                                             │
      Local observation                             Global/Context observation
              │                                             │
      image encoding once                           image encoding once
              │                                             │
      each required text:                           each required text:
      complete frozen SAM3 grounding                complete frozen SAM3 grounding
              │                                             │
      P/S/I anchor-preserving                       P/S/I anchor-preserving
      role evidence composition                     role evidence composition
              │                                             │
      native p × max(S,I)                            native p × max(S,I)
      + official-baseline compensation              + official-baseline compensation
              │                                             │
      map back / overlap aggregation                map back / overlap aggregation
              └───────────────┬─────────────────────────────┘
                       aligned class score maps
                              │
                       View evidence fusion Ψ
                              │
                    class argmax + background threshold
```

一个 observation 可以包含多个 crop，不是必然只调用两次图像编码；相同 crop 的图像编码被所有需要的文本复用。当前选中的 **同一套角色 slots** 用于两种视图，不是 S 专走 Global、I 专走 Local，也不是给每个角色单独做跨视图算子。

### 3.2 Presence 与 Instance 的准确关系

定义 `r_q` 为 raw object confidence，`M_q` 为 sigmoid 后的 mask probability，则默认实现为：

\[
Q=\{q:a r_q>\eta\},\qquad
\mathcal I(M,r;p,a)=\max_{q\in Q}M_qr_qp.
\]

这里 `a=p` 是 native admission；选用 anchor admission 时只把 `a` 换成 `p_A`，**实例幅度依然乘当前 p**。外层仍有 `F=p\max(S,I)`。原 `state.md` 把 `r_q` 定义为 raw confidence 却在 I 中漏写 p，属于公式表述漂移，本次已修正。baseline 原文的 Eq.1 用复合符号 `s_conf`，不能把它不加辨别地等同 raw confidence。[baseline 原文](https://arxiv.org/html/2512.08730v2)

对非零角色 slot，令 `B(a,b)=clip(a+0.5·clip(b−a,−0.25,0.25),0,1)`，则：

\[
p'=B(p_A,p_P),\qquad S'=B(S_A,S_S),
\]
\[
I_A'=\mathcal I(M_A,r_A;p',a),\qquad
I_I'=\mathcal I(M_I,r_I;p',a),\qquad
I'=B(I_A',I_I'),\qquad F^\theta=p'\max(S',I').
\]

零 slot 保持对应 anchor 来源；P 的变化仍可改变 anchor instance 的 query admission 和幅度。因此“只取对应角色的输出”不等于取消 native P→I 耦合。

每个 view/unit 再做 `G_v=clip(B_v^official + F_v^theta − F_v^0,0,1)`，以保护原始 aliases 与原 baseline 聚合顺序。滑窗恢复还保留 query-level 聚合后的 official correction。合并 anchor 三个分量得到的 `F_v^0` 不一定逐像素等于官方多别名 `B_v^official`，所以外层差分不是多余运算。

### 3.3 核对表

| 理论组件 | 实际代码位置 | 结论 |
|---|---|---|
| 冻结文本缓存、完整概念 grounding | `role_functional_text_screen.py:_rpt_prepare_text_cache/_rpt_set_cached_prompt`；`sam3/model/sam3_image.py:forward_grounding` | Match；每条补充文本仍完整更新其自身 grounding，不使用 anchor-clamped Replay |
| 每 view 复用 image features，按角色读取 | `role_visual_field.py:_rvf_ground_view` | Match；不是把文本 residual 直接加到 CLIP/视觉特征 |
| bounded role residual + P/I 原生耦合 | `_rvf_compose_class`、`_rvf_instance` | Match；只需修正“完全独立三头”和漏 p 的文字 |
| official anchor/alias 零更新保护 | `_jrv_ground_target`、`_jrv_accumulate_official_units` | Match；有外层 official 差分补偿 |
| Local/Context 的坐标对齐与重叠恢复 | `_rvf_visual_units`、`_jrv_accumulate_visual_units` | Match；Potsdam/Vaihingen 仍使用邻接真实 tiles，不是单 tile 放大 |
| 两视图融合 | `_jrv_fuse_views`、`_jrv_final_fuse` | Match；位于完整 P/S/I 组合之后，输入为同坐标 `C×H×W` 类别分数图 |
| 融合算子不必统一 | `configs/experiments/joint_role_view_final_v1.json` | Match；max/linear/power/logit 是 Ψ 的实例，不要求把理论固定成 max |
| 最终类别分割 | `segearthov3_segmentor.py:predict`；`role_functional_text_screen.py:_rpt_threshold` | Match；argmax 和 `prob_thd` 后产生标签，未改成 feature-space fusion |
| 实验选中的固定组合 | `tools/summarize_joint_role_view.py:summarize` | Match；先累计每个变体的混淆矩阵，再选 dataset-wide variant；没有用逐图/逐类 oracle 拼主结果 |

可用一个抽象算子写最后的融合：`Z=Ψθ(G_L,G_G)`。在正式方法图中只标 **View Evidence Fusion** 完全准确；但不能画成 “Role-specific cross-view attention” 或三路 `P_L/P_G, S_L/S_G, I_L/I_G` 逐头路由，这不是当前已验证实现。实现中的若干变量名带 `logits`，实际已 sigmoid/加权成为 `[0,1]` 分数；这里“同一空间”指类别与坐标对齐的分数域，不意味着训练过的共同概率校准。

### 3.4 日志一致性与实际部署范围

八数据集 reproduction CSV 的 `native_prompt_parity_max_abs` 与 `reference_identity_max_abs` 均为 **0**；旧六数据集 closure 的 `joint_residual` 结果与当前选中 Joint 数值一致。较老 Role-only 筛查到当前视图链的差值最多约 `0.018` mIoU（Vaihingen），因此仍用本次 matched reference 分析，不把历史数值当逐 bit 相同。

需要保留一个工程层面的区别：

- `joint_role_view` 是筛查/汇总模式，MMEngine 主出口仍是 official；方法变体由独立混淆矩阵进入 summary。
- `joint_role_view_final` 会把选中的固定方法分数作为真正的 `pred_sem_seg` 返回。
- 当前 final registry 只固定了原六数据集；UAVid/iSAID/两个自然域使用扩展筛查入口记录真实变体，尚未统一加入这份六数据集部署注册表。这是后续部署收尾，不是现有结果的理论漂移；后续导出主方法分割图时应使用/补齐固定部署入口，不能误拿 screen 模式的 official 图片。

## 4. 使用与交付范围

在已安装 NumPy、SciPy、Matplotlib 的本地环境重建：

```bash
cd /Users/pengjunhao/Desktop/SegEarth3
python docs/分析图表/2026-09-03/make_class_gain_figure.py --repo /Users/pengjunhao/Desktop/SegEarth3
```

本次所有文件均为本地研究产物；没有需要复制到服务器的代码/配置，没有触发 GPU 实验或 GitHub 提交。绘图脚本用于可追溯复画，不参与模型推理。
