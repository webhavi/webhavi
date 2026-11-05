"""Generates 4 self-contained animated SVGs. No GitHub Action needed.
   python gen_extras.py            -> writes to ./assets
   STATIC=1 python gen_extras.py   -> frozen preview frames (for checking layout)
"""
import math, os, random
random.seed(11)
OUT    = os.environ.get("OUT", "assets")
STATIC = os.environ.get("STATIC") == "1"
FONT   = "'JetBrains Mono','Fira Code',Consolas,monospace"
os.makedirs(OUT, exist_ok=True)

def mix(c1, c2, t):
    a = [int(c1[i:i+2], 16) for i in (1, 3, 5)]
    b = [int(c2[i:i+2], 16) for i in (1, 3, 5)]
    return "#%02x%02x%02x" % tuple(round(a[i] + (b[i]-a[i])*t) for i in range(3))

def save(name, parts):
    open(os.path.join(OUT, name), "w", encoding="utf-8").write("\n".join(parts))
    print("wrote", name)

def A(s):            # keep animation markup out of static previews
    return "" if STATIC else s

# ════════════════════════════════════════════════════════════════════
# 1. SKILL GALAXY  — nodes orbit, shrink + fade behind the core (fake depth)
# ════════════════════════════════════════════════════════════════════
def galaxy():
    W, H, cx, cy = 900, 480, 450, 245
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="{FONT}">',
         '<defs>'
         '<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0a0a18"/><stop offset="1" stop-color="#160c30"/></linearGradient>'
         '<radialGradient id="core"><stop offset="0" stop-color="#ffffff"/><stop offset=".25" stop-color="#e9d5ff"/><stop offset=".6" stop-color="#8b5cf6"/><stop offset="1" stop-color="#4c1d95"/></radialGradient>'
         '<radialGradient id="halo"><stop offset="0" stop-color="#a78bfa" stop-opacity=".55"/><stop offset="1" stop-color="#a78bfa" stop-opacity="0"/></radialGradient>'
         '</defs>',
         f'<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="18" fill="url(#bg)" stroke="#3b2a78" stroke-width="1.5"/>']
    # stars
    for _ in range(80):
        x, y, r = random.uniform(14, W-14), random.uniform(14, H-14), random.uniform(.5, 1.5)
        d = random.uniform(2, 6)
        o.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r:.1f}" fill="#e9ddff" opacity=".5">'
                 + A(f'<animate attributeName="opacity" values=".15;1;.15" dur="{d:.1f}s" begin="-{random.uniform(0,d):.1f}s" repeatCount="indefinite"/>')
                 + '</circle>')
    o.append('<text x="30" y="40" font-size="13" font-weight="700" fill="#bf94ff" letter-spacing="2">// SKILL GALAXY</text>')

    orbits = [
        dict(rx=150, ry=62,  dur=16, dir= 1, col="#22d3ee", nodes=["LLMs", "GenAI", "Vision"]),
        dict(rx=255, ry=100, dur=26, dir=-1, col="#bf94ff", nodes=["PyTorch", "HuggingFace", "TensorFlow", "OpenCV"]),
        dict(rx=360, ry=135, dur=38, dir= 1, col="#f472b6", nodes=["Docker", "MLflow", "FastAPI", "AWS", "SQL"]),
    ]
    for oi, ob in enumerate(orbits):
        rx, ry, dur, dr, col = ob["rx"], ob["ry"], ob["dur"], ob["dir"], ob["col"]
        sweep = 1 if dr == 1 else 0
        path = f"M{cx+rx},{cy} A{rx},{ry} 0 0,{sweep} {cx-rx},{cy} A{rx},{ry} 0 0,{sweep} {cx+rx},{cy}"
        o.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="none" stroke="{col}" stroke-opacity=".28" stroke-dasharray="3 7">'
                 + A(f'<animate attributeName="stroke-dashoffset" from="0" to="{-20 if dr==1 else 20}" dur="3s" repeatCount="indefinite"/>')
                 + '</ellipse>')
        n = len(ob["nodes"])
        for i, name in enumerate(ob["nodes"]):
            frac = (i / n + oi*0.13) % 1
            ts = [k/12 for k in range(13)]
            depth = [(math.sin(2*math.pi*t) if dr == 1 else -math.sin(2*math.pi*t)) for t in ts]
            sc = ";".join(f"{0.85+0.35*d:.3f}" for d in depth)
            op = ";".join(f"{0.72+0.28*d:.3f}" for d in depth)
            kt = ";".join(f"{t:.4f}" for t in ts)
            body = (f'<circle r="13" fill="{col}" opacity=".16"/><circle r="6" fill="{col}"/><circle r="2.2" fill="#fff"/>'
                    f'<text y="26" text-anchor="middle" font-size="12" font-weight="700" fill="#efe6ff">{name}</text>')
            if STATIC:
                ang = 2*math.pi*frac
                x = cx + rx*math.cos(ang); y = cy + (ry*math.sin(ang) if dr == 1 else -ry*math.sin(ang))
                s_ = 0.85 + 0.35*((y-cy)/ry)
                o.append(f'<g transform="translate({x:.1f},{y:.1f}) scale({s_:.2f})">{body}</g>')
            else:
                b = f'-{frac*dur:.2f}s'
                o.append(f'<g><animateMotion dur="{dur}s" begin="{b}" repeatCount="indefinite" path="{path}"/>'
                         f'<g><animateTransform attributeName="transform" type="scale" values="{sc}" keyTimes="{kt}" dur="{dur}s" begin="{b}" repeatCount="indefinite"/>'
                         f'<animate attributeName="opacity" values="{op}" keyTimes="{kt}" dur="{dur}s" begin="{b}" repeatCount="indefinite"/>'
                         f'{body}</g></g>')
    # core
    for b in ("0s", "2s"):
        o.append(f'<circle cx="{cx}" cy="{cy}" r="44" fill="none" stroke="#bf94ff" stroke-width="1.5" opacity="0">'
                 + A(f'<animate attributeName="r" values="44;140" dur="4s" begin="{b}" repeatCount="indefinite"/>'
                     f'<animate attributeName="opacity" values=".6;0" dur="4s" begin="{b}" repeatCount="indefinite"/>') + '</circle>')
    o.append(f'<circle cx="{cx}" cy="{cy}" r="80" fill="url(#halo)"/>')
    o.append(f'<circle cx="{cx}" cy="{cy}" r="40" fill="url(#core)">'
             + A('<animate attributeName="r" values="38;43;38" dur="3s" repeatCount="indefinite"/>') + '</circle>')
    o.append(f'<text x="{cx}" y="{cy+7}" text-anchor="middle" font-size="22" font-weight="800" fill="#2e1065">AI</text>')
    # legend
    lg = [("#22d3ee", "inner · models"), ("#bf94ff", "middle · frameworks"), ("#f472b6", "outer · infra")]
    x = 190
    for col, t in lg:
        o.append(f'<circle cx="{x}" cy="448" r="5" fill="{col}"/><text x="{x+12}" y="452" font-size="12" fill="#9d8fd0">{t}</text>')
        x += 190
    o.append('</svg>')
    save("galaxy.svg", o)

# ════════════════════════════════════════════════════════════════════
# 2. SKILL SKYLINE — isometric 3D towers that grow on load
# ════════════════════════════════════════════════════════════════════
SKILLS = [  # (name, self-rated depth %, colour, gx, gy)   <- EDIT ME (tall ones at back = gy 0)
    ("Python", 95, "#8b5cf6", 0, 0), ("PyTorch", 88, "#8b5cf6", 1, 0), ("LLMs", 85, "#8b5cf6", 2, 0), ("GenAI", 80, "#a78bfa", 3, 0),
    ("FastAPI", 80, "#22d3ee", 0, 1), ("Vision", 78, "#8b5cf6", 1, 1), ("MLOps", 76, "#22d3ee", 2, 1), ("Docker", 75, "#22d3ee", 3, 1),
    ("RAG", 74, "#f472b6", 0, 2), ("Agents", 72, "#f472b6", 1, 2), ("SQL", 70, "#34d399", 2, 2), ("AWS", 66, "#22d3ee", 3, 2),
]
def skyline():
    W, H = 900, 480
    s = 78; exx, exy = s*0.866, s*0.5; eyx, eyy = -s*0.866, s*0.5
    ox, oy = 440, 215; f = 0.62
    P = lambda gx, gy, h=0: (ox + gx*exx + gy*eyx, oy + gx*exy + gy*eyy - h)
    poly = lambda pts: " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="{FONT}">',
         '<defs><linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0a0a18"/><stop offset="1" stop-color="#160c30"/></linearGradient></defs>',
         f'<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="18" fill="url(#bg)" stroke="#3b2a78" stroke-width="1.5"/>',
         '<text x="30" y="40" font-size="13" font-weight="700" fill="#bf94ff" letter-spacing="2">// SKILL SKYLINE · 3D</text>']
    # ground plate + grid
    plate = [P(-.3, -.3), P(4.0, -.3), P(4.0, 3.0), P(-.3, 3.0)]
    o.append(f'<polygon points="{poly(plate)}" fill="#120a2a" stroke="#4c1d95" stroke-width="1.5"/>')
    for i in range(0, 5):
        a, b = P(i, -.3), P(i, 3.0); o.append(f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}" stroke="#2a1a55"/>')
    for j in range(0, 4):
        a, b = P(-.3, j), P(4.0, j); o.append(f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}" stroke="#2a1a55"/>')
    labels = []
    for idx, (name, pct, col, gx, gy) in enumerate(sorted(SKILLS, key=lambda t: t[3]+t[4])):
        h = 14 + pct*0.95; d = idx*0.12
        def faces(hh):
            A_, B_, C_, D_ = P(gx, gy, hh), P(gx+f, gy, hh), P(gx+f, gy+f, hh), P(gx, gy+f, hh)
            A0, B0, C0, D0 = P(gx, gy), P(gx+f, gy), P(gx+f, gy+f), P(gx, gy+f)
            return poly([A_, B_, C_, D_]), poly([D_, C_, C0, D0]), poly([C_, B_, B0, C0])
        top1, left1, right1 = faces(h); top0, left0, right0 = faces(0.01)
        tc, lc, rc = mix(col, "#ffffff", .28), col, mix(col, "#000000", .38)
        spl = 'calcMode="spline" keyTimes="0;1" keySplines=".2 .8 .2 1"'
        def poly_el(f1, f0, fill, extra=""):
            st = f'points="{f1 if STATIC else f0}" fill="{fill}" {extra}'
            an = A(f'<animate attributeName="points" from="{f0}" to="{f1}" dur="1.3s" begin="{d:.2f}s" fill="freeze" {spl}/>')
            return f'<polygon {st}>{an}</polygon>'
        o.append(poly_el(left1, left0, lc)); o.append(poly_el(right1, right0, rc))
        o.append(poly_el(top1, top0, tc, 'stroke="#ffffff" stroke-opacity=".35"'))
        if not STATIC:
            o.append(f'<polygon points="{top1}" fill="#fff" opacity="0"><animate attributeName="opacity" values="0;.4;0" dur="3.2s" begin="{d+1.6:.2f}s" repeatCount="indefinite"/></polygon>')
        lx, ly = P(gx+f/2, gy+f/2, h)
        w = len(name)*8.2 + 44
        pill = (f'<rect x="{-w/2:.0f}" y="-26" width="{w:.0f}" height="20" rx="10" fill="#0d0d1a" stroke="{col}" stroke-opacity=".8"/>'
                f'<text y="-12" text-anchor="middle" font-size="11" font-weight="700" fill="#f3e8ff">{name} <tspan fill="{col}">{pct}</tspan></text>')
        if STATIC:
            labels.append(f'<g transform="translate({lx:.1f},{ly-4:.1f})">{pill}</g>')
        else:
            labels.append(f'<g transform="translate({lx:.1f},{ly-4:.1f})" opacity="0"><animate attributeName="opacity" from="0" to="1" dur=".4s" begin="{d+0.9:.2f}s" fill="freeze"/>'
                          f'<animateTransform attributeName="transform" type="translate" additive="sum" from="0 {h:.0f}" to="0 0" dur="1.3s" begin="{d:.2f}s" fill="freeze" {spl}/>{pill}</g>')
    o += labels
    o.append(f'<text x="{W-30}" y="{H-24}" text-anchor="end" font-size="11" fill="#7c6bb0">height = self-rated depth (0–100)</text>')
    o.append('</svg>')
    save("skyline.svg", o)

# ════════════════════════════════════════════════════════════════════
# 3. PIXEL NAME — contribution-graph style glowing pixels
# ════════════════════════════════════════════════════════════════════
FONT5 = {
 "V": ["10001","10001","10001","10001","10001","01010","00100"],
 "A": ["01110","10001","10001","11111","10001","10001","10001"],
 "I": ["11111","00100","00100","00100","00100","00100","11111"],
 "B": ["11110","10001","10001","11110","10001","10001","11110"],
 "H": ["10001","10001","10001","11111","10001","10001","10001"],
}
def pixelname(word="VAIBHAVI"):
    cell, pitch, W, H = 15, 18, 900, 250
    cols = len(word)*6 - 1
    x0 = (W - cols*pitch)/2; y0 = 62
    shades = ["#7c3aed", "#8b5cf6", "#a78bfa", "#bf94ff", "#bf94ff", "#22d3ee"]
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="{FONT}">',
         '<defs><linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0a0a18"/><stop offset="1" stop-color="#160c30"/></linearGradient></defs>',
         f'<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="18" fill="url(#bg)" stroke="#3b2a78" stroke-width="1.5"/>',
         '<text x="30" y="40" font-size="13" font-weight="700" fill="#bf94ff" letter-spacing="2">// IDENTITY.PIXEL</text>']
    for c in range(cols):
        for r in range(7):
            o.append(f'<rect x="{x0+c*pitch:.0f}" y="{y0+r*pitch}" width="{cell}" height="{cell}" rx="3" fill="#171030"/>')
    for li, ch in enumerate(word):
        for r, row in enumerate(FONT5[ch]):
            for k, bit in enumerate(row):
                if bit != "1": continue
                c = li*6 + k; t = c/(cols-1); col = mix("#8b5cf6", "#d8b4fe", t*2) if t < .5 else mix("#d8b4fe", "#22d3ee", (t-.5)*2)
                wave = (f'<animate attributeName="fill-opacity" values=".6;1;.6" dur="3.2s" begin="{c*0.07:.2f}s" repeatCount="indefinite"/>')
                o.append(f'<rect x="{x0+c*pitch:.0f}" y="{y0+r*pitch}" width="{cell}" height="{cell}" rx="3" fill="{col}" fill-opacity=".85">{A(wave)}</rect>')
    o.append(f'<text x="{W/2}" y="{H-26}" text-anchor="middle" font-size="13" fill="#9d8fd0" letter-spacing="5">ML / AI ENGINEER · BUILDER · EXPLORER</text>')
    o.append('</svg>')
    save("pixel-name.svg", o)

# ════════════════════════════════════════════════════════════════════
# 4. BOOT TERMINAL — typewriter loop
# ════════════════════════════════════════════════════════════════════
def boot():
    W, H, T, cw = 900, 340, 18.0, 9.0
    ok = lambda t: ("ok", t)
    lines = [("cmd", "$ ./boot.sh --user vaibhavi"),
             ("ok",  "mounting neural.profile v2.0"),
             ("ok",  "loading transformers ............ 100%"),
             ("ok",  "compiling ideas into shipped products"),
             ("ok",  "leetcode streak detected: 25 days"),
             ("out", "> ready. let's build something extraordinary.")]
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="{FONT}">',
         '<defs><linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0a0a18"/><stop offset="1" stop-color="#160c30"/></linearGradient>'
         '<linearGradient id="scan" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#bf94ff" stop-opacity="0"/><stop offset=".5" stop-color="#bf94ff" stop-opacity=".25"/><stop offset="1" stop-color="#bf94ff" stop-opacity="0"/></linearGradient>']
    clips = []
    for i, (kind, txt) in enumerate(lines):
        n = len(txt) + (7 if kind == "ok" else 0)
        base = 100 + i*34; s = 0.8 + i*2.3; dt = 0.04
        kt, val = [0.0], [0.0]
        for k in range(1, n+1):
            kt.append((s + k*dt)/T); val.append(k*cw + 2)
        kt += [0.96, 1.0]; val += [0, 0]
        anim = A(f'<animate attributeName="width" calcMode="discrete" values="{";".join(f"{v:.1f}" for v in val)}" keyTimes="{";".join(f"{t:.4f}" for t in kt)}" dur="{T}s" repeatCount="indefinite"/>')
        w0 = (n*cw + 2) if STATIC else 0
        clips.append(f'<clipPath id="c{i}"><rect x="44" y="{base-20}" width="{w0}" height="28">{anim}</rect></clipPath>')
    o += clips + ['</defs>',
         f'<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="18" fill="url(#bg)" stroke="#3b2a78" stroke-width="1.5"/>',
         '<circle cx="34" cy="32" r="6" fill="#f472b6"/><circle cx="54" cy="32" r="6" fill="#fbbf24"/><circle cx="74" cy="32" r="6" fill="#34d399"/>',
         '<text x="96" y="36" font-size="12" fill="#6b5b95">vaibhavi@neural-profile: ~</text>',
         '<line x1="24" y1="54" x2="876" y2="54" stroke="#2a1f4d"/>']
    for i, (kind, txt) in enumerate(lines):
        base = 100 + i*34
        if kind == "cmd":   inner = f'<tspan fill="#34d399">$</tspan><tspan fill="#f3e8ff">{txt[1:]}</tspan>'
        elif kind == "ok":  inner = f'<tspan fill="#8b7bbd">[ </tspan><tspan fill="#34d399" font-weight="700">OK</tspan><tspan fill="#8b7bbd"> ]</tspan><tspan fill="#d9ccff"> {txt}</tspan>'
        else:               inner = f'<tspan fill="#22d3ee" font-weight="700">{txt.replace(">", "&gt;")}</tspan>'
        o.append(f'<text x="48" y="{base}" font-size="15" clip-path="url(#c{i})">{inner}</text>')
    by = 100 + len(lines)*34
    o.append(f'<text x="48" y="{by}" font-size="15" fill="#34d399">$</text>')
    o.append(f'<rect x="{48+cw*2}" y="{by-14}" width="9" height="18" fill="#bf94ff">'
             + A(f'<animate attributeName="opacity" values="1;0;1" dur=".9s" repeatCount="indefinite"/>') + '</rect>')
    if not STATIC:
        o.append(f'<rect x="24" y="54" width="852" height="40" fill="url(#scan)" opacity=".5"><animate attributeName="y" values="54;300;54" dur="6s" repeatCount="indefinite"/></rect>')
    o.append('</svg>')
    save("boot.svg", o)

galaxy(); skyline(); pixelname(); boot()
