"""Optional Pillow utility: normalize original artwork and author transition poses."""
from PIL import Image, ImageDraw
from pathlib import Path
import colorsys
from math import sin, pi, sqrt
src=Path(__file__).resolve().parent.parent/'assets'
out=src
for pose,file,scale in [('run','cat-walk-left.png',1),('sit','cat-awake.png',.72),('sleep','cat-sleep.png',.76)]:
 im=Image.open(src/file).convert('RGBA')
 if pose=='sit':
  for y in range(9):
   for x in range(im.width): im.putpixel((x,y),(0,0,0,0))
 # Normalize skull size, then pin the visible paws to the same ground line.
 frames=[]
 common_box=None
 if pose=='run':
  boxes=[im.crop((i*54,0,(i+1)*54,43)).getbbox() for i in range(3)]
  common_box=(min(b[0] for b in boxes),min(b[1] for b in boxes),max(b[2] for b in boxes),max(b[3] for b in boxes))
 for frame in range(3 if pose=='run' else 1):
  p=im.crop((frame*54,0,(frame+1)*54,43)) if pose=='run' else im.copy()
  box=common_box or p.getbbox();p=p.crop(box)
  p=p.resize((round(p.width*scale),round(p.height*scale)),Image.Resampling.NEAREST)
  canvas=Image.new('RGBA',(64,48));canvas.alpha_composite(p,((64-p.width)//2,48-p.height));frames.append(canvas)
 for color in ['nivi','livi']:
  sheet=Image.new('RGBA',(64*len(frames),48))
  for i,p in enumerate(frames): sheet.alpha_composite(p,(64*i,0))
  if color=='livi':
   for y in range(sheet.height):
    for x in range(sheet.width):
     r,g,b,a=sheet.getpixel((x,y));h,s,v=colorsys.rgb_to_hsv(r/255,g/255,b/255)
     if a and s>.25 and (h<.16 or h>.96):
      r,g,b=colorsys.hsv_to_rgb(.085,.40,(.23+.58*v) if v<.48 else (.86+.14*v))
      sheet.putpixel((x,y),(round(r*255),round(g*255),round(b*255),a))
  if color=='livi':
   for frame in range(len(frames)):
    marks=Image.new('L',(64,48));draw=ImageDraw.Draw(marks)
    if pose=='run':
     spots=[(28,28,34,34),(38,30,45,36),(36,25,40,29)]
    else:
     spots=[(33,35,39,40),(41,38,47,43),(39,30,44,34)]
    for spot in spots: draw.ellipse(spot,fill=255)
    for y in range(48):
     for x in range(64):
      r,g,b,a=sheet.getpixel((frame*64+x,y))
      # Tint only solid light fur, retaining outlines and transparent edges.
      if marks.getpixel((x,y)) and a and r>195 and g>145 and b>110:
       sheet.putpixel((frame*64+x,y),(166,100,59,a))
  sheet.save(out/f'play-{color}-{pose}.png')

# Full walk cycles share one torso, so neither cat changes shape between steps.
# During stance the paw travels backwards by the same distance as the torso
# travels forwards. Swing lifts the paw and returns it for the next contact.
WALK_FRAMES = 32
for color in ['nivi', 'livi']:
 body = Image.open(out/f'play-{color}-run.png').crop((0,0,64,36))
 sheet = Image.new('RGBA',(64*WALK_FRAMES,48))
 stride = 24 if color=='nivi' else 20
 duty = .6 if color=='nivi' else .7
 phases = (0,.5,.5,0) if color=='nivi' else (0,.5,.25,.75)
 fur, dark, paw = ('#df7128','#a44e26','#ffe1a3') if color=='nivi' else ('#efbb8d','#a6643b','#ffe2bb')
 for frame in range(WALK_FRAMES):
  canvas = Image.new('RGBA',(64,48))
  draw = ImageDraw.Draw(canvas)
  def leg(hip, phase, far):
   u=(frame/WALK_FRAMES+phase)%1
   travel=stride*duty
   if u<duty:
    dx=-travel/2+stride*u; lift=0
   else:
    v=(u-duty)/(1-duty)
    dx=travel/2-travel*(v*v*(3-2*v)); lift=4*sin(pi*v)
   hx,hy=hip; fx,fy=hx+dx,46-lift
   # Two equal-length limb segments bend rather than stretching the sprite.
   vx,vy=fx-hx,fy-hy; d=sqrt(vx*vx+vy*vy)
   bend=min(2.5,sqrt(max(0,8.5*8.5-d*d/4)))
   kx=(hx+fx)/2+vy/d*bend; ky=(hy+fy)/2-vx/d*bend
   points=[(round(hx),round(hy)),(round(kx),round(ky)),(round(fx),round(fy))]
   draw.line(points,fill=dark if far else fur,width=4)
   draw.rectangle((round(fx)-3,round(fy)-1,round(fx)+1,round(fy)+1),fill=dark if far else paw)
  leg((19,32),phases[0],True); leg((43,32),phases[1],True)
  canvas.alpha_composite(body,(0,0))
  leg((19,33),phases[2],False); leg((43,33),phases[3],False)
  sheet.alpha_composite(canvas,(frame*64,0))
 sheet.save(out/f'play-{color}-walk.png')

from PIL import Image, ImageDraw
from pathlib import Path
p=Path(__file__).resolve().parent.parent/'assets'
for color in ['nivi','livi']:
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
  ImageDraw.Draw(c).polygon([(hx+11,hy+11),(hx+18,hy+11),(32,ty+3),(32,ty+12),(hx+10,hy+18)],fill=('#d47d36' if color=='nivi' else '#edbb91'))
  head=run.crop((7,15,25,34))
  c.alpha_composite(head,(round(12-5*u),round(23-8*u)))
  c.save(p/f'play-{color}-stand{i}.png')
  # Curl down in three steps. The head lowers without rescaling it.
  c=Image.new('RGBA',(64,48))
  body=sleep.crop((29,24,52,48));c.alpha_composite(body,(29,24))
  head=sit.crop((12,19,31,44))
  c.alpha_composite(head,(12,round(19+6*u)))
  c.save(p/f'play-{color}-curl{i}.png')
