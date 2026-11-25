# Modul-Schnittstelle des Tisches

Status: **Entwurf** (2026-11-25). Grundsatz aus ADR 0008: Der Tisch ist das **Grundgerüst**, auf dem alles Weitere
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
| A2 | 3D-Drucker auf der Platte | Z1 | ? (größter Drucker als Auslegung) | **hoch**: bewegter Kopf/Bett, Schwingung | Bett, Hotend | 230 V | Netzwerk | 1 | Idee |
| A3 | Trockeneinheiten für Filament | Z5 | ? | keine | **ja**, Dauerbetrieb | 230 V | optional Feuchte-Sensor | 1 | Idee |
| A4 | Schubladen, Schrank, Fachboden im Unterbau | Z5, Z7 | ? inkl. Inhalt | Auszugskräfte | keine | keine | keine | 1 | Idee |
| A5 | Werkbank (Schraubstock, Montage) | Z1 | ? | **Stoßlast** (Hammer), hohe Einzellast | keine | optional | keine | 1 | Idee |
| A6 | Labor- und Messgeräte (Oszilloskop, Netzgerät, Lötstation) | Z1 | ? | gering | Lötstation, Heißluft | 230 V | USB, Netzwerk | 1 | Idee |
| A7 | Lampen, Lupenleuchten, Halter an der Nut | Z2, Z4 | gering | Hebel am Profil | gering | Kleinspannung | keine | 1 | Idee |
| A8 | Sensoren (Kamera, Wärmebild, ToF, Umgebung) | Z2, A1 | gering | keine | keine | Kleinspannung | USB, Netzwerk | 1 | Teil von A1 |
| A9 | Roboterarme (Halter, Prober) als Außenmodule | Z2, Z4 | ca. 6,5 kg je Arm + 1 kg Nutzlast | Kippmoment ca. 26 Nm, Beschleunigung | Motoren | Motorspannung | Steuerbus | **2** | Arm 1 konzipiert (ADR 0007) |
| A10 | **Tischverbund**: mehrere Tische physisch, elektrisch und datentechnisch verbinden | Z4, Z6 | – | Kräfte zwischen den Tischen | – | Weiterleitung | Netzwerk, seriell | 1 oder 2 | Idee, siehe Abschnitt 4 |

Auslegungsfälle (vorläufig): **Masse** durch A2 oder A5 oben plus A3/A4 unten, **Schwingung** durch A2,
**Stoß** durch A5, **Wärme** durch A3 und A6, **Kippen** durch A9 und durch Auszugskräfte von A4.

## 2. Zonen am Grundgerüst

| Zone | Wo | Lage (Tisch V1) | Befestigung | Für |
|---|---|---|---|---|
| Z1 | Arbeitsfläche oben | Platte z 720..738, Matte bis z 740, x/y 10..990 | Auflegen, Klemmen, Gewindeeinsätze in der Platte (offen) | A2, A5, A6 |
| Z2 | Außennuten obere Holme | X_oben_hinten (y 960..1000), Y_oben_links/rechts (x 0..40 / 960..1000), z 680..720 | Nutensteine M8, Nut 8 | A1, A7, A8, A9 |
| Z3 | Außennuten untere Seitenholme | Y_unten_links/rechts, z 505,6..545,6 | Nutensteine M8 | A1 (2. Verbinder), Fach-Module |
| Z4 | Außennuten der Pfosten | 4 Pfosten, z 50..680 | Nutensteine M8 | A9 (Laschen), A10 (Tischverbund), A7 |
| Z5 | Unterbau vorn | Knieraum, ca. 920 breit, 600 tief, 680 hoch | Einschub-Modul an Pfosten/Holmen; Knieraum **oder** Fach | A3, A4 |
| Z6 | Rack hinten 19", 3 HE | zwischen den hinteren Rack-Schienen | 19"-Einschübe, D-Ausschnitte | Strom, Netzwerk, Daten, A10 |
| Z7 | Bodenstreben | z 100..140, hinten und seitlich | Nutensteine | Fachboden, schwere Lasten tief unten |

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
- Serielle Schnittstelle (RS232 oder ähnlich): RS232 ist Punkt-zu-Punkt und auf kurze Längen ausgelegt; für eine Kette
  mehrerer Tische eignen sich busfähige Verfahren wie RS485 oder CAN besser. Auswahl offen.
- Steckverbinder in den freien D-Ausschnitten der hinteren Blende (Neutrik D-Format, nur Kleinspannung).

## 5. Woran wir „modular genug“ messen
- Ein neues Modul passt **ohne Änderung am Grundrahmen** und ohne Bohren.
- Es belegt nur Stellen, die im Belegungsplan frei oder für es reserviert sind.
- Die Lasten aller gleichzeitig möglichen Module liegen **mit Reserve** innerhalb der Nachweise (ADR 0008, `docs/normen.md`).
- Montage und Demontage mit Standardwerkzeug, Kabel und Erdung über die festgelegten Wege.

## 6. Vorgehen
1. Anwendungsliste vervollständigen: Masse, Wechsellast, Wärme je Anwendung (Herstellerangaben, Messung).
2. Zonen und Belegungsplan bestätigen, Konflikte lösen (offene Fragen 5 und 11).
3. Im CAD prüfen: jedes Modul als eigenes Makro, das nur an den Zonen anschraubt (Muster: `light_frame.py`,
   `arm_holder.py`); grobe Platzhalter für Drucker, Fach-Modul und Nachbartisch; Kollisionsprüfung.
4. Lastfälle je Modul in `frame_stiffness.py` ergänzen (Masse, Eigenfrequenz gegen Anregung durch den Drucker, Kippen).
5. Am gebauten Tisch messen (M3): Schwingung mit Drucker, Kippen mit ausgezogener Schublade.
6. Daraus eine ADR „Modul-Schnittstelle“ machen.
