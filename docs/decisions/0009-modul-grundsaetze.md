# 0009: Grundsätze der Modul-Schnittstelle

Status: angenommen (Grundsätze, 2026-11-25). Werte und Bauteile sind noch festzulegen (`docs/interfaces/module.md`).
Ergänzt `0008` (Tisch als modulare Plattform) und `0006` (Tisch).

## Kontext
Der Tisch ist das Grundgerüst, auf dem alles Weitere aufbaut (Reparatur-Assistent, 3D-Drucker, Werkbank, Labor,
Lager, Arme, Lampen, Sensoren). Mehrere Tische sollen sich zu einem Verbund zusammenschließen lassen.

## Entscheidung

1. **Auslegungsfall Drucker: QIDI Max4.** Größter vorgesehener Drucker auf der Platte. Herstellerangaben:
   Druckerabmessungen 558 × 578 × 612 mm, Nettogewicht 40 kg (Max4 Combo mit QIDI Box 46,5 kg),
   Beschleunigung des Druckkopfs bis 30 000 mm/s².
2. **Unterbau als Modul**, je nach Zweck:
   - Knieraum frei (Sitzplatz, Standard für den Reparaturplatz),
   - ein oder zwei Regalböden für Trockner und Filament-Lager,
   - Werkzeugschubladen als **19"-Rack-Schubladen**.
3. **Zwei Klassen von Modulen:**
   - **leicht** (Sensoren, kleine Halter, Kabelführung): jederzeit an den Außennuten der Holme.
   - **schwer** (Lampen mit Ausleger, Roboterarme, Lichtrahmen): **vor dem Aufbau geplant**, an den Beinen (Pfosten)
     oder an zusätzlichen Metallprofilen/Konsolen, die vorher angebracht werden. Muss nachgerüstet werden, wird der
     Tisch dafür aus dem Verbund genommen.
4. **Tischverbund** über Rack (hinten) und Pfosten: physisch verbunden, Strom durchgeschleift, gemeinsame Datenleitungen.
   Datenbus: **RS485 oder CAN** (Auswahl offen), dazu Ethernet.
5. **Tischplatte als Modul**, auf den Aluframe aufgelegt, je nach Anwendung:
   - Siebdruckplatte (Werkbank, Drucker, Lager),
   - elektrostatisch ableitfähige Platte (Elektronik) mit **Erdungsanschluss am Tisch**.

## Folgen
- **Steifigkeit**: Laut ADR 0006 ist die fest verschraubte Platte als Scheibe tragend (quer ca. 490 N/mm mit Scheibe,
  ca. 31 N/mm nur Rahmen, vor den Eckstreben gerechnet). Eine nur aufgelegte Platte fällt als Scheibe weg. Die Wechselplatten
  brauchen daher eine **schnell lösbare, aber feste Verriegelung** am Rahmen (mehrere Punkte), oder der Rahmen muss
  ohne Platte steif genug sein (Eckstreben, ggf. zusätzliche Aussteifung). Beides ist zu rechnen und am Tisch zu messen.
- **Durchbiegung**: Laut Prüfung vom 25.11. hat Tisch V1 (Frame22) keinen mittleren Querträger mehr. ADR 0006 nennt für
  eine 12-mm-Platte über 920 mm ca. 31 mm und für 18 mm mit Mittelträger ca. 1,4 mm (500 N in Feldmitte, Streifenmodell).
  Ohne Mittelträger ergibt dieselbe Rechnung für 18 mm grob ca. 9 mm. Mit Drucker (40 kg) oder Werkbank ist ein
  **Mittelträger oder eine steifere Platte nötig**, am besten als Teil des Plattenmoduls (abnehmbarer Mittelträger).
- **ESD-Platte**: Erdungsanschluss am Tisch (z. B. Druckknopf), über 1 MΩ an PE wie die ESD-Matte (`SAFETY.md`,
  DIN EN IEC 61340-5-1). Bei jedem Plattenwechsel Ableitung prüfen.
- **Drucker und Lichtrahmen**: Druckeroberkante 740 + 612 = 1352 mm, Unterkante der Kameras ca. z 1358 (light_frame.py v2):
  nur ca. 6 mm Abstand. Drucker und Lichtrahmen auf demselben Tisch nur außerhalb der Sensorschiene oder mit höherem Portal.
- **Rack-Schubladen im Unterbau** greifen das Rack-Schienen-Prinzip aus ADR 0002 wieder auf (2020-Schienen, 19"),
  jetzt als einsetzbares Modul. Vorn schließt das den Sitzplatz aus; Lage (vorn, seitlich) offen.
- Schwere Module hängen an Pfosten oder Zusatzprofilen: Lasten gehen über die Beine in den Boden, nicht über die Holme.

## Offen
- Verriegelung der Wechselplatten, Mittelträger, Plattenstärke (offene Frage 12).
- Lage und Höhe des Unterbau-Rack-Moduls, Kippen bei ausgezogenen Schubladen (offene Frage 13).
- Auswahl RS485 oder CAN, Steckverbinder, Terminierung.
- Masse des Druckkopfs Max4 für die Wechsellast (nicht angegeben).
