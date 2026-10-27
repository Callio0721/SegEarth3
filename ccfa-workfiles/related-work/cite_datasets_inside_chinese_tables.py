from pathlib import Path
p=Path(r"D:\论文\9.27论文\中文论文\论文中文版.md")
s=p.read_text(encoding='utf-8')
repls={
'| 方法 | 骨干 | Potsdam | Vaihingen | LoveDA | iSAID | OEM | UAVid | UDD5 | VDD | Avg. |':'| 方法 | 骨干 | Potsdam [42] | Vaihingen [42] | LoveDA [36] | iSAID [37] | OEM [38] | UAVid [39] | UDD5 [40] | VDD [41] | Avg. |',
'| Potsdam | S2 |':'| Potsdam [42] | S2 |',
'| Vaihingen | S3 |':'| Vaihingen [42] | S3 |',
'| LoveDA | S1 |':'| LoveDA [36] | S1 |',
'| OEM | S3 |':'| OEM [38] | S3 |',
'| UDD5 | S3 |':'| UDD5 [40] | S3 |',
'| VDD | S1 |':'| VDD [41] | S1 |',
'| Potsdam | 57.87 | 58.59 |':'| Potsdam [42] | 57.87 | 58.59 |',
'| Vaihingen | 60.86 | 61.59 |':'| Vaihingen [42] | 60.86 | 61.59 |',
'| LoveDA | 47.34 | 48.30 |':'| LoveDA [36] | 47.34 | 48.30 |',
'| iSAID | 27.64 | 28.27 |':'| iSAID [37] | 27.64 | 28.27 |',
'| OEM | 44.30 | 50.53 |':'| OEM [38] | 44.30 | 50.53 |',
'| UAVid | 54.58 | 59.50 |':'| UAVid [39] | 54.58 | 59.50 |',
'| UDD5 | 71.80 | 72.76 |':'| UDD5 [40] | 71.80 | 72.76 |',
'| VDD | 64.11 | 65.83 |':'| VDD [41] | 64.11 | 65.83 |',
'| VOC20 | 1,449 |':'| VOC20 [44] | 1,449 |',
'| Cityscapes | 500 |':'| Cityscapes [43] | 500 |',
'*表 1：遥感开放词汇语义分割结果（mIoU，%）。数据集来源见 4.1 节；已发表数值保留原有精度，可能对应 ProC-SAM3 比较时所使用的版本。*':'*表 1：遥感开放词汇语义分割结果（mIoU，%）。方法与数据集名称均引用原论文；已发表数值保留原有精度，可能对应 ProC-SAM3 比较时所使用的版本。*',
}
for a,b in repls.items():
    if a not in s:
        raise AssertionError('missing: '+a)
    s=s.replace(a,b,1)
p.write_text(s,encoding='utf-8')
print('Chinese dataset citations inserted inside tables')
