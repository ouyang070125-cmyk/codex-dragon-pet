"""Rebuild the desktop v2 pet from local source PNGs. No installation or network."""
from pathlib import Path
from PIL import Image, ImageOps
import argparse, json

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--source-dir', type=Path, default=Path(__file__).resolve().parents[1]/'sources')
parser.add_argument('--output-dir', type=Path, required=True)
args = parser.parse_args()
pet = args.output_dir
pet.mkdir(parents=True, exist_ok=True)
sources = {name: args.source_dir / (name + '.png') for name in ['base', 'emotions', 'directions']}
def trim(im):
    im = im.convert("RGBA")
    bbox = im.getchannel("A").getbbox()
    return im.crop(bbox) if bbox else im
base = trim(Image.open(sources["base"]))
emo = Image.open(sources["emotions"]).convert("RGBA")
directions = Image.open(sources["directions"]).convert("RGBA")
def quadrants(im):
    w,h=im.size
    return [trim(im.crop(box)) for box in [(0,0,w//2,h//2),(w//2,0,w,h//2),(0,h//2,w//2,h),(w//2,h//2,w,h)]]
wave,ask,sad,focus = quadrants(emo)
up,right,down,left = quadrants(directions)
W,H=192,208
atlas=Image.new("RGBA",(W*8,H*11),(0,0,0,0))
def paste(im,row,col,dx=0,dy=0,flip=False,scale=1.0):
    im=ImageOps.mirror(im) if flip else im
    maxw,maxh=int(178*scale),int(194*scale)
    ratio=min(maxw/im.width,maxh/im.height)
    im=im.resize((max(1,round(im.width*ratio)),max(1,round(im.height*ratio))),Image.Resampling.LANCZOS)
    x=col*W+(W-im.width)//2+dx
    y=row*H+H-im.height-5+dy
    atlas.alpha_composite(im,(x,y))
spec=[
 (base,6,[(0,0),(0,-1),(0,-2),(0,-1),(0,0),(0,1)]),
 (right,8,[(0,0),(2,-1),(4,0),(6,-1),(8,0),(6,-1),(4,0),(2,-1)]),
 (left,8,[(0,0),(-2,-1),(-4,0),(-6,-1),(-8,0),(-6,-1),(-4,0),(-2,-1)]),
 (wave,4,[(0,0),(0,-1),(0,-2),(0,-1)]),
 (base,5,[(0,0),(0,-5),(0,-9),(0,-5),(0,0)]),
 (sad,8,[(0,0),(0,1),(0,2),(0,1),(0,0),(0,1),(0,2),(0,1)]),
 (ask,6,[(0,0),(0,-1),(0,-2),(0,-1),(0,0),(0,1)]),
 (focus,6,[(0,0),(0,-1),(0,0),(0,1),(0,0),(0,-1)]),
 (down,6,[(0,0),(1,0),(0,0),(-1,0),(0,0),(1,0)])
]
for row,(im,n,offsets) in enumerate(spec):
    for col,(dx,dy) in enumerate(offsets):
        paste(im,row,col,dx,dy)
paste(base,0,6)
# 16 pointer directions, clockwise from twelve o'clock.
lookup=[up,up,right,right,right,right,down,down,down,down,left,left,left,left,up,up]
for i,im in enumerate(lookup):
    paste(im,9+i//8,i%8)
# Remove hidden RGB beneath fully transparent pixels, required by atlas validator.
px=atlas.load()
for y in range(atlas.height):
    for x in range(atlas.width):
        r,g,b,a=px[x,y]
        if a==0 and (r or g or b): px[x,y]=(0,0,0,0)
atlas.save(pet/"spritesheet.webp",format="WEBP",lossless=True,quality=100,method=6)
atlas.save(pet/"spritesheet.png")
manifest={
 "id":"gpt-dragon",
 "displayName":"GPT龙娘",
 "description":"白发紫眸、龙角双翼与长尾的 GPT 拟人桌宠。",
 "spriteVersionNumber":2,
 "spritesheetPath":"spritesheet.webp"
}
(pet/"pet.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding="utf-8")
print("Built desktop v2 pet in", pet)
