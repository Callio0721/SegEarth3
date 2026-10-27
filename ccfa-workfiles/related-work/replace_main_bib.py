from pathlib import Path
p=Path(r'D:\论文\9.27论文\author-kit-main\main.tex')
t=p.read_text(encoding='utf-8')
t=t.replace('\n% Keep citation numbering aligned with the Chinese manuscript reference list.\n\\nocite{R01,R02,R03,R04,R05,R06,R07,R08,R09,R10,R11,R12,R13,R14,R15,R16,R17,R18,R19,R20,R21,R22,R23,R24,R25,R26,R27,R28}\n','\n')
block='''{
    \\small
    \\bibliographystyle{ieeenat_fullname}
    \\bibliography{main}
}'''
t=t.replace(block,'\\input{references}')
if '\\input{references}' not in t:
    raise SystemExit('bibliography block not replaced')
p.write_text(t,encoding='utf-8',newline='\n')
print(p.read_text(encoding='utf-8'))
