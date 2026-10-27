# Research State

> 本文件是项目的当前事实源。优先记录可复现实验、已形成的方法逻辑、明确关闭的方向与下一步；旧对话中的过程细节仅在仍影响决策时保留。

- Last updated: 2026-09-27
- Local repository: `/Users/pengjunhao/Desktop/SegEarth3`
- Remote server: `/home/PengJunhao/workspace/SegEarth-OV-3`
- GitHub: `ssh://git@ssh.github.com:443/pengjunhao621-arch/SegEarth3.git`
- Branch: `main`
- Main task: training-free open-vocabulary semantic segmentation for remote-sensing images with SegEarth-OV3/SAM3

## 1. Current Snapshot

### 1.1 Current method

Working name: **Role–View Evidence Specialization**.

The method has two connected parts:

1. **Role-Functional Text**: preserve the official class name/alias as a shared ontology anchor, and add bounded supplementary text evidence separately to Presence, Semantic and Instance according to their computational responsibilities.
2. **Joint Role–View Profile**: use aligned Native/Local and Context/Global observations, each completing frozen SAM3 grounding, then jointly select the role-text/view evidence profile that fits the dataset.

The method does not retrain SAM3, split its shared grounding into isolated heads, or replace the native `Presence × max(Semantic, Instance)` decision chain.

### 1.2 Evidence status

- Role-only is positive over the matched baseline on all eight reproduced remote-sensing datasets.
- The user confirmed on 2026-09-04 that the original eight-dataset Joint Role–View protocol remains the main result: macro57.487, displayed as57.49. Potsdam/Vaihingen use neighbor context. The completed current-image-only experiment is an auxiliary control: both select Global and retain Role-only results (58.594/62.333), with no additional View gain (§5.8); it does not replace main-table results.
- Natural-domain evaluation is complete. Cityscapes shows a strong Role-Text gain while its selected View profile degenerates to Global; VOC20 shows smaller but near-additive positive Role and View gains under a high baseline ceiling.

### 1.3 Claim boundary

Supported:

> A single SAM3 concept preserves shared category semantics, but its Presence, Semantic and Instance readouts have heterogeneous information needs. In remote sensing, those needs are also coupled to observation scale and field of view. Preserving native grounding while specializing supplementary language and visual evidence improves segmentation across datasets.

Not supported:

- one universal prompt works for every remote-sensing dataset;
- every role must always receive non-anchor text;
- one fixed Local/Global operator works on every dataset;
- SAM3's native max fusion is itself the main error source;
- internal confidence/affinity alone can reliably correct errors;
- validation-selected profiles are automatically inferred universal rules.

## 2. Fixed Comparison Protocol

For future paper tables, slides and discussions comparing the reproduced SegEarth-OV3 baseline with ProC-SAM3, use this user-approved one-decimal table. Baseline numbers are matched local reproductions; ProC-SAM3 numbers come from its official paper.

| Method | Potsdam | Vaihingen | LoveDA | iSAID | OEM | UAVid | UDD5 | VDD | Avg. |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Baseline | 57.8 | 60.8 | 47.4 | 27.6 | 44.3* | 54.7 | 71.7 | 64.1* | 53.5 |
| ProC-SAM3 | 58.8 | 64.5 | 46.1 | 29.5 | 48.9 | 60.0 | 73.4 | 67.5 | 56.1 |

The asterisks on OEM and VDD are retained exactly as specified by the user. Full-precision matched numbers below may be used for causal analysis, but must not replace this external-comparison table silently.

Main-method protocol confirmed by the user (2026-09-04): use §5.3's original Joint results and **57.49** eight-dataset macro in subsequent main tables, slides and manuscript statistics. In experimental details, state that Potsdam/Vaihingen reconstruct spatially aligned1024×1024 RGB context around a512×512 target from neighboring tiles of the same original scene; predictions are evaluated on the target region, without neighboring GT. This is context from the original large image, not a claim that the entire original orthomosaic is fed into SAM3 at once. The baseline sees the isolated target tile, so the larger observation scope must remain explicit. Keep §5.8 as an auxiliary same-image control, not an alternative main table.

## 3. Baseline: SegEarth-OV3 / SAM3

### 3.1 Shared grounding and three readouts

For image `X` and category concept `t_c`, SAM3 first creates shared conditioned states:

\[
H_c=\Phi(X,t_c).
\]

Presence, Semantic and Instance are role-specific readouts of this coupled grounding, not three independent models.

- **Presence** `p_c`: class-level evidence that concept `c` exists.
- **Semantic** `S_c(x)`: dense category coverage from conditioned visual memory.
- **Instance**: object queries generate masks `M_{cq}(x)` and confidences `r_{cq}`; admitted queries are aggregated into a class map.

With `r_cq` denoting raw object confidence, the default implementation is:

\[
I_c(x)=\max_{q\in Q_c}M_{cq}(x)r_{cq}p_c,
\qquad Q_c=\{q:p_cr_{cq}>\eta\}.
\]

Final class evidence:

\[
F_c(x)=p_c\max(S_c(x),I_c(x)).
\]

All category maps are compared by pixel-wise argmax; thresholded pixels may become background. Official aliases and dataset ontology are part of the baseline anchor.

The processor's default instance confidence is `raw object score × presence`; the outer fusion multiplies presence again. The previous state formula omitted the inner `p_c` while naming `r_cq` as raw confidence. This was corrected on 2026-09-03 to match the existing implementation; no model operation changed.

### 3.2 Assumptions exposed by this project

- one concept string is sufficient for all three roles;
- Semantic and Instance scores can be compared by raw magnitude;
- Presence can control admission/amplitude/final class support;
- one visual observation is sufficient for dense coverage and region organization.

The project does not claim these assumptions are globally wrong. It tests how supplementary evidence should enter while protecting the original path.

## 4. Current Method

### 4.1 Part I: Role-Functional Text

For every class `c`, preserve the official prompt output as anchor `(p_c^A,S_c^A,I_c^A)`.

Generate role-functional candidates:

- Presence: how the concept is established or expected to exist in the scene;
- Semantic: dense coverage, appearance, material and continuity information;
- Instance: entity/region organization, connectivity and query separability.

Each candidate is grounded through unchanged SAM3. Only the assigned role output is used for the supplementary correction; the native coupling is retained. The stable update is bounded and residual:

\[
O_c^r=O_c^A+\alpha_r\operatorname{clip}(O_c^{candidate}-O_c^A,-\tau_r,\tau_r),
\quad r\in\{P,S,I\}.
\]

This compact equation does not imply independent roles: current Presence is used to rebuild both anchor-query and candidate-query instance maps before their residual is computed. `anchor_admission`, when selected, changes only the query-admission presence to `p_A`, not instance amplitude or final scaling. Current residual defaults are `alpha=0.5`, `tau=0.25`.

Each view/unit preserves official aliases through `G_v=clip(B_v^official + F_v^theta − F_v^0,0,1)`, followed by coordinate restoration and overlap aggregation with the official aggregation order retained. `F_v^0` is the composed role anchor, not assumed identical to the original multi-alias official map. The exact official no-update path is recoverable. Direct replacement is not the default.

### 4.2 Part II: Joint Role–View Profile

Construct aligned observations for the same spatial content:

- **Native/Local**: high-resolution detail, boundaries and small entities;
- **Context/Global**: broader geographic layout, low-frequency structure and continuity.

Both observations complete frozen SAM3 grounding. A dataset profile jointly determines role-text candidate slots, admission mode where required, visual observations and a tested light evidence-composition operator.

The second part is not an independent context add-on. It jointly configures role-functional text and visual evidence. In the verified implementation, the **same selected P/S/I slots are evaluated on both views**; each view first completes role composition and native `p × max(S,I)`. The aligned `C×H×W` class-score maps are then combined by `Z=Psi(G_Local,G_Global)`. This is output-level View Evidence Fusion, not per-head Local/Global routing or fusion-encoder attention modification. The operator can vary by profile without changing the framework.

### 4.3 Unified chain

1. Role Text specifies what functional information a readout needs.
2. View specialization supplies from what visual field that information should be read.
3. Native SAM3 grounding preserves pretrained cross-modal coupling.
4. Each view uses native P/S/I fusion; aligned view scores are fused before the unchanged cross-class argmax and background threshold.

## 5. Reproduced Baselines and Results

### 5.1 Reproduced baselines

| Dataset | Matched baseline mIoU | Status |
|---|---:|---|
| LoveDA | 47.342 | verified |
| OpenEarthMap | 44.303 | verified |
| Potsdam | 57.867 | verified |
| UDD5 | 71.804 | verified |
| Vaihingen | 60.860 | verified |
| VDD | 64.107 | verified |
| UAVid | 54.585 (paper-facing 54.7) | verified |
| iSAID | 27.643 (paper-facing 27.6) | verified after label repair |
| Pascal VOC20 | 96.8 paper-facing / 96.890 matched screen | baseline and main-method evaluation verified |
| Cityscapes | 67.9 | baseline and main-method evaluation verified; use this matched value rather than paper 69.7 |

### 5.2 Verified Role-only results

| Dataset | Baseline | Best Role-only | ΔmIoU | Role profile |
|---|---:|---:|---:|---|
| LoveDA | 47.342 | 48.305 | +0.963 | P1+S1+I0 |
| OpenEarthMap | 44.303 | 50.530 | +6.227 | P0+S3+I2 |
| Potsdam | 57.867 | 58.594 | +0.727 | P1+S2+I0 |
| UDD5 | 71.804 | 72.888 | +1.084 | historical best P1+S2+I2 |
| Vaihingen | 60.860 | 62.333 | +1.473 | historical best P0+S3+I1 |
| VDD | 64.107 | 66.116 | +2.009 | historical best P2+S1+I1 |
| UAVid | 54.585 | 59.508 | +4.923 | P2+S3+I0 |
| iSAID | 27.643 | 28.269 | +0.626 | P0+S3+I0 |

Useful non-anchor text exists on all datasets, but the best composition need not activate all roles. iSAID is strong counter-evidence to the claim that every role must be supplemented: S3 is useful while extra P/I generally reduce the gain.

### 5.3 Verified Joint Role–View results — selected main protocol

This table is the user-confirmed main experiment (2026-09-04), retaining the completed original protocol with neighboring aligned tiles for Potsdam/Vaihingen. The current-image-only auxiliary control is recorded in §5.8; it must not silently replace these results.

| Dataset | Baseline | Role reference | Joint best | Joint vs baseline | Selected Joint profile |
|---|---:|---:|---:|---:|---|
| LoveDA | 47.342 | 48.305 | 48.806 | +1.464 | P1+S1+I0, native admission, max |
| OpenEarthMap | 44.303 | 50.530 | 53.075 | +8.772 | P0+S3+I2, native, linear-g0.50 |
| Potsdam | 57.867 | 58.594 | 63.181 | +5.314 | P1+S2+I0, anchor admission, linear-g0.75 |
| UDD5 | 71.804 | 72.888 | 72.944 | +1.140 | P2+S2+I1, native, logit-g0.75 |
| Vaihingen | 60.860 | 62.333 | 66.384 | +5.524 | P0+S3+I2, native, max |
| VDD | 64.107 | 66.116 | 66.555 | +2.448 | P2+S1+I0, native, logit-g0.50 |
| UAVid | 54.585 | 59.508 | 59.822 | +5.237 | P2+S3+I1, native, power4-g0.75 |
| iSAID | 27.643 | 28.269 | 29.126 | +1.482 | P0+S3+I0, native, logit-g0.50 |

For all eight datasets under this selected main observation protocol:

- baseline macro `53.564`;
- Role-only macro gain `+2.254`;
- additional Joint View gain `+1.669`;
- final macro `57.487`;
- total gain `+3.923`;
- Role-only positive on `8/8` and Joint positive over Role-only on `8/8`.

Selected Role×View interaction is positive on `6/8`: LoveDA `+0.664`, OEM `+1.675`, Potsdam `+0.112`, UDD5 `-0.283`, Vaihingen `+2.074`, VDD `+0.526`, UAVid `+0.468`, iSAID `-0.228`; macro interaction is about `+0.626`.

### 5.4 iSAID Joint closure

iSAID Joint was evaluated on all `11,644` validation tiles with no missing records or DDP duplicates. Reproduction checks were exact: official `27.643`, Role-only `P0+S3+I0` `28.269`, and zero identity/prompt-parity error.

The selected Joint result is:

- Role profile: `P0+S3+I0`;
- admission: native;
- View operator: `logit-g0.50`;
- mIoU: `29.126` (`+1.482` over baseline, `+0.857` over Role-only);
- aAcc: `97.023`.

Anchor View-only `logit-g0.50` reaches `28.728` (`+1.084`), so the strict Role×View interaction is `-0.228`: the combined profile is the best executable result, but its two gains overlap rather than producing positive synergy on iSAID. The old PPT-only `28.30` convention is obsolete and should be replaced by this verified result. The requested `P0+S3+I1` comparison is not present in the returned Joint logs.

### 5.5 Cityscapes natural-domain extension

Cityscapes was evaluated on all `500` validation images. The summary reports no missing dataset and no DDP-padding duplicates; official identity and native-prompt parity errors are exactly zero.

| Profile | mIoU | Delta to matched baseline | Notes |
|---|---:|---:|---|
| Matched baseline | 67.903 | 0.000 | paper reference is 69.7, but causal comparisons use the matched reproduction |
| Best Role-only | 72.195 | +4.292 | `P1+S2+I0`, native admission, Global endpoint |
| Best View-only | 68.721 | +0.817 | anchor text, `logit-g0.75` |
| Best Joint | 72.195 | +4.292 | exactly the Role-only Global endpoint; no added View gain |

The winning supplementary semantics are functional rather than remote-sensing-specific: Presence uses `visible <class>`, Semantic uses `<class> pixels with coherent appearance` for stuff or `<class> silhouette and surface` for objects, and Instance remains the official anchor. P1 alone gives `+3.684`, S2 alone gives `+1.800`, while P1+S2 gives `+4.292`; their performance interaction is therefore `-1.192`, so both signals help but overlap. Adding I1/I2 to P1+S2 reduces mIoU to `71.969/71.935`.

The gain is concentrated in classes the baseline handled poorly: rider `4.85→50.67` IoU (`+45.81` points), train `9.60→40.69` (`+31.10`), person `72.31→77.98` (`+5.67`) and bus `71.20→76.40` (`+5.21`). Main losses are wall `43.83→37.71` (`-6.11`), building `-0.89`, sidewalk `-0.81`, fence `-0.51` and tree `-0.35`. Accordingly, mIoU rises strongly while aAcc changes from `94.702` to `94.576` (`-0.126`): this is a class-balance improvement, not a large-class pixel-accuracy gain.

View evidence is useful but not additive here. View-only improves `+0.817`, yet every tested non-Global operator lowers the best Role profile; its strongest non-Global result is `max=71.107`, still `-1.088` below Role-only. The P1+S2+I0 Local/Global oracle reaches `78.607`, showing complementary pixels exist, but current fixed operators cannot identify them without oracle information. Therefore Cityscapes supports transfer of Role-Functional Text beyond remote sensing, but does not support claiming that Joint View adds value on this natural-image dataset.

### 5.6 VOC20 natural-domain extension

VOC20 covers all `1,449` validation images. The merged interrupted/resumed run has no missing dataset; `199` intentional overlap/DDP records were removed only after exact payload equality checks. Reference identity and prompt parity errors are zero. Its per-image Global source is legitimately mixed by image size: `1,431` use `full_image` and `18` use `aligned_context`.

| Profile | mIoU | Delta to matched screen baseline | Configuration |
|---|---:|---:|---|
| Matched screen baseline | 96.890 | 0.000 | official anchor / Global |
| Best Role-only | 96.997 | +0.108 | `P1+S3+I0`, native / Global |
| Best View-only | 96.997 | +0.107 | anchor, `logit-g0.75` |
| Best Joint | 97.108 | +0.218 | `P1+S3+I0`, native, `logit-g0.50` |

For the selected `logit-g0.50` operator, strict Role×View interaction is slightly positive at `+0.0066`; the two main effects are therefore almost additive rather than strongly synergistic. All `13/13` tested mixed-view operators improve `P1+S3+I0` over its Global endpoint (`97.054–97.108` versus `96.997`), so the View contribution is not a single-parameter accident on VOC20.

Role gain is primarily Presence-driven: `P1+S0+I0=96.995` (`+0.105`), while `S3` alone is `-0.005` and I1/I2 alone are negative. S3 adds only `+0.002` after P1, and the best configuration keeps Instance at anchor. Thus VOC20 supports functional Role specialization beyond remote sensing but again rejects the stronger claim that every role must receive supplementary text.

The Joint result changes `143,694` pixels relative to official, including `104,721` corrections and `34,184` damages (net `+70,537`). Largest class IoU gains in percentage points are horse `+0.740`, chair `+0.722`, television monitor `+0.660`, table `+0.591`, sofa `+0.509` and dog `+0.369`; main losses are sheep `-0.117`, cow `-0.100` and train `-0.006`. The small aggregate gain is consistent with the `96.890` baseline ceiling, not with absence of useful corrections.

### 5.7 Cross-dataset class and pixel mechanism

Across the eight remote-sensing datasets, the selected Joint method improves `48/63` dataset-class pairs and harms `15/63`; `47` gains and `14` losses have magnitude at least `0.1` IoU point. Class gain has a modest negative association with baseline strength: remote-only Pearson `-0.229`, Spearman `-0.177`. For the `17` classes below `30%` baseline IoU, Role-only/View-only/Joint average gains are `+4.26/+1.84/+7.03` points; for `22` classes at `30–60%`, Joint gives `+3.82`; for `24` classes at or above `60%`, Joint gives `+1.41`. Across all ten evaluated datasets and `102` dataset-class pairs, Joint improves `74` and harms `28`; baseline-IoU versus Joint-gain Pearson correlation is `-0.387` and Spearman correlation is `-0.357`. Do not use the ten-dataset correlations to label the eight-dataset plot.

The 2026-09-03 scatter plot retains every remote class, including OEM background `+60.29`, with an explicitly marked y-axis break. Excluding only that point gives group means `+3.70/+3.82/+1.41` and Pearson `-0.193`; excluding all background/clutter gives `+3.02/+4.25/+1.49`. Supported wording is **larger average gains for weak/moderate classes than strong classes**, not strictly monotonic improvement or a causal finding from correlation. The 63-class mean `+3.769` differs from eight-dataset macro `+3.923` because weighting differs. Plot/data/caption/provenance: `docs/分析图表/2026-09-03/`.

The logged GT transition counters confirm actual pixel corrections. On the eight remote-sensing datasets, Joint changes predictions so that approximately `429.16M` wrong pixels become correct versus `165.85M` correct pixels becoming wrong, a `2.59×` correction/damage ratio and `+263.31M` net corrections. Every remote dataset has positive Joint pixel net. Across all ten datasets the ratio remains `2.53×`. Pixel net and mIoU need not agree for every isolated part: Role-only on Potsdam and Role/Joint on Cityscapes can improve mIoU while harming more raw pixels because rare weak classes improve as common-class pixels shift.

Post-hoc broad class grouping over the `63` remote dataset-class pairs gives the following Joint mean gains: background/clutter `+10.22` (`7/8`, heavily influenced by OEM background `+60.29`), water-related `+5.65` (`3/4`), vegetation/land cover `+4.95` (`14/15`), built structures `+2.48` (`7/11`), movable objects `+1.49` (`7/11`), transport surfaces `+1.26` (`6/9`) and sports fields `+0.79` (`4/5`). Role-only is strongest on weak semantic recovery, while View adds relatively more for movable objects, vegetation and water. Transport surfaces remain less stable: notable Joint losses include OEM road `-4.71` and VDD road `-1.97`.

On 2026-09-03 the paper-facing visualization was reorganized around those semantic groups rather than dataset colors/baseline-strength bins. All 55 foreground pairs and 8 background/clutter pairs remain; foreground improves on `41/55`, mean `+2.83`. Role-only→Joint group mean gains: water `+3.15→+5.65`, vegetation/land cover `+2.83→+4.95`, structures `+1.59→+2.48`, movable objects `-0.02→+1.49`, transport `+1.43→+1.26`, sports `+0.34→+0.79`. The stage difference is **not** a class-level factorial interaction; Joint may use a different role profile. Sports baseline mean `8.76` with only `+0.79` improvement also shows why low baseline alone is not a sufficient explanation. Data/mapping/provenance: `docs/论文框架/2026-09-03/`; publication figures: `output/pdf/category_evidence_20260903/`.

### 5.8 Potsdam / Vaihingen current-image-only control (2026-09-04)

Source: `logs/joint_role_view_single_image_v1_full_bc5a250/summary/`. Returned summaries cover Potsdam 2,016 images and Vaihingen 398; no missing dataset or duplicates are reported. Both identity and prompt-parity errors are zero; Global sources are exclusively `full_image`. Per-image rank files were not returned for an independent raw-record recount.

Each dataset tested seven Role candidates × 15 view settings plus one official reference (106 variants). Global is the current 512×512 image; Local comprises four 256×256 crops, with no neighbor access.

| Metric / profile | Potsdam | Vaihingen |
|---|---:|---:|
| Baseline / Anchor Global | 57.867 | 60.860 |
| Anchor Local | 48.667 | 49.993 |
| Best Role / Global | 58.594 | 62.333 |
| Same Role / Local | 49.531 | 50.973 |
| Best actual mixed-view result | 58.428, linear-g0.75 | 61.650, logit-g0.75 |
| Best Joint including endpoints | 58.594, Global | 62.333, Global |
| Best Joint − Role-only | 0.000 | 0.000 |
| Previous neighbor-context Joint | 63.181 | 66.384 |

Selected profiles: Potsdam `P1+S2+I0 / anchor_admission / global`; Vaihingen `P0+S3+I1 / native / global`. The previous Vaihingen Joint profile `P0+S3+I2 / max` gives only 58.857 with the new views. Do not confuse that fixed-profile control with the summary's sequential `P0+S3+I1 / max=59.092`.

The old Local512 endpoint is exactly the new Global512 endpoint for matched prompts in the original Joint screen. Therefore the difference is not Role-Text reproduction drift. It changes the observation pair from neighbor 512/1024 to same-image 256/512, affecting field of view, relative object scale and crop boundaries together; the experiment does not isolate those causes.

Key evidence:

- All 13 mixed operators lower each dataset's current best Role/Global. A minor exception across other Role candidates exists: Potsdam `P1+S3+I0`, Global58.120 → linear-g0.75 58.335, but still below the best58.594. Thus no best-result gain, not zero information for every possible prompt.
- Role remains useful on both observations: Local Role − Local Anchor is +0.865/+0.980. Its Global gains come mainly from Potsdam tree +5.255, and Vaihingen road +2.369, grass +1.216, car +2.011 and clutter +3.140.
- Potsdam current linear-g0.75 harms tree/car by −1.952/−1.100 versus Role/Global while helping road/clutter; mIoU drops0.166 despite aAcc +0.399. Vaihingen current max damages car by13.145 IoU points and five of six classes overall; this is the recorded max control, not a per-class analysis of its best logit mix.
- Current-Role oracle headroom is +5.552/+2.730. Local-only correct pixels are25.595M/2.855M, but Global-only correct pixels are57.729M/11.440M. Complementarity exists; tested mixing fails to exploit it without larger harm.
- Positive interaction is not sufficient: current linear-g0.75 on Potsdam has Γ+0.066 but View main effect−0.232; current logit-g0.75 on Vaihingen has Γ+0.299 but View main effect−0.982. At the selected Global endpoints both View effect and Γ are0.

If only these two entries are replaced by the current-image-only best and the other six remain unchanged, eight-dataset macro becomes **56.407** (baseline53.564; Role-only55.818; total+2.843; extra View+0.589). Independently best View-only macro changes from55.13 to54.20; this differs from the fixed-Joint-operator View counterfactual used for Γ. Overall remains8/8 above baseline, but View adds on6/8; matched Γ macro is+0.353, positive on4/8 with two zeros. This is a cross-run arithmetic re-summary, not a new eight-dataset run. Historical main/PPT tables and class charts are not overwritten. The full eight-dataset baseline/original/current/component/gain tables are preserved in §6 of the single-image report.

Decision: retain Role Text; mark the 256/512 view realization as unsuccessful for additional best mIoU on these two datasets, not a rejection of all same-image observation designs. Do not expand its operator/text search. A larger overlapping Local crop (e.g.384/512) is only a possible minimal next control, not implemented or scheduled. Full analysis: [single-image report](docs/研究记录/2026-09-04_单图Role-View实验分析.md).

## 6. Dataset/View Definitions

- LoveDA, OEM, UDD5, VDD: Local and Context are aligned observations of the same image/spatial location; no external image is introduced.
- Potsdam and Vaihingen selected main results:512×512 targets use1024×1024 context reconstructed from neighboring aligned RGB tiles of the same original geographic scene; RGB overlap/alignment was verified. Their single-image auxiliary control/result is separate (§5.8).
- UAVid: the official 1080×1280 patch is Global; four aligned 640×640 crops are Local. No second frame is used.
- iSAID: the repaired 896×896 validation tile is Global; aligned 512×512 subviews are Local. No support image is used.
- Completed same-image control (2026-09-04): Potsdam/Vaihingen use the current 512×512 image as Global and four 256×256 crops as Local, with no neighboring file access. Each view completes native grounding; continuous class-score maps are restored to view coordinates, Local maps are stitched/overlap-averaged, then views are fused before final class prediction. Best selection is Global on both; historical neighbor-context results remain separately recorded.

`power4-g0.75` means `(0.25L^4+0.75G^4)^(1/4)`. The exponent preserves strong Local evidence more than a linear average while the 0.75 Global weight favors context. It is frozen evidence composition, not training.

## 7. Major Experiment Evidence

### 7.1 Text entry-path screen

| Method | Positive cases | Mean ΔmIoU | Conclusion |
|---|---:|---:|---|
| same supplementary text re-grounds all P/S/I | 0/36 | -21.152 | one human-plausible description can conflict across roles |
| candidate Semantic directly replaces anchor Semantic | 3/36 | -6.355 | useful information exists, but replacement destroys stable semantics |
| anchor-preserving bounded Semantic residual | 13/36 | -0.500 | 36/36 pairwise better than replacement; selected cases can be positive |

OpenEarthMap S1 illustrates role assignment: Semantic-only `+1.876`, while sharing the same text across all roles gives `-1.093`.

### 7.2 View entry-path screen

- Shared Canvas proves the second observation contains information: `+0.922` macro, positive on 4/6 in the original screen.
- Fixed R0–R14 operator families are unstable: best fixed family only `+0.097` macro, positive on 3/6.
- Joint selection succeeds because Role and View are selected together, not because one operator is universally best.

### 7.3 Direct replacement vs residual

Six-dataset closure: all-residual Joint macro `61.824`; all-direct `53.288`. Direct is positive over residual only on VDD (`67.264` vs `66.555`), mainly through facade IoU while reducing background/road accuracy. Residual is the robust method; VDD direct is a validation-selected diagnostic exception.

## 8. Closed or Rejected Directions

These are implementation-level conclusions. A failed realization does not prove every imaginable broad method impossible, but no further tuning is planned without new evidence.

| Direction | What was tested | Evidence / decision |
|---|---|---|
| Top-1/Top-2 reliability routing | final-score selection and gates | surface score manipulation did not address grounding; stopped |
| self-generated point/box prompting | baseline predictions generate geometry prompts | increases coverage but cannot judge correctness; reinforces errors |
| unrestricted test-time self-calibration | entropy/self-output prompt adaptation | no independent anchor; performance dropped and errors became self-consistent |
| universal direct replacement | replace anchor role/output | residual pairwise better in 36/36; final direct fails on 5/6 |
| universal Presence `branch_once` | remove one Presence participation | early tiny gain, unstable after Role Text; not retained |
| generic dual-head recomposition | add, soft-OR, weighted/query-supported correction | no stable gain; no evidence hard max is main bottleneck |
| Block23 boundary refinement | use PE boundary signal to move query masks | AUC above random, but causal correction did not improve final mIoU; closed |
| PE intermediate guidance | intermediate spatial/region evidence | diagnostic geometry exists, but tested readouts did not yield stable gain |
| anchor-clamped Role Replay | one role state updates while others clamp | broad decline; shared grounding is coupled, not isolated channels |
| FCRA/class-role alignment | class-role scores gate residuals | D/Gamma variants could not separate helpful/harmful corrections |
| CoCo-style class calibration adaptation | common competition scale | no stable gain; class comparability was not the main bottleneck here |
| ProC-style PGRF transplant | semantic base plus gated instance residual | positive only 1/6, macro about -0.23; does not invalidate full ProC |
| universal Shared Canvas/fixed fusion | one context rule for all roles/datasets | context has information, but unified use is unstable; led to Joint Role×View |
| Prompt-SAM3 trained variant | one-dataset training and transfer | poor tested transfer; branch abandoned, without claiming all training impossible |

Retained mechanism-only observations:

- Block23 boundary evidence contains geometry not fully represented by object score, but predictive signal is not automatically actionable.
- Presence strongly interacts with Instance through admission/amplitude/final scaling, but direction varies by dataset.
- Query topology describes how a region is formed, not which semantic class it is.

## 9. Related Work Registry

| Work | Source | Core method | Relation |
|---|---|---|---|
| SegEarth-OV3 | local PDF / official code | SAM3 three readouts and native fusion | baseline |
| ProC-SAM3 | local PDF v2; GRSL 2026 | constrained prompt pool and PGRF | prompt/fusion reference; prompt-level rather than role-level; eight-dataset avg 56.1 |
| ConceptBank | local PDF | target-support prototypes, SAM3 functional scoring, Top-J embedding fusion | prompt quality by segmentation function; requires support GT |
| CoCo-SAM3 | local PDF/index | synonym calibration for cross-class comparability | class-scale reference, not role specialization |
| Promptable Concept Segmentation from Above | local PDF/index | SAM3 in overhead imagery | supports separating Presence and localization behavior |
| TMPA | local PDF/index | test-time multi-prompt adaptation in CLIP-style OVRS | motivated stable anchor plus bounded correction |
| PE intermediate-representation paper | local PDF/index | intermediate layers retain task-dependent spatial evidence | motivated a direction whose current causal use failed |
| DinoSplat-OV | arXiv:2608.03023v1, 2026-08-04; local PDF | DINOv3/DINO.txt, text-aware propagation, RGB-guided Gaussian upsampling with test-time optimization, global-supported sliding windows | newer training-free RS OVSS; not SAM3 role-text specialization; no comparable eight-dataset result |
| GeoSeg-OV | arXiv:2608.10426v1, 2026-08-11; local PDF | rotation-robust CLIP cost volume, VFM structural guidance, SGA and CAD | trained CLIP/aggregation/decoder; not a training-free competitor |
| RSGPNet | arXiv:2606.28410v1, 2026-06-25; local PDF / JSTARS DOI | SAM3 coarse text masks → box re-prompting → coarse/fine consistency verification | newly added to our index, not newly published in August; same task/backbone but different mechanism |
| GLA-CLIP | CVPR 2026 main; official PDF | extend global K/V, refine proxy anchors, dynamically normalize cross-window attention | direct context precedent; changes CLIP attention, unlike our post-grounding view evidence composition |
| PEARL | CVPR 2026 main; official PDF | geometrically align Q/K, then text-aware Laplacian propagation | clear align-then-propagate narrative and full component ablation; not evidence of a SAM3 alignment defect |
| OV-Stitcher | CVPR 2026 Findings; official PDF | stitch cross-window attention and add class-biased LLM prompts | prior text+context combination; novelty must center on P/S/I role needs and joint role/view configuration, not text+context alone |
| ConInfer | CVPR 2026 Findings; local official PDF, §§3.2/4.2 | aggregate scene/tile features for iterative consensus; reported implementation corrects every 50 images after resizing to448 | training-free RS OVSS including Potsdam/Vaihingen; cross-image feature aggregation is not proof of geographically adjacent RGB reconstruction |
| Dual Context-Conditioned Open-Vocabulary Semantic Segmentation in Remote Sensing | IEEE Access14:43664–43678,2026; DOI10.1109/ACCESS.2026.3674757 | target tile + neighboring same-resolution tile features + downsampled whole-scene features, combined in CLIP final attention with a frequency-aware gate | direct training-free RS neighboring-context precedent; publisher/Crossref metadata and original-article text verified; local PDF pending; exact512-file reconstruction protocol not verified |
| ReSeg-CLIP | arXiv:2602.23869; local PDF/code | hierarchical SAM-mask attention constraints plus RS-CLIP model composition | fully training-free but only three datasets and lower absolute results; useful method taxonomy, not current eight-dataset SOTA |
| DR-Seg | arXiv:2604.02010; local PDF | split CLIP channels into semantic/structural subspaces, DINO graph rectification and uncertainty fusion | trained30K iterations on DLRSD/iSAID; a strong trained-protocol reference, not a training-free comparator |

`参考论文/索引.md` is the detailed local literature index. `参考论文/` is local-only and gitignored.

2026-09-04 neighboring-context check: original Potsdam/Vaihingen uses aligned neighboring RGB to construct1024 context around512 target; the completed current-image-only control uses256 Local /512 Global and reads no neighbors. Literature supports neighboring/cross-window context in OVSS: Dual Context is the most direct RS precedent; GLA-CLIP/OV-Stitcher combine windows of a supplied image. None of these checks establishes that their Potsdam/Vaihingen benchmark access exactly matches our reconstruction from separate pre-cropped evaluation files. RGB-only context does not itself change the open-vocabulary/training-free task, but enlarged observation access must be distinguished from isolated512 baseline input. This is a protocol distinction, not evidence of GT leakage. The Dual Context paper is an earlier March2026 omission, not a newly published September work.

Latest literature check: **2026-09-27**. Under the strict protocol “no task-specific training, no support GT/few-shot adaptation, all eight SegEarth benchmarks reported”, ProC-SAM3 remains the highest verified published result at `56.1` average mIoU. Its GRSL publication DOI is `10.1109/LGRS.2026.3713378`. RSGPNet reports only LoveDA/Potsdam/Vaihingen/UDD5 `47.8/59.7/61.1/71.0` (mean `59.9`); ProC on the same four names is `46.1/58.8/64.5/73.4` (mean `60.7`). Dual Context reports `42.2` over the eight datasets. DinoSplat-OV and ReSeg-CLIP use partial dataset suites. DR-Seg/GeoSeg-OV/RSKT-Seg train parameters; few-shot textual inversion uses support examples. Their SOTA claims belong to different protocols and do not supersede ProC in the strict training-free full-eight comparison. The current project's internal main result is `57.487`, numerically `+1.387` over ProC, with four dataset wins and four losses, but it is unpublished and its explicit Potsdam/Vaihingen neighboring-context protocol must remain disclosed; do not describe it as externally established SOTA before submission/independent review. No newer verified September arXiv work with a higher comparable eight-dataset result was found; this is a dated search result, not an exhaustive novelty guarantee.

The literature library contains **71 PDFs / 70 works**: the original **20-paper CVPR 2025–2026 main-conference reading corpus** is preserved, with targeted follow-up on GLA-CLIP, PEARL, Findings' OV-Stitcher, ReSeg-CLIP and DR-Seg. The direct context precedents now lead the method-two discussion; HRDA supports context/detail trade-offs, and SlowFast remains only a design analogy. The earlier CLIP+SAM *Enabling Training-Free Text-Based Remote Sensing Segmentation* (arXiv:2602.17799) and few-shot *ELFSS-AR* (arXiv:2607.29278) remain indexed with their different protocols. Exact sources, actual workflows and claim boundaries are maintained in `docs/论文框架/2026-09-03/引用与论点对照.md`; that 30-entry manuscript ledger predates the two latest library additions and must be extended only if they are cited in the draft. Direct Segmentation and DLAE remain distinct records; ResCLIP's RCS name is corrected to Residual Cross-correlation Self-attention.

## 10. Manuscript Scope

The manuscript is organized around the two validated contributions: Role-Functional Text and Joint Role–View evidence composition. Follow-up work should complete their paper evidence and writing rather than introduce a third engineering topic.

## 11. Data and Reproduction Notes

### iSAID repair

- 11,644 validation image/annotation pairs;
- earlier masks were binarized because Pillow 11.3.0 plus deprecated `Image.fromarray(uint8_ids, mode='P')` corrupted the palette-index path;
- masks were rebuilt as mode `L` with official 896/384 crop geometry;
- repaired baseline reproduced `27.640` mIoU;
- Role run covers all images; 102 DDP-padding duplicates were removed in summary.
- Joint run covers all 11,644 images with no missing records or duplicate records; selected result is `29.126` mIoU.

### UAVid conversion

- 150 test frames with labels were paired and converted to official test patches;
- navy `(0,0,128)` is part of the actual label palette and must be mapped rather than rejected;
- matched baseline is 54.7 mIoU.

## 12. Implementation and Entry Points

- `segearthov3_segmentor.py`: baseline and experiment dispatch;
- `role_functional_text_screen.py`: active role-text cache, bounded updates, prediction metrics;
- `role_visual_field.py`: aligned observations, per-view role composition, Joint screen/final deployment;
- `configs/experiments/joint_role_view_final_v1.json`: frozen six-dataset closure registry;
- `tools/run_joint_role_view_final_v1.sh`: closure/audit/benchmark;
- `tools/run_domain_extension_joint_profile_v1.sh`: UAVid/natural-domain extension;
- `tools/plan_evaluation_resume.py`: derive safe iSAID/VOC20 tail indices from completed per-image JSONL records;
- `tools/run_isaid_sequential_role_view_v1.sh`: iSAID Role → View workflow;
- `tools/dataset_converters/prepare_isaid_val_annotations.py`: repaired iSAID conversion;
- `tools/dataset_converters/uavid.py`: UAVid conversion.

Baseline configs and original behavior remain available; experiments are config/script controlled.

### 12.1 Current implementation status

- Original six-dataset fixed deployment remains available; UAVid/iSAID/natural-domain screen results are verified, while selected extension profiles still need compiling when qualitative export is requested.
- VOC20/iSAID resume and summary fixes are complete. No further resume work is pending for the reported complete results.
- Main-method theory/code mapping was checked at `1b3b1d3`: complete per-prompt grounding, coupled P/I residuals, coordinate restoration, and post-head View Evidence Fusion match the method. Detailed map and closure qualifications remain in [the audit](docs/分析图表/2026-09-03/README.md).
- Same-image Potsdam/Vaihingen control is implemented and pushed at `bc5a250`: `single-image-smoke/all/summarize` modes in `tools/run_joint_role_view_profile_v1.sh`, using `role_visual_field_single_image_v1.json` and `joint_role_view_single_image_v1.json`. Each retains seven existing Role candidates, with Global 512 and four Local 256 crops; no neighbor access. Five targeted tests and shell syntax passed; full server results are analyzed in §5.8. No rerun is pending for this control.
- Smoke: `ROOT=logs/joint_role_view_single_image_v1_smoke GPU_LIST=0,1,2,3 NPROC=4 SMOKE_SAMPLES=1 bash tools/run_joint_role_view_profile_v1.sh single-image-smoke`.
- Full run and automatic summary: `ROOT=logs/joint_role_view_single_image_v1_full GPU_LIST=0,1,2,3 NPROC=4 bash tools/run_joint_role_view_profile_v1.sh single-image-all`.

Completed cleanup, resume, audit and implementation events are preserved in [the research history](docs/研究记录/实验沿革与实现记录.md), not maintained as a second current-status list.

## 13. Local Research Artifacts

Local-only, not copied to the server or GitHub:

- `docs/README.md`: single navigation entry, distinguishing current state, manuscript, history and presentation artifacts;
- `docs/研究记录/实验沿革与实现记录.md`: past method trials, completed cleanup/resume/implementation events; moved out of the current-state section without deleting the record;
- `docs/研究记录/2026-09-04_单图Role-View实验分析.md`: completed two-dataset current-image-only control, exact protocol distinction and conditional eight-dataset re-summary;
- `docs/论文框架/README.md`: manuscript file-purpose guide and recommended reading order;
- `docs/论文框架/CVPR投稿时间线.md`: dated official timeline check; not a recurring monitor;
- `docs/导师汇报/2026-08-23/导师汇报_研究进展_最终版.pptx`;
- `docs/导师汇报/2026-08-23/研究方法与试错脉络说明.docx`;
- `docs/导师汇报/2026-08-23/方法架构图/01_baseline_vs_ours_role_view.png`;
- `docs/导师汇报/2026-08-23/方法架构图/02_ours_joint_role_view_main.png`;
- `docs/导师汇报/2026-08-23/方法架构图/03_ours_joint_role_view_clean.png`;
- `参考论文/`.
- `docs/分析图表/2026-09-03/`: remote class-gain PDF/SVG/PNG, 63-point CSV, statistics/provenance JSON, reproduction script and literature/code audit README.
- `docs/论文框架/2026-09-03/`: the maintained Related Work/Method/Experiments draft, original 20-paper readings plus a targeted update, claim ledger, unified BibTeX, real main/ablation tables, semantic-group data and matched 2×2 interactions. The README explains all 11 files; no duplicate “final” drafts are introduced.
- `output/pdf/category_evidence_20260903/`: one simple grouped bar figure in PDF/SVG/PNG, showing Role Text and Role Text + View gains over baseline for seven semantic groups; all class gains/losses retained.
- `论文执笔交付包/`: local-only writer handoff assembled on 2026-09-27. It contains a dated fact snapshot, writer brief, method/code specification, exact editable result tables, claim-evidence boundaries, selected core PDFs, manuscript drafts, figures/PPT and a reproduction/provenance index. Full logs, datasets, weights, source-code copies and temporary PDF extracts are intentionally excluded; the live repository and referenced log paths remain the source of truth. The folder is gitignored.

On 2026-08-28, the supervisor deck was refreshed with verified iSAID Joint `29.126` and the actual eight-dataset aggregates: Role gain `+2.25`, View-after-Role gain `+1.67`, final macro `57.49`, total gain `+3.92`, selected interaction `6/8` with macro `+0.63`, and iSAID interaction `-0.23`. Only numeric data on slides 7, 9, 10, 14, 15 and 17 changed; slide 16 was intentionally preserved byte-for-byte at the rendered-content level as requested.

On 2026-08-27, project `tmp/` was reduced to its policy `README.md`; regenerated PDF text extracts, PPT previews/build scripts and the corresponding `/private/tmp/segearth3*` authoring caches were removed. No final document, paper PDF, log, dataset or code file was deleted.

On 2026-09-03, `tmp/` still contained only its policy `README.md`, which was retained. Removed six obsolete converter `.pyc` files and their empty cache directory; no final artifact, experiment record or source was removed.

The same-day writing follow-up retained the three new official paper PDFs, consolidated navigation and records, and removed its temporary PDF figure previews. Existing experimental CSV/JSON values and the PPT were not revised.

## 14. Current Decisions

1. Keep Role-Functional Text as the first contribution.
2. Keep Joint Role–View Profile as the second contribution.
3. Use bounded anchor-preserving residuals as the robust default.
4. Keep native SAM3 grounding and P/S/I fusion intact unless new causal evidence supports a change.
5. Do not add role candidates, view operators, boundary refinements, routers or generic fusion rules now.
6. Validation-set profile selection is accepted at this stage; do not repeatedly insist on train/support selection.
7. Keep paper development focused on the two validated contributions and their necessary evidence.
8. Main-result choice confirmed2026-09-04: retain the original Joint macro57.49 with explicit Potsdam/Vaihingen neighboring-context construction in experimental details; retain the single-image result as a control only. No new model change or rerun is requested by this decision.

### 14.1 Paper narrative decision (2026-09-03)

- Core chain: **role-functional language specifies the requested evidence; visual observation controls its observability; full native grounding preserves their coupling; aligned score fusion uses complementary outputs**.
- Keep the main mechanism at its implemented level. Do not describe explicit S→Global/I→Local routing, internal cross-view attention, or calibrated latent-space fusion; none is the current validated method.
- Separate `8/8` overall improvement from `6/8` positive fixed-profile Role×View interaction. Matched factorial macro: `m00=53.564`, `m10=55.674`, `m01=54.751`, `m11=57.487`, `Gamma=+0.626`. The stronger standalone Role-only macro `55.818` uses independently best role profiles and must not replace m10 in this equation.
- Strong conditional examples: the selected View operator gives Anchor `-0.162` on LoveDA and `-0.150` on UAVid, but adds `+0.502/+0.318` after the matched Role profile. Potsdam has large View main effect but only `+0.112` extra interaction; do not call it strongest synergy. UDD5/iSAID have overlapping gains; Cityscapes selects a single endpoint; VOC20 is nearly additive.
- Theoretical motivation: GLA-CLIP/OV-Stitcher establish the relevance of cross-window context in training-free OVSS; HRDA supports the context/detail trade-off. Our distinct mechanism is role-functional text with intact SAM3 grounding and aligned view outputs. Do not claim text+context combination itself is new. The class-margin derivation is now a supplementary-material candidate, while the main Method uses a short conditional-complementarity explanation. SlowFast is a brief design precedent, not a biological derivation.
- Main comparison follows the preserved PPT slide 16 with all competing methods. Matched component/factorial tables use precise local CSVs. Method and Related Work now explain actual computation, with external claims mapped to original sources. Writing cautions are consolidated at the end rather than interrupting each subsection.
- Main text describes Global/Local normally; actual observation construction stays in reproduction details without unsupported same-file claims.
- No inference code changed in this narrative pass. Reuse the same-day main-chain audit, not another repository-wide audit.
- Completed the requested revision: simple Role/Joint gain bars, 20 verified CVPR structure readings, three Related Work subsections, four Method subsections and six Experiments subsections. All 13 main-table numerical rows were checked against PPT slide 16; eight matched interaction identities and 20 source records/local PDF links were verified. Temporary paper extracts/layout contact sheets and the obsolete companion figure were removed; final references, charts and reproducible data remain.
- Targeted follow-up: retained the functioning chapter/table structure; updated the closest related works, tightened role-specific differentiation, moved the long margin analysis out of the main Method, and labeled natural-domain results as evaluation rather than unsupported unchanged-profile transfer. No new experimental result was introduced.
- September4 result qualification: the two-dataset single-image control no longer supports an added View contribution on Potsdam/Vaihingen; the historic8/8 extra View and6/8 interaction statements above belong to the neighbor-context protocol. The same-image replacement tally is6/8 extra View and4/8 positive interaction. Preserve both records and revise manuscript data only under an explicitly chosen observation protocol.

### 14.2 Submission planning status (checked 2026-09-03)

The next submission target is **CVPR 2027**, not the completed CVPR 2026 cycle. The official 2027 home/Dates pages list Seattle, June 20–25, 2027 (workshops/tutorials June 20–21; main June 22–25), but have not published abstract/paper/supplement/rebuttal/decision dates. CVPR 2026's November 7/13/20, 2025 deadlines are historical references only. Sources and the official-page date discrepancy are recorded in `docs/论文框架/CVPR投稿时间线.md`.

## 15. Next Actions

- [x] Settle the manuscript's Potsdam/Vaihingen observation protocol: user selected the original neighboring-context main results (eight-dataset macro57.49) on2026-09-04. Document the spatial input construction; keep the completed256/512 same-image experiment as an auxiliary control, with no repeated screen scheduled.
- [ ] Run `P0+S3+I1` on iSAID only if the missing comparison is still needed; it is not required to establish the current `P0+S3+I0` Joint result.
- [ ] Produce final qualitative segmentation comparisons after main datasets finish.
- [ ] When deployment/qualitative export is requested, add the selected UAVid/iSAID/VOC20/Cityscapes profiles to the fixed-deployment entry; do not confuse screen output images with logged method variants.
- [ ] Paper-critical control: compare final supplementary texts under equal grounding budget with shared/generic use versus role-functional allocation, initially on 2–3 representative datasets; do not re-run a large prompt grid.
- [ ] During fixed-profile qualitative export, collect the four matched Anchor/Role/View/Joint predictions and a small region-size/shape correction analysis; do not infer class-level factorial synergy from Joint−best-Role bars.
- [ ] Complete manuscript-facing Global/Local configuration and coordinate-restoration details using the actual implemented observation protocol.

## 16. Standing Collaboration Rules

- Present actual results before interpretation.
- Use mIoU as primary metric; class damage/accuracy is diagnostic support, not an automatic veto.
- A negative implementation rejects that realization, not automatically the whole idea; one evidence-driven minimal correction is allowed before closure.
- Do not use the model's own prediction as an unanchored self-evaluation signal.
- Avoid large hyperparameter searches and dataset-specific tuning as substitutes for method design.
- Do not reconsider iSAID incompleteness; label corruption was diagnosed and repaired.
- Do not proactively discuss or track inference efficiency; focus paper work on the two validated research contributions (user decision, 2026-09-03).
- Keep code changes minimal, preserve baseline behavior, and synchronize code through GitHub only for implementation tasks.
