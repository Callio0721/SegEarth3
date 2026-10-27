from pathlib import Path

root=Path(r"D:\论文\9.27论文")
intro=root/'author-kit-main'/'sec'/'1_intro.tex'
new_intro=r'''\section{Introduction}
\label{sec:introduction}

Open-vocabulary semantic segmentation (OVSS) assigns every pixel a category specified at inference time. Training-free methods adapt vision-language models to dense prediction \cite{R01,R06}. SAM3 instead conditions a shared grounding state on a text concept and exposes three readouts: Presence determines whether the concept occurs, Semantic estimates dense extent, and Instance organizes query-based regions \cite{R10}. SegEarth-OV3 applies this interface to remote sensing \cite{R11}. The shared state stabilizes category semantics, but the readouts need different evidence. In overhead scenes, small objects, continuous land cover, and scene-level existence are not captured equally well by one observation, and SAM3 presence and localization do not always improve together \cite{R24}. Figure~\ref{fig:motivation} summarizes this evidence-allocation problem.

Most existing methods adapt prompts or combine complete outputs. TMPA adjusts CLIP text embeddings \cite{R08}; ConceptBank evaluates candidate concepts with a support set \cite{R09}; ProC-SAM3 and CoCo-SAM3 fuse prompt-level evidence \cite{R12,R13}; RSGPNet refines SAM3 localization with geometric prompts \cite{R25}. A phrase is re-grounded through the full model, so it can improve dense coverage while changing presence or query organization. Replacing official class names also moves the ontology anchor. These methods operate at the category level even when their outputs affect several readouts.

Visual evidence imposes a second constraint. Local crops preserve detail but can cut long-range structure, whereas wider context exposes layout while undersampling small objects. Multi-resolution, cross-window, stitching, and scene-level inference methods exploit this complementarity \cite{R14,R15,R18,R26}, usually by changing attention, features, or a fixed fusion rule. For role-specific supplementation, the value of an observation also depends on which readout needs the missing evidence.

We introduce Joint Role--View Specialization (JRV). JRV keeps official names and aliases as an anchor, grounds role-functional candidates through the complete frozen SAM3 model, and applies only bounded corrections to their assigned readouts while preserving native Presence--Instance coupling. It then grounds aligned Local and Context observations with the same role profile and composes complete class-score fields before the original class decision. JRV does not modify SAM3 attention or give each head a separate visual path.

Our contributions are as follows:
\begin{itemize}[leftmargin=1.2em,itemsep=1pt,topsep=2pt]
  \item \textbf{Readout-level concept adaptation.} We introduce anchor-preserving Role-Functional Text. Supplementary descriptions are fully grounded, then used according to the responsibilities of Presence, Semantic, and Instance without replacing the official ontology or breaking Presence--Instance coupling.
  \item \textbf{Joint role--view specialization.} We treat role text and visual observation as joint conditions. One selected profile is reused across aligned Local and Context observations, and complete class-score fields are composed before argmax.
  \item \textbf{Evidence and scope.} On eight remote-sensing benchmarks, matched average mIoU rises from 53.56 to 55.82 with Role-only and 57.49 with Joint specialization. All datasets improve over the baseline, and six show positive Role--View interaction. Cityscapes and VOC20 test transfer and show that view composition remains distribution dependent.
\end{itemize}
'''
intro.write_text(new_intro,encoding='utf-8')

rw=root/'author-kit-main'/'sec'/'2_related_work.tex'
s=rw.read_text(encoding='utf-8')
s=s.replace(r'\subsection{Open-Vocabulary Segmentation: From Vision--Language Alignment to Concept Grounding}',r'\subsection{From OVSS to Concept Grounding}',1)
s=s.replace(r'\subsection{Concept Representation and Prompt Adaptation}',r'\subsection{Concept and Prompt Adaptation}',1)
s=s.replace(r'\subsection{Complementary Visual Observations and Context}',r'\subsection{Visual Observations and Context}',1)
rw.write_text(s,encoding='utf-8')

# Equation (12) needs a short transition.
method=root/'author-kit-main'/'sec'/'3_method.tex'
s=method.read_text(encoding='utf-8')
old=r'''\label{eq:view-operators}
\end{equation}
\begin{equation}
\Psi_{\mathrm{logit},g}(L,G)=\sigma\!\left((1-g)\operatorname{logit}(L)+g\operatorname{logit}(G)\right).'''
new=r'''\label{eq:view-operators}
\end{equation}
The logit variant uses the same mixture in log-odds space:
\begin{equation}
\Psi_{\mathrm{logit},g}(L,G)=\sigma\!\left((1-g)\operatorname{logit}(L)+g\operatorname{logit}(G)\right).'''
assert old in s
s=s.replace(old,new,1)
method.write_text(s,encoding='utf-8')

# Abstract code URL.
abstract=root/'author-kit-main'/'sec'/'0_abstract.tex'
s=abstract.read_text(encoding='utf-8')
s=s.replace('rather than treating additional text or larger visual fields as uniformly beneficial.',r'rather than treating additional text or larger visual fields as uniformly beneficial. Our code is available at \url{https://github.com/pengjunhao621-arch/SegEarth3}.',1)
abstract.write_text(s,encoding='utf-8')

# Experimental setup: hardware and first-occurrence dataset descriptions.
exp=root/'author-kit-main'/'sec'/'4_experiments.tex'
s=exp.read_text(encoding='utf-8')
old=r'''We use the same frozen SAM3 checkpoint and native grounding as the reproduced baseline. Candidate descriptions are generated offline and stored verbatim. Unless stated otherwise, $\alpha=0.5$ and $\tau=0.25$.'''
new=r'''Potsdam and Vaihingen are ISPRS airborne urban benchmarks; LoveDA covers urban and rural land cover from three Chinese cities; iSAID is a large aerial instance-segmentation dataset derived from DOTA; OpenEarthMap is a global high-resolution land-cover benchmark; UAVid focuses on oblique UAV urban scenes; UDD5 is built from semantic-constrained aerial structure-from-motion; and VDD emphasizes varied drone scenes and flight conditions. VOC20 contains the 20 PASCAL VOC foreground classes, and Cityscapes provides 19-class urban street-scene evaluation.

All experiments and inference were conducted on four NVIDIA RTX 3090 GPUs. The SAM3 weights remained frozen, and no model training or fine-tuning was performed. Candidate descriptions are generated offline and stored verbatim. Unless stated otherwise, $\alpha=0.5$ and $\tau=0.25$.'''
assert old in s
s=s.replace(old,new,1)

# Replace 4.6 lead-in and convert Table 5 to an inline table after explanatory text.
old=r'''\subsection{Natural-Image Evaluation and Scope}

Table~\ref{tab:natural} reports the natural-image transfer results under the same component definitions used in the remote-sensing evaluation.

\begin{table}[!htbp]
\centering
\caption{Natural-image evaluation (mIoU, \%). Role-only and view-only are separately selected optima; the table is not used to compute interaction. VOC20 uses the foreground vocabulary.}
\label{tab:natural}
\small
\setlength{\tabcolsep}{3pt}
\begin{tabular}{lcccccc}
\toprule
Dataset & Images & Baseline & Role & View & Joint & $\Delta$ \\
\midrule
VOC20~\cite{R44} & 1,449 & 96.89 & 97.00 & 97.00 & \textbf{97.11} & +0.22 \\
Cityscapes~\cite{R43} & 500 & 67.90 & \textbf{72.20} & 68.72 & \textbf{72.20} & +4.29 \\
\bottomrule
\end{tabular}
\end{table}'''
new=r'''\subsection{Natural-Image Evaluation and Scope}

Natural-image evaluation tests whether role supplementation transfers beyond overhead geometry and remote-sensing ontologies, while keeping the same frozen model and role definitions. VOC20 uses a 20-class foreground vocabulary, and Cityscapes evaluates 19 urban classes under a different scene distribution. We first report the joint result under the same component definitions, then separate the role and view effects.

\begin{center}
\centering
\captionsetup{hypcap=false}
\captionof{table}{Natural-image evaluation (mIoU, \%). Role-only and view-only are separately selected optima; the table is not used to compute interaction. VOC20 uses the foreground vocabulary.}
\label{tab:natural}
\captionsetup{hypcap=true}
\small
\setlength{\tabcolsep}{3pt}
\begin{tabular}{lcccccc}
\toprule
Dataset & Images & Baseline & Role & View & Joint & $\Delta$ \\
\midrule
VOC20~\cite{R44} & 1,449 & 96.89 & 97.00 & 97.00 & \textbf{97.11} & +0.22 \\
Cityscapes~\cite{R43} & 500 & 67.90 & \textbf{72.20} & 68.72 & \textbf{72.20} & +4.29 \\
\bottomrule
\end{tabular}
\end{center}'''
assert old in s
s=s.replace(old,new,1)
exp.write_text(s,encoding='utf-8')
print('English intro, subsection titles, hardware, datasets, abstract URL, and 4.6 updated')
