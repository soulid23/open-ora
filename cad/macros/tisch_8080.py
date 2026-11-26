# open-ora | cad/macros/tisch_8080.py | v1 (ADR 0010: oberer Rahmen 8080, feste Querstrebe 4080, Rackkasten, Platte 920 x 920)
# Tisch 1000 x 1000 mm. Beine, unterer Rahmen, Bodenstreben und Eckstreben 4040 (wie frame_4040.py v12),
# oberer Rahmen 8080 (innere Nutreihe: Platte, aeussere Nutreihe: Anbauten), Tischhoehe 780 mm.
# Vereinfachtes Modell: Profile als Quader mit angedeuteten Nuten, Verbinder als Platzhalter (Masse pruefen).
# Das Makro baut das Modell, prueft Ueberschneidungen und Kontakte der Verbinder und schreibt
#   bom/tisch_8080_bom.csv   (Stueckliste, Mengen aus dem Modell)
# Start in FreeCAD: exec(open(r"C:\dev\open-ora\cad\macros\tisch_8080.py", encoding="utf-8").read())

import os
import csv
import FreeCAD as App
import Part
from FreeCAD import Vector as V

REPO = r"C:\dev\open-ora"
DOC_NAME = "OpenORA_Tisch8080"

# ---------------- Parameter (mm) ----------------
P, T = 40.0, 80.0                 # 4040 / 8080
W = D = 1000.0
PLATE, ESD_T = 18.0, 2.0
Z_UP0, Z_UP1 = 680.0, 760.0       # oberer Rahmen 8080 (Unterkante = Pfostenende, wie v12)
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


def profile(name, kind, x0, y0, z0, dx, dy, dz, group="Rahmen"):
    s = Part.makeBox(dx, dy, dz, V(x0, y0, z0))
    disp = s
    for c in grooves(x0, y0, z0, dx, dy, dz):
        disp = disp.cut(c)
    o = add(name, disp, kind, group)
    parts[name]["shape"] = s          # Pruefung mit vollem Quader
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

# oberer Rahmen 8080
profile("X8080_vorn", "8080", 0, 0, Z_UP0, W, T, T)
profile("X8080_hinten", "8080", 0, D - T, Z_UP0, W, T, T)
profile("Y8080_links", "8080", 0, T, Z_UP0, T, D - 2 * T, T)
profile("Y8080_rechts", "8080", W - T, T, Z_UP0, T, D - 2 * T, T)
# feste Querstrebe oben: 4080 hochkant, buendig mit Ober- und Unterkante des 8080
profile("Querstrebe_oben_4080", "4080", T, MID_Y - P / 2, Z_UP0, W - 2 * T, P, T)

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
# Beine oben: 2 Winkel 4040 unter dem 8080 (beide unteren Nutreihen) + Zentralverbinder in die aeussere untere Nut
for n, (x, y, sx, sy) in legs.items():
    cx, cy = x + 20, y + 20
    xb = "X8080_vorn" if n in ("LV", "RV") else "X8080_hinten"
    bracket("W4040_Bein_%s_x" % n, (cx + sx * 20, cy, Z_UP0), (sx, 0, 0), (0, 0, -1), (0, 1, 0), joins=("Bein_" + n, xb))
    bracket("W4040_Bein_%s_y" % n, (cx, cy + sy * 20, Z_UP0), (0, sy, 0), (0, 0, -1), (1, 0, 0), joins=("Bein_" + n, xb))
    cv.append(("Bein_" + n, "oben", 1, xb))
# 8080 Seitenholm an 8080 vorn/hinten: 4 Zentralverbinder je Ende + Winkel 8080 innen
for side, x0, sx in (("links", T, +1), ("rechts", W - T, -1)):
    for end, y0, sy, xb in (("vorn", T, +1, "X8080_vorn"), ("hinten", D - T, -1, "X8080_hinten")):
        bracket("W8080_%s_%s" % (side, end), (x0, y0, Z_UP0 + T / 2), (sx, 0, 0), (0, sy, 0), (0, 0, 1),
                leg=70.0, width=72.0, t=6.0, joins=("Y8080_" + side, xb))
        cv.append(("Y8080_" + side, end, 4, xb))
# Querstrebe oben (4080) an die Seitenholme: 2 Zentralverbinder je Ende + 2 Winkel 4080
for side, x0, sx in (("links", T, +1), ("rechts", W - T, -1)):
    for face, y0, sy in (("vorn", MID_Y - P / 2, -1), ("hinten", MID_Y + P / 2, +1)):
        bracket("W4080_Querstrebe_%s_%s" % (side, face), (x0, y0, Z_UP0 + T / 2), (sx, 0, 0), (0, sy, 0), (0, 0, 1),
                leg=36.0, width=72.0, t=5.0, joins=("Querstrebe_oben_4080", "Y8080_" + side))
    cv.append(("Querstrebe_oben_4080", side, 2, "Y8080_" + side))
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
        for zc in (Z_UP0 + 20, Z_UP0 + 60):
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
        top = "Querstrebe_oben_4080" if end == "vorn" else "X8080_hinten"
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
            clash.append((kind, a, b, v))
real = [c for c in clash if c[0] == "KOLLISION"]
slot = [c for c in clash if c[0] != "KOLLISION"]
print("\n=== Ueberschneidungen ===")
for c in real:
    print("KOLLISION  %-28s %-28s %8.0f mm3" % (c[1], c[2], c[3]))
print("Kollisionen: %d | Forex in der Nut (geplant): %d" % (len(real), len(slot)))
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
    if p["kind"] in ("8080", "4080", "4040") and "L" in p:
        k = (p["kind"], round(p["L"], 1))
        cuts[k] = cuts.get(k, 0) + 1
kg = {"8080": 4.024, "4080": 2.342, "4040": 1.395}
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
print("Winkel 4040: %d (davon Rackkasten %d) | Winkel 8080: %d | Winkel 4080: %d | Zentralverbinder-Enden: %s"
      % (cnt("W4040_") + cnt("WK_"), cnt("WK_"), cnt("W8080_"), cnt("W4080_"), cv_by))

rows = [["Pos", "Artikel", "Artikelnr", "Menge", "Einheit", "Bemerkung"]]
for (k, L), n in sorted(cuts.items(), key=lambda kv: (kv[0][0] != "8080", kv[0][0] != "4080", -kv[0][1])):
    rows.append([0, "Nutprofil %s Zuschnitt %.1f mm" % (k, L), "Alux %s" % k, n, "Stk", "Toleranz -1/+1 mm"])
n_cv4040 = cv_by.get("4040", 0)
rows += [
    [0, "Option Profilende: Bearbeitung + Zentralverbinder 90 Grad (4040)", "Alux 4040, Option je Ende", n_cv4040, "Ende", "Beine oben, unterer Rahmen, Bodenstreben"],
    [0, "Option Profilende: 4x Bearbeitung + Zentralverbinder 90 Grad (8080)", "Alux 8080, Option je Ende", cv_by.get("8080", 0), "Ende", "Seitenholme 8080 an vorn/hinten"],
    [0, "Option Profilende: 2x Bearbeitung + Zentralverbinder 90 Grad (4080)", "Alux 4080, Option je Ende", cv_by.get("4080", 0), "Ende", "Querstrebe oben"],
    [0, "Option Profilende: Gewinde M8 (4040)", "Alux 4040, Option je Ende", 4, "Ende", "Beine unten fuer die Stellfuesse"],
    [0, "Winkel 4040", "4040L", cnt("W4040_") + cnt("WK_"), "Stk", "Rahmen %d, Rackkasten %d (Kasten-Seite: Zentrierstege abbrechen)" % (cnt("W4040_"), cnt("WK_"))],
    [0, "Winkel 8080", "8080L", cnt("W8080_"), "Stk", "Innenecken oberer Rahmen"],
    [0, "Winkel 4080", "4080L", cnt("W4080_"), "Stk", "Querstrebe oben, je Ende vorn und hinten"],
    [0, "Linsenkopfschraube ISO 7380 M8x16", "ISO 7380 M8x16", 2 * cnt("W4040_") + cnt("WK_") + 4 * cnt("W8080_") + 4 * cnt("W4080_"), "Stk", "2 je Winkel 4040, 4 je Winkel 8080/4080, 1 je Kastenwinkel"],
    [0, "Nutenstein einschwenkbar 40-Serie M8", "8-4-M8.40", 2 * cnt("W4040_") + cnt("WK_") + 4 * cnt("W8080_") + 4 * cnt("W4080_"), "Stk", "zu den Winkelschrauben"],
    [0, "Nutenstein einschwenkbar 40-Serie M8, vorab eingelegt", "8-4-M8.40", prenuts, "Stk", "Innenseite der 8080-Seitenholme, beide Reihen, fuer %d weitere Streben" % len(PRENUT_Y)],
    [0, "Winkelverbinder 45 Grad 4040", "4040-45", cnt("V45_"), "Stk", "Eckstreben (wie v12, Schrauben laut Produktseite)"],
    [0, "Gelenkstellfuss 80 mm M8x50", "80-M8x50", 4, "Stk", "wie v12"],
    [0, "Siebdruckplatte 18 mm, Zuschnitt %d x %d mm" % (PLATE_W, PLATE_W), "Baumarkt/Holzhandel", 1, "Stk", "Bohrbild: docs/build-guide/bohrplan_platte_8080.pdf"],
    [0, "Senkschraube DIN 7991 / ISO 10642 M6x25", "DIN 7991 M6x25", len(holes), "Stk", "Platte an die innere Nutreihe; Laenge an der ersten Bohrung pruefen"],
    [0, "Nutenstein einschwenkbar 40-Serie M6", "8-4-M6.40", len(holes), "Stk", "zu den Plattenschrauben"],
    [0, "ESD-Matte %d x %d mm" % (PLATE_W - 2 * ESD_MARGIN, PLATE_W - 2 * ESD_MARGIN), "(Vorschlag)", 1, "Stk", "mit 1-MOhm-Erdungsleitung"],
    [0, "Multiplex Birke 15 mm, Zuschnitt %d x %.0f mm" % (BOX_Y1 - BOX_Y0, RACK_CLEAR - 0.4), "Baumarkt/Holzhandel", 2, "Stk", "Rackkasten-Waende, Holzinnenmass 490 mm"],
    [0, "Adam Hall 19\" Heavy Duty Rackschiene 3 HE", "61535 B 3", 4, "Stk", "2 hinten (Bedienseite Rack), 2 innen bei y = %.0f (Einbautiefe %.0f mm)" % (REAR_RAIL_Y, D - REAR_RAIL_Y)],
    [0, "Senk-Holzschraube 4 x 12", "-", 16, "Stk", "4 je Schiene in die Wand"],
    [0, "Linsen-Holzschraube 5 x 12", "-", cnt("WK_"), "Stk", "Kastenwinkel an die Wand"],
    [0, "Kaefigmutter M6 + Schraube M6", "Adam Hall 5653", 16, "Satz", "4 je HE-Geraet, Reserve"],
]
for nm_, ln, h in forex:
    rows.append([0, "Forex classic 5 mm, Zuschnitt %.1f x %.1f mm" % (ln, h), "(Vorschlag)", 1, "Stk", "%s, obere Ecken %d x %d ausklinken" % (nm_, NOTCH, NOTCH)])
for i, r in enumerate(rows[1:], 1):
    r[0] = i
bom = os.path.join(REPO, "bom", "tisch_8080_bom.csv")
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
