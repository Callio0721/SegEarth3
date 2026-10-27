from pathlib import Path
p=Path(r"D:\论文\9.27论文\author-kit-main\sec\4_experiments.tex")
s=p.read_text(encoding='utf-8')
repls={
r'Method & Backbone & Potsdam & Vaihingen & LoveDA & iSAID & OEM & UAVid & UDD5 & VDD & Avg. \\':
r'Method & Backbone & Potsdam~\cite{R42} & Vaihingen~\cite{R42} & LoveDA~\cite{R36} & iSAID~\cite{R37} & OEM~\cite{R38} & UAVid~\cite{R39} & UDD5~\cite{R40} & VDD~\cite{R41} & Avg. \\',
r'Dataset & Candidate & Baseline & Semantic only & Shared P/S/I \\':
r'Dataset & Candidate & Baseline & Semantic only & Shared P/S/I \\',
r'Potsdam & S2 &':r'Potsdam~\cite{R42} & S2 &',
r'Vaihingen & S3 &':r'Vaihingen~\cite{R42} & S3 &',
r'LoveDA & S1 &':r'LoveDA~\cite{R36} & S1 &',
r'OEM & S3 &':r'OEM~\cite{R38} & S3 &',
r'UDD5 & S3 &':r'UDD5~\cite{R40} & S3 &',
r'VDD & S1 &':r'VDD~\cite{R41} & S1 &',
r'Potsdam & 57.87 & 58.59 &':r'Potsdam~\cite{R42} & 57.87 & 58.59 &',
r'Vaihingen & 60.86 & 61.59 &':r'Vaihingen~\cite{R42} & 60.86 & 61.59 &',
r'LoveDA & 47.34 & 48.30 &':r'LoveDA~\cite{R36} & 47.34 & 48.30 &',
r'iSAID & 27.64 & 28.27 &':r'iSAID~\cite{R37} & 27.64 & 28.27 &',
r'OEM & 44.30 & 50.53 &':r'OEM~\cite{R38} & 44.30 & 50.53 &',
r'UAVid & 54.58 & 59.50 &':r'UAVid~\cite{R39} & 54.58 & 59.50 &',
r'UDD5 & 71.80 & 72.76 &':r'UDD5~\cite{R40} & 71.80 & 72.76 &',
r'VDD & 64.11 & 65.83 &':r'VDD~\cite{R41} & 64.11 & 65.83 &',
r'VOC20 & 1,449 &':r'VOC20~\cite{R44} & 1,449 &',
r'Cityscapes & 500 &':r'Cityscapes~\cite{R43} & 500 &',
r'Dataset sources are cited in Section~\ref{sec:experiments}. Avg. is the equal-weight mean over eight datasets':r'Dataset and method names cite their original papers. Avg. is the equal-weight mean over eight datasets',
}
for a,b in repls.items():
    if a not in s:
        raise AssertionError('missing: '+a[:80])
    s=s.replace(a,b,1)
p.write_text(s,encoding='utf-8')
print('English dataset citations inserted inside tables')

