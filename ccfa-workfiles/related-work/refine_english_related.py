from pathlib import Path
ROOT=Path(r"D:\论文\9.27论文")
EN=ROOT/'Astra_docs'/'manuscript_v1'/'English_draft.md'
CN=ROOT/'Astra_docs'/'manuscript_v1'/'Chinese_draft.md'
OUT=ROOT/'ccfa-workfiles'/'related-work'/'bilingual-related-work.md'
en_section=r'''## 2. Related Work

### 2.1 Open-Vocabulary Segmentation: From Vision-Language Alignment to Concept Grounding

Vision-language pretraining specifies categories through text rather than a fixed classifier [1]. Applying this capability to segmentation requires category semantics at dense spatial resolution. Training-free methods reorganize pretrained representations. LPOSS propagates labels across patches and pixels [2]. CASS transfers object-context structure through spectral graph matching [3]. PEARL combines attention-space alignment with text-aware propagation [4]. Trained approaches instead improve region-text correspondence or cost aggregation, as in Mask-Adapter [5] and PCA-Seg [17]. These methods improve the spatial usability of a shared vision-language representation, but the intervention remains at the level of representation, matching, or aggregation.

Remote sensing adds variation in object scale, appearance, and dataset ontology. SegEarth-OV adapts CLIP through feature upsampling and global-bias mitigation [6]. ReAttnCLIP reorganizes patch and global-token attention [7]. ReSeg-CLIP uses hierarchical SAM-mask constraints and remote-sensing CLIP composition [28]. DinoSplat-OV combines DINOv3/DINO.txt propagation with test-time upsampling [27]. RSGPNet converts coarse SAM3 text masks into geometric prompts and verifies cross-scale consistency [25]. SkySense-O builds a vision-centric model through remote-sensing pretraining [21]. These methods address domain shift, prompt localization, or representation combination, generally within a unified prediction. Our work starts from a frozen concept-grounded baseline and studies how evidence should be used by different native readouts after grounding.

### 2.2 Concept Representation and Prompt Adaptation

Textual equivalence does not guarantee equivalent visual grounding. SynCLIP studies spatial inconsistencies across synonymous expressions [20]. TMPA generates context-aware descriptions and adapts CLIP text embeddings using high-confidence visual evidence and test-time entropy optimization [8]. ConceptBank builds visual prototypes from labeled support regions and evaluates concepts by their induced segmentation quality [9]. Promptable Concept Segmentation from Above evaluates zero-shot and one-shot SAM3 in overhead imagery and identifies a gap between concept presence and localization [24]. These approaches implement category adaptation through candidate generation, embedding updates, or support prototypes, and their adaptation unit remains primarily the category or concept.

SAM3 turns text prompts into shared concept grounding and exposes category presence and spatial masks through a presence head and segmentation readouts [10]. SegEarth-OV3 organizes its semantic, instance, and presence outputs for remote-sensing OVSS [11]. ProC-SAM3 constructs a constrained prompt pool and adds a gated nonnegative instance advantage to a semantic base [12]. CoCo-SAM3 aggregates synonymous concept evidence and calibrates competition among independently prompted categories [13]. These methods improve prompt coverage, concept boundaries, or output fusion. We retain the official category anchor and complete grounding, allocate supplementary text according to the computational roles of Presence, Semantic, and Instance, and configure these roles jointly with visual observations. The closest comparator, ProC-SAM3, performs prompt-level fusion on a semantic base. Our distinction is readout-specific evidence use.

### 2.3 Complementary Visual Observations and Context

Detail and context form a basic trade-off in dense prediction. HRDA combines high-resolution detail crops with lower-resolution context predictions through learned scale attention [18]. SegMAN models multi-scale contextual dependencies within one segmentation network [23], and F2Net uses frequency decomposition for ultra-high-resolution remote-sensing segmentation [19]. In training-free open-vocabulary segmentation, GLA-CLIP extends cross-window attention keys and values to exchange global information [14]. OV-Stitcher stitches cross-window Q/K/V and incorporates class-biased text prompts [15]. ConInfer aggregates scene and tile features and calibrates predictions through iterative consensus [26]. DPSeg uses visual prompts alongside text in cost-volume learning [16], while MM-OVSeg obtains complementary evidence from registered optical and SAR imagery [22]. These works show that context and multimodal observations provide useful evidence, and fusion generally occurs in pretrained attention, a feature space, or a fixed output rule.

We use neither an auxiliary modality nor a modified SAM3 attention operator. For the same target region, we construct spatially aligned Local and Context observations from RGB data, ground each observation with the same frozen SAM3 model, and reuse one selected role profile across both. Their complete class-score fields are then composed in the target coordinate system. The resulting question is how role-specific textual supplementation changes the value of a visual observation and when the two form complementary evidence. GLA-CLIP and OV-Stitcher already combine context with text for training-free OVSS. Our distinction lies in jointly organizing evidence across native SAM3 readout responsibilities and observation conditions, not in context or text-vision collaboration itself.
'''
raw=EN.read_bytes(); bom=raw.startswith(b'\xef\xbb\xbf'); text=raw.decode('utf-8-sig')
s=text.index('## 2. Related Work'); e=text.index('## 3. Method',s)
text=text[:s]+en_section.rstrip()+'\n\n'+text[e:]
EN.write_text(text,encoding='utf-8-sig' if bom else 'utf-8',newline='\n')
cn=CN.read_text(encoding='utf-8-sig'); cs=cn.index('## 2. 相关工作'); ce=cn.index('## 3. 方法',cs); cn_sec=cn[cs:ce].rstrip()
OUT.write_text('# 双语相关工作\n\n'+cn_sec+'\n\n---\n\n'+en_section.rstrip()+'\n',encoding='utf-8',newline='\n')
print('updated',EN,OUT)
