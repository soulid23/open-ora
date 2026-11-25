# open-ora: Offener Reparatur-Assistent

Ein offener, modularer Reparaturtisch für Elektronik: Ein Halter-Arm bringt die Platine in Position,
ein Prober tastet Testpunkte ab, Kameras und eine lokale KI helfen bei der Fehlersuche.

Webseite: [www.open-ora.de](https://www.open-ora.de)

## Status
Konzept- und Konstruktionsphase. Alles wird parametrisch in FreeCAD 1.1 (Python-Makros) konstruiert.

| Baugruppe | Stand |
|---|---|
| Tisch | Version 1 konstruiert (FreeCAD-Modell), Bestellung in Vorbereitung |
| Arm 1 (Halter) | Version 2; Konzept vorgeschlagen (ADR 0007), Fuß als abnehmbares Außenmodul modelliert |
| Licht- und Sensorrahmen | Makro v2 konstruiert (Portal an den Seitenholmen, LED-Panel, Sensorschiene) |
| Arm 2 (Prober) | Version 2, offen |
| Sensorik, Elektronik, KI | offen |

Version 1 umfasst Tisch, Licht- und Sensorrahmen, Kamera, Wärmebild und KI; die Arme folgen in Version 2 (ADR 0008).
Plan und Meilensteine: `docs/plan.md`. Entscheidungen: `docs/decisions/`. Stand je Baustelle: `docs/status/`.

## Bestandteile
- **Tisch**: 1000 x 1000 mm, Arbeitshöhe 740 mm (Oberkante ESD-Matte), Rahmen aus Alu-Nutprofil 4040,
  18-mm-Siebdruckplatte mit ESD-Matte, Sitzplatz vorn frei, 19"-Rack (3 HE) hinten, Forex-Verkleidung mit Logo (ADR 0006)
- **Licht- und Sensorrahmen**: Portal aus 4040 an den Seitenholmen, LED-Panel 595 x 595 mm, Sensorschiene für Kameras,
  Wärmebild und ToF
- **Arme** (Version 2): Halter (Nutzlast bis 1 kg, SCARA mit Hubsäule) hinten rechts, Prober (Präzision) noch offen
- **Sensorik und KI**: Kameras, Wärmebild, ToF über dem Tisch; Auswertung lokal, ohne Cloud
- **Rechner** (ADR 0005): Desktop (RTX 3080) für Entwicklung und Training, Laptop am Tisch (RTX 3070) für die
  Echtzeit-Erkennung, Raspberry Pi für Kameras und Bahnplanung, ESP32 für Motoren und Sensoren
- **Druckteile** für Qidi Max4 (Bauvolumen 390 x 390 x 340 mm)

## Aufbau des Repos
| Ordner | Inhalt |
|---|---|
| `cad/macros/` | FreeCAD-Makros (`frame_4040.py` Tisch, `light_frame.py` Licht- und Sensorrahmen, `arm_holder.py` Arm 1) |
| `cad/analysis/` | Überschlagsrechnungen (Steifigkeit Tisch, Auslegung Arm 1) |
| `bom/` | Stücklisten und Bestelllisten |
| `docs/` | Entscheidungen, Status, Schnittstellen, Bilder, Branding und Webseite |
| `firmware/`, `software/` | noch leer |

Die FreeCAD-Dateien (`*.FCStd`) sind nicht im Repo; sie entstehen aus den Makros.

## Sicherheit
Nachbau auf eigene Verantwortung. Arbeiten an Netzspannung nur durch eine Elektrofachkraft, siehe `SAFETY.md`.

## Lizenzen
- Hardware/CAD: CERN-OHL-W v2
- Software/Firmware: Apache-2.0
