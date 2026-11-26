"""open-ora | software/vision/ki-test/waerme.py | M1 KI-Test: Waermebild aufnehmen und auswerten.

Kamera: Topdon TC001 oder InfiRay P2 Pro (256 x 192, USB-UVC). Beide liefern ein Bild mit 256 x 384 Pixeln:
obere Haelfte Anzeigebild, untere Haelfte Temperaturen (16 Bit, Einheit 1/64 Kelvin).

Aufrufe (im Ordner software/vision/ki-test, venv aktiv):
  python waerme.py probe                         # Kameras suchen, Bildformat anzeigen
  python waerme.py aufnehmen P01 --kamera 1      # Platine P01: Waermebild nach daten/P01/ speichern
  python waerme.py aufnehmen P01 --name ref      # Referenzbild (gleiche Platine, ohne Strom oder Gut-Platine)
  python waerme.py auswerten P01                 # Heisse Stellen finden, Bild + JSON nach daten/P01/
  python waerme.py demo                          # Auswertung mit kuenstlichen Daten testen (ohne Kamera)

Nur Platinen mit Schutzkleinspannung und strombegrenzter Versorgung pruefen (SAFETY.md).
"""
import argparse
import json
import sys
import time
from pathlib import Path

import numpy as np
import cv2

HIER = Path(__file__).resolve().parent
DATEN = HIER / "daten"
W, H = 256, 192


# ---------------------------------------------------------------- Kamera
def oeffnen(index: int):
    """Kamera ohne Farbumwandlung oeffnen, sonst gehen die Temperaturdaten verloren."""
    backends = [cv2.CAP_DSHOW, cv2.CAP_MSMF, cv2.CAP_ANY] if sys.platform == "win32" else [cv2.CAP_V4L2, cv2.CAP_ANY]
    for be in backends:
        cap = cv2.VideoCapture(index, be)
        if not cap.isOpened():
            continue
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, W)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 2 * H)
        cap.set(cv2.CAP_PROP_CONVERT_RGB, 0)
        ok, f = cap.read()
        if ok and f is not None and f.size >= W * 2 * H * 2:
            return cap
        cap.release()
    return None


def roh_zu_temp(frame: np.ndarray) -> np.ndarray:
    """Rohbild (YUYV, 256 x 384 x 2 Bytes) -> Temperaturfeld 192 x 256 in Grad C."""
    a = np.asarray(frame, dtype=np.uint8).reshape(-1)
    if a.size < W * 2 * H * 2:
        raise ValueError("Bild zu klein (%d Bytes): Kamera liefert kein 256 x 384 YUYV" % a.size)
    a = a[: W * 2 * H * 2].reshape(2 * H, W, 2)
    t = a[H:, :, 0].astype(np.uint16) | (a[H:, :, 1].astype(np.uint16) << 8)
    return t.astype(np.float32) / 64.0 - 273.15


def aufnehmen(platine: str, index: int, name: str, mittel: int) -> Path:
    cap = oeffnen(index)
    if cap is None:
        sys.exit("Keine Waermebildkamera mit 256 x 384 Bildern an Index %d. Erst 'python waerme.py probe'." % index)
    for _ in range(10):          # Kamera einschwingen lassen
        cap.read()
    bilder = []
    while len(bilder) < mittel:
        ok, f = cap.read()
        if ok:
            bilder.append(roh_zu_temp(f))
    cap.release()
    t = np.mean(bilder, axis=0)  # mitteln gegen Rauschen
    ziel = DATEN / platine
    ziel.mkdir(parents=True, exist_ok=True)
    np.save(ziel / ("waerme_%s.npy" % name), t)
    cv2.imwrite(str(ziel / ("waerme_%s.png" % name)), farbbild(t))
    print("gespeichert: %s  (min %.1f / median %.1f / max %.1f Grad C, %d Bilder gemittelt)"
          % (ziel / ("waerme_%s.npy" % name), t.min(), np.median(t), t.max(), mittel))
    return ziel


def probe():
    print("Suche Kameras 0..5 ...")
    for i in range(6):
        cap = oeffnen(i)
        if cap is None:
            c2 = cv2.VideoCapture(i)
            if c2.isOpened():
                ok, f = c2.read()
                print("  %d: Kamera, aber kein Waermebild-Rohformat (%s)" % (i, None if not ok else f.shape))
            c2.release()
            continue
        ok, f = cap.read()
        t = roh_zu_temp(f)
        print("  %d: WAERMEBILD erkannt, Rohdaten %s, Temperatur %.1f .. %.1f Grad C" % (i, f.shape, t.min(), t.max()))
        cap.release()


# ---------------------------------------------------------------- Auswertung
def farbbild(t: np.ndarray, lo=None, hi=None, gross=3) -> np.ndarray:
    lo = np.percentile(t, 1) if lo is None else lo
    hi = max(np.percentile(t, 99.9), lo + 1) if hi is None else hi
    g = np.clip((t - lo) / (hi - lo) * 255, 0, 255).astype(np.uint8)
    img = cv2.applyColorMap(g, cv2.COLORMAP_INFERNO)
    return cv2.resize(img, (t.shape[1] * gross, t.shape[0] * gross), interpolation=cv2.INTER_NEAREST)


def heisse_stellen(t: np.ndarray, ref: np.ndarray | None, delta: float, min_px: int):
    """Stellen, die mehr als `delta` Kelvin ueber der Umgebung (Median) oder ueber dem Referenzbild liegen."""
    basis = ref if ref is not None else np.full_like(t, float(np.median(t)))
    d = t - basis
    maske = (d > delta).astype(np.uint8)
    n, lab, stats, cent = cv2.connectedComponentsWithStats(maske, connectivity=8)
    funde = []
    for k in range(1, n):
        x, y, w, h, a = stats[k]
        if a < min_px:
            continue
        sel = lab == k
        iy, ix = np.unravel_index(np.argmax(np.where(sel, t, -1e9)), t.shape)
        funde.append({"x": int(ix), "y": int(iy), "box": [int(x), int(y), int(w), int(h)], "pixel": int(a),
                      "t_max": round(float(t[iy, ix]), 1), "ueber_basis": round(float(d[iy, ix]), 1)})
    funde.sort(key=lambda f: -f["ueber_basis"])
    return funde, float(np.median(basis))


def auswerten(platine: str, delta: float, min_px: int, name="mess") -> dict:
    ziel = DATEN / platine
    t = np.load(ziel / ("waerme_%s.npy" % name))
    ref = ziel / "waerme_ref.npy"
    ref = np.load(ref) if ref.exists() else None
    funde, umgebung = heisse_stellen(t, ref, delta, min_px)
    img = farbbild(t)
    for i, f in enumerate(funde[:5], 1):
        x, y, w, h = [v * 3 for v in f["box"]]
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 255), 1)
        cv2.putText(img, "%d: %.1f C" % (i, f["t_max"]), (x, max(12, y - 4)), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 255, 255), 1)
    cv2.imwrite(str(ziel / "waerme_auswertung.png"), img)
    erg = {"platine": platine, "zeit": time.strftime("%Y-%m-%d %H:%M"), "basis": "Referenzbild" if ref is not None else "Median",
           "umgebung_c": round(umgebung, 1), "schwelle_k": delta, "funde": funde,
           "befund": ("heisse Stelle(n) gefunden" if funde else "keine heisse Stelle ueber der Schwelle")}
    (ziel / "waerme_auswertung.json").write_text(json.dumps(erg, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(erg, indent=2, ensure_ascii=False))
    return erg


def demo():
    """Kuenstliche Platine: 25 Grad, ein Regler mit 30 K Uebertemperatur, ein Kurzschluss-Punkt mit 12 K."""
    rng = np.random.default_rng(1)
    ref = 25 + rng.normal(0, 0.15, (H, W)).astype(np.float32)
    t = ref.copy() + 1.0                                  # Platine insgesamt leicht warm
    yy, xx = np.mgrid[0:H, 0:W]
    t += 30 * np.exp(-((xx - 60) ** 2 + (yy - 50) ** 2) / (2 * 4 ** 2))
    t += 12 * np.exp(-((xx - 180) ** 2 + (yy - 120) ** 2) / (2 * 2 ** 2))
    ziel = DATEN / "DEMO"
    ziel.mkdir(parents=True, exist_ok=True)
    np.save(ziel / "waerme_ref.npy", ref)
    np.save(ziel / "waerme_mess.npy", t)
    erg = auswerten("DEMO", delta=5.0, min_px=3)
    assert len(erg["funde"]) == 2 and abs(erg["funde"][0]["x"] - 60) <= 1, "Demo fehlgeschlagen"
    print("Demo ok: 2 heisse Stellen gefunden.")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest="cmd", required=True)
    sp.add_parser("probe")
    sp.add_parser("demo")
    a = sp.add_parser("aufnehmen"); a.add_argument("platine"); a.add_argument("--kamera", type=int, default=1)
    a.add_argument("--name", default="mess", help="mess oder ref"); a.add_argument("--mittel", type=int, default=25)
    b = sp.add_parser("auswerten"); b.add_argument("platine")
    b.add_argument("--schwelle", type=float, default=5.0, help="Kelvin ueber Umgebung/Referenz (Standard 5)")
    b.add_argument("--min-pixel", type=int, default=3)
    args = ap.parse_args()
    if args.cmd == "probe":
        probe()
    elif args.cmd == "demo":
        demo()
    elif args.cmd == "aufnehmen":
        aufnehmen(args.platine, args.kamera, args.name, args.mittel)
    else:
        auswerten(args.platine, args.schwelle, args.min_pixel)
