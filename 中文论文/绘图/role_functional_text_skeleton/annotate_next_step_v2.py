from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import math

src = Path(r"C:\Users\ZHANGB~1\AppData\Local\Temp\codex-clipboard-049bebe8-6df2-40c1-8ad6-f1fd0c25d3e2.png")
out = Path(r"D:\论文\9.27论文\中文论文\绘图\role_functional_text_skeleton")
base = Image.open(src).convert("RGBA")
W, H = base.size
ov = Image.new("RGBA", (W, H), (255, 255, 255, 0))
d = ImageDraw.Draw(ov)

NAVY=(22,50,79,255); SLATE=(60,82,104,255); GREY=(110,122,134,255)
PURPLE=(114,87,163,255); TEAL=(49,125,121,255); ORANGE=(198,120,63,255)
BLUE=(231,239,249,240); TEALF=(231,247,245,240); ORANGEF=(255,245,236,240)
WHITE=(255,255,255,255)
FONT=r"C:\Windows\Fonts\times.ttf"
FONTB=r"C:\Windows\Fonts\timesbd.ttf"
if not Path(FONTB).exists(): FONTB=FONT

def f(sz,b=False): return ImageFont.truetype(FONTB if b else FONT,sz)
def tx(x,y,s,sz=28,c=NAVY,a="la",b=False): d.text((x,y),s,font=f(sz,b),fill=c,anchor=a)
def rr(box,fill,outline,w=3,r=18): d.rounded_rectangle(box,radius=r,fill=fill,outline=outline,width=w)
def dash_line(p1,p2,c=SLATE,w=3,dash=13,gap=8):
    x1,y1=p1; x2,y2=p2; L=math.hypot(x2-x1,y2-y1)
    if L==0: return
    ux,uy=(x2-x1)/L,(y2-y1)/L; t=0
    while t<L:
        a=(x1+ux*t,y1+uy*t); b=(x1+ux*min(t+dash,L),y1+uy*min(t+dash,L))
        d.line((a,b),fill=c,width=w); t+=dash+gap
def arrow(p1,p2,c=SLATE,w=4,head=13,dash=False):
    if dash: dash_line(p1,p2,c,w)
    else: d.line((p1,p2),fill=c,width=w)
    x1,y1=p1; x2,y2=p2; ang=math.atan2(y2-y1,x2-x1)
    a1=ang+math.pi*0.82; a2=ang-math.pi*0.82
    q1=(x2+head*math.cos(a1),y2+head*math.sin(a1)); q2=(x2+head*math.cos(a2),y2+head*math.sin(a2))
    d.polygon([p2,q1,q2],fill=c)

def dashed_border(box,c=NAVY,w=4,r=30):
    x1,y1,x2,y2=box; seg=16; gap=10
    for x in range(x1+r,x2-r,seg+gap):
        d.line((x,y1,min(x+seg,x2-r),y1),fill=c,width=w)
        d.line((x,y2,min(x+seg,x2-r),y2),fill=c,width=w)
    for y in range(y1+r,y2-r,seg+gap):
        d.line((x1,y,x1,min(y+seg,y2-r)),fill=c,width=w)
        d.line((x2,y,x2,min(y+seg,y2-r)),fill=c,width=w)
    d.arc((x1,y1,x1+2*r,y1+2*r),180,270,fill=c,width=w)
    d.arc((x2-2*r,y1,x2,y1+2*r),270,360,fill=c,width=w)
    d.arc((x1,y2-2*r,x1+2*r,y2),90,180,fill=c,width=w)
    d.arc((x2-2*r,y2-2*r,x2,y2),0,90,fill=c,width=w)

# New panel (c), aligned to the existing canvas height
dashed_border((820,350,1955,952),c=NAVY,w=4,r=30)
tx(858,360,"(c) Joint Role–View Composition",44,NAVY,b=True)

# Shared role profile. Existing top role arrows merge at the bus above.
rr((980,410,1490,480),BLUE,(102,133,166,255),2,20)
tx(1235,445,"Shared role profile  π = (P?, S?, I?)",29,NAVY,"mm",True)
# Route from the old top bus around the title into profile
d.line((1735,336,1735,445),fill=(102,133,166,255),width=3)
d.line((1735,445,1490,445),fill=(102,133,166,255),width=3)
arrow((1530,445),(1490,445),c=(102,133,166,255),w=3,head=12)

# Local branch
rr((880,525,1560,650),TEALF,TEAL,3,22)
tx(915,536,"Local / native view",29,TEAL,b=True)
rr((930,572,1120,632),(238,243,248,250),(120,140,158,255),2,12)
tx(1025,602,"Frozen SAM3",25,NAVY,"mm",True)
arrow((1120,602),(1160,602),SLATE,4)
rr((1160,572,1320,632),(234,242,250,250),(102,133,166,255),2,12)
tx(1240,602,"Rπ",29,NAVY,"mm",True)
arrow((1320,602),(1360,602),SLATE,4)
rr((1360,572,1545,632),(245,249,252,250),TEAL,2,12)
tx(1452,602,"G_L,π",29,TEAL,"mm",True)
arrow((716,575),(880,588),TEAL,3,head=12,dash=True)

# Context branch
rr((880,690,1560,815),ORANGEF,ORANGE,3,22)
tx(915,701,"Context / wider view",29,ORANGE,b=True)
rr((930,737,1120,797),(238,243,248,250),(120,140,158,255),2,12)
tx(1025,767,"Frozen SAM3",25,NAVY,"mm",True)
arrow((1120,767),(1160,767),SLATE,4)
rr((1160,737,1320,797),(234,242,250,250),(102,133,166,255),2,12)
tx(1240,767,"Rπ",29,NAVY,"mm",True)
arrow((1320,767),(1360,767),SLATE,4)
rr((1360,737,1545,797),(255,249,244,250),ORANGE,2,12)
tx(1452,767,"G_G,π",29,ORANGE,"mm",True)
arrow((716,835),(880,758),ORANGE,3,head=12,dash=True)

# Profile to two branches; route context connection around the local branch
arrow((1120,480),(1120,525),(102,133,166,255),3,12,dash=True)
d.line((1490,445,1588,445),fill=(102,133,166,255),width=3)
d.line((1588,445,1588,690),fill=(102,133,166,255),width=3)
arrow((1588,690),(1500,690),(102,133,166,255),3,12)
tx(1598,565,"same π",22,(70,100,130,255),'la',False)

# Fusion and decision
arrow((1545,602),(1605,670),SLATE,4)
arrow((1545,767),(1605,730),SLATE,4)
rr((1605,640,1780,780),TEALF,TEAL,3,20)
tx(1692,677,"Aligned fusion",25,NAVY,"mm",True)
tx(1692,714,"Ψω",31,TEAL,"mm",True)
tx(1692,750,"max / power / logit",18,GREY,"mm")
arrow((1780,710),(1815,710),SLATE,4)
rr((1815,655,1940,765),NAVY,NAVY,2,16)
tx(1877,685,"argmax +",20,WHITE,"mm",True)
tx(1877,714,"threshold",20,WHITE,"mm",True)
tx(1877,744,"Ŷ",24,WHITE,"mm",True)

# Minimal legend, clear of the panel content
tx(860,900,"solid: data / computation     dashed: shared profile",20,GREY)

outimg=Image.alpha_composite(base,ov).convert("RGB")
outimg.save(out/"next_step_annotation_v2.png",quality=95)
print(out/"next_step_annotation_v2.png")