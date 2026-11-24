# open-ora | cad/analysis/arm_holder_sizing.py | v1
# Ueberschlags-Auslegung Arm 1 (Halter): Massen, Lastmomente, Antriebe, Steifigkeit am Werkzeugpunkt, Arbeitsraum.
# Kinematik (Vorschlag ADR 0007): SCARA mit Hubsaeule
#   J1 Drehung Saeule (senkrecht) | Z Hub (Trapezspindel) | J2 Ellbogen (senkrecht)
#   J4 Gieren (senkrecht) | J5 Nicken (waagerecht) | J6 Rollen (Werkzeugachse) | Traeger-Kupplung
# Koordinaten wie frame_4040.py: X 0..1000 links->rechts (Blick von vorn), Y 0 vorn (Sitzseite) .. 1000 hinten,
# Z ab Boden; Oberkante ESD-Matte = DESK_H.
# ALLE Massen, Wirkungsgrade und Steifigkeiten sind ANNAHMEN fuer die Groessenordnung, keine Herstellerwerte.
# Start: python cad/analysis/arm_holder_sizing.py   (schreibt docs/images/arm1_arbeitsraum.png, wenn matplotlib da ist)

import math
import os

G = 9.81
DESK_H = 740.0

# ---------------- Geometrie (mm) ----------------
BASE_X, BASE_Y = 920.0, 920.0        # J1-Achse hinten rechts, Fuss direkt auf der Rahmenecke ueber Pfosten_RH
L1, L2 = 300.0, 300.0                # Oberarm, Unterarm (Achsabstaende)
TOOL_REACH = 210.0                   # J5-Achse bis Platinenmitte (J5-Gehaeuse 35 + J6 50 + Kupplung 15 + halber Rahmen 110)
WRIST_DROP = 120.0                   # J2-Ebene bis J5-Achse (Handgelenk haengt unter dem Unterarm)
TCP_OFF = 210.0                      # J5-Achse bis Schwerpunkt der Nutzlast (= TOOL_REACH)
Z_STROKE = 200.0
P0 = (500.0, 450.0)                  # Praesentationspunkt (Tischmitte, vor dem Sitzplatz)
ZONE = 100.0                         # +- Verfahrbereich um P0 in X und Y

# ---------------- Massen (kg, ANNAHMEN) ----------------
M_PAY = 1.0                          # Nutzlast max. (Mittel 0,5)
M_CARRIER = 0.30                     # Platinenrahmen / Traeger
M_COUPLING = 0.15                    # Kupplungshaelfte am Arm mit Verriegelung
M_J6 = 0.45                          # NEMA14 + Schnecke + Lager
M_J5 = 0.85                          # NEMA17 60 mm + Schnecke + Gehaeuse
M_J4 = 0.55
M_L2 = 0.55                          # Unterarm (Alu 2040, 300 mm + Lagerstellen)
M_L1 = 0.70                          # Oberarm inkl. J2-Lagerung
M_J2_MOT = 0.40                      # J2-Motor sitzt an der Saeule (Riemen zum Ellbogen)
M_COLUMN = 1.6                       # Drehsaeule mit Schienen, Z-Motor, Spindel
M_BASE = 1.2                         # Grundplatte, J1-Lagerung, J1-Motor (steht)

# ---------------- Antriebe (ANNAHMEN) ----------------
T_N17 = 0.45      # Nm Haltemoment NEMA17 (48 mm), nutzbar bei Drehzahl ca. 60 %
T_N17S = 0.28     # NEMA17 kurz (34 mm)
T_N14 = 0.18
T_N17L = 0.65     # NEMA17 60 mm (J5)
SF = 2.0          # Sicherheitsfaktor auf statische Momente
I_J1, I_J2 = 20.0, 12.0              # Riemen 2-stufig GT2 (20:80 x 20:100 bzw. 20:60 x 20:80)
I_J4, I_J5, I_J6 = 30.0, 30.0, 20.0  # Schneckentriebe (selbsthemmend)
ETA_BELT, ETA_WORM = 0.9, 0.40       # selbsthemmende Schnecke: Wirkungsgrad < 50 %
SCREW_P, SCREW_D, MU = 2.0, 8.0, 0.20   # TR8x2, Reibwert Messing/Stahl trocken-geschmiert

F_PROBE = 2.0     # N Tastkraft des Probers (Annahme, Federkontakt 1-2 N)

lines = []
def out(s=""):
    print(s)
    lines.append(s)

# ---------------- 1. Massen ----------------
m_wrist = M_J4 + M_J5 + M_J6 + M_COUPLING
m_moving_z = M_L1 + M_J2_MOT + M_L2 + m_wrist + M_CARRIER + M_PAY   # J2-Motor sitzt am Oberarm an der Saeule (hebt mit)
m_arm = M_BASE + M_COLUMN + M_L1 + M_J2_MOT + M_L2 + m_wrist
out("1) MASSEN")
out("   Arm ohne Nutzlast: %.1f kg (Annahme in frame_stiffness.py: 6 kg je Arm)" % m_arm)
out("   Handgelenk (J4+J5+J6+Kupplung): %.2f kg" % m_wrist)
out("   bewegte Masse an der Z-Achse inkl. 1 kg Nutzlast: %.1f kg" % m_moving_z)

# ---------------- 2. Lastmomente Handgelenk ----------------
# J5 (Nicken): ungunstig waagerecht ausgestreckt
t5 = G * (M_J6 * 0.04 + M_COUPLING * 0.08 + M_CARRIER * 0.12 + M_PAY * TCP_OFF / 1000)
t6 = G * (M_CARRIER + M_PAY) * 0.03          # Schwerpunkt 30 mm neben der Rollachse
out("\n2) HANDGELENK")
for name, t, mot, i in (("J5 Nicken", t5, T_N17L, I_J5), ("J6 Rollen", t6, T_N14, I_J6)):
    avail = mot * i * ETA_WORM
    out("   %-10s Lastmoment %.2f Nm, mit SF %.1f: %.2f Nm | Antrieb %.2f Nm x %d x %.2f = %.2f Nm -> Reserve %.1fx"
        % (name, t, SF, t * SF, mot, i, ETA_WORM, avail, avail / (t * SF)))
out("   Schnecken selbsthemmend: Achsen halten ohne Strom, keine Lastumkehr am Motor.")

# ---------------- 3. Z-Achse ----------------
F_z = m_moving_z * G + F_PROBE
lead_ang = math.atan(SCREW_P / (math.pi * (SCREW_D - SCREW_P / 2)))
fr_ang = math.atan(MU / math.cos(math.radians(15)))      # Trapez 30 Grad
t_z = F_z * (SCREW_D - SCREW_P / 2) / 2 / 1000 * math.tan(lead_ang + fr_ang)
out("\n3) Z-ACHSE (TR8x2)")
out("   Last %.0f N, Antriebsmoment %.3f Nm (NEMA17: Reserve %.0fx)" % (F_z, t_z, T_N17 * 0.6 / t_z))
out("   Steigungswinkel %.1f Grad < Reibungswinkel %.1f Grad -> %s"
    % (math.degrees(lead_ang), math.degrees(fr_ang),
       "selbsthemmend, Arm sackt bei Stromausfall nicht ab" if lead_ang < fr_ang else "NICHT selbsthemmend, Bremse noetig"))

# ---------------- 4. J1 / J2 ----------------
r1, r2 = L1 / 1000, (L1 + L2) / 1000
r3 = r2 + TOOL_REACH / 1000             # Nutzlast ausgestreckt, Werkzeug zeigt nach aussen (ungunstig)
J_j1 = (M_L1 * r1 ** 2 / 3 + M_L2 * ((r1 + r2) / 2) ** 2 + m_wrist * r2 ** 2 + (M_CARRIER + M_PAY) * r3 ** 2)
J_j2 = M_L2 * (L2 / 1000) ** 2 / 3 + m_wrist * (L2 / 1000) ** 2 + (M_CARRIER + M_PAY) * (L2 / 1000 + TOOL_REACH / 1000) ** 2
V_DEG, T_ACC = 60.0, 0.6            # Halter muss nicht schnell sein: 60 Grad/s, Rampe 0,6 s
alpha = math.radians(V_DEG) / T_ACC
out("\n4) J1 / J2 (senkrechte Achsen, keine Schwerkraftlast)")
for name, J, i, mot, mname in (("J1", J_j1, I_J1, T_N17L, "NEMA17 60 mm"), ("J2", J_j2, I_J2, T_N17, "NEMA17 48 mm")):
    t_out = J * alpha * SF
    t_mot = t_out / i / ETA_BELT
    out("   %s: Traegheit %.3f kgm2, Moment fuer %.0f Grad/s in %.1f s (SF %.0f) %.2f Nm -> Motor %.3f Nm (%s nutzbar %.2f), Motordrehzahl %.0f U/min"
        % (name, J, V_DEG, T_ACC, SF, t_out, t_mot, mname, mot * 0.6, V_DEG * i / 6))
m_tilt = G * (M_L1 * r1 / 2 + M_J2_MOT * 0.03 + M_L2 * (r1 + r2) / 2 + m_wrist * r2 + (M_CARRIER + M_PAY) * r3)
out("   Kippmoment am J1-Lager (ausgestreckt, 1 kg): %.0f Nm -> Lagerpaar mit Abstand >= 80 mm oder Vierpunktlager" % m_tilt)
out("   Befestigung: Fussplatte auf der Rahmenecke (X_oben_hinten + Y_oben_rechts), Kraft geht direkt in Pfosten_RH.")

# ---------------- 5. Steifigkeit am Werkzeugpunkt ----------------
out("\n5) STEIFIGKEIT unter %.0f N Tastkraft (Groessenordnung)" % F_PROBE)
E_AL = 70000.0
I_2040 = 6.9e4         # mm4, 2040 hochkant, ANNAHME (Herstellerwert pruefen)
d_links = F_PROBE * (L1 ** 3 + L2 ** 3 + 3 * L1 * L2 * (L1 + L2)) / (3 * E_AL * I_2040)
out("   Biegung Ober-/Unterarm (2040 hochkant, senkrechte Kraft): %.3f mm" % d_links)
k_step = T_N17 * 50                      # Nm/rad: Schrittmotor-Haltesteifigkeit ca. T_hold * Polpaare
k_j1 = k_step * I_J1 ** 2                # am Abtrieb
d_j1 = F_PROBE / (k_j1) * r3 * r3 * 1000
out("   J1 nachgiebig bei waagerechter Kraft (Schrittmotor %.0f Nm/rad, Riemen ideal): %.2f mm" % (k_step, d_j1))
out("   -> waagerechte Kraefte (schraeg gestellte Platine) sind der Schwachpunkt; senkrechte Tastkraft geht in die Lager.")
out("   -> Abhilfe bei Bedarf: Haltebremse J1/J2 oder Andockstation (siehe ADR 0007).")
# Platinenbiegung: Streifen 100 mm breit, 1,6 mm FR4, beidseitig gelagert
E_FR4, t_pcb, b = 20000.0, 1.6, 100.0
I_pcb = b * t_pcb ** 3 / 12
for span in (300.0, 150.0, 80.0):
    d = F_PROBE * span ** 3 / (48 * E_FR4 * I_pcb)
    out("   Platine 1,6 mm, Stuetzweite %3.0f mm, Kraft in Feldmitte: %.2f mm" % (span, d))
out("   -> Die Platine biegt sich weit mehr als der Arm. Der Traeger braucht verstellbare Stuetzstifte (Abstand <= 80 mm).")

# ---------------- 6. Arbeitsraum ----------------
reach = L1 + L2
def dist(x, y):
    return math.hypot(x - BASE_X, y - BASE_Y)
def wrist_r(x, y):
    """Abstand Handgelenk (J4) zur J1-Achse, wenn die Werkzeugachse von der Basis weg zeigt."""
    return dist(x, y) - TOOL_REACH
corners = [(P0[0] + sx * ZONE, P0[1] + sy * ZONE) for sx in (-1, 1) for sy in (-1, 1)]
out("\n6) ARBEITSRAUM (Armreichweite %.0f mm + Werkzeug %.0f mm, Basis bei x=%.0f y=%.0f)" % (reach, TOOL_REACH, BASE_X, BASE_Y))
for name, c in [("P0", P0)] + [("Ecke", c) for c in corners]:
    out("   %-4s (%.0f, %.0f): Platinenmitte %.0f mm von J1, Handgelenk %.0f mm = %.0f %% der Armreichweite"
        % (name, c[0], c[1], dist(*c), wrist_r(*c), 100 * wrist_r(*c) / reach))
out("   Werkzeugachse frei drehbar (J4): die Platine kann auch quer oder zur Basis hin stehen, solange das Handgelenk in Reichweite bleibt.")
out("   Hoehe Werkzeugpunkt ueber Matte: ca. 30 bis %.0f mm (Hub %.0f mm)" % (30 + Z_STROKE, Z_STROKE))
out("   Saeulenoberkante ca. 400 mm ueber der Matte -> mit dem Kameraportal abstimmen.")

here = os.path.dirname(os.path.abspath(__file__))
try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle, Circle
    fig, ax = plt.subplots(figsize=(7, 7))
    ax.add_patch(Rectangle((0, 0), 1000, 1000, fill=False, lw=1.5, ec="#444"))
    ax.add_patch(Rectangle((0, 980), 1000, 20, color="#bbb"))
    ax.add_patch(Rectangle((0, 610), 1000, 20, fill=False, ls=":", ec="#999"))
    ax.add_patch(Rectangle((830, 830), 170, 170, fill=False, ls="--", ec="#c60"))
    ax.add_patch(Circle((BASE_X, BASE_Y), reach + TOOL_REACH, fill=False, ec="#1f6fb2", lw=1.5))
    ax.add_patch(Circle((BASE_X, BASE_Y), reach, fill=False, ec="#1f6fb2", ls="--", lw=0.8))
    ax.add_patch(Circle((1000 - BASE_X, BASE_Y), reach + TOOL_REACH, fill=False, ec="#999", lw=1, ls="-."))
    ax.add_patch(Rectangle((P0[0] - ZONE, P0[1] - ZONE), 2 * ZONE, 2 * ZONE, color="#2a9d55", alpha=0.25))
    ax.plot(*P0, "o", color="#2a9d55")
    ax.plot(BASE_X, BASE_Y, "s", color="#1f6fb2", ms=10)
    ax.plot(1000 - BASE_X, BASE_Y, "s", color="#999", ms=8)
    ax.text(BASE_X - 20, BASE_Y + 45, "Arm 1 Halter", ha="right", color="#1f6fb2")
    ax.text(1000 - BASE_X + 20, BASE_Y + 45, "Arm 2 Prober? (Spiegelung, offen)", ha="left", color="#777", fontsize=8)
    ax.text(P0[0], P0[1] - ZONE - 25, "Praesentationszone", ha="center", color="#2a9d55")
    ax.text(915, 805, "Eckausschnitt Platte,\nFuss auf dem Rahmen", ha="center", va="top", color="#c60", fontsize=8)
    ax.text(500, 20, "vorn: Sitzseite", ha="center", color="#444")
    ax.set_xlim(-50, 1050); ax.set_ylim(-50, 1050); ax.set_aspect("equal")
    ax.set_xlabel("X [mm]"); ax.set_ylabel("Y [mm]")
    ax.set_title("Arm 1 Halter, Draufsicht: Platinenmitte bis %.0f mm (durchgezogen), Handgelenk bis %.0f mm (gestrichelt)" % (reach + TOOL_REACH, reach), fontsize=9)
    img = os.path.normpath(os.path.join(here, "..", "..", "docs", "images", "arm1_arbeitsraum.png"))
    os.makedirs(os.path.dirname(img), exist_ok=True)
    fig.savefig(img, dpi=110, bbox_inches="tight")
    out("\nBild: %s" % img)
except ImportError:
    pass
