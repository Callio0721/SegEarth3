# 参考文献核验记录（2026-10-20）

## 范围与结论

- 正文参考文献由 28 条扩展到 51 条（R01–R51）。
- 英文 `references.tex`、`main.bib` 与中文 `参考文献.md`、`references.bib` 均为 51 条。
- 全稿实际引用 51 条：无未使用条目，无未定义 key。
- 本地 `参考论文` 目录中有 29 条工作直接进入当前稿；其余工作与本文论证不直接对应，未为凑数加入。

## 新增文献与用途

| Key | 文献 | 核验来源 | 正文用途 |
|---|---|---|---|
| R29 | SCLIP, ECCV 2024 | DOI `10.1007/978-3-031-72664-4_18` | Related Work、表 1 |
| R30 | ClearCLIP, ECCV 2024 | DOI `10.1007/978-3-031-72970-6_9` | Related Work、表 1 |
| R31 | ProxyCLIP, ECCV 2024 | DOI `10.1007/978-3-031-73113-6_5` | Related Work、表 1 |
| R32 | VIP, ICML 2026 | arXiv `2605.12325`；arXiv 页面注明 ICML 2026 接收 | 表 1 |
| R33 | RSCLIP, IEEE JSTARS 2026 | DOI `10.1109/JSTARS.2026.3688939` | 表 1 |
| R34 | CorrCLIP, ICCV 2025 | DOI `10.1109/ICCV51701.2025.02288` | 表 1 |
| R35 | ActiveSAM, arXiv 2026 | arXiv `2606.16996` | Related Work、表 1 |
| R36 | LoveDA, NeurIPS D&B 2021 | 官方 NeurIPS 论文 URL | 4.1 数据集引用 |
| R37 | iSAID, CVPRW 2019 | arXiv `1905.12886`；页面注明 CVPRW | 4.1 数据集引用 |
| R38 | OpenEarthMap, WACV 2023 | DOI `10.1109/WACV56688.2023.00619` | 4.1 数据集引用 |
| R39 | UAVid, ISPRS JPRS 2020 | DOI `10.1016/j.isprsjprs.2020.05.009` | 4.1 数据集引用 |
| R40 | UDD5, PRCV 2018 | DOI `10.1007/978-3-030-03398-9_30` | 4.1 数据集引用 |
| R41 | VDD, JVCIR 2025 | DOI `10.1016/j.jvcir.2025.104429` | 4.1 数据集引用 |
| R42 | ISPRS Potsdam/Vaihingen benchmark | 官方 benchmark 页面 | 4.1 数据集引用 |
| R43 | Cityscapes, CVPR 2016 | DOI `10.1109/CVPR.2016.350` | 4.1 数据集引用 |
| R44 | PASCAL VOC, IJCV 2010 | DOI `10.1007/s11263-009-0275-4` | 4.1 数据集引用 |
| R45 | GroupViT, CVPR 2022 | DOI `10.1109/CVPR52688.2022.01760` | Related Work |
| R46 | OVSeg, CVPR 2023 | DOI `10.1109/CVPR52729.2023.00682` | Related Work |
| R47 | ResCLIP, CVPR 2025 | DOI `10.1109/CVPR52734.2025.02789` | Related Work |
| R48 | CAT-Seg, CVPR 2024 | DOI `10.1109/CVPR52733.2024.00394` | Related Work |
| R49 | SED, CVPR 2024 | DOI `10.1109/CVPR52733.2024.00329` | Related Work |
| R50 | AVION, CVPR 2026 | CVF 官方论文页 | Related Work |
| R51 | The Power of Prior, CVPR 2026 | CVF 官方论文页 | Related Work |

## 本轮纠正的书目问题

- OpenEarthMap 页码采用 Crossref 记录 `6243--6253`。
- UDD5 作者采用 Crossref 记录：Yu Chen, Yao Wang, Peng Lu, Yisong Chen, Guoping Wang。
- VDD 使用 2025 年 JVCIR 正式期刊版本，不优先引用 2023 预印本。
- VIP 使用 ICML 2026 接收信息；ActiveSAM 保持 arXiv 预印本标记。
- `Stage` 是本文消融阶段，不是外部论文中的方法，因此没有添加伪造引用；表注明确指向第 3 节配置。

## 编译与版面检查

- 完整英文稿使用 MiKTeX `pdflatex` 连续编译两遍通过。
- `main.log` 无 Overfull/Underfull box，无 undefined citation。
- 表序：Table 1 → 2 → 3 → 4 → 5。\n- 表 1 的列标题、表 3–5 的 Dataset 行均已直接加入数据集引用。
- 图序：Figure 1 → 2 → 3 → 4 → 5。
- 公式 (2)、(5)、(6)、(10) 已改为 `aligned` 多行结构。
- Figure 5 仍是明确的定性结果占位，不是实际预测。

