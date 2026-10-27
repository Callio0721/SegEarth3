# Role–View Evidence Specialization：论文执笔交付包

快照日期：2026-09-27  
代码基线：`main@bc5a250d3d29f032d1ea461c1c4cc63134de39b9`  
任务：Training-Free Open-Vocabulary Semantic Segmentation for Remote Sensing Images

## 1. 先读什么

建议按以下顺序接手，不要从旧英文初稿直接开始改：

1. [执笔者任务书](00_开始阅读/执笔者任务书.md)：十分钟理解论文要写什么、不能写什么。
2. [最新事实口径](00_开始阅读/最新事实口径.md)：所有数字和比较口径的优先级。
3. [最终方法规范](02_方法与实现/最终方法规范.md)：理论描述必须与当前代码一致。
4. [主实验与消融事实表](03_实验与证据/主实验与消融事实表.md)：可直接用于论文的结果、消融和边界。
5. [论点—证据—边界](03_实验与证据/论点_证据_边界.md)：每个核心 claim 有什么证据、不能外推到哪里。
6. [相关工作阅读路线](04_相关工作/阅读路线.md)：先读最接近的工作，再读写法参考。
7. [论文结构与写作蓝图](01_论文主线与初稿/02_CVPR论文结构与写作蓝图.md)：章节和图表安排。
8. `英文参考初稿.md` / `中文参考初稿.md`：作为措辞素材，不是最终事实源。

## 2. 当前论文的一句话主线

> A shared concept anchors category semantics, while useful supplementary evidence depends on both the responsibility of the SAM3 readout and the visual observation from which it is grounded.

中文：SAM3 的统一 concept 保留类别语义共识，但 Presence、Semantic 与 Instance 对补充信息具有不同的功能需求；这些补充信息能否发挥作用，又取决于可见的视觉范围。我们在不训练、不拆解原生 grounding 的前提下，按角色组织语言补充，并联合 Local/Global 观察形成互补证据。

## 3. 三个最重要的数字

- 八个遥感数据集配对基准：`53.564` mIoU。
- Role-Functional Text：`55.818`，相对基准 `+2.254`，`8/8` 数据集为正。
- Joint Role–View：`57.487`，相对基准 `+3.923`，相对 Role-only `+1.669`，`8/8` 数据集为正。

固定最终配置的四格 factorial 口径为：Baseline `53.564`、Role `55.674`、View `54.751`、Joint `57.487`，平均 interaction `+0.626`，`6/8` 为正。不要用独立挑选的 Role-only 宏平均 `55.818` 代替四格中的 `55.674`。

## 4. 必须保留的协议说明

- 主表使用原始 Joint 协议。Potsdam / Vaihingen 的 512×512 目标块利用同一原始场景的相邻 RGB tile 重建 1024×1024 对齐上下文；只在目标区域评价，不使用相邻 GT。
- 同图 256/512 控制实验是辅助结果：这两个数据集最终均退化为 Global endpoint，不能替换主表。
- Profile 是验证集上从已测试候选中选出的可执行配置；不要描述成模型自动推断的通用路由器。
- 当前方法保持 SAM3 原生完整 grounding 和每个视图内的 `Presence × max(Semantic, Instance)`；View 融合发生在对齐后的类别分数图上。

## 5. 文件夹说明

| 目录 | 用途 |
|---|---|
| `00_开始阅读/` | 事实口径、任务书和完整 `state.md` 快照 |
| `01_论文主线与初稿/` | CVPR 写作蓝图、参考初稿、20/50篇写法研究 |
| `02_方法与实现/` | 最终方法规范、实验沿革、代码入口 |
| `03_实验与证据/` | 主结果、interaction、消融、可编辑 CSV/JSON 和论文图 |
| `04_相关工作/` | 核心论文 PDF、阅读路线、引用账本和 BibTeX |
| `05_图表与汇报/` | PPT、Word 说明和三版方法架构图 |
| `06_复现与来源索引/` | 源码、配置、日志来源与复现命令，不复制大日志 |
| `07_待办与限制/` | 写作前最小待补项、旧稿审阅记录 |

## 6. 事实源优先级

出现冲突时按以下顺序处理：

1. 本包 `最新事实口径.md` 与 `state_事实源快照_2026-09-27.md`；
2. `可编辑数据/main_results.csv`、`matched_interactions.csv` 等精确数据；
3. 真实日志路径和当前源码；
4. 2026-09-05 的中英文参考初稿；
5. 历史 PPT 中的四舍五入展示值。

旧稿可复用叙事和句式，但其中任何数字、SOTA 判断或绝对性表述都必须按本包事实重新核对。

## 7. 本包不包含什么

- 不复制完整 `logs/`、数据集、权重或 checkpoint；它们体量大，且论文执笔者只需来源索引。
- 不复制整个源码；当前仓库本身才是唯一代码事实源，避免副本漂移。
- 不复制 `Astra_docs/_work/`、PDF 抽取文本、页面截图等中间缓存。
- 不把已关闭实验包装成第三个贡献；它们只用于解释设计选择和 limitation。

