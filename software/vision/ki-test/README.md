# KI-Test M1 (provisorisch, ohne Tisch)

Prüft, ob Wärmebild und ein lokales Bildmodell Fehler auf Platinen finden. Testplan und Protokoll:
`docs/tests/m1-ki-test.md`. Alles läuft lokal auf dem Desktop (RTX 3080, 10 GB), keine Cloud.

| Datei | Zweck |
|---|---|
| `waerme.py` | Wärmebild (Topdon TC001 / InfiRay P2 Pro) aufnehmen, heiße Stellen gegen Umgebung oder Referenzbild finden |
| `visuell.py` | Foto aufnehmen und vom Bildmodell `qwen3-vl:8b` (Ollama) als Blindtest prüfen lassen |
| `daten/<Platine>/` | Aufnahmen und Ergebnisse je Platine (nicht im Repo) |

## Einrichtung (einmalig, Windows)
OpenCV und andere Pakete gibt es für Python 3.15 oft noch nicht fertig, daher Python 3.12:
```
py install 3.12
cd /d C:\dev\open-ora\software\vision\ki-test
py -V:3.12 -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python waerme.py demo
```
`demo` prüft die Auswertung mit künstlichen Daten (ohne Kamera).

Bildmodell: Ollama für Windows von ollama.com installieren, dann
```
ollama pull qwen3-vl:8b
```
(ca. 6 GB; nicht gleichzeitig mit anderen großen Modellen auf der Karte, ADR 0005).

## Ablauf je Platine (Kurzform)
```
python visuell.py foto P01 --kamera 0          (oder Handyfoto als daten\P01\foto.jpg ablegen)
python visuell.py pruefen P01
python waerme.py probe                         (einmal: welcher Index ist die Wärmebildkamera?)
python waerme.py aufnehmen P01 --name ref --kamera 1    (ohne Strom)
python waerme.py aufnehmen P01 --kamera 1               (mit Strom, nach 30 bis 60 s)
python waerme.py auswerten P01
python visuell.py pruefen P01 --mit-waerme
```

## Hinweise
- Wärmebild nur an Platinen mit Schutzkleinspannung und strombegrenzter Versorgung (SAFETY.md). Netzteilplatinen
  nie unter Strom prüfen.
- Raspberry Pi / Banana Pi werden für M1 nicht gebraucht: beide Kameras hängen per USB am Desktop.
- Rohformat der Wärmebildkamera unter Windows ist nicht mit echter Kamera getestet. Falls `probe` kein
  Wärmebild findet, Ausgabe notieren; Plan B ist der Banana Pi / Raspberry Pi mit Linux (V4L2), dort ist das Format
  von PyThermalCamera bekannt.
