from pathlib import Path
p=Path(r"D:\论文\9.27论文\中文论文\论文中文版.md")
s=p.read_text(encoding='utf-8')

s=s.replace('我们的代码开源在：github链接', '我们的代码开源在：https://github.com/pengjunhao621-arch/SegEarth3', 1)

start=s.index('## 1. 引言')
end=s.index('\n## 2. 相关工作', start)
intro='''## 1. 引言

开放词汇语义分割（OVSS）要求在推理时为每个像素分配任意文本类别。免训练方法通常改造视觉—语言模型的稠密预测 [1,6]。SAM3 转而以文本概念约束一个共享 grounding 状态，并从中提供三种 readout：Presence 判断概念是否存在，Semantic 估计稠密覆盖，Instance 组织 query 生成的区域 [10]；SegEarth-OV3 将该接口用于遥感 [11]。共享状态稳定了类别语义，但三种 readout 对证据的需求并不相同。遥感场景中的小目标、连续地表和场景级存在性无法由同一种观察同时充分刻画，已有评估也表明 SAM3 的存在性与定位能力并不总是同步 [24]。图 1 概括了这一证据分配问题。

现有方法主要调整类别提示或组合完整输出。TMPA 依据图像调整 CLIP 文本嵌入 [8]；ConceptBank 用支持集评价候选概念 [9]；ProC-SAM3 与 CoCo-SAM3 在提示级融合多源证据 [12,13]；RSGPNet 用几何提示改进 SAM3 定位 [25]。一条描述会经过完整 grounding，因此它在改善稠密覆盖的同时，也可能改变存在性判断或 query 组织；替换官方类别名还会移动 ontology anchor。这些方法主要停留在类别级，即使其输出会影响多个 readout。

视觉证据构成第二个约束。局部裁块保留细节，却可能切断长距离结构；更大视野提供上下文，却会降低小目标的采样密度。多分辨率、跨窗口、窗口拼接和场景级推断方法利用这种互补性 [14,15,18,26]，通常通过修改注意力、特征或固定融合规则实现。对于按角色补充证据而言，一种观察是否有用还取决于哪个 readout 需要缺失的信息。

本文提出角色—视图联合专门化（Joint Role--View Specialization，JRV）。JRV 保留官方类别名与别名形成的 anchor，用完整冻结的 SAM3 对角色功能候选进行 grounding，并只对其对应 readout 施加有界修正，同时保留 Presence--Instance 原生耦合。随后，方法在空间对齐的 Local 与 Context 观察上分别完成 grounding，复用同一角色配置，并在原始类别决策前组合完整类别分数场。JRV 不修改 SAM3 注意力，也不为每个 head 分配独立视觉路径。

本文贡献如下：

- **Readout 级概念适配。** 提出保留 anchor 的 Role-Functional Text：补充描述经过完整 grounding 后，按 Presence、Semantic 和 Instance 的职责使用，而不替换官方 ontology，也不破坏 Presence--Instance 耦合。
- **Role--View 联合专门化。** 将角色文本与视觉观察作为联合条件，在同一 role profile 下处理空间对齐的 Local 与 Context 观察，并在 argmax 前组合完整类别分数场。
- **证据与适用范围。** 在八个遥感基准上，配对平均 mIoU 从 53.56 提升到 Role-only 的 55.82 和 Joint 的 57.49；全部数据集超过 baseline，六个数据集呈正 Role--View 交互。Cityscapes 与 VOC20 检验自然图像迁移，并表明视图组合仍依赖数据分布。
'''
s=s[:start]+intro+s[end:]

s=s.replace('### 2.1 开放词汇分割：从图文对齐到概念定位','### 2.1 从 OVSS 到概念定位',1)
s=s.replace('### 2.2 概念表示与提示适配','### 2.2 概念与提示适配',1)
s=s.replace('### 2.3 互补视觉观察与上下文','### 2.3 视觉观察与上下文',1)

# Dataset first-occurrence descriptions.
old='''我们在 SegEarth-OV 和 SegEarth-OV3 [6,11] 使用的八个遥感基准上评价：Potsdam 与 Vaihingen [42]、LoveDA [36]、iSAID [37]、OpenEarthMap（OEM）[38]、UAVid [39]、UDD5 [40] 和 VDD [41]。保持 baseline 的评测划分、类别映射、忽略标签以及基于图像的 UAVid 协议。iSAID 包含 11,644 个处理后的验证切片，UAVid 包含 1,020 个评测图块。主指标为 mIoU（%）。总体平均对八个数据集等权；类别组分析对数据集—类别对等权并单独报告。VOC20 [44] 与 Cityscapes [43] 用于自然图像扩展评价。'''
new='''我们在 SegEarth-OV 和 SegEarth-OV3 [6,11] 使用的八个遥感基准上评价：Potsdam 与 Vaihingen [42]、LoveDA [36]、iSAID [37]、OpenEarthMap（OEM）[38]、UAVid [39]、UDD5 [40] 和 VDD [41]。Potsdam 与 Vaihingen 是 ISPRS 航空城市场景基准；LoveDA 覆盖中国三座城市的城乡地表覆盖；iSAID 是由 DOTA 扩展的大规模航空实例分割数据集；OpenEarthMap 是全球高分辨率地表覆盖基准；UAVid 关注无人机倾斜视角下的城市场景；UDD5 由带语义约束的航空 SfM 数据构建；VDD 强调多样无人机场景和飞行条件。VOC20 [44] 包含 20 个 PASCAL VOC 前景类别，Cityscapes [43] 提供 19 类城市街景评价。保持 baseline 的评测划分、类别映射、忽略标签以及基于图像的 UAVid 协议。iSAID 包含 11,644 个处理后的验证切片，UAVid 包含 1,020 个评测图块。主指标为 mIoU（%）。总体平均对八个数据集等权；类别组分析对数据集—类别对等权并单独报告。'''
assert old in s
s=s.replace(old,new,1)

old='''使用与复现 baseline 相同的冻结 SAM3 权重和原生 grounding。候选描述离线生成并按原文保存。无特别说明时 \(\alpha=0.5\)、\(\tau=0.25\)。'''
new='''全部实验和推理在 4 块 NVIDIA RTX 3090 GPU 上完成。SAM3 权重保持冻结，不进行模型训练或微调。候选描述离线生成并按原文保存。无特别说明时 \(\alpha=0.5\)、\(\tau=0.25\)。'''
assert old in s
s=s.replace(old,new,1)

# Transition before logit equation (12).
old='''\tag{11}
\]

\[
\Psi_{\mathrm{logit},g}(L,G)=\sigma\!\left((1-g)\operatorname{logit}(L)+g\operatorname{logit}(G)\right).'''
new='''\tag{11}
\]

logit 版本在对数几率空间中执行同样的混合：

\[
\Psi_{\mathrm{logit},g}(L,G)=\sigma\!\left((1-g)\operatorname{logit}(L)+g\operatorname{logit}(G)\right).'''
assert old in s
s=s.replace(old,new,1)

# 4.6: substantive text before the table.
old='''### 4.6 自然域评价与范围

表 5 在与遥感评价相同的组件定义下报告自然图像迁移结果。

*表 5：自然图像评价（mIoU，%）。Role-only 与 View-only 分别选择各自最优配置；该表不用于计算交互。VOC20 使用前景词表。*'''
new='''### 4.6 自然域评价与范围

自然图像评价检验角色补充能否从俯视几何和遥感 ontology 迁移到不同场景分布，同时保持冻结模型与角色定义不变。VOC20 使用 20 类前景词表，Cityscapes 在另一种场景分布下评价 19 个城市类别。下面先报告同一组件定义下的联合结果，再分别分析角色与视图效应。

*表 5：自然图像评价（mIoU，%）。Role-only 与 View-only 分别选择各自最优配置；该表不用于计算交互。VOC20 使用前景词表。*'''
assert old in s
s=s.replace(old,new,1)

p.write_text(s,encoding='utf-8')
print('Chinese abstract, intro, subsection titles, setup, equation transition, and 4.6 synchronized')
