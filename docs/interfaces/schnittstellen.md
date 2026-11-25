# Schnittstellen

Zentrale Datei für alle Werte, die mehrere Baustellen betreffen.
Nur belegte Werte eintragen, alles andere als "offen" markieren.

## Mechanik
| Parameter | Wert | Einheit | Quelle/Entscheidung | betrifft | Stand |
|---|---|---|---|---|---|
| Tischfläche | 1000 x 1000 | mm | 0006 | Tisch, Arm 1, Arm 2 | angenommen |
| Oberkante ESD-Matte | 780 (vorher 740) | mm über Boden | 0010 | alle | angenommen |
| Oberer Rahmen | 8080, z 680..760; innere Nutreihe (60 mm vom Rand) für die Platte, äußere (20 mm) und Außenflächen für Anbauten | mm | 0010 | Tisch, alle Module, Lichtrahmen | angenommen |
| Feste Querstrebe | oben 4080 hochkant y 600..640, z 680..760; unten 4040 y 600..640, z 505,6..545,6 | mm | 0010 | Tisch, Rack | angenommen |
| Rack-Raum | Rackkasten Multiplex 15 mm, Holzinnenmaß 490, 3 HE, Schienen Adam Hall 61535 an der Rückseite und bei y = 620 (Einbautiefe 380) | mm | 0010 | Tisch, Elektrik | angenommen |
| Arm 1: J1-Achse (Fuß) | x = 920, y = 920, hinten rechts auf dem Aluframe | mm | 0007 (Vorgabe) | Tisch, Arm 2, Sensorik | angenommen |
| Arm 1: Fuß am Rahmen | Modul von außen: 2 Wangen 10 mm an X_oben_hinten / Y_oben_rechts / Pfosten_RH, Deckplatte 12 mm 2 mm über der Matte, 7 × M8 + Nutensteine | - | 0007 Nachtrag | Tisch, Lichtrahmen | vorgeschlagen |
| Arm 1: Eckausschnitt Platte + Matte | entfällt bei Außenmodul (nur bei `MOUNT = "innen"`: 170 x 170) | mm | 0007 Nachtrag | Tisch | vorgeschlagen |
| Arm 1: Masse ohne Nutzlast | ca. 6,5 | kg | 0007 (Rechnung) | Tisch | vorgeschlagen |
| Arm 1: Nutzlast | max. 1,0 (Mittel 0,5) | kg | Vorgabe | Arm 1 | angenommen |
| Arm 1: Kippmoment am Fuß | ca. 26 | Nm | 0007 (Rechnung) | Tisch | vorgeschlagen |
| Arm 1: Säulenhöhe über Matte | ca. 400 | mm | 0007 | Sensorik (Portal) | vorgeschlagen |
| Lichtrahmen: Stützen am Tisch | 4 × 4040 außen (x -40..0 / 1000..1040), y 600..640 und 920..960, z 505,6..1460; je 2 Verbinder an Y_oben_* und Y_unten_*, kein Bodenkontakt | mm | light_frame.py v2 (Vorgabe Nutzer 2026-11-25) | Tisch, Arm 1, Sensorik | vorgeschlagen |
| Lichtrahmen: Oberkante / Unterkante Ausleger | 1500 / 1460 | mm über Boden | light_frame.py v2 | Sensorik, Sicherheit (Kopffreiheit) | vorgeschlagen |
| LED-Panel: Lage und Höhe | 595 x 595, Mitte x 500 / y 450, Unterkante z 1423 (683 über Matte) | mm | light_frame.py v2 | Sensorik, Arm 1 | vorgeschlagen |
| Sensorschiene: Lage | 2020 quer, y 440..460, z 1393..1413; Kamera-Unterkante ca. z 1358 | mm | light_frame.py v2 | Sensorik, Arm 1, Arm 2 | vorgeschlagen |
| Präsentationspunkt P0 | x = 500, y = 450, Zone ±100 | mm | 0007 | Arm 1, Arm 2, Sensorik | vorgeschlagen |
| Platinenhöhe in der Zone | 30 bis 230 über Matte | mm | 0007 | Arm 2, Sensorik | vorgeschlagen |
| Auslegung Drucker auf der Platte | QIDI Max4: 558 × 578 × 612 mm, 40 kg (Combo 46,5 kg), Kopf bis 30 000 mm/s² | mm, kg | 0009 (Hersteller) | Tisch, Sicherheit, Sensorik | angenommen |
| Nutzlast Tischplatte gesamt (inkl. Wechsel- und Stoßlast) | offen | kg, N | 0008, 0009 | Tisch, Sicherheit | offen |
| Nutzlast Unterbau (1 bis 2 Regalböden, 19"-Schubladen) | offen | kg | 0009 | Tisch | offen |
| Modul-Befestigung am Rahmen | leicht: Außennuten der Holme (Nut 8, Nutensteine M8); schwer: Pfosten oder vorab montierte Zusatzprofile; Raster und Last je Punkt offen | - | 0009, module.md | alle Module | vorgeschlagen |
| Datenbus Tischverbund | RS485 oder CAN (Auswahl offen) über RJ45, unverwechselbar zu Ethernet; dazu Ethernet | - | 0009 | Elektronik, alle Tische | vorgeschlagen |
| Befestigung Wechselplatte | (1) verschraubt: Platte 920 x 920 x 18, 29 × DIN 7991 M6x25 + Nutenstein M6 in innerer Reihe und Querstrebe (Bohrplan); (2) Schnellspannsystem offen; Vor-Nutensteine an der Innenseite der 8080-Seitenholme | - | 0009, 0010 | Tisch | angenommen (1) / offen (2) |
| Tastkraft Prober (Auslegung Halter) | max. 2 | N | Annahme 0007 | Arm 1, Arm 2 | offen |
| Träger-Kupplung | 3 Kugeln / 3 Nuten, Ø 60 mm, Verriegelung selbsthemmend | - | 0007 | Arm 1, Träger | vorgeschlagen |

## Elektrik
| Parameter | Wert | Einheit | Quelle/Entscheidung | betrifft | Stand |
|---|---|---|---|---|---|
| ESD: Ableitwiderstand Arbeitsfläche gegen Erde | < 1 · 10⁹ (Norm), Matte über 1 MΩ an PE | Ω | DIN EN IEC 61340-5-1, SAFETY.md | Tisch, Sicherheit | vorgeschlagen |

## Daten und Protokolle
| Parameter | Wert | Einheit | Quelle/Entscheidung | betrifft | Stand |
|---|---|---|---|---|---|

## Software-Schnittstellen
| Parameter | Wert | Einheit | Quelle/Entscheidung | betrifft | Stand |
|---|---|---|---|---|---|