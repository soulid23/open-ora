# Schnittstellen

Zentrale Datei für alle Werte, die mehrere Baustellen betreffen.
Nur belegte Werte eintragen, alles andere als "offen" markieren.

## Mechanik
| Parameter | Wert | Einheit | Quelle/Entscheidung | betrifft | Stand |
|---|---|---|---|---|---|
| Tischfläche | 1000 x 1000 | mm | 0006 | Tisch, Arm 1, Arm 2 | angenommen |
| Oberkante ESD-Matte | 740 | mm über Boden | 0006 | alle | angenommen |
| Arm 1: J1-Achse (Fuß) | x = 920, y = 920, hinten rechts auf dem Aluframe | mm | 0007 (Vorgabe) | Tisch, Arm 2, Sensorik | angenommen |
| Arm 1: Fuß am Rahmen | Modul von außen: 2 Wangen 10 mm an X_oben_hinten / Y_oben_rechts / Pfosten_RH, Deckplatte 12 mm 2 mm über der Matte, 7 × M8 + Nutensteine | - | 0007 Nachtrag | Tisch, Lichtrahmen | vorgeschlagen |
| Arm 1: Eckausschnitt Platte + Matte | entfällt bei Außenmodul (nur bei `MOUNT = "innen"`: 170 x 170) | mm | 0007 Nachtrag | Tisch | vorgeschlagen |
| Arm 1: Masse ohne Nutzlast | ca. 6,5 | kg | 0007 (Rechnung) | Tisch | vorgeschlagen |
| Arm 1: Nutzlast | max. 1,0 (Mittel 0,5) | kg | Vorgabe | Arm 1 | angenommen |
| Arm 1: Kippmoment am Fuß | ca. 26 | Nm | 0007 (Rechnung) | Tisch | vorgeschlagen |
| Arm 1: Säulenhöhe über Matte | ca. 400 | mm | 0007 | Sensorik (Portal) | vorgeschlagen |
| Präsentationspunkt P0 | x = 500, y = 450, Zone ±100 | mm | 0007 | Arm 1, Arm 2, Sensorik | vorgeschlagen |
| Platinenhöhe in der Zone | 30 bis 230 über Matte | mm | 0007 | Arm 2, Sensorik | vorgeschlagen |
| Nutzlast Tischplatte (3D-Drucker o. Ä., inkl. Wechsellast) | offen | kg, N | 0008 | Tisch, Sicherheit | offen |
| Nutzlast Unterbau-Fach (Trockeneinheiten) | offen | kg | 0008 | Tisch | offen |
| Modul-Befestigung am Rahmen | Nutprofil 4040, Nut 8, Nutensteine M8; Raster und Last je Punkt offen | - | 0008 | alle Module | offen |
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