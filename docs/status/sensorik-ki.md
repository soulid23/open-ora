# Status: sensorik-ki

## Ziel
Kamera und Wärmebild über dem Tisch erkennen Fehler auf Platinen (heiße Bauteile, Kurzschlüsse, sichtbare Schäden);
eine lokale KI wertet aus und schlägt nächste Schritte vor. Ohne Cloud.

## Aktueller Stand (2026-11-25)
- Laut ADR 0008 ist das das größte Risiko des Projekts und wird zuerst getestet (Meilenstein M1, provisorischer
  Aufbau auf Stativ, Auswertung auf der RTX 3080).
- **Licht- und Sensorrahmen: Makro v2 `cad/macros/light_frame.py` im Repo** (Bilder `docs/images/lichtrahmen_v2_iso.png`,
  `lichtrahmen_v2_seite.png`).
  - Portal aus Alux 4040: 4 Stützen außen am Tisch (x -40..0 und 1000..1040), Mitte y 600..640, hinten y 920..960
    (vor dem Erdungspunkt). Stützen z 505,6..1460 (ca. 954 mm), **nur an den oberen beiden Seitenholmen verschraubt**
    (Y_oben_* z 680..720 und Y_unten_* z 505,6..545,6, je 2 Verbinder), kein Bodenkontakt (Vorgabe Nutzer 2026-11-25).
  - Ausleger 2 × 860 mm (y 100..960), Oberkante z 1500; Traversen vorn (y 100), Panel hinten (y 760), hinten (y 920),
    je 1000 mm. Sensorschiene 2020 quer (y 440..460, z 1393..1413), 1000 mm. Zusammen ca. 8,5 m 4040 und 1 m 2020.
  - LED-Panel 595 x 595 mm (Mitte x 500 / y 450), Unterkante z 1423 = 683 mm über der Matte, an 4 Abhängern.
  - Sensorplätze: Hauptkamera Mitte, Wärmebild, ToF, 2 Reserven; Schrägkamera unter der vorderen Traverse;
    LED-Treiber auf der hinteren Traverse. Abhänger und Halter vorerst nur Platzhalter (Druckteil oder Alu-Winkel).
  - Makro übernimmt Tischmaß und Holmhöhen aus dem offenen Tischdokument und schreibt `bom/light_frame_bom.csv`.
  - Geprüft an einer Kopie von Tisch V1 (Frame22): 24 Objekte, 0 Kollisionen, alle Stützen liegen an beiden Holmen an.
    Die linke Mittelstütze und beide hinteren Stützen verdecken Teile des Logo-Drucks der Seitenplatten (vom Nutzer
    akzeptiert). Profile im Modell vereinfacht (Vollquader ohne Nuten).
  - Abschätzung (I 4040 = 9 cm⁴ angenommen, Alux-Datenblatt prüfen): Panel 4000 lm gibt ca. 3200 lx Mitte Platine,
    ca. 2200 lx Mitte Matte, ca. 800 lx Ecke Arbeitsfeld; Rahmen seitlich ca. 190 N/mm, f1 ca. 22 Hz (Tisch starr
    gerechnet); Ausleger 0,4 mm bei 30 N an der Spitze; Kamera Cam 3 (66° x 41°): ca. 600 x 345 mm Bildfeld auf
    Platinenhöhe, 0,13 mm/px.
- Rechnerrollen nach ADR 0005: Training auf dem Desktop (RTX 3080), Echtzeit-Erkennung auf dem Laptop am Tisch.

## Entscheidungen (Verweise auf docs/decisions/)
- `0005-rechnerrollen.md`
- `0008-version1-modularer-tisch-normen.md` (KI-Test zuerst, Lichtrahmen gehört zu Version 1)

## Offene Fragen
- Welches Wärmebildmodul (Auflösung reicht für Bauteile auf Platinen?) und welche Kamera?
- Woher kommen Testplatinen mit bekanntem Defekt (eigene, Repair Café)?
- Höhe und Lage des Kameraportals (offene Frage 1), Konflikt hintere rechte Stütze mit dem Arm-Außenmodul
  (offene Frage 5, erst für Version 2).
- Kopffreiheit im Stehen: vordere Traverse Unterkante z 1460.
- Verbinder Stütze an Seitenholm: Typ und Tragfähigkeit (nur 2 Verbinder je Stütze), Alux-Artikelnummern.
- LED-Panel: CRI ≥ 90, flimmerfrei, dimmbar; Kabelführung in der Nut.

## Nächste Schritte
1. Testaufbau für M1 planen: Stativ, Kamera, Wärmebildmodul, Beleuchtung, Stromversorgung der Testplatinen.
2. Testplatinen sammeln und je Platine den bekannten Defekt beschreiben.
3. Erfolgskriterium aus `docs/plan.md` (M1) bestätigen oder anpassen.
4. Lichtrahmen: Portalhöhe bestätigen (offene Frage 1), Verbinder wählen, Abhänger und Halter als Druckteile konstruieren.

## Abhängigkeiten zu anderen Baustellen
- **Tisch**: Lichtrahmen mit vier Stützen außen an den Seitenholmen oben und Mitte (y 600..640 und 920..960).
- **Elektronik**: Raspberry Pi für die Kameras, Netzwerk zum Laptop.
- **Stromversorgung**: LED-Panel und Treiber, Versorgung der Testplatinen (strombegrenzt).
