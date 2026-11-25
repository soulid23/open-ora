# Status: arm1-halter

## Ziel
Ein Arm, der eine Platine oder ein anderes Objekt (max. 1 kg, im Mittel 0,5 kg) in die Präsentationszone bringt,
kippt und wendet und dort ruhig hält, während Prober und Kameras arbeiten.

## Aktueller Stand (2026-11-22)
- Montage: hinten rechts auf dem Aluframe (Vorgabe), J1 bei x = 920, y = 920, Fuß über Pfosten_RH.
- Konzept vorgeschlagen: SCARA mit Hubsäule, 3-Achs-Handgelenk mit Schneckentrieben, Wechselträger mit 3-Kugel-Kupplung.
- Überschlagsrechnung: `cad/analysis/arm_holder_sizing.py` (Ergebnisse in ADR 0007).
- FreeCAD-Konzeptmodell mit Platzhaltern und inverser Kinematik: `cad/macros/arm_holder.py`. Es zeichnet den Tisch v8 mit
  (ohne BOM-Export). Drei Posen sind ohne Kollision mit dem Tisch.
- Bilder: `docs/images/arm1_konzept_v1.png`, `docs/images/arm1_arbeitsraum.png`.

## Stand 2026-11-24
- Makro `cad/macros/arm_holder.py` v2: baut auf Tisch V1 (`OpenORA_Frame22.FCStd`) auf.
- J1-Fuß als **abnehmbares Modul von außen** an X_oben_hinten, Y_oben_rechts und Pfosten_RH (`MOUNT = "aussen"`):
  2 Wangen 10 mm, Deckplatte 12 mm über der Matte, 7 × M8 mit Nutensteinen, Lagergehäuse Ø 120 mm.
  Kein Eckausschnitt in Platte und Matte mehr nötig. Keine Kollision mit Tisch V1. Stückliste `bom/arm1_fuss_bom.csv`.
- Bilder: `docs/images/arm1_konzept_v2.png`, `arm1_fuss_v2.png`, `arm1_fuss_v2_innen.png`.
- Konflikt: rechte hintere Stütze des Lichtrahmens sitzt an der Stelle der rechten Wange (klären).

## Entscheidungen (Verweise auf docs/decisions/)
- `0007-arm1-halter-konzept.md` (vorgeschlagen)

## Offene Fragen
- Bewegungsumfang und Antriebsart bestätigen (in ADR 0007 nur angenommen).
- Höhe des Kameraportals gegen die Säulenhöhe (ca. 400 mm über der Matte).
- Aufteilung der Präsentationszone mit Arm 2 (Prober).

## Nächste Schritte
1. Annahmen bestätigen, ADR 0007 auf "angenommen" setzen.
2. Selbstkollision und Achsgrenzen ins Makro einbauen.
3. Handgelenk J5/J6 konstruieren (Schnecken auswählen, nachstellbarer Achsabstand), Druckteile für den Qidi Max4.
4. Platinenrahmen (Träger A) mit Randbacken, Stützstiften und Kupplung konstruieren.
5. J1-Lagergehäuse konstruieren (Lagerwahl, Riemenstufe); Anschluss an den Rahmen ist als Außenmodul modelliert (v2).
6. BOM für Arm 1 aus dem Makro erzeugen.

## Abhängigkeiten zu anderen Baustellen
- **Tisch**: Fuß als Außenmodul an der Ecke hinten rechts, kein Eckausschnitt mehr (bei `MOUNT = "aussen"`).
  Masse ca. 6,5 kg + 1 kg Nutzlast (Annahme in `frame_stiffness.py`: 6 kg). Platte bleibt Scheibe, Ausschnitt prüfen.
- **Sensorik/KI**: Kameraportal-Höhe, Marker am Träger zur Lageerkennung.
- **Elektronik/Stromversorgung**: 6 Schrittmotortreiber, 6 Absolutgeber, Endschalter, Not-Aus auf der Motorspannung.
- **Arm 2 (Prober)**: Montageort (gespiegelt hinten links bei x = 80?), Arbeitsraum und Reihenfolge in der Präsentationszone.
- **Sicherheit**: Not-Aus, Geschwindigkeitsbegrenzung, Quetschstellen.
