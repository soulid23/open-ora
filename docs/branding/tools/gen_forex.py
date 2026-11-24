import json, os
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "gen_logo.py")).read().split("# ---------- SVG ----------")[0])
INK, LIGHT, ACC, TAG = "#16181B", "#F4F2EE", "#E8743B", "#C9C6C0"
lock = geo["lockup"]; url = geo["url"]
def place(faces, em, ox, oy, color_override=None):
    out = []
    for f in faces:
        out.append({"color": color_override or f["color"],
                    "loops": [[[round(ox + x * em, 3), round(oy + y * em, 3)] for x, y in l] for l in f["loops"]]})
    return out
def panel(kind):
    if kind == "seite":
        W, H = 936.0, 150.4
        em = 118.0
        bx0, by0, bx1, by1 = lock["bbox"]
        lh = (by1 - by0) * em
        ox = 40 - bx0 * em; oy = (H - lh) / 2 - by0 * em
        faces = place(lock["faces"], em, ox, oy)
        us = 30.0
        ub = url["bbox"]
        faces += place(url["faces"], us, 896 - ub[2] * us, oy, "url")       # auf der Grundlinie des Schriftzugs
    else:
        W, H = 225.0, 150.4
        bx0, by0, bx1, by1 = lock["bbox"]
        em = 185.0 / (bx1 - bx0)
        us = 14.0; ub = url["bbox"]
        lh = (by1 - by0) * em; gap = 14.0; uh = (ub[3] - ub[1]) * us
        tot = lh + gap + uh
        top = (H + tot) / 2
        oy = top - by1 * em; ox = (W - (bx1 - bx0) * em) / 2 - bx0 * em
        faces = place(lock["faces"], em, ox, oy)
        uy = oy + by0 * em - gap - ub[3] * us
        faces += place(url["faces"], us, (W - (ub[2] - ub[0]) * us) / 2 - ub[0] * us, uy, "url")
    return W, H, faces
layout = {"einheit": "mm, Ursprung unten links der Platte (Zuschnitt), y nach oben", "farben": {"ink": LIGHT, "tag": TAG, "accent": ACC, "url": LIGHT, "grund": INK}}
for k in ("seite", "hinten"):
    W, H, faces = panel(k)
    layout[k] = {"w": W, "h": H, "faces": faces}
    cols = layout["farben"]
    d = {}
    for f in faces:
        d.setdefault(f["color"], []).append(" ".join("M" + " L".join(f"{x:.3f} {H - y:.3f}" for x, y in l) + " Z" for l in f["loops"]))
    svgp = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}mm" height="{H}mm" viewBox="0 0 {W} {H}">', f'<rect width="{W}" height="{H}" fill="{INK}"/>']
    for c, ps in d.items():
        svgp.append(f'<path fill="{cols[c]}" fill-rule="nonzero" d="{" ".join(ps)}"/>')
    svgp.append("</svg>")
    name = "forex-seite-936x150.svg" if k == "seite" else "forex-hinten-225x150.svg"
    open(os.path.join(OUT, name), "w").write("\n".join(svgp))
json.dump(layout, open(os.path.join(OUT, "forex_layout.json"), "w"))
print("ok")
