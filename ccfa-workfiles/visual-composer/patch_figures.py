from pathlib import Path
p=Path(r'D:\论文\9.27论文\ccfa-workfiles\visual-composer\draw_figures.py')
t=p.read_text(encoding='utf-8')

# Remove the extra top view thumbnails that obscured the role cards.
start=t.index("# small image strips in view cards? use tiny icons at right")
end=t.index("intro=make_svg", start)
t=t[:start]+t[end:]

overview=r'''# 2. Method overview
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

'''
s=t.index('# 2. Method overview'); e=t.index('# 3. Method detail')
t=t[:s]+overview+t[e:]

detail=r'''# 3. Method detail
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

'''
s=t.index('# 3. Method detail'); e=t.index('# 4. Category gain')
t=t[:s]+detail+t[e:]

# Increase category chart text sizes for final single-column width.
t=t.replace("text(50,28,'Joint ΔIoU vs matched baseline (points)',18", "text(50,28,'Joint ΔIoU vs matched baseline (points)',22")
t=t.replace("text(x0-14,y+17,name,15", "text(x0-14,y+17,name,18")
t=t.replace("text(x0+bw+8,y+17,f'+{val:.2f}',14", "text(x0+bw+8,y+17,f'+{val:.2f}',17")
t=t.replace("text(x,y0+dy*7+13,str(tick),14", "text(x,y0+dy*7+13,str(tick),17")
t=t.replace("text(x0-18,y0+7*dy+45,'* background/clutter mean is influenced by OEM',12", "text(x0-18,y0+7*dy+45,'* background/clutter mean is influenced by OEM',14")

qual=r'''# 5. Qualitative placeholder
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

'''
s=t.index('# 5. Qualitative placeholder'); e=t.index('for name,svg in',s)
t=t[:s]+qual+t[e:]
p.write_text(t,encoding='utf-8',newline='\n')
print('patched figure generator')
