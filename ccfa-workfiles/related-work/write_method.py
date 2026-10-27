from pathlib import Path

ROOT=Path(r"D:\论文\9.27论文")
KIT=ROOT/"author-kit-main"
CN=ROOT/"中文论文"/"论文中文版.md"

en_method=r'''\section{Method}
\label{sec:method}

\subsection{Preliminaries: Native Concept Grounding}

Given an RGB image $X$ and a set of class concepts $\mathcal C$, open-vocabulary semantic segmentation assigns each evaluated pixel a class in $\mathcal C$, with background determined by the benchmark protocol. For class $c$ and its text concept $t_c$, SegEarth-OV3 uses SAM3 to form a condition-dependent state \cite{R10,R11}:
\begin{equation}
H_c=\Phi(X,t_c).
\label{eq:state}
\end{equation}
The state supports three native readouts: a class-level Presence score $p_c$, a dense Semantic map $S_c(x)$, and an Instance map assembled from object-query masks. For query $q$, let $M_{cq}(x)$ be its mask value at pixel $x$ and $r_{cq}$ its raw object confidence. Let $\eta$ be the query-admission threshold and $a_c$ the admission score. The native implementation uses $a_c=p_c$; an anchor-admission variant described below uses the anchor Presence instead. The admitted queries and instance map are
\begin{equation}
Q_c=\{q:a_c r_{cq}>\eta\},
\qquad
I_c(x)=\max_{q\in Q_c}M_{cq}(x)r_{cq}p_c.
\label{eq:instance}
\end{equation}
Semantic and instance evidence are combined by the native chain
\begin{equation}
F_c(x)=p_c\max\bigl(S_c(x),I_c(x)\bigr).
\label{eq:native-fusion}
\end{equation}
Presence therefore acts on query admission, instance amplitude, and final class scaling. The class maps are compared by pixel-wise argmax, and the baseline threshold assigns low-confidence pixels to background. For a class with aliases, the official path aggregates the prompt-wise outputs in its original order. We denote the resulting single-observation class-score map by $G^{\mathrm{o}}$.

\subsection{Role-Functional Text}

The official class name and aliases define an ontology anchor. We keep their native outputs as $(p_c^A,S_c^A,I_c^A)$ and build a small, frozen candidate bank for each class. Presence candidates describe how the concept is established or visible in a scene; Semantic candidates describe dense appearance, surface, coverage, and continuity; Instance candidates describe the organization and separation of query-supported regions. A zero slot keeps the anchor for that role, so not every class requires a non-anchor phrase.

Each non-anchor candidate is grounded through the complete frozen SAM3 model, producing $(p_c^r,S_c^r,I_c^r)$ for $r\in\{P,S,I\}$. We do not route a candidate directly into an isolated head. The assigned readout is combined with its anchor through a bounded residual. For two scalar or spatial quantities $a$ and $b$, define
\begin{equation}
\mathcal B(a,b)=\operatorname{clip}_{[0,1]}\!\left(a+\alpha\,\operatorname{clip}(b-a,-\tau,\tau)\right),
\label{eq:bounded}
\end{equation}
with $\alpha=0.5$ and $\tau=0.25$ in the reported configuration. The Presence and Semantic updates are
\begin{equation}
\tilde p_c=\mathcal B(p_c^A,p_c^{\pi_P}),
\qquad
\tilde S_c(x)=\mathcal B(S_c^A(x),S_c^{\pi_S}(x)).
\label{eq:role-updates}
\end{equation}
Because Presence affects instance construction, the instance maps are rebuilt after the Presence update. With admission score $a$, the anchor and candidate instance maps are
\begin{equation}
I_A^{\tilde p}=\mathcal I(Q_A;\tilde p,a),
\qquad
I_{\pi_I}^{\tilde p}=\mathcal I(Q_{\pi_I};\tilde p,a),
\qquad
\tilde I_c=\mathcal B(I_A^{\tilde p},I_{\pi_I}^{\tilde p}),
\label{eq:instance-rebuild}
\end{equation}
where $\mathcal I$ denotes the query aggregation in Eq.~\eqref{eq:instance}. The role-composed class evidence is then
\begin{equation}
F_{\pi,c}(x)=\tilde p_c\max\bigl(\tilde S_c(x),\tilde I_c(x)\bigr).
\label{eq:role-final}
\end{equation}
For native admission, $a=\tilde p_c$; for anchor admission, only query membership uses $a=p_c^A$, while the amplitude and final scaling still use the updated Presence. If all role slots are zero, the updates reduce to the anchor.

The official score field is retained to preserve aliases and the baseline aggregation order. Let $G_v^{\mathrm{o}}$ be the official map for observation $v$, $F_{v,\pi}$ the role-composed map, and $F_v^A$ the anchor composition without supplementary text. The observation-level output is
\begin{equation}
G_{v,\pi}=\operatorname{clip}_{[0,1]}\!\left(G_v^{\mathrm{o}}+F_{v,\pi}-F_v^A\right).
\label{eq:official-compensation}
\end{equation}
Thus, disabling all role updates returns the official map exactly. The construction is not an ensemble of three independent predictions: candidates are re-grounded completely, only their assigned readout changes the anchor, and the native Presence--Instance coupling remains active.

\subsection{Aligned Local and Context Observations}

A text description can specify a continuous surface or a complete region, but it cannot create visual evidence absent from the observation. Local observations preserve effective sampling density for boundaries and small objects; Context observations expose a wider spatial layout and long-range continuity. For datasets supplied as coordinate tiles, Context observations are assembled from spatially aligned neighboring RGB tiles without neighboring labels; otherwise they are enlarged crops of the input image. The evaluation protocol specifies the exact construction.

Every observation completes the native grounding and role composition independently. The Local and Context observations reuse the same selected role profile; JRV does not assign Presence to one view, Semantic to a second, or Instance to a third. For a view family $v\in\{L,G\}$ with target units $\mathcal U_v$, each unit $u$ produces a role-composed map $G_{u,\pi}$ on its own coordinate system. Let $W_u$ restore the map to the target coordinates and let $w_u(x)$ indicate valid coverage. The aligned view evidence is
\begin{equation}
\overline G_{v,c}(x)=
\frac{\sum_{u\in\mathcal U_v}w_u(x)\,W_u[G_{u,\pi,c}](x)}
{\sum_{u\in\mathcal U_v}w_u(x)}.
\label{eq:view-average}
\end{equation}
The final class-score field is
\begin{equation}
Z_c(x)=\Psi_{\omega}\!\left(\overline G_{L,c}(x),\overline G_{G,c}(x)\right),
\qquad
\widehat Y=\mathcal D_{\mathrm{base}}(Z),
\label{eq:view-fusion}
\end{equation}
where $\mathcal D_{\mathrm{base}}$ retains the baseline argmax and background threshold. The profile operator $\Psi_{\omega}$ is fixed rather than learned. We use element-wise maximum, Local or Context endpoints, weighted power means, and weighted logit fusion:
\begin{equation}
\Psi_{\max}(L,G)=\max(L,G),
\qquad
\Psi_{\rho,g}(L,G)=\left((1-g)L^{\rho}+gG^{\rho}\right)^{1/\rho},
\label{eq:view-operators}
\end{equation}
\begin{equation}
\Psi_{\mathrm{logit},g}(L,G)=\sigma\!\left((1-g)\operatorname{logit}(L)+g\operatorname{logit}(G)\right).
\label{eq:logit-operator}
\end{equation}
The operator family is a profile choice, not a new learned attention module. Combining complete class-score fields preserves the native cross-category decision after role and view composition.

\subsection{Inference Protocol and Profile Definition}

A dataset profile is a fixed tuple
\begin{equation}
\pi=(s_P,s_S,s_I,a,\Psi_{\omega}),
\label{eq:profile}
\end{equation}
where each $s_r$ indexes a candidate slot in the frozen text bank, $s_r=0$ retains the anchor, $a$ specifies native or anchor admission, and $\Psi_{\omega}$ specifies the view operator. The same profile is applied to every image in a benchmark and to both Local and Context observations. The text bank and profile are fixed before inference; SAM3 weights are never updated. Profile selection is dataset-level and offline, and the experimental section reports the selection protocol. No image-level ground-truth routing is used.

The implementation has three properties used by the experiments. First, every required supplementary phrase undergoes full native grounding rather than modifying an isolated decoder state. Second, an unchanged slot or an all-zero role profile recovers the anchor path, including the official alias aggregation. Third, Local and Context outputs are combined after complete role composition and coordinate restoration, so the method changes evidence use rather than SAM3 attention or its internal fusion operator.
'''

cn_method=r'''## 3. 方法

### 3.1 原生概念定位

给定 RGB 图像 \(X\) 和类别概念集合 \(\mathcal C\)，开放词汇语义分割为每个参与评价的像素分配一个类别，背景由基准协议决定。对于类别 \(c\) 及其文本概念 \(t_c\)，SegEarth-OV3 使用 SAM3 形成条件状态 [10,11]：

\[
H_c=\Phi(X,t_c).
\tag{1}
\]

该状态支持三种原生 readout：类别级 Presence 分数 \(p_c\)、稠密 Semantic 图 \(S_c(x)\)，以及由 object query 聚合得到的 Instance 图。对于 query \(q\)，记其 mask 在像素 \(x\) 上的值为 \(M_{cq}(x)\)，raw object confidence 为 \(r_{cq}\)。令 \(\eta\) 为 query admission 阈值，\(a_c\) 为 admission 分数。原生实现使用 \(a_c=p_c\)；下文的 anchor admission 变体则使用 anchor Presence。合格 query 与 instance 图为

\[
Q_c=\{q:a_c r_{cq}>\eta\},
\qquad
I_c(x)=\max_{q\in Q_c}M_{cq}(x)r_{cq}p_c.
\tag{2}
\]

Semantic 与 Instance 证据按原生链路融合：

\[
F_c(x)=p_c\max\bigl(S_c(x),I_c(x)\bigr).
\tag{3}
\]

因此，Presence 同时参与 query 准入、instance 幅度和最终类别缩放。所有类别图通过逐像素 argmax 比较，再由 baseline 阈值把低置信像素归为背景。对于带别名的类别，官方路径按照原有顺序聚合 prompt 输出。记这一单观察类别分数图为 \(G^{\mathrm{o}}\)。

### 3.2 角色功能文本

官方类别名和别名定义 ontology anchor。我们保留其原生输出 \((p_c^A,S_c^A,I_c^A)\)，并为每个类别构造一个小型、冻结的候选库。Presence 候选描述概念在场景中如何成立或可见；Semantic 候选描述稠密外观、表面、覆盖和连续性；Instance 候选描述 query 支持区域的组织、分离与定位。零号槽表示该 role 保留 anchor，因此并不要求每个类别都使用非 anchor 文本。

每条非 anchor 候选都经过完整、冻结的 SAM3 grounding，得到 \((p_c^r,S_c^r,I_c^r)\)，其中 \(r\in\{P,S,I\}\)。我们不会把候选文本直接送入某个隔离 head，而是把其对应 readout 与 anchor 通过有界残差组合。对于标量或空间量 \(a,b\)，定义

\[
\mathcal B(a,b)=\operatorname{clip}_{[0,1]}\!\left(a+\alpha\,\operatorname{clip}(b-a,-\tau,\tau)\right),
\tag{4}
\]

其中报告设置取 \(\alpha=0.5\)、\(\tau=0.25\)。Presence 和 Semantic 的更新为

\[
\tilde p_c=\mathcal B(p_c^A,p_c^{\pi_P}),
\qquad
\tilde S_c(x)=\mathcal B(S_c^A(x),S_c^{\pi_S}(x)).
\tag{5}
\]

由于 Presence 会影响 instance 构造，更新 Presence 后必须重建 instance 图。令 admission 分数为 \(a\)，anchor 和候选 instance 图为

\[
I_A^{\tilde p}=\mathcal I(Q_A;\tilde p,a),
\qquad
I_{\pi_I}^{\tilde p}=\mathcal I(Q_{\pi_I};\tilde p,a),
\qquad
\tilde I_c=\mathcal B(I_A^{\tilde p},I_{\pi_I}^{\tilde p}),
\tag{6}
\]

其中 \(\mathcal I\) 表示式 (2) 的 query 聚合。角色组合后的类别证据为

\[
F_{\pi,c}(x)=\tilde p_c\max\bigl(\tilde S_c(x),\tilde I_c(x)\bigr).
\tag{7}
\]

在 native admission 下，\(a=\tilde p_c\)；在 anchor admission 下，只有 query 准入使用 \(a=p_c^A\)，instance 幅度和最终缩放仍使用更新后的 Presence。若所有 role 槽均为零，则更新退化为 anchor。

为了保留官方别名与 baseline 聚合顺序，我们保留官方分数场。令 \(G_v^{\mathrm{o}}\) 为观察 \(v\) 的官方类别图，\(F_{v,\pi}\) 为角色组合图，\(F_v^A\) 为无补充文本时的结构 anchor 组合。观察级输出为

\[
G_{v,\pi}=\operatorname{clip}_{[0,1]}\!\left(G_v^{\mathrm{o}}+F_{v,\pi}-F_v^A\right).
\tag{8}
\]

因此，关闭所有角色更新会精确返回官方图。该构造不是三个独立预测的集成：候选文本经过完整 grounding，只有其被分配 role 的输出改变 anchor，且 Presence 与 Instance 的原生耦合仍然存在。

### 3.3 对齐的 Local 与 Context 观察

文本描述可以要求连续表面或完整区域，却不能创造当前观察中不存在的视觉证据。Local 观察保留边界和小目标的有效采样密度；Context 观察提供更大范围的空间布局和长距离连续性。对于以坐标图块提供的数据集，Context 观察由空间对齐的邻接 RGB 图块组成，不使用邻接标签；其他数据集使用输入图像的扩大裁块。具体构造由实验协议给出。

每个观察独立完成原生 grounding 和角色组合。Local 与 Context 观察复用同一组已选角色配置；JRV 不会把 Presence 分配给一个视图、Semantic 分配给第二个视图、Instance 分配给第三个视图。对于视图族 \(v\in\{L,G\}\) 及其目标单元集合 \(\mathcal U_v\)，每个单元 \(u\) 在自己的坐标系中产生角色组合图 \(G_{u,\pi}\)。令 \(W_u\) 将图恢复到目标坐标，\(w_u(x)\) 表示有效覆盖。对齐后的视图证据为

\[
\overline G_{v,c}(x)=
\frac{\sum_{u\in\mathcal U_v}w_u(x)\,W_u[G_{u,\pi,c}](x)}
{\sum_{u\in\mathcal U_v}w_u(x)}.
\tag{9}
\]

最终类别分数场为

\[
Z_c(x)=\Psi_{\omega}\!\left(\overline G_{L,c}(x),\overline G_{G,c}(x)\right),
\qquad
\widehat Y=\mathcal D_{\mathrm{base}}(Z),
\tag{10}
\]

其中 \(\mathcal D_{\mathrm{base}}\) 保留 baseline 的 argmax 和背景阈值。视图算子 \(\Psi_{\omega}\) 是固定配置，不是学习式门控。我们使用逐元素最大值、Local 或 Context 单端点、加权幂平均以及加权 logit 融合：

\[
\Psi_{\max}(L,G)=\max(L,G),
\qquad
\Psi_{\rho,g}(L,G)=\left((1-g)L^{\rho}+gG^{\rho}\right)^{1/\rho},
\tag{11}
\]

\[
\Psi_{\mathrm{logit},g}(L,G)=\sigma\!\left((1-g)\operatorname{logit}(L)+g\operatorname{logit}(G)\right).
\tag{12}
\]

算子族是数据集 profile 的一部分，不是新的学习式 attention 模块。组合发生在完整类别分数场层面，因此角色和视图组合之后仍沿用原生跨类别决策。

### 3.4 推理协议与 Profile 定义

一个数据集 profile 是固定元组

\[
\pi=(s_P,s_S,s_I,a,\Psi_{\omega}),
\tag{13}
\]

其中 \(s_r\) 索引冻结文本库中的候选槽，\(s_r=0\) 表示保留 anchor；\(a\) 指定 native 或 anchor admission；\(\Psi_{\omega}\) 指定视图算子。同一 profile 应用于该 benchmark 的所有图像，并同时用于 Local 与 Context 观察。文本库和 profile 在推理前固定，SAM3 权重不更新。Profile 在数据集级别离线选择，实验部分报告选择协议，推理不使用逐图 GT 路由。

实现具有三个与实验对应的性质。第一，每条需要的补充文本都完成完整原生 grounding，而不是修改隔离的 decoder 状态。第二，未改变的槽或全零 role profile 会回到 anchor 路径，并保留官方别名聚合。第三，Local 与 Context 在完整角色组合和坐标恢复之后才组合，因此方法改变的是证据使用方式，而不是 SAM3 attention 或内部融合算子。
'''

# English method
(KIT/"sec"/"3_method.tex").write_text(en_method,encoding="utf-8",newline="\n")
main=(KIT/"main.tex").read_text(encoding="utf-8")
if '\\input{sec/3_method}' not in main:
    main=main.replace('\\input{sec/2_related_work}', '\\input{sec/2_related_work}\n\n\\input{sec/3_method}')
else:
    main=main.replace('\\input{sec/3_method}\n\n\\input{sec/2_related_work}', '\\input{sec/2_related_work}\n\n\\input{sec/3_method}')
main=(KIT/"main.tex").write_text(main,encoding="utf-8",newline="\n")

# Chinese method
raw=CN.read_bytes(); bom=raw.startswith(b'\xef\xbb\xbf'); text=raw.decode('utf-8-sig')
text=text.replace('*Introduction、Related Work、Method、Experiments 英文初稿的独立中文对照版。当前已整理 Introduction 与 Related Work；其余章节待补。', '*Introduction、Related Work、Method、Experiments 英文初稿的独立中文对照版。当前已整理 Introduction、Related Work 与 Method；其余章节待补。')
if '## 3. 方法' not in text:
    text=text.rstrip()+'\n\n'+cn_method.strip()+'\n'
else:
    start=text.index('## 3. 方法'); text=text[:start]+cn_method.strip()+'\n'
CN.write_text(text,encoding='utf-8-sig' if bom else 'utf-8',newline='\n')

mapping=ROOT/'中文论文'/'中英章节对应.md'
mt=mapping.read_text(encoding='utf-8-sig')
mt=mt.replace('| `论文中文版.md` / 方法 | `sec/3_method.tex` | 待整理 |', '| `论文中文版.md` / 方法 | `sec/3_method.tex` | 已完成 |')
mapping.write_text(mt,encoding='utf-8',newline='\n')
print('method written')
