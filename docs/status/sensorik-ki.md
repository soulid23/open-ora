# Status: sensorik-ki

## Ziel
Kamera und Wärmebild über dem Tisch erkennen Fehler auf Platinen (heiße Bauteile, Kurzschlüsse, sichtbare Schäden);
eine lokale KI wertet aus und schlägt nächste Schritte vor. Ohne Cloud.

## Aktueller Stand (2026-11-25)
- Laut ADR 0008 ist das das größte Risiko des Projekts und wird zuerst getestet (Meilenstein M1, provisorischer
  Aufbau auf Stativ, Auswertung auf der RTX 3080).
- Licht- und Sensorrahmen als FreeCAD-Makro v1 (`light_frame.py`, 22.11.) vorhanden, aber noch nicht im Repo:
  Portal aus 4040 mit vier Stützen außen am Tisch, LED-Panel 595 x 595 mm, Sensorschiene mit Hauptkamera,
  Wärmebild, ToF und Reserveplätzen.
- Rechnerrollen nach ADR 0005: Training auf dem Desktop (RTX 3080), Echtzeit-Erkennung auf dem Laptop am Tisch.

## Entscheidungen (Verweise auf docs/decisions/)
- `0005-rechnerrollen.md`
- `0008-version1-modularer-tisch-normen.md` (KI-Test zuerst)

## Offene Fragen
- Welches Wärmebildmodul (Auflösung reicht für Bauteile auf Platinen?) und welche Kamera?
- Woher kommen Testplatinen mit bekanntem Defekt (eigene, Repair Café)?
- Höhe und Lage des Kameraportals (offene Frage 1), Konflikt hintere rechte Stütze (offene Frage 5).

## Nächste Schritte
1. Testaufbau für M1 planen: Stativ, Kamera, Wärmebildmodul, Beleuchtung, Stromversorgung der Testplatinen.
2. Testplatinen sammeln und je Platine den bekannten Defekt beschreiben.
3. Erfolgskriterium aus `docs/plan.md` (M1) bestätigen oder anpassen.
4. `light_frame.py` ins Repo.

## Abhängigkeiten zu anderen Baustellen
- **Tisch**: Licht- und Sensorrahmen mit vier Stützen außen am Tisch.
- **Elektronik**: Raspberry Pi für die Kameras, Netzwerk zum Laptop.
- **Stromversorgung**: LED-Panel und Treiber, Versorgung der Testplatinen (strombegrenzt).
