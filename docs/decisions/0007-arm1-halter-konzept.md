# 0007: Arm 1 (Halter), Konzept

Status: **vorgeschlagen** (Annahmen unten bestätigen oder ändern, dann "angenommen").
Ergänzt `0001-architektur.md` (Halter = Nutzlast, Prober = Präzision) und `0006-tisch-1x1-verstrebung.md`.

## Aufgabe
Der Halter nimmt ein Objekt (Platine oder anderes Teil) auf, bringt es in die Präsentationszone vor dem Sitzplatz,
kippt und wendet es und **hält es dort ruhig**, während Prober und Kameras arbeiten.

- Nutzlast: **max. 1 kg, im Mittel 0,5 kg** (Vorgabe).
- Tastkraft des Probers: bis 2 N angenommen (Federkontakte 1 bis 2 N).

## Annahmen (nicht bestätigt, bitte prüfen)
- Bewegung: Positionieren, Kippen (bis ±90°) und Wenden (180°). Dafür sind 6 Achsen nötig.
- Antriebe: Schrittmotoren mit Absolutgebern am Abtrieb, ESP32.

## Montage (Vorgabe 2026-11-22)
**Hinten rechts, direkt auf dem Aluframe.** J1-Achse bei x = 920, y = 920. Das J1-Gehäuse (170 × 170 mm) steht auf der
Rahmenecke aus X_oben_hinten und Y_oben_rechts, mit Nutensteinen in den oberen Nuten, und liegt genau über Pfosten_RH.
Kippmoment und Gewicht gehen damit direkt in Rahmen und Bein, nicht in die Siebdruckplatte. Platte und ESD-Matte
bekommen dort einen Eckausschnitt von 170 × 170 mm. Der J1-Motor hängt unter dem Gehäuse geschützt in der Rahmenecke.
Ein Zusatzträger unter der Platte ist nicht nötig. Der Prober kommt gespiegelt nach hinten links (offen, Baustelle Arm 2).

## Vorschlag
**SCARA mit Hubsäule und 3-Achs-Handgelenk.** Alle Antriebe, die Schwerkraft tragen, sind selbsthemmend.

| Achse | Funktion | Antrieb | Begründung |
|---|---|---|---|
| J1 | Drehung Säule (senkrecht) | **NEMA17 60 mm**, GT2-Riemen 2-stufig 1:20 | keine Schwerkraftlast, Riemen ohne Spiel |
| Z | Hub 200 mm | NEMA17, TR8x2, 2 × MGN12 | selbsthemmend: sackt bei Stromausfall nicht ab |
| J2 | Ellbogen (senkrecht) | NEMA17 an der Säule, Riemen 1:12 | Motor sitzt innen, Unterarm bleibt leicht |
| J4 | Gieren | NEMA17 kurz, Schnecke 1:30 | selbsthemmend |
| J5 | Nicken (Kippen) | **NEMA17 60 mm**, Schnecke 1:30 | höchstes Lastmoment, selbsthemmend |
| J6 | Rollen (Wenden) | NEMA14, Schnecke 1:20 | selbsthemmend |

- Glieder: Ober- und Unterarm je **300 mm** Achsabstand (von der Ecke aus ist der Weg zur Tischmitte länger), Alux 2040 hochkant. Säule 4080, ca. 400 mm über der Matte.
- **Wechselträger statt Greiferbacken**: Der Arm greift das Objekt nicht direkt. Er kuppelt einen Träger an, über eine
  3-Kugel/3-Nut-Kupplung (wiederholgenau, steif). Die Verriegelung ist eine selbsthemmende Spindel, kein Magnet.
  So hält der Arm den Träger auch ohne Strom fest. Träger A ist ein **Platinenrahmen** mit verstellbaren Randbacken und
  **Stützstiften im Raster ≤ 80 mm**. Für andere Objekte gibt es weitere Träger mit derselben Kupplung.
- Befestigung: siehe Montage. Kippmoment am Fuß ca. 26 Nm.

## Ergebnis der Überschlagsrechnung (`cad/analysis/arm_holder_sizing.py`)
- Masse Arm ohne Nutzlast ca. 6,5 kg. Das liegt knapp über der Annahme von 6 kg je Arm in `frame_stiffness.py`.
- J5: Lastmoment 2,7 Nm. Mit Sicherheitsfaktor 2 und Schneckenwirkungsgrad 0,4 hat der Antrieb 1,4-fache Reserve.
- Z: TR8x2 ist selbsthemmend (Steigungswinkel 5,2°, Reibungswinkel ca. 11,7°). Antriebsmoment 0,05 Nm.
- J1: ausgestreckt 1,7 kgm². Für 60°/s mit 0,6 s Rampe braucht der Motor ca. 0,33 Nm. Deshalb ein NEMA17 60 mm
  (nutzbar ca. 0,39 Nm). Der Halter muss nicht schnell sein.
- **Steifigkeit bei 2 N**: Die Glieder biegen sich ca. 0,03 mm. J1 gibt bei waagerechter Kraft ca. 0,15 mm nach
  (Haltesteifigkeit des Schrittmotors). Senkrechte Tastkraft geht in die Lager und wirkt in dieselbe Richtung wie die
  Schwerkraft, das Lagerspiel kippt also nicht um.
- **Die Platine ist das weichste Glied**: 1,6 mm FR4 biegt sich bei 2 N über 300 mm Stützweite ca. 1,7 mm durch,
  über 80 mm nur ca. 0,03 mm. Deshalb braucht der Träger Stützstifte.
- Arbeitsraum: Präsentationspunkt P0 (500, 450), Zone ±100 mm. In P0 steht das Handgelenk bei 70 % der Armreichweite
  (600 mm), in der fernen Zonenecke (400, 350) bei 94 %, das ist die Grenze. Platinenoberseite 30 bis 230 mm über der Matte.
- FreeCAD (`cad/macros/arm_holder.py`): vier Posen ohne Kollision mit dem Tisch (P0 waagerecht mit beiden Ellbogenseiten,
  Ecke (400, 350) 45° gekippt, Ecke (600, 550) gewendet). Selbstkollisionen des Arms prüft das Makro noch nicht.

## Sicherheit (siehe SAFETY.md)
- Not-Aus schaltet die Motorspannung in Hardware ab. Weil Z, J4, J5 und J6 selbsthemmend sind, fällt dabei nichts herunter.
- Endschalter in Hardware an Z (oben/unten) und am J1-Anschlag (Kabelführung). Motorstrom auf das nötige Maß begrenzen.
- Der Arm arbeitet direkt vor einer sitzenden Person. Deshalb Geschwindigkeit begrenzen (60°/s, Z 20 mm/s) und Quetschstellen
  zwischen Säule, Oberarm und Platte abdecken.

## Alternativen (verworfen oder später)
- **Knickarm mit 6 Achsen**: Schulter und Ellbogen tragen die ganze Schwerkraftlast. Das braucht große Getriebe, und
  das Spiel wechselt beim Kippen die Seite. Weniger steif bei gleichem Aufwand.
- **Smart-Servos**: wenig Haltemoment, sie halten nicht ohne Strom, und der Lagerregler zittert. Für einen Halter ungeeignet.
- **Gedrucktes Zykloidgetriebe an J5**: Es hat 0,1 bis 0,3° Spiel, das sind am Träger 0,4 bis 1 mm. Die Schnecke lässt sich
  nachstellen und hält selbst.
- **Andockstation** (später, falls Messungen es verlangen): Der Arm setzt den Träger auf eine kinematische Aufnahme auf der
  Platte. Das ist am steifsten, aber dann ist nur waagerecht möglich.

## Offene Punkte
- Bewegungsumfang und Antriebsart bestätigen (Annahmen oben). Montageort ist vorgegeben.
- Höhe und Lage des Kameraportals: Die Säule ragt ca. 400 mm über die Matte.
- Eckausschnitt in Platte und Matte: Die Platte ist eine tragende Scheibe (0006). Den Ausschnitt in der Steifigkeitsrechnung prüfen.
- Prober-Bauart und Lage: Wird der Prober gespiegelt nach hinten links gesetzt? Wer arbeitet wann in der Präsentationszone (Kollisionen)?
- Schnecken: Zukauf (Stahl/Messing, Modul 0,5 bis 1) oder gedruckt, Achsabstand nachstellbar.
- Lager J1 (Lagerpaar ≥ 80 mm Abstand oder Vierpunktlager), J2 und J4 auswählen.
- Kupplung und Verriegelung des Trägers konstruieren, Stromübertragung zum Träger (falls nötig).
- Selbstkollisionen im Makro prüfen.
- Steifigkeit nach dem Aufbau messen und die Rechnung anpassen.
