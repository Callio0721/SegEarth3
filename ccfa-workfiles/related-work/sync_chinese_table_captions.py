from pathlib import Path
p=Path(r"D:\论文\9.27论文\中文论文\论文中文版.md")
s=p.read_text(encoding='utf-8')
old='''该因子对照衡量 Joint 的 mIoU 增益是否超过两个匹配单组件的增益之和，而不是逐像素交互计数。

| 数据集 | \(m_{00}\) | \(m_{10}\) | \(m_{01}\) | \(m_{11}\) | \(\Gamma\) |'''
new='''该因子对照衡量 Joint 的 mIoU 增益是否超过两个匹配单组件的增益之和，而不是逐像素交互计数。

*表 4：匹配的 Role–View 消融。Role 列使用最终联合角色配置，而不是独立重选的最优配置；数值在舍入前计算。*

| 数据集 | \(m_{00}\) | \(m_{10}\) | \(m_{01}\) | \(m_{11}\) | \(\Gamma\) |'''
assert old in s
s=s.replace(old,new,1)
old='''### 4.6 自然域评价与范围

| 数据集 | 图像数 | Baseline | Role | View | Joint | Δ |'''
new='''### 4.6 自然域评价与范围

表 5 在与遥感评价相同的组件定义下报告自然图像迁移结果。

*表 5：自然图像评价（mIoU，%）。Role-only 与 View-only 分别选择各自最优配置；该表不用于计算交互。VOC20 使用前景词表。*

| 数据集 | 图像数 | Baseline | Role | View | Joint | Δ |'''
assert old in s
s=s.replace(old,new,1)
p.write_text(s,encoding='utf-8')
print('Chinese table captions synchronized')
