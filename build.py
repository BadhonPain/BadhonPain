import json
import os
from xml.sax.saxutils import escape

art = open("ascii-art.txt", encoding="utf-8").read().splitlines()
stats = json.load(open("stats.json")) if os.path.exists("stats.json") else {}

FS, CW, LH = 7, 4.2, 8.4
PFS, PCW, PLH, PW = 13, 7.8, 22, 50
W = 985
aw = max(map(len, art)) * CW
px = int(15 + aw + 35)
H = int(len(art) * LH + 40)

themes = {
    "dark_mode.svg": dict(bg="#0d1117", fg="#c9d1d9", ac="#22d3ee", mu="#4b5563", hi="#a5f3fc", lo="#164e63"),
    "light_mode.svg": dict(bg="#f6f8fa", fg="#24292f", ac="#0e7490", mu="#9ca3af", hi="#0e7490", lo="#a8b3bd"),
}

def n(k):
    v = stats.get(k)
    return f"{v:,}" if isinstance(v, int) else "-"

rows = [
    ("head", "badhon@pain"),
    ("kv", "OS", "Windows 11"),
    ("kv", "Focus", "Full-stack, DSA, AL/ML"),
    ("gap",),
    ("kv", "Languages", "C, C++, Java, Python, JS, TS, Rust"),
    ("kv", "Stack", "React, Next.js, Node, MySQL, Express.js"),
    ("gap",),
    ("head", "GitHub Stats"),
    ("kv", "Repos", n("repos")),
    ("kv", "Commits", n("commits")),
    ("kv", "Lines of Code", f'{n("loc")} ({n("add")}++, {n("del")}--)'),
]

def build(name, t):
    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="Consolas,Menlo,monospace">',
        '<style>text{white-space:pre}.l{opacity:0;animation:f .4s forwards}'
        '@keyframes f{to{opacity:1}}.c{animation:b 1s steps(1) infinite}@keyframes b{50%{opacity:0}}</style>',
        f'<defs><radialGradient id="g" gradientUnits="userSpaceOnUse" cx="{15 + aw * .45:.0f}" cy="{H * .42:.0f}" r="{aw * .7:.0f}">'
        f'<stop offset="0" stop-color="{t["hi"]}"/><stop offset=".45" stop-color="{t["ac"]}"/><stop offset="1" stop-color="{t["lo"]}"/></radialGradient></defs>',
        f'<rect width="{W}" height="{H}" rx="14" fill="{t["bg"]}"/>',
    ]
    for i, line in enumerate(art):
        y = 24 + i * LH
        out.append(f'<text class="l" style="animation-delay:{i * .03:.2f}s" x="15" y="{y:.1f}" font-size="{FS}" fill="url(#g)">{escape(line)}</text>')
    y = 38
    last = (px, y)
    for r in rows:
        if r[0] == "gap":
            y += PLH // 2
            continue
        if r[0] == "head":
            title = r[1]
            out.append(
                f'<text x="{px}" y="{y}" font-size="{PFS}"><tspan fill="{t["fg"]}" font-weight="bold">{escape(title)}</tspan>'
                f'<tspan fill="{t["mu"]}"> {"-" * (PW - len(title) - 1)}</tspan></text>'
            )
            last = (px + PW * PCW, y)
        else:
            k, v = r[1], r[2]
            dots = "." * max(2, PW - len(k) - len(v) - 2)
            out.append(
                f'<text x="{px}" y="{y}" font-size="{PFS}"><tspan fill="{t["ac"]}">{escape(k)}</tspan>'
                f'<tspan fill="{t["mu"]}"> {dots} </tspan><tspan fill="{t["fg"]}">{escape(v)}</tspan></text>'
            )
            last = (px + PW * PCW, y)
        y += PLH
    out.append(f'<rect class="c" x="{last[0] + 6:.0f}" y="{last[1] - 11}" width="8" height="14" fill="{t["ac"]}"/>')
    out.append("</svg>")
    open(name, "w", encoding="utf-8").write("".join(out))

for n, t in themes.items():
    build(n, t)