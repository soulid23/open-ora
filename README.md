# open-ora: Offener Reparatur-Assistent

Ein offener, modularer Reparaturtisch für Elektronik: Platinen werden
von Sensoren und lokaler KI gescannt, ein Halter-Arm positioniert,
ein Prober tastet Testpunkte ab.

## Status
Frühe Konzeptphase. Siehe `docs/decisions/`.

## Bestandteile
- Tisch: 500 x 600 mm, 4040-Aluprofil, ESD- und hitzefeste Arbeitsfläche
- Sensorik und KI: Kameras, lokale Auswertung (RTX 3070)
- Steuerung: Raspberry Pi, ESP32
- Druckteile für Qidi Max4 (Bauvolumen 390 x 390 x 340 mm)

## Lizenzen
- Hardware/CAD: CERN-OHL-W v2
- Software/Firmware: Apache-2.0
