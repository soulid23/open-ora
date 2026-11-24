import json, math, os
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..")
from fontTools.ttLib import TTFont
from fontTools.pens.basePen import BasePen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

SB = TTFont(os.path.join(HERE, "..", "fonts", "SpaceGrotesk-SemiBold.ttf")); MD = TTFont(os.path.join(HERE, "..", "fonts", "SpaceGrotesk-Medium.ttf"))
UPM = 1000.0

def kern_table(font):
    pairs = {}; classes = []
    gpos = font["GPOS"].table
    for li in gpos.FeatureList.FeatureRecord:
        if li.FeatureTag != "kern": continue
        for idx in li.Feature.LookupListIndex:
            lk = gpos.LookupList.Lookup[idx]
            for st in lk.SubTable:
                if lk.LookupType == 9: st = st.ExtSubTable
                if getattr(st, "LookupType", 2) != 2 and lk.LookupType not in (2, 9): continue
                if not hasattr(st, "Format"): continue
                cov = st.Coverage.glyphs
                if st.Format == 1:
                    for i, g1 in enumerate(cov):
                        for pvr in st.PairSet[i].PairValueRecord:
                            v = pvr.Value1.XAdvance if pvr.Value1 and hasattr(pvr.Value1, "XAdvance") else 0
                            pairs.setdefault((g1, pvr.SecondGlyph), v or 0)
                elif st.Format == 2:
                    classes.append(st)
    return pairs, classes

def kern(font, kt, g1, g2):
    pairs, classes = kt
    if (g1, g2) in pairs: return pairs[(g1, g2)]
    for st in classes:
        if g1 not in st.Coverage.glyphs: continue
        c1 = st.ClassDef1.classDefs.get(g1, 0); c2 = st.ClassDef2.classDefs.get(g2, 0)
        rec = st.Class1Record[c1].Class2Record[c2]
        v = getattr(rec.Value1, "XAdvance", 0) if rec.Value1 else 0
        if v: return v
    return 0

KT_SB = kern_table(SB)
def gname(font, ch): return font.getBestCmap()[ord(ch)]
def adv(font, ch): return font["hmtx"][gname(font, ch)][0] / UPM

class FlatPen(BasePen):
    def __init__(self, gs, xf, n=10):
        super().__init__(gs); self.xf = xf; self.loops = []; self.cur = None; self.n = n
    def _moveTo(self, p): self.cur = [self.xf(p)]; self.start = p; self.last = p
    def _lineTo(self, p): self.cur.append(self.xf(p)); self.last = p
    def _curveToOne(self, p1, p2, p3):
        p0 = self.last
        for i in range(1, self.n + 1):
            t = i / self.n; mt = 1 - t
            x = mt**3*p0[0] + 3*mt*mt*t*p1[0] + 3*mt*t*t*p2[0] + t**3*p3[0]
            y = mt**3*p0[1] + 3*mt*mt*t*p1[1] + 3*mt*t*t*p2[1] + t**3*p3[1]
            self.cur.append(self.xf((x, y)))
        self.last = p3
    def _closePath(self):
        if self.cur and len(self.cur) > 2:
            if self.cur[0] == self.cur[-1]: self.cur.pop()
            self.loops.append(self.cur)
        self.cur = None
    _endPath = _closePath

# items: dict(kind="glyph", font, ch, x, y, size, color) or mark
items = []
def place_text(font, text, x, y, size, color, ls=0.0, kt=None):
    prev = None
    for ch in text:
        g = gname(font, ch)
        if prev is not None and kt is not None:
            x += kern(font, kt, prev, g) / UPM * size
        items.append(dict(kind="glyph", font=font, ch=ch, x=x, y=y, size=size, color=color))
        x += adv(font, ch) * size + ls
        prev = g
    return x

# ---------- Lockup (em units, baseline y = 0, y up) ----------
LS = -0.03
x = place_text(SB, "o", 0, 0, 1, "ink", LS, KT_SB)
cx0 = x
x = place_text(SB, "pen-", x, 0, 1, "ink", LS, KT_SB)
x += 0.03
mark_x0 = x
items.append(dict(kind="mark", x0=x, y0=0.0, size=0.5))
x += 0.5 + 0.03
x = place_text(SB, "ra", x, 0, 1, "ink", LS, KT_SB)
W = x - cx0
# tagline
TS, TTOP, TL, TR = 0.19, -0.13, 0.2, 0.03
asc, desc = 0.984, 0.292
base1 = (1 - (asc + desc)) / 2 + asc                   # 0.846
tag_base_from_top = 1 + TTOP + TS * base1
tag_y = -(tag_base_from_top - base1)
tag = "offener Reparatur-Assistent"
rx0, rx1 = cx0 + TL, cx0 + W - TR
advs = [adv(MD, c) * TS for c in tag]
gap = (rx1 - rx0 - sum(advs)) / (len(tag) - 1)
tx = rx0
for c, a in zip(tag, advs):
    if c != " ":
        items.append(dict(kind="glyph", font=MD, ch=c, x=tx, y=tag_y, size=TS, color="tag"))
    tx += a + gap
print("W", round(W, 4), "cx0", round(cx0, 4), "tag_y", round(tag_y, 4), "gap", round(gap, 4), "tag natural", round(sum(advs), 3), "region", round(rx1 - rx0, 3))

# ---------- Mark geometry (in em) ----------
def mark_loops(m, n=96):
    s = m["size"] / 94.0
    cx, cy = m["x0"] + (60 - 13) * s, m["y0"] + (107 - 60) * s   # svg y down: ring centre 60, bottom 107
    a0, a1 = math.radians(25), math.radians(335)
    ring = []
    for i in range(n + 1):
        t = a0 + (a1 - a0) * i / n
        ring.append((cx + 47 * s * math.cos(t), cy - 47 * s * math.sin(t)))
    for i in range(n + 1):
        t = a1 - (a1 - a0) * i / n
        ring.append((cx + 33 * s * math.cos(t), cy - 33 * s * math.sin(t)))
    x0, x1, hw = cx + 16 * s, cx + 44 * s, 3 * s
    probe = []
    for i in range(17):
        t = math.pi / 2 - math.pi * i / 16
        probe.append((x1 + hw * math.cos(t), cy + hw * math.sin(t)))
    for i in range(17):
        t = -math.pi / 2 - math.pi * i / 16
        probe.append((x0 + hw * math.cos(t), cy + hw * math.sin(t)))
    dot = [(cx + 12 * s * math.cos(2 * math.pi * i / 64), cy + 12 * s * math.sin(2 * math.pi * i / 64)) for i in range(64)]
    return [("ink", [ring]), ("ink", [probe]), ("accent", [dot])], (cx, cy, s)

def glyph_loops(it):
    gs = it["font"].getGlyphSet()
    k = it["size"] / UPM
    pen = FlatPen(gs, lambda p: (it["x"] + p[0] * k, it["y"] + p[1] * k))
    gs[gname(it["font"], it["ch"])].draw(pen)
    return pen.loops

def glyph_svgpath(it, X, Y, S):
    gs = it["font"].getGlyphSet()
    k = it["size"] / UPM
    pen = SVGPathPen(gs)
    tp = TransformPen(pen, (k * S, 0, 0, -k * S, X(it["x"]), Y(it["y"])))
    gs[gname(it["font"], it["ch"])].draw(tp)
    return pen.getCommands()

# ---------- geometry JSON (for FreeCAD) ----------
def build_geometry(its):
    out = []
    for it in its:
        if it["kind"] == "glyph":
            out.append({"color": it["color"], "loops": [[[round(a, 5), round(b, 5)] for a, b in l] for l in glyph_loops(it)]})
        else:
            for col, loops in mark_loops(it)[0]:
                out.append({"color": col, "loops": [[[round(a, 5), round(b, 5)] for a, b in l] for l in loops]})
    return out

allpts = [p for g in build_geometry(items) for l in g["loops"] for p in l]
bb = (min(p[0] for p in allpts), min(p[1] for p in allpts), max(p[0] for p in allpts), max(p[1] for p in allpts))
print("bbox em", [round(v, 4) for v in bb])

url_items = []
_save = items; items = url_items
ux = place_text(MD, "open-ora.de", 0, 0, 1, "url", 0.0, kern_table(MD))
items = _save
geo = {"units": "em (Schriftgroesse 1), Grundlinie y=0, y nach oben",
       "lockup": {"bbox": bb, "baseline": 0.0, "faces": build_geometry(items)},
       "url": {"advance": ux, "faces": build_geometry(url_items)}}
ub = [p for g in geo["url"]["faces"] for l in g["loops"] for p in l]
geo["url"]["bbox"] = (min(p[0] for p in ub), min(p[1] for p in ub), max(p[0] for p in ub), max(p[1] for p in ub))
json.dump(geo, open(os.path.join(OUT, "logo_geometry.json"), "w"))

# ---------- SVG ----------
INK, LIGHT, ACC = "#16181B", "#F4F2EE", "#E8743B"
def svg(colors, bg=None, pad=0.12, with_url=False, name="x.svg"):
    S = 100.0
    x0, y0, x1, y1 = bb
    extra = 0
    if with_url:
        extra = 0.42
    w = (x1 - x0 + 2 * pad) * S; h = (y1 - y0 + 2 * pad + extra) * S
    X = lambda ex: (ex - x0 + pad) * S
    Y = lambda ey: (y1 - ey + pad) * S
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:.1f} {h:.1f}" width="{w:.0f}" height="{h:.0f}" role="img" aria-label="open-ora – offener Reparatur-Assistent">']
    if bg: parts.append(f'<rect width="100%" height="100%" fill="{bg}"/>')
    paths = {}
    for it in items:
        if it["kind"] == "glyph":
            paths.setdefault(it["color"], []).append(glyph_svgpath(it, X, Y, S))
    for col, ds in paths.items():
        parts.append(f'<path fill="{colors[col]}" d="{" ".join(ds)}"/>')
    m = [i for i in items if i["kind"] == "mark"][0]
    _, (cx, cy, s) = mark_loops(m)
    k = s * S
    parts.append(f'<g transform="translate({X(cx) - 60 * k:.3f} {Y(cy) - 60 * k:.3f}) scale({k:.5f})"><path d="M96.25 76.9 A40 40 0 1 1 96.25 43.1" fill="none" stroke="{colors["ink"]}" stroke-width="14"/><line x1="76" y1="60" x2="104" y2="60" stroke="{colors["ink"]}" stroke-width="6" stroke-linecap="round"/><circle cx="60" cy="60" r="12" fill="{colors["accent"]}"/></g>')
    if with_url:
        uw = (geo["url"]["bbox"][2]) * 0.16
        ux0 = (x0 + x1) / 2 - uw / 2
        for it in url_items:
            it2 = dict(it); it2["x"] = ux0 + it["x"] * 0.16; it2["size"] = 0.16; it2["y"] = y0 - 0.30
            parts.append(f'<path fill="{colors["ink"]}" d="{glyph_svgpath(it2, X, Y, S)}"/>')
    parts.append("</svg>")
    open(os.path.join(OUT, name), "w").write("\n".join(parts))

svg({"ink": INK, "tag": "#5B5E63", "accent": ACC}, None, name="open-ora-logo.svg")
svg({"ink": LIGHT, "tag": "#C9C6C0", "accent": ACC}, None, name="open-ora-logo-hell.svg")
svg({"ink": LIGHT, "tag": "#C9C6C0", "accent": ACC}, INK, name="open-ora-logo-dunkel-mit-domain.svg", with_url=True)
