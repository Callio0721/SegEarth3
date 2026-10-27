"""Build manuscript bibliography and the source-linked CVPR reading ledger.

Local writing artifacts only. Does not change or execute the research model.
"""
from pathlib import Path
import csv
import json
import re

ASTRA = Path(__file__).resolve().parents[1]
PROJECT = ASTRA.parent
WORK = ASTRA / '_work' / 'cvpr50'
OUT = ASTRA / 'manuscript_v1'
STUDY = ASTRA / 'CVPR50写法研究'
OUT.mkdir(exist_ok=True)
STUDY.mkdir(exist_ok=True)
papers = json.loads((WORK / 'manifest.json').read_text())
packets = json.loads((WORK / 'reading_packets.json').read_text())

# Author-written observations from the actual section/table/figure reading.
# Each entry: argument organization | evidence design | use in our manuscript.
notes = [
('DSGG 生成监督、DSGS 利用监督，两个模块分别回答“得到什么”和“怎样使用”。', '框架图先给两阶段；消融比较注意力替代策略与监督损失，而非只堆组件。', '区分补充描述的产生与角色化使用；同信息、不同用途是关键对照。'),
('先给双曲空间预备，再从半径变化引出具体微调操作与理论分析。', '半径可视化与受控半径实验对应同一解释，主表区分微调范式。', '理论必须描述我们实际操作；不把几何最优性借成 mIoU 保证。'),
('LPOSS 按 patch 传播、跨窗口传播、pixel 传播的处理对象展开。', '窗口大小/步长控制与 Boundary IoU 补充主指标；流程图标出空间还原。', '我们的 Local 必须明确 crop→grounding→坐标还原→重叠聚合。'),
('S-Seg 先定义简单图文监督路线，再解释伪掩膜与自训练。', '先检验自然的简单替代方案，再报主结果；背景计分协议分开列。', '不能用复杂筛查记录代替最直观的普通多提示对照。'),
('Mask-Adapter 从“已有好 mask 仍然分类不好”定位区域读出问题。', 'GT mask 条件下的诊断与真实推理结果分开；主图放大 adapter。', '相关性/上界诊断用于定位，不代替最终方法的真实收益。'),
('PartCATSeg 将 object 与 part 的粒度矛盾映射到两路 cost 与引导。', '结构图使用同色模块贯通输入、聚合和输出；消融比较聚合及引导来源。', '三角色是计算职责，不粗暴等同 thing/stuff 或局部/全局。'),
('H-CLIP 先定义需要保存的几何关系，再给参数化及通信模块。', '理论对象、约束和模型插入点逐项对齐；主表分骨干。', '只陈述有界更新的实际性质，不虚构强正确性定理。'),
('DPSeg 显式讨论模态差距，再提出双 prompt cost 与二次细化。', '单一 embedding 平均、cost 平均、cost 拼接等同级替代比较。', '比较信息进入哪里；不能把它写成 SAM3 的免训练先例。'),
('ESC-Net 将 CLIP correlation 转为伪 prompt，再复用 SAM 并进行跨模态融合。', '总体架构与伪提示/融合细节分图；点、框、mask 有组合消融。', '我们的模型是原生 concept grounding，不是 CLIP 生成点再提示 SAM。'),
('SegEarth-OV 从分辨率不足与 global bias 两个具体矛盾引出模块。', '主多类表、二类任务、模块消融、可迁移性各司其职。', '主线写问题—操作—证据；背景不照搬 CLIP 到 SAM3。'),
('CASS 分对象级图结构与类别存在上下文，按信息来源展开。', '图结构的处理前后对照和多骨干支持机制；mIoU 与 pAcc 分表。', '角色互补需自己的配对证据，不借别人的注意力图解释。'),
('SemLA 将离线 LoRA 库与在线检索融合分成两个明确阶段。', 'leave-one-domain-out 和 all-inclusive 分表，训练资源在协议中说明。', '冻结推理与配置选择是否使用标签是两个问题，设置中统一交代。'),
('DeCLIP 先展示联合监督的冲突，再分 content/context 进行蒸馏。', '朴素合并基线显示任务之间的损益，支撑结构设计而非只支撑总分。', '借鉴“损益随用途变化”的论证，不照搬内部解耦到 SAM3。'),
('Hybrid Global-Local RIS 区分目标局部识别与上下文空间关系。', 'mask/crop、blur/token mask、空间关系等替代对照解释各自职责。', '可借采样互补的思路，但其 proposal 评分不等于我们的 dense 预测。'),
('SAM-REF 从图像与 prompt 交互位置引出 global/local refinement。', '比较将 local 贴回原 SAM 或 global-refined 结果，验证组合位置。', '控制组合接口比反复调强度更能证明问题。'),
('SkySense-O 先交代数据缺口，再写数据引擎与 vision-centric 训练。', '数据性质表和任务结果表分开；消融区分训练数据与建模选择。', 'Related Work 区分训练式遥感基础模型与我们的冻结适配。'),
('SegMAN 将全局上下文、局部细节、多尺度对应 encoder/decoder 设计。', '总图与局部 block 同页层次清楚；encoder、decoder 分别验证。', '我们的文本作用与观察范围各有位置，但要在联合表验证连接。'),
('MFuser 用 VFM 局部特征与 VLM 文本对齐的差异引出桥接模块。', '先给两种特征的例子，再做 fuser 与文本增强替代消融。', '解释互补要指向具体缺失的信息；不能仅称“两模态更丰富”。'),
('SemiDAViL 将类别混淆和类别不平衡映射到语言引导与损失。', '标注量、域、监督类型分别控制；模块表和类别解释分层。', '我们的数据集平均与类别平均分别报告，避免混用统计单位。'),
('ExCEL 从 patch-text 对齐切入，区分文本语义与视觉校准。', '训练免训练结果、CAM seed 与最终 segmentation 分表。', '辅助响应增强与最终分割提升不能当成同一结果。'),
('POT 从单 prototype 无法覆盖多模态外观引出分区、分配、激活。', 'single/multi cluster 与 OT 单独消融，CAM 与分割分别评价。', '描述信息量与使用结构需要分开控制。'),
('CCS Shape 先数学定义，再推平滑约束，最后实例化到模型。', '模块/损失/后处理三种接口比较；形状假设有具体成立条件。', '有形式化条件才能谈结构保证；我们的 region prompt 不是拓扑保证。'),
('PCRE 将 over-expansion 明确为方法针对的问题。', 'CAM、伪标签、最终结果分别列，逐步扩张示意图解释具体操作。', '不要把“覆盖更多像素”写成“必然更准确”，记录 correction/damage。'),
('DFormerv2 反问 depth 是否必须再经独立 encoder，提出几何先验 attention。', '旧双编码与新先验接口并排；模态控制区分语义与形状贡献。', 'Related Work 比较使用机制，不只列共享关键词。'),
('MQ-Former 按 mixed query 设计、数据/任务扩展展开。', 'learnable/conditional/mixed query 在相同任务设置直接比较。', '角色/查询含义必须明确；主表不要混合不同任务指标。'),
('SynCLIP 以同义词导致 grounding 不一致作为中心现象。', '同义词实例表、attention 对比、独立与联合模块消融形成闭环。', '更像人类同义的文字未必产生相同 mask，支持按功能评价提示。'),
('ReAttnCLIP 先展开原 attention 的贡献项，再针对不同项修正。', '主遥感表与单类任务分开，逐组件和替代相似度检验计算解释。', 'P 对 query admission、幅度、最终分数的耦合要写清。'),
('RNS 先形式化完整/缺失视觉与文本支持，再定义检索融合。', '有无标注、support 数量、域数据分栏；按信息可用性组织实验。', '我们的方法没有在线外部样本库，不能混称同一种 training-free 设置。'),
('Direct Segmentation 先重新表述目标，再推解析操作及对应变体。', '常规 raw-logit baseline 与各解析步骤逐项比较。', '数学只保留帮助读者理解实际计算的部分。'),
('OVRCOAT 将 objectness 提前丢 mask 与区域文本错配分开处理。', '2×2 因子表之外，还有 mask 阶段与类别层分析。', '我们的 PI 耦合属于原生机制；主文不要用角色名称替代机制。'),
('HOPS 单列 Problem Analysis：对象过分割与部件欠分割不同。', 'mOSI/mUSI 对应两个具体问题，非只有最终 h-IoU。', '角色结论应有用途控制；结构连通未量化时不宣称拓扑改善。'),
('DenseRC 从 CLS 实际聚合了什么推出 dense feature 构造。', '消融 multi-value 时先关 attention 模块，以免混淆因素。', '配对消融固定角色与视图配置，不能用各自最优替代。'),
('MM-OVSeg 从云遮挡下光学证据缺失引出 SAR 与两阶段融合。', '天气、域、模态设置先用表定义，随后结果表一一对应。', '明确我们是 RGB 的不同观察，不是 Optical-SAR 多模态方法。'),
('SegEarth-R2 从复杂指令维度定义任务，再说明数据与分割 query。', '按粒度、多目标、推理、语言多样性分解能力。', '我们的 role prompt 是类别补充，不夸成复杂指令推理或新数据任务。'),
('PCA-Seg 从串行空间/类别聚合的干扰转向并行 cost aggregation。', 'serial/parallel 直接对照先于专家与正交项；语义/部件协议分表。', '主动区分“角色使用”与内部特征解耦，避免仅换术语的创新陈述。'),
('VDA 从静态文字原型不足转向视觉属性分布与组合原型。', '属性组件表、静态/动态融合曲线、CAM 对比解释信息进入方式。', '文本不必越长越好；我们保留类别锚点而非以自预测替换语义。'),
('FOB/AHP 从伪装对象和背景混淆切入，联结语义探针与 SAM 提示。', 'probe、SAM、hybrid prompt 的增量与框/点删除对照。', '不把训练免训练边界与 CLIP→SAM 的额外前置条件省略。'),
('SkySense-VITA 将 prompt fusion 与 target decoding 两个流程分开。', 'visual/text/fused 三种输入表与 naive fusion 对照暴露负干扰。', '组合好于较弱端点不够，还需对更好端点及单组件解释。'),
('HySeg 明确生成结构先验，再投影为 affinity 引导分割。', '除 region IoU，还用 clDice/Betti error 对齐拓扑主张。', '我们没有这些结构指标，不能把 IoU 上涨直接写成连通性证明。'),
('S2-Corr 先分析 OVSS 在新域的失败，再建立 SSM baseline 和改进。', '训练域与测试词表大小分开，模块表在两个骨干复现。', '自然域实验是边界检查，不声称跨域配置直接迁移。'),
('FSeg-LLaVA 按问答、text-visual response、mask generation 三步展开。', '不同问句和选层、mask 组合均有直接消融。', 'prompt 表达本身是有效变量，具体描述应可回查。'),
('SPAR 先解释固定输入分辨率，再给任意分辨率蒸馏。', 'single-pass 与 sliding-window 对照及不同任务验证表征收益。', '固定模型输入下分辨率/覆盖范围的取舍是事实基础，非生物学装饰。'),
('GLA-CLIP 的 global K/V 扩展产生 locality bias，继续用 proxy 修正。', '跨窗口 Boundary Error Rate 与注意力稳定性对应主问题；配置声明明确。', '承认 global/local 已有先例，我们的新焦点是其与角色文本的条件互补。'),
('TMPA 先文本歧义，再数据集描述生成，最后低熵视觉均值引导在线 bias。', 'dataset description、VGTA 和骨干通用性分别测试。', '借其任务适配思想，不把 CLIP embedding 的线性混合硬套到 SAM3。'),
('S2C2Seg 将类别子集筛选与全局语义/局部空间组合分开。', '比较加、乘、学习权重等融合，并按有无背景分组。', '不能笼统声称“首次全局局部+文本”；我们的职责对象与接口须具体。'),
('PEARL 将 attention 几何对齐和文本感知传播串成 align-then-propagate。', 'PA/TLP 四格与替代策略验证各自功能。', '优先用短操作链和配对消融，不堆无关失败模块。'),
('DPAD 对准推理游离目标的问题，把 grounded description 放入奖励。', '二值/差值/缩放奖励替代对照，而非只报完整框架。', '我们的描述不含这个 RL 工作流，不能仅因 anchor 一词就混引。'),
('HERA 以层间可迁移性差异引出 select–regularize–calibrate。', '层规则、support-only 与最终三组件效应各有表。', '离线可解码信息不等于任意插入点有效；不要重开已停的层选择实验。'),
('F2Net 把 UHR 的细节/上下文矛盾对应到频率分支及组合。', '三分支单独、两两、完整组合表，比只写模块累加更有说服力。', '借用匹配组合表，不声称我们进行了频率分解。'),
('Vocabulary Scaling Law 将 openness 定义为稳定性与扩展性后推导条件。', '同时报告闭集准确率、扩展、干扰类稳定性，直接检验所称能力。', '当前固定测试词表结果不足以声称未知任意词表的稳健性。'),
]
assert len(notes) == len(papers) == 50

header = '''# 50 篇 CVPR 主会论文：结构、论证与图表阅读记录

日期：2026-09-05。范围为 **CVPR 2025 主会 25 篇 + CVPR 2026 主会 25 篇**，全部以 CVF 官方 proceedings 页面核验；Findings、arXiv 和较早论文没有充当这 50 篇的计数。开放词汇分割为中心，向遥感、密集预测、跨域及局部—全局建模扩展。

阅读粒度：逐篇阅读章节结构、方法入口和关键段落、实验/消融段落、表格比较对象及图注；渲染并检查了 50 篇的代表正文页面。对 TMPA、SegEarth-OV、GLA-CLIP、PEARL 等直接相关机制另读原方法。**这是 50 篇结构与关键内容的定向学习，不声称逐句精读所有正文和补充材料。**

PDF、官方页面、官方 BibTeX 和抽取文本保存在 `../_work/cvpr50/`；`sources.csv` 给出逐篇映射。每个题目链接均为主会官方来源。下列是阅读后的分析，不是原文摘抄。

## 共同采用、而非机械照抄的写作原则

1. Related Work 按“问题与解法”归类，每段结尾解释本文差异，不按论文年份逐篇报菜名。
2. Method 先定义输入、输出与原模型机制，然后每一小节按“缺口→操作→作用对象→与下一步关系”推进。
3. 主图给整体数据流；局部放大只画新操作。不用几十个实验代号代替方法名称。
4. 主表回答竞争力；配对模块表回答归因；结构替代对照回答“为什么这样做”；类别/定性图回答何处受益与边界。
5. 理论厚度来自准确的计算对象、前置条件和作用链；不是补一些未实现的公式或借来的定理。
6. 有监督、测试时梯度、冻结推理、标注支持、配置选择需分别说明；不同论文的数字不能自动视为同协议复现。

## 逐篇记录

'''
chunks=[header]
for p,pack,note in zip(papers,packets,notes):
    ident=p['id']
    sections='；'.join(s for _,s in pack['headings'] if re.match(r'^\d+\.\s+[A-Z]',s) and len(s)<72)
    chunks.append(f"### {ident} · CVPR {p['year']} · [{p['title']}]({p['url']})\n\n"
                  f"- 结构定位：{sections or '见全文抽取与官方 PDF'}。\n"
                  f"- 方法论证：{note[0]}\n- 图表组织：{note[1]}\n- 对本稿的采用/边界：{note[2]}\n"
                  f"- 本地原文：[PDF](../_work/cvpr50/{ident}.pdf)；[文本](../_work/cvpr50/{ident}.txt)。\n\n")
(STUDY/'阅读记录.md').write_text(''.join(chunks))
with (STUDY/'sources.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=['id','year','title','url','pdf_url','pdf','verified']);w.writeheader();w.writerows(papers)
all_bib=[]
for p in papers:
    b=(WORK/f"{p['id']}.bib").read_text().strip()
    all_bib.append(re.sub(r'(@\w+\{)[^,]+',rf'\g<1>{p["id"]}',b,count=1))
(STUDY/'cvpr50.bib').write_text('\n\n'.join(all_bib)+'\n')

old=(PROJECT/'docs/论文框架/2026-09-03/论文引用.bib').read_text()
oldblocks={m.group(2):m.group(0).strip() for m in re.finditer(r'(@\w+\{)([^,]+),.*?^\}',old,re.S|re.M)}
mapping={2:'C03',3:'C11',4:'C46',5:'C05',6:'C10',7:'C27',8:'C44',14:'C43',16:'C08',17:'C35',19:'C49',20:'C26',21:'C16',22:'C33',23:'C17'}
oldmap={9:'R04',10:'R01',11:'R02',12:'R03',13:'R05',15:'R10',18:'R07'}
bibs={1:'''@InProceedings{R01,
 author = {Radford, Alec and Kim, Jong Wook and Hallacy, Chris and Ramesh, Aditya and Goh, Gabriel and Agarwal, Sandhini and Sastry, Girish and Askell, Amanda and Mishkin, Pamela and Clark, Jack and Krueger, Gretchen and Sutskever, Ilya},
 title = {Learning Transferable Visual Models From Natural Language Supervision},
 booktitle = {Proceedings of the 38th International Conference on Machine Learning},
 year = {2021}, pages = {8748--8763}, volume = {139}, publisher = {PMLR},
 url = {https://proceedings.mlr.press/v139/radford21a.html}
}'''}
for num,ident in mapping.items():
    b=(WORK/f'{ident}.bib').read_text().strip()
    b=re.sub(r'(@\w+\{)[^,]+',rf'\g<1>R{num:02d}',b,count=1)
    p=next(x for x in papers if x['id']==ident)
    # CVF's exported entry does not include a URL.
    if not re.search(r'\burl\s*=',b):b=b.rstrip()[:-1].rstrip()+',\n    url = {'+p['url']+'}\n}'
    b=b.replace(',\n,',',\n')
    bibs[num]=b
for num,key in oldmap.items():
    bibs[num]=re.sub(r'(@\w+\{)[^,]+',rf'\g<1>R{num:02d}',oldblocks[key],count=1)
(OUT/'references.bib').write_text('% Numbered keys match the English and Chinese drafts.\n'+ '\n\n'.join(bibs[k] for k in sorted(bibs))+'\n')

def field(b,key):
    m=re.search(r'\b'+key+r'\s*=\s*\{',b)
    if not m:
        return ''
    start=m.end(); depth=1; end=start
    while end < len(b) and depth:
        depth += (b[end]=='{') - (b[end]=='}')
        end += 1
    return b[start:end-1].replace('{','').replace('}','').strip()
ref=['# References / 两版初稿共同参考文献\n\n数字编号与正文一致；BibTeX key 为 R01–R23。本表是实际引用库，不是 50 篇写法语料库。\n\n']
for k,b in sorted(bibs.items()):
    title=field(b,'title');author=field(b,'author');url=field(b,'url')
    author=author.replace(r"Stojni\'c",'Stojnić').replace(r"Ji\vr\'\i",'Jiří')
    venue=field(b,'booktitle') or field(b,'journal')
    ref.append(f'<a id="r{k:02d}"></a>\n\n[{k}] {author}. [{title}]({url}). {venue}, {field(b,"year")}.\n\n')
(OUT/'references.md').write_text(''.join(ref))
print('Saved 50-paper ledger, source manifest, CVPR BibTeX, and 23 manuscript references.')
