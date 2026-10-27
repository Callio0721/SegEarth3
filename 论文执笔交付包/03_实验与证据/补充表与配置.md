# Supplementary Tables and Configuration Notes / 补充表与配置说明

本文件服务于中英文初稿的复现细节与补充材料，不是新增主文章节。所有数值来自已经完成的实验；“—”保持为空，不由其他实验推算。显示使用四舍五入到两位小数，差值先用未舍入数据计算。

## Appendix A. Selected configuration / 已选配置

**Table A1. Fixed configurations for the main JRV results.** P/S/I index the recorded role prompt bank. Zero retains the canonical anchor; the same selected triple is used in both view families. Native admission uses updated presence; anchor admission uses anchor presence for query membership. All main rows use the anchor-preserving strategy with α = 0.5 and τ = 0.25.

| Dataset | P/S/I | Query admission | View operator | Global weight | Joint mIoU |
| --- | ---: | ---: | ---: | ---: | ---: |
| Potsdam | 1 / 2 / 0 | Anchor | linear | 0.75 | 63.18 |
| Vaihingen | 0 / 3 / 2 | Native | max | — | 66.38 |
| LoveDA | 1 / 1 / 0 | Native | max | — | 48.81 |
| iSAID | 0 / 3 / 0 | Native | logit | 0.50 | 29.13 |
| OEM | 0 / 3 / 2 | Native | linear | 0.50 | 53.08 |
| UAVid | 2 / 3 / 1 | Native | power4 | 0.75 | 59.82 |
| UDD5 | 2 / 2 / 1 | Native | logit | 0.75 | 72.94 |
| VDD | 2 / 1 / 0 | Native | logit | 0.50 | 66.55 |

### View composition definitions

For aligned continuous scores \(L_c(x),G_c(x)\), let \(g\) be the Global weight. The tested fixed operators are:

\[
\begin{aligned}
\Psi_{\max}(L,G)&=\max(L,G),\\
\Psi_{\rho,g}(L,G)&=\big((1-g)L^\rho+gG^\rho\big)^{1/\rho},\\
\Psi_{\mathrm{logit},g}(L,G)&=\sigma\big((1-g)\operatorname{logit}(L)+g\operatorname{logit}(G)\big).
\end{aligned}
\]

Here ρ = 1 gives a linear mean; ρ = 2 or 4 gives a power mean. Logit inputs are clipped to [ε, 1−ε], with ε = 10⁻⁶. The screen used g ∈ {0.25, 0.50, 0.75}, along with Local and Global endpoints and element-wise maximum. This is 13 mixed operators plus two endpoints. A name such as `power4_g075` therefore means a fourth-power mean with 75% Global weight. These operators combine complete class-score fields after grounding; they are not different operators assigned to P, S and I separately.

配置中的 `linear`、`logit`、`power4` 都是最后两类视图分数的组合；不要把旧图示解读为每个 head 内部各自执行不同融合。它们不是方法的三个新子模块。

### Role prompt source and examples

The role bank contains a candidate phrase for each dataset category and role index. One selected index is shared across categories, but its actual phrase is category-specific. For example, Potsdam's `S2` maps road to “continuous road surface”; it does not send that sentence to all categories.

- 原六数据集提示库：[role_functional_text_v2](../../configs/prompt_banks/role_functional_text_v2/)。
- iSAID、UAVid：[role_functional_text_v3](../../configs/prompt_banks/role_functional_text_v3/)。
- 真实示例：[potsdam.json](../../configs/prompt_banks/role_functional_text_v2/potsdam.json) 中 road 的 anchor 是 `road`；P1 是 `roads`；S2 是 `continuous road surface`；I1 候选是 `complete connected road network`。最终 Potsdam 用 P1/S2/I0，所以 I1 只能用作候选示例。
- LLM 的现有生成记录标注为 Codex；文稿不补写未记录的 Qwen/GPT 具体模型版本、temperature 或 seed。投稿补充材料应附实际候选文本与已选描述，不能重新生成后当作当时的实验输入。

**Table A2. Best completed component results.** Each component can have its own selected configuration. This table measures the best recorded stage performance; it is not used to compute factorial interaction.

| Dataset | Baseline | Best Role-only | Joint | Role − baseline | Joint − Role |
| --- | ---: | ---: | ---: | ---: | ---: |
| Potsdam | 57.87 | 58.59 | 63.18 | +0.73 | +4.59 |
| Vaihingen | 60.86 | 62.33 | 66.38 | +1.47 | +4.05 |
| LoveDA | 47.34 | 48.30 | 48.81 | +0.96 | +0.50 |
| iSAID | 27.64 | 28.27 | 29.13 | +0.63 | +0.86 |
| OEM | 44.30 | 50.53 | 53.08 | +6.23 | +2.55 |
| UAVid | 54.58 | 59.51 | 59.82 | +4.92 | +0.31 |
| UDD5 | 71.80 | 72.89 | 72.94 | +1.08 | +0.06 |
| VDD | 64.11 | 66.12 | 66.55 | +2.01 | +0.44 |
| Average | 53.56 | 55.82 | 57.49 | +2.25 | +1.67 |

结果来源及未舍入数值：[main_results.csv](../evidence/main_results.csv)。正文匹配四格的 Role 平均是 **55.67**，本表独立最优 Role 平均是 **55.82**；不能互换。

## Appendix B. Structural alternatives and observation extent / 结构替代与观察范围

**Table B1. Direct prediction versus the anchor-preserving strategy.** The final role, admission and view settings are fixed within a row. “Direct” uses candidate role values directly and does not retain the official-score compensation of Equation (6). Thus this compares two complete update strategies; it does not isolate clipping or residual strength. iSAID and UAVid are not included in the completed six-dataset finalization comparison.

| Dataset | Direct | Anchor-preserving | Anchor-preserving − Direct |
| --- | ---: | ---: | ---: |
| Potsdam | 56.17 | 63.18 | +7.01 |
| Vaihingen | 54.69 | 66.38 | +11.70 |
| LoveDA | 30.99 | 48.81 | +17.81 |
| iSAID | — | — | — |
| OEM | 39.37 | 53.08 | +13.70 |
| UAVid | — | — | — |
| UDD5 | 71.24 | 72.94 | +1.70 |
| VDD | 67.26 | 66.55 | −0.71 |

Source: [final_profiles.csv](../../logs/joint_role_view_final_v1_full_f332bdb/summary/final_profiles.csv), rows `joint_direct` and `joint_residual`. Residual is better on five of six completed datasets. VDD's Direct score is a genuine completed alternative, but does not replace the fixed main-method result.

**Table B2. Target-tile-only observation control.** The main protocol uses a 512-pixel target and aligned 1,024-pixel same-scene RGB context. The target-only control instead uses the 512-pixel target as Global and four 256-pixel crops as Local. Profiles were compared within each condition. The control changes both available field of view and effective resolution; it is not a pure single-factor test of neighboring RGB access.

| Observation configuration | Potsdam | Vaihingen |
|---|---:|---:|
| Baseline on the 512-pixel target | 57.87 | 60.86 |
| Best Role-only on that target | 58.59 | 62.33 |
| Best actual two-view mixture within the target | 58.43 | 61.65 |
| Best target-only configuration, endpoints allowed | 58.59 | 62.33 |
| Main JRV with wider same-scene context | 63.18 | 66.38 |

The target-only Local/Global realization does not improve the best Role-only endpoint on either dataset. This supports the importance of useful observation extent in the main result, not a claim that adding any extra crop is beneficial. Source: [completed control report](../../docs/研究记录/2026-09-04_单图Role-View实验分析.md) and [profile CSV](../../logs/joint_role_view_single_image_v1_full_bc5a250/summary/joint_role_view_profiles.csv).

## Appendix C. Complete shared-description control / 全部同文本用途对照

**Table C1. Semantic-only use versus shared P/S/I use of the same candidate.** Both strategies use bounded anchor-relative supplementation. All 18 available dataset–candidate settings are included. These are semantic-oriented candidates; the table alone does not test every possible shared phrase or every role permutation.

| Dataset | Candidate | Baseline | Semantic-only | Shared P/S/I | Semantic-only − Shared |
| --- | ---: | ---: | ---: | ---: | ---: |
| Potsdam | S1 | 57.87 | 57.08 | 55.49 | +1.59 |
| Potsdam | S2 | 57.87 | 58.00 | 56.63 | +1.38 |
| Potsdam | S3 | 57.87 | 57.77 | 57.98 | −0.21 |
| Vaihingen | S1 | 60.86 | 59.67 | 58.35 | +1.31 |
| Vaihingen | S2 | 60.86 | 60.18 | 59.18 | +1.00 |
| Vaihingen | S3 | 60.86 | 61.57 | 61.28 | +0.29 |
| LoveDA | S1 | 47.34 | 48.09 | 46.61 | +1.48 |
| LoveDA | S2 | 47.34 | 47.02 | 44.48 | +2.54 |
| LoveDA | S3 | 47.34 | 47.14 | 45.81 | +1.33 |
| OEM | S1 | 44.30 | 44.79 | 42.46 | +2.33 |
| OEM | S2 | 44.30 | 44.95 | 43.35 | +1.60 |
| OEM | S3 | 44.30 | 46.28 | 44.02 | +2.26 |
| UDD5 | S1 | 71.80 | 61.83 | 62.11 | −0.28 |
| UDD5 | S2 | 71.80 | 72.63 | 72.85 | −0.22 |
| UDD5 | S3 | 71.80 | 71.56 | 73.04 | −1.48 |
| VDD | S1 | 64.11 | 65.27 | 65.05 | +0.22 |
| VDD | S2 | 64.11 | 64.39 | 64.24 | +0.16 |
| VDD | S3 | 64.11 | 65.25 | 65.76 | −0.51 |

Source: [shared_vs_role_text.csv](../evidence/shared_vs_role_text.csv), preserving the original variant/source identifiers. Semantic-only is better in 13/18 settings; shared use is positive over the baseline in 7/18 settings. UDD5–S3 is an important opposite case: shared supplementation obtains 73.04, so the data do not justify “shared descriptions always harm grounding.” This diagnostic is not used to silently replace the agreed main-result registry.

## Appendix D. Reserved controls / 尚待补齐的核心对照

These entries are intentionally empty. They are proposed controls, not measured failures. Their purpose is to distinguish role-sensitive information use from a generic benefit of more prompts and predictions. Fix the candidate pool, anchor and view condition within each comparison.

**Table D1. Prompt-information use controls (not yet available as a matched final-method comparison).**

| Information use | Potsdam | Vaihingen | LoveDA | iSAID | OEM | UAVid | UDD5 | VDD |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Role-agnostic use of the same final candidate pool | — | — | — | — | — | — | — | — |
| Fixed role permutation with the same candidate set | — | — | — | — | — | — | — | — |
| Complete-prediction ensemble of the same prompts | — | — | — | — | — | — | — | — |

优先补第一行与第三行所对应的一个紧凑匹配对照；不需将其扩展为新的大搜索。已有表 C 的 18 组结果能够支持“用途会改变效果”，但不完全等价于“相同最终信息量下，专门化优于任意普通多提示集成”。固定角色置换可作为这一对照的诊断列，而不必独立形成新方向。

**Qualitative figure slots.** Reserve real, aligned predictions rather than synthesized segmentation examples:

| Panel | Purpose | Required predictions | Current figure status |
|---|---|---|---|
| OEM | Strong Role benefit and positive interaction | RGB, GT, B, matched R, matched V, J | — |
| UAVid or LoveDA | View becomes useful after Role supplementation | RGB, GT, B, matched R, matched V, J | — |
| Vaihingen | Strongest measured matched interaction | RGB, GT, B, matched R, matched V, J | — |
| iSAID or UDD5 | Positive total gain with overlapping component gains | RGB, GT, B, matched R, matched V, J | — |

这里的 “—” 表示本稿尚未放入核对过的对应版式，不是宣称没有任何历史可视化。仅当固定 profile、同图坐标和输出身份核对一致后，才使用已有图；否则保留占位。不要从聚合 IoU 推画具体边界修复。

## Source map / 数值来源

主表及 A2：[main_results.csv](../evidence/main_results.csv)；正文交互：[matched_interactions.csv](../evidence/matched_interactions.csv)；自然域：[VOC20](../../logs/domain_extension_joint_profile_v1_full_462ef8c_voc20/summary/joint_role_view_profiles.csv)、[Cityscapes](../../logs/domain_extension_joint_profile_v1_full_462ef8c_cityscapes/summary/joint_role_view_profiles.csv)；类别组：[category_group_summary.csv](../../docs/论文框架/2026-09-03/category_group_summary.csv)。每个数值表均为本地既有结果的整理，不增加推理。
