"""Build manuscript companion tables from existing results; no model execution."""
from pathlib import Path
from decimal import Decimal, ROUND_HALF_UP
import csv

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'Astra_docs/manuscript_v1/Additional_tables.md'
NAMES = dict(potsdam='Potsdam', vaihingen='Vaihingen', loveda='LoveDA',
             isaid='iSAID', openearthmap='OEM', uavid='UAVid', udd5='UDD5', vdd='VDD')
ORDER = list(NAMES)

def rows(path):
    with (ROOT/path).open(newline='') as stream:
        return list(csv.DictReader(stream))

def num(value, signed=False):
    d=Decimal(str(value)).quantize(Decimal('.01'), rounding=ROUND_HALF_UP)
    return (('+' if d >= 0 else '−') + f'{abs(d):.2f}') if signed else f'{d:.2f}'

def table(head, body):
    lines=['| '+' | '.join(head)+' |', '| '+' | '.join(['---']+['---:']*(len(head)-1))+' |']
    lines += ['| '+' | '.join(map(str,row))+' |' for row in body]
    return '\n'.join(lines)+'\n\n'

main = rows('Astra_docs/evidence/main_results.csv')
by_dataset = {r['dataset']:r for r in main}
text = [r'''# Supplementary Tables and Configuration Notes / 补充表与配置说明

本文件服务于中英文初稿的复现细节与补充材料，不是新增主文章节。所有数值来自已经完成的实验；“—”保持为空，不由其他实验推算。显示使用四舍五入到两位小数，差值先用未舍入数据计算。

## Appendix A. Selected configuration / 已选配置

**Table A1. Fixed configurations for the main JRV results.** P/S/I index the recorded role prompt bank. Zero retains the canonical anchor; the same selected triple is used in both view families. Native admission uses updated presence; anchor admission uses anchor presence for query membership. All main rows use the anchor-preserving strategy with α = 0.5 and τ = 0.25.

''']
text.append(table(['Dataset','P/S/I','Query admission','View operator','Global weight','Joint mIoU'],[
    [NAMES[r['dataset']],r['joint_slots'].replace('+',' / '),
     'Anchor' if r['admission']=='anchor_admission' else 'Native',
     r['operator'].split('_')[0],
     {'linear_g075':'0.75','linear_g050':'0.50','power4_g075':'0.75',
      'logit_g075':'0.75','logit_g050':'0.50','max':'—'}[r['operator']], num(r['joint'])]
    for r in main]))
text.append(r'''### View composition definitions

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

''')
text.append(table(['Dataset','Baseline','Best Role-only','Joint','Role − baseline','Joint − Role'],[
    [NAMES[r['dataset']],num(r['baseline']),num(r['role_only']),num(r['joint']),
     num(r['role_gain'],True),num(r['joint_over_role'],True)] for r in main]+[
    ['Average']+[num(sum(float(r[k]) for r in main)/8,k in ('role_gain','joint_over_role'))
                 for k in ('baseline','role_only','joint','role_gain','joint_over_role')]]))
text.append(r'''结果来源及未舍入数值：[main_results.csv](../evidence/main_results.csv)。正文匹配四格的 Role 平均是 **55.67**，本表独立最优 Role 平均是 **55.82**；不能互换。

## Appendix B. Structural alternatives and observation extent / 结构替代与观察范围

**Table B1. Direct prediction versus the anchor-preserving strategy.** The final role, admission and view settings are fixed within a row. “Direct” uses candidate role values directly and does not retain the official-score compensation of Equation (6). Thus this compares two complete update strategies; it does not isolate clipping or residual strength. iSAID and UAVid are not included in the completed six-dataset finalization comparison.

''')
direct = rows('logs/joint_role_view_final_v1_full_f332bdb/summary/final_profiles.csv')
db={(r['dataset'],r['profile']):r for r in direct}
b=[]
for ds in ORDER:
    d=db.get((ds,'joint_direct'));r=db.get((ds,'joint_residual'))
    b.append([NAMES[ds],num(d['miou']) if d else '—',num(r['miou']) if r else '—',
              num(float(r['miou'])-float(d['miou']),True) if d and r else '—'])
text.append(table(['Dataset','Direct','Anchor-preserving','Anchor-preserving − Direct'],b))
text.append(r'''Source: [final_profiles.csv](../../logs/joint_role_view_final_v1_full_f332bdb/summary/final_profiles.csv), rows `joint_direct` and `joint_residual`. Residual is better on five of six completed datasets. VDD's Direct score is a genuine completed alternative, but does not replace the fixed main-method result.

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

''')
shared=rows('Astra_docs/evidence/shared_vs_role_text.csv')
text.append(table(['Dataset','Candidate','Baseline','Semantic-only','Shared P/S/I','Semantic-only − Shared'],[
    [NAMES[r['dataset']],'S'+r['semantic_slot'],num(r['baseline']),num(r['semantic_only']),
     num(r['same_text_all_roles']),num(r['semantic_only_minus_shared'],True)] for r in shared]))
text.append(r'''Source: [shared_vs_role_text.csv](../evidence/shared_vs_role_text.csv), preserving the original variant/source identifiers. Semantic-only is better in 13/18 settings; shared use is positive over the baseline in 7/18 settings. UDD5–S3 is an important opposite case: shared supplementation obtains 73.04, so the data do not justify “shared descriptions always harm grounding.” This diagnostic is not used to silently replace the agreed main-result registry.

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
''')
OUT.write_text(''.join(text),encoding='utf-8')
print(OUT)
