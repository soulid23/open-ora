import FreeCAD as App
import Part
from FreeCAD import Vector, Rotation, Placement

# ---------- Parameter (mm) ----------
P     = 40      # Profilmaß 4040
W     = 500     # Tischbreite  (X)
D     = 600     # Tischtiefe   (Y)
H     = 150     # Gesamthöhe Rahmen (Z)
PLATE = 12      # Plattenstärke (Siebdruck)
# ------------------------------------

doc = App.newDocument("OpenORA_Frame")
bom = {}

def profile(L):
    """Vereinfachtes 4040-Profil (Nut B, 8 mm), Querschnitt um die Achse zentriert."""
    s = Part.makeBox(P, P, L, Vector(-P/2, -P/2, 0))
    opening = Part.makeBox(4.6, 8,  L + 2, Vector(P/2 - 4.5, -4, -1))
    cavity  = Part.makeBox(5.5, 16, L + 2, Vector(P/2 - 10, -8, -1))
    slot = opening.fuse(cavity)
    for angle in (0, 90, 180, 270):
        sl = slot.copy()
        sl.rotate(Vector(0, 0, 0), Vector(0, 0, 1), angle)
        s = s.cut(sl)
    s = s.cut(Part.makeCylinder(3.4, L, Vector(0, 0, 0)))  # Mittelbohrung
    return s

def add(name, L, start, axis):
    """Profil der Länge L ab 'start' entlang axis ('X', 'Y' oder 'Z')."""
    rot = {"X": Rotation(Vector(0, 1, 0), 90),
           "Y": Rotation(Vector(1, 0, 0), -90),
           "Z": Rotation()}[axis]
    obj = doc.addObject("Part::Feature", name)
    obj.Shape = profile(L)
    obj.Placement = Placement(Vector(*start), rot)
    bom[L] = bom.get(L, 0) + 1

zb, zt = P/2, H - P/2   # Mittelhöhe untere/obere Ebene

# Lange Träger (Y-Richtung), unten und oben
for z, tag in ((zb, "unten"), (zt, "oben")):
    for x, side in ((P/2, "links"), (W - P/2, "rechts")):
        add(f"Laengs_{tag}_{side}", D, (x, 0, z), "Y")

# Kurze Träger (X-Richtung) zwischen den langen
for z, tag in ((zb, "unten"), (zt, "oben")):
    for y, side in ((P/2, "vorne"), (D - P/2, "hinten")):
        add(f"Quer_{tag}_{side}", W - 2*P, (P, y, z), "X")

# Pfosten in den vier Ecken
for x, xs in ((P/2, "L"), (W - P/2, "R")):
    for y, ys in ((P/2, "V"), (D - P/2, "H")):
        add(f"Pfosten_{xs}{ys}", H - 2*P, (x, y, P), "Z")

# Arbeitsplatte (liegt auf dem oberen Rahmen)
plate = doc.addObject("Part::Box", "Platte")
plate.Length, plate.Width, plate.Height = W, D, PLATE
plate.Placement = Placement(Vector(0, 0, H), Rotation())

doc.recompute()
try:
    import FreeCADGui as Gui
    Gui.ActiveDocument.ActiveView.viewIsometric()
    Gui.SendMsgToActiveView("ViewFit")
except Exception:
    pass

print("Stückliste 4040-Zuschnitt (Länge mm: Anzahl):", bom)