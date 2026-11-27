# open-ora: Offener Reparatur-Assistent

Ein offener, modularer Werkstatttisch aus Alu-Nutprofilen. Die erste Anwendung ist ein Reparatur-Assistent für
Elektronik: Licht, Kamera und Wärmebild über dem Tisch, eine lokale KI hilft bei der Fehlersuche. Derselbe Tisch
trägt auch andere Module, z. B. einen 3D-Drucker oben und Filament-Trockner im Unterbau.

Webseite: [www.open-ora.de](https://www.open-ora.de)

## Status
Konstruktionsphase, erster Test der KI läuft an. Alles wird parametrisch in FreeCAD 1.1 (Python-Makros) konstruiert.

| Baugruppe | Stand |
|---|---|
| Tisch | konstruiert in zwei Ausführungen: schwer mit oberem Rahmen 8080 (ADR 0010) und leicht mit 4080 flach, dazu eine Variante mit Motedis-Teilen; Einkaufslisten erstellt, Bestellung in Vorbereitung |
| Licht- und Sensorrahmen | Makro v2 konstruiert (Portal an den Seitenholmen, LED-Panel, Sensorschiene), noch auf Tischhöhe 740 mm ausgelegt |
| KI-Test (M1) | in Arbeit: Testplan und Skripte für Wärmebild und lokales Bildmodell (`software/vision/ki-test/`) |
| Sensorik, Elektronik | offen |
| Arm 1 (Halter), Arm 2 (Prober) | Version 2; Arm 1 als Konzept (ADR 0007) |

Version 1 umfasst Tisch, Licht- und Sensorrahmen, Kamera, Wärmebild und KI; die Arme folgen in Version 2 (ADR 0008).
Plan und Meilensteine: `docs/plan.md`. Entscheidungen: `docs/decisions/`. Stand je Baustelle: `docs/status/`.

## Bestandteile
- **Tisch**: 1000 x 1000 mm, Arbeitshöhe 780 mm (Oberkante ESD-Matte). Beine, unterer Rahmen und Streben aus
  Nutprofil 4040, oberer Rahmen 8080 (schwer) oder 4080 flach (leicht); innere Nutreihe trägt die Platte, äußere
  bleibt frei für Anbauten. Feste Querstrebe, 19"-Rackkasten (3 HE) hinten, Siebdruckplatte 920 x 920 x 18 mm mit
  29 Senkschrauben (Bohrplan `docs/build-guide/bohrplan_platte_8080.pdf`), ESD-Matte, Forex-Verkleidung mit Logo,
  Sitzplatz vorn frei (ADR 0006, 0010)
- **Modularität**: Anwendungen, Zonen, Tischverbund (Strom, Ethernet, RS485/CAN über RJ45) und Wechselplatten in
  `docs/interfaces/module.md` (ADR 0009)
- **Licht- und Sensorrahmen**: Portal aus 4040 an den Seitenholmen, LED-Panel 595 x 595 mm, Sensorschiene für Kameras,
  Wärmebild und ToF
- **Sensorik und KI**: Kamera und Wärmebild über dem Tisch; Auswertung lokal mit einem Bildmodell, ohne Cloud
- **Arme** (Version 2): Halter (Nutzlast bis 1 kg, SCARA mit Hubsäule) hinten rechts, Prober noch offen
- **Rechner** (ADR 0005): Desktop (RTX 3080) für Entwicklung und Training, Laptop am Tisch (RTX 3070) für die
  Echtzeit-Erkennung, Raspberry Pi für Kameras, ESP32 für Motoren und Sensoren
- **Druckteile** für Qidi Max4 (Bauvolumen 390 x 390 x 340 mm)

## Aufbau des Repos
| Ordner | Inhalt |
|---|---|
| `cad/macros/` | FreeCAD-Makros: `tisch_8080.py` (schwer), `tisch_4080.py` (leicht), `tisch_4080_motedis.py` (leicht, Motedis-Teile aus STEP), `frame_4040.py` (Version 1), `light_frame.py` (Licht- und Sensorrahmen), `arm_holder.py` (Arm 1) |
| `cad/analysis/` | Überschlagsrechnungen (Steifigkeit Tisch, Auslegung Arm 1) |
| `bom/` | Stücklisten je Makro (`tisch_8080_bom.csv`, `tisch_4080_bom.csv`, `tisch_4080_motedis_bom.csv`, ...) |
| `software/vision/ki-test/` | KI-Test M1: Wärmebild (Topdon TC001 / InfiRay P2 Pro) und Bildmodell über Ollama |
| `docs/` | Plan, Entscheidungen, Status, Schnittstellen, Testpläne, Bauanleitung, Bilder, Branding und Webseite |
| `firmware/` | noch leer |

Die FreeCAD-Dateien (`*.FCStd`) sind nicht im Repo, sie entstehen aus den Makros. Herstellerdaten (STEP von Alux und
Motedis) liegen ebenfalls nicht im Repo; die Makros nennen die Quelle.

## Sicherheit
Nachbau auf eigene Verantwortung. Arbeiten an Netzspannung nur durch eine Elektrofachkraft, siehe `SAFETY.md`.

## Lizenzen
- Hardware/CAD: CERN-OHL-W v2
- Software/Firmware: Apache-2.0
