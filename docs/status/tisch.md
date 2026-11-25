# Status: tisch

## Ziel
Ein stabiler, nachbaubarer Arbeitstisch 1000 x 1000 mm in Schreibtischhöhe, an dem man sitzend arbeitet, mit Platz für
zwei Arme, den Licht- und Sensorrahmen und ein 19"-Rack für Netz, Netzwerk und Schublade.

## Aktueller Stand (2026-11-24)
- **Version 1 final**: `cad/frame/OpenORA_Frame22.FCStd` (nicht im Repo), Bild `docs/images/open-oratischV1.png`.
- Makro `cad/macros/frame_4040.py`: 1000 x 1000 mm, Oberkante ESD-Matte 740 mm, Alux 4040, 18-mm-Siebdruckplatte mit
  ESD-Matte, Mittelträger, Eckstreben 45° (`BRACING = "knee"`), Gelenkstellfüße 80 mm, Sitzplatz vorn frei
  (`FRONT_RACK = False`), 19"-Rack 3 HE hinten (Schublade 87556, Blende 872215 mit powerCON IN/OUT und etherCON),
  Rack-Zargen 2020, Forex-Verkleidung 5 mm in der Nut mit Logo (`LOGO_MODE = "druck"`).
- Stücklisten: `bom/frame_bom.csv` (vom Makro), Bestellliste Alux `bom/alux_bestellliste.ods`/`.csv`
  (Preise und Artikelnummern noch auszufüllen).
- Steifigkeit: `cad/analysis/frame_stiffness.py`, Ergebnisse in ADR 0006 (mit Platte als Scheibe ca. 490 N/mm quer,
  f1 ca. 14,6 Hz; Eckstreben, Zargen und Forex noch nicht eingerechnet).

## Entscheidungen (Verweise auf docs/decisions/)
- `0006-tisch-1x1-verstrebung.md` (angenommen, mit Nachträgen bis Version 1)
- `0002`, `0003`, `0004`: Rack, Einbauten, Rahmenprinzip (Maße durch 0006 ersetzt)

## Offene Fragen
- Konflikt Arm-1-Außenmodul mit der hinteren rechten Stütze des Lichtrahmens (offene Frage 5).
- Ort des Prüf-/Tastinterface (offene Frage 6).
- Alux: 2020-Profil mit passender Nut, Einfassprofil 8-12.40 für Forex freigegeben, echte Artikelnummern.
- Echte Maße aus STEP (Verbinder 4040-45, Füße) und aus den Adam-Hall-Zeichnungen.
- Branding mit der Druckerei klären: Druck oder Gravur, sichtbarer Rand in der Nut, Dateiformat.

## Nächste Schritte
1. Bestellliste Alux mit Preisen und Artikelnummern füllen, BOM prüfen, bestellen.
2. Steifigkeit mit Eckstreben, Zargen und Forex neu rechnen.
3. Makro auf den Stand von Frame22 bringen, falls dort von Hand geändert wurde.
4. Rahmen montieren, Platte als Scheibe verschrauben (mind. 20 Senkkopfschrauben), Steifigkeit messen (100 N seitlich).

## Abhängigkeiten zu anderen Baustellen
- **Arm 1 (Halter)**: Fuß als Außenmodul an der Ecke hinten rechts (ADR 0007, Nachtrag), ca. 6,5 kg + 1 kg Nutzlast.
- **Sensorik/KI**: Licht- und Sensorrahmen (`light_frame.py` v2): vier Stützen außen, je 2 Verbinder an Y_oben_* und
  Y_unten_* (y 600..640 und 920..960), kein Bodenkontakt; verdecken Teile des Logo-Drucks auf den Seitenplatten (akzeptiert).
  Lasten des Portals gehen damit in die Seitenholme: bei der Steifigkeitsrechnung berücksichtigen.
- **Stromversorgung**: Netzeingang und Netzteile im Rack hinten, Schutzleiter an Rahmen und ESD-Matte (SAFETY.md).
