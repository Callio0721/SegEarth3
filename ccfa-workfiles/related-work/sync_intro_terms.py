from pathlib import Path
ROOT=Path(r"D:\论文\9.27论文")
en=ROOT/'author-kit-main'/'sec'/'1_intro.tex'
t=en.read_text(encoding='utf-8')
t=t.replace('TMPA adjusts CLIP text embeddings using image evidence \\cite{R08}; ConceptBank evaluates and fuses candidate concepts with a support set \\cite{R09}; ProC-SAM3 constructs a constrained prompt pool and applies residual fusion to multi-prompt outputs \\cite{R12}; CoCo-SAM3 aggregates synonymous evidence and calibrates competition among categories \\cite{R13}; and RSGPNet uses geometric prompts with consistency verification to refine SAM3 localization \\cite{R25}.', 'TMPA adjusts CLIP text embeddings using image evidence \\cite{R08}, while ConceptBank evaluates and fuses candidate concepts with a support set \\cite{R09}. ProC-SAM3 constructs a constrained prompt pool and applies residual fusion to multi-prompt outputs \\cite{R12}. CoCo-SAM3 aggregates synonymous evidence and calibrates competition among categories \\cite{R13}. RSGPNet uses geometric prompts with consistency verification to refine SAM3 localization \\cite{R25}.')
t=t.replace('We introduce Role--View Evidence Specialization (JRV). JRV preserves', 'We introduce Joint Role--View Specialization (JRV), a framework for role--view evidence specialization. JRV preserves')
en.write_text(t,encoding='utf-8',newline='\n')
cn=ROOT/'中文论文'/'论文中文版.md'
raw=cn.read_bytes(); bom=raw.startswith(b'\xef\xbb\xbf'); ct=raw.decode('utf-8-sig')
ct=ct.replace('据此，本文提出角色—视图证据专门化（Role–View Evidence Specialization，JRV）。', '据此，本文提出角色—视图联合专门化（Joint Role–View Specialization，JRV）。')
cn.write_text(ct,encoding='utf-8-sig' if bom else 'utf-8',newline='\n')
print('terminology synced')
