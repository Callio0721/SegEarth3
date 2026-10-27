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
PURPLEF=(241,235,250,245); TEALF=(231,247,245,245); ORANGEF=(255,245,236,245)
BLUE=(231,239,249,245); WHITE=(255,255,255,255)
FONT=r"C:\Windows\Fonts\times.ttf"; FONTB=r"C:\Windows\Fonts\timesbd.ttf"
if not Path(FONTB).exists(): FONTB=FONT

def f(sz,b=False): return ImageFont.truetype(FONTB if b else FONT,sz)
def tx(x,y,s,sz=26,c=NAVY,a="la",b=False): d.text((x,y),s,font=f(sz,b),fill=c,anchor=a)
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
        d.line((x,y1,min(x+seg,x2-r),y1),fill=c,width=w); d.line((x,y2,min(x+seg,x2-r),y2),fill=c,width=w)
    for y in range(y1+r,y2-r,seg+gap):
        d.line((x1,y,x1,min(y+seg,y2-r)),fill=c,width=w); d.line((x2,y,x2,min(y+seg,y2-r)),fill=c,width=w)
    for b0,a0,a1 in [((x1,y1,x1+2*r,y1+2*r),180,270),((x2-2*r,y1,x2,y1+2*r),270,360),((x1,y2-2*r,x1+2*r,y2),90,180),((x2-2*r,y2-2*r,x2,y2),0,90)]:
        d.arc(b0,a0,a1,fill=c,width=w)

# panel c
dashed_border((820,350,1955,952),c=NAVY,w=4,r=30)
tx(858,360,"(c) Joint Role–View Composition",44,NAVY,b=True)

# Explicit role profile, no question marks
tx(880,402,"Selected role profile  (same configuration for both views)",25,NAVY,b=True)
# P chip
rr((880,430,1170,486),PURPLEF,PURPLE,2,16)
tx(895,443,"P  slot 1",20,PURPLE,b=True)
tx(995,443,"visible roadway",20,NAVY)
# S chip
rr((1195,430,1510,486),TEALF,TEAL,2,16)
tx(1210,443,"S  slot 2",20,TEAL,b=True)
tx(1315,443,"continuous paved road surface",18,NAVY)
# I chip
rr((1535,430,1855,486),ORANGEF,ORANGE,2,16)
tx(1550,443,"I  slot 3",20,ORANGE,b=True)
tx(1655,443,"connected road region",19,NAVY)
tx(881,490,"slot 0 = anchor;  1/2/3 = selected candidate.  Profile is fixed at inference.",17,GREY)

# profile handoff from the top role bus
d.line((1735,336,1735,410),fill=(102,133,166,255),width=3)
d.line((1735,410,1855,410),fill=(102,133,166,255),width=3)
arrow((1890,410),(1855,410),c=(102,133,166,255),w=3,head=12)

# profile fan-out to the two view branches
d.line((1360,486,1360,508),fill=(102,133,166,255),width=3)
d.line((1360,508,1025,508),fill=(102,133,166,255),width=3)
arrow((1025,508),(1025,525),c=(102,133,166,255),w=3,head=12,dash=True)
d.line((1360,508,1588,508),fill=(102,133,166,255),width=3)
d.line((1588,508,1588,690),fill=(102,133,166,255),width=3)
arrow((1588,690),(1510,690),c=(102,133,166,255),w=3,head=12)
tx(1600,555,"same profile",19,(70,100,130,255))

# local lane
rr((880,525,1560,650),TEALF,TEAL,3,22)
tx(915,535,"Local / native view",28,TEAL,b=True)
rr((925,572,1110,632),(238,243,248,250),(120,140,158,255),2,12)
tx(1018,591,"Frozen SAM3",23,NAVY,"mm",True)
tx(1018,615,"anchor + selected prompts",15,GREY,"mm")
arrow((1110,602),(1145,602),SLATE,3,10)
rr((1145,563,1360,642),(234,242,250,250),(102,133,166,255),2,12)
tx(1252,577,"Bounded correction",20,NAVY,"mm",True)
tx(1252,599,"B(a_A, a_π)",23,NAVY,"mm",True)
tx(1252,623,"P → I recoupling",16,PURPLE,"mm",True)
arrow((1360,602),(1395,602),SLATE,3,10)
rr((1395,572,1545,632),(245,249,252,250),TEAL,2,12)
tx(1470,602,"G_L,π",27,TEAL,"mm",True)
arrow((716,575),(880,588),TEAL,3,head=12,dash=True)

# context lane
rr((880,690,1560,815),ORANGEF,ORANGE,3,22)
tx(915,700,"Context / wider view",28,ORANGE,b=True)
rr((925,737,1110,797),(238,243,248,250),(120,140,158,255),2,12)
tx(1018,756,"Frozen SAM3",23,NAVY,"mm",True)
tx(1018,780,"anchor + selected prompts",15,GREY,"mm")
arrow((1110,767),(1145,767),SLATE,3,10)
rr((1145,728,1360,807),(234,242,250,250),(102,133,166,255),2,12)
tx(1252,742,"Bounded correction",20,NAVY,"mm",True)
tx(1252,764,"B(a_A, a_π)",23,NAVY,"mm",True)
tx(1252,788,"P → I recoupling",16,PURPLE,"mm",True)
arrow((1360,767),(1395,767),SLATE,3,10)
rr((1395,737,1545,797),(255,249,244,250),ORANGE,2,12)
tx(1470,767,"G_G,π",27,ORANGE,"mm",True)
arrow((716,835),(880,758),ORANGE,3,head=12,dash=True)

# explicit bounded correction formula
rr((880,835,1560,930),(250,252,254,245),(150,165,180,255),2,16)
tx(900,847,"Bounded correction used in both branches",20,NAVY,b=True)
tx(900,876,"B(a_A,a_π) = clip[0,1] ( a_A + α · clip(a_π − a_A, −τ, τ) )",20,NAVY)
tx(900,906,"α = 0.5,  τ = 0.25   →   max change per element = ατ = 0.125;   p̃ rebuilds I",17,GREY)

# fusion and decision
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

# legend
tx(860,945,"solid: data / computation       dashed: shared configuration / profile",16,GREY)

outimg=Image.alpha_composite(base,ov).convert("RGB")
outimg.save(out/"next_step_annotation_v3.png",quality=95)
print(out/"next_step_annotation_v3.png")