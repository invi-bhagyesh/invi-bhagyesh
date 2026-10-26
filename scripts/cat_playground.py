#!/usr/bin/env python3
"""Build a self-contained pixel-cat playground for the profile README."""
import base64
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def image(name, width, height, extra=''):
    data = base64.b64encode((ROOT / 'assets' / name).read_bytes()).decode()
    return f'<image width="{width}" height="{height}" href="data:image/png;base64,{data}" {extra}/>'


def cat(name):
    walk = image('cat-walk-left.png', 162, 43, 'class="walk-sheet"')
    rest = image('cat-awake.png', 57, 46)
    return f'''<g class="cat {name}"><g class="facing">
      <g class="running"><svg x="-27" y="-43" width="54" height="43" viewBox="0 0 54 43" overflow="hidden">{walk}</svg></g>
      <g class="resting" transform="translate(-28 -46)">{rest}</g>
    </g></g>'''


def render():
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="860" height="200" viewBox="0 0 860 200" role="img" aria-labelledby="title desc">
<title id="title">A little cat playground</title>
<desc id="desc">Two orange pixel cats chase and bat a bouncing ball. One leaps into a blue portal and reappears through a pink portal. They pause between games. No contribution data is displayed.</desc>
<style>
:root{{--floor:#d8d2c4;--muted:#897c68;--blue:#79b9cc;--pink:#ce92b7}}
@media(prefers-color-scheme:dark){{:root{{--floor:#454640;--muted:#aaa18c;--blue:#89d2e6;--pink:#e7a7cc}}}}
image{{image-rendering:pixelated}}
.cat,.ball-travel,.ball-hop,.ball-spin,.portal,.facing,.running,.resting{{animation-duration:20s;animation-iteration-count:infinite}}
.cat{{animation-timing-function:cubic-bezier(.4,0,.2,1)}}
.first{{animation-name:first}}.second{{animation-name:second}}
.walk-sheet{{animation:gait .36s steps(1,end) infinite}}
@keyframes gait{{0%{{transform:translateX(0)}}33.333%{{transform:translateX(-54px)}}66.667%{{transform:translateX(-108px)}}}}
@keyframes first{{
0%,8%{{transform:translate(120px,150px);opacity:1}}
22%{{transform:translate(260px,150px)}}
40%{{transform:translate(450px,150px)}}
46%{{transform:translate(595px,102px);opacity:1}}
49%{{transform:translate(620px,143px);opacity:0}}
51%{{transform:translate(100px,143px);opacity:0}}
54%{{transform:translate(125px,130px);opacity:1}}
58%{{transform:translate(160px,150px)}}
68%,76%{{transform:translate(235px,150px)}}
93%,100%{{transform:translate(120px,150px);opacity:1}}
}}
@keyframes second{{
0%,24%{{transform:translate(720px,150px)}}
36%{{transform:translate(590px,150px)}}
41%{{transform:translate(560px,137px)}}
45%,53%{{transform:translate(545px,150px)}}
64%{{transform:translate(620px,150px)}}
80%,100%{{transform:translate(720px,150px)}}
}}
.first .facing{{animation-name:face-first;animation-timing-function:steps(1,end)}}
.second .facing{{animation-name:face-second;animation-timing-function:steps(1,end)}}
@keyframes face-first{{0%{{transform:scaleX(-1)}}76%{{transform:scaleX(1)}}100%{{transform:scaleX(-1)}}}}
@keyframes face-second{{0%{{transform:scaleX(1)}}53%{{transform:scaleX(-1)}}80%,100%{{transform:scaleX(1)}}}}
.first .running{{animation-name:run-first;animation-timing-function:steps(1,end)}}
.first .resting{{animation-name:rest-first;animation-timing-function:steps(1,end)}}
.second .running{{animation-name:run-second;animation-timing-function:steps(1,end)}}
.second .resting{{animation-name:rest-second;animation-timing-function:steps(1,end)}}
@keyframes run-first{{0%{{opacity:0}}8%{{opacity:1}}68%{{opacity:0}}76%{{opacity:1}}93%,100%{{opacity:0}}}}
@keyframes rest-first{{0%{{opacity:1}}8%{{opacity:0}}68%{{opacity:1}}76%{{opacity:0}}93%,100%{{opacity:1}}}}
@keyframes run-second{{0%{{opacity:0}}24%{{opacity:1}}45%{{opacity:0}}53%{{opacity:1}}80%,100%{{opacity:0}}}}
@keyframes rest-second{{0%{{opacity:1}}24%{{opacity:0}}45%{{opacity:1}}53%{{opacity:0}}80%,100%{{opacity:1}}}}
.ball-travel{{animation-name:ball-travel;animation-timing-function:linear}}
@keyframes ball-travel{{0%,22%{{transform:translateX(290px)}}41%{{transform:translateX(530px)}}68%{{transform:translateX(270px)}}76%{{transform:translateX(290px)}}100%{{transform:translateX(290px)}}}}
.ball-hop{{animation-name:ball-hop;animation-timing-function:ease-out}}
@keyframes ball-hop{{0%,22%{{transform:translateY(142px)}}26%{{transform:translateY(119px)}}30%{{transform:translateY(142px)}}33%{{transform:translateY(130px)}}36%,41%{{transform:translateY(142px)}}46%{{transform:translateY(110px)}}51%{{transform:translateY(142px)}}55%{{transform:translateY(125px)}}59%{{transform:translateY(142px)}}62%{{transform:translateY(135px)}}65%,100%{{transform:translateY(142px)}}}}
.ball-spin{{animation-name:ball-spin;animation-timing-function:linear}}
@keyframes ball-spin{{0%,22%{{transform:rotate(0deg)}}41%{{transform:rotate(900deg)}}68%{{transform:rotate(-60deg)}}76%,100%{{transform:rotate(0deg)}}}}
.portal{{animation-name:portal;transform-box:fill-box;transform-origin:center}}
@keyframes portal{{0%,37%,64%,100%{{opacity:0;transform:scale(.2,.05)}}42%,58%{{opacity:1;transform:scale(1)}}}}
@media(prefers-reduced-motion:reduce){{
.cat,.ball-travel,.ball-hop,.ball-spin,.portal,.facing,.running,.resting,.walk-sheet{{animation:none!important}}
.first{{transform:translate(120px,150px)}}.second{{transform:translate(720px,150px)}}
.running,.portal{{display:none}}.resting{{opacity:1}}.first .facing{{transform:scaleX(-1)}}
.ball-travel{{transform:translateX(290px)}}.ball-hop{{transform:translateY(142px)}}
}}
</style>
<path d="M55 152H805" stroke="var(--floor)" stroke-width="1" stroke-linecap="round"/>
<g class="portal" fill="none" stroke="var(--pink)"><ellipse cx="100" cy="126" rx="11" ry="29" stroke-width="5" opacity=".18"/><ellipse cx="100" cy="126" rx="7" ry="26" stroke-width="2"/></g>
<g class="portal" fill="none" stroke="var(--blue)"><ellipse cx="620" cy="126" rx="11" ry="29" stroke-width="5" opacity=".18"/><ellipse cx="620" cy="126" rx="7" ry="26" stroke-width="2"/></g>
<g class="ball-travel"><g class="ball-hop"><g class="ball-spin">
<circle r="8" fill="#dfaf68" stroke="#a97943" stroke-width="1"/>
<path d="M-7-3Q0 3 7-3M-5 6Q1-2 5-6" fill="none" stroke="#fff0cf" stroke-width="1.5"/>
</g></g></g>
{cat('first')}{cat('second')}
</svg>'''


if __name__ == '__main__':
    output = ROOT / 'assets/cat-playground.svg'
    output.write_text(render())
    print(f'Generated {output}')
