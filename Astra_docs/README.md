# Astra：研究接手与 CVPR 写作工作区

日期：2026-09-05。

本工作区已经从项目接手推进到 **Related Work / Method / Experiments 的英文初稿与独立中文对照**。**原有代码、`state.md`、PPT、参考论文和日志均未修改。** 所有结果来自既有实验，不包含新推理。

## 先读本轮交付

1. [英文论文初稿](manuscript_v1/English_draft.md)：三个章节的实际正文，含五张真实结果表、九个编号公式及待补图注。
2. [独立中文对照](manuscript_v1/Chinese_draft.md)：与英文共享术语、公式、表格和证据边界。
3. [补充表与已选配置](manuscript_v1/Additional_tables.md)：全部配置、Residual/Direct、18组同文本用途对照及缺失对照的空位。
4. [写作审阅与待补项](manuscript_v1/写作审阅与待补项.md)：本版判断、落版安排、少量待补证据，以及集中说明的数值/引用注意点。
5. [正文参考文献](manuscript_v1/references.md) · [BibTeX](manuscript_v1/references.bib)：正文实际使用的23篇来源。
6. [50篇CVPR写法阅读记录](CVPR50写法研究/阅读记录.md)：2025/2026主会各25篇，逐篇结构与图表分析；[来源表](CVPR50写法研究/sources.csv) · [50篇BibTeX](CVPR50写法研究/cvpr50.bib)。

50篇的官方页面、PDF、文本与代表页检查文件保存在 `_work/cvpr50/`。它们是写法学习语料，不是要求全部引用进正文。

## 接手阶段的认识与证据

需要回查研究背景时再阅读：

1. [项目认识与投稿判断](01_项目认识与投稿判断.md)：目前真正做成了什么，贡献应如何界定，本轮发现哪些需要收紧的旧结论。
2. [CVPR 论文结构与写作蓝图](02_CVPR论文结构与写作蓝图.md)：八页安排、章节逻辑、理论支撑、真实表格、主图和定性图安排，以及初稿推进顺序。
3. [证据账本与最小补充清单](03_证据账本与最小补充清单.md)：论文—代码—实验对照、关键文献实际方法、少量必要补充与待同步记录。

## 本轮固定的主结果

- 遵循用户决定，八个遥感数据集的主方法平均 mIoU 保留 **57.49**。
- Potsdam / Vaihingen 主结果包含来自同一原始场景的邻接 RGB 上下文；当前单图控制是辅助实验，不替换主表。
- 同次日志的宏平均为 Baseline **53.56** → Role-only **55.82** → Joint **57.49**。
- 上述配对消融基准与用户指定的对外比较表 Baseline **53.5** 是不同记录口径，不能混算或静默覆盖。
- 暂不新增贡献，也不重新打开已关闭的研究方向。

## 数据与工作文件

`evidence/` 保存从现有 CSV 重组的数据，不包含新推理结果：

- `main_results.csv`：八数据集的已选 Baseline / Role / Joint、配置及来源。
- `matched_interactions.csv`：固定最终配置的四格 Role×View 对照。
- `shared_vs_role_text.csv`：后期 18 个共享补充文本与单独 Semantic 补充对照。
- `selected_profiles.csv`：相关三个实验汇总中的 profile 行，含原文件路径。
- `statistics.json`：从未舍入数据计算的宏平均与计数。

`_work/` 是隔离的阅读缓存：论文抽取文本、结构目录、抽样页面预览、PPT 文本和数据整理脚本。不是交付论文，也不需要上传服务器。重算上述证据表可在项目根目录执行：

```bash
PYTHONDONTWRITEBYTECODE=1 python Astra_docs/_work/build_evidence.py
```

本轮不提交 GitHub、不刷新原知识图谱、不复制文件到服务器。
