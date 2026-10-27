from pathlib import Path

ROOT = Path(r"D:\论文\9.27论文")
WORK = ROOT / "ccfa-workfiles" / "related-work"
CN = ROOT / "Astra_docs" / "manuscript_v1" / "Chinese_draft.md"
EN = ROOT / "Astra_docs" / "manuscript_v1" / "English_draft.md"
REFS = ROOT / "Astra_docs" / "manuscript_v1" / "references.md"
BIB = ROOT / "Astra_docs" / "manuscript_v1" / "references.bib"
OUT = WORK / "bilingual-related-work.md"

cn_section = r'''## 2. 相关工作

### 2.1 开放词汇分割：从图文对齐到概念定位

视觉—语言预训练使模型能够通过文本指定类别，而不必依赖固定分类头 [1]。将这种能力应用到语义分割，需要在稠密空间恢复类别语义。免训练方法通过重排预训练表征缩小这一差距：LPOSS 在图像块和像素之间传播标签 [2]；CASS 利用谱图匹配迁移对象—上下文结构 [3]；PEARL 结合注意力空间对齐和文本感知传播 [4]。训练式方法则优化区域—文本对应或代价聚合，如 Mask-Adapter [5] 和 PCA-Seg [17]。这些方法提高了统一视觉—语言表征的空间可用性，但主要作用于表征、匹配或聚合本身。

遥感数据进一步带来尺度、外观与数据集 ontology 的差异。SegEarth-OV 通过特征上采样和全局偏置处理适配 CLIP [6]，ReAttnCLIP 重组图像块间及全局 token 的注意力 [7]，ReSeg-CLIP 用分层 SAM mask 约束 CLIP 的图像块交互并组合多个遥感 CLIP 模型 [28]，DinoSplat-OV 利用 DINOv3/DINO.txt 的文本感知传播和测试时上采样 [27]，RSGPNet 将 SAM3 的文本粗 mask 转为几何提示并做一致性校验 [25]，SkySense-O 则通过遥感预训练构建视觉中心模型 [21]。这些方法处理域差异、提示定位或表征组合，通常在统一预测层面改进结果。本文从冻结的概念定位基线出发，研究 grounding 后不同读出职责如何使用补充证据。

### 2.2 概念表示与提示适配

语言表达的等价并不保证视觉定位等价。SynCLIP 研究同义表达引起的空间响应差异 [20]；TMPA 依据当前图像生成上下文描述，并用高置信视觉证据和测试时熵优化调整 CLIP 文本嵌入 [8]；ConceptBank 从带标注支持区域构建视觉原型，并按候选概念诱导的分割质量进行评价和融合 [9]；Promptable Concept Segmentation from Above 在俯视场景中评估 SAM3 的零样本与单样本能力，指出其概念存在性与定位表现之间的差异 [24]。这些工作把类别适配落实为候选概念生成、嵌入更新或支持集原型构建，适配单元仍主要是类别或概念。

SAM3 将文本 prompt 转化为共享的概念 grounding，并由 presence head 和分割读出产生类别存在性与空间 mask [10]。SegEarth-OV3 将 semantic、instance 与 presence 输出组织为遥感 OVSS 的融合链路 [11]。ProC-SAM3 构造受约束的提示池，并在语义预测上加入门控的非负实例优势 [12]；CoCo-SAM3 聚合同义概念证据并校准独立类别提示之间的竞争 [13]。这些方法改善提示覆盖、概念边界或输出融合。本文保留官方类别 anchor 与完整 grounding，按 Presence、Semantic、Instance 三类读出的职责分配补充文本，再与视觉观察共同配置。最接近的 ProC-SAM3 以语义预测为基本盘进行提示级融合；本文的区分点是 readout-specific evidence use。

### 2.3 互补视觉观察与上下文

细节与上下文构成密集预测中的基本权衡。HRDA 将高分辨率细节裁块与低分辨率上下文预测通过可学习尺度注意力结合 [18]；SegMAN 在单网络内建模多尺度上下文依赖 [23]；F2Net 通过频率分解处理超高分辨率遥感分割 [19]。在免训练开放词汇分割中，GLA-CLIP 扩展跨窗口注意力的 key/value 以交换全局信息 [14]；OV-Stitcher 拼接跨窗口 Q/K/V，并引入类别偏置文本提示 [15]；ConInfer 汇集场景与图块特征，通过迭代共识校准预测 [26]；DPSeg 在代价体中同时使用视觉提示和文本提示 [16]；MM-OVSeg 从配准的光学与 SAR 图像中获取互补证据 [22]。这些方法说明上下文和多模态观察均能提供有效信息，其融合通常发生在预训练注意力、特征空间或固定的输出聚合规则中。

本文不使用辅助传感器，也不修改 SAM3 的内部注意力。对于同一目标区域，我们从 RGB 图像构造空间对齐的 Local 与 Context 观察，每个观察分别完成冻结 SAM3 concept grounding，并复用同一已选角色配置。随后在目标坐标上组合完整类别分数场。研究问题是角色化文本补充如何改变不同视觉观察的价值，以及二者何时形成互补。GLA-CLIP 和 OV-Stitcher 已将上下文与文本结合用于免训练 OVSS，因此本文的差异落在 SAM3 原生读出职责与观察条件的联合证据组织，而不是上下文或文本—视觉协作本身。
'''

en_section = r'''## 2. Related Work

### 2.1 Open-Vocabulary Segmentation: From Vision-Language Alignment to Concept Grounding

Vision-language pretraining specifies categories through text rather than a fixed classifier [1]. Applying this capability to segmentation requires category semantics at dense spatial resolution. Training-free methods reorganize pretrained representations: LPOSS propagates labels across patches and pixels [2], CASS transfers object-context structure through spectral graph matching [3], and PEARL combines attention-space alignment with text-aware propagation [4]. Trained approaches instead improve region-text correspondence or cost aggregation, as in Mask-Adapter [5] and PCA-Seg [17]. These methods improve the spatial usability of a shared vision-language representation, but the intervention remains at the level of representation, matching, or aggregation.

Remote sensing adds variation in object scale, appearance, and dataset ontology. SegEarth-OV adapts CLIP through feature upsampling and global-bias mitigation [6]; ReAttnCLIP reorganizes patch and global-token attention [7]; ReSeg-CLIP uses hierarchical SAM-mask constraints and remote-sensing CLIP composition [28]; DinoSplat-OV combines DINOv3/DINO.txt propagation with test-time upsampling [27]; RSGPNet converts coarse SAM3 text masks into geometric prompts and verifies cross-scale consistency [25]; and SkySense-O builds a vision-centric model through remote-sensing pretraining [21]. These methods address domain shift, prompt localization, or representation combination, generally within a unified prediction. Our work starts from a frozen concept-grounded baseline and studies how evidence should be used by different native readouts after grounding.

### 2.2 Concept Representation and Prompt Adaptation

Textual equivalence does not guarantee equivalent visual grounding. SynCLIP studies spatial inconsistencies across synonymous expressions [20]. TMPA generates context-aware descriptions and adapts CLIP text embeddings using high-confidence visual evidence and test-time entropy optimization [8]. ConceptBank builds visual prototypes from labeled support regions and evaluates concepts by their induced segmentation quality [9]. Promptable Concept Segmentation from Above evaluates zero-shot and one-shot SAM3 in overhead imagery and identifies a gap between concept presence and localization [24]. These approaches implement category adaptation through candidate generation, embedding updates, or support prototypes; their adaptation unit remains primarily the category or concept.

SAM3 turns text prompts into shared concept grounding and exposes category presence and spatial masks through a presence head and segmentation readouts [10]. SegEarth-OV3 organizes its semantic, instance, and presence outputs for remote-sensing OVSS [11]. ProC-SAM3 constructs a constrained prompt pool and adds a gated nonnegative instance advantage to a semantic base [12], while CoCo-SAM3 aggregates synonymous concept evidence and calibrates competition among independently prompted categories [13]. These methods improve prompt coverage, concept boundaries, or output fusion. We retain the official category anchor and complete grounding, allocate supplementary text according to the computational roles of Presence, Semantic, and Instance, and configure these roles jointly with visual observations. The closest comparator, ProC-SAM3, performs prompt-level fusion on a semantic base; our distinction is readout-specific evidence use.

### 2.3 Complementary Visual Observations and Context

Detail and context form a basic trade-off in dense prediction. HRDA combines high-resolution detail crops with lower-resolution context predictions through learned scale attention [18]. SegMAN models multi-scale contextual dependencies within one segmentation network [23], and F2Net uses frequency decomposition for ultra-high-resolution remote-sensing segmentation [19]. In training-free open-vocabulary segmentation, GLA-CLIP extends cross-window attention keys and values to exchange global information [14]. OV-Stitcher stitches cross-window Q/K/V and incorporates class-biased text prompts [15]. ConInfer aggregates scene and tile features and calibrates predictions through iterative consensus [26]. DPSeg uses visual prompts alongside text in cost-volume learning [16], while MM-OVSeg obtains complementary evidence from registered optical and SAR imagery [22]. These works show that context and multimodal observations provide useful evidence; fusion generally occurs in pretrained attention, a feature space, or a fixed output rule.

We use neither an auxiliary modality nor a modified SAM3 attention operator. For the same target region, we construct spatially aligned Local and Context observations from RGB data, ground each observation with the same frozen SAM3 model, and reuse one selected role profile across both. Their complete class-score fields are then composed in the target coordinate system. The resulting question is how role-specific textual supplementation changes the value of a visual observation and when the two form complementary evidence. GLA-CLIP and OV-Stitcher already combine context with text for training-free OVSS; our distinction lies in jointly organizing evidence across native SAM3 readout responsibilities and observation conditions, not in context or text-vision collaboration itself.
'''

refs_addition = r'''
<a id="r24"></a>

[24] Dabaja, Mohammad and Celik, Turgay. [Promptable Concept Segmentation from Above: Evaluating SAM 3's Zero-Shot and One-Shot Capabilities in Remote Sensing](https://arxiv.org/abs/2607.09583). arXiv preprint arXiv:2607.09583, 2026.

<a id="r25"></a>

[25] Wang, Shanwen and Sun, Xin and Wang, Sirui and Zhu, Xiao Xiang. [RSGPNet: Geometric Prompting for Remote Sensing Open-Vocabulary Semantic Segmentation](https://arxiv.org/abs/2606.28410). arXiv preprint arXiv:2606.28410, 2026.

<a id="r26"></a>

[26] Chen, Wenyang and Hu, Zhanxuan and Zhang, Yaping and Ning, Hailong and Tai, Yonghang. [ConInfer: Context-Aware Inference for Training-Free Open-Vocabulary Remote Sensing Segmentation](https://openaccess.thecvf.com/content/CVPR2026F/html/Chen_ConInfer_Context-Aware_Inference_for_Training-Free_Open-Vocabulary_Remote_Sensing_Segmentation_CVPRF_2026_paper.html). Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR) Findings, 2026.

<a id="r27"></a>

[27] Zhao, Changhao and Li, Haoxiang and Li, Yuke and Liu, Hai and Zeng, LingLin. [Standalone DINOv3 for Remote Sensing Training-Free Open-Vocabulary Semantic Segmentation](https://arxiv.org/abs/2608.03023). arXiv preprint arXiv:2608.03023, 2026.

<a id="r28"></a>

[28] Heidarianbaei, Mohammadreza and Dorozynski, Mareike and Kanyamahanga, Hubert and Mehltretter, Max and Rottensteiner, Franz. [Open-Vocabulary Semantic Segmentation in Remote Sensing via Hierarchical Attention Masking and Model Composition](https://arxiv.org/abs/2602.23869). arXiv preprint arXiv:2602.23869, 2026.
'''

bib_addition = r'''
@article{R24,
    author  = {Dabaja, Mohammad and Celik, Turgay},
    title   = {Promptable Concept Segmentation from Above: Evaluating SAM 3's Zero-Shot and One-Shot Capabilities in Remote Sensing},
    journal = {arXiv preprint arXiv:2607.09583},
    year    = {2026},
    url     = {https://arxiv.org/abs/2607.09583}
}

@article{R25,
    author  = {Wang, Shanwen and Sun, Xin and Wang, Sirui and Zhu, Xiao Xiang},
    title   = {RSGPNet: Geometric Prompting for Remote Sensing Open-Vocabulary Semantic Segmentation},
    journal = {arXiv preprint arXiv:2606.28410},
    year    = {2026},
    url     = {https://arxiv.org/abs/2606.28410}
}

@InProceedings{R26,
    author    = {Chen, Wenyang and Hu, Zhanxuan and Zhang, Yaping and Ning, Hailong and Tai, Yonghang},
    title     = {ConInfer: Context-Aware Inference for Training-Free Open-Vocabulary Remote Sensing Segmentation},
    booktitle = {Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR) Findings},
    year      = {2026},
    url       = {https://openaccess.thecvf.com/content/CVPR2026F/html/Chen_ConInfer_Context-Aware_Inference_for_Training-Free_Open-Vocabulary_Remote_Sensing_Segmentation_CVPRF_2026_paper.html}
}

@article{R27,
    author  = {Zhao, Changhao and Li, Haoxiang and Li, Yuke and Liu, Hai and Zeng, LingLin},
    title   = {Standalone DINOv3 for Remote Sensing Training-Free Open-Vocabulary Semantic Segmentation},
    journal = {arXiv preprint arXiv:2608.03023},
    year    = {2026},
    url     = {https://arxiv.org/abs/2608.03023}
}

@article{R28,
    author  = {Heidarianbaei, Mohammadreza and Dorozynski, Mareike and Kanyamahanga, Hubert and Mehltretter, Max and Rottensteiner, Franz},
    title   = {Open-Vocabulary Semantic Segmentation in Remote Sensing via Hierarchical Attention Masking and Model Composition},
    journal = {arXiv preprint arXiv:2602.23869},
    year    = {2026},
    url     = {https://arxiv.org/abs/2602.23869}
}
'''

def read_text(path):
    raw = path.read_bytes()
    bom = raw.startswith(b'\xef\xbb\xbf')
    return raw.decode('utf-8-sig'), bom

def write_text(path, text, bom=False):
    path.write_text(text, encoding='utf-8-sig' if bom else 'utf-8', newline='\n')

def replace_section(text, start_marker, end_marker, replacement):
    start = text.find(start_marker)
    if start < 0:
        raise RuntimeError(f'Missing start marker: {start_marker}')
    end = text.find(end_marker, start + len(start_marker))
    if end < 0:
        raise RuntimeError(f'Missing end marker: {end_marker}')
    return text[:start] + replacement.rstrip() + '\n\n' + text[end:]

cn, cn_bom = read_text(CN)
en, en_bom = read_text(EN)
cn_new = replace_section(cn, '## 2. 相关工作', '## 3. 方法', cn_section)
en_new = replace_section(en, '## 2. Related Work', '## 3. Method', en_section)
write_text(CN, cn_new, cn_bom)
write_text(EN, en_new, en_bom)

refs, refs_bom = read_text(REFS)
if '<a id="r24"></a>' not in refs:
    refs = refs.rstrip() + '\n' + refs_addition
write_text(REFS, refs, refs_bom)

bib = BIB.read_text(encoding='utf-8')
if '@article{R24' not in bib:
    bib = bib.rstrip() + '\n' + bib_addition
BIB.write_text(bib, encoding='utf-8', newline='\n')

OUT.write_text('# 双语相关工作\n\n' + cn_section + '\n\n---\n\n' + en_section, encoding='utf-8', newline='\n')
print({
    'chinese_chars': len(cn_new),
    'english_chars': len(en_new),
    'references_chars': len(refs),
    'bib_chars': len(bib),
    'bilingual_output': str(OUT),
})
