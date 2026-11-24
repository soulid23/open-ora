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
- **Sitzseite**: siehe Nachtrag unten. Probesitzen mit Stuhl und Knien unter der Platte, danach `DESK_H` ggf. anpassen.
- Siebdruckplatte 18 mm: tatsächliches Gewicht und E-Modul beim Hersteller prüfen.
- Stellfüße mit verbreiterter Fußplatte auswählen.

## Nachtrag: Sitzseite vorn frei (Y = 0)
Der Tisch wird sitzend benutzt. Deshalb entfallen vorn der untere Querträger, die 19"-Schienen und die vordere D12-Blende (Schalter `FRONT_RACK = False` im Makro). Das Rack mit Netz, Netzwerk und Schublade bleibt hinten.
- Beinraum: 920 mm breit, 600 mm tief ab Tischkante (Mittelträger nach `MID_Y = 620`), 680 mm hoch unter dem oberen Rahmen. Schubladen-Einbautiefe 370 mm (Hersteller 360 bis 480 mm).
- Profil 4040: 13,92 m, ca. 19,4 kg; 24 Verbindungen; Makro ohne Kollisionen.
- Steifigkeit (X = Querrichtung, nur Rahmen, Verbinder 2 kNm/rad): 31 N/mm statt 47 N/mm mit geschlossener Front; f1 ca. 3,6 Hz statt 4,3 Hz. Mit als Scheibe verschraubter Platte bleibt es bei ca. 490 N/mm (0,2 mm bei 100 N), f1 ca. 14,6 Hz. Die Platten-Verschraubung ist damit tragend, nicht optional. Y (Tiefe) unverändert durch die Seitendiagonalen.
- Das Prüf- und Tastinterface, das vorn im Rack vorgesehen war, ist noch offen: seitliches Rack außerhalb der Knieräume oder auf der Platte.

## Nachtrag: Rack-Zarge und Forex-Verkleidung
- **Rack-Zarge**: je Seite zwei waagerechte 2020-Profile (oben, unten), 350 mm lang, zwischen hinterer Rack-Schiene und Tiefenschiene, auf der Schienenachse. Die Schublade (435 mm breit) läuft daran vorbei. 4 Profile, 8 Winkel.
- **Forex classic 5 mm in der Nut (Stand v8)**: Die Platten stecken in der 8-mm-Nut der 4040-Profile (Mittelebene, 8 mm Eingriff) und werden mit dem Alux-Einfassprofil 8-12.40 (Plattenstärke 4 bis 6 mm) geklemmt. Das Einfassprofil nennt Plexiglas, Polycarbonat und Dibond; Forex steht dort nicht, bei Alux nachfragen. Es sind vier Platten: Seiten links/rechts 936 x 150,4 mm und hinten links/rechts 225 x 150,4 mm (rechts vom Rack-Fenster ebenso). Vorn bleibt offen (Kniefreiheit). Montage: Platte vor dem letzten Profil einschieben, dann Einfassprofil eindrücken.
- **Schriftzug** "open-ora" (Bahnschrift, 0,8 mm tief graviert, außen): einmal links, rechts und hinten (hinten auf dem linken Stück). Im Makro über `LOGO_TEXT`, `LOGO_FONTS`, `LOGO_DEPTH` einstellbar. Vorher war die Verkleidung 3 mm außen aufgesetzt (v7), das entfällt.
- Forex ist nicht leitfähig und hält keine hohen Temperaturen aus (erweicht bei ca. 70 bis 80 °C). Es ist eine Abdeckung, kein Berührschutz für Netzteile. Netzseitige Teile bleiben Sache der Elektrofachkraft, siehe SAFETY.md. Lüftung der Netzteile nach Einbau prüfen.
- Das Makro meldet 48 Objekte ohne Kollisionen (Bild: `docs/images/frame_v8.png`). Nuttiefe von 12 mm ist geschätzt, gegen den STEP-Schnitt prüfen. Die Steifigkeitsrechnung ist nicht aktualisiert; Zargen und Platten bringen eher Steifigkeit dazu und sind dort nicht angesetzt.

## Nachtrag: Diagonalen angeschlossen (v9)
Die drei 2020-Diagonalen schwebten bisher frei. Jetzt sitzt jede Diagonale an beiden Enden auf einem Knotenblech (Alu 4 mm, 130 x 130 mm) auf der Innenseite der Rahmenprofile. Das Blech liegt über beiden Profilen der Ecke und wird mit je zwei M8-Schrauben und Nutensteinen pro 4040-Profil befestigt, die Diagonale mit zwei M5-Schrauben. Wo ein Quer-Profil im Weg ist, ist das Blech ausgeklinkt. Die Diagonalen sind dafür 930 mm lang (vorher 900 mm) und nach innen versetzt (Blechdicke plus halbe Profilbreite). 6 Bleche, Makro ohne Kollisionen, Kontakt Diagonale/Blech 0 mm. Die Bohrbilder und die Festigkeit der Bleche sind noch nicht ausgelegt. Bei der Steifigkeitsrechnung werden die Diagonalen weiter als gelenkig angeschlossene Stäbe angesetzt.

## Nachtrag: Eckstreben 45 Grad statt Diagonalen (v10)
Alux führt den Winkelverbinder 4040-45 (Art. 4040-45, 3,39 EUR netto, STEP `4040-45.STEP` auf der Produktseite). Die 2020-Diagonalen (ca. 22 Grad) und die Knotenbleche entfallen, `BRACING = "knee"` im Makro (`"diag"` bringt die alte Lösung zurück).
- Je Wand (links, rechts, hinten) und je Pfosten eine Strebe aus 4040 unter dem unteren Rahmen: 6 Streben à 283,6 mm mit 90-Grad-Enden, 12 Verbinder, Schenkel 250 mm. Die Streben liegen in der Profilebene und ragen nicht in den Beinraum.
- **Platzhalter**: Verbinderhöhe (`KNEE_TRIM = 35 mm`) und -breite (40 mm) sind angenommen. Sobald das STEP des 4040-45 vorliegt, werden die Werte eingesetzt, die Strebenlänge ändert sich damit. Auch die Schrauben (je Verbinder 2x M8x16, 2x M8x25, 2 Nutensteine) sind aus der Seite des 4080-45 übernommen, nicht geprüft.
- Makro: 63 Objekte, keine Kollisionen, alle Teile berühren sich. 15,62 m Profil 4040 (ca. 21,8 kg).
- Steifigkeit **nicht neu gerechnet**. Die Eckstreben machen die Ecken am unteren Rahmen deutlich steifer als der Winkel allein. Als grobe Einordnung liegt der Tisch dann zwischen den Spalten "steif" und "starr" der Tabelle oben, nicht in der Spalte "weich". Für belastbare Zahlen müssen die Streben in `frame_stiffness.py` als Stäbe ergänzt werden.

## Nachtrag: Füße (v11)
- **Gewählt**: Alux Gelenkstellfuß 80 mm, M8x50 (Art. 80-M8x50, 3,49 EUR netto, PA6 glasfaserverstärkt mit Gummiauflage, STEP auf der Produktseite). Der Gelenkkopf gleicht Bodenunebenheiten aus, die Ø80-Auflage verteilt die Last und dämpft.
- **Befestigung**: M8-Gewinde (ca. 25 mm tief, von unten) in den Kernkanal des 4040-Pfostens schneiden (Kernloch 6,8 mm laut Profil). Der Fuß schraubt direkt ein, es entfällt Plattenmaterial. Die Pfosten werden um die Fußbauhöhe kürzer (630 statt 680 mm), die Tischhöhe bleibt 740 mm.
- **Platzhalter**: Fußbauhöhe 50 mm (Mittelstellung), Auflagehöhe 12 mm und Verstellweg +-15 mm sind angenommen. Das STEP `80mm stelvoet + K13.5 M8x50 spindel.STEP` von der Produktseite liefert die echten Maße. Die Belastbarkeit nennt Alux nicht; bei ca. 80 bis 100 kg Tischgewicht und 4 Füßen sind es etwa 25 kg je Fuß, vor der Bestellung nachfragen.
- **Alternative**: Montageplatten-Set 80 mm (Art. Feet-set 80, 34,99 EUR netto für 4 Füße, 5-mm-Stahlplatten, die seitlich in die Nut des Pfostens geschraubt werden; Füße stehen dann etwas außerhalb des Pfostens, das hilft bei der Kippsicherheit). Maße der Platten stehen nicht auf der Seite.
- Makro: 67 Objekte, keine Kollisionen, Höhe 740 mm.
