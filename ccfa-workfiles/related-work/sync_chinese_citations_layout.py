from pathlib import Path
import re
p=Path(r"D:\论文\9.27论文\中文论文\论文中文版.md")
s=p.read_text(encoding='utf-8')

old='''视觉—语言预训练使模型能够通过文本指定类别，而不必依赖固定分类头 [1]。将这种能力应用到语义分割，需要在稠密空间恢复类别语义。免训练方法通过重排预训练表征缩小这一差距：LPOSS 在图像块和像素之间传播标签 [2]；CASS 利用谱图匹配迁移对象—上下文结构 [3]；PEARL 结合注意力空间对齐和文本感知传播 [4]。训练式方法则优化区域—文本对应或代价聚合，如 Mask-Adapter [5] 和 PCA-Seg [17]。这些方法提高了统一视觉—语言表征的空间可用性，但主要作用于表征、匹配或聚合本身。'''
new='''视觉—语言预训练使模型能够通过文本指定类别，而不必依赖固定分类头 [1]。GroupViT 通过文本监督学习分层语义分组 [45]，OVSeg 将掩码区域适配到 CLIP 进行开放词汇分类 [46]。免训练稠密方法随后重组 CLIP 表征：SCLIP 修改自注意力 [29]，ClearCLIP 分解最后一层表征 [30]，ProxyCLIP 引入视觉基础模型的代理注意力 [31]，ResCLIP 复用残差交叉相关注意力 [47]。训练式方法则学习代价聚合或编码器—解码器融合，如 CAT-Seg [48] 和 SED [49]。将上述表征用于分割仍需在稠密空间恢复类别语义：LPOSS 在图像块和像素之间传播标签 [2]；CASS 利用谱图匹配迁移对象—上下文结构 [3]；PEARL 结合注意力空间对齐和文本感知传播 [4]。其他训练式方法改进区域—文本对应或代价聚合，如 Mask-Adapter [5] 和 PCA-Seg [17]。这些方法提高了统一视觉—语言表征的空间可用性，但主要作用于表征、匹配或聚合本身。'''
assert old in s
s=s.replace(old,new,1)

old='''这些工作把类别适配落实为候选概念生成、嵌入更新或支持集原型构建，适配单元仍主要是类别或概念。'''
new='''AVION 用视觉原型筛选大语言模型生成的航空描述，再蒸馏到提示调优编码器中 [50]，因此包含训练过程；The Power of Prior 使用 LLaVA 的空间先验引导 SAM 提示，不进行任务特定微调 [51]。这些工作把类别适配落实为候选概念生成、嵌入更新或支持集原型构建，适配单元仍主要是类别或概念。'''
assert old in s
s=s.replace(old,new,1)

old='''ProC-SAM3 构造受约束的提示池，并在语义预测上加入门控的非负实例优势 [12]；CoCo-SAM3 聚合同义概念证据并校准独立类别提示之间的竞争 [13]。这些方法改善提示覆盖、概念边界或输出融合。'''
new='''ProC-SAM3 构造受约束的提示池，并在语义预测上加入门控的非负实例优势 [12]；CoCo-SAM3 聚合同义概念证据并校准独立类别提示之间的竞争 [13]；ActiveSAM 保持 SAM3 冻结，并将全分辨率解码限制在图像条件化的激活词表上 [35]，其目标是推理效率与词表裁剪，而不是按读出职责分配证据。这些方法改善提示覆盖、推理效率、概念边界或输出融合。'''
assert old in s
s=s.replace(old,new,1)

# Equation (2)
old=r'''\[
Q_c=\{q:a_c r_{cq}>\eta\},
\qquad
I_c(x)=\max_{q\in Q_c}M_{cq}(x)r_{cq}p_c.
\tag{2}
\]'''
new=r'''\[
\begin{aligned}
Q_c&=\{q:a_c r_{cq}>\eta\},\\
I_c(x)&=\max_{q\in Q_c}M_{cq}(x)r_{cq}p_c.
\end{aligned}
\tag{2}
\]'''
assert old in s
s=s.replace(old,new,1)

# Equation (5)
old=r'''\[
\tilde p_c=\mathcal B(p_c^A,p_c^{\pi_P}),
\qquad
\tilde S_c(x)=\mathcal B(S_c^A(x),S_c^{\pi_S}(x)).
\tag{5}
\]'''
new=r'''\[
\begin{aligned}
\tilde p_c&=\mathcal B(p_c^A,p_c^{\pi_P}),\\
\tilde S_c(x)&=\mathcal B(S_c^A(x),S_c^{\pi_S}(x)).
\end{aligned}
\tag{5}
\]'''
assert old in s
s=s.replace(old,new,1)

# Equation (6)
old=r'''\[
I_A^{\tilde p}=\mathcal I(Q_A;\tilde p,a),
\qquad
I_{\pi_I}^{\tilde p}=\mathcal I(Q_{\pi_I};\tilde p,a),
\qquad
\tilde I_c=\mathcal B(I_A^{\tilde p},I_{\pi_I}^{\tilde p}),
\tag{6}
\]'''
new=r'''\[
\begin{aligned}
I_A^{\tilde p}&=\mathcal I(Q_A;\tilde p,a),\\
I_{\pi_I}^{\tilde p}&=\mathcal I(Q_{\pi_I};\tilde p,a),\\
\tilde I_c&=\mathcal B(I_A^{\tilde p},I_{\pi_I}^{\tilde p}),
\end{aligned}
\tag{6}
\]'''
assert old in s
s=s.replace(old,new,1)

# Equation (10)
old=r'''\[
Z_c(x)=\Psi_{\omega}\!\left(\overline G_{L,c}(x),\overline G_{G,c}(x)\right),
\qquad
\widehat Y=\mathcal D_{\mathrm{base}}(Z),
\tag{10}
\]'''
new=r'''\[
\begin{aligned}
Z_c(x)&=\Psi_{\omega}\!\left(\overline G_{L,c}(x),\overline G_{G,c}(x)\right),\\
\widehat Y&=\mathcal D_{\mathrm{base}}(Z),
\end{aligned}
\tag{10}
\]'''
assert old in s
s=s.replace(old,new,1)

# Dataset citations in 4.1
old='''我们在 SegEarth-OV 和 SegEarth-OV3 [6,11] 使用的八个遥感基准上评价：Potsdam、Vaihingen、LoveDA、iSAID、OpenEarthMap（OEM）、UAVid、UDD5 和 VDD。保持 baseline 的评测划分、类别映射、忽略标签以及基于图像的 UAVid 协议。iSAID 包含 11,644 个处理后的验证切片，UAVid 包含 1,020 个评测图块。主指标为 mIoU（%）。总体平均对八个数据集等权；类别组分析对数据集—类别对等权并单独报告。VOC20 与 Cityscapes 用于自然图像扩展评价。'''
new='''我们在 SegEarth-OV 和 SegEarth-OV3 [6,11] 使用的八个遥感基准上评价：Potsdam 与 Vaihingen [42]、LoveDA [36]、iSAID [37]、OpenEarthMap（OEM）[38]、UAVid [39]、UDD5 [40] 和 VDD [41]。保持 baseline 的评测划分、类别映射、忽略标签以及基于图像的 UAVid 协议。iSAID 包含 11,644 个处理后的验证切片，UAVid 包含 1,020 个评测图块。主指标为 mIoU（%）。总体平均对八个数据集等权；类别组分析对数据集—类别对等权并单独报告。VOC20 [44] 与 Cityscapes [43] 用于自然图像扩展评价。'''
assert old in s
s=s.replace(old,new,1)

# Main table lead-in and method citations
old='''### 4.2 与已有方法的比较

| 方法 | 骨干 | Potsdam | Vaihingen | LoveDA | iSAID | OEM | UAVid | UDD5 | VDD | Avg. |'''
new='''### 4.2 与已有方法的比较

表 1 在统一的八数据集口径下比较 JRV 与代表性方法。方法列引用原论文；竞争方法数值转录自 ProC-SAM3 的比较表 [12]，复现的 SegEarth-OV3 与 JRV 来自匹配的本地运行。

*表 1：遥感开放词汇语义分割结果（mIoU，%）。数据集来源见 4.1 节；已发表数值保留原有精度，可能对应 ProC-SAM3 比较时所使用的版本。*

| 方法 | 骨干 | Potsdam | Vaihingen | LoveDA | iSAID | OEM | UAVid | UDD5 | VDD | Avg. |'''
assert old in s
s=s.replace(old,new,1)
row_repls={
'| VIP |':'| VIP [32] |',
'| SCLIP |':'| SCLIP [29] |',
'| ClearCLIP |':'| ClearCLIP [30] |',
'| ProxyCLIP |':'| ProxyCLIP [31] |',
'| SegEarth-OV |':'| SegEarth-OV [6] |',
'| RSCLIP |':'| RSCLIP [33] |',
'| CorrCLIP |':'| CorrCLIP [34] |',
'| ConInfer |':'| ConInfer [26] |',
'| ReAttnCLIP |':'| ReAttnCLIP [7] |',
'| ActiveSAM |':'| ActiveSAM [35] |',
'| SegEarth-OV3（复现） |':'| SegEarth-OV3（复现）[11] |',
'| ProC-SAM3 |':'| ProC-SAM3 [12] |',
}
for a,b in row_repls.items():
    assert a in s, a
    s=s.replace(a,b,1)

# 4.3 lead-in and Stage caption
old='''### 4.3 补充文本的功能性使用

| 阶段 | Macro mIoU | 相对 baseline | 正提升数据集 |'''
new='''### 4.3 补充文本的功能性使用

我们首先在固定推理配方下区分最终系统的两个阶段。表 2 报告八个基准上的宏观进展，并在匹配的交互分析之前先确定语言证据阶段的作用。

*表 2：宏观组件进展。Stage 指第 3 节定义的本文配置，而不是外部方法。Role-only 是独立记录的最优配置，不是交互分析中固定的匹配 Role 条件。*

| 阶段 | Macro mIoU | 相对 baseline | 正提升数据集 |'''
assert old in s
s=s.replace(old,new,1)

# Lead-in for Table 3
old='''| OEM | S3 | 44.30 | **46.28** | 44.02 |'''
# Insert lead-in before the table containing this row by finding preceding table start.
anchor='''| 数据集 | 候选 | Baseline | 仅 Semantic | 共享 P/S/I |'''
assert anchor in s
idx=s.find(anchor)
assert idx!=-1
lead='''我们固定 role 槽与 admission 模式，进一步考察同一语义候选应如何使用。表 3 比较“仅用于 Semantic”与“在 Presence/Semantic/Instance 中共享”两种方式。\n\n*表 3：同一语义候选的不同角色使用方式。两种变体都保留 anchor 与有界更新；数值为最终 mIoU。*\n\n'''
s=s[:idx]+lead+s[idx:]

p.write_text(s,encoding='utf-8')
print('Chinese text, citations, equations, and table lead-ins synchronized.')

