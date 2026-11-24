# open-ora | cad/macros/frame_4040.py | v6 (Branding: Wortmarke open-ora mit Zeichen als o + open-ora.de auf den Forex-Platten)
# Tisch 1000 x 1000 mm aus Alux Nutprofil 4040 (aluxprofil.de, Art.-Nr. 4040), vorn/hinten = Y=0 / Y=D.
# Tischhoehe DESK_H (Oberkante ESD-Matte) ist Parameter; die Pfosten/Fuesse ergeben sich daraus.
# Obere Ebene: lange X-Traeger nehmen die komplette Breite ein. Untere Ebene (Rack-Boden): zwischen den Pfosten.
# Standfestigkeit: Bodenstreben hinten + seitlich, Eckstreben 45 Grad (4040) unter dem unteren Rahmen (oder 2020-Diagonalen), Mittelträger.
# Rack-Raum 3 HE; Schublade (hinten, 1. HE) haengt an den hinteren Schienen und den Tiefenschienen (Mittelträger).
# Sitzplatz: Vorderseite (Y=0) bleibt unter der Platte frei (FRONT_RACK = False): kein unterer Traeger, keine Rack-Schienen.
# Berechnung der Steifigkeit: cad/analysis/frame_stiffness.py
# Datenblatt 4040: 40x40, Nut 8 mm (+0,3), Nuttiefe 12 mm, Kernbohrung 6,8 mm,
#                  Flaeche 504,8 mm2, 1,395 kg/m, EN-AW 6063 T66
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
W      = 1000                     # Tischbreite  (X)
D      = 1000                     # Tischtiefe   (Y)
SLOT, SLOT_DEPTH, LIP, CAVITY_W = 8.0, 12.0, 4.0, 16.0   # Nut (CAVITY_W und LIP geschaetzt)
CORE_BORE = 6.8
KG_PER_M  = 1.395
AREA_REF  = 504.8                 # Datenblatt, zur Pruefung des STEP-Querschnitts
USE_STEP  = True
STEP_FILE = next((os.path.join(d, "alux_4040.STEP") for d in ASSET_DIRS
                  if os.path.exists(os.path.join(d, "alux_4040.STEP"))),
                 os.path.join(ASSET_DIRS[0], "alux_4040.STEP"))
ANGLES_PER_JOINT = 2              # Winkel 4040 je Verbindung
# ----- Hoehenaufbau (Z) -----
PLATE        = 18                 # Siebdruckplatte (12 mm waere bei 1 m Spannweite zu weich, siehe cad/analysis)
ESD_T        = 2                  # ESD-Matte
DESK_H       = 740                # Tischhoehe = Oberkante ESD-Matte (Schreibtisch ca. 720-750 mm)
U            = 44.45              # 1 HE
RACK_U       = 3                  # Rack-Raum: 3 HE
RACK_EXTRA   = 1.05               # Luft im Rack-Raum (Adam-Hall-Blenden sind 44,5 mm hoch)
RACK_CLEAR   = RACK_U * U + RACK_EXTRA   # lichte Hoehe = 134,4 mm
FOOT_H       = DESK_H - (P + RACK_CLEAR + P + PLATE + ESD_T)   # Unterkante unterer Rahmen (Beinlaenge darunter)
Z_LOW0       = FOOT_H             # Unterkante unterer Rahmen
Z_LOW1       = Z_LOW0 + P         # Oberkante unterer Rahmen = Beginn Rack-Raum
Z_UP0        = Z_LOW1 + RACK_CLEAR   # Unterkante oberer Rahmen = Pfostenende
H            = Z_UP0 + P         # Oberkante Rahmen = Unterseite Platte
BRACE_Z0     = 100                # Unterkante der Bodenstreben (hinten + seitlich)
FRONT_RACK   = False              # False: Sitzseite vorn frei; True: 19"-Rack auch vorn (dann kein Sitzplatz vorn)
MID_Y        = 620                # Mittelträger (oben + unten) und Tiefenschienen der Schublade (Y-Mitte)
                                  # Beinraumtiefe ab Tischkante = MID_Y - P/2 (hier 600 mm)

# ----- 19"-Rack (EIA-310): Schienen aus 2020 vorn und hinten -----
R            = 20                 # Profilmass 2020
RACK_PITCH   = 465.1              # Abstand der Nutmitten = Lochabstand der 19"-Winkel
                                  # (lichte Weite zwischen den Schienen dann 445,1 mm)
HOLE_D       = 6.5                # Befestigungsloecher der Blenden

# ----- Adam Hall 19" Parts (Daten aus Produktseiten/Haendlerangaben, gegen 2D-Zeichnung pruefen) -----
PANEL_W      = 484.0              # Breite der Blenden und der Schublade
PANEL_UH     = 44.5               # Hoehe 1 HE laut Hersteller
D12_T        = 1.5                # RACK U PAN 01 D12 TIE BAR (872215): Stahl 1,5 mm
D_HOLE       = 24.3               # D-Ausschnitt (Neutrik D-Format, ca. 24 mm)
D_PITCH      = 36.0               # PLATZHALTER: Lochabstand der 12 D-Loecher aus der 2D-Zeichnung uebernehmen!
N_D          = 12
TRAY_T       = 1.6                # RACK TRAY 01 PULLOUT (87556): Stahl 1,6 mm
TRAY_BODY_W  = 435.0              # Breite des Schubladenkoerpers
TRAY_BODY_H  = 40.0               # PLATZHALTER
TRAY_MOUNT_D = D - (MID_Y + R / 2)  # Einbautiefe: Aussenflaeche hinten bis Tiefenschiene (Hersteller 360-480 mm)
TRAY_BODY_D  = TRAY_MOUNT_D       # Schubladenkoerper-Platzhalter

# ----- Belegung (Einheit 1 = unterste; D-Loch-Nr. von links, Blick von aussen) -----
REAR_TRAY_U  = 1
BRACING      = "knee"           # "knee": Eckstreben 4040 mit Alux 4040-45 | "diag": 2020-Diagonalen mit Knotenblechen
CLAD         = True               # Forex-Fuellplatten in die 8-mm-Nut der 4040-Profile (Rackband, Seiten + hinten)
FOREX_T      = 5.0                # Forex classic 5 mm; Alux-Einfassprofil 8-12.40 nimmt 4-6 mm
SLOT_INS     = 8.0                # Einschubtiefe der Platte in die Nut (Nuttiefe ca. 12 mm, Rest fuer Einfassprofil/Spiel)
RACK_WIN_W   = 486.0              # Ausschnitt hinten: Blenden 484 mm + 1 mm Luft je Seite
# ----- Branding der Forex-Platten (Logo "Offenes O", docs/branding) -----
LOGO_MODE    = "druck"            # "druck": Platte dunkel, Logo als Druckschicht (Sponsor Lehmann) | "gravur": Logo eingraviert
LOGO_LAYOUT  = os.path.join(REPO, "docs", "branding", "forex_layout.json")   # Logo-Umrisse in mm je Plattentyp (aus docs/branding/tools/gen_forex.py)
LOGO_DEPTH   = 0.8                # Gravurtiefe (mm) in der Aussenseite der Platte (nur "gravur")
PRINT_T      = 0.1                # Dicke der Druckschicht im Modell (nur zur Darstellung, "druck")
COL_INK      = (0.086, 0.094, 0.106)   # #16181B
COL_LIGHT    = (0.957, 0.949, 0.933)   # #F4F2EE
COL_ACCENT   = (0.910, 0.455, 0.231)   # #E8743B
COL_TAG      = (0.788, 0.776, 0.753)   # #C9C6C0 (Unterzeile)
REAR_D12_U   = 3
FRONT_D12_U  = 3
REAR_D12     = {1: "powerCON_IN_blau", 2: "powerCON_OUT_weiss", 3: "Cat_etherCON"}   # Rest: Blindkappen
FRONT_D12    = {}                                                                    # vorerst alles Blindkappen

# ----- Fuesse: Alux Gelenkstellfuss 80 mm, M8x50 (Art. 80-M8x50), direkt in den M8-Gewindekern des 4040-Pfostens -----
FOOT_STACK   = 50.0               # PLATZHALTER: Bauhoehe Fuss unter dem Pfosten (Mittelstellung), aus STEP "80mm stelvoet ... M8x50 spindel" uebernehmen
FOOT_D       = 80.0               # Durchmesser der Gummiauflage
FOOT_PAD_H   = 12.0               # PLATZHALTER: Hoehe der Gummiauflage
FOOT_NECK_D  = 24.0               # PLATZHALTER: Durchmesser Gelenkkopf
FOOT_TRAVEL  = 15.0               # Verstellweg nach oben und unten ab Mittelstellung (Gewindelaenge 50 mm, ANNAHME)
ESD_MARGIN = 10                   # Matte liegt 10 mm eingerueckt auf der Platte
# ------------------------------------------------

doc = App.newDocument("OpenORA_Frame")
beams = []                        # (Name, Laenge)


# ---------- Profil-Querschnitt ----------
def section_from_step(path):
    """Liest die Hersteller-STEP, schneidet den Querschnitt aus und gibt eine Flaeche
    in der XY-Ebene (zentriert, z=0) zurueck. Rueckgabe None bei Problemen (mit Grund in der Konsole)."""
    import traceback
    try:
        size = os.path.getsize(path)
        print("STEP gefunden: %s (%d Bytes)" % (path, size))
        if size < 1000:
            print("Datei ist zu klein (Nextcloud-Platzhalter? 'Immer auf diesem Geraet behalten' waehlen).")
            return None
        shp = Part.read(path)
        bb = shp.BoundBox
        print("STEP-Abmessungen: %.1f x %.1f x %.1f mm" % (bb.XLength, bb.YLength, bb.ZLength))
        lens = [bb.XLength, bb.YLength, bb.ZLength]
        ax = lens.index(max(lens))
        normal = [Vector(1, 0, 0), Vector(0, 1, 0), Vector(0, 0, 1)][ax]
        mid = [bb.Center.x, bb.Center.y, bb.Center.z][ax]
        wires = shp.slice(normal, mid)
        print("Schnittkonturen: %d" % len(wires))
        try:
            face = Part.makeFace(wires, "Part::FaceMakerBullseye")
        except Exception:
            faces = sorted((Part.Face(w) for w in wires), key=lambda f: -f.Area)
            face = Part.Face([faces[0].OuterWire] + [f.OuterWire for f in faces[1:]])
        if ax == 0:
            face.rotate(Vector(0, 0, 0), Vector(0, 1, 0), -90)
        elif ax == 1:
            face.rotate(Vector(0, 0, 0), Vector(1, 0, 0), 90)
        c = face.BoundBox.Center
        face.translate(Vector(-c.x, -c.y, -face.BoundBox.ZMin))
        if abs(face.Area - AREA_REF) / AREA_REF > 0.05:
            print("STEP-Querschnitt weicht ab (%.1f mm2, Soll %.1f), nutze Ersatzprofil." % (face.Area, AREA_REF))
            return None
        print("STEP-Querschnitt geladen, Flaeche %.1f mm2 (Soll %.1f)." % (face.Area, AREA_REF))
        return face
    except Exception:
        print("STEP konnte nicht ausgewertet werden:")
        print(traceback.format_exc())
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


if USE_STEP and os.path.exists(STEP_FILE):
    SECTION = section_from_step(STEP_FILE)
else:
    SECTION = None
    if USE_STEP:
        print("STEP-Datei NICHT gefunden. Gesucht in:")
        for d in ASSET_DIRS:
            print("  ", os.path.join(d, "alux_4040.STEP"))
print("Profil:", "STEP-Querschnitt" if SECTION is not None else "Ersatzprofil")


def color(o, rgb):
    try:
        o.ViewObject.ShapeColor = rgb
    except Exception:
        pass

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
zl = Z_LOW0 + P / 2                 # Mittelhoehe untere Ebene
zu = Z_UP0 + P / 2                  # Mittelhoehe obere Ebene

# Obere Ebene: lange X-Traeger (600 mm) nehmen die komplette Breite ein, Y-Traeger dazwischen
for y, side in ((P / 2, "vorn"), (D - P / 2, "hinten")):
    add("X_oben_%s" % side, W, (0, y, zu), "X")
for x, side in ((P / 2, "links"), (W - P / 2, "rechts")):
    add("Y_oben_%s" % side, D - 2 * P, (x, P, zu), "Y")

# Untere Ebene: alles zwischen den durchgehenden Pfosten
for y, side in ((P / 2, "vorn"), (D - P / 2, "hinten")):
    if side == "vorn" and not FRONT_RACK:
        continue                  # Sitzseite: kein Traeger in Knie- und Schienbeinhoehe
    add("X_unten_%s" % side, W - 2 * P, (P, y, zl), "X")
for x, side in ((P / 2, "links"), (W - P / 2, "rechts")):
    add("Y_unten_%s" % side, D - 2 * P, (x, P, zl), "Y")

# Mittelträger (stuetzen die Platte und tragen die Tiefenschienen der Schublade)
add("X_oben_mitte", W - 2 * P, (P, MID_Y, zu), "X")
add("X_unten_mitte", W - 2 * P, (P, MID_Y, zl), "X")

# Bodenstreben (Querstreben) hinten und seitlich; vorne bleibt frei (Beinraum)
zf = BRACE_Z0 + P / 2
add("X_boden_hinten", W - 2 * P, (P, D - P / 2, zf), "X")
for x, side in ((P / 2, "links"), (W - P / 2, "rechts")):
    add("Y_boden_%s" % side, D - 2 * P, (x, P, zf), "Y")

# Pfosten = Fuesse: vom Boden bis unter den oberen Rahmen
for x, xs in ((P / 2, "L"), (W - P / 2, "R")):
    for y, ys in ((P / 2, "V"), (D - P / 2, "H")):
        add("Pfosten_%s%s" % (xs, ys), Z_UP0 - FOOT_STACK, (x, y, FOOT_STACK), "Z")

# Gelenkstellfuesse (Platzhalter-Geometrie), mittig unter dem Pfosten
for x, xs in ((P / 2, "L"), (W - P / 2, "R")):
    for y, ys in ((P / 2, "V"), (D - P / 2, "H")):
        fo = doc.addObject("Part::Feature", "Fuss_%s%s" % (xs, ys))
        pad = Part.makeCylinder(FOOT_D / 2, FOOT_PAD_H, Vector(x, y, 0))
        neck = Part.makeCylinder(FOOT_NECK_D / 2, 8, Vector(x, y, FOOT_PAD_H))
        spindle = Part.makeCylinder(4, FOOT_STACK - FOOT_PAD_H - 4, Vector(x, y, FOOT_PAD_H + 4))
        fo.Shape = pad.fuse(neck).fuse(spindle)
        color(fo, (0.1, 0.1, 0.1))

# ---------- Platte, ESD-Matte, Erdungspunkt ----------
plate = doc.addObject("Part::Box", "Platte")
plate.Length, plate.Width, plate.Height = W, D, PLATE
plate.Placement = Placement(Vector(0, 0, H), Rotation())

esd = doc.addObject("Part::Box", "ESD_Matte")
esd.Length, esd.Width, esd.Height = W - 2 * ESD_MARGIN, D - 2 * ESD_MARGIN, ESD_T
esd.Placement = Placement(Vector(ESD_MARGIN, ESD_MARGIN, H + PLATE), Rotation())

# Erdungspunkt: Markierung an der Aussenflaeche von Pfosten_LH (hinten links), Mitte Rack-Raum
gnd = doc.addObject("Part::Feature", "Erdungspunkt")
gnd.Shape = Part.makeCylinder(6, 3, Vector(-3, D - P / 2, Z_LOW1 + RACK_CLEAR / 2), Vector(1, 0, 0))

# ---------- 19"-Schienen (2020) ----------
# Vorn (y=0) und hinten (y=D): je zwei senkrechte 2020-Schienen im Rack-Raum, Nutmitte auf dem 19"-Lochabstand,
# buendig mit der Rahmenaussenflaeche.
def profile20(L):
    """Vereinfachtes 2020 (Nut 6, M5). Nutgeometrie nur angenaehert."""
    s_ = Part.makeBox(R, R, L, Vector(-R / 2, -R / 2, 0))
    xo = R / 2
    opening = Part.makeBox(2.0, 6.2, L + 2, Vector(xo - 1.8, -3.1, -1))
    cavity = Part.makeBox(4.3, 7.6, L + 2, Vector(xo - 6.1, -3.8, -1))
    slot = opening.fuse(cavity)
    for a_ in (0, 90, 180, 270):
        sl = slot.copy()
        sl.rotate(Vector(0, 0, 0), Vector(0, 0, 1), a_)
        s_ = s_.cut(sl)
    return s_.cut(Part.makeCylinder(2.1, L, Vector(0, 0, 0)))

RAIL_L = RACK_CLEAR
for side, yc in (("vorn", R / 2), ("hinten", D - R / 2)):
    if side == "vorn" and not FRONT_RACK:
        continue
    for tag, xc in (("L", W / 2 - RACK_PITCH / 2), ("R", W / 2 + RACK_PITCH / 2)):
        o = doc.addObject("Part::Feature", "Rack_Schiene_%s_%s" % (side, tag))
        o.Shape = profile20(RAIL_L)
        o.Placement = Placement(Vector(xc, yc, Z_LOW1), Rotation())

# Tiefenschienen: tragen das hintere Ende der Auszugschublade (senkrecht zwischen den Mittelträgern)
for tag, xc in (("L", W / 2 - RACK_PITCH / 2), ("R", W / 2 + RACK_PITCH / 2)):
    o = doc.addObject("Part::Feature", "Rack_Tiefenschiene_%s" % tag)
    o.Shape = profile20(RAIL_L)
    o.Placement = Placement(Vector(xc, MID_Y, Z_LOW1), Rotation())

# Rack-Zarge: je Seite zwei waagerechte 2020-Profile (oben, unten) zwischen hinterer Rack-Schiene und Tiefenschiene.
# Sie liegen auf der Schienenachse und laufen an der Schubladenkante vorbei (Schublade 435 mm breit, Profil bei x = 257..277).
ZARGE_Y0 = MID_Y + R / 2
ZARGE_L = (D - R) - ZARGE_Y0
for tag, xc in (("L", W / 2 - RACK_PITCH / 2), ("R", W / 2 + RACK_PITCH / 2)):
    for lvl, zc_ in (("unten", Z_LOW1 + R / 2), ("oben", Z_UP0 - R / 2)):
        o = doc.addObject("Part::Feature", "Rack_Zarge_%s_%s" % (tag, lvl))
        o.Shape = profile20(ZARGE_L)
        o.Placement = Placement(Vector(xc, ZARGE_Y0, zc_), Rotation(Vector(1, 0, 0), -90))

# ---------- Diagonalen (2020, im Feld zwischen Bodenstreben und unterem Rahmen) ----------
DIAG_TRIM = 30.0                  # Abstand der Diagonalenenden zur Innenecke (Platz auf dem Knotenblech)
GUSSET_T  = 4.0                   # Knotenblech Alu 4 mm, liegt auf der Innenflaeche der 4040-Profile
GUSSET_G  = 130.0                 # Kantenlaenge des quadratischen Knotenblechs (liegt ueber beiden Profilen der Ecke)
diags = []
gussets = []

def diag20(name, p0, p1):
    d = p1 - p0
    full = d.Length
    d.normalize()
    start = p0 + d * DIAG_TRIM
    L = full - 2 * DIAG_TRIM
    o = doc.addObject("Part::Feature", name)
    o.Shape = profile20(L)
    o.Placement = Placement(start, Rotation(Vector(0, 0, 1), d))
    diags.append(L)

def gusset(name, plane, face, corner, sh, sv):
    """Knotenblech in einer Innenecke. plane 'x' (Seitenwand, Flaeche bei x=face) oder 'y' (Rueckwand, Flaeche bei y=face).
    corner = (h, z): Innenecke in der Wandebene (h = y bzw. x). sh/sv = +1/-1: Richtung, in die das Blech vom Eckpunkt aus in den freien Raum reicht.
    Das Blech liegt nach innen (zur Tischmitte) auf der Profilflaeche und wird in die Nut beider Profile geschraubt (M8)."""
    # Das Blech liegt auf den Flaechen BEIDER Profile der Ecke: es beginnt 10 mm vor der Nutmitte des Profils,
    # das die Ecke bildet (Nutmitte = 20 mm hinter der Innenecke), und reicht G mm in den Raum hinein.
    h0 = corner[0] - (P / 2 + 10) if sh > 0 else corner[0] + (P / 2 + 10) - GUSSET_G
    z0 = corner[1] - (P / 2 + 10) if sv > 0 else corner[1] + (P / 2 + 10) - GUSSET_G
    if plane == "y":     # Rueckwand: Flaeche y = D - P, nach innen = -y
        box = Part.makeBox(GUSSET_G, GUSSET_T, GUSSET_G, Vector(h0, face - GUSSET_T, z0))
    else:                # Seitenwand: Flaeche x = P (links, nach innen +x) bzw. W - P (rechts, nach innen -x)
        x0 = face if face < W / 2 else face - GUSSET_T
        box = Part.makeBox(GUSSET_T, GUSSET_G, GUSSET_G, Vector(x0, h0, z0))
    # Dort, wo ein quer anschliessendes Profil im Weg ist, bekommt das Blech eine Ausklinkung
    for f in doc.Objects:
        if f.Name.startswith(("Pfosten", "X_", "Y_")) and f.Shape.BoundBox.intersect(box.BoundBox):
            box = box.cut(f.Shape)
    o = doc.addObject("Part::Feature", name)
    o.Shape = box
    color(o, (0.75, 0.75, 0.78))
    gussets.append(name)

if BRACING == "diag":
    zb0 = BRACE_Z0 + P               # Oberkante Bodenstrebe
    OFF = GUSSET_T + R / 2           # Diagonale liegt auf dem Knotenblech, nach innen versetzt
    yi, xl, xr = D - P, P, W - P     # Innenflaechen: Rueckwand, linke und rechte Seitenwand

    # Rueckwand: von unten links nach oben rechts
    diag20("Diagonale_hinten", Vector(xl, yi - OFF, zb0), Vector(xr, yi - OFF, Z_LOW0))
    gusset("Knotenblech_hinten_unten", "y", yi, (xl, zb0), +1, +1)
    gusset("Knotenblech_hinten_oben", "y", yi, (xr, Z_LOW0), -1, -1)
    # linke Seitenwand: von vorn unten nach hinten oben
    diag20("Diagonale_links", Vector(xl + OFF, P, zb0), Vector(xl + OFF, yi, Z_LOW0))
    gusset("Knotenblech_links_unten", "x", xl, (P, zb0), +1, +1)
    gusset("Knotenblech_links_oben", "x", xl, (yi, Z_LOW0), -1, -1)
    # rechte Seitenwand: von hinten unten nach vorn oben
    diag20("Diagonale_rechts", Vector(xr - OFF, yi, zb0), Vector(xr - OFF, P, Z_LOW0))
    gusset("Knotenblech_rechts_unten", "x", xr, (yi, zb0), -1, +1)
    gusset("Knotenblech_rechts_oben", "x", xr, (P, Z_LOW0), +1, -1)


# ---------- Eckstreben 45 Grad (4040) mit Alux-Winkelverbinder 4040-45 ----------
# Je Wand (links, rechts, hinten) und je Pfosten eine Strebe unter dem unteren Rahmen: Pfosten und Traeger werden im 45-Grad-Dreieck
# verbunden. Die Streben liegen in der Profilebene (Wanddicke 40 mm) und ragen nicht in den Beinraum.
KNEE_A    = 250.0                 # Schenkel: Abstand der Befestigungspunkte von der Innenecke (Pfosten- bzw. Traegerflaeche)
KNEE_TRIM = 35.0                  # PLATZHALTER: Abstand Strebenende - Befestigungspunkt (Hoehe des Verbinders 4040-45, aus STEP uebernehmen)
KNEE_W    = 40.0                  # PLATZHALTER: Verbinderbreite (Richtung quer zur Wandebene)
knees = []
connectors = []

def knee_brace(wall, hp, sh, tag):
    """wall: 'links' | 'rechts' | 'hinten'; hp: Lage der Pfostenflaeche in der Wandebene; sh: Richtung (+1/-1) vom Pfosten weg."""
    base = {"links": (0.0, "x"), "rechts": (W - P, "x"), "hinten": (D - P, "y")}[wall]
    def to3(h, z):
        return Vector(base[0], h, z) if base[1] == "x" else Vector(h, base[0], z)
    nrm = Vector(1, 0, 0) if base[1] == "x" else Vector(0, 1, 0)
    zb = Z_LOW0                                   # Unterseite des unteren Traegers
    f_post = (hp, zb - KNEE_A)                    # Befestigungspunkt auf der Pfostenflaeche
    f_beam = (hp + sh * KNEE_A, zb)               # Befestigungspunkt unter dem Traeger
    dv = (f_beam[0] - f_post[0], f_beam[1] - f_post[1])
    ln = (dv[0] ** 2 + dv[1] ** 2) ** 0.5
    d = (dv[0] / ln, dv[1] / ln)
    n = (-d[1], d[0])                             # Normale in der Wandebene
    e1 = (f_post[0] + d[0] * KNEE_TRIM, f_post[1] + d[1] * KNEE_TRIM)
    e2 = (f_beam[0] - d[0] * KNEE_TRIM, f_beam[1] - d[1] * KNEE_TRIM)
    L = ((e2[0] - e1[0]) ** 2 + (e2[1] - e1[1]) ** 2) ** 0.5
    # Strebe: 4040, 90-Grad-Enden, Achse von e1 nach e2
    p1, p2 = to3(*e1) + nrm * (P / 2), to3(*e2) + nrm * (P / 2)
    ax = p2 - p1
    ax.normalize()
    o = doc.addObject("Part::Feature", "Eckstrebe_%s_%s" % (wall, tag))
    o.Shape = profile(L)
    o.Placement = Placement(p1, Rotation(Vector(0, 0, 1), ax))
    beams.append((o.Name, L))
    knees.append(L)
    # Verbinder-Platzhalter: Keil zwischen Strebenende und Profilflaeche, 40 mm breit
    def wedge(name, end, to_face):
        pts2 = []
        for sgn in (+1, -1):
            v = (end[0] + sgn * n[0] * P / 2, end[1] + sgn * n[1] * P / 2)
            pts2.append(v)
        for v in list(reversed(pts2)):
            pts2.append(to_face(v))
        pts = [to3(*q) for q in pts2]
        pts.append(pts[0])
        face = Part.Face(Part.makePolygon(pts))
        sol = face.extrude(nrm * KNEE_W)
        po = doc.addObject("Part::Feature", name)
        po.Shape = sol
        color(po, (0.55, 0.55, 0.6))
        connectors.append(name)
    wedge("Verbinder45_%s_%s_Pfosten" % (wall, tag), e1,
          lambda v: (hp, v[1] - (v[0] - hp) * d[1] / d[0]))          # entlang -d zurueck auf die Pfostenflaeche
    wedge("Verbinder45_%s_%s_Traeger" % (wall, tag), e2,
          lambda v: (v[0] + (zb - v[1]) * d[0] / d[1], zb))          # entlang +d vor auf die Traegerunterseite

if BRACING == "knee":
    knee_brace("links", P, +1, "vorn")
    knee_brace("links", D - P, -1, "hinten")
    knee_brace("rechts", P, +1, "vorn")
    knee_brace("rechts", D - P, -1, "hinten")
    knee_brace("hinten", P, +1, "links")
    knee_brace("hinten", W - P, -1, "rechts")

# ---------- Rack-Einbauten ----------
def u_z0(i):
    """Unterkante der Rack-Einheit i (1 = unterste)."""
    return Z_LOW1 + RACK_EXTRA / 2 + (i - 1) * U

def make_d12(name, side, unit, assign):
    """RACK U PAN 01 D12 TIE BAR (872215) mit 12 D-Loechern als Platzhalter."""
    y0 = -D12_T if side == "vorn" else D
    x0 = (W - PANEL_W) / 2
    zc = u_z0(unit) + U / 2
    body = Part.makeBox(PANEL_W, D12_T, PANEL_UH, Vector(x0, y0, zc - PANEL_UH / 2))
    out = Vector(0, -1, 0) if side == "vorn" else Vector(0, 1, 0)
    y_face = 0 if side == "vorn" else D + D12_T
    for xc in (W / 2 - RACK_PITCH / 2, W / 2 + RACK_PITCH / 2):          # Ohrloecher (2 je Seite)
        for dz in (-15.875, 15.875):
            body = body.cut(Part.makeCylinder(HOLE_D / 2, D12_T + 2, Vector(xc, y0 - 1, zc + dz), Vector(0, 1, 0)))
    for i in range(1, N_D + 1):                                          # D-Loecher
        off = (i - (N_D + 1) / 2.0) * D_PITCH
        xh = W / 2 + off if side == "vorn" else W / 2 - off
        body = body.cut(Part.makeCylinder(D_HOLE / 2, D12_T + 2, Vector(xh, y0 - 1, zc), Vector(0, 1, 0)))
    o = doc.addObject("Part::Feature", name)
    o.Shape = body
    color(o, (0.1, 0.1, 0.1))
    for i in range(1, N_D + 1):                                          # Steckverbinder-Platzhalter
        off = (i - (N_D + 1) / 2.0) * D_PITCH
        xh = W / 2 + off if side == "vorn" else W / 2 - off
        fn = assign.get(i, "Blindkappe")
        po = doc.addObject("Part::Feature", "%s_%02d_%s" % (name, i, fn))
        po.Shape = Part.makeCylinder(10.5, 12, Vector(xh, y_face, zc), out)
        color(po, (0.2, 0.4, 0.9) if "blau" in fn else (0.95, 0.95, 0.95) if "weiss" in fn
              else (0.85, 0.65, 0.1) if fn != "Blindkappe" else (0.35, 0.35, 0.35))

def make_tray(name, unit):
    """RACK TRAY 01 PULLOUT (87556) hinten: Frontblende + Koerper-Platzhalter (Maße gegen Zeichnung pruefen)."""
    x0 = (W - PANEL_W) / 2
    zc = u_z0(unit) + U / 2
    front = Part.makeBox(PANEL_W, TRAY_T, PANEL_UH, Vector(x0, D, zc - PANEL_UH / 2))
    body = Part.makeBox(TRAY_BODY_W, TRAY_BODY_D, TRAY_BODY_H,
                        Vector((W - TRAY_BODY_W) / 2, D - TRAY_BODY_D, zc - TRAY_BODY_H / 2))
    o = doc.addObject("Part::Feature", name)
    o.Shape = front.fuse(body)
    color(o, (0.15, 0.15, 0.15))

make_tray("Rack_hinten_U%d_Schublade_87556" % REAR_TRAY_U, REAR_TRAY_U)
make_d12("Rack_hinten_U%d_D12_Netz" % REAR_D12_U, "hinten", REAR_D12_U, REAR_D12)
if FRONT_RACK:
    make_d12("Rack_vorn_U%d_D12" % FRONT_D12_U, "vorn", FRONT_D12_U, FRONT_D12)

# ---------- Forex-Fuellplatten in der 8-mm-Nut (Rackband; Sitzseite vorn bleibt offen) ----------
# Die Platten liegen in der Mittelebene der Profile (Nut sitzt mittig) und greifen SLOT_INS mm in die Nut ein.
# Montage: Platte vor dem letzten Profil einschieben, danach Einfassprofil (Alux 8-12.40) in die Nut druecken.
CLAD_H = RACK_CLEAR + 2 * SLOT_INS       # Plattenhoehe (Oeffnung zwischen unterem und oberem Rahmen + Eingriff)
clad_parts, logo_state = [], {"font": None}

# --- Logo-Geometrie: fertige Umrisse (Space Grotesk + Zeichen) aus docs/branding/forex_layout.json ---
_layout_cache = {}
LAYER_OF = {"ink": "hell", "url": "hell", "tag": "grau", "accent": "akzent"}
LAYER_COL = {"hell": COL_LIGHT, "grau": COL_TAG, "akzent": COL_ACCENT}

def logo_layout(face, full_w, full_h):
    """Logo-Flaechen in der XY-Ebene, Ursprung Plattenmitte, mm. Gleiche Daten wie die Druckvorlagen forex-*.svg."""
    import json
    if not _layout_cache:
        if not os.path.exists(LOGO_LAYOUT):
            print("Logo-Layout fehlt: %s" % LOGO_LAYOUT)
            return []
        with open(LOGO_LAYOUT, encoding="utf-8") as f:
            _layout_cache.update(json.load(f))
        logo_state["font"] = "Space Grotesk (Umrisse aus forex_layout.json)"
    lay = _layout_cache["seite" if face in ("links", "rechts") else "hinten"]
    k = min(full_w / lay["w"], full_h / lay["h"])
    if abs(k - 1) > 1e-3:
        print("Hinweis: Platte %.1f x %.1f weicht vom Layout %.1f x %.1f ab, Logo skaliert (%.3f)" % (full_w, full_h, lay["w"], lay["h"], k))
    out = []
    for f in lay["faces"]:
        wires = []
        for loop in f["loops"]:
            pts = [Vector((x - lay["w"] / 2) * k, (y - lay["h"] / 2) * k, 0) for x, y in loop]
            wires.append(Part.makePolygon(pts + [pts[0]]))
        try:
            out.append((Part.makeFace(wires, "Part::FaceMakerBullseye"), LAYER_OF.get(f["color"], "hell")))
        except Exception as e:
            print("Logo-Flaeche uebersprungen: %s" % e)
    return out

def forex_panel(name, box_origin, box_size, face, centre):
    """Platte als Box; Logo auf der Aussenseite (bedruckt oder graviert).
    face: 'links' | 'rechts' | 'hinten' (Blickrichtung des Betrachters von aussen)."""
    sh = Part.makeBox(box_size[0], box_size[1], box_size[2], Vector(*box_origin))
    if face in ("links", "rechts"):     # obere Ecken freischneiden: dort liegt der durchgehende X-Traeger des oberen Rahmens
        y0_, y1_ = box_origin[1], box_origin[1] + box_size[1]
        for ya, yb in ((y0_, P), (D - P, y1_)):
            sh = sh.cut(Part.makeBox(box_size[0] + 2, yb - ya, 20, Vector(box_origin[0] - 1, ya, Z_UP0)))
    # Text-Achsen (Rechts, Hoch, Normale nach aussen) je Seite
    axes = {"links":  (Vector(0, -1, 0), Vector(0, 0, 1), Vector(-1, 0, 0)),
            "rechts": (Vector(0, 1, 0),  Vector(0, 0, 1), Vector(1, 0, 0)),
            "hinten": (Vector(-1, 0, 0), Vector(0, 0, 1), Vector(0, 1, 0))}[face]
    along = box_size[1] if face in ("links", "rechts") else box_size[0]
    xt, yt, zt = axes
    m = App.Matrix(xt.x, yt.x, zt.x, centre.x,
                   xt.y, yt.y, zt.y, centre.y,
                   xt.z, yt.z, zt.z, centre.z,
                   0, 0, 0, 1)
    items = logo_layout(face, along, box_size[2])
    layers = {}
    for f, col in items:
        t = f.copy()
        t.transformShape(m)
        layers.setdefault(col, []).append(t)
    if LOGO_MODE == "gravur" and layers:
        cutter = Part.Compound([f.extrude(zt * -LOGO_DEPTH) for fs in layers.values() for f in fs])
        sh = sh.cut(cutter)
    o = doc.addObject("Part::Feature", name)
    o.Shape = sh
    color(o, COL_INK if LOGO_MODE == "druck" else (0.93, 0.93, 0.93))
    if LOGO_MODE == "druck":
        for col, fs in layers.items():
            p = doc.addObject("Part::Feature", "%s_Druck_%s" % (name, col))
            p.Shape = Part.Compound([f.extrude(zt * PRINT_T) for f in fs])
            color(p, LAYER_COL[col])
            try:                        # Kanten in Druckfarbe, sonst wirken die Buchstaben schwarz umrandet
                p.ViewObject.LineColor = LAYER_COL[col]
                p.ViewObject.PointColor = LAYER_COL[col]
            except Exception:
                pass
    clad_parts.append((name, box_size))
    return o

if CLAD:
    y_lo, y_hi = P - SLOT_INS, D - P + SLOT_INS        # zwischen den Pfosten (vorn/hinten) plus Eingriff
    z_lo = Z_LOW1 - SLOT_INS
    for face, xm in (("links", P / 2), ("rechts", W - P / 2)):
        ox = xm - FOREX_T / 2
        out_x = ox if face == "links" else ox + FOREX_T
        forex_panel("Forex_Seite_%s" % face, (ox, y_lo, z_lo), (FOREX_T, y_hi - y_lo, CLAD_H), face,
                    Vector(out_x, (y_lo + y_hi) / 2, z_lo + CLAD_H / 2))
    # Rueckseite: zwei Stuecke neben dem Rack-Fenster (zwischen Pfosten und Rack-Schiene), beide mit Logo
    ym = D - P / 2
    oy = ym - FOREX_T / 2
    for nm, (xa, xb) in (("Forex_Rueck_links", (P - SLOT_INS, (W - RACK_WIN_W) / 2)),
                         ("Forex_Rueck_rechts", ((W + RACK_WIN_W) / 2, W - P + SLOT_INS))):
        forex_panel(nm, (xa, oy, z_lo), (xb - xa, FOREX_T, CLAD_H), "hinten",
                    Vector((xa + xb) / 2, oy + FOREX_T, z_lo + CLAD_H / 2))

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
    cuts[round(L, 1)] = cuts.get(round(L, 1), 0) + 1
total_m = sum(L for _, L in beams) / 1000.0
JOINTS = 26 if FRONT_RACK else 24   # 4 Y_oben + 4 Pfosten (oben), untere Rahmenenden (8, ohne Frontträger 6), 6 Bodenstreben-Enden, 4 Mittelträger-Enden
N_RAILS = 6 if FRONT_RACK else 4    # Rack-Schienen (vorn+hinten bzw. nur hinten) + 2 Tiefenschienen
N_D12 = 2 if FRONT_RACK else 1
angles = JOINTS * ANGLES_PER_JOINT
N_ZARGE = 4
ANG20 = N_RAILS * 2 + N_ZARGE * 2      # Winkel 2020: Schienen oben/unten + je 2 Enden der Zargen
n_blind = (N_D - len(REAR_D12)) + ((N_D - len(FRONT_D12)) if FRONT_RACK else 0)

rows = [["Pos", "Artikel", "Artikelnr", "Menge", "Einheit", "Bemerkung"]]
for i, (L, n) in enumerate(sorted(cuts.items(), reverse=True), 1):
    rows.append([i, "Nutprofil 4040 Zuschnitt %.1f mm" % L, "Alux 4040", n, "Stk", "Toleranz -1/+1 mm"])
n0 = len(rows)
rows += [
    [n0,      "Winkel 4040", "(Vorschlag)", angles, "Stk", "%d Verbindungen x %d" % (JOINTS, ANGLES_PER_JOINT)],
    [n0 + 1,  "Nutenstein einschwenkbar 40-Profil M8", "8-4-M8.40", angles * 2, "Stk", "2 je Winkel"],
    [n0 + 2,  "Schraube M8 (Innensechskant)", "(Laenge waehlen)", angles * 2, "Stk", "2 je Winkel"],
    [n0 + 3,  "Profilabdeckkappe 4040", "(Vorschlag)", 16, "Stk", "freie Profilenden, Anzahl pruefen"],
    [n0 + 4,  "Alux Gelenkstellfuss 80 mm, Gewinde M8x50", "80-M8x50", 4, "Stk", "Gummi-Gelenkfuss, Gewinde in den Profilkern des Pfostens; Verstellweg ca. +-%.0f mm (ANNAHME), STEP der Produktseite" % FOOT_TRAVEL],
    [n0 + 27, "Gewinde M8 in den Profilkern der Pfosten schneiden", "Handgewindebohrer M8", 4, "Stk", "Kernloch 6,8 mm laut Profil; mind. 25 mm tief, Gewinde von unten; Werkzeug, kein Kaufteil"],
    [n0 + 5,  "Nutprofil 2020 (Nut 6) Zuschnitt %.1f mm" % RAIL_L, "(Alux 2020 T-Nut pruefen)", N_RAILS, "Stk", "Rack-Schienen hinten (2)%s + 2 Tiefenschienen" % (" + vorn (2)" if FRONT_RACK else "")],
    [n0 + 21, "Nutprofil 2020 (Nut 6) Zuschnitt %.1f mm" % ZARGE_L, "(Alux 2020 T-Nut pruefen)", N_ZARGE, "Stk", "Rack-Zarge: oben und unten, links und rechts, zwischen Rack-Schiene und Tiefenschiene"],
    [n0 + 7,  "Winkel 2020", "2020L-Alu", ANG20, "Stk", "je Rack-/Tiefenschiene oben + unten, je Zargenende"],
    [n0 + 8,  "Schraube ISO 7380 M5x8", "ISO 7380-M5x8", ANG20 * 2, "Stk", "2 je Winkel"],
    [n0 + 9,  "Nutenstein M5 fuer 6-mm-Nut (2020)", "(Vorschlag)", ANG20, "Stk", "1 je Winkel"],
    [n0 + 10, "Nutenstein M5 fuer 8-mm-Nut (4040)", "(Vorschlag)", N_RAILS * 2, "Stk", "1 je Winkel"],
    [n0 + 12, "Adam Hall 19\" Parts RACK TRAY 01 PULLOUT (1 HE, Auszug)", "87556", 1, "Stk", "hinten, 1. HE; Einbautiefe %.0f mm (Hersteller 360-480), Last 25 kg" % TRAY_MOUNT_D],
    [n0 + 13, "Adam Hall 19\" Parts RACK U PAN 01 D12 TIE BAR", "872215", N_D12, "Stk", "1 HE, 12 D-Loecher, Zugentlastung; hinten%s, 3. HE" % (" + vorn" if FRONT_RACK else "")],
    [n0 + 14, "Neutrik powerCON Einbau, blau (IN)", "(Teilenr. pruefen, z. B. NAC3MPA-1)", 1, "Stk", "Netzeingang, D-Format"],
    [n0 + 15, "Neutrik powerCON Einbau, weiss/hellgrau (OUT)", "(Teilenr. pruefen, z. B. NAC3MPB-1)", 1, "Stk", "Netzausgang, D-Format"],
    [n0 + 16, "Netzwerk-Durchfuehrung (Cat), D-Format", "(Teilenr. pruefen, etherCON-Familie)", 1, "Stk", "hinten"],
    [n0 + 17, "Blindplatte/Abdeckung fuer D-Ausschnitt", "(z. B. Neutrik DBA-BL pruefen)", n_blind, "Stk", "unbelegte D-Loecher hinten%s" % (" + vorn" if FRONT_RACK else "")],
    [n0 + 18, "Schraube M5 + Nutenstein M5 (6-mm-Nut)", "(Vorschlag)", 4 * N_D12 + 8, "Satz", "4 je D12-Blende, 8 fuer die Schublade"],
    [n0 + 19, "Siebdruckplatte %d mm, %d x %d mm" % (PLATE, W, D), "(Vorschlag)", 1, "Stk", "als Scheibe fest verschrauben: mind. 20 Senkkopfschrauben mit Nutenstein in obere Traeger"],
    [n0 + 20, "ESD-Matte", "(Vorschlag)", 1, "Stk", "mit 1-MOhm-Widerstand an den Erdungspunkt"],
]
if BRACING == "diag":
    rows += [
        [n0 + 6,  "Nutprofil 2020 (Nut 6) Zuschnitt %.1f mm" % diags[0], "(Alux 2020 T-Nut pruefen)", 3, "Stk", "Diagonalen hinten, links, rechts; Laengen je Feld leicht unterschiedlich: %s" % ", ".join("%.1f" % d for d in diags)],
        [n0 + 11, "Knotenblech Alu %.0f mm, %d x %d mm" % (GUSSET_T, GUSSET_G, GUSSET_G), "(Zuschnitt)", len(gussets), "Stk", "je Diagonalenende; Bohrungen M8 (2 je Profil) und M5 (2 fuer die 2020-Diagonale), Innenseite der Rahmenprofile"],
        [n0 + 25, "Schraube M8 + Nutenstein M8 (40er Profil)", "(Vorschlag)", len(gussets) * 4, "Satz", "4 je Knotenblech (2 je 4040-Profil)"],
        [n0 + 26, "Schraube M5 + Nutenstein M5 (2020, Nut 6)", "(Vorschlag)", len(gussets) * 2, "Satz", "2 je Knotenblech in die Diagonale"],
    ]
else:
    rows += [
        [0, "Alux Winkelverbinder 45 Grad, Profil 40x40", "4040-45", len(connectors), "Stk", "2 je Eckstrebe (%d Streben a %.1f mm aus 4040, 90-Grad-Enden); Mass des Verbinders ist Platzhalter (STEP 4040-45 einsetzen)" % (len(knees), knees[0])],
        [0, "Linsenkopfschraube ISO 7380 M8x16", "ISO 7380 M8x16", len(connectors) * 2, "Stk", "ANNAHME je Verbinder 2 (Variante Stirnflaeche-Nut wie bei 4080-45), Seite 4040-45 pruefen"],
        [0, "Linsenkopfschraube ISO 7380 M8x25", "ISO 7380 M8x25", len(connectors) * 2, "Stk", "ANNAHME, siehe oben"],
        [0, "Nutenstein einschwenkbar 40-Profil M8", "8-4-M8.40", len(connectors) * 2, "Stk", "ANNAHME, siehe oben"],
    ]
if CLAD:
    _sz = {}
    for _n, _sz3 in clad_parts:
        _dims = sorted(_sz3, reverse=True)[:2]
        _sz.setdefault((round(_dims[0], 1), round(_dims[1], 1)), []).append(_n)
    _edge_m = sum(2 * (sorted(z3, reverse=True)[0] + sorted(z3, reverse=True)[1]) for _, z3 in clad_parts) / 1000.0
    for (_a, _b), _names in _sz.items():
        rows.append([0, "Forex classic %.0f mm, Zuschnitt %.1f x %.1f mm" % (FOREX_T, _a, _b), "(Vorschlag)", len(_names), "Stk", "Fuellplatte in 8-mm-Nut: %s; %s" % (", ".join(_names), "bedruckt, Druckdaten docs/branding/forex-*.svg" if LOGO_MODE == "druck" else "Logo graviert")])
    rows += [
        [0, "Einfassprofil / Abdeckprofil 8 mm, 1000 mm (Alux)", "8-12.40", int(_edge_m) + 2, "Stk", "fuer Plattenstaerke 4-6 mm; ca. %.1f m Plattenkante, davon in die Nut zu pressen; Forex nicht ausdruecklich gelistet, bei Alux nachfragen" % _edge_m],
    ]
for _i, _r in enumerate(rows[1:], 1):
    _r[0] = _i
print("\nZuschnitt (Laenge mm: Anzahl):", cuts)
print("Profil 4040 gesamt: %.2f m, ca. %.1f kg" % (total_m, total_m * KG_PER_M))
print("Rack-Raum lichte Hoehe: %.2f mm (%d HE + %.2f), Rahmen-Oberkante: %.2f mm, Platte oben: %.2f mm"
      % (RACK_CLEAR, RACK_U, RACK_EXTRA, H, H + PLATE + ESD_T))
print("Verbindungen: %d, Winkel 4040: %d" % (JOINTS, angles))
print("Tischhoehe (Oberkante ESD): %.1f mm (Soll %d) | Pfostenlaenge %.1f | Beinlaenge unter dem Rack-Boden %.1f mm" % (H + PLATE + ESD_T, DESK_H, Z_UP0, FOOT_H))
print("Schubladen-Einbautiefe (Aussenflaeche hinten bis Tiefenschiene): %.0f mm (Hersteller: 360-480)" % TRAY_MOUNT_D)
print("Rack-Zargen: %d x %.1f mm | Forex %.0f mm in der Nut: %s, Plattenhoehe %.1f mm | Logo: %s, Schriftart: %s" % (N_ZARGE, ZARGE_L, FOREX_T, "an" if CLAD else "aus", CLAD_H, LOGO_MODE, logo_state["font"]))
print("Aussteifung: %s | Diagonalen: %s | Eckstreben: %d x %s mm" % (BRACING, ", ".join("%.1f" % d for d in diags) or "-", len(knees), ", ".join("%.1f" % k for k in knees[:1]) or "-"))
print("Sitzseite vorn: %s | Beinraumtiefe ab Tischkante: %.0f mm (bis Vorderkante Mittelträger), Beinraumbreite %d mm, Hoehe unter der Platte: %.1f mm"
      % ("frei" if not FRONT_RACK else "durch Rack belegt", MID_Y - P / 2, W - 2 * P, Z_UP0))

bom_dir = os.path.join(REPO, "bom")
if os.path.isdir(bom_dir):
    with open(os.path.join(bom_dir, "frame_bom.csv"), "w", newline="", encoding="utf-8") as f:
        csv.writer(f, delimiter=";").writerows(rows)
    print("BOM geschrieben:", os.path.join(bom_dir, "frame_bom.csv"))
else:
    print("bom-Ordner nicht gefunden, REPO-Pfad pruefen.")
