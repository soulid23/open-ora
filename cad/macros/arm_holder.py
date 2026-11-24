# open-ora | cad/macros/arm_holder.py | v1 (Konzept, Platzhaltergeometrie)
# Arm 1 "Halter" auf dem Tisch v8, hinten rechts auf dem Aluframe: SCARA mit Hubsaeule und 3-Achs-Handgelenk, Traeger-Kupplung, Platinenrahmen.
#   J1 Drehung Saeule (senkrecht, Riemen 1:20) | Z Hub (TR8x2, selbsthemmend) | J2 Ellbogen (senkrecht, Riemen 1:12)
#   J4 Gieren (Schnecke 1:30) | J5 Nicken (Schnecke 1:30) | J6 Rollen (Schnecke 1:20) | Kupplung (3 Kugeln / 3 Nuten)
# Siehe docs/decisions/0007-arm1-halter-konzept.md und cad/analysis/arm_holder_sizing.py.
# Koordinaten wie frame_4040.py: X links->rechts (Blick von vorn), Y 0 = vorn (Sitzseite), Z ab Boden.
# Alle Koerper sind Platzhalter fuer Bauraum und Kollisionspruefung, keine Fertigungsteile.
# Start in FreeCAD: exec(open(r"C:\dev\open-ora\cad\macros\arm_holder.py").read())

import math
import os
import FreeCAD as App
import Part
from FreeCAD import Vector, Rotation, Placement

# ---------------- Parameter (mm, Grad) ----------------
REPO          = r"C:\dev\open-ora"
INCLUDE_FRAME = True              # Tisch aus frame_4040.py mitzeichnen (ohne die BOM neu zu schreiben)
DESK_H        = 740.0             # Oberkante ESD-Matte (wie frame_4040.py)
PLATE_TOP     = DESK_H - 2.0      # Oberkante Siebdruckplatte (Referenz)
H_FRAME       = 720.0             # Oberkante oberer Rahmen = Unterseite Platte
P             = 40.0

BASE_X, BASE_Y = 920.0, 920.0     # J1-Achse hinten rechts
CORNER_CUT    = 170.0             # Eckausschnitt in Platte und Matte; der Fuss steht direkt auf dem Aluframe
                                  # (X_oben_hinten + Y_oben_rechts, ueber Pfosten_RH), Nutensteine in den oberen Nuten

BASE_H        = 90.0              # J1-Gehaeuse ab Rahmenoberkante (Lagerpaar, Riemenstufe), 70 mm ueber der Matte
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
if INCLUDE_FRAME:
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

# ---------------- Unterbau ----------------
# Eckausschnitt in Siebdruckplatte und ESD-Matte (Fuss steht auf dem Rahmen)
corner = Part.makeBox(CORNER_CUT + 1, CORNER_CUT + 1, 100, Vector(1000 - CORNER_CUT, 1000 - CORNER_CUT, H_FRAME - 1))
for nm in ("Platte", "ESD_Matte"):
    o = doc.getObject(nm)
    if o is not None and o.TypeId == "Part::Box":
        sh = o.Shape.cut(corner)
        col_ = o.ViewObject.ShapeColor if o.ViewObject else None
        doc.removeObject(nm)
        n_ = doc.addObject("Part::Feature", nm)
        n_.Shape = sh
        if col_:
            n_.ViewObject.ShapeColor = col_
part("J1_Gehaeuse", Part.makeBox(CORNER_CUT, CORNER_CUT, BASE_H, Vector(1000 - CORNER_CUT, 1000 - CORNER_CUT, H_FRAME)), (0.15, 0.15, 0.18))
# J1-Motor haengt unter dem Gehaeuse in der Rahmenecke (geschuetzt unter der Platte)
part("J1_Motor_NEMA17_60", Part.makeBox(42, 42, 60, Vector(BASE_X - 60, BASE_Y - 60, H_FRAME - 60)), (0.1, 0.1, 0.1))

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
ok_pairs = set()
hits = [h for h in hits if (h[0], h[1]) not in ok_pairs]
print("Kollisionen Arm/Tisch: %s" % ("keine" if not hits else "; ".join("%s / %s (%.0f mm3)" % h for h in hits)))
try:
    import FreeCADGui as Gui
    Gui.ActiveDocument.ActiveView.viewIsometric()
    Gui.SendMsgToActiveView("ViewFit")
except Exception:
    pass
