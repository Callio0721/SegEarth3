from pathlib import Path
p=Path(r"D:\论文\9.27论文\中文论文\论文中文版.md")
lines=p.read_text(encoding='utf-8').splitlines()
out=[]
indent='\u3000\u3000'
in_math=False
in_code=False
changed=0
for line in lines:
    stripped=line.strip()
    if stripped.startswith('```'):
        in_code=not in_code
        out.append(line)
        continue
    if in_code:
        out.append(line)
        continue
    if stripped.startswith('\\['):
        in_math=True
        out.append(line)
        continue
    if in_math:
        out.append(line)
        if stripped.startswith('\\]'):
            in_math=False
        continue
    skip = (
        not stripped or
        stripped.startswith('#') or
        stripped.startswith('|') or
        stripped.startswith('- ') or
        stripped.startswith('* ') or
        stripped.startswith('>') or
        stripped.startswith('!') or
        stripped.startswith('<') or
        stripped.startswith('\\') or
        (stripped.startswith('*') and stripped.endswith('*'))
    )
    if skip:
        out.append(line)
        continue
    clean=line.lstrip(' \t\u3000')
    out.append(indent+clean)
    changed += 1
p.write_text('\n'.join(out)+'\n',encoding='utf-8')
print('indented paragraphs:',changed)
