import json
import os
from xml.sax.saxutils import escape

art = open("ascii-art.txt", encoding="utf-8").read().splitlines()
stats = json.load(open("stats.json")) if os.path.exists("stats.json") else {}

FS, CW, LH = 7, 4.2, 8.4
PFS, PCW, PLH, PW = 16, 8.8, 20, 50
W = 1100
aw = max(map(len, art)) * CW
px = int(15 + aw + 35)
H = int(len(art) * LH + 40)

themes = {
    "dark_mode.svg": dict(bg="#161b22", fg="#c9d1d9", key="#ffa657", val="#a5d6ff", cc="#616e7f", add="#3fb950", dele="#f85149", ac="#22d3ee", hi="#a5f3fc", lo="#164e63"),
    "light_mode.svg": dict(bg="#f6f8fa", fg="#24292f", key="#953800", val="#0a3069", cc="#c2cfde", add="#1a7f37", dele="#cf222e", ac="#0e7490", hi="#0e7490", lo="#a8b3bd"),
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
            y += PLH
            continue
        if r[0] == "head":
            title = r[1]
            line = f'<tspan fill="{t["fg"]}">{escape(title)}</tspan><tspan fill="{t["cc"]}"> {"-" * (PW - len(title) - 1)}</tspan>'
        else:
            if r[0] == "loc" or r[1] == "Lines of Code":
                a, d, l = n("add"), n("del"), n("loc")
                k = "Lines of Code:"
                plain = f"{l} ({a}++, {d}--)"
                v = (
                    f'<tspan fill="{t["val"]}">{l} (</tspan>'
                    f'<tspan fill="{t["add"]}">{a}++</tspan>'
                    f'<tspan fill="{t["val"]}">, </tspan>'
                    f'<tspan fill="{t["dele"]}">{d}--</tspan>'
                    f'<tspan fill="{t["val"]}">)</tspan>'
                )
            else:
                k, plain = r[1] + ":", r[2]
                v = f'<tspan fill="{t["val"]}">{escape(plain)}</tspan>'
            dots = "." * max(2, PW - len(k) - len(plain) - 2)
            line = f'<tspan fill="{t["key"]}">{escape(k)}</tspan><tspan fill="{t["cc"]}"> {dots} </tspan>{v}'
        out.append(f'<text x="{px}" y="{y}" font-size="{PFS}" fill="{t["fg"]}">{line}</text>')
        last = (px + PW * PCW, y)
        y += PLH
    out.append(f'<rect class="c" x="{last[0] + 6:.0f}" y="{last[1] - 11}" width="8" height="14" fill="{t["ac"]}"/>')
    out.append("</svg>")
    open(name, "w", encoding="utf-8").write("".join(out))

for name, t in themes.items():
    build(name, t)