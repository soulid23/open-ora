# open-ora | cad/macros/arm_holder.py | v2 (Konzept, Platzhaltergeometrie; Fuss an den oberen Rahmenprofilen verschraubt)
# Arm 1 "Halter" auf dem Tisch V1 (cad/frame/OpenORA_Frame22.FCStd), hinten rechts auf dem Aluframe: SCARA mit Hubsaeule und 3-Achs-Handgelenk, Traeger-Kupplung, Platinenrahmen.
#   J1 Drehung Saeule (senkrecht, Riemen 1:20) | Z Hub (TR8x2, selbsthemmend) | J2 Ellbogen (senkrecht, Riemen 1:12)
#   J4 Gieren (Schnecke 1:30) | J5 Nicken (Schnecke 1:30) | J6 Rollen (Schnecke 1:20) | Kupplung (3 Kugeln / 3 Nuten)
# Siehe docs/decisions/0007-arm1-halter-konzept.md und cad/analysis/arm_holder_sizing.py.
# v2: J1-Fuss = Grundplatte auf X_oben_hinten + Y_oben_rechts, zwei Wangen an den Innenseiten beider Profile,
#     7 x M8 mit Nutensteinen (3 senkrecht in die oberen Nuten, 4 waagerecht in die inneren Nuten), Lagergehaeuse rund.
# Koordinaten wie frame_4040.py: X links->rechts (Blick von vorn), Y 0 = vorn (Sitzseite), Z ab Boden.
# Alle Koerper sind Platzhalter fuer Bauraum und Kollisionspruefung, keine Fertigungsteile.
# v2b: MOUNT = "aussen" (Standard): Modul von aussen verschraubt, Platte ohne Ausschnitt.
# Start in FreeCAD: exec(open(r"C:\dev\open-ora\cad\macros\arm_holder.py").read())

import math
import os
import FreeCAD as App
import Part
from FreeCAD import Vector, Rotation, Placement

# ---------------- Parameter (mm, Grad) ----------------
REPO          = r"C:\dev\open-ora"
INCLUDE_FRAME = True              # Tisch mitzeichnen
FRAME_FILE    = os.path.join(REPO, "cad", "frame", "OpenORA_Frame22.FCStd")   # Tisch V1 (final); fehlt die Datei,
                                  # wird der Tisch aus frame_4040.py erzeugt (ohne die BOM neu zu schreiben)
DESK_H        = 740.0             # Oberkante ESD-Matte (wie frame_4040.py)
PLATE_TOP     = DESK_H - 2.0      # Oberkante Siebdruckplatte (Referenz)
H_FRAME       = 720.0             # Oberkante oberer Rahmen = Unterseite Platte
P             = 40.0

BASE_X, BASE_Y = 920.0, 920.0     # J1-Achse hinten rechts
CORNER_CUT    = 170.0             # Eckausschnitt in Platte und Matte; der Fuss steht direkt auf dem Aluframe
                                  # (X_oben_hinten + Y_oben_rechts, ueber Pfosten_RH), Nutensteine in den oberen Nuten

BASE_H        = 90.0              # Fuss ab Rahmenoberkante (Grundplatte + Lagergehaeuse), Oberkante 70 mm ueber der Matte
# ----- Fuss an den oberen Rahmenprofilen (v2) -----
MOUNT         = "aussen"          # "aussen": Modul von aussen an X_oben_hinten, Y_oben_rechts und Pfosten_RH geschraubt,
                                  #           Deckplatte ueber der Matte, Platte bleibt ganz (abnehmbar, modular)
                                  # "innen":  Grundplatte im Eckausschnitt der Platte, Wangen an den Innenseiten
OUT_T         = 10.0              # aussen: Wangen Alu an den Aussenseiten
TOP_T         = 12.0              # aussen: Deckplatte Alu
MAT_GAP       = 2.0               # aussen: Luft Deckplatte ueber der ESD-Matte
TAB_Z0        = 600.0             # aussen: Lasche der Wangen reicht am Pfosten bis hier herunter
OUT_SCREWS    = [850.0, 885.0, 985.0]   # aussen: in die aeussere Nut der oberen Profile (z = 700)
POST_SCREWS   = [640.0]           # aussen: in die aeusseren Nuten von Pfosten_RH (je Seite)
MOTOR_BACK    = True              # aussen: J1-Motor haengt hinter dem Tisch unter der Deckplatte (Riemen zur J1-Achse)
FOOT_T        = 12.0              # Grundplatte Alu (EN AW 5083 o. ae.), liegt in der Ecke auf beiden Profiloberseiten
FOOT_GAP      = 1.0               # Luft zur Siebdruckplatte im Eckausschnitt
CHEEK_T       = 8.0               # Wangen Alu an den Innenseiten von X_oben_hinten und Y_oben_rechts
HOUSING_D     = 120.0             # J1-Lagergehaeuse (rund, Vierpunktlager / Lagerpaar)
SLOT_C        = 20.0              # Nutmitte ab Profilkante (4040, eine Nut je Seite)
NUT_L, NUT_W  = 11.0, 11.0        # Nutenstein M8 (Platzhalter, liegt in der Nutkammer)
NUT_D0, NUT_D1 = 4.6, 8.4         # Nutenstein von ... bis ... mm unter der Profiloberflaeche (Nutsteg ca. 4,5 mm)
SCREW_D, HEAD_D, HEAD_H = 7.6, 13.0, 8.0   # M8 ISO 4762 (Schaft im Modell 7,6 wegen 8-mm-Nutoeffnung)
TOP_SCREWS    = [(845.0, "X"), (985.0, "X"), (845.0, "Y")]   # senkrecht: Lage entlang der oberen Nut von X_oben_hinten / Y_oben_rechts
SIDE_SCREWS   = [(860.0, "X"), (935.0, "X"), (860.0, "Y"), (935.0, "Y")]   # waagerecht durch die Wangen in die inneren Nuten
TIP_MOMENT    = 26.0              # Nm, Kippmoment am Fuss (ADR 0007)
COL_W, COL_D  = 80.0, 40.0        # Drehsaeule 4080 mit zwei MGN12-Schienen
COL_H         = 400.0             # Saeulenhoehe ueber J1-Gehaeuse
Z_STROKE      = 200.0
L1, L2        = 300.0, 300.0      # Achsabstaende Oberarm / Unterarm
LINK_W, LINK_H = 20.0, 40.0       # 2040 hochkant
HUB_D         = 60.0              # Lagerstellen J2 / J4
WRIST_DROP    = 120.0             # Unterarm-Mitte bis J5-Achse
J6_L          = 50.0              # Rollgehaeuse
CPL_D, CPL_T  = 60.0, 15.0        # Kupplung (Arm- und Traegerhaelfte zusammen)
CARRIER_L, CARRIER_W, CARRIER_T = 220.0, 200.0, 12.0   # Platinenrahmen
PCB_L, PCB_W, PCB_T = 200.0, 160.0, 1.6
PIN_PITCH     = 70.0              # Stuetzstifte unter der Platine (<= 80 mm, siehe Rechnung)

# Pose: Platinenmitte (Ziel) und Ausrichtung
TARGET        = (500.0, 450.0)    # Praesentationspunkt P0
TARGET_H      = 150.0             # Platinenoberseite ueber der Matte
PITCH         = 0.0               # J5: 0 = Platine waagerecht
ROLL          = 0.0               # J6: 180 = Platine gewendet
ELBOW         = -1                # Ellbogen-Seite (+1 / -1), -1 haelt den Ellbogen von der Sitzseite weg
# ------------------------------------------------

# Eigenes Dokument je Lauf (wie frame_4040.py); offene Tisch-Dokumente werden nicht veraendert.
def _norm(p):
    return os.path.normcase(os.path.normpath(p or ""))

if INCLUDE_FRAME and os.path.exists(FRAME_FILE):
    # Tisch V1 aus der FCStd-Datei in ein neues Dokument kopieren; die Tischdatei selbst wird nicht veraendert.
    src_doc = next((d for d in App.listDocuments().values() if _norm(d.FileName) == _norm(FRAME_FILE)), None)
    opened_here = src_doc is None
    if opened_here:
        src_doc = App.openDocument(FRAME_FILE, True)          # versteckt oeffnen
    doc = App.newDocument("OpenORA_Arm1")
    for so in src_doc.Objects:
        if not hasattr(so, "Shape") or so.Shape.isNull():
            continue
        no = doc.addObject("Part::Feature", so.Name)
        no.Label = so.Label
        no.Shape = so.Shape.copy()
        try:
            no.ViewObject.ShapeColor = so.ViewObject.ShapeColor
            no.ViewObject.Transparency = so.ViewObject.Transparency
        except Exception:
            pass
    if opened_here:
        App.closeDocument(src_doc.Name)
    print("Tisch aus %s (%d Objekte)" % (os.path.basename(FRAME_FILE), len(doc.Objects)))
elif INCLUDE_FRAME:
    src = open(os.path.join(REPO, "cad", "macros", "frame_4040.py"), encoding="utf-8").read()
    cut = src.find("# ---------- Stueckliste")
    exec(src[:cut] if cut > 0 else src, {"__name__": "frame_4040"})   # nur Geometrie, BOM bleibt unberuehrt
    doc = App.ActiveDocument
else:
    doc = App.newDocument("OpenORA_Arm1")
App.setActiveDocument(doc.Name)

# alte Arm-Objekte entfernen (Makro mehrfach ausfuehrbar)
for o in [o for o in doc.Objects if o.Name.startswith("A1_")]:
    doc.removeObject(o.Name)

arm_objs = []
def part(name, shape, rgb=(0.2, 0.45, 0.75)):
    o = doc.addObject("Part::Feature", "A1_" + name)
    o.Shape = shape
    try:
        o.ViewObject.ShapeColor = rgb
    except Exception:
        pass
    arm_objs.append(o)
    return o

def bar(p0, p1, w, h):
    """Quader von p0 nach p1 (waagerecht), Breite w, Hoehe h, mittig auf der Verbindungslinie."""
    d = p1 - p0
    L = d.Length
    s = Part.makeBox(L, w, h, Vector(0, -w / 2, -h / 2))
    s.Placement = Placement(p0, Rotation(Vector(0, 0, 1), math.degrees(math.atan2(d.y, d.x))))
    return s

# ---------------- Inverse Kinematik (Platine waagerecht) ----------------
psi = math.atan2(TARGET[1] - BASE_Y, TARGET[0] - BASE_X)          # Werkzeugachse zeigt von der Basis weg
J5_FRONT = 35.0                                                     # J5-Achse bis Vorderseite J5-Gehaeuse
reach_tcp = J5_FRONT + J6_L + CPL_T + CARRIER_L / 2                 # J5-Achse bis Platinenmitte
wx = TARGET[0] - reach_tcp * math.cos(psi)
wy = TARGET[1] - reach_tcp * math.sin(psi)
dx, dy = wx - BASE_X, wy - BASE_Y
r = math.hypot(dx, dy)
if r > L1 + L2 - 1 or r < abs(L1 - L2) + 1:
    raise ValueError("Ziel ausserhalb der Reichweite (r = %.0f mm)" % r)
c2 = (r * r - L1 * L1 - L2 * L2) / (2 * L1 * L2)
q2 = ELBOW * math.acos(max(-1.0, min(1.0, c2)))
q1 = math.atan2(dy, dx) - math.atan2(L2 * math.sin(q2), L1 + L2 * math.cos(q2))
q4 = psi - (q1 + q2)                                                # J4 relativ zum Unterarm

z_mat = DESK_H
z_j5 = z_mat + TARGET_H + CARRIER_T / 2 + 10                       # J5 etwas ueber Rahmenmitte
z_link = z_j5 + WRIST_DROP
z_base_top = H_FRAME + BASE_H
z_min_link = z_base_top + 60
z_lift = z_link - z_min_link
if not (0 <= z_lift <= Z_STROKE):
    print("WARNUNG: Hub %.0f mm ausserhalb 0..%.0f" % (z_lift, Z_STROKE))

J1 = Vector(BASE_X, BASE_Y, 0)
E  = Vector(BASE_X + L1 * math.cos(q1), BASE_Y + L1 * math.sin(q1), z_link)
W  = Vector(wx, wy, z_link)

# ---------------- Unterbau: Fuss an den oberen Rahmenprofilen ----------------
IN   = 1000 - P                                                  # Innenkante der Profile (960)
SC   = 1000 - SLOT_C                                             # Nutmitte am Pfosten bzw. obere Nut (980)
ZSC  = H_FRAME - SLOT_C                                          # Nutmitte der Seitenflaechen der oberen Profile (700)
COL_FOOT = (0.55, 0.57, 0.6)
COL_HW   = (0.75, 0.75, 0.78)
screws, nuts, bom_foot = [], [], []

def side_screw(p_head, direction, nut_box):
    """M8 von aussen nach innen: Kopf an p_head, Schaft in Richtung direction, Nutenstein als Box."""
    screws.append(Part.makeCylinder(SCREW_D / 2, OUT_T + NUT_D1, p_head, direction))
    screws.append(Part.makeCylinder(HEAD_D / 2, HEAD_H, p_head, direction * -1))
    nuts.append(nut_box)

if MOUNT == "aussen":
    E_OUT  = 1000 + OUT_T                                        # Aussenkante der Wangen
    Z_TOP0 = DESK_H + MAT_GAP                                    # Unterkante Deckplatte (ueber der Matte)
    Z_FOOT1 = Z_TOP0 + TOP_T
    X0 = 1000 - CORNER_CUT                                       # Deckplatte ab x/y = 830
    Y_BACK = E_OUT + (60.0 if MOTOR_BACK else 0.0)               # Deckplatte ragt hinten fuer den J1-Motor ueber
    part("Fuss_Deckplatte", Part.makeBox(E_OUT - X0, Y_BACK - X0, TOP_T, Vector(X0, X0, Z_TOP0)), COL_FOOT)
    # Wangen: oben ueber die Profilhoehe bis unter die Deckplatte, Lasche am Pfosten nach unten
    wz0 = H_FRAME - P - 10                                       # 10 mm unter der Profilunterkante
    rear = Part.makeBox(E_OUT - X0, OUT_T, Z_TOP0 - wz0, Vector(X0, 1000, wz0))
    rear = rear.fuse(Part.makeBox(E_OUT - IN, OUT_T, wz0 - TAB_Z0 + 1, Vector(IN, 1000, TAB_Z0))).removeSplitter()
    right = Part.makeBox(OUT_T, 1000 - X0, Z_TOP0 - wz0, Vector(1000, X0, wz0))
    right = right.fuse(Part.makeBox(OUT_T, 1000 - IN, wz0 - TAB_Z0 + 1, Vector(1000, IN, TAB_Z0))).removeSplitter()
    part("Fuss_Wange_hinten", rear, COL_FOOT)
    part("Fuss_Wange_rechts", right, COL_FOOT)
    part("J1_Lagergehaeuse", Part.makeCylinder(HOUSING_D / 2, H_FRAME + BASE_H - Z_FOOT1, Vector(BASE_X, BASE_Y, Z_FOOT1)),
         (0.15, 0.15, 0.18))
    if MOTOR_BACK:   # haengt hinter der hinteren Wange unter der Deckplatte, Riemen 115 mm nach vorn zur J1-Achse
        part("J1_Motor_NEMA17_60", Part.makeBox(42, 42, 60, Vector(BASE_X - 21, E_OUT + 4, Z_TOP0 - 60)), (0.1, 0.1, 0.1))
    else:
        part("J1_Motor_NEMA17_60", Part.makeBox(42, 42, 60, Vector(BASE_X - 60, BASE_Y - 60, Z_FOOT1)), (0.1, 0.1, 0.1))
    # Schrauben: hinten in die aeussere Nut von X_oben_hinten (y = 1000) und Pfosten_RH (Nut bei x = 980),
    #            rechts in die aeussere Nut von Y_oben_rechts (x = 1000) und Pfosten_RH (Nut bei y = 980)
    for x in OUT_SCREWS:
        side_screw(Vector(x, E_OUT, ZSC), Vector(0, -1, 0),
                   Part.makeBox(NUT_L, NUT_D1 - NUT_D0, NUT_W, Vector(x - NUT_L / 2, 1000 - NUT_D1, ZSC - NUT_W / 2)))
    for y in [v for v in OUT_SCREWS if v < IN]:                   # Y_oben_rechts endet bei y = 960
        side_screw(Vector(E_OUT, y, ZSC), Vector(-1, 0, 0),
                   Part.makeBox(NUT_D1 - NUT_D0, NUT_L, NUT_W, Vector(1000 - NUT_D1, y - NUT_L / 2, ZSC - NUT_W / 2)))
    for z in POST_SCREWS:
        side_screw(Vector(SC, E_OUT, z), Vector(0, -1, 0),
                   Part.makeBox(NUT_W, NUT_D1 - NUT_D0, NUT_L, Vector(SC - NUT_W / 2, 1000 - NUT_D1, z - NUT_L / 2)))
        side_screw(Vector(E_OUT, SC, z), Vector(-1, 0, 0),
                   Part.makeBox(NUT_D1 - NUT_D0, NUT_W, NUT_L, Vector(1000 - NUT_D1, SC - NUT_W / 2, z - NUT_L / 2)))
    n_scr = len(nuts)
    bom_foot = [
        ["Deckplatte Alu %.0f mm, %.0f x %.0f mm" % (TOP_T, E_OUT - X0, Y_BACK - X0), "(Zuschnitt/Fraesteil)", 1, "Stk",
         "liegt %.0f mm ueber der ESD-Matte; Bohrungen Lagergehaeuse, J1-Riemen, Wangen" % MAT_GAP],
        ["Wange hinten Alu %.0f mm, %.0f x %.0f mm mit Lasche am Pfosten" % (OUT_T, E_OUT - X0, Z_TOP0 - TAB_Z0), "(Zuschnitt/Laser)", 1, "Stk",
         "aussen an X_oben_hinten + Pfosten_RH"],
        ["Wange rechts Alu %.0f mm, %.0f x %.0f mm mit Lasche am Pfosten" % (OUT_T, 1000 - X0, Z_TOP0 - TAB_Z0), "(Zuschnitt/Laser)", 1, "Stk",
         "aussen an Y_oben_rechts + Pfosten_RH"],
        ["Zylinderschraube ISO 4762 M8x20", "ISO 4762-M8x20", n_scr, "Stk", "waagerecht durch die Wangen in die aeusseren Nuten"],
        ["Nutenstein einschwenkbar 40-Profil M8", "8-4-M8.40", n_scr, "Stk", "wie Rahmen"],
        ["Scheibe ISO 7089 8", "ISO 7089-8", n_scr, "Stk", ""],
        ["Zylinderschraube ISO 4762 M6x20 + Gewinde M6 in den Wangen", "ISO 4762-M6x20", 6, "Stk", "Deckplatte mit den Wangen verschrauben"]]
else:
    # Eckausschnitt in Siebdruckplatte und ESD-Matte (der Fuss liegt direkt auf dem Aluframe, nicht auf der Platte)
    corner = Part.makeBox(CORNER_CUT + 1, CORNER_CUT + 1, 100, Vector(1000 - CORNER_CUT, 1000 - CORNER_CUT, H_FRAME - 1))
    for nm in ("Platte", "ESD_Matte"):
        o = doc.getObject(nm)
        if o is not None and hasattr(o, "Shape"):
            sh = o.Shape.cut(corner)
            lab, col_ = o.Label, (o.ViewObject.ShapeColor if o.ViewObject else None)
            doc.removeObject(nm)
            n_ = doc.addObject("Part::Feature", nm)
            n_.Label, n_.Shape = lab, sh
            if col_:
                n_.ViewObject.ShapeColor = col_

    FX0, FX1 = 1000 - CORNER_CUT + FOOT_GAP, 1000 - FOOT_GAP     # Grundplatte im Eckausschnitt
    Z_FOOT1  = H_FRAME + FOOT_T
    COL_FOOT = (0.55, 0.57, 0.6)
    COL_HW   = (0.75, 0.75, 0.78)
    part("Fuss_Grundplatte", Part.makeBox(FX1 - FX0, FX1 - FX0, FOOT_T, Vector(FX0, FX0, H_FRAME)), COL_FOOT)
    # Wangen: an den Innenseiten (X_oben_hinten bei y = 960, Y_oben_rechts bei x = 960), volle Profilhoehe,
    # von oben mit der Grundplatte verschraubt. Zusammen mit der Grundplatte bilden sie einen Eckwinkel um beide Profile.
    IN = 1000 - P                                                    # Innenkante der Profile (960)
    part("Fuss_Wange_X", Part.makeBox(IN - CHEEK_T - FX0, CHEEK_T, P, Vector(FX0, IN - CHEEK_T, H_FRAME - P)), COL_FOOT)
    part("Fuss_Wange_Y", Part.makeBox(CHEEK_T, IN - FX0, P, Vector(IN - CHEEK_T, FX0, H_FRAME - P)), COL_FOOT)
    part("J1_Lagergehaeuse", Part.makeCylinder(HOUSING_D / 2, H_FRAME + BASE_H - Z_FOOT1, Vector(BASE_X, BASE_Y, Z_FOOT1)),
         (0.15, 0.15, 0.18))
    # J1-Motor haengt unter der Grundplatte in der Rahmenecke (geschuetzt unter der Platte), Riemen nach oben ins Gehaeuse
    part("J1_Motor_NEMA17_60", Part.makeBox(42, 42, 60, Vector(BASE_X - 60, BASE_Y - 60, H_FRAME - 60)), (0.1, 0.1, 0.1))

    # Schrauben und Nutensteine (Platzhalter). Nutmitte: 20 mm ab Profilkante.
    SC  = 1000 - SLOT_C                                              # obere Nuten bei y = 980 (X-Profil) bzw. x = 980 (Y-Profil)
    ZSC = H_FRAME - SLOT_C                                           # innere Nuten bei z = 700
    for s, prof in TOP_SCREWS:
        x, y = (s, SC) if prof == "X" else (SC, s)
        screws.append(Part.makeCylinder(SCREW_D / 2, Z_FOOT1 - (H_FRAME - NUT_D1), Vector(x, y, H_FRAME - NUT_D1)))
        screws.append(Part.makeCylinder(HEAD_D / 2, HEAD_H, Vector(x, y, Z_FOOT1)))
        a, b = (NUT_L, NUT_W) if prof == "X" else (NUT_W, NUT_L)
        nuts.append(Part.makeBox(a, b, NUT_D1 - NUT_D0, Vector(x - a / 2, y - b / 2, H_FRAME - NUT_D1)))
    for s, prof in SIDE_SCREWS:
        if prof == "X":       # durch Wange_X in die innere Nut von X_oben_hinten (Richtung +y)
            p0 = Vector(s, IN - CHEEK_T, ZSC)
            screws.append(Part.makeCylinder(SCREW_D / 2, CHEEK_T + NUT_D1, p0, Vector(0, 1, 0)))
            screws.append(Part.makeCylinder(HEAD_D / 2, HEAD_H, p0, Vector(0, -1, 0)))
            nuts.append(Part.makeBox(NUT_L, NUT_D1 - NUT_D0, NUT_W, Vector(s - NUT_L / 2, IN + NUT_D0, ZSC - NUT_W / 2)))
        else:                 # durch Wange_Y in die innere Nut von Y_oben_rechts (Richtung +x)
            p0 = Vector(IN - CHEEK_T, s, ZSC)
            screws.append(Part.makeCylinder(SCREW_D / 2, CHEEK_T + NUT_D1, p0, Vector(1, 0, 0)))
            screws.append(Part.makeCylinder(HEAD_D / 2, HEAD_H, p0, Vector(-1, 0, 0)))
            nuts.append(Part.makeBox(NUT_D1 - NUT_D0, NUT_L, NUT_W, Vector(IN + NUT_D0, s - NUT_L / 2, ZSC - NUT_W / 2)))


    n_scr = len(nuts)
    bom_foot = [
        ["Grundplatte Alu %.0f mm, %.0f x %.0f mm" % (FOOT_T, FX1 - FX0, FX1 - FX0), "(Zuschnitt/Fraesteil)", 1, "Stk",
         "liegt im Eckausschnitt auf X_oben_hinten + Y_oben_rechts"],
        ["Wange Alu %.0f mm, %.0f x %.0f mm" % (CHEEK_T, IN - CHEEK_T - FX0, P), "(Zuschnitt)", 1, "Stk", "Innenseite X_oben_hinten"],
        ["Wange Alu %.0f mm, %.0f x %.0f mm" % (CHEEK_T, IN - FX0, P), "(Zuschnitt)", 1, "Stk", "Innenseite Y_oben_rechts"],
        ["Zylinderschraube ISO 4762 M8x20", "ISO 4762-M8x20", len(TOP_SCREWS), "Stk", "senkrecht in die oberen Nuten"],
        ["Zylinderschraube ISO 4762 M8x16", "ISO 4762-M8x16", len(SIDE_SCREWS), "Stk", "waagerecht durch die Wangen"],
        ["Nutenstein einschwenkbar 40-Profil M8", "8-4-M8.40", n_scr, "Stk", "wie Rahmen"],
        ["Scheibe ISO 7089 8", "ISO 7089-8", n_scr, "Stk", ""],
        ["Zylinderschraube ISO 4762 M6x16 + Gewinde M6 in den Wangen", "ISO 4762-M6x16", 4, "Stk", "Grundplatte mit den Wangen verschrauben"]]
part("Fuss_Schrauben_M8", Part.makeCompound(screws), COL_HW)
part("Fuss_Nutensteine_M8", Part.makeCompound(nuts), COL_HW)

# ---------------- Drehsaeule (dreht mit J1) ----------------
col = Part.makeBox(COL_D, COL_W, COL_H, Vector(-COL_D / 2 - 40, -COL_W / 2, z_base_top))
col.rotate(Vector(0, 0, 0), Vector(0, 0, 1), math.degrees(q1))
col.translate(Vector(BASE_X, BASE_Y, 0))
part("Saeule_4080", col, (0.6, 0.6, 0.65))
zm = Part.makeBox(42, 42, 48, Vector(-21 - 40, -21, z_base_top + COL_H))
zm.rotate(Vector(0, 0, 0), Vector(0, 0, 1), math.degrees(q1))
zm.translate(Vector(BASE_X, BASE_Y, 0))
part("Z_Motor_NEMA17", zm, (0.1, 0.1, 0.1))

# ---------------- Oberarm, Ellbogen, Unterarm ----------------
car = Part.makeBox(30, 90, 90, Vector(-20, -45, z_link - 45))      # Z-Schlitten
car.rotate(Vector(0, 0, 0), Vector(0, 0, 1), math.degrees(q1))
car.translate(Vector(BASE_X, BASE_Y, 0))
part("Z_Schlitten", car, (0.15, 0.15, 0.18))
part("Oberarm_2040", bar(Vector(BASE_X, BASE_Y, z_link) + (E - Vector(BASE_X, BASE_Y, z_link)).normalize() * 10,
                         E, LINK_W, LINK_H))
j2m = Part.makeBox(42, 42, 48, Vector(40, LINK_W / 2 + 4, z_link - 24))
j2m.rotate(Vector(0, 0, 0), Vector(0, 0, 1), math.degrees(q1))
j2m.translate(Vector(BASE_X, BASE_Y, 0))
part("J2_Motor_NEMA17", j2m, (0.1, 0.1, 0.1))
part("J2_Lager", Part.makeCylinder(HUB_D / 2, LINK_H + 20, Vector(E.x, E.y, z_link - LINK_H / 2 - 10)), (0.15, 0.15, 0.18))
part("Unterarm_2040", bar(E, W, LINK_W, LINK_H))

# ---------------- Handgelenk ----------------
part("J4_Gieren_Schnecke", Part.makeCylinder(HUB_D / 2, (z_link + LINK_H / 2 + 15) - (z_j5 + 30),
                                             Vector(W.x, W.y, z_j5 + 30)), (0.15, 0.15, 0.18))
t = Vector(math.cos(psi), math.sin(psi), 0)        # Werkzeugachse (waagerecht)
n = Vector(-t.y, t.x, 0)                           # J5-Achse (waagerecht, quer)
J5 = Vector(W.x, W.y, z_j5)
j5box = Part.makeBox(70, 90, 60, Vector(-35, -45, -30))
j5box.Placement = Placement(J5, Rotation(Vector(0, 0, 1), math.degrees(psi)))
part("J5_Nicken_Schnecke", j5box, (0.15, 0.15, 0.18))

# Werkzeugkette ab J5: um J5-Achse (n) nicken, um Werkzeugachse rollen
rot_tool = Rotation(n, -PITCH).multiply(Rotation(Vector(0, 0, 1), math.degrees(psi))).multiply(Rotation(Vector(1, 0, 0), ROLL))
def tool(shape):
    shape.Placement = Placement(J5, rot_tool).multiply(shape.Placement)
    return shape
part("J6_Rollen", tool(Part.makeCylinder(25, J6_L, Vector(J5_FRONT, 0, 0), Vector(1, 0, 0))), (0.15, 0.15, 0.18))
part("Kupplung_3Kugeln", tool(Part.makeCylinder(CPL_D / 2, CPL_T, Vector(J5_FRONT + J6_L, 0, 0), Vector(1, 0, 0))), (0.85, 0.6, 0.1))

# ---------------- Traeger: Platinenrahmen mit Randbacken und Stuetzstiften ----------------
x0 = J5_FRONT + J6_L + CPL_T                       # Rahmen beginnt an der Kupplung
fr = Part.makeBox(CARRIER_L, CARRIER_W, CARRIER_T, Vector(x0, -CARRIER_W / 2, -CARRIER_T / 2 - 10))
fr = fr.cut(Part.makeBox(CARRIER_L - 24, CARRIER_W - 24, CARRIER_T + 2, Vector(x0 + 12, -CARRIER_W / 2 + 12, -CARRIER_T / 2 - 11)))
part("Traeger_Rahmen", tool(fr), (0.85, 0.6, 0.1))
pcb_z = CARRIER_T / 2 - 10 - 4
part("Platine", tool(Part.makeBox(PCB_L, PCB_W, PCB_T, Vector(x0 + (CARRIER_L - PCB_L) / 2, -PCB_W / 2, pcb_z))), (0.1, 0.5, 0.2))
pins = []
nx = int(PCB_L // PIN_PITCH)
ny = int(PCB_W // PIN_PITCH)
for i in range(nx):
    for j in range(ny):
        px = x0 + CARRIER_L / 2 + (i - (nx - 1) / 2) * PIN_PITCH
        py = (j - (ny - 1) / 2) * PIN_PITCH
        pins.append(Part.makeCylinder(2.5, 14, Vector(px, py, pcb_z - 14)))
if pins:
    part("Stuetzstifte", tool(Part.makeCompound(pins)), (0.8, 0.8, 0.8))

doc.recompute()

# ---------------- Pruefung ----------------
print("\nArm 1 Halter (Konzept): J1 %.1f  J2 %.1f  J4 %.1f  Grad | Hub %.0f mm von %.0f | J5 %.0f  J6 %.0f Grad"
      % (math.degrees(q1), math.degrees(q2), math.degrees(q4), z_lift, Z_STROKE, PITCH, ROLL))
print("Handgelenk-Abstand zur J1-Achse: %.0f mm (%.0f %% von %.0f)" % (r, 100 * r / (L1 + L2), L1 + L2))
frame_objs = [o for o in doc.Objects if not o.Name.startswith("A1_") and hasattr(o, "Shape")
              and not o.Shape.isNull() and o.Shape.Volume > 1]
hits = []
for a in arm_objs:
    for f in frame_objs:
        if not a.Shape.BoundBox.intersect(f.Shape.BoundBox):
            continue
        try:
            v = a.Shape.common(f.Shape).Volume
        except Exception:
            v = 0
        if v > 1.0:
            hits.append((a.Label, f.Label, v))
ok_pairs = set()   # Schrauben/Nutensteine liegen in den Nuten und sollen das Profil nicht schneiden: keine Ausnahmen
hits = [h for h in hits if (h[0], h[1]) not in ok_pairs]
print("Kollisionen Arm/Tisch: %s" % ("keine" if not hits else "; ".join("%s / %s (%.0f mm3)" % h for h in hits)))
# Lastabschaetzung Fuss (grob): Kippmoment ueber einen Hebel von ca. 150 mm auf je 2 Schrauben
print("Fuss (%s): %d Schrauben M8. Kippmoment %.0f Nm -> ca. %.0f N je Schraube"
      % (MOUNT, n_scr, TIP_MOMENT, TIP_MOMENT * 1000 / 150.0 / 2))

# ---------------- Stueckliste Fuss (Befestigung am Rahmen) ----------------
try:
    import csv
    rows = [["Pos", "Artikel", "Artikelnr", "Menge", "Einheit", "Bemerkung"]] + [[k + 1] + r for k, r in enumerate(bom_foot)]
    with open(os.path.join(REPO, "bom", "arm1_fuss_bom.csv"), "w", newline="", encoding="utf-8") as fh:
        csv.writer(fh, delimiter=";").writerows(rows)
    print("BOM: bom/arm1_fuss_bom.csv (%s)" % MOUNT)
except Exception as e:
    print("BOM nicht geschrieben:", e)

try:
    import FreeCADGui as Gui
    Gui.ActiveDocument.ActiveView.viewIsometric()
    Gui.SendMsgToActiveView("ViewFit")
except Exception:
    pass
