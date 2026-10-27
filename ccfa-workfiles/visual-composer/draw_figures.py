from pathlib import Path
from PIL import Image
import base64, csv, html

ROOT=Path(r'D:\论文\9.27论文')
OUT=ROOT/'author-kit-main'/'fig'
ASSETS=ROOT/'ccfa-workfiles'/'visual-composer'/'assets'
OUT.mkdir(parents=True,exist_ok=True)
ASSETS.mkdir(parents=True,exist_ok=True)
FONT='Times New Roman, Times, serif'
C={'ink':'#111827','muted':'#4B5563','light':'#F3F4F6','line':'#9CA3AF','Navy':'#174A7C','Presence':'#6A4C93','Semantic':'#0B7285','Instance':'#D95F02','accent':'#0072B2','positive':'#0072B2','neutral':'#8491B4','paleP':'#F1ECF8','paleS':'#E7F4F5','paleI':'#FFF0E5','paleBlue':'#EAF2F8'}

def esc(s): return html.escape(str(s), quote=True)
def b64(path): return base64.b64encode(path.read_bytes()).decode('ascii')

def make_svg(w,h,body,defs=''):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w/200}in" height="{h/200}in" viewBox="0 0 {w} {h}">
<defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="#4B5563"/></marker>{defs}</defs>
<rect width="100%" height="100%" fill="white"/>
<g font-family="{FONT}" text-rendering="geometricPrecision" shape-rendering="geometricPrecision">
{body}
</g></svg>'''

def rect(x,y,w,h,fill='#FFFFFF',stroke='#4B5563',sw=2,rx=10,dash=None):
    d=f' stroke-dasharray="{dash}"' if dash else ''
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d}/>'
def text(x,y,s,size=22,weight='normal',fill=None,anchor='middle',style='normal'):
    fill=fill or C['ink']
    lines=str(s).split('\n')
    out=[]
    for i,line in enumerate(lines):
        out.append(f'<text x="{x}" y="{y+i*size*1.12}" font-size="{size}" font-weight="{weight}" font-style="{style}" fill="{fill}" text-anchor="{anchor}">{esc(line)}</text>')
    return ''.join(out)
def line(x1,y1,x2,y2,color=None,width=2.5,dash=None,arrow=False):
    color=color or C['muted']; d=f' stroke-dasharray="{dash}"' if dash else ''
    marker=' marker-end="url(#arrow)"' if arrow else ''
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{width}"{d}{marker} stroke-linecap="round"/>'
def path(d,color=None,width=2.5,fill='none',dash=None,arrow=False):
    color=color or C['muted']; marker=' marker-end="url(#arrow)"' if arrow else ''
    da=f' stroke-dasharray="{dash}"' if dash else ''
    return f'<path d="{d}" fill="{fill}" stroke="{color}" stroke-width="{width}"{da}{marker} stroke-linejoin="round" stroke-linecap="round"/>'
def circle(x,y,r,fill,stroke='none',sw=1):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'
def image(x,y,w,h,href,label=None,label_y=None,label_size=18):
    s=f'<image x="{x}" y="{y}" width="{w}" height="{h}" preserveAspectRatio="xMidYMid slice" href="data:image/png;base64,{href}"/>'
    if label: s+=text(x+w/2,label_y or y+h+24,label,label_size,fill=C['muted'])
    return s

# Prepare teaser crops from a real remote-sensing scene.
src=Image.open(ROOT/'SegEarth3-main'/'resources'/'oem_koeln_50.tif').convert('RGB')
full=src.resize((440,440),Image.Resampling.LANCZOS); full.save(ASSETS/'teaser_full.png')
local=src.crop((250,250,750,750)).resize((260,260),Image.Resampling.LANCZOS); local.save(ASSETS/'teaser_local.png')
context=src.resize((260,260),Image.Resampling.LANCZOS); context.save(ASSETS/'teaser_context.png')
FULL=b64(ASSETS/'teaser_full.png'); LOCAL=b64(ASSETS/'teaser_local.png'); CONTEXT=b64(ASSETS/'teaser_context.png')

# 1. Intro teaser
parts=[]
parts.append(rect(30,26,410,255,'#FFFFFF','#D1D5DB',1.5,12))
parts.append(image(40,36,180,180,FULL))
parts.append(text(130,246,'Aerial scene',20,fill=C['muted']))
# anchor
parts.append(rect(70,285,0,0)) if False else ''
parts.append(rect(490,56,190,104,C['Navy'],C['Navy'],2,12))
parts.append(text(585,91,'Concept anchor',19,weight='bold',fill='#FFFFFF'))
parts.append(text(585,123,'"road" + aliases',21,weight='bold',fill='#FFFFFF'))
parts.append(line(460,145,486,145,width=2.5,arrow=True))
# role cards
role_info=[('P','Presence','exists in scene?',C['Presence'],C['paleP']),('S','Semantic','dense appearance?',C['Semantic'],C['paleS']),('I','Instance','region organization?',C['Instance'],C['paleI'])]
for i,(letter,name,q,color,pale) in enumerate(role_info):
    x=730+i*205
    parts.append(rect(x,32,185,130,pale,color,2,10))
    parts.append(circle(x+26,57,16,color))
    parts.append(text(x+26,64,letter,18,weight='bold',fill='#FFFFFF'))
    parts.append(text(x+54,64,name,19,weight='bold',fill=color,anchor='start'))
    parts.append(text(x+20,100,q,18,fill=C['ink'],anchor='start'))
parts.append(line(680,97,727,97,width=2.5,arrow=True))
# same profile band
parts.append(rect(730,190,581,46,C['light'],'#D1D5DB',1.2,10))
parts.append(text(1020,219,'same role profile: what evidence does each readout need?',20,fill=C['muted']))
# view cards
view_y=258
parts.append(rect(730,258,270,31,'#FFFFFF','#D1D5DB',1.2,8))
parts.append(text(865,280,'Local / native observation',19,fill=C['ink']))
parts.append(rect(1025,258,286,31,'#FFFFFF','#D1D5DB',1.2,8))
parts.append(text(1168,280,'Context / wider observation',19,fill=C['ink']))
parts.append(line(865,236,865,254,width=2,arrow=True))
parts.append(line(1168,236,1168,254,width=2,arrow=True))
intro=make_svg(1400,320,''.join(parts))

# 2. Method overview
parts=[]
# top row
parts.append(rect(25,30,190,130,'#FFFFFF',C['Navy'],2,12))
parts.append(text(120,62,'Concept anchor',18,weight='bold',fill=C['Navy']))
parts.append(text(120,98,'"road"',22,weight='bold'))
parts.append(text(120,128,'official aliases',17,fill=C['muted']))
parts.append(rect(245,30,180,130,C['light'],'#D1D5DB',1.2,12))
parts.append(text(335,58,'Role candidates',18,weight='bold'))
for i,(letter,color,pale) in enumerate([('P',C['Presence'],C['paleP']),('S',C['Semantic'],C['paleS']),('I',C['Instance'],C['paleI'])]):
    y=76+i*27
    parts.append(rect(258,y,155,21,pale,color,1.1,5))
    parts.append(text(268,y+15,f'{letter}  functional text',15,fill=color,anchor='start'))
parts.append(line(215,95,242,95,width=2.3,arrow=True))
parts.append(rect(455,30,390,130,'#F8FAFC',C['ink'],1.6,12))
parts.append(text(650,60,'Frozen SAM3 full grounding',19,weight='bold'))
parts.append(text(650,85,'each required prompt is grounded',17,fill=C['muted']))
for i,(letter,name,color,pale) in enumerate([('P','presence',C['Presence'],C['paleP']),('S','semantic',C['Semantic'],C['paleS']),('I','instance',C['Instance'],C['paleI'])]):
    x=476+i*117
    parts.append(rect(x,104,104,42,pale,color,1.1,7))
    parts.append(text(x+52,123,letter,17,weight='bold',fill=color))
    parts.append(text(x+52,139,name,14,fill=C['muted']))
parts.append(line(425,95,452,95,width=2.3,arrow=True))
parts.append(rect(875,30,245,130,C['paleBlue'],C['Navy'],1.6,12))
parts.append(text(998,60,'Role composition',19,weight='bold',fill=C['Navy']))
parts.append(text(998,88,'bounded residual',17))
parts.append(text(998,112,'P -> I coupling',17))
parts.append(text(998,136,'official compensation',17))
parts.append(line(845,95,872,95,width=2.3,arrow=True))
# same profile band
parts.append(rect(330,190,900,42,'#F9FAFB','#D1D5DB',1.1,10))
parts.append(text(780,217,'same selected P/S/I profile is used in both views',18,fill=C['muted']))
parts.append(line(998,160,998,187,width=2.3,arrow=True))
# views
for x,label,img in [(40,'Local / native',LOCAL),(760,'Context / wider',CONTEXT)]:
    parts.append(rect(x,275,600,112,'#FFFFFF','#9CA3AF',1.6,12))
    parts.append(image(x+18,291,78,78,img))
    parts.append(text(x+112,310,label,18,weight='bold',anchor='start'))
    parts.append(text(x+112,336,'full grounding',16,anchor='start'))
    parts.append(text(x+112,360,'role composition + class scores',16,fill=C['muted'],anchor='start'))
    parts.append(text(x+112,382,'same selected profile',15,fill=C['muted'],anchor='start'))
    parts.append(line(x+300,232,x+300,272,width=2.2,arrow=True))
parts.append(text(485,260,'each view completes full grounding',15,fill=C['muted'],anchor='start'))
# fusion bus
parts.append(line(340,387,340,415,width=2.2))
parts.append(line(1060,387,1060,415,width=2.2))
parts.append(line(340,415,1060,415,width=2.2))
parts.append(line(700,415,700,428,width=2.2,arrow=True))
parts.append(rect(455,430,430,68,C['Navy'],C['Navy'],1.6,10))
parts.append(text(670,457,'aligned view fusion Psi',19,weight='bold',fill='#FFFFFF'))
parts.append(text(670,482,'max / power / logit',15,fill='#FFFFFF'))
parts.append(rect(930,430,240,68,'#FFFFFF',C['Navy'],1.6,10))
parts.append(text(1050,457,'argmax / threshold',18,weight='bold',fill=C['Navy']))
parts.append(line(885,464,927,464,width=2.2,arrow=True))
method_overview=make_svg(1400,540,''.join(parts))

# 3. Method detail
parts=[]
# Panel a
parts.append(text(40,32,'(a) Role-functional evidence',21,weight='bold',fill=C['ink'],anchor='start'))
parts.append(rect(40,55,170,180,'#FFFFFF',C['Presence'],1.5,12))
parts.append(text(125,84,'official anchor',17,weight='bold',fill=C['Presence']))
parts.append(text(125,118,'P_A',19)); parts.append(text(125,149,'S_A',19)); parts.append(text(125,180,'I_A',19))
parts.append(rect(245,55,180,180,C['light'],'#D1D5DB',1.1,12))
parts.append(text(335,84,'candidate',17,weight='bold'))
parts.append(text(335,116,'full SAM3',17)); parts.append(text(335,142,'grounding',17))
parts.append(text(335,182,'P_r  S_r  I_r',16,fill=C['muted']))
parts.append(rect(460,55,200,180,'#FFFFFF',C['Semantic'],1.5,12))
parts.append(text(560,84,'bounded update',17,weight='bold',fill=C['Semantic']))
parts.append(text(560,116,'B(a,b)',19,weight='bold'))
parts.append(text(560,144,'alpha=0.5, tau=0.25',14,fill=C['muted']))
parts.append(text(560,174,'P -> I coupling',16))
parts.append(line(212,145,242,145,width=2.1,arrow=True)); parts.append(line(427,145,457,145,width=2.1,arrow=True))
parts.append(rect(175,285,475,85,'#F8FAFC','#D1D5DB',1.1,10))
parts.append(text(412,311,'official alias compensation',17,weight='bold'))
parts.append(text(412,336,'G = clip(G_o + F_pi - F_A)',16))
parts.append(text(412,358,'zero update returns G_o',15,fill=C['muted']))
parts.append(line(560,235,560,282,width=2.1,arrow=True))
# Panel b
parts.append(line(715,25,715,440,color='#D1D5DB',width=1.1))
parts.append(text(760,32,'(b) Joint Role-View composition',21,weight='bold',fill=C['ink'],anchor='start'))
parts.append(rect(760,55,570,65,C['paleBlue'],C['Navy'],1.4,10))
parts.append(text(1045,79,'selected profile',17,weight='bold',fill=C['Navy']))
parts.append(text(1045,102,'same P/S/I slots + admission + view operator',14,fill=C['muted']))
for x,label,img in [(760,'Local',LOCAL),(1075,'Context',CONTEXT)]:
    parts.append(rect(x,145,250,135,'#FFFFFF','#9CA3AF',1.4,10))
    parts.append(image(x+16,160,68,68,img))
    parts.append(text(x+100,179,label,17,weight='bold',anchor='start'))
    parts.append(text(x+100,205,'full grounding',15,anchor='start'))
    parts.append(text(x+100,230,'role composition',15,anchor='start'))
    parts.append(text(x+100,255,'class score',15,anchor='start'))
    parts.append(line(x+125,120,x+125,142,width=2,arrow=True))
parts.append(text(1042,300,'same profile in both views',15,fill=C['muted']))
parts.append(rect(835,325,430,70,'#FFFFFF',C['Navy'],1.5,10))
parts.append(text(1035,351,'aligned class-score fusion Psi',18,weight='bold',fill=C['Navy']))
parts.append(text(1035,375,'max / power / logit',15,fill=C['muted']))
parts.append(line(885,280,885,322,width=2,arrow=True)); parts.append(line(1200,280,1200,322,width=2,arrow=True))
parts.append(rect(1280,325,90,70,'#F8FAFC','#9CA3AF',1.1,7))
parts.append(text(1325,350,'argmax',14)); parts.append(text(1325,372,'threshold',14))
parts.append(line(1265,360,1277,360,width=1.8,arrow=True))
method_detail=make_svg(1400,460,''.join(parts))

# 4. Category gain
rows=[]
with (ROOT/'论文执笔交付包'/'03_实验与证据'/'可编辑数据'/'category_group_summary.csv').open(encoding='utf-8-sig') as f:
    for r in csv.DictReader(f): rows.append((r['category_group'],float(r['joint_delta_mean'])))
order=['Water-related','Vegetation & land cover','Built structures','Movable objects','Transport surfaces','Sports grounds','Background / clutter']
rows=[(n,next(v for k,v in rows if k==n)) for n in order]
w,h=680,370; parts=[]
# plot area
parts.append(text(50,28,'Joint ΔIoU vs matched baseline (points)',22,weight='bold',anchor='start'))
# grid and axis
x0=205; x1=620; y0=55; dy=38
for tick in range(0,11,2):
    x=x0+(x1-x0)*tick/11
    parts.append(line(x,y0-8,x,y0+dy*7-8,color='#E5E7EB',width=1))
    parts.append(text(x,y0+dy*7+13,str(tick),17,fill=C['muted']))
for i,(name,val) in enumerate(rows):
    y=y0+i*dy
    color=C['neutral'] if name.startswith('Background') else C['positive']
    parts.append(text(x0-14,y+17,name,18,anchor='end',fill=C['ink']))
    bw=(x1-x0)*val/11
    parts.append(rect(x0,y,bw,22,color,color,0.8,3))
    parts.append(text(x0+bw+8,y+17,f'+{val:.2f}',17,weight='bold',fill=color,anchor='start'))
parts.append(text(x0-18,y0+7*dy+45,'* background/clutter mean is influenced by OEM',14,fill=C['muted'],anchor='start'))
category=make_svg(w,h,''.join(parts))

# 5. Qualitative placeholder
parts=[]
headers=['RGB','GT','Baseline','Role-only','View-only','Joint']
row_names=['OEM','Vaihingen','UAVid / LoveDA']
x0=180; cellw=190; gap=12; y0=62; rowh=96; rhgap=28
for j,hname in enumerate(headers):
    x=x0+j*(cellw+gap)
    parts.append(text(x+cellw/2,32,hname,18,weight='bold',fill=C['ink']))
for i,row in enumerate(row_names):
    y=y0+i*(rowh+rhgap)
    parts.append(text(160,y+rowh/2,row,16,weight='bold',anchor='end',fill=C['ink']))
    for j,hname in enumerate(headers):
        x=x0+j*(cellw+gap)
        fill=C['paleBlue'] if j in (0,1) else C['light']
        parts.append(rect(x,y,cellw,rowh,fill,'#9CA3AF',1.1,8,dash='5 5'))
        parts.append(text(x+cellw/2,y+rowh/2-2,'placeholder',17,fill=C['muted']))
        parts.append(text(x+cellw/2,y+rowh/2+18,'real mask export required',12,fill=C['muted']))
parts.append(rect(100,450,1300,42,'#FFF7ED','#D95F02',1.2,8))
parts.append(text(750,477,'Layout placeholder only: no prediction or improvement is shown.',17,weight='bold',fill=C['Instance']))
qual=make_svg(1400,510,''.join(parts))

for name,svg in [('intro_teaser',intro),('method_overview',method_overview),('method_detail',method_detail),('category_gain',category),('qualitative_placeholder',qual)]:
    (OUT/f'{name}.svg').write_text(svg,encoding='utf-8')
print('wrote',', '.join(str(OUT/f'{n}.svg') for n in ['intro_teaser','method_overview','method_detail','category_gain','qualitative_placeholder']))
