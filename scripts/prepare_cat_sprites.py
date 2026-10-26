"""Optional Pillow utility: normalize original artwork and author transition poses."""
from PIL import Image
from pathlib import Path
import colorsys
src=Path(__file__).resolve().parent.parent/'assets'
out=src
for pose,file,scale in [('run','cat-walk-left.png',1),('sit','cat-awake.png',.72),('sleep','cat-sleep.png',.76)]:
 im=Image.open(src/file).convert('RGBA')
 if pose=='sit':
  for y in range(9):
   for x in range(im.width): im.putpixel((x,y),(0,0,0,0))
 # Normalize skull size, then pin the visible paws to the same ground line.
 frames=[]
 for frame in range(3 if pose=='run' else 1):
  p=im.crop((frame*54,0,(frame+1)*54,43)) if pose=='run' else im.copy()
  box=p.getbbox();p=p.crop(box)
  p=p.resize((round(p.width*scale),round(p.height*scale)),Image.Resampling.NEAREST)
  canvas=Image.new('RGBA',(64,48));canvas.alpha_composite(p,((64-p.width)//2,48-p.height));frames.append(canvas)
 for color in ['ginger','slate']:
  sheet=Image.new('RGBA',(64*len(frames),48))
  for i,p in enumerate(frames): sheet.alpha_composite(p,(64*i,0))
  if color=='slate':
   for y in range(sheet.height):
    for x in range(sheet.width):
     r,g,b,a=sheet.getpixel((x,y));h,s,v=colorsys.rgb_to_hsv(r/255,g/255,b/255)
     if a and s>.25 and (h<.16 or h>.96):
      r,g,b=colorsys.hsv_to_rgb(.585,min(s*.42,.36),v*.86+.07)
      sheet.putpixel((x,y),(round(r*255),round(g*255),round(b*255),a))
  sheet.save(out/f'play-{color}-{pose}.png')

from PIL import Image, ImageDraw
from pathlib import Path
p=Path(__file__).resolve().parent.parent/'assets'
for color in ['ginger','slate']:
 run=Image.open(p/f'play-{color}-run.png').crop((0,0,64,48))
 sit=Image.open(p/f'play-{color}-sit.png')
 sleep=Image.open(p/f'play-{color}-sleep.png')
 for i in range(1,4):
  u=i/4
  c=Image.new('RGBA',(64,48))
  # Unfold the torso and paws, retaining the same head pixels and skull size.
  legs=run.crop((7,36,49,48)).resize((42,round(5+7*u)),Image.Resampling.NEAREST)
  c.alpha_composite(legs,(7,48-legs.height))
  torso=run.crop((24,25,48,38)).resize((round(18+6*u),13),Image.Resampling.NEAREST)
  c.alpha_composite(torso,(24,round(34-9*u)))
  tail=run.crop((48,7,57,32)).resize((9,round(9+16*u)),Image.Resampling.NEAREST)
  c.alpha_composite(tail,(45,round(34-27*u)))
  hx,hy=round(12-5*u),round(23-8*u)
  ty=round(34-9*u)
  ImageDraw.Draw(c).polygon([(hx+11,hy+11),(hx+18,hy+11),(32,ty+3),(32,ty+12),(hx+10,hy+18)],fill=('#d47d36' if color=='ginger' else '#7e929e'))
  head=run.crop((7,15,25,34))
  c.alpha_composite(head,(round(12-5*u),round(23-8*u)))
  c.save(p/f'play-{color}-stand{i}.png')
  # Curl down in three steps. The head lowers without rescaling it.
  c=Image.new('RGBA',(64,48))
  body=sleep.crop((29,24,52,48));c.alpha_composite(body,(29,24))
  head=sit.crop((12,19,31,44))
  c.alpha_composite(head,(12,round(19+6*u)))
  c.save(p/f'play-{color}-curl{i}.png')
