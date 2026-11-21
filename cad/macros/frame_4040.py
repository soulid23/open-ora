# open-ora | cad/macros/frame_4040.py | v2
# Tischrahmen 500 x 600 x 220 mm aus Alux Nutprofil 4040 (aluxprofil.de, Art.-Nr. 4040)
# Datenblatt: 40x40, Nut 8 mm (+0,3), Nuttiefe 12 mm, Kernbohrung 6,8 mm,
#             Flaeche 504,8 mm2, 1,395 kg/m, EN-AW 6063 T66
# Start in FreeCAD: exec(open(r"C:\dev\open-ora\cad\macros\frame_4040.py").read())

import os
import csv
import FreeCAD as App
import Part
from FreeCAD import Vector, Rotation, Placement

# ---------------- Parameter (mm) ----------------
REPO = r"C:\dev\open-ora"
# Herstellerdateien (nicht im Git-Repo): erster Ordner mit alux_4040.STEP wird benutzt
ASSET_DIRS = [
    r"C:\Users\julia\Nextcloud\open-ora-assets",   # <- ggf. an deinen Assets-Ordner anpassen
    os.path.join(REPO, "cad", "vendor"),
]
P      = 40                       # Profilmass 4040
W      = 500                      # Tischbreite  (X)
D      = 600                      # Tischtiefe   (Y)
H      = 220                      # Rahmenhoehe  (Z) -> lichte Hoehe innen = H - 2*P = 140
PLATE  = 12                       # Siebdruckplatte
ESD_T  = 2                        # ESD-Matte
ESD_MARGIN = 10                   # Matte liegt 10 mm eingerueckt auf der Platte
SLOT, SLOT_DEPTH, LIP, CAVITY_W = 8.0, 12.0, 4.0, 16.0   # Nut (CAVITY_W und LIP geschaetzt)
CORE_BORE = 6.8
KG_PER_M  = 1.395
AREA_REF  = 504.8                 # Datenblatt, zur Pruefung des STEP-Querschnitts
USE_STEP  = True
STEP_FILE = next((os.path.join(d, "alux_4040.STEP") for d in ASSET_DIRS
                  if os.path.exists(os.path.join(d, "alux_4040.STEP"))),
                 os.path.join(ASSET_DIRS[0], "alux_4040.STEP"))
ANGLES_PER_JOINT = 2              # Winkel 4040 je Verbindung
# ------------------------------------------------

doc = App.newDocument("OpenORA_Frame")
beams = []                        # (Name, Laenge)


# ---------- Profil-Querschnitt ----------
def section_from_step(path):
    """Liest die Hersteller-STEP, schneidet den Querschnitt aus und gibt eine Flaeche
    in der XY-Ebene (zentriert, z=0) zurueck. Rueckgabe None bei Problemen."""
    try:
        shp = Part.read(path)
        bb = shp.BoundBox
        lens = [bb.XLength, bb.YLength, bb.ZLength]
        ax = lens.index(max(lens))
        normal = [Vector(1, 0, 0), Vector(0, 1, 0), Vector(0, 0, 1)][ax]
        mid = [bb.Center.x, bb.Center.y, bb.Center.z][ax]
        wires = shp.slice(normal, mid)
        faces = sorted((Part.Face(w) for w in wires), key=lambda f: -f.Area)
        outer = faces[0]
        face = Part.Face([outer.OuterWire] + [f.OuterWire for f in faces[1:]])
        if ax == 0:
            face.rotate(Vector(0, 0, 0), Vector(0, 1, 0), -90)
        elif ax == 1:
            face.rotate(Vector(0, 0, 0), Vector(1, 0, 0), 90)
        c = face.BoundBox.Center
        face.translate(Vector(-c.x, -c.y, -face.BoundBox.ZMin))
        if abs(face.Area - AREA_REF) / AREA_REF > 0.05:
            print("STEP-Querschnitt weicht ab (%.1f mm2), nutze Ersatzprofil." % face.Area)
            return None
        print("STEP-Querschnitt geladen, Flaeche %.1f mm2 (Soll %.1f)." % (face.Area, AREA_REF))
        return face
    except Exception as e:
        print("STEP nicht nutzbar (%s), nutze Ersatzprofil." % e)
        return None


def fallback_profile(L):
    """Vereinfachtes 4040 nach Datenblattmassen (Nutgeometrie angenaehert)."""
    s = Part.makeBox(P, P, L, Vector(-P / 2, -P / 2, 0))
    x_out = P / 2
    opening = Part.makeBox(LIP + 0.2, SLOT, L + 2, Vector(x_out - LIP, -SLOT / 2, -1))
    cavity = Part.makeBox(SLOT_DEPTH - LIP, CAVITY_W, L + 2,
                          Vector(x_out - SLOT_DEPTH, -CAVITY_W / 2, -1))
    slot = opening.fuse(cavity)
    for a in (0, 90, 180, 270):
        sl = slot.copy()
        sl.rotate(Vector(0, 0, 0), Vector(0, 0, 1), a)
        s = s.cut(sl)
    return s.cut(Part.makeCylinder(CORE_BORE / 2, L, Vector(0, 0, 0)))


SECTION = section_from_step(STEP_FILE) if (USE_STEP and os.path.exists(STEP_FILE)) else None
if SECTION is None and USE_STEP:
    print("Hinweis: %s nicht gefunden/nutzbar -> Ersatzprofil." % STEP_FILE)


def profile(L):
    return SECTION.extrude(Vector(0, 0, L)) if SECTION is not None else fallback_profile(L)


def add(name, L, start, axis):
    rot = {"X": Rotation(Vector(0, 1, 0), 90),
           "Y": Rotation(Vector(1, 0, 0), -90),
           "Z": Rotation()}[axis]
    o = doc.addObject("Part::Feature", name)
    o.Shape = profile(L)
    o.Placement = Placement(Vector(*start), rot)
    beams.append((name, L))


# ---------- Rahmen ----------
zb, zt = P / 2, H - P / 2          # Mittelhoehe untere / obere Ebene

for z, tag in ((zb, "unten"), (zt, "oben")):          # lange Traeger (Y)
    for x, side in ((P / 2, "links"), (W - P / 2, "rechts")):
        add("Laengs_%s_%s" % (tag, side), D, (x, 0, z), "Y")

for z, tag in ((zb, "unten"), (zt, "oben")):          # kurze Traeger (X)
    for y, side in ((P / 2, "vorne"), (D - P / 2, "hinten")):
        add("Quer_%s_%s" % (tag, side), W - 2 * P, (P, y, z), "X")

for x, xs in ((P / 2, "L"), (W - P / 2, "R")):        # Pfosten
    for y, ys in ((P / 2, "V"), (D - P / 2, "H")):
        add("Pfosten_%s%s" % (xs, ys), H - 2 * P, (x, y, P), "Z")

# ---------- Platte, ESD-Matte, Erdungspunkt ----------
plate = doc.addObject("Part::Box", "Platte")
plate.Length, plate.Width, plate.Height = W, D, PLATE
plate.Placement = Placement(Vector(0, 0, H), Rotation())

esd = doc.addObject("Part::Box", "ESD_Matte")
esd.Length, esd.Width, esd.Height = W - 2 * ESD_MARGIN, D - 2 * ESD_MARGIN, ESD_T
esd.Placement = Placement(Vector(ESD_MARGIN, ESD_MARGIN, H + PLATE), Rotation())

# Erdungspunkt: Markierung an der Aussenflaeche von Pfosten_LV (Befestigung spaeter per Nutenstein M8 + Oese)
gnd = doc.addObject("Part::Feature", "Erdungspunkt")
gnd.Shape = Part.makeCylinder(6, 3, Vector(-3, P / 2, H / 2), Vector(1, 0, 0))

doc.recompute()
try:
    import FreeCADGui as Gui
    Gui.ActiveDocument.ActiveView.viewIsometric()
    Gui.SendMsgToActiveView("ViewFit")
except Exception:
    pass

# ---------- Stueckliste ----------
cuts = {}
for _, L in beams:
    cuts[L] = cuts.get(L, 0) + 1
total_m = sum(L for _, L in beams) / 1000.0
joints = len([n for n, _ in beams if n.startswith(("Quer", "Pfosten"))]) * 2   # 2 Enden je Stab
angles = joints * ANGLES_PER_JOINT

rows = [["Pos", "Artikel", "Artikelnr_Alux", "Menge", "Einheit", "Bemerkung"]]
for i, (L, n) in enumerate(sorted(cuts.items(), reverse=True), 1):
    rows.append([i, "Nutprofil 4040 Zuschnitt %d mm" % L, "4040", n, "Stk", "Toleranz -1/+1 mm"])
rows += [
    [len(rows), "Winkel 4040", "(Vorschlag)", angles, "Stk", "%d Verbindungen x %d" % (joints, ANGLES_PER_JOINT)],
    [len(rows) + 1, "Nutenstein einschwenkbar 40-Profil M8", "8-4-M8.40", angles * 2, "Stk", "2 je Winkel"],
    [len(rows) + 2, "Schraube M8 (Innensechskant)", "(passende Laenge waehlen)", angles * 2, "Stk", "2 je Winkel"],
    [len(rows) + 3, "Profilabdeckkappe 4040", "(Vorschlag)", 12, "Stk", "freie Profilenden, Anzahl pruefen"],
]
print("\nZuschnitt (Laenge mm: Anzahl):", cuts)
print("Profil gesamt: %.2f m, ca. %.1f kg" % (total_m, total_m * KG_PER_M))
print("Verbindungen: %d, Winkel: %d" % (joints, angles))

bom_dir = os.path.join(REPO, "bom")
if os.path.isdir(bom_dir):
    with open(os.path.join(bom_dir, "frame_bom.csv"), "w", newline="", encoding="utf-8") as f:
        csv.writer(f, delimiter=";").writerows(rows)
    print("BOM geschrieben:", os.path.join(bom_dir, "frame_bom.csv"))
else:
    print("bom-Ordner nicht gefunden, REPO-Pfad pruefen.")
