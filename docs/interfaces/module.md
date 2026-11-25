# Modul-Schnittstelle des Tisches

Status: **Entwurf** (2026-11-25), Grundsätze angenommen in ADR 0009. Grundsatz aus ADR 0008: Der Tisch ist das **Grundgerüst**, auf dem alles Weitere
aufbaut. Anwendungen kommen als Module dazu, **ohne den Grundrahmen zu ändern**. Wird ein Modul nur mit einer Änderung
am Rahmen möglich, ist diese Schnittstelle unvollständig und wird ergänzt.

Ziel dieser Datei: alle geplanten Anwendungen sammeln, daraus die ungünstigsten Lasten ableiten (offene Frage 8),
die Befestigungszonen festlegen und den Platz am Rahmen verteilen, bevor zwei Module dieselbe Stelle wollen
(Beispiel: Ecke hinten rechts, offene Frage 5). Sobald die Werte belegt sind, wird daraus eine ADR.

Koordinaten wie `frame_4040.py`: X 0..1000 (links nach rechts, Blick von vorn), Y 0 vorn (Sitzplatz) bis 1000 hinten,
Z ab Boden. Maße nach Tisch V1 (`OpenORA_Frame22.FCStd`).

## 1. Anwendungsliste

Werte mit „?“ sind noch zu ermitteln. Masse ohne Tisch, Wechsellast = dynamische Kraft im Betrieb.

| Nr. | Anwendung | Zone | Masse | Wechsel-/Stoßlast | Wärme | Strom | Daten | Version | Stand |
|---|---|---|---|---|---|---|---|---|---|
| A1 | Reparatur-Assistent: Licht- und Sensorrahmen, Kameras, Wärmebild | Z2, Z3 | ca. 15 kg ? | gering | LED-Panel ca. 40 W | 230 V / Kleinspannung | Kameras, Netzwerk | 1 | konstruiert (`light_frame.py` v2) |
| A2 | 3D-Drucker auf der Platte, Auslegung **QIDI Max4** (558 × 578 × 612 mm) | Z1 | 40 kg (Combo mit QIDI Box 46,5 kg) | **hoch**: Druckkopf bis 30 000 mm/s², Kopfmasse ? | Bett ≤ 120 °C, beheizter Bauraum | 230 V | Netzwerk | 1 | Vorgabe (ADR 0009) |
| A3 | Trockner und Filament-Lager auf 1 bis 2 Regalböden | Z5, Z7 | ? | keine | **ja**, Dauerbetrieb | 230 V | optional Feuchte-Sensor | 1 | Vorgabe (ADR 0009) |
| A4 | Werkzeugschubladen als 19"-Rack-Schubladen im Unterbau | Z5 | ? inkl. Inhalt | Auszugskräfte, Kippen | keine | keine | keine | 1 | Vorgabe (ADR 0009), Lage offen |
| A5 | Werkbank (Schraubstock, Montage) | Z1 | ? | **Stoßlast** (Hammer), hohe Einzellast | keine | optional | keine | 1 | Idee |
| A6 | Labor- und Messgeräte (Oszilloskop, Netzgerät, Lötstation) | Z1 | ? | gering | Lötstation, Heißluft | 230 V | USB, Netzwerk | 1 | Idee |
| A7 | Lampen, Lupenleuchten (mit Ausleger = schweres Modul) | Z2, Z4, Z8 | gering | Hebel am Profil | gering | Kleinspannung | keine | 1 | Idee |
| A8 | Sensoren (Kamera, Wärmebild, ToF, Umgebung) | Z2, A1 | gering | keine | keine | Kleinspannung | USB, Netzwerk | 1 | Teil von A1 |
| A9 | Roboterarme (Halter, Prober), schweres Modul, vorab geplant | Z4, Z8 | ca. 6,5 kg je Arm + 1 kg Nutzlast | Kippmoment ca. 26 Nm, Beschleunigung | Motoren | Motorspannung | Steuerbus | **2** | Arm 1 konzipiert (ADR 0007) |
| A10 | **Tischverbund**: mehrere Tische physisch, elektrisch und datentechnisch verbinden | Z4, Z6 | – | Kräfte zwischen den Tischen | – | Weiterleitung | Ethernet, RS485 oder CAN | 1 oder 2 | Grundsatz (ADR 0009), siehe Abschnitt 4 |
| A11 | **Wechselplatte**: Siebdruck oder ESD-ableitfähig, auf den Aluframe aufgelegt und verriegelt | Z1 | ? | trägt alle Lasten von Z1 | – | – | – | 1 | Grundsatz (ADR 0009), siehe Abschnitt 5 |

Auslegungsfälle (vorläufig): **Masse** durch A2 (Max4, 40 bis 46,5 kg auf vier Füßen) oder A5 oben plus A3/A4 unten,
**Schwingung** durch A2, **Stoß** durch A5, **Wärme** durch A2, A3 und A6, **Kippen** durch A9 und durch ausgezogene
Schubladen von A4.

**Modulklassen (ADR 0009):** *leicht* = jederzeit an den Außennuten der Holme (Z2, Z3). *schwer* = vor dem Aufbau geplant,
an den Pfosten (Z4) oder an vorher angebrachten Zusatzprofilen/Konsolen (Z8); zum Nachrüsten wird der Tisch aus dem Verbund genommen.

## 2. Zonen am Grundgerüst

| Zone | Wo | Lage (Tisch V1) | Befestigung | Für |
|---|---|---|---|---|
| Z1 | Arbeitsfläche oben | Wechselplatte (A11) auf dem oberen Rahmen, z 720..740 | Auflegen und verriegeln; Geräte auflegen, klemmen oder in Gewindeeinsätze der Platte (offen) | A2, A5, A6 |
| Z2 | Außennuten obere Holme | X_oben_hinten (y 960..1000), Y_oben_links/rechts (x 0..40 / 960..1000), z 680..720 | Nutensteine M8, Nut 8 | A1, A7, A8, A9 |
| Z3 | Außennuten untere Seitenholme | Y_unten_links/rechts, z 505,6..545,6 | Nutensteine M8 | A1 (2. Verbinder), Fach-Module |
| Z4 | Außennuten der Pfosten | 4 Pfosten, z 50..680 | Nutensteine M8 | A9 (Laschen), A10 (Tischverbund), A7 |
| Z5 | Unterbau vorn | Knieraum, ca. 920 breit, 600 tief, 680 hoch | Unterbau-Modul an Pfosten/Holmen: **Knieraum frei**, **1 bis 2 Regalböden** oder **19"-Rack-Modul mit Schubladen** | A3, A4 |
| Z6 | Rack hinten 19", 3 HE | zwischen den hinteren Rack-Schienen | 19"-Einschübe, D-Ausschnitte | Strom, Netzwerk, Daten, A10 |
| Z7 | Bodenstreben | z 100..140, hinten und seitlich | Nutensteine | Regalboden unten, schwere Lasten tief unten |
| Z8 | Zusatzprofile/Konsolen für schwere Module | an Pfosten und Bodenstreben, vor dem Aufbau montiert | M8, Verbinder 4040 | A7 mit Ausleger, A9, Lichtrahmen |

Belegt durch den Grundrahmen selbst: die **inneren Nuten zwischen den Holmen an Seiten und Rückseite** (Forex-Platten
in der 8-mm-Nut, ADR 0006), der **Erdungspunkt** hinten links (x -3..0, y 974..986, z 607..619), die Plattenverschraubung.

## 3. Belegungsplan

Jede Stelle am Rahmen, an der ein Modul sitzt oder sitzen soll. „reserviert“ = für eine spätere Version freigehalten.

| Stelle | Bereich | Modul | Version | Stand |
|---|---|---|---|---|
| Y_oben_links/rechts außen, y 600..640 | Z2 | Lichtrahmen, Mittelstützen (je 2 Verbinder oben/unten) | 1 | vorgeschlagen |
| Y_unten_links/rechts außen, y 600..640 | Z3 | Lichtrahmen, Mittelstützen | 1 | vorgeschlagen |
| Y_oben_links außen, y 920..960 | Z2 | Lichtrahmen, Stütze hinten links | 1 | vorgeschlagen |
| Y_unten_links außen, y 920..960 | Z3 | Lichtrahmen, Stütze hinten links | 1 | vorgeschlagen |
| Y_oben_rechts außen, y 920..960 | Z2 | Lichtrahmen, Stütze hinten rechts | 1 | **Konflikt** mit Arm 1 (offene Frage 5) |
| Y_unten_rechts außen, y 920..960 | Z3 | Lichtrahmen, Stütze hinten rechts | 1 | **Konflikt** mit Arm 1 (offene Frage 5) |
| Y_oben_rechts außen, y 830..1000 | Z2 | Arm 1, rechte Wange (2 x M8 bei y 850, 885) | 2 | reserviert, Konflikt |
| X_oben_hinten außen, x 830..1000 | Z2 | Arm 1, hintere Wange (3 x M8 bei x 850, 885, 985) | 2 | reserviert |
| Pfosten hinten rechts, beide Außennuten, z 600..680 | Z4 | Arm 1, Laschen | 2 | reserviert |
| X_oben_hinten außen, x 0..170 (gespiegelt) | Z2 | Arm 2 (Prober), falls gespiegelt hinten links | 2 | offen (offene Frage 2) |
| Rack hinten, HE 1 | Z6 | Auszugschublade 87556 | 1 | vorgeschlagen (ADR 0003) |
| Rack hinten, HE 2 | Z6 | frei (z. B. Netzwerk-Switch, Tischverbund) | 1 | frei |
| Rack hinten, HE 3 | Z6 | Blende 872215: powerCON IN/OUT, etherCON, 9 freie D-Ausschnitte | 1 | vorgeschlagen (ADR 0003) |
| Pfosten außen (alle 4) | Z4 | Tischverbund-Verbinder | 1 oder 2 | offen, siehe Abschnitt 4 |
| Oberer Rahmen, Mitte | Z1 | Mittelträger der Wechselplatte (abnehmbar) | 1 | offen (offene Frage 12) |
| Raum über der Platte unter der Sensorschiene | Z1 | Drucker Max4 (Oberkante z 1352) gegen Kameras (Unterkante ca. z 1358): nur ca. 6 mm | 1 | Hinweis: Drucker nicht unter der Sensorschiene |

## 4. Tischverbund (A10)

Mehrere Tische sollen sich verbinden lassen: physisch, elektrisch und über gemeinsame Datenleitungen. Die Verbindung
läuft über das Rack (Z6) und die Pfosten (Z4).

### Physisch
- Verbinder zwischen benachbarten Pfosten (z. B. Verbindungsplatten mit Nutensteinen in den Außennuten); gleiche Höhe
  über die Stellfüße (±15 mm Verstellweg, ADR 0006).
- **Konflikt seitlich**: Die Stützen des Lichtrahmens sitzen außen an den Seiten (x -40..0 und 1000..1040). Zwei Tische
  mit Lichtrahmen nebeneinander hätten 80 mm Spalt oder kollidieren. Mögliche Wege: Verbund nur Rücken an Rücken,
  gemeinsame Stütze für zwei Tische, oder die Stütze selbst als Verbindungsstück (offene Frage 11).
- Ein Verbund ist steifer als ein einzelner Tisch; die Rechnung (`frame_stiffness.py`) gilt bisher nur für einen Tisch.

### Elektrisch
- Vorhanden: powerCON IN (blau) und OUT (weiß) in der hinteren Blende (ADR 0003): Durchschleifen von Tisch zu Tisch.
- Zu klären durch die Elektrofachkraft: Gesamtstrom der Kette (begrenzt durch die erste Steckdose und deren Absicherung),
  Absicherung und Fehlerstromschutz je Tisch, durchgehender Schutzleiter, ESD-Erdung der Tische auf gleichem Potenzial,
  Bemessungsdaten der Steckverbinder. Netzseite nur durch Elektrofachkraft (`SAFETY.md`).

### Daten
- Netzwerk: etherCON-Durchführung vorhanden; je Tisch ein kleiner Switch (Rack HE 2) oder durchgeschleift.
- Verbund-Bus: **RS485 oder CAN** (ADR 0009; RS232 wäre nur Punkt-zu-Punkt). Auswahl, Steckverbinder, Terminierung
  am Kettenende und Adressierung der Tische offen.
- Steckverbinder in den freien D-Ausschnitten der hinteren Blende (Neutrik D-Format, nur Kleinspannung).

## 5. Wechselplatte (A11)
- Varianten: **Siebdruck 18 mm** (Werkbank, Drucker, Lager) und **ESD-ableitfähig** (Elektronik). Weitere möglich.
- Wird auf den oberen Rahmen aufgelegt und **verriegelt** (schnell lösbar, mehrere Punkte), weil die Platte als Scheibe
  zur Quersteifigkeit beiträgt (ADR 0006, ADR 0009).
- **Mittelträger**: Tisch V1 hat keinen mittleren Querträger; für Drucker und Werkbank ist ein Mittelträger nötig,
  am besten abnehmbar als Teil des Plattenmoduls (grobe Durchbiegung ohne Mittelträger ca. 9 mm bei 500 N, ADR 0009).
- **ESD-Platte**: Erdungsanschluss am Tisch (Druckknopf o. Ä.), über 1 MΩ an PE; Ableitwiderstand nach jedem Wechsel prüfen.
- Kanten, Überstand und Auflage so, dass Lichtrahmen-Stützen und Arm-Module außen frei bleiben.

## 6. Woran wir „modular genug“ messen
- Ein neues Modul passt **ohne Änderung am Grundrahmen** und ohne Bohren.
- Es belegt nur Stellen, die im Belegungsplan frei oder für es reserviert sind.
- Die Lasten aller gleichzeitig möglichen Module liegen **mit Reserve** innerhalb der Nachweise (ADR 0008, `docs/normen.md`).
- Montage und Demontage mit Standardwerkzeug, Kabel und Erdung über die festgelegten Wege.

## 7. Vorgehen
1. Anwendungsliste vervollständigen: Masse, Wechsellast, Wärme je Anwendung (Herstellerangaben, Messung).
2. Zonen und Belegungsplan bestätigen, Konflikte lösen (offene Fragen 5 und 11).
3. Im CAD prüfen: jedes Modul als eigenes Makro, das nur an den Zonen anschraubt (Muster: `light_frame.py`,
   `arm_holder.py`); grobe Platzhalter für Drucker, Fach-Modul und Nachbartisch; Kollisionsprüfung.
4. Lastfälle je Modul in `frame_stiffness.py` ergänzen (Masse, Eigenfrequenz gegen Anregung durch den Drucker, Kippen).
5. Am gebauten Tisch messen (M3): Schwingung mit Drucker, Kippen mit ausgezogener Schublade.
6. Daraus eine ADR „Modul-Schnittstelle“ machen.
