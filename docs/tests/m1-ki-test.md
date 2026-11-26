# Testplan M1: KI-Test provisorisch

Stand 2026-11-26. Gehört zu Meilenstein M1 in `docs/plan.md`, Baustelle sensorik-ki. Software: `software/vision/ki-test/`.

## Frage
Findet ein Aufbau aus Kamera, Wärmebildkamera und lokalem Bildmodell bekannte Fehler auf Platinen so zuverlässig,
dass sich der Tisch mit Licht- und Sensorrahmen lohnt?

**Erfolgskriterium** (aus dem Plan): bei mindestens 5 Platinen mit bekanntem Defekt wird der Fehler in mindestens 4 Fällen
angezeigt (heißes Bauteil, Kurzschluss oder sichtbarer Schaden). Ein Fund zählt, wenn Ort **und** Art stimmen.
Zusätzlich je Platine notieren: falsche Funde, Laufzeit.

## Aufbau (provisorisch, ohne Tisch)
| Teil | Wahl | Status |
|---|---|---|
| Rechner | Desktop, RTX 3080 10 GB, Python 3.12, Ollama | Python 3.12 und Ollama fehlen noch |
| Bildmodell | `qwen3-vl:8b` (ca. 6 GB) über Ollama | zu installieren |
| Kamera sichtbar | vorerst Handy oder Webcam; später Pi Camera Module 3 am Raspberry Pi 5 | vorhanden |
| Wärmebild | Topdon TC001 oder InfiRay P2 Pro (256 x 192, USB, Rohtemperaturen auslesbar), ca. 220 bis 270 EUR | zu kaufen |
| Halterung | Stativ oder Schwanenhals, Kamera 200 bis 300 mm über der Platine | offen |
| Licht | helle, gleichmäßige Beleuchtung ohne harte Reflexe (Schreibtischlampe seitlich) | vorhanden |
| Versorgung der Testplatinen | Labornetzteil mit Strombegrenzung, nur Schutzkleinspannung | zu klären |
| Raspberry Pi / Banana Pi | für M1 nicht nötig; Plan B, falls die Wärmebildkamera unter Windows kein Rohformat liefert | Banana Pi vorhanden, Pi 5 bestellt |

Auflösung Wärmebild (56° x 42°, 256 x 192): in 300 mm Abstand ca. 1,25 mm je Pixel, in 200 mm ca. 0,8 mm.
Ein Bauteil 0603 ist damit 1 bis 2 Pixel groß, Regler, Transistoren und ICs gut erkennbar. Das ist der Grund gegen
ein MLX90640 (32 x 24): dort wäre ein Pixel in 300 mm Abstand rund 10 mm groß.

## Testplatinen
| Nr. | Platine | Defekt (Wahrheit) | geprüft mit | Hinweise |
|---|---|---|---|---|
| P01 | Subwoofer, Netzteilplatine | vermutlich durchgebrannt: Bauteile und Ort vorher feststellen und fotografieren | nur Foto, **ohne Strom** | Netzseite: Elkos vor dem Anfassen entladen prüfen |
| P02 | Subwoofer, Endstufe | vermutlich durchgebrannt: wie P01 | nur Foto, ohne Strom | Endstufe hängt an hohen Versorgungsspannungen: nicht unter Strom setzen |
| P03 | Kleinspannungsplatine, z. B. Spannungsreglermodul oder Arduino-Klon, Abblockkondensator kurzgeschlossen (Lötbrücke) | Regler oder Kurzschlussstelle wird heiß | Wärmebild + Foto, 5 V strombegrenzt | präparierter Fehler, Ort bekannt |
| P04 | Kleinspannungsplatine, Lötbrücke zwischen IC-Pins | sichtbar, eventuell warm | Foto + Wärmebild | präpariert |
| P05 | Platine mit defektem oder verpoltem Bauteil (z. B. Diode, Elko) | Bauteil warm oder sichtbar beschädigt | Foto + Wärmebild | präpariert |
| P06 | Gut-Platine (kein Fehler) | keiner | Foto + Wärmebild | prüft falsche Funde |

Bei P01 und P02 ist der Defekt nur „wahrscheinlich“. Für die Wertung brauchen wir die Wahrheit **vor** dem KI-Test:
sichtbare Schäden fotografieren und beschreiben, mit dem Multimeter (ohne Strom) Kurzschlüsse an Endstufen-Transistoren,
Gleichrichter und Sicherung prüfen. Das Modell bekommt diese Beschreibung nicht (Blindtest).

## Ablauf je Platine
1. Wahrheit festhalten (Tabelle oben, Fotos), Platine nummerieren.
2. Foto von oben, Platine füllt das Bild, Licht seitlich: `python visuell.py foto P0x` oder Handyfoto als `daten/P0x/foto.jpg`.
3. `python visuell.py pruefen P0x`
4. Nur Kleinspannungsplatinen: Wärmebild ohne Strom als Referenz, dann mit Strom (Strombegrenzung zuerst niedrig,
   30 bis 60 s warten), `python waerme.py auswerten P0x`, danach `python visuell.py pruefen P0x --mit-waerme`.
5. Ergebnis ins Protokoll.

## Protokoll
| Nr. | Wahrheit | Bildmodell: Befund | Wärmebild: Befund | Treffer (Ort und Art) | falsche Funde | Laufzeit | Bemerkung |
|---|---|---|---|---|---|---|---|
| P01 | | | (entfällt) | | | | |
| P02 | | | (entfällt) | | | | |
| P03 | | | | | | | |
| P04 | | | | | | | |
| P05 | | | | | | | |
| P06 | kein Fehler | | | | | | |

## Sicherheit
- Unter Strom nur Platinen mit Schutzkleinspannung und Labornetzteil mit Strombegrenzung (SAFETY.md).
- Netzteil- und Endstufenplatinen aus Netzgeräten bleiben stromlos. Große Elkos können auch ausgebaut noch geladen
  sein: vor dem Anfassen Spannung messen, bei Bedarf über einen Widerstand entladen.
- Heiße Bauteile nicht anfassen, Platine auf eine nicht brennbare Unterlage legen.

## Danach
Ergebnis gegen das Erfolgskriterium werten, kurzer Baubericht, Status `docs/status/sensorik-ki.md` aktualisieren.
Wenn das Kriterium verfehlt wird: Ursache notieren (Auflösung, Licht, Modell), bevor Geld in den Lichtrahmen geht.
