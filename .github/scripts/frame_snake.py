"""Wrap the raw Platane/snk SVG in a premium glass frame (Awwwards / Figma style).

usage: python3 frame_snake.py <input.svg> <output.svg>
"""
import re
import sys

src, dst = sys.argv[1], sys.argv[2]
raw = open(src, encoding="utf-8").read()

m = re.search(r"<svg[^>]*>", raw)
tag = m.group(0)
inner = raw[m.end(): raw.rindex("</svg>")]
vb = re.search(r'viewBox="([^"]+)"', tag).group(1).replace(",", " ").split()
vx, vy, vw, vh = [float(v) for v in vb]

C, V, P = "#00F7FF", "#A78BFA", "#FF4D9D"
BASE, TXT, MUT, BLUE = "#070a14", "#e6edf3", "#8b98a8", "#0d99ff"
MONO = "Consolas, Menlo, Courier New, monospace"
DOTS = ["#151b2e", "#0b4f63", "#0a8da8", "#00c2dc", "#00f7ff"]

W = 1000
PAD = 40
iw = W - 2 * PAD
ih = round(iw * vh / vw)
TOP = 76
H = TOP + ih + 64
R = 30


def mono(x, y, s, fill=MUT, anchor="start", size=11, ls=2):
    w = len(s) * (size * 0.6 + ls)
    return (f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-family="{MONO}" font-size="{size}" fill="{fill}" '
            f'textLength="{w:.0f}" lengthAdjust="spacing">{s}</text>')


legend = ""
lx = W - PAD - 5 * 16 - 44
for i, c in enumerate(DOTS):
    legend += f'<rect x="{lx + i * 16}" y="30" width="11" height="11" rx="3" fill="{c}" stroke="#fff" stroke-opacity=".15"/>'

orbs = [(120, H - 20, 170, C, .42, 120, -20, 12), (520, H, 190, V, .45, -80, -30, 10), (900, H - 30, 180, P, .42, -120, -10, 13), (500, -30, 140, V, .18, 60, 20, 14)]
orb_svg = "".join(
    f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{col}" opacity="{op}"><animateTransform attributeName="transform" type="translate" values="0 0;{dx} {dy};0 0" dur="{dur}s" repeatCount="indefinite"/></circle>'
    for (cx, cy, r, col, op, dx, dy, dur) in orbs)
grid = "".join(f'<line x1="{PAD + i * (iw / 12):.1f}" y1="0" x2="{PAD + i * (iw / 12):.1f}" y2="{H}" stroke="#fff" stroke-opacity=".04"/>' for i in range(13))

out = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Contribution snake">
<defs>
<filter id="fz-bl" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="46"/></filter>
<filter id="fz-nz" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency=".85" numOctaves="2" stitchTiles="stitch"/><feColorMatrix values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 .9 0"/></filter>
<clipPath id="fz-rc"><rect width="{W}" height="{H}" rx="{R}"/></clipPath>
<linearGradient id="fz-gf" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".15"/><stop offset="1" stop-color="#fff" stop-opacity=".03"/></linearGradient>
<linearGradient id="fz-gs" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".5"/><stop offset=".45" stop-color="#fff" stop-opacity=".07"/><stop offset="1" stop-color="#fff" stop-opacity=".25"/></linearGradient>
<linearGradient id="fz-sh" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".12"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
<clipPath id="fz-pc"><rect x="20" y="62" width="{W-40}" height="{ih+24}" rx="22"/></clipPath>
</defs>
<g clip-path="url(#fz-rc)"><rect width="{W}" height="{H}" fill="{BASE}"/><g filter="url(#fz-bl)">{orb_svg}</g>
<rect width="{W}" height="{H}" filter="url(#fz-nz)" opacity=".07"/>{grid}</g>
<path d="M18 24h12M24 18v12M{W-30} 24h12M{W-24} 18v12" stroke="#fff" stroke-opacity=".35" fill="none"/>
{mono(PAD + 18, 40, "CONTRIBUTION SNAKE", C)}
<circle cx="{PAD + 4}" cy="36" r="3.5" fill="{P}"><animate attributeName="opacity" values="1;.25;1" dur="1.6s" repeatCount="indefinite"/></circle>
{mono(lx - 14, 40, "LESS", MUT, "end")}{legend}{mono(W - PAD, 40, "MORE", MUT, "end")}
<line x1="{PAD}" y1="54" x2="{W-PAD}" y2="54" stroke="#fff" stroke-opacity=".14"/>
<rect x="20" y="62" width="{W-40}" height="{ih+24}" rx="22" fill="url(#fz-gf)" stroke="url(#fz-gs)" stroke-width="1.2"/>
<path d="M42 63.6H{W-42}" stroke="#fff" stroke-opacity=".30" stroke-linecap="round"/>
<g clip-path="url(#fz-pc)"><rect x="-200" y="50" width="140" height="{ih+60}" fill="url(#fz-sh)" transform="skewX(-20)"><animate attributeName="x" values="-200;{W+120};{W+120}" keyTimes="0;.45;1" dur="9s" repeatCount="indefinite"/></rect></g>
<svg x="{PAD}" y="{TOP}" width="{iw}" height="{ih}" viewBox="{vx} {vy} {vw} {vh}" overflow="hidden">{inner}</svg>
<line x1="{PAD}" y1="{H-46}" x2="{W-PAD}" y2="{H-46}" stroke="#fff" stroke-opacity=".14"/>
{mono(PAD, H-22, "EATING COMMITS  /  UPDATES EVERY 12 HOURS")}
{mono(W-PAD, H-22, "DANU'ZZ  /  GITHUB.COM/DNUZI", TXT, "end")}
<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="{R}" fill="none" stroke="#fff" stroke-opacity=".10"/>
</svg>
'''
open(dst, "w", encoding="utf-8").write(out)
print(f"framed {src} -> {dst} ({W}x{H})")
