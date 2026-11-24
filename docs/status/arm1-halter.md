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
5. J1-Gehäuse mit Lagerung und Anschluss an die Rahmenecke (Nutensteine in X_oben_hinten und Y_oben_rechts).
6. BOM für Arm 1 aus dem Makro erzeugen.

## Abhängigkeiten zu anderen Baustellen
- **Tisch**: Eckausschnitt 170 × 170 mm hinten rechts in Platte und ESD-Matte, Fuß auf der Rahmenecke.
  Masse ca. 6,5 kg + 1 kg Nutzlast (Annahme in `frame_stiffness.py`: 6 kg). Platte bleibt Scheibe, Ausschnitt prüfen.
- **Sensorik/KI**: Kameraportal-Höhe, Marker am Träger zur Lageerkennung.
- **Elektronik/Stromversorgung**: 6 Schrittmotortreiber, 6 Absolutgeber, Endschalter, Not-Aus auf der Motorspannung.
- **Arm 2 (Prober)**: Montageort (gespiegelt hinten links bei x = 80?), Arbeitsraum und Reihenfolge in der Präsentationszone.
- **Sicherheit**: Not-Aus, Geschwindigkeitsbegrenzung, Quetschstellen.
