import random, math, os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
MONO = "'JetBrains Mono','Fira Code','SF Mono',Consolas,'Courier New',monospace"
SANS = "'Inter','Segoe UI',Roboto,'Helvetica Neue',Arial,sans-serif"
P, P2, CY, PK = "#bf94ff", "#7c3aed", "#22d3ee", "#f472b6"


def save(name, svg):
    with open(f"{OUT}/{name}", "w") as f:
        f.write(svg)


def stars(rng, n, w, h, cls="tw"):
    s = []
    for _ in range(n):
        x, y = rng.uniform(4, w - 4), rng.uniform(4, h - 4)
        r = rng.uniform(0.5, 1.3)
        d = rng.uniform(0, 5)
        s.append(f'<circle class="{cls}" cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="#e9d5ff" style="animation-delay:{d:.1f}s"/>')
    return "\n".join(s)


def layer_pos(xs, counts, cy, sp):
    layers = []
    for x, n in zip(xs, counts):
        layers.append([(x, cy + (i - (n - 1) / 2) * sp) for i in range(n)])
    return layers


def net_edges(layers, op=0.28, w=0.8, color=P2):
    out = []
    for a, b in zip(layers, layers[1:]):
        for (x1, y1) in a:
            for (x2, y2) in b:
                out.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{color}" stroke-opacity="{op}" stroke-width="{w}"/>')
    return "\n".join(out)


def net_nodes(rng, layers, r=6, inner=2.4):
    out = []
    for li, L in enumerate(layers):
        for (x, y) in L:
            d = rng.uniform(0, 4)
            col = CY if li in (0, len(layers) - 1) else P
            out.append(
                f'<g class="nd" style="animation-delay:{d:.1f}s"><circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="#0d0a1f" stroke="{col}" stroke-width="1.4"/>'
                f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{inner}" fill="{col}"/></g>')
    return "\n".join(out)


def pulses(rng, layers, n, color=CY, dur=(2.6, 4.2)):
    out = []
    for _ in range(n):
        pts = [rng.choice(L) for L in layers]
        d = "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts)
        t = rng.uniform(*dur)
        b = rng.uniform(0, 5)
        out.append(
            f'<circle r="2.6" fill="{color}" filter="url(#glow)"><animateMotion path="{d}" dur="{t:.1f}s" begin="{b:.1f}s" repeatCount="indefinite"/>'
            f'<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.1;0.9;1" dur="{t:.1f}s" begin="{b:.1f}s" repeatCount="indefinite"/></circle>')
    return "\n".join(out)


COMMON_DEFS = f"""
<filter id="glow" x="-100%" y="-100%" width="300%" height="300%"><feGaussianBlur stdDeviation="2.6" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<linearGradient id="tg" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#f3e8ff"/><stop offset=".5" stop-color="{P}"/><stop offset="1" stop-color="{CY}"/></linearGradient>
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0b0818"/><stop offset=".55" stop-color="#140b2e"/><stop offset="1" stop-color="#07060f"/></linearGradient>
<linearGradient id="bd" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{P2}"/><stop offset=".5" stop-color="{CY}" stop-opacity=".7"/><stop offset="1" stop-color="{P}"/></linearGradient>
<pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse"><path d="M40 0H0V40" fill="none" stroke="{P2}" stroke-opacity=".08"/></pattern>
"""

COMMON_CSS = """
.tw{animation:tw 4s ease-in-out infinite;opacity:.15}
@keyframes tw{0%,100%{opacity:.1}50%{opacity:.9}}
.nd{animation:nd 3.2s ease-in-out infinite;transform-box:fill-box;transform-origin:center}
@keyframes nd{0%,100%{opacity:.55;transform:scale(1)}50%{opacity:1;transform:scale(1.25)}}
"""


def frame(w, h, body, defs="", css="", title=""):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{title}">
<title>{title}</title>
<defs>{COMMON_DEFS}{defs}
<clipPath id="rc"><rect width="{w}" height="{h}" rx="18"/></clipPath>
</defs>
<style>{COMMON_CSS}{css}</style>
<g clip-path="url(#rc)">
<rect width="{w}" height="{h}" fill="url(#bg)"/>
<rect width="{w}" height="{h}" fill="url(#grid)"/>
{body}
</g>
<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="17" fill="none" stroke="url(#bd)" stroke-opacity=".55" stroke-width="1.5"/>
</svg>"""


# ------------------------------------------------------------------ BANNER
def banner():
    rng = random.Random(7)
    W, H = 1200, 320
    L = layer_pos([40, 102, 164, 226], [5, 7, 7, 5], 160, 36)
    R = layer_pos([974, 1036, 1098, 1160], [5, 7, 7, 5], 160, 36)
    # flow arcs between nets (behind the name)
    arcs = []
    for i, dy in enumerate([-60, -30, 0, 30, 60]):
        y = 160 + dy
        arcs.append(f'<path d="M226 {y} C 420 {y-70}, 780 {y+70}, 974 {y}" fill="none" stroke="{CY}" stroke-opacity=".28" stroke-width="1" stroke-dasharray="4 8" class="flow" style="animation-delay:{i*0.4}s"/>')
    phrases = [
        "Building neural networks from scratch",
        "Fine-tuning LLMs &amp; transformers",
        "Turning data into intelligence",
        "Shipping AI-powered products",
    ]
    rot = "\n".join(
        f'<text class="rot" x="600" y="244" text-anchor="middle" style="animation-delay:{i*3}s" font-family="{MONO}" font-size="17" fill="#e9d5ff">'
        f'<tspan fill="{CY}">&gt; </tspan>{p}<tspan fill="{CY}" class="cur">_</tspan></text>'
        for i, p in enumerate(phrases))
    body = f"""
{stars(rng, 70, W, H)}
<ellipse cx="600" cy="160" rx="360" ry="110" fill="{P2}" opacity=".16" filter="url(#blur)"/>
{''.join(arcs)}
{net_edges(L)}{net_edges(R)}
{net_nodes(rng, L)}{net_nodes(rng, R)}
{pulses(rng, L, 9)}{pulses(rng, R, 9, color=P)}
<text x="40" y="28" font-family="{MONO}" font-size="10" fill="{P}" opacity=".6" letter-spacing="3">INPUT LAYER</text>
<text x="1160" y="28" text-anchor="end" font-family="{MONO}" font-size="10" fill="{P}" opacity=".6" letter-spacing="3">OUTPUT LAYER</text>
<text x="600" y="98" text-anchor="middle" font-family="{MONO}" font-size="12" fill="{CY}" letter-spacing="6">// NEURAL.PROFILE  v2.0</text>
<text x="290" y="158" textLength="620" lengthAdjust="spacingAndGlyphs" font-family="{SANS}" font-size="50" font-weight="800" fill="url(#tg)" filter="url(#glow)">VAIBHAVI SHARNAGAT</text>
<text x="600" y="196" text-anchor="middle" font-family="{MONO}" font-size="15" fill="#9d7fe0" letter-spacing="6">ML / AI ENGINEER · BUILDER · EXPLORER</text>
<line x1="470" y1="214" x2="730" y2="214" stroke="url(#tg)" stroke-width="1.4" stroke-opacity=".7"/>
{rot}
<g font-family="{MONO}" font-size="11" fill="#9d7fe0">
<circle cx="476" cy="292" r="3.5" fill="#34d399" class="nd"/>
<text x="487" y="296" letter-spacing="2">STATUS: TRAINING</text>
<text x="650" y="296" letter-spacing="2">LOSS ↓  ·  ACC ↑  ·  SHIP IT</text>
</g>
"""
    defs = '<filter id="blur"><feGaussianBlur stdDeviation="28"/></filter>'
    css = """
.flow{animation:flow 3s linear infinite}
@keyframes flow{to{stroke-dashoffset:-48}}
.rot{opacity:0;animation:rot 12s infinite}
@keyframes rot{0%{opacity:0}2.5%{opacity:1}22%{opacity:1}25%{opacity:0}100%{opacity:0}}
.cur{animation:cur 1s steps(1) infinite}
@keyframes cur{50%{opacity:0}}
"""
    save("banner.svg", frame(W, H, body, defs, css, "Vaibhavi Sharnagat — ML / AI Engineer"))


# ------------------------------------------------------------------ DIVIDER
def divider():
    rng = random.Random(3)
    W, H = 1200, 44
    nodes = "".join(
        f'<g class="nd" style="animation-delay:{rng.uniform(0,3):.1f}s"><circle cx="{x}" cy="22" r="4" fill="#0d0a1f" stroke="{P}" stroke-width="1.3"/><circle cx="{x}" cy="22" r="1.6" fill="{CY}"/></g>'
        for x in range(120, 1100, 120))
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="presentation">
<defs><linearGradient id="fade" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{P2}" stop-opacity="0"/><stop offset=".5" stop-color="{P}"/><stop offset="1" stop-color="{P2}" stop-opacity="0"/></linearGradient>
<filter id="glow" x="-100%" y="-100%" width="300%" height="300%"><feGaussianBlur stdDeviation="2.4" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>
<style>{COMMON_CSS}</style>
<line x1="40" y1="22" x2="1160" y2="22" stroke="url(#fade)" stroke-width="1.5"/>
{nodes}
<circle r="3.4" cy="22" fill="{CY}" filter="url(#glow)"><animate attributeName="cx" values="40;1160" dur="4.5s" repeatCount="indefinite"/><animate attributeName="opacity" values="0;1;1;0" keyTimes="0;.1;.9;1" dur="4.5s" repeatCount="indefinite"/></circle>
</svg>"""
    save("divider.svg", svg)


# ------------------------------------------------------------------ ABOUT
def about():
    rng = random.Random(11)
    W, H = 1200, 540
    # terminal
    TX, TY, TW, TH = 36, 30, 650, 480
    C_KEY, C_STR, C_PUN, C_NUM = "#bf94ff", "#86efac", "#94a3b8", "#fbbf24"
    lines = [
        [("vaibhavi@neural-net", "#34d399"), (":", C_PUN), ("~", "#60a5fa"), ("$ ", C_PUN), ("cat about.json", "#e9d5ff")],
        [("{", C_PUN)],
        [('  "name"', C_KEY), (": ", C_PUN), ('"Vaibhavi Sharnagat"', C_STR), (",", C_PUN)],
        [('  "role"', C_KEY), (": ", C_PUN), ('"ML / AI Engineer"', C_STR), (",", C_PUN)],
        [('  "location"', C_KEY), (": ", C_PUN), ('"Earth (mostly online)"', C_STR), (",", C_PUN)],
        [('  "languages"', C_KEY), (": ", C_PUN), ('["Python", "C++", "SQL", "Bash"]', C_STR), (",", C_PUN)],
        [('  "focus"', C_KEY), (": ", C_PUN), ('["LLMs", "Computer Vision", "MLOps", "GenAI"]', C_STR), (",", C_PUN)],
        [('  "currently"', C_KEY), (": ", C_PUN), ('"Building intelligent systems', C_STR)],
        [('                that actually work"', C_STR), (",", C_PUN)],
        [('  "learning"', C_KEY), (": ", C_PUN), ('["Agent frameworks", "RLHF",', C_STR)],
        [('               "Diffusion models"]', C_STR), (",", C_PUN)],
        [('  "ask_me_about"', C_KEY), (": ", C_PUN), ('["ML pipelines", "fine-tuning",', C_STR)],
        [('                   "research papers"]', C_STR), (",", C_PUN)],
        [('  "fun_fact"', C_KEY), (": ", C_PUN), ('"I debug neural nets at 2AM', C_STR)],
        [('               and somehow enjoy it"', C_STR)],
        [("}", C_PUN)],
        [("vaibhavi@neural-net", "#34d399"), (":", C_PUN), ("~", "#60a5fa"), ("$ ", C_PUN), ("echo ", "#e9d5ff"), ('"Let\'s build something extraordinary."', C_STR)],
    ]
    trows = []
    y0, lh = 130, 20.5
    for i, parts in enumerate(lines):
        spans = ""
        first = True
        for t, c in parts:
            t = t.replace("&", "&amp;").replace("<", "&lt;")
            spans += f'<tspan fill="{c}">{t}</tspan>'
        trows.append(f'<text class="ln" xml:space="preserve" x="{TX+26}" y="{y0+i*lh:.1f}" style="animation-delay:{0.35*i:.2f}s">{spans}</text>')
    trows.append(f'<text x="{TX+26}" y="{y0+len(lines)*lh+6:.1f}" font-family="{MONO}" font-size="14" fill="#34d399" class="cur">█</text>')
    terminal = f"""
<rect x="{TX}" y="{TY}" width="{TW}" height="{TH}" rx="14" fill="#0a0716" stroke="{P2}" stroke-opacity=".6"/>
<path d="M{TX} {TY+14} a14 14 0 0 1 14 -14 H{TX+TW-14} a14 14 0 0 1 14 14 V{TY+40} H{TX} Z" fill="#150e30"/>
<circle cx="{TX+24}" cy="{TY+20}" r="6" fill="#ff5f57"/><circle cx="{TX+44}" cy="{TY+20}" r="6" fill="#febc2e"/><circle cx="{TX+64}" cy="{TY+20}" r="6" fill="#28c840"/>
<text x="{TX+TW/2}" y="{TY+25}" text-anchor="middle" font-family="{MONO}" font-size="12" fill="#9d7fe0">vaibhavi — zsh — 80×24</text>
<text x="{TX+26}" y="{TY+74}" font-family="{MONO}" font-size="11" fill="{CY}" letter-spacing="3">// WHOAMI</text>
<g font-family="{MONO}" font-size="13.5">{''.join(trows)}</g>
"""
    # network panel
    NX, NY, NW, NH = 712, 30, 452, 480
    layers = layer_pos([752, 862, 972, 1082], [3, 5, 5, 2], 215, 46)
    heads = ["INPUT", "HIDDEN", "HIDDEN", "OUTPUT"]
    hd = "".join(f'<text x="{x}" y="{NY+68}" text-anchor="middle" font-family="{MONO}" font-size="10" fill="#9d7fe0" letter-spacing="2">{h}</text>'
                 for (x, h) in zip([752, 862, 972, 1082], heads))
    labels_in = ["curiosity", "data", "code"]
    li = "".join(f'<text x="{layers[0][i][0]-14}" y="{layers[0][i][1]+4}" text-anchor="end" font-family="{MONO}" font-size="0"> </text>' for i in range(3))
    tiles = [("66", "LEETCODE SOLVED"), ("25", "DAY MAX STREAK"), ("123", "ACTIVE DAYS")]
    tl = ""
    for i, (n, l) in enumerate(tiles):
        x = NX + 14 + i * 144
        tl += f"""<g><rect x="{x}" y="372" width="132" height="104" rx="10" fill="#120d26" stroke="{P2}" stroke-opacity=".5"/>
<text x="{x+66}" y="422" text-anchor="middle" font-family="{SANS}" font-size="36" font-weight="800" fill="url(#tg)">{n}</text>
<text x="{x+66}" y="450" text-anchor="middle" font-family="{MONO}" font-size="9.5" fill="#9d7fe0" letter-spacing="1.5">{l}</text></g>"""
    panel = f"""
<rect x="{NX}" y="{NY}" width="{NW}" height="{NH}" rx="14" fill="#0a0716" stroke="{P2}" stroke-opacity=".6"/>
<text x="{NX+24}" y="{NY+30}" font-family="{MONO}" font-size="11" fill="{CY}" letter-spacing="3">// FORWARD PASS</text>
<text x="{NX+NW-24}" y="{NY+30}" text-anchor="end" font-family="{MONO}" font-size="10" fill="#9d7fe0" letter-spacing="2">curiosity + data + code</text>
{hd}
{net_edges(layers, 0.3)}
{net_nodes(rng, layers, 7, 2.8)}
{pulses(rng, layers, 12)}
<text x="{NX+NW/2}" y="338" text-anchor="middle" font-family="{SANS}" font-size="16" font-weight="700" fill="#e9d5ff" letter-spacing="1">→ intelligence that ships</text>
{tl}
"""
    css = """
.ln{opacity:0;animation:ln 18s infinite;font-family:%s}
@keyframes ln{0%%{opacity:0}1.5%%{opacity:1}93%%{opacity:1}97%%{opacity:0}100%%{opacity:0}}
.cur{animation:cur 1s steps(1) infinite}
@keyframes cur{50%%{opacity:0}}
""" % MONO.replace("'", "'")
    body = stars(rng, 40, W, H) + terminal + panel
    save("about.svg", frame(W, H, body, "", css.replace("%%", "%"), "About Vaibhavi"))


# ------------------------------------------------------------------ STACK
def stack():
    rng = random.Random(5)
    W, H = 1200, 600
    skills = [("MACHINE LEARNING", 95), ("DEEP LEARNING", 90), ("NLP / LLMs", 88), ("COMPUTER VISION", 85),
              ("MLOps / PIPELINES", 80), ("DATA ENGINEERING", 75), ("CLOUD ARCHITECTURE", 70), ("BACKEND / API", 65)]
    BW = 440
    bars = ""
    for i, (n, v) in enumerate(skills):
        y = 150 + i * 52
        ticks = "".join(f'<line x1="{60+BW*k/10:.0f}" y1="{y+8}" x2="{60+BW*k/10:.0f}" y2="{y+20}" stroke="#0b0818" stroke-width="2"/>' for k in range(1, 10))
        bars += f"""<g>
<text x="60" y="{y}" font-family="{MONO}" font-size="12" fill="#e9d5ff" letter-spacing="2">{n}</text>
<text x="{60+BW}" y="{y}" text-anchor="end" font-family="{MONO}" font-size="12" fill="{CY}">{v}%</text>
<rect x="60" y="{y+8}" width="{BW}" height="12" rx="6" fill="#1a1433"/>
<rect class="bar" x="60" y="{y+8}" width="{BW*v/100:.1f}" height="12" rx="6" fill="url(#barg)" style="animation-delay:{i*0.12:.2f}s" filter="url(#glow)"/>
{ticks}</g>"""
    groups = [
        ("AI / ML CORE", P, ["Python", "PyTorch", "TensorFlow", "HuggingFace", "scikit-learn", "OpenCV", "LangChain", "ONNX"]),
        ("MLOPS & INFRA", CY, ["Docker", "Kubernetes", "MLflow", "W&amp;B", "FastAPI", "Airflow", "GitHub Actions"]),
        ("CLOUD & DATA", PK, ["AWS", "GCP", "PostgreSQL", "MongoDB", "Redis", "Apache Spark"]),
    ]
    PX0, PXW = 620, 540
    chips = ""
    y = 112
    ci = 0
    for title, col, items in groups:
        title = title.replace("&", "&amp;")
        chips += f'<circle cx="{PX0+6}" cy="{y}" r="4" fill="{col}" class="nd"/><text x="{PX0+20}" y="{y+4}" font-family="{MONO}" font-size="12" fill="{col}" letter-spacing="3">{title}</text>'
        chips += f'<line x1="{PX0+20+len(title)*10+10}" y1="{y}" x2="{PX0+PXW}" y2="{y}" stroke="{col}" stroke-opacity=".3"/>'
        y += 18
        x = PX0
        for it in items:
            plain = it.replace("&amp;", "&")
            w = len(plain) * 8.2 + 28
            if x + w > PX0 + PXW:
                x = PX0
                y += 42
            chips += f"""<g class="chip" style="animation-delay:{(ci%7)*0.35:.2f}s"><rect x="{x:.0f}" y="{y}" width="{w:.0f}" height="32" rx="8" fill="#120d26" stroke="{col}" stroke-opacity=".6"/>
<text x="{x+w/2:.0f}" y="{y+21}" text-anchor="middle" font-family="{MONO}" font-size="13" fill="#f3e8ff">{it}</text></g>"""
            x += w + 10
            ci += 1
        y += 62
    body = f"""
{stars(rng, 50, W, H)}
<text x="60" y="52" font-family="{SANS}" font-size="28" font-weight="800" fill="url(#tg)">CAPABILITY STACK</text>
<text x="60" y="76" font-family="{MONO}" font-size="12" fill="#9d7fe0" letter-spacing="2">// from tensors to production — end to end</text>
<line x1="60" y1="96" x2="1160" y2="96" stroke="url(#bd)" stroke-opacity=".5"/>
<text x="60" y="124" font-family="{MONO}" font-size="11" fill="{CY}" letter-spacing="3">// SKILL MATRIX</text>
{bars}
{chips}
"""
    defs = f'<linearGradient id="barg" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{P2}"/><stop offset="1" stop-color="{CY}"/></linearGradient>'
    css = """
.bar{transform-box:fill-box;transform-origin:left center;animation:grow 9s ease-out infinite}
@keyframes grow{0%{transform:scaleX(0)}16%{transform:scaleX(1)}100%{transform:scaleX(1)}}
.chip{animation:fl 4.5s ease-in-out infinite}
@keyframes fl{0%,100%{transform:translateY(0)}50%{transform:translateY(-3px)}}
"""
    save("stack.svg", frame(W, H, body, defs, css, "Capability stack"))


# ------------------------------------------------------------------ LEETCODE
def hexagon(cx, cy, r, num, c1, c2, uid, delay):
    def pts(rr):
        return " ".join(f"{cx+rr*math.cos(math.radians(a)):.1f},{cy+rr*math.sin(math.radians(a)):.1f}" for a in range(-90, 270, 60))
    return f"""<g class="fl" style="animation-delay:{delay}s">
<polygon points="{pts(r)}" fill="#0d0a1f" stroke="url(#{uid})" stroke-width="3" filter="url(#glow)"/>
<polygon points="{pts(r*0.78)}" fill="url(#{uid}f)" opacity=".9"/>
<text x="{cx}" y="{cy+9}" text-anchor="middle" font-family="{SANS}" font-size="{26 if len(num)<3 else 22}" font-weight="800" fill="#fff">{num}</text>
<text x="{cx}" y="{cy+24}" text-anchor="middle" font-family="{MONO}" font-size="7.5" fill="#fff" letter-spacing="2" opacity=".85">DAYS</text></g>"""


def leetcode():
    rng = random.Random(9)
    W, H = 1200, 400
    E, M, Hd = 28, 35, 3
    tot = E + M + Hd
    # ring
    cx, cy, r = 210, 222, 80
    C = 2 * math.pi * r
    arc = C * 270 / 360
    segs = [("#00b8a3", E), ("#ffc01e", M), ("#ff375f", Hd)]
    ring = f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#1a1433" stroke-width="12" stroke-linecap="round" stroke-dasharray="{arc:.1f} {C:.1f}" transform="rotate(135 {cx} {cy})"/>'
    gap = 7
    start = 0
    for col, v in segs:
        ln = (arc - gap * 2) * v / tot
        ring += f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{col}" stroke-width="12" stroke-linecap="round" stroke-dasharray="{ln:.1f} {C:.1f}" stroke-dashoffset="{-start:.1f}" transform="rotate(135 {cx} {cy})" filter="url(#glow)"/>'
        start += ln + gap
    card1 = f"""
<rect x="40" y="72" width="340" height="300" rx="14" fill="#0a0716" stroke="{P2}" stroke-opacity=".55"/>
<text x="64" y="102" font-family="{MONO}" font-size="11" fill="{CY}" letter-spacing="3">// SOLVED</text>
<circle cx="{cx}" cy="{cy}" r="104" fill="none" stroke="{P}" stroke-opacity=".35" stroke-dasharray="2 10" class="spin"/>
{ring}
<text x="{cx}" y="{cy+8}" text-anchor="middle" font-family="{SANS}" font-size="54" font-weight="800" fill="url(#tg)">{tot}</text>
<text x="{cx+44}" y="{cy+8}" font-family="{MONO}" font-size="14" fill="#9d7fe0" text-anchor="start" opacity="0"> </text>
<text x="{cx}" y="{cy+34}" text-anchor="middle" font-family="{MONO}" font-size="12" fill="#9d7fe0">of 4101 problems</text>
<text x="{cx}" y="{cy+98}" text-anchor="middle" font-family="{MONO}" font-size="12" fill="#e9d5ff">7 attempting</text>
"""
    rows = [("EASY", E, 975, "#00b8a3"), ("MEDIUM", M, 2139, "#ffc01e"), ("HARD", Hd, 987, "#ff375f")]
    bars = ""
    for i, (n, v, t, col) in enumerate(rows):
        y = 150 + i * 62
        bars += f"""<g><text x="440" y="{y}" font-family="{MONO}" font-size="12" fill="{col}" letter-spacing="2" font-weight="700">{n}</text>
<text x="760" y="{y}" text-anchor="end" font-family="{MONO}" font-size="13" fill="#64748b">/ {t}</text><text x="{760-8-len(str(t))*8-14}" y="{y}" text-anchor="end" font-family="{MONO}" font-size="13" fill="#f3e8ff" font-weight="700">{v}</text>
<rect x="440" y="{y+10}" width="320" height="10" rx="5" fill="#1a1433"/>
<rect class="bar" x="440" y="{y+10}" width="{320*v/tot:.1f}" height="10" rx="5" fill="{col}" filter="url(#glow)" style="animation-delay:{i*0.2}s"/></g>"""
    card2 = f"""
<rect x="410" y="72" width="380" height="300" rx="14" fill="#0a0716" stroke="{P2}" stroke-opacity=".55"/>
<text x="440" y="102" font-family="{MONO}" font-size="11" fill="{CY}" letter-spacing="3">// DIFFICULTY SPLIT</text>
{bars}
<text x="440" y="342" font-family="{MONO}" font-size="11" fill="#9d7fe0">bar = share of my solves · totals = LeetCode catalogue</text>
<g><rect x="440" y="320" width="0" height="0"/></g>
"""
    # card 3 : badges + stats
    b1 = hexagon(930, 168, 48, "50", "#34d399", "#16a34a", "hx1", 0)
    b2 = hexagon(1050, 168, 48, "100", "#60a5fa", "#2563eb", "hx2", 0.8)
    stats = [("241", "SUBMISSIONS / YR"), ("123", "ACTIVE DAYS"), ("25", "MAX STREAK")]
    st = ""
    for i, (n, l) in enumerate(stats):
        x = 836 + i * 106
        st += f"""<g><rect x="{x}" y="262" width="98" height="64" rx="9" fill="#120d26" stroke="{P2}" stroke-opacity=".45"/>
<text x="{x+49}" y="290" text-anchor="middle" font-family="{SANS}" font-size="22" font-weight="800" fill="url(#tg)">{n}</text>
<text x="{x+49}" y="311" text-anchor="middle" font-family="{MONO}" font-size="7.5" fill="#9d7fe0" letter-spacing="1">{l}</text></g>"""
    card3 = f"""
<rect x="820" y="72" width="340" height="300" rx="14" fill="#0a0716" stroke="{P2}" stroke-opacity=".55"/>
<text x="844" y="102" font-family="{MONO}" font-size="11" fill="{CY}" letter-spacing="3">// BADGES</text>
{b1}{b2}
<text x="930" y="238" text-anchor="middle" font-family="{MONO}" font-size="10" fill="#e9d5ff">50 Days Badge</text>
<text x="1050" y="238" text-anchor="middle" font-family="{MONO}" font-size="10" fill="#e9d5ff">100 Days 2026</text>
{st}
<text x="990" y="352" text-anchor="middle" font-family="{MONO}" font-size="11" fill="#9d7fe0">global rank <tspan fill="{CY}" font-weight="700">2,331,830</tspan></text>
"""
    body = f"""
{stars(rng, 40, W, H)}
<text x="40" y="44" font-family="{SANS}" font-size="24" font-weight="800" fill="url(#tg)">LEETCODE // PROBLEM SOLVING</text>
<text x="1160" y="44" text-anchor="end" font-family="{MONO}" font-size="13" fill="#9d7fe0">@vaibhavisharnagat</text>
{card1}{card2}{card3}
"""
    defs = f"""
<linearGradient id="hx1" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#a7f3d0"/><stop offset="1" stop-color="#059669"/></linearGradient>
<linearGradient id="hx1f" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#34d399"/><stop offset="1" stop-color="#065f46"/></linearGradient>
<linearGradient id="hx2" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#bfdbfe"/><stop offset="1" stop-color="#1d4ed8"/></linearGradient>
<linearGradient id="hx2f" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#60a5fa"/><stop offset="1" stop-color="#1e3a8a"/></linearGradient>
"""
    css = """
.spin{transform-box:fill-box;transform-origin:center;animation:spin 30s linear infinite}
@keyframes spin{to{transform:rotate(360deg)}}
.bar{transform-box:fill-box;transform-origin:left center;animation:grow 8s ease-out infinite}
@keyframes grow{0%{transform:scaleX(0)}18%{transform:scaleX(1)}100%{transform:scaleX(1)}}
.fl{animation:fl 3.6s ease-in-out infinite}
@keyframes fl{0%,100%{transform:translateY(0)}50%{transform:translateY(-6px)}}
"""
    save("leetcode.svg", frame(W, H, body, defs, css, "LeetCode stats for vaibhavisharnagat"))


# ------------------------------------------------------------------ TROPHIES
def cup(cx, cy, grad, uid, delay):
    bowl = "M-28 -40 H28 V-10 C28 14 12 24 0 24 C-12 24 -28 14 -28 -10 Z"
    return f"""<g transform="translate({cx} {cy}) scale(1.25)" class="cp" style="animation-delay:{delay}s">
<clipPath id="c{uid}"><path d="{bowl}"/></clipPath>
<path d="M-28 -32 C-52 -34 -50 -4 -24 -2" fill="none" stroke="url(#{grad})" stroke-width="6" stroke-linecap="round"/>
<path d="M28 -32 C52 -34 50 -4 24 -2" fill="none" stroke="url(#{grad})" stroke-width="6" stroke-linecap="round"/>
<rect x="-5" y="22" width="10" height="16" fill="url(#{grad})"/>
<rect x="-20" y="38" width="40" height="9" rx="3" fill="url(#{grad})"/>
<path d="{bowl}" fill="url(#{grad})" stroke="#ffffff" stroke-opacity=".35"/>
<path d="M0 -26 l4.5 9.5 10.3 1.4 -7.5 7.2 1.9 10.3 -9.2 -5 -9.2 5 1.9 -10.3 -7.5 -7.2 10.3 -1.4 z" fill="#ffffff" fill-opacity=".85"/>
<rect class="sh" x="-60" y="-50" width="14" height="110" fill="#fff" fill-opacity=".55" clip-path="url(#c{uid})"/>
</g>"""


def trophies():
    rng = random.Random(21)
    W, H = 1200, 430
    items = [
        ("SOLVER", "66", "problems solved", "gold", "LEETCODE"),
        ("STREAK", "25", "day max streak", "purple", "CONSISTENCY"),
        ("GRINDER", "123", "active days", "cyan", "DISCIPLINE"),
        ("VOLUME", "241", "submissions / year", "silver", "OUTPUT"),
        ("MILESTONE", "100", "days badge 2026", "gold", "LEETCODE"),
        ("MILESTONE", "50", "days badge", "bronze", "LEETCODE"),
    ]
    cw, gap, x0 = 176, 12.8, 40
    out = ""
    for i, (t, v, s, g, tag) in enumerate(items):
        x = x0 + i * (cw + gap)
        mx = x + cw / 2
        out += f"""<g>
<rect x="{x:.1f}" y="84" width="{cw}" height="294" rx="14" fill="#0a0716" stroke="{P2}" stroke-opacity=".5"/>
<text x="{mx:.1f}" y="112" text-anchor="middle" font-family="{MONO}" font-size="10" fill="{CY}" letter-spacing="3">{tag}</text>
<ellipse cx="{mx:.1f}" cy="205" rx="60" ry="46" fill="url(#{g})" opacity=".13" filter="url(#blur)"/>
{cup(mx, 192, g, i, i*0.4)}
<text x="{mx:.1f}" y="294" text-anchor="middle" font-family="{MONO}" font-size="12" fill="#e9d5ff" letter-spacing="3" font-weight="700">{t}</text>
<text x="{mx:.1f}" y="335" text-anchor="middle" font-family="{SANS}" font-size="36" font-weight="800" fill="url(#tg)">{v}</text>
<text x="{mx:.1f}" y="358" text-anchor="middle" font-family="{MONO}" font-size="10" fill="#9d7fe0">{s}</text>
</g>"""
    shelf = f'<rect x="40" y="392" width="1120" height="3" rx="2" fill="url(#bd)" filter="url(#glow)"/>'
    defs = "<filter id='blur'><feGaussianBlur stdDeviation='14'/></filter>"
    for name, (a, b, c) in {"gold": ("#fde68a", "#f59e0b", "#b45309"), "silver": ("#f8fafc", "#94a3b8", "#475569"),
                             "bronze": ("#fdba74", "#c2410c", "#7c2d12"), "purple": ("#e9d5ff", "#a855f7", "#6d28d9"),
                             "cyan": ("#a5f3fc", "#22d3ee", "#0e7490")}.items():
        defs += f'<linearGradient id="{name}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{a}"/><stop offset=".55" stop-color="{b}"/><stop offset="1" stop-color="{c}"/></linearGradient>'
    css = """
.cp{animation:cp 4.2s ease-in-out infinite}
@keyframes cp{0%,100%{transform-box:fill-box}}
.sh{animation:sh 3.6s ease-in-out infinite}
@keyframes sh{0%{transform:translateX(0) skewX(-20deg);opacity:0}15%{opacity:1}55%{transform:translateX(130px) skewX(-20deg);opacity:0}100%{transform:translateX(130px) skewX(-20deg);opacity:0}}
"""
    body = f"""
{stars(rng, 40, W, H)}
<text x="40" y="44" font-family="{SANS}" font-size="24" font-weight="800" fill="url(#tg)">TROPHY CABINET // ACHIEVEMENTS</text>
<text x="1160" y="44" text-anchor="end" font-family="{MONO}" font-size="13" fill="#9d7fe0">unlocked via consistent shipping</text>
<line x1="40" y1="64" x2="1160" y2="64" stroke="url(#bd)" stroke-opacity=".4"/>
{out}{shelf}
"""
    save("trophies.svg", frame(W, H, body, defs, css, "Trophy cabinet"))


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    banner(); divider(); about(); stack(); leetcode(); trophies()
    print("ok")
