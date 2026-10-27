# 论文写作与类别证据

更新：2026-09-03。这里是唯一持续修订的论文框架工作目录；文件名不因每次讨论重复增加“最终版”。

## 先读三份文档

1. [论文主线与方法实验写作稿](论文主线与方法实验写作稿.md)：论文应该怎么讲；含真实主表/消融表。较长理论推导已移到文末补充候选。
2. [引用与论点对照](引用与论点对照.md)：我们写的外部论点由哪篇论文、哪个模块/章节支持。
3. [20 篇 CVPR 论文结构与图表阅读](20篇CVPR论文结构与图表阅读.md)：学习文章组织；原 20 篇记录保留，末尾增加 GLA-CLIP、PEARL 和 Findings 的 OV-Stitcher。

## 每个文件的用途

| 文件 | 具体用途 | 什么时候使用 |
|---|---|---|
| `README.md` | 本目录导航与统计口径 | 初次打开目录 |
| `论文主线与方法实验写作稿.md` | Related Work、Method、Experiments 的行文主稿；真实数据表、图表分工和最必要待补证据 | 写论文/讨论叙事时主要修改它 |
| `20篇CVPR论文结构与图表阅读.md` | 论文怎样提出问题、安排模块和验证；包含直接 OVSS 和相邻任务写法参照 | 想知道某种结构为什么值得借鉴 |
| `引用与论点对照.md` | claim→paper→section 对照、作者/出处/本地原文位置 | 每次引用前核对，防止套引用 |
| `论文引用.bib` | C01–C20、R01–R10 共 30 条可供使用的 BibTeX | 后续 LaTeX 排版；不要求全引用 |
| `cvpr20_sources.json` | 原 20 篇 CVF 元数据与本地 PDF 路径 | 机器检索/核对原阅读样本；不是论文正文 |
| `category_class_data.csv` | 八遥感数据集 63 个类别对的 Baseline/Role/Joint IoU、变体和来源 | 检查某类的实际涨跌 |
| `category_group_summary.csv` | 七个语义组的均值、中位数、正提升数量 | 柱状图数值及正文类别结论 |
| `category_statistics.json` | 类别分组映射、统计定义和源文件哈希 | 确认分组与数据溯源 |
| `matched_role_view_interactions.csv` | 固定 Joint 文本/算子的 Baseline、Role、View、Joint 四路及 Γ | 解释真正的 Role×View interaction |
| `build_category_figures.py` | 从已有结果重建类别组图的本地脚本 | 需要重新出图时；不运行 SAM3 |

原 `cvpr20_references.bib` 已并入并更名为 `论文引用.bib`，不保留重复引用库。其他数据文件各有独立用途，未删除或改写实验数值。

## 当前论文图

[PDF](../../../output/pdf/category_evidence_20260903/category_structured_gains.pdf) · [SVG](../../../output/pdf/category_evidence_20260903/category_structured_gains.svg) · [PNG](../../../output/pdf/category_evidence_20260903/category_structured_gains.png)

图仅有七个语义组、Role Text 和 Role Text + View 两种相对 baseline 的增益柱。保留全部 55 个前景、8 个背景/杂类类别对，包括负增益。旧散点图保留作分析记录，不再是正文推荐主图。

**统计口径：** 类别组按类别对等权，不是八数据集 macro；Joint−最佳 Role 是阶段变化，不是 Γ。交互只用匹配四路 CSV。主表保留用户 PPT p16 数值，其他表由精确日志计算后显示两位小数。

本地复画（已有 NumPy、Matplotlib 环境）：

```bash
cd /Users/pengjunhao/Desktop/SegEarth3
MPLCONFIGDIR=/tmp/segearth-paper-mpl python docs/论文框架/2026-09-03/build_category_figures.py
```

## 范围与状态

- 最新方法/实验状态：[state.md](../../../state.md)；历史试错：[研究记录](../../研究记录/实验沿革与实现记录.md)。
- Potsdam/Vaihingen 单图对照已完成，最佳退回Global，58.59/62.33；[结果分析](../../研究记录/2026-09-04_单图Role-View实验分析.md)。本目录原图表仍记录历史邻域协议，未静默替换数值。
- 投稿时间：[CVPR 官方核验](../CVPR投稿时间线.md)，与方法文稿分开维护。
- 本轮只修改本地研究文档、引用与导航，不修改模型/实验脚本、不改 PPT、不发起 GPU 推理。无需同步服务器。
