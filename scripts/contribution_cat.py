#!/usr/bin/env python3
"""Generate a self-contained running-cat SVG from a public GitHub calendar."""
import argparse
import base64
from math import pi, sin, cos, hypot
from datetime import date, timedelta
from html import escape
from html.parser import HTMLParser
from pathlib import Path
import re
from urllib.request import Request, urlopen


class Calendar(HTMLParser):
    def __init__(self):
        super().__init__()
        self.days = {}

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'td' and 'data-date' in attrs and 'data-level' in attrs:
            day = date.fromisoformat(attrs['data-date'])
            level = int(attrs['data-level'])
            if not 0 <= level <= 4:
                raise ValueError('Unexpected contribution level')
            self.days[day] = level


def render(days, username):
    if len(days) < 300:
        raise ValueError('Incomplete contribution calendar; keeping the previous SVG')
    start = min(days)
    start -= timedelta(days=(start.weekday() + 1) % 7)
    columns = (max(days) - start).days // 7 + 1
    pitch, left, top = 14, 60, 88
    width = columns * pitch + 120
    # A rounded perimeter keeps the full 54x43 sprite clear of every square.
    x0, x1, y0, y1, radius = 28, width - 28, 44, 224, 14
    route = [(x0 + radius, y0), (x1 - radius, y0)]
    for cx, cy, start_angle, endpoint in [
        (x1-radius, y0+radius, -pi/2, (x1, y1-radius)),
        (x1-radius, y1-radius, 0, (x0+radius, y1)),
        (x0+radius, y1-radius, pi/2, (x0, y0+radius)),
        (x0+radius, y0+radius, pi, (x0+radius, y0)),
    ]:
        for step in range(1, 13):
            angle = start_angle + step*pi/24
            route.append((cx + radius*cos(angle), cy + radius*sin(angle)))
        route.append(endpoint)
    distances = [0.0]
    for previous, point in zip(route, route[1:]):
        distances.append(distances[-1] + hypot(point[0]-previous[0], point[1]-previous[1]))
    total = distances[-1]
    css = ['''
:root{--empty:#eeeae2;--l1:#d6ddbd;--l2:#acbf8b;--l3:#789964;--l4:#42684b;--ink:#443c38;--muted:#80766c}
@media(prefers-color-scheme:dark){:root{--empty:#292e30;--l1:#354d3e;--l2:#4e7654;--l3:#79a568;--l4:#b2d392;--ink:#e6dfd3;--muted:#a99f91}}
.cell{fill:var(--empty)}.l1{fill:var(--l1)}.l2{fill:var(--l2)}.l3{fill:var(--l3)}.l4{fill:var(--l4)}
.runner{animation:route 24s linear infinite}.facing{animation:facing 24s steps(1,end) infinite}
.sprite-sheet{image-rendering:pixelated;animation:gait .36s steps(1,end) infinite}
@keyframes gait{0%{transform:translateX(0)}33.333%{transform:translateX(-54px)}66.667%{transform:translateX(-108px)}}
''']
    css.append('@keyframes route{' + ''.join(
        f'{distance/total*100:.5f}%{{transform:translate({x:.3f}px,{y:.3f}px)}}'
        for (x,y), distance in zip(route, distances)) + '}')
    # The source sprite faces left; flip on the top/right half of the lap.
    css.append('@keyframes facing{0%{transform:scaleX(-1)}50%{transform:scaleX(1)}100%{transform:scaleX(-1)}}')
    css.append('@media(prefers-reduced-motion:reduce){.runner,.facing,.sprite-sheet{animation:none!important}.runner{display:none}}')
    cells = []
    for day, level in sorted(days.items()):
        col, row = divmod((day-start).days, 7)
        cells.append(f'<rect class="cell l{level}" x="{left+col*pitch}" y="{top+row*pitch}" width="10" height="10" rx="2"><title>{day}: contribution level {level} of 4</title></rect>')
    sprite_path = Path(__file__).resolve().parent.parent / 'assets/cat-walk-left.png'
    sprite_data = base64.b64encode(sprite_path.read_bytes()).decode('ascii')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="280" viewBox="0 0 {width} 280" role="img" aria-labelledby="title desc">
<title id="title">{escape(username)}'s contribution cat</title>
<desc id="desc">The orange pixel cat runs around the contribution calendar, avoiding the squares and leaving every contribution intact. {min(days)} through {max(days)}.</desc>
<style>{''.join(css)}</style>
<text x="60" y="16" fill="var(--ink)" font-family="monospace" font-size="11">a year of little steps</text>
{''.join(cells)}
<g class="runner"><g class="facing">
<svg x="-27" y="-21.5" width="54" height="43" viewBox="0 0 54 43" overflow="hidden">
<image class="sprite-sheet" width="162" height="43" href="data:image/png;base64,{sprite_data}"/>
</svg></g></g>
<text x="60" y="270" fill="var(--muted)" font-family="monospace" font-size="9">@{escape(username)} · {min(days)} — {max(days)}</text>
</svg>'''


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--user', default='invi-bhagyesh')
    parser.add_argument('--output', type=Path, default=Path('assets/contribution-cat.svg'))
    parser.add_argument('--input', type=Path, help='Saved GitHub calendar HTML for offline generation')
    args = parser.parse_args()
    if not re.fullmatch(r'[A-Za-z0-9-]{1,39}', args.user):
        parser.error('Invalid GitHub username')
    if args.input:
        html = args.input.read_text()
    else:
        request = Request(f'https://github.com/users/{args.user}/contributions', headers={'User-Agent': 'contribution-cat'})
        with urlopen(request, timeout=30) as response:
            html = response.read().decode()
    calendar = Calendar()
    calendar.feed(html)
    svg = render(calendar.days, args.user)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    temporary = args.output.with_suffix('.tmp')
    temporary.write_text(svg)
    temporary.replace(args.output)
    print(f'Generated {args.output} from {len(calendar.days)} contribution days')


if __name__ == '__main__':
    main()
