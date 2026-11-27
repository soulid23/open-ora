# open-ora | cad/macros/tisch_4080_motedis.py | v1 (Leichttisch 4080 mit Motedis-Teilen, abgeleitet von tisch_4080.py v2)
# Gleiche Geometrie wie tisch_4080.py (oberer Rahmen 4080 flach, Tischhoehe 780 mm), aber mit Teilen von motedis.com:
#   Profile 40x40L und 40x80L I-Typ Nut 8 mit ECHTEM Querschnitt aus den Motedis-STEP-Dateien,
#   Winkel 40 I-Typ Nut 8 (S8IBR40) als echtes STEP-Teil an jeder Winkelstelle (Zentrierstege in der Nut),
#   Stueckliste mit Motedis-Teilen: bom/tisch_4080_motedis_bom.csv
# Profilenden: Motedis-Option "I-SSV 90 Grad (I-Typ), montiert" statt Alux-Zentralverbinder.
# STEP-Dateien (nicht im Repo, Herstellerdaten) unter ASSETS; Quelle: motedis.com, Produktseiten -> Dateien:
#   P40L_N8_I.stp (40x40L I-Type slot 8.zip), Motedis_Profile 40x80L I-Type slot 8.stp, Motedis_S8IBR40.stp
# Fehlen sie, baut das Makro mit Quadern und Platzhalter-Winkeln wie tisch_4080.py.
# Start in FreeCAD: exec(open(r"C:\dev\open-ora\cad\macros\tisch_4080_motedis.py", encoding="utf-8").read())

import os
import csv
import FreeCAD as App
import Part
from FreeCAD import Vector as V

REPO = r"C:\dev\open-ora"
DOC_NAME = "OpenORA_Tisch4080_Motedis"
ASSETS = r"C:\dev\open-ora-assets\motedis"
KG_M = {"4080": 3.059, "4040": 1.774}          # aus den STEP-Querschnitten (Dichte 2,70)
I_MM4 = {"4080": (169448.0, 701672.0), "4040": (92642.0, 92642.0)}   # Motedis 40x80L / 40x40L (STEP)
I_ALUX = {"4080": (148277.0, 587887.0), "4040": (75648.0, 75648.0)}

# ---------------- Parameter (mm) ----------------
P, T = 40.0, 80.0                 # 4040 / 8080
W = D = 1000.0
PLATE, ESD_T = 18.0, 2.0
Z_UP0, Z_UP1 = 720.0, 760.0       # oberer Rahmen 4080 flach, Oberkante 760 wie beim 8080-Tisch; Beine 40 mm laenger
DESK_H = Z_UP1 + PLATE + ESD_T    # 780
FOOT_STACK = 50.0                 # Fussbauhoehe (Platzhalter, wie v12)
RACK_CLEAR = 3 * 44.45 + 1.05     # 134,4
Z_LOW1 = Z_UP0 - RACK_CLEAR       # 545,6 Oberkante unterer Rahmen
Z_LOW0 = Z_LOW1 - P               # 505,6
BRACE_Z0 = 100.0
MID_Y = 620.0                     # feste Querstrebe (Mitte), oben 4080 hochkant, unten 4040
PLATE_INSET = 40.0                # Platte endet in der Mitte des 8080 -> aeussere Nutreihe bleibt frei
PLATE_W = W - 2 * PLATE_INSET     # 920
ESD_MARGIN = 10.0
# Rackkasten
BOX_T = 15.0                      # Multiplex Birke 15 mm
BOX_IN = 490.0                    # Holzinnenmass fuer Adam Hall 61535 (19")
BOX_Y0, BOX_Y1 = MID_Y - P / 2, D # 600 .. 1000
RAIL_W, RAIL_D, RAIL_T = 21.0, 30.0, 2.0   # Adam Hall 61535 (Breite 30, Tiefe 21): Lochflaeche 21 mm, Schenkel 30 mm an der Wand -> lichte Weite 448 mm
RAIL_L = 3 * 44.45                # 3 HE
REAR_RAIL_Y = 620.0               # Lochebene der hinteren (inneren) Schienen -> Einbautiefe 380 mm
BR_T = 4.0                        # Winkel-Platzhalter: Wandstaerke
# Eckstreben (wie v12)
KNEE_A, KNEE_TRIM = 250.0, 35.0
# Forex
FOREX_T, SLOT_INS = 5.0, 8.0
PRENUT_Y = (200.0, 420.0, 820.0)  # weitere Strebenplaetze (Vor-Nutensteine), 620 ist die feste Querstrebe
# Bohrbild Platte (Tischkoordinaten, Lochmitte = Nutmitte der inneren Reihe)
ROW_IN = T - 20.0                 # 60: innere Nutreihe des 8080
HOLES_X = (60, 200, 340, 500, 660, 800, 940)          # vordere und hintere Reihe
HOLES_SIDE_Y = (180, 320, 460, 620, 780)               # Seitenreihen
HOLES_MID_X = (200, 340, 500, 660, 800)                # auf der Querstrebe (y = 620)

if DOC_NAME in App.listDocuments():
    App.closeDocument(DOC_NAME)
doc = App.newDocument(DOC_NAME)


def _lade(name):
    p = os.path.join(ASSETS, name)
    return Part.read(p) if os.path.exists(p) else None


def _querschnitt(step):
    """Querschnitt eines Profil-STEP als Flaeche in der XY-Ebene, linke untere Ecke auf (0,0)."""
    if step is None:
        return None
    bb = step.BoundBox
    z = bb.ZMin + bb.ZLength / 2
    box = Part.makeBox(bb.XLength + 2, bb.YLength + 2, 0.5, V(bb.XMin - 1, bb.YMin - 1, z))
    sl = step.common(box)
    f = [x for x in sl.Faces if abs(x.normalAt(0, 0).z) > 0.99 and abs(x.CenterOfMass.z - z) < 1e-3]
    f = f[0] if len(f) == 1 else Part.makeCompound(f)
    f = f.copy(); f.translate(V(-bb.XMin, -bb.YMin, -z))
    return f


SEC = {"4040": _querschnitt(_lade("P40L_N8_I.stp")), "4080": _querschnitt(_lade("Motedis_Profile 40x80L I-Type slot 8.stp"))}
ANGLE40 = _lade("Motedis_S8IBR40.stp")
ECHT = all(v is not None for v in SEC.values()) and ANGLE40 is not None
print("Motedis-STEP gefunden:" if ECHT else "Motedis-STEP fehlen, Quader-Modell:", ASSETS)

parts = {}      # Name -> dict(shape, kind, group)
groups = {}
COL = {"8080": (0.93, 0.55, 0.17), "4080": (0.95, 0.70, 0.25), "4040": (0.76, 0.78, 0.80),
       "winkel": (0.30, 0.30, 0.33), "platte": (0.55, 0.40, 0.25), "esd": (0.20, 0.45, 0.75),
       "kasten": (0.85, 0.72, 0.52), "schiene": (0.10, 0.10, 0.10), "forex": (0.09, 0.09, 0.11),
       "fuss": (0.1, 0.1, 0.1), "nut": (0.85, 0.60, 0.10), "geraet": (0.18, 0.18, 0.20)}


def grp(name):
    if name not in groups:
        groups[name] = doc.addObject("App::DocumentObjectGroup", name)
    return groups[name]


def add(name, shape, kind, group, transp=0, check=True):
    o = doc.addObject("Part::Feature", name)
    o.Shape = shape
    try:
        o.ViewObject.ShapeColor = COL[kind]
        o.ViewObject.Transparency = transp
    except Exception:
        pass
    grp(group).addObject(o)
    parts[name] = dict(shape=shape, kind=kind, group=group, check=check, obj=o)
    return o


def grooves(x0, y0, z0, dx, dy, dz):
    """Angedeutete 8-mm-Nuten (3 mm tief) im 40er-Raster auf den vier Laengsflaechen."""
    dims = [dx, dy, dz]
    ax = dims.index(max(dims))
    L = dims[ax]
    o = [x0, y0, z0]
    cuts = []
    others = [i for i in range(3) if i != ax]
    for i in others:
        j = [k for k in others if k != i][0]
        for side in (0, 1):
            n = int(round(dims[j] / 40.0))
            for k in range(n):
                c = o[j] + 20 + 40 * k
                pos = [0, 0, 0]
                size = [0, 0, 0]
                pos[ax], size[ax] = o[ax] - 1, L + 2
                pos[j], size[j] = c - 4, 8
                pos[i] = o[i] - 0.01 if side == 0 else o[i] + dims[i] - 3
                size[i] = 3.01
                cuts.append(Part.makeBox(size[0], size[1], size[2], V(*pos)))
    return cuts


def echt_profil(kind, x0, y0, z0, dx, dy, dz):
    """Echter Motedis-Querschnitt, auf den Quader (x0, y0, z0, dx, dy, dz) gelegt."""
    sec = SEC.get(kind)
    if sec is None:
        return None
    dims = [dx, dy, dz]
    ax = dims.index(max(dims))
    c1, c2 = [i for i in range(3) if i != ax]
    sw, sh = sec.BoundBox.XLength, sec.BoundBox.YLength
    if abs(dims[c1] - sw) > 0.5:          # Querschnitt um 90 Grad drehen
        c1, c2 = c2, c1
    e = [V(1, 0, 0), V(0, 1, 0), V(0, 0, 1)]
    ex, ey, ez = e[c1], e[c2], e[ax]
    org = V(x0, y0, z0)
    if ex.cross(ey).dot(ez) < 0:          # rechtshaendig halten (Querschnitt ist symmetrisch)
        org = org + ey * dims[c2]
        ey = ey * -1
    sol = sec.extrude(V(0, 0, dims[ax]))
    m = App.Matrix(ex.x, ey.x, ez.x, org.x, ex.y, ey.y, ez.y, org.y, ex.z, ey.z, ez.z, org.z, 0, 0, 0, 1)
    return _place(sol, m)


def _place(sol, m):
    s = sol.copy()
    s.transformShape(m)
    return s


def profile(name, kind, x0, y0, z0, dx, dy, dz, group="Rahmen"):
    s = Part.makeBox(dx, dy, dz, V(x0, y0, z0))
    real = echt_profil(kind, x0, y0, z0, dx, dy, dz) if ECHT else None
    disp = real
    if disp is None:
        disp = s
        for c in grooves(x0, y0, z0, dx, dy, dz):
            disp = disp.cut(c)
    o = add(name, disp, kind, group)
    parts[name]["shape"] = real if real is not None else s   # Pruefung mit echtem Profil (Nuten offen)
    parts[name]["L"] = max(dx, dy, dz)
    return o


def bracket(name, O, a, b, w, leg=40.0, width=36.0, t=BR_T, kind="winkel", joins=()):
    """L-Winkel in einer Innenecke. O = Eckpunkt; a, b = Schenkelrichtungen (Achsen, +-1);
    w = Breitenrichtung (mittig um O). Schenkel a liegt auf der Flaeche mit Normale b und umgekehrt."""
    O, a, b, w = V(*O), V(*a), V(*b), V(*w)
    def box(p0, p1):
        lo = V(min(p0.x, p1.x), min(p0.y, p1.y), min(p0.z, p1.z))
        hi = V(max(p0.x, p1.x), max(p0.y, p1.y), max(p0.z, p1.z))
        return Part.makeBox(hi.x - lo.x, hi.y - lo.y, hi.z - lo.z, lo)
    if ECHT:
        # Motedis-Winkel 40 (S8IBR40): im STEP liegt Schenkel a auf -x, Schenkel b auf +y, Breite auf z
        ex, ey, ez = a * -1, b, w
        if ex.cross(ey).dot(ez) < 0:
            ez = ez * -1
        m = App.Matrix(ex.x, ey.x, ez.x, O.x, ex.y, ey.y, ez.y, O.y, ex.z, ey.z, ez.z, O.z, 0, 0, 0, 1)
        o = add(name, _place(ANGLE40, m), kind, "Verbinder")
    else:
        p1 = box(O - w * (width / 2), O + a * leg + b * t + w * (width / 2))
        p2 = box(O - w * (width / 2), O + a * t + b * leg + w * (width / 2))
        o = add(name, p1.fuse(p2).removeSplitter(), kind, "Verbinder")
    parts[name]["joins"] = joins
    return o


# ---------------- Rahmen ----------------
legs = {"LV": (0, 0, +1, +1), "RV": (W - P, 0, -1, +1), "LH": (0, D - P, +1, -1), "RH": (W - P, D - P, -1, -1)}
for n, (x, y, sx, sy) in legs.items():
    profile("Bein_%s" % n, "4040", x, y, FOOT_STACK, P, P, Z_UP0 - FOOT_STACK)
    f = Part.makeCylinder(40, 12, V(x + 20, y + 20, 0)).fuse(Part.makeCylinder(12, 8, V(x + 20, y + 20, 12))) \
        .fuse(Part.makeCylinder(4, FOOT_STACK - 20, V(x + 20, y + 20, 20)))
    add("Fuss_%s" % n, f, "fuss", "Rahmen")

# oberer Rahmen 4080 flach (80 breit, 40 hoch): zwei Nutreihen oben, zwei unten
profile("X4080_vorn", "4080", 0, 0, Z_UP0, W, T, P)
profile("X4080_hinten", "4080", 0, D - T, Z_UP0, W, T, P)
profile("Y4080_links", "4080", 0, T, Z_UP0, T, D - 2 * T, P)
profile("Y4080_rechts", "4080", W - T, T, Z_UP0, T, D - 2 * T, P)
# feste Querstrebe oben: 4040 flach, buendig mit Ober- und Unterkante des Rahmens
profile("Querstrebe_oben_4040", "4040", T, MID_Y - P / 2, Z_UP0, W - 2 * T, P, P)

# unterer Rahmen 4040 (vorn offen)
profile("X_unten_hinten", "4040", P, D - P, Z_LOW0, W - 2 * P, P, P)
profile("Y_unten_links", "4040", 0, P, Z_LOW0, P, D - 2 * P, P)
profile("Y_unten_rechts", "4040", W - P, P, Z_LOW0, P, D - 2 * P, P)
profile("Querstrebe_unten_4040", "4040", P, MID_Y - P / 2, Z_LOW0, W - 2 * P, P, P)
# Bodenstreben
profile("X_boden_hinten", "4040", P, D - P, BRACE_Z0, W - 2 * P, P, P)
profile("Y_boden_links", "4040", 0, P, BRACE_Z0, P, D - 2 * P, P)
profile("Y_boden_rechts", "4040", W - P, P, BRACE_Z0, P, D - 2 * P, P)

# Eckstreben 45 Grad (4040) unter dem unteren Rahmen, wie v12
knees = []
def knee(name, wall, hp, sh):
    base = {"links": (0.0, "x"), "rechts": (W - P, "x"), "hinten": (D - P, "y")}[wall]
    def to3(h, z):
        return V(base[0], h, z) if base[1] == "x" else V(h, base[0], z)
    nrm = V(1, 0, 0) if base[1] == "x" else V(0, 1, 0)
    f_post, f_beam = (hp, Z_LOW0 - KNEE_A), (hp + sh * KNEE_A, Z_LOW0)
    dv = (f_beam[0] - f_post[0], f_beam[1] - f_post[1]); ln = (dv[0] ** 2 + dv[1] ** 2) ** 0.5
    d = (dv[0] / ln, dv[1] / ln)
    e1 = (f_post[0] + d[0] * KNEE_TRIM, f_post[1] + d[1] * KNEE_TRIM)
    e2 = (f_beam[0] - d[0] * KNEE_TRIM, f_beam[1] - d[1] * KNEE_TRIM)
    L = ((e2[0] - e1[0]) ** 2 + (e2[1] - e1[1]) ** 2) ** 0.5
    p1 = to3(*e1) + nrm * (P / 2)
    ax = to3(*e2) + nrm * (P / 2) - p1; ax.normalize()
    s = Part.makeBox(P, P, L, V(-P / 2, -P / 2, 0))
    s.Placement = App.Placement(p1, App.Rotation(V(0, 0, 1), ax))
    add(name, s, "4040", "Rahmen"); parts[name]["L"] = L
    knees.append(L)
    # Verbinder 4040-45 (Platzhalter-Keil wie v12)
    n_ = (-d[1], d[0])
    for tag, end, face in (("Bein", e1, lambda v: (hp, v[1] - (v[0] - hp) * d[1] / d[0])),
                           ("Traeger", e2, lambda v: (v[0] + (Z_LOW0 - v[1]) * d[0] / d[1], Z_LOW0))):
        pts2 = [(end[0] + s_ * n_[0] * P / 2, end[1] + s_ * n_[1] * P / 2) for s_ in (+1, -1)]
        pts2 += [face(v) for v in reversed(pts2)]
        pts = [to3(*q) for q in pts2]; pts.append(pts[0])
        add("V45_%s_%s" % (name, tag), Part.Face(Part.makePolygon(pts)).extrude(nrm * P), "winkel", "Verbinder")
knee("Eckstrebe_links_vorn", "links", P, +1)
knee("Eckstrebe_links_hinten", "links", D - P, -1)
knee("Eckstrebe_rechts_vorn", "rechts", P, +1)
knee("Eckstrebe_rechts_hinten", "rechts", D - P, -1)
knee("Eckstrebe_hinten_links", "hinten", P, +1)
knee("Eckstrebe_hinten_rechts", "hinten", W - P, -1)

# ---------------- Verbinder ----------------
cv = []   # Zentralverbinder (Profil-Option "Bearbeitung + Zentralverbinder"): (Profil, Ende, Anzahl, Ziel)
# Beine oben: 2 Winkel 4040 unter dem 4080 (beide unteren Nutreihen) + Zentralverbinder in die aeussere untere Nut
for n, (x, y, sx, sy) in legs.items():
    cx, cy = x + 20, y + 20
    xb = "X4080_vorn" if n in ("LV", "RV") else "X4080_hinten"
    bracket("W4040_Bein_%s_x" % n, (cx + sx * 20, cy, Z_UP0), (sx, 0, 0), (0, 0, -1), (0, 1, 0), joins=("Bein_" + n, xb))
    bracket("W4040_Bein_%s_y" % n, (cx, cy + sy * 20, Z_UP0), (0, sy, 0), (0, 0, -1), (1, 0, 0), joins=("Bein_" + n, xb))
    cv.append(("Bein_" + n, "oben", 1, xb))
# 4080 Seitenholm an 4080 vorn/hinten: 2 Zentralverbinder je Ende + Winkel 4040 in der Innenecke (Innenflaeche ist 40 hoch, eine Nut)
for side, x0, sx in (("links", T, +1), ("rechts", W - T, -1)):
    for end, y0, sy, xb in (("vorn", T, +1, "X4080_vorn"), ("hinten", D - T, -1, "X4080_hinten")):
        bracket("W4040_Eck_%s_%s" % (side, end), (x0, y0, Z_UP0 + P / 2), (sx, 0, 0), (0, sy, 0), (0, 0, 1),
                leg=40.0, width=36.0, t=5.0, joins=("Y4080_" + side, xb))
        cv.append(("Y4080_" + side, end, 2, xb))
# Querstrebe oben (4040) an die Seitenholme: 1 Zentralverbinder je Ende + je ein Winkel 4040 vorn und hinten
for side, x0, sx in (("links", T, +1), ("rechts", W - T, -1)):
    for face, y0, sy in (("vorn", MID_Y - P / 2, -1), ("hinten", MID_Y + P / 2, +1)):
        bracket("W4040_Quer_%s_%s" % (side, face), (x0, y0, Z_UP0 + P / 2), (sx, 0, 0), (0, sy, 0), (0, 0, 1),
                leg=36.0, width=36.0, t=5.0, joins=("Querstrebe_oben_4040", "Y4080_" + side))
    cv.append(("Querstrebe_oben_4040", side, 1, "Y4080_" + side))

# unterer Rahmen: Zentralverbinder + Winkel unter dem Traeger (oben liegt die Forex-Nut)
for side, x, xs in (("links", 0, "LV"), ("rechts", W - P, "RV")):
    for end, yy, sy, leg_ in (("vorn", P, +1, xs), ("hinten", D - P, -1, xs.replace("V", "H"))):
        bracket("W4040_Yu_%s_%s" % (side, end), (x + 20, yy, Z_LOW0), (0, sy, 0), (0, 0, -1), (1, 0, 0),
                joins=("Y_unten_" + side, "Bein_" + leg_))
        cv.append(("Y_unten_" + side, end, 1, "Bein_" + leg_))
for end, xx, sx, leg_ in (("links", P, +1, "LH"), ("rechts", W - P, -1, "RH")):
    bracket("W4040_Xu_hinten_%s" % end, (xx, D - 20, Z_LOW0), (sx, 0, 0), (0, 0, -1), (0, 1, 0),
            joins=("X_unten_hinten", "Bein_" + leg_))
    cv.append(("X_unten_hinten", end, 1, "Bein_" + leg_))
    side = "links" if end == "links" else "rechts"
    # Winkel auf Stirn- und Rueckseite der Querstrebe (Flaechen y = 600 / 640), Schraube in die Innenflaeche des Y_unten
    for face, y0, sy in (("vorn", MID_Y - P / 2, -1), ("hinten", MID_Y + P / 2, +1)):
        bracket("W4040_Qu_%s_%s" % (end, face), (xx, y0, Z_LOW0 + P / 2), (sx, 0, 0), (0, sy, 0), (0, 0, 1),
                leg=36.0, width=36.0, t=5.0, joins=("Querstrebe_unten_4040", "Y_unten_" + side))
    cv.append(("Querstrebe_unten_4040", end, 1, "Y_unten_" + side))
# Bodenstreben: Zentralverbinder + Winkel oben
for side, x, xs in (("links", 0, "LV"), ("rechts", W - P, "RV")):
    for end, yy, sy, leg_ in (("vorn", P, +1, xs), ("hinten", D - P, -1, xs.replace("V", "H"))):
        bracket("W4040_Yb_%s_%s" % (side, end), (x + 20, yy, BRACE_Z0 + P), (0, sy, 0), (0, 0, 1), (1, 0, 0),
                joins=("Y_boden_" + side, "Bein_" + leg_))
        cv.append(("Y_boden_" + side, end, 1, "Bein_" + leg_))
for end, xx, sx, leg_ in (("links", P, +1, "LH"), ("rechts", W - P, -1, "RH")):
    bracket("W4040_Xb_hinten_%s" % end, (xx, D - 20, BRACE_Z0 + P), (sx, 0, 0), (0, 0, 1), (0, 1, 0),
            joins=("X_boden_hinten", "Bein_" + leg_))
    cv.append(("X_boden_hinten", end, 1, "Bein_" + leg_))

# Vor-Nutensteine (Innenseite der 8080-Seitenholme, beide Reihen) fuer weitere Streben
prenuts = 0
for side, xf, sx in (("links", T, -1), ("rechts", W - T, +1)):
    for yc in PRENUT_Y:
        for zc in (Z_UP0 + 20,):
            b = Part.makeBox(4, 14, 10, V(xf + (0 if sx > 0 else -4) + sx * 4, yc - 7, zc - 5))
            add("Vornut_%s_%d_%d" % (side, yc, zc), b, "nut", "Vor-Nutensteine", check=False)
            prenuts += 1

# ---------------- Platte, ESD ----------------
plate = Part.makeBox(PLATE_W, PLATE_W, PLATE, V(PLATE_INSET, PLATE_INSET, Z_UP1))
holes = [(x, ROW_IN) for x in HOLES_X] + [(x, D - ROW_IN) for x in HOLES_X] + \
        [(ROW_IN, y) for y in HOLES_SIDE_Y] + [(W - ROW_IN, y) for y in HOLES_SIDE_Y] + \
        [(x, MID_Y) for x in HOLES_MID_X]
for (hx, hy) in holes:
    plate = plate.cut(Part.makeCylinder(3.3, PLATE + 2, V(hx, hy, Z_UP1 - 1)))
    plate = plate.cut(Part.makeCone(3.3, 6.6, 3.3, V(hx, hy, Z_UP1 + PLATE - 3.3), V(0, 0, 1)))   # Senkung 90 Grad, Durchmesser 13,2
add("Siebdruckplatte_18", plate, "platte", "Platte", transp=30)
add("ESD_Matte", Part.makeBox(PLATE_W - 2 * ESD_MARGIN, PLATE_W - 2 * ESD_MARGIN, ESD_T,
                              V(PLATE_INSET + ESD_MARGIN, PLATE_INSET + ESD_MARGIN, Z_UP1 + PLATE)), "esd", "Platte", transp=40)

# ---------------- Rackkasten ----------------
xin0, xin1 = W / 2 - BOX_IN / 2, W / 2 + BOX_IN / 2      # 255 / 745
for side, x0 in (("links", xin0 - BOX_T), ("rechts", xin1)):
    add("Kasten_Wand_%s" % side, Part.makeBox(BOX_T, BOX_Y1 - BOX_Y0, RACK_CLEAR - 0.4, V(x0, BOX_Y0, Z_LOW1 + 0.2)),
        "kasten", "Rackkasten")
# Winkel aussen an den Waenden: oben/unten, vorn (Querstreben) und hinten (8080 / X_unten_hinten)
for side, xw, sx in (("links", xin0 - BOX_T, -1), ("rechts", xin1 + BOX_T, +1)):
    for end, yc in (("vorn", MID_Y), ("hinten", D - 20)):
        top = "Querstrebe_oben_4040" if end == "vorn" else "X4080_hinten"
        bot = "Querstrebe_unten_4040" if end == "vorn" else "X_unten_hinten"
        bracket("WK_%s_%s_oben" % (side, end), (xw, yc, Z_UP0), (sx, 0, 0), (0, 0, -1), (0, 1, 0),
                joins=("Kasten_Wand_" + side, top))
        bracket("WK_%s_%s_unten" % (side, end), (xw, yc, Z_LOW1), (sx, 0, 0), (0, 0, 1), (0, 1, 0),
                joins=("Kasten_Wand_" + side, bot))
# 19"-Schienen Adam Hall 61535 (L-Profil): Lochflaeche 21 x 2, Schenkel 30 an der Wand (Annahme, gegen Teil pruefen)
z_r = Z_LOW1 + (RACK_CLEAR - RAIL_L) / 2
def rail(name, x_wall, sx, y_face, sy):
    xa, xb = (x_wall, x_wall + RAIL_W) if sx > 0 else (x_wall - RAIL_W, x_wall)
    face = Part.makeBox(RAIL_W, RAIL_T, RAIL_L, V(xa, y_face - (RAIL_T if sy > 0 else 0), z_r))
    ya, yb = (y_face - RAIL_D, y_face) if sy > 0 else (y_face, y_face + RAIL_D)
    xl = x_wall if sx > 0 else x_wall - RAIL_T
    legp = Part.makeBox(RAIL_T, yb - ya, RAIL_L, V(xl, ya, z_r))
    add(name, face.fuse(legp).removeSplitter(), "schiene", "Rackkasten")
rail("Schiene_hinten_links", xin0, +1, D, +1)
rail("Schiene_hinten_rechts", xin1, -1, D, +1)
rail("Schiene_innen_links", xin0, +1, REAR_RAIL_Y, -1)
rail("Schiene_innen_rechts", xin1, -1, REAR_RAIL_Y, -1)
# Geraete-Platzhalter: Auszugboden 1 HE (87556) unten, D12-Blende 3. HE (wie v12)
add("Geraet_U1_Auszug_87556", Part.makeBox(484, 1.6, 44.5, V(W / 2 - 242, D, z_r)).fuse(
    Part.makeBox(435, D - REAR_RAIL_Y, 40, V(W / 2 - 217.5, REAR_RAIL_Y, z_r + 2))), "geraet", "Rackkasten")
add("Geraet_U3_D12_872215", Part.makeBox(484, 1.5, 44.5, V(W / 2 - 242, D, z_r + 2 * 44.45)), "geraet", "Rackkasten")

# ---------------- Forex (in der 8-mm-Nut, wie v12, neue Ausklinkungen) ----------------
zf0, zf1 = Z_LOW1 - SLOT_INS, Z_UP0 + SLOT_INS
NOTCH = 52.0      # Ausklinkung an den oberen Ecken: Platz fuer die Bein-Winkel und den kreuzenden 8080
forex = []
for side, xm in (("links", 20.0), ("rechts", W - 20.0)):
    y0, y1 = P - SLOT_INS, D - P + SLOT_INS
    s = Part.makeBox(FOREX_T, y1 - y0, zf1 - zf0, V(xm - FOREX_T / 2, y0, zf0))
    s = s.cut(Part.makeBox(FOREX_T + 2, NOTCH + 4, NOTCH, V(xm - FOREX_T / 2 - 1, y0 - 2, zf1 - NOTCH)))
    s = s.cut(Part.makeBox(FOREX_T + 2, NOTCH + 4, NOTCH, V(xm - FOREX_T / 2 - 1, y1 - NOTCH - 2, zf1 - NOTCH)))
    add("Forex_Seite_%s" % side, s, "forex", "Forex"); forex.append(("Forex_Seite_%s" % side, y1 - y0, zf1 - zf0))
ym = D - 20.0
for side, (xa, xb) in (("links", (P - SLOT_INS, xin0 - BOX_T - 40)), ("rechts", (xin1 + BOX_T + 40, W - P + SLOT_INS))):
    # endet 40 mm vor der Kastenwand: dort sitzen die Kastenwinkel auf den hinteren Traegern
    s = Part.makeBox(xb - xa, FOREX_T, zf1 - zf0, V(xa, ym - FOREX_T / 2, zf0))
    cx = xa - 2 if side == "links" else xb - NOTCH - 2
    s = s.cut(Part.makeBox(NOTCH + 4, FOREX_T + 2, NOTCH, V(cx, ym - FOREX_T / 2 - 1, zf1 - NOTCH)))
    add("Forex_Rueck_%s" % side, s, "forex", "Forex"); forex.append(("Forex_Rueck_%s" % side, xb - xa, zf1 - zf0))

doc.recompute()

# ---------------- Pruefung ----------------
SLOT_OK = ("Forex",)           # Forex steckt planmaessig in der Nut der Profile
names = [n for n, p in parts.items() if p["check"]]
clash = []
for i, a in enumerate(names):
    sa = parts[a]["shape"]
    for b in names[i + 1:]:
        sb = parts[b]["shape"]
        if not sa.BoundBox.intersect(sb.BoundBox):
            continue
        v = sa.common(sb).Volume
        if v > 1.0:
            fa, fb = parts[a]["group"], parts[b]["group"]
            kind = "Nut (geplant)" if ("Forex" in (fa, fb) and ("Rahmen" in (fa, fb))) else "KOLLISION"
            wk = a if a.startswith(("W4040_", "WK_")) else b if b.startswith(("W4040_", "WK_")) else None
            if kind == "KOLLISION" and ECHT and wk and v < 150:
                kind = "Zentriersteg"   # Steg des Motedis-Winkels liegt nicht in einer Nut
            
            clash.append((kind, a, b, v))
real = [c for c in clash if c[0] == "KOLLISION"]
print("\n=== Ueberschneidungen ===")
for c in real:
    print("KOLLISION  %-28s %-28s %8.0f mm3" % (c[1], c[2], c[3]))
steg = [c for c in clash if c[0] == "Zentriersteg"]
slot = [c for c in clash if c[0] == "Nut (geplant)"]
for c in steg:
    print("STEG ABBRECHEN  %-28s an %s (%.0f mm3)" % (c[2] if c[2].startswith(("W4040_", "WK_")) else c[1],
          c[1] if c[2].startswith(("W4040_", "WK_")) else c[2], c[3]))
print("Kollisionen: %d | Zentriersteg abbrechen: %d | Forex in der Nut (geplant): %d" % (len(real), len(steg), len(slot)))
for c in slot:
    bb = parts[c[1]]["shape"].common(parts[c[2]]["shape"]).BoundBox
    depth = min(bb.XLength, bb.YLength, bb.ZLength)
    if depth > SLOT_INS + 0.1:
        print("  Forex tiefer als %.0f mm in der Nut: %s / %s (%.1f mm)" % (SLOT_INS, c[1], c[2], depth))
print("\n=== Kontakt der Winkel (Abstand zu beiden verbundenen Teilen) ===")
bad = 0
nbr = 0
for n, p in parts.items():
    if "joins" not in p:
        continue
    nbr += 1
    ds = [p["shape"].distToShape(parts[j]["shape"])[0] for j in p["joins"]]
    if max(ds) > 0.01:
        bad += 1
        print("OFFEN  %-30s %s" % (n, ", ".join("%s %.1f mm" % (j, d) for j, d in zip(p["joins"], ds))))
print("Winkel: %d, davon ohne Kontakt: %d" % (nbr, bad))

# ---------------- Stueckliste ----------------
cuts = {}
for n, p in parts.items():
    if p["kind"] in ("4080", "4040") and "L" in p:
        k = (p["kind"], round(p["L"], 1))
        cuts[k] = cuts.get(k, 0) + 1
kg = KG_M
mass = sum(kg[k] * L / 1000 * n for (k, L), n in cuts.items())
cnt = lambda pre: sum(1 for n in parts if n.startswith(pre))
cv_by = {}
for prof_, end, num, tgt in cv:
    kind = parts[prof_]["kind"]
    cv_by[kind] = cv_by.get(kind, 0) + 1
print("\n=== Zuschnitt ===")
for (k, L), n in sorted(cuts.items(), key=lambda kv: (kv[0][0], -kv[0][1])):
    print("  %s  %7.1f mm  x %d" % (k, L, n))
print("Profilmasse ca. %.1f kg | Tischhoehe %.0f mm | Platte %d x %d mm, %d Bohrungen" % (mass, DESK_H, PLATE_W, PLATE_W, len(holes)))
print("Winkel 4040: %d (davon Rackkasten %d) | Zentralverbinder-Enden: %s"
      % (cnt("W4040_") + cnt("WK_"), cnt("WK_"), cv_by))

# Durchbiegung (Einzellast 500 N in Feldmitte, beidseitig gelenkig, E = 70 000 N/mm2)
def durch(I, L, F=500.0):
    return F * L ** 3 / (48 * 70000.0 * I)
print("\n=== Durchbiegung 500 N Mitte, Motedis gegen Alux ===")
print("  4080 flach, Seitenholm 840 mm:  %.2f mm (Alux %.2f mm)" % (durch(I_MM4["4080"][0], 840), durch(I_ALUX["4080"][0], 840)))
print("  4080 flach, vorn/hinten 920 mm: %.2f mm (Alux %.2f mm)" % (durch(I_MM4["4080"][0], 920), durch(I_ALUX["4080"][0], 920)))
print("  4040 Querstrebe oben 840 mm:    %.2f mm (Alux %.2f mm)" % (durch(I_MM4["4040"][0], 840), durch(I_ALUX["4040"][0], 840)))

n_w = cnt("W4040_") + cnt("WK_")
n_45 = cnt("V45_")
rows = [["Pos", "Artikel", "Artikelnr", "Menge", "Einheit", "Bemerkung"]]
for (k, L), n in sorted(cuts.items(), key=lambda kv: (kv[0][0] != "4080", -kv[0][1])):
    nm_ = {"4080": "Aluprofil 40x80L I-Typ Nut 8", "4040": "Aluprofil 40x40L I-Typ Nut 8"}[k]
    rows.append([0, "%s, Zuschnitt %.1f mm" % (nm_, L), "Motedis", n, "Stk", "Laenge im Shop eintragen (50 bis 1980 mm)"])
rows += [
    [0, "Profilende-Option I-SSV 90 Grad (I-Typ), montiert", "Motedis, Option am 40x40L", cv_by.get("4040", 0), "Ende", "Beine oben, unterer Rahmen, Querstreben, Bodenstreben; ob eine Zugangsbohrung im Gegenprofil noetig ist, vor Bestellung klaeren"],
    [0, "Profilende-Option I-SSV 90 Grad (I-Typ), montiert, 2 je Ende", "Motedis, Option am 40x80L", cv_by.get("4080", 0), "Ende", "Seitenholme 40x80L an vorn/hinten"],
    [0, "Profilende-Option M8", "Motedis, Option am 40x40L", 4, "Ende", "Beine unten fuer die Fuesse"],
    [0, "Winkel 40 I-Typ Nut 8", "S8IBR40", n_w, "Stk", "Rahmen %d, Rackkasten %d; Zentrierstege abbrechen an den %d Kastenwinkeln (Holzseite) und am waagerechten Schenkel der 4 Bein-Winkel _y (quer zur Nut); 10er-Packungen" % (cnt("W4040_"), cnt("WK_"), cnt("WK_"))],
    [0, "Zylinderschraube DIN 912 M8x16", "DIN 912 M8x16", 2 * cnt("W4040_") + cnt("WK_") + n_45, "Stk", "2 je Winkel, 1 je Kastenwinkel, 1 je 45-Grad-Verbinder (Nut)"],
    [0, "Nutenstein mit Steg I-Typ Nut 8 M8", "S8ISMONM8", 2 * cnt("W4040_") + cnt("WK_") + n_45 + prenuts, "Stk", "Winkel, 45-Grad-Verbinder und %d vorab in die Seitenholme; 100er-Pack" % prenuts],
    [0, "Winkelverbinder 45 Grad 40 I-Typ Nut 8", "S8IALUCON45", n_45, "Stk", "Eckstreben; ohne Schrauben. Eckstrebenlaenge mit dem STEP pruefen (Makro nimmt Alux-Mass an)"],
    [0, "Zylinderschraube DIN 912 M8x30", "DIN 912 M8x30", n_45, "Stk", "Kernbefestigung 45-Grad-Verbinder"],
    [0, "Justierfuss D80 M8 L80", "Justierfuesse D80 M8 L80 WH", 4, "Stk", "4er-Pack; Gelenk und Traglast laut Datenblatt pruefen"],
    [0, "Siebdruckplatte 18 mm, Zuschnitt %d x %d mm" % (PLATE_W, PLATE_W), "Baumarkt/Holzhandel", 1, "Stk", "Bohrbild docs/build-guide/bohrplan_platte_8080.pdf"],
    [0, "Senkschraube DIN 7991 M6x25", "DIN 7991 M6x25", len(holes), "Stk", "Laenge an der ersten Bohrung pruefen"],
    [0, "Nutenstein mit Steg I-Typ Nut 8 M6", "S8ISMONM6", len(holes), "Stk", "zu den Plattenschrauben; 100er-Pack"],
    [0, "ESD-Matte %d x %d mm" % (PLATE_W - 2 * ESD_MARGIN, PLATE_W - 2 * ESD_MARGIN), "(Vorschlag)", 1, "Stk", "mit 1-MOhm-Erdungsleitung"],
    [0, "Multiplex Birke 15 mm, Zuschnitt %d x %.0f mm" % (BOX_Y1 - BOX_Y0, RACK_CLEAR - 0.4), "Baumarkt/Holzhandel", 2, "Stk", "Rackkasten-Waende, Holzinnenmass 490 mm"],
    [0, "Adam Hall 19\" Heavy Duty Rackschiene 3 HE", "61535 B 3", 4, "Stk", "2 hinten, 2 innen bei y = %.0f" % REAR_RAIL_Y],
    [0, "Senk-Holzschraube 4 x 12", "-", 16, "Stk", "4 je Schiene"],
    [0, "Linsen-Holzschraube 5 x 12", "-", cnt("WK_"), "Stk", "Kastenwinkel an die Wand"],
    [0, "Kaefigmutter M6 + Schraube M6", "Adam Hall 5653", 16, "Satz", "4 je HE-Geraet, Reserve"],
]
for nm_, ln, h in forex:
    rows.append([0, "Forex classic 5 mm, Zuschnitt %.1f x %.1f mm" % (ln, h), "(Vorschlag)", 1, "Stk", "%s, obere Ecken %d x %d ausklinken" % (nm_, NOTCH, NOTCH)])
for i, r in enumerate(rows[1:], 1):
    r[0] = i
bom = os.path.join(REPO, "bom", "tisch_4080_motedis_bom.csv")
if os.path.isdir(os.path.dirname(bom)):
    with open(bom, "w", newline="", encoding="utf-8") as f:
        csv.writer(f, delimiter=";").writerows(rows)
    print("BOM geschrieben:", bom)

try:
    import FreeCADGui as Gui
    Gui.ActiveDocument.ActiveView.viewIsometric()
    Gui.SendMsgToActiveView("ViewFit")
except Exception:
    pass
