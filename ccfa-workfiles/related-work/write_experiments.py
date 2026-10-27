from pathlib import Path

ROOT=Path(r"D:\论文\9.27论文")
KIT=ROOT/"author-kit-main"
CN=ROOT/"中文论文"/"论文中文版.md"

en_exp=r'''\section{Experiments}
\label{sec:experiments}

\subsection{Experimental Setup}

\textbf{Benchmarks and metrics.} We evaluate on the eight remote-sensing benchmarks used by SegEarth-OV and SegEarth-OV3 \cite{R06,R11}: Potsdam, Vaihingen, LoveDA, iSAID, OpenEarthMap (OEM), UAVid, UDD5, and VDD. We retain the baseline evaluation splits, class mappings, ignored labels, and image-based UAVid protocol. iSAID contains 11,644 processed validation tiles, and UAVid contains 1,020 evaluated patches. The primary metric is mean intersection over union (mIoU, \%). The overall average weights the eight datasets equally. Class-group analysis weights dataset--class pairs equally and is reported separately. VOC20 and Cityscapes provide additional natural-image evaluations.

\textbf{Implementation and profile selection.} We use the same frozen SAM3 checkpoint and native grounding as the reproduced baseline. Candidate descriptions are generated offline and stored verbatim. Unless stated otherwise, $\alpha=0.5$ and $\tau=0.25$. For each benchmark, the role slots, admission mode, and view operator are selected offline using the available evaluation annotations and then fixed for every image. Inference with a fixed profile does not access annotations. The reported results therefore use evaluation-selected dataset-level profiles, not an independent held-out configuration-selection split.

Local and Context observations are built from RGB data. For Potsdam and Vaihingen, the selected main protocol uses spatially aligned neighboring RGB tiles from the same original scene to reconstruct a 1,024-pixel context around a 512-pixel target; only the target region is scored, and neighboring ground truth is never used. This input extent is larger than the isolated-tile baseline. The same-image 256/512 control is reported as a scope experiment rather than a replacement for the main protocol. No temporal frames, labeled visual exemplars, or auxiliary sensing modalities are used.

\textbf{Comparison sources.} Competitor values in Table~\ref{tab:main-comparison} are transcribed from the ProC-SAM3 comparison \cite{R12}; the reproduced SegEarth-OV3 row and JRV come from matched local runs. All component gains and interaction statistics use the full-precision matched baseline, not the one-decimal comparison table. The mixed provenance means that Table~\ref{tab:main-comparison} supports an internal numerical comparison, not an independently established leaderboard rank.

\subsection{Comparison with Existing Methods}

\begin{table*}[t]
\centering
\caption{Remote-sensing open-vocabulary semantic segmentation (mIoU, \%). Competitor rows follow the reported values in ProC-SAM3 \cite{R12}; the SegEarth-OV3 row is our reproduction, and JRV is evaluated with the context-access protocol described in Section~\ref{sec:experiments}. Avg. is the equal-weight mean over eight datasets. Published one-decimal values are kept at their reported precision.}
\label{tab:main-comparison}
\setlength{\tabcolsep}{3pt}
\scriptsize
\begin{tabular}{lccccccccc}
\toprule
Method & Backbone & Potsdam & Vaihingen & LoveDA & iSAID & OEM & UAVid & UDD5 & VDD & Avg. \\
\midrule
VIP & DINOv3 + dino.txt & 23.0 & 30.5 & 31.2 & 23.5 & 20.7 & 19.9 & 35.2 & 52.5 & 29.6 \\
SCLIP & CLIP & 39.6 & 35.9 & 30.4 & 16.1 & 29.3 & 31.4 & 38.7 & 37.9 & 32.4 \\
ClearCLIP & CLIP & 42.0 & 36.2 & 32.4 & 18.2 & 31.0 & 36.2 & 41.8 & 39.3 & 34.6 \\
ProxyCLIP & CLIP + DINOv2 & 49.0 & 47.5 & 34.3 & 21.8 & 38.9 & 35.8 & 40.8 & 47.8 & 39.5 \\
SegEarth-OV & CLIP & 48.5 & 29.1 & 36.9 & 21.7 & 40.3 & 42.5 & 50.6 & 45.3 & 39.2 \\
RSCLIP & CLIP & 47.4 & 40.3 & 35.5 & 21.2 & 39.8 & 42.5 & 50.4 & 42.5 & 39.9 \\
CorrCLIP & CLIP + DINO + SAM2 & 51.9 & 47.0 & 36.9 & 25.5 & 32.9 & 38.3 & 46.1 & 47.3 & 40.7 \\
ConInfer & CLIP + DINOv3 & 50.0 & 31.4 & 39.3 & 20.1 & 42.0 & 46.4 & 46.9 & 50.3 & 40.8 \\
ReAttnCLIP & CLIP & 48.7 & 29.9 & 37.0 & 23.2 & 41.1 & 44.0 & 53.7 & 49.7 & 40.9 \\
ActiveSAM & SAM3 & 40.6 & 45.1 & 41.1 & 28.3 & 40.7 & 53.3 & 72.1 & 62.2 & 47.9 \\
SegEarth-OV3 (reproduced) & SAM3 & 57.8 & 60.8 & 47.4 & 27.6 & 44.3 & 54.7 & 71.7 & 64.1 & 53.5 \\
ProC-SAM3 & SAM3 & 58.8 & 64.5 & 46.1 & \textbf{29.5} & 48.9 & \textbf{60.0} & \textbf{73.4} & \textbf{67.5} & 56.1 \\
JRV (ours) & SAM3 & \textbf{63.2} & \textbf{66.4} & \textbf{48.8} & 29.1 & \textbf{53.1} & 59.8 & 72.9 & 66.6 & \textbf{57.5} \\
\bottomrule
\end{tabular}
\end{table*}

JRV reaches 57.49 average mIoU in the full-precision pairwise evaluation. The matched baseline is 53.56, giving an average gain of 3.92 points. Role-Functional Text accounts for 2.25 points, and joint view composition adds another 1.67 over the independently selected best role-only stage. Gains appear on all eight datasets. The largest increases are on OEM (+8.77), Vaihingen (+5.52), Potsdam (+5.31), and UAVid (+5.24).

Against the reported ProC-SAM3 row, JRV is higher on four datasets and lower on four, with a 1.39-point higher displayed average. The comparison is useful for positioning because ProC-SAM3 is the strongest verified published result under the full eight-dataset, training-free protocol. It remains a mixed-source comparison, and we do not describe the internal 57.49 result as an independently established state of the art.

\subsection{Functional Use of Supplementary Text}

\begin{table}[t]
\centering
\caption{Macro component progression. Role-only is the best recorded independent role profile; it is not the matched Role condition used for interaction analysis.}
\label{tab:component-progression}
\small
\begin{tabular}{lccc}
\toprule
Stage & Macro mIoU & $\Delta$ vs baseline & Positive \\
\midrule
Matched baseline & 53.56 & -- & -- \\
Role-Functional Text & 55.82 & +2.25 & 8/8 \\
Joint Role--View & 57.49 & +3.92 & 8/8 \\
\bottomrule
\end{tabular}
\end{table}

Table~\ref{tab:component-progression} separates the two stages of the final system. Role-only improves every dataset over the matched baseline, including gains of 6.23 on OEM and 4.92 on UAVid. Joint composition then improves over the role-only stage on every dataset. The component progression therefore supports both the language-evidence stage and the additional view stage, while the interaction analysis below fixes the profile to avoid selecting a different role configuration for each cell.

\begin{table}[t]
\centering
\caption{The same semantic-oriented candidate used either only for Semantic supplementation or for all three roles. Both variants retain the anchor and bounded update; values are final mIoU.}
\label{tab:role-use}
\small
\setlength{\tabcolsep}{4pt}
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
\end{table}

The utility of a description depends on where it is used. Across all 18 recorded dataset--candidate settings, semantic-only supplementation is better in 13 cases, while shared use exceeds the baseline in 7. On OEM, the S3 description gives 46.28 when used only for Semantic and 44.02 when shared across all roles. LoveDA follows the same direction. UDD5 reverses it, reaching 73.04 with shared use. Shared supplementation is therefore not uniformly harmful; the supported conclusion is that a category-level phrase does not have a uniform functional effect across readouts.

Anchor preservation also matters as a complete strategy. With the final profile fixed, the residual path gives 61.82 macro mIoU over the six datasets with completed direct-prediction closure, compared with 53.29 for direct prediction. VDD is the exception, where direct prediction reaches 67.26 versus 66.55 for the residual path. This control changes both the bounded update and the official-score compensation, so the result supports the anchor-preserving composition as a whole rather than clipping in isolation.

\subsection{Matched Role--View Interaction}

We evaluate four conditions with the final role slots, admission mode, and view operator held fixed: baseline $m_{00}$, role-only $m_{10}$, view-only $m_{01}$, and joint $m_{11}$. The performance interaction is
\begin{equation}
\Gamma=m_{11}-m_{10}-m_{01}+m_{00}.
\label{eq:interaction}
\end{equation}
This factorial contrast measures whether the joint mIoU gain exceeds the sum of the matched individual gains. It is not a pixel-level interaction count.

\begin{table}[t]
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
\end{table}

The joint configuration is better than either matched component on all eight datasets, and $\Gamma$ is positive on six. The largest positive interactions are on Vaihingen (+2.07) and OEM (+1.68). LoveDA and UAVid provide direct evidence of conditional usefulness: the selected view operator slightly lowers the anchor prediction ($-0.16$ and $-0.15$), but its interaction with the role configuration is positive (+0.66 and +0.47). Potsdam behaves differently: view composition already provides a large main effect (+4.48), and the additional interaction is only +0.11. iSAID and UDD5 have positive total gains but negative interactions, indicating overlapping rather than complementary corrections.

A broader view screen provides context for these results. A shared-canvas observation produces +0.92 macro over 4/6 datasets, confirming that the additional observation contains usable information. The best fixed universal operator family, however, gives only +0.10 macro over 3/6, showing that a single view rule is unstable across datasets. The joint profile is selected per benchmark and fixed for inference; the interaction table tests whether role-conditioned text changes the value of that observation, not whether every possible context fusion is beneficial.

\subsection{Category and Pixel Analysis}

\begin{table}[t]
\centering
\caption{Category-group improvements over the matched baseline. Each entry averages dataset--class pairs; ``Additional'' is Joint minus the independently selected role-only result, not the interaction in Equation~\ref{eq:interaction}.}
\label{tab:category-groups}
\small
\setlength{\tabcolsep}{3.5pt}
\begin{tabular}{lcccc}
\toprule
Category group & Pairs & Positive & Role $\Delta$ & Joint $\Delta$ \\
\midrule
Water-related & 4 & 3 & +3.15 & +5.65 \\
Vegetation / land cover & 15 & 14 & +2.83 & +4.95 \\
Built structures & 11 & 7 & +1.59 & +2.48 \\
Movable objects & 11 & 7 & -0.02 & +1.49 \\
Transport surfaces & 9 & 6 & +1.43 & +1.26 \\
Sports grounds & 5 & 4 & +0.34 & +0.79 \\
Background / clutter & 8 & 7 & +6.64 & +10.22 \\
\bottomrule
\end{tabular}
\end{table}

JRV improves 48 of 63 dataset--class pairs, including 41 of 55 foreground pairs. Vegetation and land cover show the broadest consistency at 14/15 positive pairs. Water-related and built-structure groups also improve on average. Movable objects receive little average benefit from role text alone ($-0.02$) but improve after joint composition (+1.49), showing that the two stages do not have to benefit the same category groups.

The gains concentrate on classes with weaker baseline performance. The 17 pairs below 30\% baseline IoU improve by +7.03 on average; the 30--60\% group improves by +3.82; the group above 60\% improves by +1.41. This is an average trend, not a monotone guarantee. Transport surfaces are a counterexample: they improve by +1.26 over the baseline but decline by 0.17 relative to role-only prediction. The background/clutter mean is +10.22 and is strongly influenced by OEM; its group median is +1.56, so the foreground results provide the more informative aggregate.

Pixel transitions show that the gains correspond to corrected assignments. Approximately 429.16 million baseline errors become correct, while 165.85 million previously correct pixels become incorrect, a net increase of 263.31 million correct assignments and a correction-to-damage ratio of 2.59. These counts refer to evaluated images and tiles, not independent geographic samples. They complement class-balanced mIoU without implying that every class or component improves.

\subsection{Natural-Image Evaluation and Scope}

\begin{table}[t]
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
\end{table}

Role-functional evidence also improves the two natural-image evaluations. VOC20 rises from 96.89 to 97.11, with a small additional view gain and a near-additive interaction (+0.01 after rounding). Cityscapes rises from 67.90 to 72.20, driven by role supplementation. Its joint optimum reduces to the role-specialized Global endpoint, so additional view composition does not improve that endpoint.

The same-image control clarifies the role of observation construction. On Potsdam and Vaihingen, using four 256-pixel crops and a 512-pixel Global view from the current image selects Global in both cases and returns 58.59 and 62.33, respectively, without an additional view gain. The main table instead uses aligned neighboring context for these two datasets. We therefore attribute the large Potsdam and Vaihingen gains to the combined role and observation protocol, not to an arbitrary extra crop. The natural-image results support the transfer of role supplementation while showing that view composition depends on whether the alternative observation yields compatible evidence.

Across the evaluations, the method uses a fixed dataset profile selected offline, freezes all SAM3 weights, and performs no image-level ground-truth routing. These constraints define the evidence: the experiments support role-sensitive evidence organization and conditional view composition under the reported protocols, not universal superiority of shared text, larger fields, or a particular fusion operator.
'''

cn_exp=r'''## 4. 实验

### 4.1 实验设置

**基准与指标。** 我们在 SegEarth-OV 和 SegEarth-OV3 [6,11] 使用的八个遥感基准上评价：Potsdam、Vaihingen、LoveDA、iSAID、OpenEarthMap（OEM）、UAVid、UDD5 和 VDD。保持 baseline 的评测划分、类别映射、忽略标签以及基于图像的 UAVid 协议。iSAID 包含 11,644 个处理后的验证切片，UAVid 包含 1,020 个评测图块。主指标为 mIoU（%）。总体平均对八个数据集等权；类别组分析对数据集—类别对等权并单独报告。VOC20 与 Cityscapes 用于自然图像扩展评价。

**实现与 profile 选择。** 使用与复现 baseline 相同的冻结 SAM3 权重和原生 grounding。候选描述离线生成并按原文保存。无特别说明时 \(\alpha=0.5\)、\(\tau=0.25\)。每个 benchmark 的 role 槽、admission 模式和视图算子使用现有评测标注离线选择，然后对所有图像固定。固定 profile 后的推理不访问标注。因此，报告的是评测集选择的数据集级 profile，而不是由独立留出集选择出的配置结果。

Local 与 Context 由 RGB 数据构造。Potsdam 和 Vaihingen 的主协议使用同一原始场景中空间对齐的邻接 RGB 图块，在 512 像素目标周围重建 1,024 像素上下文；只评价目标区域，从不使用邻接标签。该输入范围大于隔离图块 baseline。同一图像内部的 256/512 控制作为范围实验报告，不替代主协议。方法不使用视频时序帧、带标注视觉样例或辅助传感模态。

**比较来源。** 表 1 的竞争者数值转录自 ProC-SAM3 的比较表 [12]；复现的 SegEarth-OV3 行与 JRV 来自匹配的本地实验。所有组件增益与交互统计都使用全精度匹配 baseline，而不是一位小数比较表。由于来源混合，表 1 支持内部数值比较，不构成经过独立复现的排行榜结论。

### 4.2 与已有方法的比较

| 方法 | 骨干 | Potsdam | Vaihingen | LoveDA | iSAID | OEM | UAVid | UDD5 | VDD | Avg. |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| VIP | DINOv3 + dino.txt | 23.0 | 30.5 | 31.2 | 23.5 | 20.7 | 19.9 | 35.2 | 52.5 | 29.6 |
| SCLIP | CLIP | 39.6 | 35.9 | 30.4 | 16.1 | 29.3 | 31.4 | 38.7 | 37.9 | 32.4 |
| ClearCLIP | CLIP | 42.0 | 36.2 | 32.4 | 18.2 | 31.0 | 36.2 | 41.8 | 39.3 | 34.6 |
| ProxyCLIP | CLIP + DINOv2 | 49.0 | 47.5 | 34.3 | 21.8 | 38.9 | 35.8 | 40.8 | 47.8 | 39.5 |
| SegEarth-OV | CLIP | 48.5 | 29.1 | 36.9 | 21.7 | 40.3 | 42.5 | 50.6 | 45.3 | 39.2 |
| RSCLIP | CLIP | 47.4 | 40.3 | 35.5 | 21.2 | 39.8 | 42.5 | 50.4 | 42.5 | 39.9 |
| CorrCLIP | CLIP + DINO + SAM2 | 51.9 | 47.0 | 36.9 | 25.5 | 32.9 | 38.3 | 46.1 | 47.3 | 40.7 |
| ConInfer | CLIP + DINOv3 | 50.0 | 31.4 | 39.3 | 20.1 | 42.0 | 46.4 | 46.9 | 50.3 | 40.8 |
| ReAttnCLIP | CLIP | 48.7 | 29.9 | 37.0 | 23.2 | 41.1 | 44.0 | 53.7 | 49.7 | 40.9 |
| ActiveSAM | SAM3 | 40.6 | 45.1 | 41.1 | 28.3 | 40.7 | 53.3 | 72.1 | 62.2 | 47.9 |
| SegEarth-OV3（复现） | SAM3 | 57.8 | 60.8 | 47.4 | 27.6 | 44.3 | 54.7 | 71.7 | 64.1 | 53.5 |
| ProC-SAM3 | SAM3 | 58.8 | 64.5 | 46.1 | **29.5** | 48.9 | **60.0** | **73.4** | **67.5** | 56.1 |
| JRV（本文） | SAM3 | **63.2** | **66.4** | **48.8** | 29.1 | **53.1** | 59.8 | 72.9 | 66.6 | **57.5** |

JRV 在全精度配对评价中达到 57.49 的平均 mIoU。匹配 baseline 为 53.56，平均提升 3.92。Role-Functional Text 贡献 2.25，联合视图组合在独立最优 Role-only 基础上再增加 1.67。八个数据集均出现提升，最大增益出现在 OEM（+8.77）、Vaihingen（+5.52）、Potsdam（+5.31）和 UAVid（+5.24）。

与 ProC-SAM3 的报告行相比，JRV 在四个数据集上更高、四个上更低，展示平均值高 1.39。该比较有助于定位，因为 ProC-SAM3 是完整八数据集、免训练协议下已核验的最强公开结果。但它仍是混合来源比较，不能把内部 57.49 描述为已经独立建立的公开 SOTA。

### 4.3 补充文本的功能性使用

| 阶段 | Macro mIoU | 相对 baseline | 正提升数据集 |
|---|---:|---:|---:|
| 匹配 baseline | 53.56 | — | — |
| Role-Functional Text | 55.82 | +2.25 | 8/8 |
| Joint Role–View | 57.49 | +3.92 | 8/8 |

该表区分最终系统的两个阶段。Role-only 在八个数据集上均超过匹配 baseline，其中 OEM 提升 6.23，UAVid 提升 4.92。联合组合随后在八个数据集上全部超过 Role-only。组件递进因此同时支持语言证据阶段和额外视图阶段；下面的交互分析固定最终 profile，以避免在不同四格中使用不同 role 配置。

| 数据集 | 候选 | Baseline | 仅 Semantic | 共享 P/S/I |
|---|---|---:|---:|---:|
| Potsdam | S2 | 57.87 | **58.00** | 56.63 |
| Vaihingen | S3 | 60.86 | **61.57** | 61.28 |
| LoveDA | S1 | 47.34 | **48.09** | 46.61 |
| OEM | S3 | 44.30 | **46.28** | 44.02 |
| UDD5 | S3 | 71.80 | 71.56 | **73.04** |
| VDD | S1 | 64.11 | **65.27** | 65.05 |

描述的价值取决于使用位置。全部 18 组数据集—候选设置中，仅 Semantic 使用在 13 组更好，共享使用在 7 组超过 baseline。OEM 的 S3 描述在仅用于 Semantic 时为 46.28，共享给三个 role 时为 44.02；LoveDA 同向。UDD5 反向，共享使用时达到 73.04。共享补充并不总是有害；可以支持的结论是，类别级短语对不同 readout 并不具有统一的功能效果。

Anchor 保留作为完整策略也很重要。固定最终 profile 后，残差路径在具有完整 direct closure 的六个数据集上达到 61.82 macro mIoU，而直接预测为 53.29。VDD 是例外，直接预测为 67.26，残差路径为 66.55。该对照同时改变有界更新与官方分数补偿，因此支持的是完整 anchor-preserving 组合，而不是单独把差异归因于 clip。

### 4.4 匹配的 Role–View 交互

我们固定最终 role 槽、admission 模式和视图算子，比较四种条件：baseline \(m_{00}\)、Role-only \(m_{10}\)、View-only \(m_{01}\) 和 Joint \(m_{11}\)。性能交互为

\[
\Gamma=m_{11}-m_{10}-m_{01}+m_{00}.
\tag{14}
\]

该因子对照衡量 Joint 的 mIoU 增益是否超过两个匹配单组件的增益之和，而不是逐像素交互计数。

| 数据集 | \(m_{00}\) | \(m_{10}\) | \(m_{01}\) | \(m_{11}\) | \(\Gamma\) |
|---|---:|---:|---:|---:|---:|
| Potsdam | 57.87 | 58.59 | 62.34 | **63.18** | +0.11 |
| Vaihingen | 60.86 | 61.59 | 63.58 | **66.38** | +2.07 |
| LoveDA | 47.34 | 48.30 | 47.18 | **48.81** | +0.66 |
| iSAID | 27.64 | 28.27 | 28.73 | **29.13** | −0.23 |
| OEM | 44.30 | 50.53 | 45.17 | **53.08** | +1.68 |
| UAVid | 54.58 | 59.50 | 54.43 | **59.82** | +0.47 |
| UDD5 | 71.80 | 72.76 | 72.27 | **72.94** | −0.28 |
| VDD | 64.11 | 65.83 | 64.30 | **66.55** | +0.53 |
| **平均** | **53.56** | **55.67** | **54.75** | **57.49** | **+0.63** |

联合配置在八个数据集上均优于任一匹配单组件，\(\Gamma\) 在六个数据集为正。最强正交互出现在 Vaihingen（+2.07）和 OEM（+1.68）。LoveDA 与 UAVid 直接体现条件价值：所选视图算子在 anchor 上分别降低 0.16 和 0.15，但在匹配 role 配置下产生 +0.66 和 +0.47 的交互。Potsdam 的情况不同，视图本身已有 +4.48 的主效应，额外交互只有 +0.11。iSAID 与 UDD5 的总增益为正，但交互为负，说明收益重叠而非互补。

更广泛的视图筛查为这一结果提供背景。shared-canvas 观察在 4/6 个数据集上产生 +0.92 macro，说明第二观察包含可用信息；最佳固定通用算子族只有 +0.10，3/6 为正，说明单一视图规则不稳定。Joint profile 按 benchmark 选择并在推理时固定；交互表检验的是角色化文本是否改变该观察的价值，而不是任意上下文融合都有效。

### 4.5 类别与像素分析

| 类别组 | 类别对 | 正提升 | Role ΔIoU | Joint ΔIoU |
|---|---:|---:|---:|---:|
| 水体相关 | 4 | 3 | +3.15 | +5.65 |
| 植被与土地覆盖 | 15 | 14 | +2.83 | +4.95 |
| 建筑结构 | 11 | 7 | +1.59 | +2.48 |
| 可移动目标 | 11 | 7 | −0.02 | +1.49 |
| 交通地表 | 9 | 6 | +1.43 | +1.26 |
| 体育场地 | 5 | 4 | +0.34 | +0.79 |
| 背景 / 杂项 | 8 | 7 | +6.64 | +10.22 |

JRV 在 63 个数据集—类别对中提升 48 个，在 55 个前景对中提升 41 个。植被与土地覆盖最一致，15 对中提升 14 对；水体与建筑结构也平均受益。可移动目标从 Role-only 中平均几乎没有收益（−0.02），但在联合组合后提升 1.49，说明两个阶段不必对同一类别组产生相同贡献。

增益集中在 baseline 较弱的类别。低于 30% baseline IoU 的 17 个类别对平均提升 7.03；30–60% 组提升 3.82；高于 60% 的组提升 1.41。这是平均趋势，不是单调保证。交通地表是反例：相对 baseline 提升 1.26，但相对 Role-only 下降 0.17。背景/杂项平均提升 10.22，且受 OEM 强烈影响；其组内中位数只有 1.56，因此前景结果更能说明广泛语义改善。

像素转移进一步表明增益对应真实纠正。约 4.2916 亿个 baseline 错误像素变为正确，约 1.6585 亿个原本正确像素变为错误，净增约 2.6331 亿个正确赋值，修正/损害比为 2.59。这些计数对应评测图像与切片，不是独立地理样本。它们补充类别均衡的 mIoU，但不意味着每个类别或组件都提升。

### 4.6 自然域评价与范围

| 数据集 | 图像数 | Baseline | Role | View | Joint | Δ |
|---|---:|---:|---:|---:|---:|---:|
| VOC20 | 1,449 | 96.89 | 97.00 | 97.00 | **97.11** | +0.22 |
| Cityscapes | 500 | 67.90 | **72.20** | 68.72 | **72.20** | +4.29 |

Role-functional evidence 在两种自然图像评价上也有效。VOC20 从 96.89 提升到 97.11，并有小幅额外视图收益，交互在舍入后接近可加（+0.01）。Cityscapes 从 67.90 提升到 72.20，主要来自角色补充；其联合最优退化为角色化 Global 单端点，额外视图组合未超过该端点。

同图控制说明了观察构造的作用。在 Potsdam 和 Vaihingen 上，使用当前图像的四个 256 像素裁块与一个 512 像素 Global 视图时，二者均选择 Global，分别得到 58.59 和 62.33，没有额外视图收益。主表对这两个数据集改用空间对齐的邻接上下文。因此，较大的 Potsdam 与 Vaihingen 增益应归属于角色与观察协议的组合，而不是任意增加裁块。自然域结果支持角色补充的迁移性，同时表明视图组合取决于替代观察是否提供兼容证据。

全部评价使用离线选择后固定的数据集 profile，SAM3 权重冻结，不使用逐图 GT 路由。这些约束界定了证据范围：实验支持报告协议下按角色组织证据及条件化视图组合，而不是共享文本、更大视野或某个固定融合算子的普遍优越性。
'''

# English section
(KIT/"sec"/"4_experiments.tex").write_text(en_exp,encoding="utf-8",newline="\n")
main=(KIT/"main.tex").read_text(encoding="utf-8")
if '\\input{sec/4_experiments}' not in main:
    main=main.replace('\\input{sec/3_method}', '\\input{sec/3_method}\n\n\\input{sec/4_experiments}')
else:
    main=main.replace('\\input{sec/4_experiments}\n\n\\input{sec/3_method}', '\\input{sec/3_method}\n\n\\input{sec/4_experiments}')
(KIT/"main.tex").write_text(main,encoding="utf-8",newline="\n")

# Chinese section
raw=CN.read_bytes(); bom=raw.startswith(b'\xef\xbb\xbf'); text=raw.decode('utf-8-sig')
text=text.replace('*Introduction、Related Work、Method、Experiments 英文初稿的独立中文对照版。当前已整理 Introduction、Related Work 与 Method；其余章节待补。', '*Introduction、Related Work、Method、Experiments 英文初稿的独立中文对照版。当前已整理 Introduction、Related Work、Method 与 Experiments；其余章节待补。')
if '## 4. 实验' not in text:
    text=text.rstrip()+'\n\n'+cn_exp.strip()+'\n'
else:
    start=text.index('## 4. 实验'); text=text[:start]+cn_exp.strip()+'\n'
CN.write_text(text,encoding='utf-8-sig' if bom else 'utf-8',newline='\n')

mapping=ROOT/'中文论文'/'中英章节对应.md'
mt=mapping.read_text(encoding='utf-8-sig')
mt=mt.replace('| `论文中文版.md` / 实验 | `sec/4_experiments.tex` | 待整理 |', '| `论文中文版.md` / 实验 | `sec/4_experiments.tex` | 已完成 |')
mapping.write_text(mt,encoding='utf-8',newline='\n')
print('experiments written')
