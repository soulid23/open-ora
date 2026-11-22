# open-ora | cad/analysis/frame_stiffness.py
# Naeherung fuer Standfestigkeit und Seitensteifigkeit des Tischrahmens (Stabwerk, 3D).
#
# WICHTIG: Das ist eine Ueberschlagsrechnung mit Annahmen (siehe unten), kein Festigkeitsnachweis.
# Gemessene Werte (Schwingungsmessung, Last-Verformungs-Versuch am fertigen Tisch) gehen vor.
#
# Aufruf: python frame_stiffness.py        (benoetigt numpy und scipy)

import numpy as np
from scipy.linalg import eigh

# ---------------- Geometrie (mm), wie im Makro frame_4040.py ----------------
P          = 40.0
W, D       = 1000.0, 1000.0
DESK_H     = 740.0                 # Oberkante ESD-Matte ueber Boden
PLATE, ESD_T = 18.0, 2.0
RACK_CLEAR = 134.4
FOOT_H     = DESK_H - (P + RACK_CLEAR + P + PLATE + ESD_T)    # Unterkante unterer Rahmen
Z_UP0      = FOOT_H + P + RACK_CLEAR                          # Unterkante oberer Rahmen = Pfostenende
BRACE_Z0   = 100.0                 # Unterkante der Bodenstreben
MID_Y      = 620.0                 # Mittelträger (Tiefenschienen der Schublade)
FRONT_OPEN = True                  # Sitzseite vorn: unterer vorderer X-Träger entfällt (wie Makro FRONT_RACK=False)

# Knotenebenen (Profilmitten)
Z_F = BRACE_Z0 + P / 2
Z_L = FOOT_H + P / 2
Z_U = Z_UP0 + P / 2
XL, XR = P / 2, W - P / 2          # Pfostenmitten
YF, YB = P / 2, D - P / 2

# ---------------- Werkstoff und Querschnitte ----------------
E, G   = 70000.0, 26000.0          # N/mm2 (EN AW-6063 T66, Naeherung)
A40, I40 = 516.7, 75648.0          # aus dem STEP-Querschnitt (FreeCAD)
J40    = 0.5 * 2 * I40             # ANNAHME: Torsionskonstante, Einfluss gering
A20    = 210.8                     # Ersatzprofil 2020 aus dem Makro (ANNAHME, nicht Hersteller)
KG_M   = 1.395e-3                  # kg/mm 4040 (Datenblatt)

# ---------------- Massen-ANNAHMEN (kg) ----------------
M_PLATE   = 9.0 * (W * D / 1e6) * (PLATE / 12.0)   # Siebdruck ca. 9 kg/m2 bei 12 mm
M_ESD     = 2.0
M_ARMS    = 12.0                   # zwei Arme
M_PORTAL  = 8.0                    # Sensorportal mit Kameras
M_MISC    = 10.0                   # Werkzeug, Kleinteile
M_RACK    = 8.0 + 3.7 + 3.5        # Netzteile etc., Schublade, Laptop
M_TOP     = M_PLATE + M_ESD + M_ARMS + M_PORTAL + M_MISC
g = 9.81


# ---------------- Stabwerk-Loeser ----------------
def beam_k(Aa, I, J, L):
    k = np.zeros((12, 12))
    ea, gj = E * Aa / L, G * J / L
    k[0, 0] = k[6, 6] = ea;  k[0, 6] = k[6, 0] = -ea
    k[3, 3] = k[9, 9] = gj;  k[3, 9] = k[9, 3] = -gj
    a, b, c, d = 12 * E * I / L**3, 6 * E * I / L**2, 4 * E * I / L, 2 * E * I / L
    kz = np.array([[a, b, -a, b], [b, c, -b, d], [-a, -b, a, -b], [b, d, -b, c]])
    ky = np.array([[a, -b, -a, -b], [-b, c, b, d], [-a, b, a, b], [-b, d, b, c]])
    for M, idx in ((kz, [1, 5, 7, 11]), (ky, [2, 4, 8, 10])):
        for i in range(4):
            for j in range(4):
                k[idx[i], idx[j]] += M[i, j]
    return k


def rot_block(xl):
    ref = np.array([0, 0, 1.0]) if abs(xl[2]) < 0.99 else np.array([1.0, 0, 0])
    yl = np.cross(ref, xl); yl /= np.linalg.norm(yl)
    zl = np.cross(xl, yl)
    R = np.vstack([xl, yl, zl])
    T = np.zeros((12, 12))
    for i in range(4):
        T[3 * i:3 * i + 3, 3 * i:3 * i + 3] = R
    return T


class Frame:
    def __init__(self):
        self.nodes, self.members, self.trusses, self.masses = {}, [], [], {}

    def node(self, name, x, y, z):
        self.nodes[name] = np.array([x, y, z], float)
        return name

    def beam(self, a, b, joint_a, joint_b, A=A40, I=I40, J=J40):
        """joint_*: 'rigid' = durchlaufend/fest am Knoten, 'bolted' = Winkelverbinder (Drehfeder)."""
        self.members.append((a, b, joint_a, joint_b, A, I, J))

    def truss(self, a, b, A=A20):
        self.trusses.append((a, b, A))

    def mass(self, name, kg):
        self.masses[name] = self.masses.get(name, 0.0) + kg

    def solve(self, kr, fixed_nodes, loads, extra_springs=()):
        names = list(self.nodes)
        n = len(names)
        ix = {nm: i for i, nm in enumerate(names)}
        nt, ndof = 3 * n, 6 * n
        # Elementendrotationen bekommen eigene Freiheitsgrade, wenn 'bolted'
        end_rot = {}
        for mi, (a, b, ja, jb, *_r) in enumerate(self.members):
            for e, jt in ((0, ja), (1, jb)):
                if jt == "bolted":
                    end_rot[(mi, e)] = ndof
                    ndof += 3
        K = np.zeros((ndof, ndof))

        def tdofs(nm): return list(range(3 * ix[nm], 3 * ix[nm] + 3))
        def rdofs(nm): return list(range(nt + 3 * ix[nm], nt + 3 * ix[nm] + 3))

        for mi, (a, b, ja, jb, Aa, I, J) in enumerate(self.members):
            pa, pb = self.nodes[a], self.nodes[b]
            L = np.linalg.norm(pb - pa)
            T = rot_block((pb - pa) / L)
            kg = T.T @ beam_k(Aa, I, J, L) @ T
            ra = list(range(end_rot[(mi, 0)], end_rot[(mi, 0)] + 3)) if (mi, 0) in end_rot else rdofs(a)
            rb = list(range(end_rot[(mi, 1)], end_rot[(mi, 1)] + 3)) if (mi, 1) in end_rot else rdofs(b)
            dm = tdofs(a) + ra + tdofs(b) + rb
            K[np.ix_(dm, dm)] += kg
            for (nd, er) in ((a, ra), (b, rb)):
                if er != rdofs(nd):
                    for u, v in zip(er, rdofs(nd)):
                        K[u, u] += kr; K[v, v] += kr; K[u, v] -= kr; K[v, u] -= kr
        for a, b, Aa in self.trusses:
            d = self.nodes[b] - self.nodes[a]
            L = np.linalg.norm(d); d /= L
            kk = E * Aa / L * np.outer(d, d)
            dm = tdofs(a) + tdofs(b)
            blk = np.block([[kk, -kk], [-kk, kk]])
            K[np.ix_(dm, dm)] += blk
        for a, b, kax in extra_springs:             # Scheibe: Diagonalfeder mit Steifigkeit kax [N/mm]
            d = self.nodes[b] - self.nodes[a]; d /= np.linalg.norm(d)
            kk = kax * np.outer(d, d)
            dm = tdofs(a) + tdofs(b)
            K[np.ix_(dm, dm)] += np.block([[kk, -kk], [-kk, kk]])

        fixed = []
        for nm in fixed_nodes:
            fixed += tdofs(nm)
        free = [i for i in range(ndof) if i not in set(fixed)]
        f = np.zeros(ndof)
        for nm, vec in loads.items():
            for k_, v in enumerate(vec):
                f[tdofs(nm)[k_]] += v
        Kff = K[np.ix_(free, free)] + 1e-6 * np.eye(len(free))
        u = np.zeros(ndof)
        u[free] = np.linalg.solve(Kff, f[free])
        # Eigenfrequenz (translatorische Massen an Knoten, Rotationen kondensiert)
        mt = [m for m in free if m < nt]
        rr = [m for m in free if m >= nt]
        Ktt = K[np.ix_(mt, mt)]
        Ktr = K[np.ix_(mt, rr)]
        Krr = K[np.ix_(rr, rr)] + 1e-6 * np.eye(len(rr))
        Kc = Ktt - Ktr @ np.linalg.solve(Krr, Ktr.T)
        mvec = np.array([self.masses.get(names[m // 3], 0.0) for m in mt]) + 1e-9
        Mm = np.diag(mvec)
        w2 = eigh(Kc, Mm, eigvals_only=True)
        w2 = w2[w2 > 1e-6]
        f1 = np.sqrt(w2[0] * 1000.0) / (2 * np.pi) if len(w2) else 0.0   # N/mm je kg = 1000 1/s2
        return u, ix, f1


def build(variant):
    F = Frame()
    corners = {"LV": (XL, YF), "RV": (XR, YF), "LH": (XL, YB), "RH": (XR, YB)}
    levels = {"U": Z_U, "L": Z_L}
    if variant >= 1:
        levels["F"] = Z_F
    for c, (x, y) in corners.items():
        F.node("%s_B" % c, x, y, 0.0)
        for lv, z in levels.items():
            F.node("%s_%s" % (c, lv), x, y, z)
    # Pfosten: durchlaufend (rigid) bis zum unteren Rahmen, oben angeschraubt (bolted)
    for c in corners:
        chain = [("B", 0.0)] + [(lv, z) for lv, z in sorted(levels.items(), key=lambda kv: kv[1])]
        for (l1, _), (l2, _) in zip(chain[:-1], chain[1:]):
            top = (l2 == "U")
            F.beam("%s_%s" % (c, l1), "%s_%s" % (c, l2), "rigid", "bolted" if top else "rigid")
    ring = [("LV", "RV"), ("LH", "RH"), ("LV", "LH"), ("RV", "RH")]
    for lv in ("U", "L"):
        for a, b in ring:
            if FRONT_OPEN and lv == "L" and (a, b) == ("LV", "RV"):
                continue
            F.beam("%s_%s" % (a, lv), "%s_%s" % (b, lv), "bolted", "bolted")
    if variant >= 1:   # Bodenstreben hinten und seitlich (vorne frei fuer Beine/Fuesse)
        for a, b in (("LH", "RH"), ("LV", "LH"), ("RV", "RH")):
            F.beam("%s_F" % a, "%s_F" % b, "bolted", "bolted")
    if variant >= 2:   # Diagonalen (2020, gelenkig) im unteren Feld: hinten und seitlich
        F.truss("LH_F", "RH_L"); F.truss("LV_F", "LH_L"); F.truss("RV_F", "RH_L")
    # Massen: Profile je zur Haelfte an die Endknoten, Aufbauten dazu
    for (a, b, *_r) in F.members:
        m = np.linalg.norm(F.nodes[b] - F.nodes[a]) * KG_M * 1.05
        F.mass(a, m / 2); F.mass(b, m / 2)
    for c in corners:
        F.mass("%s_U" % c, M_TOP / 4)
        F.mass("%s_L" % c, M_RACK / 4)
    return F


def tip_over():
    prof = 4 * Z_UP0 + 2 * W + 2 * (D - 2 * P) + 2 * (W - 2 * P) + 2 * (D - 2 * P)
    prof += 3 * (W - 2 * P)                              # Bodenstreben
    if FRONT_OPEN:
        prof -= (W - 2 * P)                              # kein vorderer unterer Träger
    m_prof = prof * KG_M * 1.05 + 3 * 1044 * 0.0004      # Diagonalen ca. 0,4 kg/m
    items = [(m_prof, DESK_H * 0.45), (M_PLATE + M_ESD, DESK_H), (M_ARMS, DESK_H + 100),
             (M_PORTAL, DESK_H + 300), (M_MISC, DESK_H + 50), (M_RACK, Z_L + 80)]
    M = sum(m for m, _ in items)
    zc = sum(m * z for m, z in items) / M
    return M, zc


def plate_check():
    """Durchbiegung der Siebdruckplatte unter 500 N Einzellast in Feldmitte (Streifenmodell, einfach gelagert).
    ANNAHMEN: E_Platte 6000 N/mm2 (konservativ), mittragende Breite 300 mm. Nur Groessenordnung."""
    Ep, b, Pn = 6000.0, 300.0, 500.0
    print("\nPLATTE: Durchbiegung unter 500 N in Feldmitte (Streifenmodell)")
    for t in (12.0, 18.0, 21.0):
        I = b * t**3 / 12.0
        out = []
        for label, L in (("ohne Mittelträger, Feld 920 mm", D - 2 * P),
                         ("mit Mittelträger, groesstes Feld", MID_Y - P / 2 - P - 0.0)):
            out.append("%s: %.1f mm" % (label, Pn * L**3 / (48 * Ep * I)))
        print("  %2.0f mm:  %s" % (t, "   ".join(out)))


if __name__ == "__main__":
    print("Tischhoehe (Oberkante ESD) %.0f mm | FOOT_H %.1f | Pfostenlaenge %.1f | Rahmen oben %.1f..%.1f"
          % (DESK_H, FOOT_H, Z_UP0, Z_UP0, Z_UP0 + P))
    M, zc = tip_over()
    half = (W - P) / 2                                   # kuerzester Hebel zur Kippkante (Pfostenmitte)
    h = DESK_H
    print("\nKIPPEN: Gesamtmasse ca. %.0f kg, Schwerpunkthoehe ca. %.0f mm" % (M, zc))
    print("  horizontale Kraft an der Tischkante (%.0f mm hoch), die den Tisch kippen wuerde: %.0f N (= %.0f kg)"
          % (h, M * g * half / h, M * half / h))
    print("  ohne Berechnung der Lastverschiebung durch Arme; Verlust der Ruhelage erst bei dieser Kraft.")

    plate_check()
    print("\nSEITENSTEIFIGKEIT (100 N horizontal am Tischrand, je 25 N auf die 4 oberen Ecken)")
    print("Angabe: Verschiebung der am staerksten verschobenen oberen Ecke und daraus Steifigkeit")
    print("kr = Drehfeder je Winkelverbindung (ANNAHME, N*mm/rad); f1 = 1. Eigenfrequenz (Massen siehe oben)")
    krs = [(5e5, "weich 0,5 kNm/rad"), (2e6, "mittel 2 kNm/rad"), (1e7, "steif 10 kNm/rad"), (1e12, "starr")]
    cases = [("V0 nur Rahmen+Pfosten", 0, 0.0),
             ("V1 + Bodenstreben hinten/seitlich", 1, 0.0),
             ("V2 + Diagonalen hinten/seitlich", 2, 0.0),
             ("V2 + Diagonalen, Platte als Scheibe (ANNAHME 1000 N/mm)", 2, 1000.0)]
    for nm, vi, kax in cases:
        print("\n%s" % nm)
        for kr, label in krs:
            row = []
            for direction, vec in (("X", (25.0, 0, 0)), ("Y", (0, 25.0, 0))):
                F = build(vi)
                fixed = ["%s_B" % c for c in ("LV", "RV", "LH", "RH")]
                loads = {"%s_U" % c: vec for c in ("LV", "RV", "LH", "RH")}
                extra = [("LV_U", "RH_U", kax), ("RV_U", "LH_U", kax)] if kax else []
                u, ix, f1 = F.solve(kr, fixed, loads, extra)
                ids = [ix["%s_U" % c] for c in ("LV", "RV", "LH", "RH")]
                dmax = max(abs(u[3 * i + ("XYZ".index(direction))]) for i in ids)
                row.append((dmax, 100.0 / max(dmax, 1e-9), f1))
            print("  %-22s X: %7.2f mm (%6.0f N/mm)  Y: %7.2f mm (%6.0f N/mm)  f1 ~ %.1f Hz"
                  % (label, row[0][0], row[0][1], row[1][0], row[1][1], min(row[0][2], row[1][2])))
