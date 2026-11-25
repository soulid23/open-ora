# -*- coding: utf-8 -*-
"""
open-ora – Licht- und Sensorrahmen (Makro v2, 2026-11-25)
Baustelle sensorik-ki, gehört zu Version 1 (ADR 0008).

Portalrahmen über dem Tisch, verankert an vier Stützen außerhalb der
Tischfläche: hinten links/rechts und Mitte links/rechts. Die Stützen werden
nur an den oberen beiden Seitenholmen (Y_oben_*, Y_unten_*) verschraubt und
reichen nicht bis zum Boden (v2; v1 ging bis zur Bodenstrebe). Trägt ein LED-Panel
und eine Sensorschiene (Kameras, Wärmebild, ToF, Reserve).

Koordinaten wie frame_4040.py: X = Breite (0..1000), Y = Tiefe (0 = Sitzplatz
vorn, 1000 = hinten), Z = Höhe ab Boden. Oberkante ESD-Matte Z = 740.

Läuft eigenständig: baut in das aktive Dokument (oder ein neues).
Am besten in Tisch V1 (cad/frame/OpenORA_Frame22.FCStd) oder im Dokument von
frame_4040.py ausführen: Tischmaß und Holmhöhen werden dann übernommen, und
die Kollisionsprüfung läuft gegen Tisch (und Arm, falls im Dokument).
Geprüft 2026-11-25 an einer Kopie von Frame22: 24 Objekte, 0 Kollisionen.
Die Profile sind vereinfachte Vollquader (keine Nuten).
Stückliste: bom/light_frame_bom.csv (wird geschrieben, wenn das Makro aus
cad/macros/ gestartet wird).

Abschätzung (v1, 4040 mit I = 9 cm^4 angenommen, Alux-Datenblatt prüfen):
- Panel 4000 lm, Unterkante Z 1423: Platine (Z 898) Mitte ~3200 lx,
  Rand Panelfläche ~1700 lx; Matte Mitte ~2200 lx, Ecke Arbeitsfeld ~800 lx.
- Stützen 740 mm frei über Tischholm, eingespannt über 2 Verbinder (Abstand ~175 mm): ~190 N/mm seitlich (4 Stützen),
  f1 ~22 Hz bei 10 kg oben (Tisch starr gerechnet; real begrenzt der Tisch).
- Ausleger-Kragarm 520 mm: 0,4 mm bei 30 N an der Spitze.
- Kamera Cam 3 (66x41°) Unterkante Z 1358: auf Platine 600 x 345 mm,
  0,13 mm/px.
"""
import FreeCAD as App
import Part

# ---------------------------------------------------------------- Parameter
TABLE_W, TABLE_D = 1000.0, 1000.0
MAT_TOP = 740.0              # Oberkante ESD-Matte
P = 40.0                     # 4040-Profil
P2 = 20.0                    # 2020-Profil

POST_Z0 = 505.6              # Stützenfuß = Unterkante mittlerer Seitenholm (Y_unten_*);
                             # verschraubt nur an den oberen beiden Seitenholmen, kein Bodenkontakt.
                             # Wird unten automatisch aus dem Tischdokument übernommen.
FRAME_TOP = 1500.0           # Oberkante Ausleger/Traversen
POST_Y_REAR = 920.0          # Stütze hinten: Y 920..960 (am Seitenholm, vor dem Erdungspunkt Y 974..986)
POST_Y_MID = 600.0           # Stütze Mitte: Y 600..640 (Logo-Druck der Seiten darf überdeckt werden)
BEAM_Y_FRONT = 100.0         # Ausleger enden 100 mm hinter Vorderkante (Kopffreiheit)

PANEL_W, PANEL_D, PANEL_T = 595.0, 595.0, 12.0   # Standard-LED-Panel 62x62 (Einlegemaß 595)
PANEL_CX, PANEL_CY = 500.0, 450.0                # Mitte Arbeitsbereich
PANEL_HANG = 25.0                                # Abhänger unter Traverse
REAR_TRAV_Y = 760.0                              # hintere Paneltraverse Y 760..800

SENSOR_Y = 440.0             # Sensorschiene 2020, Y 440..460
SENSOR_GAP = 10.0            # Abstand Unterkante Panel -> Oberkante Schiene

FRAME_COLOR = (0.75, 0.75, 0.78)
PANEL_COLOR = (1.0, 1.0, 0.85)
SENSOR_COLOR = (0.15, 0.15, 0.15)

# ------------------------------------------------------------------ Helfer
doc = App.ActiveDocument or App.newDocument("OpenORA_Licht")

# Maße aus dem Tischdokument übernehmen, falls vorhanden (frame_4040.py)
def _bb(name):
    o = doc.getObject(name)
    return o.Shape.BoundBox if o is not None and hasattr(o, "Shape") and not o.Shape.isNull() else None

_plate, _top, _mid = _bb("Platte"), _bb("Y_oben_links"), _bb("Y_unten_links")
if _plate:
    TABLE_W, TABLE_D = _plate.XLength, _plate.YLength
if _mid:
    POST_Z0 = _mid.ZMin
print("Tisch %.0f x %.0f, Seitenholm oben Z %s, mitte Z %s -> Stützen ab Z %.1f" % (
    TABLE_W, TABLE_D,
    "%.1f..%.1f" % (_top.ZMin, _top.ZMax) if _top else "?",
    "%.1f..%.1f" % (_mid.ZMin, _mid.ZMax) if _mid else "?", POST_Z0))

grp = doc.addObject("App::DocumentObjectGroup", "Lichtrahmen")
BOM = []


def box(name, x0, x1, y0, y1, z0, z1, color=FRAME_COLOR, bom=None):
    s = Part.makeBox(x1 - x0, y1 - y0, z1 - z0, App.Vector(x0, y0, z0))
    o = doc.addObject("Part::Feature", name)
    o.Shape = s
    grp.addObject(o)
    if App.GuiUp:
        o.ViewObject.ShapeColor = color
    if bom:
        BOM.append((name,) + bom)
    return o


def prof(name, kind, x0, x1, y0, y1, z0, z1):
    L = max(x1 - x0, y1 - y0, z1 - z0)
    return box(name, x0, x1, y0, y1, z0, z1, bom=(kind, round(L, 1)))


# ------------------------------------------------------------- Geometrie
ZB0 = FRAME_TOP - P                      # Unterkante Ausleger
XL0, XL1 = -P, 0.0                       # links außen
XR0, XR1 = TABLE_W, TABLE_W + P          # rechts außen

# Stützen (Alux 4040), stehen auf Z=POST_Z0, tragen die Ausleger von unten
for side, (xa, xb) in (("L", (XL0, XL1)), ("R", (XR0, XR1))):
    prof(f"LR_Stuetze_hinten_{side}", "Alux 4040", xa, xb, POST_Y_REAR, POST_Y_REAR + P, POST_Z0, ZB0)
    prof(f"LR_Stuetze_mitte_{side}", "Alux 4040", xa, xb, POST_Y_MID, POST_Y_MID + P, POST_Z0, ZB0)
    # Ausleger längs Y, liegt auf beiden Stützen
    prof(f"LR_Ausleger_{side}", "Alux 4040", xa, xb, BEAM_Y_FRONT, POST_Y_REAR + P, ZB0, FRAME_TOP)

# Traversen (X) zwischen den Auslegern
prof("LR_Traverse_hinten", "Alux 4040", 0, TABLE_W, POST_Y_REAR, POST_Y_REAR + P, ZB0, FRAME_TOP)
prof("LR_Traverse_vorn", "Alux 4040", 0, TABLE_W, BEAM_Y_FRONT, BEAM_Y_FRONT + P, ZB0, FRAME_TOP)
prof("LR_Traverse_Panel_hinten", "Alux 4040", 0, TABLE_W, REAR_TRAV_Y, REAR_TRAV_Y + P, ZB0, FRAME_TOP)

# LED-Panel, abgehängt (4 Abhänger an vorderer und hinterer Traverse)
pz1 = ZB0 - PANEL_HANG
pz0 = pz1 - PANEL_T
px0, px1 = PANEL_CX - PANEL_W / 2, PANEL_CX + PANEL_W / 2
py0, py1 = PANEL_CY - PANEL_D / 2, PANEL_CY + PANEL_D / 2
box("LR_LED_Panel_595", px0, px1, py0, py1, pz0, pz1, PANEL_COLOR,
    bom=("LED-Panel 595x595, ~40 W, CRI>=90, 4000-5000 K, flimmerfrei", 595))
# Abhänger: Winkel 40 mm breit, von Traverse-Unterkante bis Panel-Oberkante.
# Vorn liegt das Panel hinter der Traverse -> Flachwinkel nach hinten (nur als Block)
for i, x in enumerate((px0 + 40, px1 - 80)):
    box(f"LR_Abhaenger_vorn_{i+1}", x, x + 40, BEAM_Y_FRONT, py0 + 30, pz1, ZB0,
        bom=("Abhänger Panel (Druckteil/Flachwinkel)", 0))
    box(f"LR_Abhaenger_hinten_{i+1}", x, x + 40, py1 - 30, REAR_TRAV_Y + P, pz1, ZB0,
        bom=("Abhänger Panel (Druckteil/Flachwinkel)", 0))

# Sensorschiene 2020 (X) unter dem Panel, an den Auslegern über Abhängewinkel
sz1 = pz0 - SENSOR_GAP
sz0 = sz1 - P2
prof("LR_Sensorschiene", "Alux 2020", 0, TABLE_W, SENSOR_Y, SENSOR_Y + P2, sz0, sz1)
for side, (xa, xb) in (("L", (XL0, XL1)), ("R", (XR0, XR1))):
    box(f"LR_Sensorhalter_{side}", xa, xb, SENSOR_Y, SENSOR_Y + P2, sz0, ZB0,
        bom=("Halter Sensorschiene (Druckteil/Winkel)", 0))

# Sensor-Platzhalter an der Sensorschiene (Unterseite)
def sensor(name, cx, w, d, h, desc):
    box(name, cx - w / 2, cx + w / 2, SENSOR_Y + P2 / 2 - d / 2, SENSOR_Y + P2 / 2 + d / 2,
        sz0 - h, sz0, SENSOR_COLOR, bom=(desc, 0))

sensor("LR_Kamera_oben_Mitte", 500, 40, 40, 35, "Hauptkamera Draufsicht (z.B. RPi HQ/Cam 3)")
sensor("LR_Waermebild", 400, 35, 35, 30, "Wärmebildkamera (z.B. MLX90640)")
sensor("LR_ToF_Tiefe", 600, 30, 30, 20, "ToF/Tiefensensor")
sensor("LR_Reserve_1", 250, 30, 30, 20, "Reserveplatz Sensor")
sensor("LR_Reserve_2", 750, 30, 30, 20, "Reserveplatz Sensor")

# Schrägkamera an der vorderen Traverse (Blick nach hinten-unten)
box("LR_Kamera_vorn_schraeg", 480, 520, BEAM_Y_FRONT + 5, BEAM_Y_FRONT + 35, ZB0 - 45, ZB0,
    SENSOR_COLOR, bom=("Kamera schräg vorn (Seitenansicht Bauteile)", 0))

# LED-Treiber auf der hinteren Traverse
box("LR_LED_Treiber", 400, 600, POST_Y_REAR, POST_Y_REAR + P, FRAME_TOP, FRAME_TOP + 30,
    (0.3, 0.3, 0.35), bom=("LED-Treiber (Konstantstrom, dimmbar, flimmerfrei)", 0))

doc.recompute()

# Kollisionsprüfung gegen alle übrigen Körper im Dokument (Tisch, Arm)
_new = list(grp.Group)
_others = [o for o in doc.Objects if o not in _new and hasattr(o, "Shape")
           and o.TypeId != "App::DocumentObjectGroup" and not o.Shape.isNull()]
_hits = []
for i, a in enumerate(_new):
    for b in _others + _new[i + 1:]:
        if a.Shape.BoundBox.intersect(b.Shape.BoundBox):
            v = a.Shape.common(b.Shape).Volume
            if v > 1.0:
                _hits.append((a.Name, b.Name, round(v)))
print("Kollisionen:", _hits if _hits else 0)

# Verbinder (nur Stückliste)
BOM += [
    ("Verbinder Stütze-Tisch", "Flachverbinder/Nutenstein M8 an Seitenholm oben + mitte, 2 je Stütze", 8),
    ("Verbinder Stütze-Ausleger", "Winkel 4040 + Nutensteine", 8),
    ("Verbinder Traverse-Ausleger", "Winkel 4040 + Nutensteine", 12),
    ("Endkappen 4040", "Ausleger vorn/hinten", 4),
]

print("Lichtrahmen: %d Objekte" % len(grp.Group))
for r in BOM:
    print(";".join(str(v) for v in r))

# Stückliste ins Repo schreiben (nur wenn das Makro aus cad/macros/ läuft)
try:
    import os, csv
    _root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    _bomdir = os.path.join(_root, "bom")
    if os.path.isdir(_bomdir):
        with open(os.path.join(_bomdir, "light_frame_bom.csv"), "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f, delimiter=";")
            w.writerow(["Teil", "Material/Beschreibung", "Länge mm / Anzahl"])
            w.writerows(BOM)
        print("Stückliste geschrieben:", os.path.join(_bomdir, "light_frame_bom.csv"))
except NameError:
    print("Stückliste nicht geschrieben (Makro nicht aus einer Datei gestartet).")
