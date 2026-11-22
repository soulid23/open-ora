# 0006: Tisch 1000 x 1000 mm, Schreibtischhöhe, Verstrebung

Status: angenommen. Die Berechnung ist eine Überschlagsrechnung mit Annahmen (siehe unten); sie ersetzt keine Messung am fertigen Tisch.
Ergänzt `0004-rahmenaufbau.md` (dort noch 600 x 500 mm ohne Verstrebung).

## Entscheidung
- Grundfläche **1000 x 1000 mm**, Tischhöhe (Oberkante ESD-Matte) **740 mm**. Die Höhe ist der Parameter `DESK_H` im Makro, die Beinlänge ergibt sich daraus.
- Aufbau von unten: Beine/Pfosten 680 mm lang, Unterkante des unteren Rahmens (Rack-Boden) bei 505,6 mm,
  Rack-Raum 3 HE (134,4 mm lichte Höhe), oberer Rahmen 680 bis 720 mm, Siebdruckplatte **18 mm**, ESD-Matte 2 mm.
- **Platte 18 mm statt 12 mm** und je ein **Mittelträger** oben und unten bei y = 550 mm. Grobe Abschätzung der Durchbiegung
  unter 500 N in Feldmitte (Streifenmodell, E = 6000 N/mm2 angenommen): 12 mm über 920 mm Spannweite ca. 31 mm, 18 mm über das größte Feld
  neben dem Mittelträger ca. 1,4 mm.
- **Verstrebung**: Bodenstreben (4040) hinten und an beiden Seiten bei 100 bis 140 mm Höhe. Je eine **Diagonale aus 2020**
  hinten, links und rechts im Feld zwischen Bodenstrebe und Rack-Boden (Zuschnitt je ca. 900 mm). Die **Vorderseite bleibt frei** (Bedienseite, Beinraum).
- **Platte als Scheibe**: fest mit dem oberen Rahmen verschrauben (mind. 20 Senkkopfschrauben mit Nutenstein, gleichmäßig verteilt). Ohne diese Scheibe ist die offene Vorderseite in Querrichtung (X) weich.
- **Tiefenschienen** (2020) auf den Mittelträgern tragen das hintere Ende der Auszugschublade. Die Einbautiefe beträgt 440 mm
  (Hersteller: 360 bis 480 mm). Vorher lag die Schublade zwischen vorderen und hinteren Schienen, das geht bei 1000 mm Tiefe nicht mehr.

## Ergebnis der Rechnung (`cad/analysis/frame_stiffness.py`)
Kippen: Gesamtmasse ca. 81 kg (angenommen), Schwerpunkt ca. 663 mm hoch. Der Tisch kippt erst bei ca. 515 N (ca. 53 kg) waagerecht an der Tischkante.
Das gilt für Stellfüße direkt unter den Pfosten. Eine nach außen verbreiterte Fußplatte erhöht den Wert.

Seitensteifigkeit (100 N waagerecht am Tischrand, ungünstigste obere Ecke, Winkelverbinder mit mittlerer Drehsteifigkeit 2 kNm/rad, **angenommen**):

| Variante | Verschiebung X | Verschiebung Y | 1. Eigenfrequenz |
|---|---|---|---|
| nur Rahmen und Pfosten | 4,5 mm | 4,5 mm | ca. 3 Hz |
| + Bodenstreben | 3,8 mm | 2,6 mm | ca. 3 Hz |
| + Diagonalen hinten und seitlich | 2,1 mm | 0,04 mm | ca. 4 Hz |
| + Diagonalen, Platte als Scheibe (angenommen) | 0,20 mm | 0,04 mm | ca. 15 Hz |

Aussage: Die Diagonalen und die fest verschraubte Platte sind entscheidend. Die Bodenstreben allein bringen wenig.
Die Werte hängen stark von der Steifigkeit der Winkelverbinder ab (im Skript von weich bis starr durchgerechnet).

## Annahmen und Grenzen der Rechnung
- Drehsteifigkeit der Winkelverbinder (0,5 bis 10 kNm/rad und starr): geschätzt, nicht gemessen.
- Plattenscheibe: Ersatzsteifigkeit 1000 N/mm angenommen (Schraubenschlupf).
- Massen (Platte, Arme, Portal, Rack-Einbauten, Sonstiges): geschätzt, zusammen ca. 81 kg mit Rahmen.
- 2020-Profil: Ersatzquerschnitt aus dem Makro, kein Herstellerwert. Torsionskonstante des 4040 geschätzt. Schubverformung vernachlässigt.
- Nur lineare Statik und die erste Eigenfrequenz, keine Festigkeitsnachweise der Verbinder.

## Offene Punkte
- **Messen**: seitlich mit 100 N belasten und die Verschiebung messen, danach Ausschwingen oder Schwingungsmessung. Dann Rechnung anpassen.
- **Sitzen am Tisch**: Die vordere untere Rahmenebene liegt 505,6 mm über dem Boden und nimmt dort Beinraum. Für Sitzen vorn ist das vermutlich knapp, mit einem Stuhl probieren. Für Stehen oder einen hohen Hocker `DESK_H` erhöhen.
- Anschluss der Diagonalen an die 4040-Profile (Gelenk- oder Gehrungswinkel) ist noch zu wählen.
- Siebdruckplatte 18 mm: tatsächliches Gewicht und E-Modul beim Hersteller prüfen.
- Stellfüße mit verbreiterter Fußplatte auswählen.
