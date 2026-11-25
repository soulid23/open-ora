# 0010: Oberer Rahmen 8080, feste Querstrebe, Rackkasten, Platte 920 x 920

Status: angenommen (2026-11-26). Die Werte unten sind Überschlagsrechnungen mit Annahmen; Messungen am fertigen Tisch gehen vor.
Ergänzt 0006 (Tisch 1000 x 1000) und 0009 (Modul-Grundsätze). Makro: `cad/macros/tisch_8080.py`, Modell `cad/frame/OpenORA_Tisch8080.FCStd` (nicht im Repo).

## Entscheidung
- **Oberer Rahmen aus 8080** (Alux 8080): vorn/hinten 1000 mm durchgehend, Seitenholme 840 mm dazwischen.
  Beine, unterer Rahmen, Bodenstreben und Eckstreben bleiben 4040 wie in Version 1 (Beine 630 mm, unterer Rahmen 505,6 bis 545,6 mm, Rack-Raum 3 HE).
- **Tischhöhe 780 mm** (Oberkante ESD-Matte), oberer Rahmen 680 bis 760 mm.
- **Nutreihen**: die innere Reihe (60 mm vom Rand) trägt die Platte, die äußere (20 mm vom Rand) und die Außenflächen bleiben frei für Anbauten.
- **Platte 920 x 920 mm**, Siebdruck 18 mm, 40 mm vom Rand eingerückt, damit die äußere Reihe frei bleibt. 29 Senkschrauben M6x25 mit Nutenstein M6 in der inneren Reihe und auf der Querstrebe (Bohrplan `docs/build-guide/bohrplan_platte_8080.pdf`). Die Platte wirkt weiter als Scheibe (ADR 0006).
- **Feste Querstrebe oben**: 4080 hochkant bei y = 600 bis 640 mm, bündig mit Ober- und Unterkante des 8080. Sie stützt die Platte und trägt den Rackkasten. Durchbiegung bei 500 N in der Mitte ca. 0,15 mm (4040 an gleicher Stelle: ca. 1,2 mm). Damit ist der abnehmbare Mittelträger aus ADR 0009 für schwere Lasten (Drucker, Werkbank) nicht mehr nötig.
- **Feste Querstrebe unten**: 4040 bei y = 620 mm im unteren Rahmen (wie bisher Mittelträger unten).
- **Rackkasten** statt 2020-Rackschienen und Zargen: zwei Wände Multiplex Birke 15 mm (400 x 134 mm), Holzinnenmaß 490 mm, auf/unter den Querstreben und den hinteren Trägern, je Wand 4 Winkel 4040. Darin 4 Rackschienen Adam Hall 61535 B 3 (3 HE): zwei an der Rückseite, zwei innen bei y = 620 (Einbautiefe 380 mm).

## Verbindungen (geprüft im Makro: 0 Kollisionen, alle 40 Winkel liegen an beiden Teilen an)
| Stelle | Verbindung |
|---|---|
| Bein oben an 8080 vorn/hinten | Zentralverbinder (Option am Bein) + 2 Winkel 4040 unter dem 8080, je einer in jeder unteren Nutreihe |
| 8080 seitlich an 8080 vorn/hinten | 4 Zentralverbinder je Ende (Option am 8080) + Winkel 8080 in der Innenecke (beide Reihen) |
| Querstrebe 4080 an 8080 seitlich | 2 Zentralverbinder je Ende + 2 Winkel 4080 |
| unterer Rahmen, untere Querstrebe, Bodenstreben | Zentralverbinder + Winkel 4040 (unterer Rahmen: Winkel unter dem Träger) |
| Eckstreben | Winkelverbinder 4040-45 wie Version 1 |
| Rackkasten | 8 Winkel 4040 außen an den Wänden, Zentrierstege auf der Holzseite abbrechen |

Gefundene und gelöste Konflikte:
- Winkel oben auf dem unteren Rahmen und an den Beinoberseiten lägen in der Ebene der Forex-Platten. Unterer Rahmen: Winkel deshalb unter dem Träger, dazu Zentralverbinder. Beine oben: Forex an den oberen Ecken 52 x 52 mm ausklinken.
- Forex hinten endet 40 mm vor den Kastenwänden (Platz für die Kastenwinkel), Zuschnitt 168 x 150,4 mm.
- Rackschienen 61535: Lochfläche 21 mm, Schenkel 30 mm an der Wand angenommen; lichte Weite dann 448 mm. Am Teil prüfen.

## Folgen
- Profilmasse ca. 31,6 kg (Version 1 mit 4040 oben ca. 22 kg).
- Seitensteifigkeit ändert sich durch 8080 allein kaum; der Gewinn kommt aus den steiferen Ecken (Zentralverbinder + Winkel in beiden Reihen) und der verschraubten Platte. Messung offen.
- Max4 plus Lichtrahmen: Oberkante Drucker 1392 mm, Kameras heute ca. 1358 mm. Das Portal muss für einen Tisch mit beidem mindestens ca. 40 mm höher.
- Sitzen: 780 mm liegt über Schreibtischhöhe, höherer Stuhl oder Fußstütze; Probesitzen.
- Stückliste: `bom/tisch_8080_bom.csv` (aus dem Makro); Einkaufsliste mit Preisen als Claude-Sheet.

## Offen
- Preise Alux: Shop zeigt je Profil einen Stückpreis der Grundkonfiguration; Längenpreis im Konfigurator prüfen.
- Maße der Winkel 4080L/8080L und der Schrauben je Winkel aus dem Datenblatt.
- Schraubenlänge Platte (M6x25) an der ersten Bohrung prüfen.
- Steifigkeit mit 8080-Ecken in `frame_stiffness.py` neu rechnen.
