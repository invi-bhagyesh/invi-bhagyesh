#!/usr/bin/env python3
"""Deterministic 24-second playground: shared contact times, ballistic bounces."""
import base64
from math import pi
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DURATION = 24
GROUND = 220
CAT_SCALE = 1.5
BALL_RADIUS = 12
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
    # Paw contacts: Nivi at 4s, Livi at 6s, Nivi again at 10s.
    if t < 4: bx = 286
    elif t < 6:
        u=t-4; bx=286+160*u-9*u*u
    elif t < 10:
        u=t-6; bx=570-130*u+9*u*u
    elif t < 12:
        u=t-10; bx=194+92*u-23*u*u
    else: bx=286
    lift = bounce(t,4,70) if t < 6 else bounce(t,6,90) if t < 10 else bounce(t,10,35)
    by = GROUND-BALL_RADIUS-lift
    # Scaled paw offset is 39 px; contacts include the 12 px ball radius.
    if t < 2: ax=150
    elif t < 4: ax=ease(t,2,4,150,235)
    elif t < 5.2: ax=ease(t,4,5.2,235,400)
    elif t < 6.4: ax=400+(t-5.2)/1.2*152
    elif t < 6.8: ax=48+(t-6.4)/.4*95
    elif t < 9.8: ax=143
    elif t < 12: ax=143
    elif t < 14: ax=ease(t,12,14,143,150)
    else: ax=150
    # Ballistic leap, landing at the portal before running through it.
    u=max(0,min(1,(t-5.2)/.9))
    ay=GROUND-4*34*u*(1-u)
    if 6.4 <= t <= 6.8:
        u=(t-6.4)/.4;ay=GROUND-4*8*u*(1-u)
    if t < 3: cx=680
    elif t < 6: cx=ease(t,3,6,680,621)
    elif t < 10.5: cx=621
    elif t < 14: cx=ease(t,10.5,14,621,680)
    else: cx=680
    def pose(running, sleeping):
        return 'sleep' if sleeping else 'run' if running else 'sit'
    # Brief held walking poses at impacts keep the same paw on the ball.
    ap=pose(2<=t<6.8 or 9.9<=t<10.15 or 12<=t<14,15<=t<21)
    cp=pose(3<=t<6.15 or 10.5<=t<14,t<2.3 or t>=15)
    # Three authored in-between poses: unfold before locomotion, settle after.
    def transition(pose, events):
        for start, family, reverse in events:
            if start <= t < start+.3:
                frame=min(2,int((t-start)/.1))
                return family+str(3-frame if reverse else frame+1)
        return pose
    ap=transition(ap,[(1.7,'stand',False),(6.8,'stand',True),(9.6,'stand',False),(10.15,'stand',True),
        (11.7,'stand',False),(14,'stand',True),(14.7,'curl',False),(21,'curl',True)])
    cp=transition(cp,[(2.3,'curl',True),(2.7,'stand',False),
        (6.15,'stand',True),(10.2,'stand',False),(14,'stand',True),(14.7,'curl',False)])
    af=-1
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


def environment():
    """Original platformer scenery, kept behind the playable ground plane."""
    bricks = ''.join(
        f'<path d="M{x} {y}v24"/>'
        for y, offset in [(232, 0), (256, 24)] for x in range(offset, 861, 48)
    )
    tufts = ''.join(
        f'<path d="M{x} 220v-6h4v3h4v-7h4v10Z"/>'
        for x in [24, 65, 330, 360, 755, 810]
    )
    blocks = []
    for x,y,paw in [(294,76,False),(326,76,True),(358,76,False),(690,66,True),(722,66,False)]:
        blocks.append(f'<rect x="{x}" y="{y}" width="30" height="28" rx="1" fill="var(--block)" stroke="var(--floor)" stroke-width="2"/>')
        blocks.append(f'<path d="M{x+3} {y+24}V{y+3}h24" fill="none" stroke="#fff0cd" opacity=".5" stroke-width="2"/>')
        if paw:
            blocks.append(f'<path d="M{x+11} {y+15}h9v7h-9ZM{x+7} {y+8}h4v5h-4ZM{x+14} {y+5}h4v5h-4ZM{x+21} {y+8}h4v5h-4Z" fill="var(--floor)"/>')
    return f'''<g aria-hidden="true" shape-rendering="crispEdges">
<rect width="860" height="280" rx="12" fill="var(--sky)"/>
<g fill="var(--cloud)">
<path d="M45 45h12V33h20V25h28v8h20v12h13v13H45Z"/>
<path d="M450 34h16V22h24V16h24v6h20v12h16v14H450Z"/>
<path d="M762 39h10V29h18v-8h24v8h14v10h14v12h-80Z"/>
</g>
<path d="M0 220v-54h18v-24h24v-24h30v-12h32v12h30v24h24v24h18v54ZM410 220v-40h22v-24h22v-28h30v-16h30v16h30v28h22v24h22v40Z" fill="var(--hill)"/>
<path d="M170 220v-22h18v-18h26v-14h32v14h26v18h18v22ZM610 220v-24h18v-18h22v-16h30v16h26v18h22v24Z" fill="var(--hill-front)"/>
{''.join(blocks)}
<rect y="220" width="860" height="60" fill="var(--soil)"/>
<path d="M0 232H860M0 256H860" stroke="var(--mortar)" stroke-width="2"/>
<g stroke="var(--mortar)" stroke-width="2">{bricks}</g>
<path d="M0 220H860v8H0Z" fill="var(--grass)"/>
<path d="M0 220H860" stroke="var(--floor)"/>
<g fill="var(--grass)">{tufts}</g>
</g>'''


def render():
    times=[i/FPS for i in range(DURATION*FPS+1)]
    states=[state(t) for t in times]
    css=['''
:root{--speech-ink:#493b30;--floor:#9d7655;--blue:#77a785;--pink:#b57b92;--sky:#faf0dc;--cloud:#fffaf0;--hill:#d5ddbb;--hill-front:#bbcda1;--grass:#88a871;--soil:#c3926c;--mortar:#ad7e5d;--block:#dcb775}
@media(prefers-color-scheme:dark){:root{--speech-ink:#f2e8d4;--floor:#715f4d;--blue:#9cc9a4;--pink:#dba5bd;--sky:#272c30;--cloud:#41484a;--hill:#39473e;--hill-front:#465a43;--grass:#698a5a;--soil:#785b47;--mortar:#5c4639;--block:#a08050}}
image{image-rendering:pixelated}
.portal{transform-box:fill-box;transform-origin:center;animation:portal 24s linear infinite}
@keyframes portal{0%,20%,31%,100%{opacity:0;transform:scale(.1,.05)}22%,29%{opacity:1;transform:scale(1)}}
.orange-gate{animation:gate 24s steps(1,end) infinite}
@keyframes gate{0%{clip-path:url(#entry-clip)}26.66667%{clip-path:url(#exit-clip)}100%{clip-path:url(#entry-clip)}}
''']
    cats=[]
    for prefix,color in [('a','nivi'),('c','livi')]:
        css.append(frames(prefix+'-move',[f'transform:translate({s[prefix+"x"]:.0f}px,{s[prefix+"y"]:.0f}px)' for s in states]))
        css.append(frames(prefix+'-face',[f'transform:scaleX({s[prefix+"f"]})' for s in states],True))
        # Advance the feet by actual distance, not wall-clock time. Teleport
        # jumps and airborne movement cannot generate extra steps.
        distance=0.0
        gait=[]
        for i, current in enumerate(states):
            if i:
                previous=states[i-1]
                dx=abs(current[prefix+'x']-previous[prefix+'x'])
                grounded=current[prefix+'y']>=GROUND-.05 and previous[prefix+'y']>=GROUND-.05
                if dx<12 and grounded and current[prefix+'p']=='run':
                    distance+=dx
            stride_length=30 if prefix=='a' else 43
            frame=int(distance/stride_length*3)%3
            gait.append(f'transform:translateX({-64*frame}px)')
        gait_css=frames(prefix+'-stride',gait,True)
        css.append(gait_css.replace('.'+prefix+'-stride{','.'+prefix+'-move .stride{'))
        poses=[]
        for pose in ['run','sit','sleep','stand1','stand2','stand3','curl1','curl2','curl3']:
            name=prefix+'-'+pose
            css.append(frames(name,[f'opacity:{int(s[prefix+"p"]==pose)}' for s in states],True))
            poses.append(f'<g class="{name} pose"><g transform="scale({CAT_SCALE})">{sprite(color,pose)}</g></g>')
        cats.append(f'<g class="{prefix}-move cat"><g class="{prefix}-face">'+''.join(poses)+'</g></g>')
    css.append(frames('ball-move',[f'transform:translate({s["bx"]:.3f}px,{s["by"]:.3f}px)' for s in states]))
    css.append(frames('ball-spin',[f'transform:rotate({(s["bx"]-286)/BALL_RADIUS*180/pi:.3f}deg)' for s in states]))
    css.append(frames('ball-shadow',[f'transform:translate({s["bx"]:.3f}px,221px) scale({1-(208-s["by"])/100:.3f},1);opacity:{.15-(208-s["by"])/400:.3f}' for s in states]))
    dialogue=[
        ('a',0.15,2.25,'Play with me?'),
        ('c',2.35,4.0,'One round.'),
        ('a',4.1,5.2,'Heads up!'),
        ('c',6.85,9.5,'Portals? Really?'),
        ('a',9.6,12.0,'Work smarter.'),
        ('c',12.15,14.7,'Nap harder.'),
        ('a',21.3,23.9,'Rematch?'),
    ]
    bubbles=[]
    for number,(speaker,start,end,line) in enumerate(dialogue):
        name=f'speech-{number}'
        css.append(frames(name,[f'opacity:{int(start<=t<end)};visibility:{"visible" if start<=t<end else "hidden"}' for t in times],True))
        css.append(frames(name+'-position',[f'transform:translate({max(115,min(745,s[speaker+"x"])):.3f}px,{s[speaker+"y"]-104:.3f}px)' for s in states]))
        width=max(146,len(line)*9+28)
        label='NIVI' if speaker=='a' else 'LIVI'
        bubbles.append(f'<g class="{name} speech"><g class="{name}-position"><path d="M-8 0l8 10 8-10" fill="var(--cloud)" stroke="var(--floor)"/><rect x="{-width/2}" y="-48" width="{width}" height="50" rx="7" fill="var(--cloud)" stroke="var(--floor)"/><text y="-32" text-anchor="middle" font-family="monospace" font-size="9" fill="var(--floor)">{label}</text><text y="-12" text-anchor="middle" font-family="monospace" font-size="16" fill="var(--speech-ink)">{line}</text></g></g>')
    css.append('''@media(prefers-reduced-motion:reduce){
+*{animation:none!important}.portal,.speech{display:none}.orange-gate{clip-path:none}
+.a-move{transform:translate(150px,220px)}.c-move{transform:translate(680px,220px)}.a-face{transform:scaleX(-1)}
+.pose{opacity:0}.a-sit,.c-sleep{opacity:1}.ball-move{transform:translate(286px,208px)}.ball-shadow{transform:translate(286px,221px);opacity:.15}
+}'''.replace('+',''))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="860" height="280" viewBox="0 0 860 280" role="img" aria-labelledby="title desc">
<title id="title">Nivi and Livi: a little pixel playground</title>
<desc id="desc">Nivi, a ginger cat, nudges a ball toward Livi, a sleepy white cat, who wakes and bats it back. Nivi takes a portal shortcut to catch it. Nivi asks, Play with me? Livi agrees, One round. After the portal shortcut, Livi asks, Portals? Really? Nivi replies, Work smarter. Livi says, Nap harder. Nivi later asks for a rematch. All poses share a consistent head scale and ground line.</desc>
<style>{''.join(css)}</style>
<defs><clipPath id="entry-clip"><rect x="0" y="0" width="500" height="280"/></clipPath><clipPath id="exit-clip"><rect x="100" y="0" width="760" height="280"/></clipPath></defs>
{environment()}
<g class="portal" fill="none" stroke="var(--pink)"><ellipse cx="100" cy="181" rx="15" ry="40" stroke-width="6" opacity=".15"/><ellipse cx="100" cy="181" rx="9" ry="39" stroke-width="2"/></g>
<g class="portal" fill="none" stroke="var(--blue)"><ellipse cx="500" cy="181" rx="15" ry="40" stroke-width="6" opacity=".15"/><ellipse cx="500" cy="181" rx="9" ry="39" stroke-width="2"/></g>
<ellipse class="ball-shadow" rx="12" ry="1.5" fill="#554b42"/>
<g class="ball-move"><g class="ball-spin"><circle r="12" fill="#8cae82" stroke="#526e50" stroke-width="1.5"/><path d="M-10-5Q0 5 10-5M-7 9Q2-3 7-9" fill="none" stroke="#fff0cf" stroke-width="1.5"/></g></g>
<g class="orange-gate">{cats[0]}</g>{cats[1]}
{''.join(bubbles)}
</svg>'''


if __name__=='__main__':
    output=ROOT/'assets/cat-playground.svg'
    output.write_text(render())
    print(f'Generated {output} ({output.stat().st_size:,} bytes)')
