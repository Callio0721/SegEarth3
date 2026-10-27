from pathlib import Path
p=Path(r'D:\论文\9.27论文\author-kit-main\sec\4_experiments.tex')
t=p.read_text(encoding='utf-8')
t=t.replace(r'\textbf{Benchmarks and metrics.} ', '')
t=t.replace(r'\textbf{Implementation and profile selection.} ', '')
t=t.replace(r'\textbf{Comparison sources.} ', '')
# Allow the five single-column tables to stay near their references.
t=t.replace(r'\begin{table}[t]', r'\begin{table}[!htbp]')
# Tighten the small tables that received overfull warnings.
t=t.replace("\\label{tab:component-progression}\n\\small\n\\begin{tabular}", "\\label{tab:component-progression}\n\\small\n\\setlength{\\tabcolsep}{3pt}\n\\begin{tabular}")
t=t.replace("\\label{tab:role-use}\n\\small\n\\setlength{\\tabcolsep}{4pt}", "\\label{tab:role-use}\n\\small\n\\setlength{\\tabcolsep}{2.5pt}")
p.write_text(t,encoding='utf-8',newline='\n')

cn=Path(r'D:\论文\9.27论文\中文论文\论文中文版.md')
raw=cn.read_bytes(); bom=raw.startswith(b'\xef\xbb\xbf'); c=raw.decode('utf-8-sig')
c=c.replace('**基准与指标。** ', '').replace('**实现与 profile 选择。** ', '').replace('**比较来源。** ', '')
cn.write_text(c,encoding='utf-8-sig' if bom else 'utf-8',newline='\n')
print('polished experiment layout inputs')
