"""Render documentation previews from the real desktop sprite frames."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
atlas = Image.open(ROOT/'skills/install-gpt-dragon-pet/assets/gpt-dragon/spritesheet.webp').convert('RGBA')
out = ROOT/'previews'
out.mkdir(exist_ok=True)
font_path = Path('C:/Windows/Fonts/msyh.ttc')
def font(size):
    return ImageFont.truetype(str(font_path), size) if font_path.exists() else ImageFont.load_default(size=size)
def frame(row, col=0):
    return atlas.crop((col*192,row*208,(col+1)*192,(row+1)*208))
def label(draw, xy, text, size=20, fill='#625976'):
    draw.text(xy,text,font=font(size),fill=fill)

hero = Image.new('RGB',(1280,640),'#f5f2fa')
d = ImageDraw.Draw(hero)
d.rounded_rectangle((35,35,1245,605),radius=32,fill='#fdfcff',outline='#e1daee',width=2)
label(d,(85,88),'GPT / DRAGON GIRL',22)
label(d,(80,155),'GPT龙娘',70,'#3e3553')
label(d,(85,263),'银发 · 白角 · 淡紫双翼',28)
label(d,(85,320),'陪你把每一个想法，慢慢变成现实。',24)
label(d,(85,445),'CODEX DESKTOP COMPANION',20)
label(d,(85,485),'9 states   /   desktop v2   /   open source',18)
hero.paste(frame(0).resize((432,468),Image.Resampling.LANCZOS),(770,80),frame(0).resize((432,468),Image.Resampling.LANCZOS))
hero.save(out/'cover.png')
names=['Idle / 待机','Right / 向右','Left / 向左','Wave / 挥手','Jump / 跳跃','Failed / 失落','Waiting / 等待','Running / 专注','Review / 检查']
grid=Image.new('RGB',(930,900),'#f5f2fa')
gd=ImageDraw.Draw(grid)
for row,name in enumerate(names):
    x=(row%3)*310; y=(row//3)*300
    gd.rounded_rectangle((x+12,y+12,x+298,y+288),radius=20,fill='#fdfcff',outline='#e1daee')
    grid.paste(frame(row),(x+59,y+27),frame(row))
    label(gd,(x+35,y+245),name,19)
grid.save(out/'states.png')
frames=[]
for i in range(6):
    im=Image.new('RGB',(320,300),'#f5f2fa')
    im.paste(frame(0,i),(64,24),frame(0,i))
    label(ImageDraw.Draw(im),(47,260),'GPT龙娘 · Idle',20)
    frames.append(im)
frames[0].save(out/'idle.gif',save_all=True,append_images=frames[1:],duration=120,loop=0,optimize=False,disposal=2)
print('Rendered cover, states and 6-frame idle GIF (120ms/frame).')
