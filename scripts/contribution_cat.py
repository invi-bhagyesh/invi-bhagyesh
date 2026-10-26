#!/usr/bin/env python3
"""Generate a self-contained running-cat SVG from a public GitHub calendar."""
import argparse
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
    pitch, left, top = 14, 28, 50
    width = columns * pitch + 56
    # Sweep alternating rows. The cat reaches every square, including empty ones.
    route = [(col, row) for row in range(7)
             for col in (range(columns) if row % 2 == 0 else reversed(range(columns)))]
    visits = {point: i for i, point in enumerate(route)}
    def percent(i):
        return 3 + 90 * i / (len(route) - 1)
    css = ['''
:root{--empty:#eeeae2;--l1:#d6ddbd;--l2:#acbf8b;--l3:#789964;--l4:#42684b;--ink:#443c38;--muted:#80766c;--fur:#c78658;--stripe:#805137;--eye:#252320}
@media(prefers-color-scheme:dark){:root{--empty:#292e30;--l1:#354d3e;--l2:#4e7654;--l3:#79a568;--l4:#b2d392;--ink:#e6dfd3;--muted:#a99f91;--fur:#dda06d;--stripe:#825639}}
.cell{fill:var(--empty)}.l1{fill:var(--l1)}.l2{fill:var(--l2)}.l3{fill:var(--l3)}.l4{fill:var(--l4)}
.runner{animation:route 42s linear infinite}.facing{animation:facing 42s steps(1,end) infinite}
.body{animation:bob .28s ease-in-out infinite alternate}.leg{transform-box:fill-box;transform-origin:50% 0;animation:stride .28s ease-in-out infinite alternate}.back{animation-delay:-.28s}.tail{transform-origin:-7px -5px;animation:tail .56s ease-in-out infinite alternate}
@keyframes bob{to{transform:translateY(-1.5px)}}@keyframes stride{from{transform:rotate(-32deg)}to{transform:rotate(32deg)}}@keyframes tail{to{transform:rotate(12deg)}}
''']
    def position(point):
        col, row = point
        return f'transform:translate({left + col*pitch + 5}px,{top + row*pitch + 5}px)'
    frames = [f'0%,3%{{{position(route[0])}}}']
    # Only corners need keyframes; movement across each row is linear.
    for i, point in enumerate(route):
        if i % columns in (0, columns-1):
            frames.append(f'{percent(i):.4f}%{{{position(point)}}}')
    frames.append(f'96%,100%{{{position(route[-1])};opacity:0}}')
    frames.append('0%,94%{opacity:1}')
    css.append('@keyframes route{' + ''.join(frames) + '}')
    css.append('@keyframes facing{' + ''.join(
        f'{percent(row*columns):.4f}%{{transform:scaleX({1 if row%2 == 0 else -1})}}'
        for row in range(7)) + '}')
    cells = []
    for day, level in sorted(days.items()):
        col, row = divmod((day-start).days, 7)
        name = f'c{col}_{row}'
        if level:
            hit = percent(visits[col, row])
            css.append(f'.{name}{{animation:{name} 42s linear infinite}}'
                       f'@keyframes {name}{{0%,{hit-.01:.4f}%{{fill:var(--l{level})}}'
                       f'{hit:.4f}%,96%{{fill:var(--empty)}}100%{{fill:var(--l{level})}}}}')
        cells.append(f'<rect class="cell l{level} {name}" x="{left+col*pitch}" y="{top+row*pitch}" width="10" height="10" rx="2"><title>{day}: contribution level {level} of 4</title></rect>')
    css.append('@media(prefers-reduced-motion:reduce){.runner,.facing,.body,.leg,.tail,.cell{animation:none!important}.runner{display:none}}')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="180" viewBox="0 0 {width} 180" role="img" aria-labelledby="title desc">
<title id="title">{escape(username)}'s contribution cat</title>
<desc id="desc">A running ginger cat clears seven rows of GitHub contribution squares, then the calendar refills. {min(days)} through {max(days)}. Dark mode and reduced motion supported.</desc>
<style>{''.join(css)}</style>
<text x="28" y="24" fill="var(--ink)" font-family="monospace" font-size="11">a year of little steps</text>
{''.join(cells)}
<g class="runner"><g class="facing"><g class="body" fill="var(--fur)" stroke="var(--stripe)" stroke-width="1" stroke-linecap="round" stroke-linejoin="round">
<path class="tail" d="M-7-5 Q-18-8-15-17 Q-14-20-12-18" fill="none" stroke="var(--fur)" stroke-width="3"/>
<path class="leg" d="M-6-3 v8 h3" fill="none" stroke-width="3"/>
<path class="leg back" d="M4-3 v8 h3" fill="none" stroke-width="3"/>
<ellipse cx="-2" cy="-6" rx="9" ry="5"/>
<path d="M3-9 L3-18 8-14 13-17 15-9 Q14-3 8-4 Q3-4 3-9Z"/>
<path d="M-6-9 l1 3 M-2-10 l1 3" fill="none"/>
<circle cx="11" cy="-10" r="1" fill="var(--eye)" stroke="none"/>
<path d="M15-7 h2 M14-5 l3 1" fill="none" stroke-width=".7"/>
</g></g></g>
<text x="28" y="170" fill="var(--muted)" font-family="monospace" font-size="9">@{escape(username)} · {min(days)} — {max(days)}</text>
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
