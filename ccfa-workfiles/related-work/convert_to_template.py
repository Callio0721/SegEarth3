from pathlib import Path
import re

ROOT = Path(r"D:\论文\9.27论文")
KIT = ROOT / "author-kit-main"
CN_DIR = ROOT / "中文论文"
CN_DIR.mkdir(exist_ok=True)

# Extract the finalized English Related Work from the bilingual manuscript source.
en_text = (ROOT / "Astra_docs" / "manuscript_v1" / "English_draft.md").read_text(encoding="utf-8-sig")
start = en_text.index("## 2. Related Work")
end = en_text.index("## 3. Method", start)
related_md = en_text[start:end].strip()

key_map = {
    1: "R01", 2: "R02", 3: "R03", 4: "R04", 5: "R05", 6: "R06", 7: "R07",
    8: "R08", 9: "R09", 10: "R10", 11: "R11", 12: "R12", 13: "R13", 14: "R14",
    15: "R15", 16: "R16", 17: "R17", 18: "R18", 19: "R19", 20: "R20", 21: "R21",
    22: "R22", 23: "R23", 24: "R24", 25: "R25", 26: "R26", 27: "R27", 28: "R28",
}

def cite_repl(match):
    nums = [int(x) for x in match.group(1).split(",")]
    keys = ",".join(key_map[n] for n in nums)
    return r"\cite{" + keys + "}"

related_tex = re.sub(r"\[(\d+(?:,\d+)*)\]", cite_repl, related_md)
related_tex = related_tex.replace("## 2. Related Work", "\\section{Related Work}\n\\label{sec:related_work}")
related_tex = re.sub(r"^###\s+(.*)$", r"\\subsection{\1}", related_tex, flags=re.M)
related_tex = related_tex.replace("Vision-Language", "Vision--Language")
related_tex = related_tex.replace("object-context", "object--context")
related_tex = related_tex.replace("region-text", "region--text")
related_tex = related_tex.replace("global-token", "global-token")
related_tex = related_tex.replace("remote-sensing", "remote-sensing")
related_tex = related_tex.replace("class-score", "class-score")
related_tex = related_tex.replace("text-vision", "text--vision")

(KIT / "sec" / "2_related_work.tex").write_text(related_tex.rstrip() + "\n", encoding="utf-8", newline="\n")

main_tex = r'''% CVPR 2026 Paper Template; see https://github.com/cvpr-org/author-kit

\documentclass[10pt,twocolumn,letterpaper]{article}

%%%%%%%%% PAPER TYPE
\usepackage[review]{cvpr}

% Import additional packages in the preamble file, before hyperref
\input{preamble}

\definecolor{cvprblue}{rgb}{0.21,0.49,0.74}
\usepackage[pagebackref,breaklinks,colorlinks,allcolors=cvprblue]{hyperref}

%%%%%%%%% PAPER ID - UPDATE FOR THE SUBMISSION
\def\paperID{*****}
\def\confName{CVPR}
\def\confYear{2027}

%%%%%%%%% TITLE
\title{Joint Role--View Specialization for Training-Free Open-Vocabulary Remote Sensing Segmentation}

%%%%%%%%% AUTHORS - UPDATE FOR THE SUBMISSION
\author{First Author\\
Institution\\
Address\\
{\tt\small firstauthor@example.org}
}

\begin{document}
\maketitle

% The Chinese counterpart is maintained at ../中文论文/论文中文版.md.
% Future English sections should follow the section order in that file.

\input{sec/2_related_work}

{
    \small
    \bibliographystyle{ieeenat_fullname}
    \bibliography{main}
}

\end{document}
'''
(KIT / "main.tex").write_text(main_tex, encoding="utf-8", newline="\n")

# Make the template bibliography self-contained.
bib = (ROOT / "Astra_docs" / "manuscript_v1" / "references.bib").read_text(encoding="utf-8")
(KIT / "main.bib").write_text(bib.rstrip() + "\n", encoding="utf-8", newline="\n")

# Chinese manuscript lives in its own directory from now on.
cn = (ROOT / "Astra_docs" / "manuscript_v1" / "Chinese_draft.md").read_text(encoding="utf-8-sig")
(CN_DIR / "论文中文版.md").write_text(cn.rstrip() + "\n", encoding="utf-8", newline="\n")

mapping = r'''# 中英稿件对应关系

| 中文稿件 | 英文模板 | 当前状态 | 同步规则 |
|---|---|---|---|
| `论文中文版.md` / 摘要 | `sec/0_abstract.tex` | 待撰写 | 中文摘要修改后同步英文摘要 |
| `论文中文版.md` / Introduction | `sec/1_intro.tex` | 待撰写 | 英文引言与中文引言逐段对应 |
| `论文中文版.md` / 相关工作 | `sec/2_related_work.tex` | 已完成 | 中文修改后同步英文对应段落 |
| `论文中文版.md` / 方法 | `sec/3_method.tex` | 待整理 | 中文方法修改后同步英文公式、术语和段落 |
| `论文中文版.md` / 实验 | `sec/4_experiments.tex` | 待整理 | 中文实验修改后同步英文表格、数字和结论 |
| `论文中文版.md` / 结论 | `sec/5_conclusion.tex` | 待整理 | 中文结论修改后同步英文结论 |

英文论文根目录：`author-kit-main`  
英文主文件：`author-kit-main/main.tex`  
中文论文根目录：`中文论文`
'''
(CN_DIR / "中英章节对应.md").write_text(mapping, encoding="utf-8", newline="\n")

print({
    "english_section": str(KIT / "sec" / "2_related_work.tex"),
    "main_tex": str(KIT / "main.tex"),
    "main_bib": str(KIT / "main.bib"),
    "chinese_manuscript": str(CN_DIR / "论文中文版.md"),
    "sync_mapping": str(CN_DIR / "中英章节对应.md"),
})
