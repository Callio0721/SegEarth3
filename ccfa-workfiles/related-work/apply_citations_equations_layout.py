from pathlib import Path
import re
root=Path(r"D:\论文\9.27论文")
rw_path=root/'author-kit-main'/'sec'/'2_related_work.tex'
exp_path=root/'author-kit-main'/'sec'/'4_experiments.tex'
method_path=root/'author-kit-main'/'sec'/'3_method.tex'

# ---------- Related Work ----------
rw=rw_path.read_text(encoding='utf-8')
old='''Vision-language pretraining specifies categories through text rather than a fixed classifier \\cite{R01}. Applying this capability to segmentation requires category semantics at dense spatial resolution. Training-free methods reorganize pretrained representations. LPOSS propagates labels across patches and pixels \\cite{R02}. CASS transfers object--context structure through spectral graph matching \\cite{R03}. PEARL combines attention-space alignment with text-aware propagation \\cite{R04}. Trained approaches instead improve region--text correspondence or cost aggregation, as in Mask-Adapter \\cite{R05} and PCA-Seg \\cite{R17}. These methods improve the spatial usability of a shared vision-language representation, but the intervention remains at the level of representation, matching, or aggregation.'''
new='''Vision-language pretraining specifies categories through text rather than a fixed classifier \\cite{R01}. Early open-vocabulary models learn text-supervised grouping or adapt masked regions to CLIP, as in GroupViT \\cite{R45} and OVSeg \\cite{R46}. Training-free dense methods subsequently reorganize pretrained CLIP representations: SCLIP modifies self-attention \\cite{R29}, ClearCLIP decomposes final-layer representations \\cite{R30}, ProxyCLIP injects spatial proxy attention from a vision foundation model \\cite{R31}, and ResCLIP reuses residual cross-correlation attention \\cite{R47}. Trained dense predictors instead learn cost aggregation or encoder--decoder fusion, as in CAT-Seg \\cite{R48} and SED \\cite{R49}. Applying these representations to segmentation still requires category semantics at dense spatial resolution. Training-free label propagation moves class evidence across patches and pixels \\cite{R02}; CASS transfers object--context structure through spectral graph matching \\cite{R03}; PEARL combines attention-space alignment with text-aware propagation \\cite{R04}. Other trained approaches improve region--text correspondence or cost aggregation, as in Mask-Adapter \\cite{R05} and PCA-Seg \\cite{R17}. These methods improve the spatial usability of a shared vision-language representation, but the intervention remains at the level of representation, matching, or aggregation.'''
assert old in rw
rw=rw.replace(old,new,1)
old='''These approaches implement category adaptation through candidate generation, embedding updates, or support prototypes, and their adaptation unit remains primarily the category or concept.'''
new='''AVION verifies LLM-generated aerial descriptions with visual prototypes and distills them into prompt-tuned encoders \\cite{R50}; it therefore involves training. The Power of Prior uses LLaVA-derived spatial priors to guide SAM prompts without task-specific fine-tuning \\cite{R51}. These approaches implement category adaptation through candidate generation, embedding updates, or support prototypes, and their adaptation unit remains primarily the category or concept.'''
assert old in rw
rw=rw.replace(old,new,1)
old='''ProC-SAM3 constructs a constrained prompt pool and adds a gated nonnegative instance advantage to a semantic base \\cite{R12}. CoCo-SAM3 aggregates synonymous concept evidence and calibrates competition among independently prompted categories \\cite{R13}. These methods improve prompt coverage, concept boundaries, or output fusion.'''
new='''ProC-SAM3 constructs a constrained prompt pool and adds a gated nonnegative instance advantage to a semantic base \\cite{R12}. CoCo-SAM3 aggregates synonymous concept evidence and calibrates competition among independently prompted categories \\cite{R13}. ActiveSAM keeps SAM3 frozen and restricts full-resolution decoding to an image-conditioned active vocabulary \\cite{R35}; it targets inference efficiency and vocabulary pruning rather than readout-specific evidence allocation. These methods improve prompt coverage, inference efficiency, concept boundaries, or output fusion.'''
assert old in rw
rw=rw.replace(old,new,1)
rw_path.write_text(rw,encoding='utf-8')

# ---------- Method equations ----------
method=method_path.read_text(encoding='utf-8')
old=r'''\begin{equation}
Q_c=\{q:a_c r_{cq}>\eta\},
\qquad
I_c(x)=\max_{q\in Q_c}M_{cq}(x)r_{cq}p_c.
\label{eq:instance}
\end{equation}'''
new=r'''\begin{equation}
\begin{aligned}
Q_c&=\{q:a_c r_{cq}>\eta\},\\
I_c(x)&=\max_{q\in Q_c}M_{cq}(x)r_{cq}p_c.
\end{aligned}
\label{eq:instance}
\end{equation}'''
assert old in method
method=method.replace(old,new,1)
old=r'''\begin{equation}
\tilde p_c=\mathcal B(p_c^A,p_c^{\pi_P}),
\qquad
\tilde S_c(x)=\mathcal B(S_c^A(x),S_c^{\pi_S}(x)).
\label{eq:role-updates}
\end{equation}'''
new=r'''\begin{equation}
\begin{aligned}
\tilde p_c&=\mathcal B(p_c^A,p_c^{\pi_P}),\\
\tilde S_c(x)&=\mathcal B(S_c^A(x),S_c^{\pi_S}(x)).
\end{aligned}
\label{eq:role-updates}
\end{equation}'''
assert old in method
method=method.replace(old,new,1)
old=r'''\begin{equation}
I_A^{\tilde p}=\mathcal I(Q_A;\tilde p,a),
\qquad
I_{\pi_I}^{\tilde p}=\mathcal I(Q_{\pi_I};\tilde p,a),
\qquad
\tilde I_c=\mathcal B(I_A^{\tilde p},I_{\pi_I}^{\tilde p}),
\label{eq:instance-rebuild}
\end{equation}'''
new=r'''\begin{equation}
\begin{aligned}
I_A^{\tilde p}&=\mathcal I(Q_A;\tilde p,a),\\
I_{\pi_I}^{\tilde p}&=\mathcal I(Q_{\pi_I};\tilde p,a),\\
\tilde I_c&=\mathcal B(I_A^{\tilde p},I_{\pi_I}^{\tilde p}),
\end{aligned}
\label{eq:instance-rebuild}
\end{equation}'''
assert old in method
method=method.replace(old,new,1)
old=r'''\begin{equation}
Z_c(x)=\Psi_{\omega}\!\left(\overline G_{L,c}(x),\overline G_{G,c}(x)\right),
\qquad
\widehat Y=\mathcal D_{\mathrm{base}}(Z),
\label{eq:view-fusion}
\end{equation}'''
new=r'''\begin{equation}
\begin{aligned}
Z_c(x)&=\Psi_{\omega}\!\left(\overline G_{L,c}(x),\overline G_{G,c}(x)\right),\\
\widehat Y&=\mathcal D_{\mathrm{base}}(Z),
\end{aligned}
\label{eq:view-fusion}
\end{equation}'''
assert old in method
method=method.replace(old,new,1)
method_path.write_text(method,encoding='utf-8')

# ---------- Experiments ----------
exp=exp_path.read_text(encoding='utf-8')
old=r'''We evaluate on the eight remote-sensing benchmarks used by SegEarth-OV and SegEarth-OV3 \cite{R06,R11}: Potsdam, Vaihingen, LoveDA, iSAID, OpenEarthMap (OEM), UAVid, UDD5, and VDD. We retain the baseline evaluation splits, class mappings, ignored labels, and image-based UAVid protocol. iSAID contains 11,644 processed validation tiles, and UAVid contains 1,020 evaluated patches. The primary metric is mean intersection over union (mIoU, \%). The overall average weights the eight datasets equally. Class-group analysis weights dataset--class pairs equally and is reported separately. VOC20 and Cityscapes provide additional natural-image evaluations.'''
new=r'''We evaluate on the eight remote-sensing benchmarks used by SegEarth-OV and SegEarth-OV3 \cite{R06,R11}: Potsdam and Vaihingen \cite{R42}, LoveDA \cite{R36}, iSAID \cite{R37}, OpenEarthMap (OEM) \cite{R38}, UAVid \cite{R39}, UDD5 \cite{R40}, and VDD \cite{R41}. We retain the baseline evaluation splits, class mappings, ignored labels, and image-based UAVid protocol. iSAID contains 11,644 processed validation tiles, and UAVid contains 1,020 evaluated patches. The primary metric is mean intersection over union (mIoU, \%). The overall average weights the eight datasets equally. Class-group analysis weights dataset--class pairs equally and is reported separately. VOC20 \cite{R44} and Cityscapes \cite{R43} provide additional natural-image evaluations.'''
assert old in exp
exp=exp.replace(old,new,1)

# Extract main table block, replace with strip block, and move before 4.2.
m=re.search(r'\\begin\{table\*\}\[t\].*?\\end\{table\*\}',exp,re.S)
assert m
block=m.group(0)
exp=exp[:m.start()]+exp[m.end():]
block=block.replace(r'\begin{table*}[t]',r'\begin{strip}',1)
block=block.replace(r'\end{table*}',r'\end{strip}',1)
old_caption=r'''\caption{Remote-sensing open-vocabulary semantic segmentation (mIoU, \%). Competitor rows follow the reported values in ProC-SAM3 \cite{R12}; the SegEarth-OV3 row is our reproduction, and JRV is evaluated with the context-access protocol described in Section~\ref{sec:experiments}. Avg. is the equal-weight mean over eight datasets. Published one-decimal values are kept at their reported precision.}'''
new_caption=r'''\captionsetup{hypcap=false}
\captionof{table}{Remote-sensing open-vocabulary semantic segmentation (mIoU, \%). Method names cite their original papers. Competitor metrics follow the comparison in ProC-SAM3 \cite{R12}; published values may correspond to the versions used there. The SegEarth-OV3 row is our reproduction, and JRV uses the context-access protocol in Section~\ref{sec:experiments}. Dataset sources are cited in Section~\ref{sec:experiments}. Avg. is the equal-weight mean over eight datasets, and published values retain their reported precision.}
\captionsetup{hypcap=true}'''
assert old_caption in block
block=block.replace(old_caption,new_caption,1)
# Method citations.
row_repls={
r'VIP & DINOv3 + dino.txt':r'VIP~\cite{R32} & DINOv3 + dino.txt',
r'SCLIP & CLIP':r'SCLIP~\cite{R29} & CLIP',
r'ClearCLIP & CLIP':r'ClearCLIP~\cite{R30} & CLIP',
r'ProxyCLIP & CLIP + DINOv2':r'ProxyCLIP~\cite{R31} & CLIP + DINOv2',
r'SegEarth-OV & CLIP':r'SegEarth-OV~\cite{R06} & CLIP',
r'RSCLIP & CLIP':r'RSCLIP~\cite{R33} & CLIP',
r'CorrCLIP & CLIP + DINO + SAM2':r'CorrCLIP~\cite{R34} & CLIP + DINO + SAM2',
r'ConInfer & CLIP + DINOv3':r'ConInfer~\cite{R26} & CLIP + DINOv3',
r'ReAttnCLIP & CLIP':r'ReAttnCLIP~\cite{R07} & CLIP',
r'ActiveSAM & SAM3':r'ActiveSAM~\cite{R35} & SAM3',
r'SegEarth-OV3 (reproduced) & SAM3':r'SegEarth-OV3 (reproduced)~\cite{R11} & SAM3',
r'ProC-SAM3 & SAM3':r'ProC-SAM3~\cite{R12} & SAM3',
}
for a,b in row_repls.items():
    assert a in block, a
    block=block.replace(a,b,1)
# Insert table at the end of 4.1, before 4.2 heading.
marker=r'\subsection{Comparison with Existing Methods}'
assert marker in exp
exp=exp.replace(marker,'\n'+block+'\n\n'+marker,1)

# 4.3 lead-in before Table 2; update caption and following paragraph.
old=r'''\subsection{Functional Use of Supplementary Text}

\begin{center}'''
new=r'''\subsection{Functional Use of Supplementary Text}

We first separate the two stages of the final system under a fixed inference recipe. Table~\ref{tab:component-progression} reports the macro progression over the eight benchmarks and establishes the language-evidence stage before the matched interaction analysis.

\begin{center}'''
assert old in exp
exp=exp.replace(old,new,1)
old=r'''\captionof{table}{Macro component progression. Role-only is the best recorded independent role profile; it is not the matched Role condition used for interaction analysis.}'''
new=r'''\captionof{table}{Macro component progression. Stage entries refer to the configurations defined in Section~3; Role-only is the best recorded independent role profile and is not the matched Role condition used for interaction analysis.}'''
assert old in exp
exp=exp.replace(old,new,1)
old=r'''Table~\ref{tab:component-progression} separates the two stages of the final system. Role-only improves every dataset over the matched baseline, including gains of 6.23 on OEM and 4.92 on UAVid.'''
new=r'''Across the sequence, Role-only improves every dataset over the matched baseline, including gains of 6.23 on OEM and 4.92 on UAVid.'''
assert old in exp
exp=exp.replace(old,new,1)

# Lead-in before Table 3.
old=r'''\begin{center}
\centering
{\captionsetup{hypcap=false}
\captionof{table}{The same semantic-oriented candidate used either only for Semantic supplementation or for all three roles. Both variants retain the anchor and bounded update; values are final mIoU.}
}'''
new=r'''We next hold the role slots and admission mode fixed and ask how the same semantic-oriented candidate should be used. Table~\ref{tab:role-use} compares Semantic-only supplementation with sharing that candidate across Presence, Semantic, and Instance.

\begin{center}
\centering
{\captionsetup{hypcap=false}
\captionof{table}{The same semantic-oriented candidate used either only for Semantic supplementation or for all three roles. Both variants retain the anchor and bounded update; values are final mIoU.}
}'''
assert old in exp
exp=exp.replace(old,new,1)
exp_path.write_text(exp,encoding='utf-8')
print('English related work, method equations, and experiments updated.')
