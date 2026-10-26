#!/usr/bin/env python3
"""Deterministic 24-second playground: shared contact times, ballistic bounces."""
import base64
from math import pi
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DURATION = 24
GROUND = 150
FPS = 30


def ease(t, a, b, x, y):
    u = max(0, min(1, (t-a)/(b-a)))
    return x+(y-x)*(u*u*(3-2*u))


def bounce(t, start, speed):
    """Gravity in px/s² and coefficient of restitution; no floor penetration."""
    elapsed = t-start
    if elapsed < 0:
        return 0
    gravity = 200
    for _ in range(8):
        flight = 2*speed/gravity
        if elapsed <= flight:
            return speed*elapsed-.5*gravity*elapsed*elapsed
        elapsed -= flight
        speed *= .45
    return 0


def state(t):
    # Paw contacts: ginger at 4s, slate at 6s, ginger again at 10s.
    if t < 4: bx = 286
    elif t < 6:
        u=t-4; bx=286+160*u-9*u*u
    elif t < 10:
        u=t-6; bx=570-130*u+9*u*u
    elif t < 12:
        u=t-10; bx=194+92*u-23*u*u
    else: bx=286
    lift = bounce(t,4,70) if t < 6 else bounce(t,6,90) if t < 10 else bounce(t,10,35)
    by = GROUND-8-lift
    # Walking sprite's front paw is about 26 px from its root.
    if t < 2: ax=150
    elif t < 4: ax=ease(t,2,4,150,252)
    elif t < 5.2: ax=ease(t,4,5.2,252,400)
    elif t < 6.4: ax=400+(t-5.2)/1.2*128
    elif t < 6.8: ax=72+(t-6.4)/.4*56
    elif t < 9.8: ax=ease(t,6.8,9.8,128,160)
    elif t < 12: ax=160
    elif t < 14: ax=ease(t,12,14,160,150)
    else: ax=150
    # Ballistic leap, landing at the portal before running through it.
    u=max(0,min(1,(t-5.2)/.9))
    ay=GROUND-4*34*u*(1-u)
    if 6.4 <= t <= 6.8:
        u=(t-6.4)/.4;ay=GROUND-4*8*u*(1-u)
    if t < 3: cx=680
    elif t < 6: cx=ease(t,3,6,680,604)
    elif t < 10.5: cx=604
    elif t < 14: cx=ease(t,10.5,14,604,680)
    else: cx=680
    def pose(running, sleeping):
        return 'sleep' if sleeping else 'run' if running else 'sit'
    # Brief held walking poses at impacts keep the same paw on the ball.
    ap=pose(2<=t<10.15 or 12<=t<14,15<=t<21)
    cp=pose(3<=t<6.15 or 10.5<=t<14,t<2.3 or t>=15)
    # Three authored in-between poses: unfold before locomotion, settle after.
    def transition(pose, events):
        for start, family, reverse in events:
            if start <= t < start+.3:
                frame=min(2,int((t-start)/.1))
                return family+str(3-frame if reverse else frame+1)
        return pose
    ap=transition(ap,[(1.7,'stand',False),(10.15,'stand',True),
        (11.7,'stand',False),(14,'stand',True),(14.7,'curl',False),(21,'curl',True)])
    cp=transition(cp,[(2.3,'curl',True),(2.7,'stand',False),
        (6.15,'stand',True),(10.2,'stand',False),(14,'stand',True),(14.7,'curl',False)])
    af=1 if 12<=t<21 else -1
    cf=-1 if 10.5<=t<14 else 1
    return dict(ax=ax,ay=ay,cx=cx,cy=GROUND,ap=ap,cp=cp,af=af,cf=cf,bx=bx,by=by)


def frames(name, values, discrete=False):
    # Keep identical states only at the boundaries of each constant interval.
    keys=[]
    for i, value in enumerate(values):
        if i in (0,len(values)-1) or value!=values[i-1] or value!=values[i+1]:
            keys.append(f'{i/(len(values)-1)*100:.5f}%{{{value}}}')
    return f'.{name}{{animation:{name} {DURATION}s {"steps(1,end)" if discrete else "linear"} infinite}}@keyframes {name}{{'+''.join(keys)+'}'


def sprite(color, pose):
    data=base64.b64encode((ROOT/'assets'/f'play-{color}-{pose}.png').read_bytes()).decode()
    width=192 if pose=='run' else 64
    return f'<svg x="-32" y="-48" width="64" height="48" viewBox="0 0 64 48" overflow="hidden"><image class="{"stride" if pose=="run" else ""}" width="{width}" height="48" href="data:image/png;base64,{data}"/></svg>'


def render():
    times=[i/FPS for i in range(DURATION*FPS+1)]
    states=[state(t) for t in times]
    css=['''
:root{--floor:#d8d2c4;--blue:#68b4cd;--pink:#d68bab}
@media(prefers-color-scheme:dark){:root{--floor:#454640;--blue:#89d2e6;--pink:#e7a7cc}}
image{image-rendering:pixelated}.stride{animation:stride .36s steps(1,end) infinite}
@keyframes stride{0%{transform:translateX(0)}33.333%{transform:translateX(-64px)}66.667%{transform:translateX(-128px)}}
.portal{transform-box:fill-box;transform-origin:center;animation:portal 24s linear infinite}
@keyframes portal{0%,20%,31%,100%{opacity:0;transform:scale(.1,.05)}22%,29%{opacity:1;transform:scale(1)}}
.orange-gate{animation:gate 24s steps(1,end) infinite}
@keyframes gate{0%{clip-path:url(#entry-clip)}26.66667%{clip-path:url(#exit-clip)}100%{clip-path:url(#entry-clip)}}
''']
    cats=[]
    for prefix,color in [('a','ginger'),('c','slate')]:
        css.append(frames(prefix+'-move',[f'transform:translate({s[prefix+"x"]:.3f}px,{s[prefix+"y"]:.3f}px)' for s in states]))
        css.append(frames(prefix+'-face',[f'transform:scaleX({s[prefix+"f"]})' for s in states],True))
        poses=[]
        for pose in ['run','sit','sleep','stand1','stand2','stand3','curl1','curl2','curl3']:
            name=prefix+'-'+pose
            css.append(frames(name,[f'opacity:{int(s[prefix+"p"]==pose)}' for s in states],True))
            poses.append(f'<g class="{name} pose">{sprite(color,pose)}</g>')
        cats.append(f'<g class="{prefix}-move cat"><g class="{prefix}-face">'+''.join(poses)+'</g></g>')
    css.append(frames('ball-move',[f'transform:translate({s["bx"]:.3f}px,{s["by"]:.3f}px)' for s in states]))
    css.append(frames('ball-spin',[f'transform:rotate({(s["bx"]-286)/8*180/pi:.3f}deg)' for s in states]))
    css.append(frames('ball-shadow',[f'transform:translate({s["bx"]:.3f}px,151px) scale({1-(142-s["by"])/100:.3f},1);opacity:{.15-(142-s["by"])/400:.3f}' for s in states]))
    css.append('''@media(prefers-reduced-motion:reduce){
+*{animation:none!important}.portal{display:none}.orange-gate{clip-path:none}
+.a-move{transform:translate(150px,150px)}.c-move{transform:translate(680px,150px)}.a-face{transform:scaleX(-1)}
+.pose{opacity:0}.a-sit,.c-sleep{opacity:1}.ball-move{transform:translate(286px,142px)}.ball-shadow{transform:translate(286px,151px);opacity:.15}
+}'''.replace('+',''))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="860" height="200" viewBox="0 0 860 200" role="img" aria-labelledby="title desc">
<title id="title">Ginger and slate: a little game of fetch</title>
<desc id="desc">A ginger cat nudges a ball toward a sleepy blue-grey cat, who wakes and bats it back. Ginger takes a portal shortcut to catch it. Both return to their spots and nap. All poses share a consistent head scale and ground line.</desc>
<style>{''.join(css)}</style>
<defs><clipPath id="entry-clip"><rect x="0" y="0" width="500" height="200"/></clipPath><clipPath id="exit-clip"><rect x="100" y="0" width="760" height="200"/></clipPath></defs>
<path d="M55 151H805" stroke="var(--floor)" stroke-linecap="round"/>
<g class="portal" fill="none" stroke="var(--pink)"><ellipse cx="100" cy="125" rx="10" ry="27" stroke-width="6" opacity=".15"/><ellipse cx="100" cy="125" rx="6" ry="26" stroke-width="2"/></g>
<g class="portal" fill="none" stroke="var(--blue)"><ellipse cx="500" cy="125" rx="10" ry="27" stroke-width="6" opacity=".15"/><ellipse cx="500" cy="125" rx="6" ry="26" stroke-width="2"/></g>
<ellipse class="ball-shadow" rx="8" ry="1.5" fill="#554b42"/>
<g class="ball-move"><g class="ball-spin"><circle r="8" fill="#e8b66f" stroke="#a97943"/><path d="M-7-3Q0 3 7-3M-5 6Q1-2 5-6" fill="none" stroke="#fff0cf" stroke-width="1.5"/></g></g>
<g class="orange-gate">{cats[0]}</g>{cats[1]}
</svg>'''


if __name__=='__main__':
    output=ROOT/'assets/cat-playground.svg'
    output.write_text(render())
    print(f'Generated {output} ({output.stat().st_size:,} bytes)')
