"""open-ora | software/vision/ki-test/visuell.py | M1 KI-Test: Foto einer Platine von einem lokalen Bildmodell pruefen lassen.

Laeuft gegen Ollama auf diesem Rechner (http://localhost:11434), Modell Standard qwen3-vl:8b. Keine Cloud.

Aufrufe:
  python visuell.py foto P01 --kamera 0          # Foto mit Webcam nach daten/P01/foto.jpg
  python visuell.py pruefen P01                  # daten/P01/foto.jpg (oder alle *.jpg/*.png darin) pruefen
  python visuell.py pruefen P01 --mit-waerme     # Waerme-Befund aus waerme_auswertung.json mitgeben

Die Antwort wird nach daten/P01/visuell.json gespeichert. Der bekannte Defekt wird dem Modell NICHT gesagt
(Blindtest); er steht nur im Testprotokoll.
"""
import argparse
import base64
import json
import sys
import time
from pathlib import Path

import requests

HIER = Path(__file__).resolve().parent
DATEN = HIER / "daten"
OLLAMA = "http://localhost:11434/api/chat"

PROMPT = """Du bist Pruefer fuer Elektronik-Reparaturen. Das Bild zeigt eine Leiterplatte von oben.
Suche sichtbare Schaeden oder Auffaelligkeiten: verbrannte oder verfaerbte Bauteile oder Leiterbahnen,
aufgeblaehte oder ausgelaufene Elkos, Risse, fehlende oder verdrehte Bauteile, Loetbruecken, kalte oder gebrochene
Loetstellen, Korrosion, Fremdkoerper.
Antworte NUR mit JSON in dieser Form:
{"befund": "auffaellig" | "unauffaellig" | "unklar",
 "funde": [{"was": "...", "wo": "Lage auf dem Bild (z. B. oben links, neben dem grossen Elko)", "sicherheit": 0.0-1.0}],
 "naechster_schritt": "ein konkreter Messvorschlag fuer den Reparateur"}
Wenn du nichts Sicheres erkennst, gib "unklar" an und rate nicht."""


def foto(platine: str, index: int):
    import cv2
    cap = cv2.VideoCapture(index, cv2.CAP_DSHOW if sys.platform == "win32" else cv2.CAP_ANY)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 3840)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 2160)
    for _ in range(15):
        cap.read()
    ok, f = cap.read()
    cap.release()
    if not ok:
        sys.exit("Kein Bild von Kamera %d" % index)
    ziel = DATEN / platine
    ziel.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(ziel / "foto.jpg"), f, [cv2.IMWRITE_JPEG_QUALITY, 95])
    print("gespeichert:", ziel / "foto.jpg", f.shape)


def pruefen(platine: str, modell: str, mit_waerme: bool):
    ziel = DATEN / platine
    bilder = sorted([p for p in ziel.glob("*") if p.suffix.lower() in (".jpg", ".jpeg", ".png")
                     and not p.name.startswith("waerme")])
    if not bilder:
        sys.exit("Keine Fotos in %s" % ziel)
    text = PROMPT
    if mit_waerme and (ziel / "waerme_auswertung.json").exists():
        w = json.loads((ziel / "waerme_auswertung.json").read_text(encoding="utf-8"))
        text += "\n\nZusatzinfo aus dem Waermebild (256 x 192, andere Perspektive): %s. Funde: %s" % (
            w["befund"], json.dumps(w["funde"][:3], ensure_ascii=False))
    msg = {"role": "user", "content": text,
           "images": [base64.b64encode(p.read_bytes()).decode() for p in bilder]}
    t0 = time.time()
    try:
        r = requests.post(OLLAMA, json={"model": modell, "messages": [msg], "stream": False, "format": "json",
                                        "options": {"temperature": 0.2}}, timeout=600)
        r.raise_for_status()
    except requests.ConnectionError:
        sys.exit("Ollama laeuft nicht (http://localhost:11434). Ollama starten und 'ollama pull %s'." % modell)
    antwort = r.json()["message"]["content"]
    try:
        erg = json.loads(antwort)
    except json.JSONDecodeError:
        erg = {"befund": "unklar", "roh": antwort}
    erg.update({"platine": platine, "modell": modell, "bilder": [p.name for p in bilder],
                "sekunden": round(time.time() - t0, 1), "zeit": time.strftime("%Y-%m-%d %H:%M")})
    (ziel / "visuell.json").write_text(json.dumps(erg, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(erg, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest="cmd", required=True)
    a = sp.add_parser("foto"); a.add_argument("platine"); a.add_argument("--kamera", type=int, default=0)
    b = sp.add_parser("pruefen"); b.add_argument("platine"); b.add_argument("--modell", default="qwen3-vl:8b")
    b.add_argument("--mit-waerme", action="store_true")
    args = ap.parse_args()
    if args.cmd == "foto":
        foto(args.platine, args.kamera)
    else:
        pruefen(args.platine, args.modell, args.mit_waerme)
