"""
generate_diagrams.py — gera os 6 diagramas do ensaio "Billie Jean — Structural Analysis".
Uso:  pip install Pillow && python generate_diagrams.py [pasta_de_saida]
Os diagramas são ESQUEMÁTICOS (didáticos), não transcrições da gravação original.
"""
import os, sys
from PIL import Image, ImageDraw, ImageFont

OUT = sys.argv[1] if len(sys.argv) > 1 else "diagramas"
os.makedirs(OUT, exist_ok=True)

BG, GOLD, WHITE = (15,15,15), (196,160,80), (235,235,230)
GRAY, DIM, RED, GREEN = (130,130,125), (60,60,58), (180,70,60), (80,160,100)
W = 1200

def font(size, bold=False, mono=False):
    names = (["DejaVuSansMono.ttf","LiberationMono-Regular.ttf"] if mono else
             ["DejaVuSerif-Bold.ttf","LiberationSerif-Bold.ttf"] if bold else
             ["DejaVuSerif.ttf","LiberationSerif-Regular.ttf","FreeSerif.ttf"])
    for d in ("/usr/share/fonts/truetype/dejavu/","/usr/share/fonts/truetype/liberation/","/usr/share/fonts/truetype/freefont/"):
        for n in names:
            if os.path.exists(d+n): return ImageFont.truetype(d+n, size)
    return ImageFont.load_default()

F = dict(title=font(36,True), sub=font(22), label=font(20,True), body=font(20),
         small=font(17), tiny=font(16,mono=True))

def canvas(h):
    img = Image.new("RGB",(W,h),BG); return img, ImageDraw.Draw(img)
def rule(d,y,c=DIM): d.line([(60,y),(W-60,y)], fill=c, width=1)
def header(d,title,sub):
    d.text((W//2,44),title,font=F["title"],fill=GOLD,anchor="mm")
    d.text((W//2,84),sub,font=F["sub"],fill=GRAY,anchor="mm"); rule(d,108,GOLD)
def footer(d,y,text): rule(d,y-28,GOLD); d.text((W//2,y),text,font=F["sub"],fill=GOLD,anchor="mm")
def save(img,name): img.save(os.path.join(OUT,name)); print("  ok",name)

def cell_row(d, label, notes, funcs, colors, y_label, y_note):
    d.text((80,y_label),label,font=F["label"],fill=GRAY)
    xs = [260+i*195 for i in range(4)]
    for i,(n,fn,c,x) in enumerate(zip(notes,funcs,colors,xs)):
        d.ellipse([x-32,y_note-32,x+32,y_note+32],outline=c,width=2)
        d.text((x,y_note),n,font=F["label"],fill=c,anchor="mm")
        d.text((x,y_note+45),f"[{fn}]",font=F["tiny"],fill=GRAY,anchor="mm")
        if i<3: d.line([(x+36,y_note),(xs[i+1]-36,y_note)],fill=GRAY,width=1)

def d1():
    img,d = canvas(520); header(d,"VERWANDLUNG","Célula intervalar — State of Independence (1981) → Billie Jean (1982)")
    cell_row(d,"State of Independence (1981)",["F♯","A","B","E"],["repouso","tensão","pivô","abertura"],[GREEN,GOLD,GOLD,WHITE],140,205)
    rule(d,272)
    cell_row(d,"Billie Jean (1982)",["B","F♯","A","E"],["impulso","âncora","tensão","res. suspensa"],[GOLD,GREEN,GOLD,WHITE],300,365)
    footer(d,478,"Mesmo DNA intervalar · organismo rítmico novo"); save(img,"diagram_1_verwandlung.png")

def grid16(d, x0, x1, top, bottom):
    sw=(x1-x0)/16; xs=[int(x0+(i+.5)*sw) for i in range(16)]
    labs=["1","e","+","a"]*4
    for i,(x,l) in enumerate(zip(xs,labs)):
        d.text((x,128),str((i//4)+1) if i%4==0 else l,font=F["tiny"],fill=GOLD if i%4==0 else DIM,anchor="mm")
    for i in (0,4,8,12): d.line([(xs[i]-int(sw//2),116),(xs[i]-int(sw//2),bottom)],fill=DIM,width=1)
    return xs

def rows(d, xs, spec, x_label=100):
    for name,hits,col,y in spec:
        d.text((x_label,y),name,font=F["label"],fill=col,anchor="mm")
        for i,x in enumerate(xs):
            if i in hits:
                r = 5 if name=="Hi-Hat" else 9
                d.ellipse([x-r,y-r,x+r,y+r],fill=col)

def d2():
    img,d = canvas(460); header(d,"O COMPASSO QUE RESPIRA","Expectativa métrica × realidade rítmica (esquema didático)")
    bx=[220,420,620,820]
    for x,b in zip(bx,"1234"):
        d.text((x,130),b,font=F["label"],fill=GOLD,anchor="mm"); d.line([(x,115),(x,400)],fill=DIM,width=1)
    for lab,y in (("Pulso formal",168),("Expectativa",228),("Realidade",298)): d.text((100,y),lab,font=F["small"],fill=GRAY,anchor="mm")
    for x in bx: d.ellipse([x-8,160,x+8,176],fill=WHITE)
    for x,t,c in zip(bx,["forte","fraco","forte","fraco"],[WHITE,GRAY,WHITE,GRAY]): d.text((x,228),f"[{t}]",font=F["tiny"],fill=c,anchor="mm")
    for x,t,c in zip(bx,["forte","antecipa↑","forte+","desloca↓"],[WHITE,GOLD,WHITE,RED]): d.text((x,298),f"[{t}]",font=F["tiny"],fill=c,anchor="mm")
    d.text((bx[1],335),"síncope entra\nantes do tempo 2",font=F["tiny"],fill=GOLD,anchor="mm")
    d.text((bx[3],335),"baixo prepara\no próximo 1",font=F["tiny"],fill=GOLD,anchor="mm")
    footer(d,435,"Nunca onde se espera · sempre onde precisa estar"); save(img,"diagram_2_metric.png")

BASS = {0,2,3,4,6,7}  # esquema: 8 colcheias do baixo mapeadas na grade de 16 posições (colcheias = posições pares)
BASS_POS = [0,2,4,6,8,10,12,14]

def d3():
    img,d = canvas(500); header(d,"CONTRAPONTO INSTRUMENTAL","1 compasso de 4/4 · quatro vozes independentes (esquema didático)")
    xs=grid16(d,180,W-60,116,450)
    rows(d,xs,[("Bumbo",{0,8},GOLD,178),("Caixa",{4,12},WHITE,248),("Hi-Hat",set(BASS_POS),GRAY,318),("Baixo",set(BASS_POS),GREEN,388)])
    footer(d,478,"Cada voz com autonomia · juntas, coesão absoluta"); save(img,"diagram_3_polyrhythm.png")

def d4():
    img,d = canvas(440); header(d,"O FANTASMA NA MÁQUINA","Pré-delay de reverb na caixa · esquema ilustrativo")
    bx=[160,400,640,880]
    for x,b in zip(bx,"1234"):
        d.text((x,155),b,font=F["label"],fill=GOLD,anchor="mm"); d.line([(x,168),(x,390)],fill=DIM,width=1)
    for si in (1,3):
        sx=bx[si]; d.ellipse([sx-14,186,sx+14,214],fill=WHITE); d.text((sx,228),"ataque seco",font=F["tiny"],fill=WHITE,anchor="mm")
        end=sx+220
        for s in range(18):
            a=int(140*(1-s/18)); tx=sx+14+int(s*(end-sx-14)/18)
            d.rectangle([tx,192,tx+int((end-sx-14)/18)+1,208],fill=(a,int(a*.7),0))
        d.text(((sx+end)//2,258),"cauda do reverb invade o tempo seguinte",font=F["tiny"],fill=GOLD,anchor="mm")
    rule(d,310); d.text((W//2,350),"2 eventos percebidos onde há 1 · o compasso se dilata",font=F["body"],fill=WHITE,anchor="mm")
    footer(d,418,"Engenheirado para respirar"); save(img,"diagram_4_ghost.png")

def d5():
    img,d = canvas(480); header(d,"A ARQUITETURA DO SILÊNCIO","Minimalismo · cada nota tem função · cada pausa trabalha (esquema didático)")
    xs=grid16(d,200,W-80,116,420)
    rows(d,xs,[("Bumbo",{0,8},GOLD,165),("Caixa",{4,12},WHITE,225),("Hi-Hat",set(BASS_POS),GRAY,285),("Baixo",set(BASS_POS)-{4},GREEN,345)])
    x=xs[4]; d.rectangle([x-18,327,x+18,363],outline=RED,width=1); d.text((x,345),"—",font=F["label"],fill=RED,anchor="mm")
    d.text((100,405),"Pads",font=F["small"],fill=DIM,anchor="mm")
    d.text((W//2,405),"~~~ sustentação harmônica contínua ~~~",font=F["tiny"],fill=DIM,anchor="mm")
    d.text((x,382),"silêncio funcional",font=F["tiny"],fill=RED,anchor="mm")
    footer(d,462,"O silêncio trabalha tanto quanto qualquer nota"); save(img,"diagram_5_silence.png")

def d6():
    img,d = canvas(440); header(d,"A LINHA DE BAIXO","Fá♯ · função harmônica · resolução perpetuamente adiada")
    steps=[("I","F♯","âncora",GREEN),("—","—","vazio",RED),("V","C♯","tensão",GOLD),("♭VII","E","prepara I",WHITE)]
    xs=[200,430,660,890]
    for i,((deg,n,fn,c),x) in enumerate(zip(steps,xs)):
        d.text((x,168),deg,font=F["label"],fill=GOLD,anchor="mm")
        if n=="—": d.rectangle([x-38,202,x+38,278],outline=c,width=1)
        else: d.ellipse([x-38,202,x+38,278],outline=c,width=2)
        d.text((x,240),n,font=F["label"],fill=c,anchor="mm"); d.text((x,298),f"[{fn}]",font=F["tiny"],fill=GRAY,anchor="mm")
        if i<3: d.line([(x+46,240),(xs[i+1]-46,240)],fill=GRAY,width=1)
    footer(d,418,"O adiamento da resolução mantém o corpo dançando"); save(img,"diagram_6_bassline.png")

if __name__ == "__main__":
    print("Gerando diagramas em", OUT)
    for f in (d1,d2,d3,d4,d5,d6): f()
