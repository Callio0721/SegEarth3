from pathlib import Path
ROOT=Path(r'D:\论文\9.27论文')
en=ROOT/'author-kit-main'/'sec'/'3_method.tex'
t=en.read_text(encoding='utf-8')
old='The implementation has three properties used by the experiments. First, every required supplementary phrase undergoes full native grounding rather than modifying an isolated decoder state. Second, an unchanged slot or an all-zero role profile recovers the anchor path, including the official alias aggregation. Third, Local and Context outputs are combined after complete role composition and coordinate restoration, so the method changes evidence use rather than SAM3 attention or its internal fusion operator.'
new='Three implementation properties connect the method to the experimental analysis. Every required supplementary phrase undergoes full native grounding rather than modifying an isolated decoder state. An unchanged slot or an all-zero role profile recovers the anchor path, including the official alias aggregation. Local and Context outputs are combined only after complete role composition and coordinate restoration, so the method changes evidence use rather than SAM3 attention or its internal fusion operator.'
if old not in t:
    raise SystemExit('English implementation paragraph not found')
en.write_text(t.replace(old,new),encoding='utf-8',newline='\n')
cn=ROOT/'中文论文'/'论文中文版.md'
raw=cn.read_bytes(); bom=raw.startswith(b'\xef\xbb\xbf'); ct=raw.decode('utf-8-sig')
old_cn='实现具有三个与实验对应的性质。第一，每条需要的补充文本都完成完整原生 grounding，而不是修改隔离的 decoder 状态。第二，未改变的槽或全零 role profile 会回到 anchor 路径，并保留官方别名聚合。第三，Local 与 Context 在完整角色组合和坐标恢复之后才组合，因此方法改变的是证据使用方式，而不是 SAM3 attention 或内部融合算子。'
new_cn='实现中的三个性质直接对应后续实验。每条需要的补充文本都完成完整原生 grounding，而不是修改隔离的 decoder 状态。未改变的槽或全零 role profile 会回到 anchor 路径，并保留官方别名聚合。Local 与 Context 在完整角色组合和坐标恢复之后才组合，因此方法改变的是证据使用方式，而不是 SAM3 attention 或内部融合算子。'
if old_cn not in ct:
    raise SystemExit('Chinese implementation paragraph not found')
cn.write_text(ct.replace(old_cn,new_cn),encoding='utf-8-sig' if bom else 'utf-8',newline='\n')
print('rewritten')
