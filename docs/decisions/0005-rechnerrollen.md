# 0005: Rechnerrollen

Status: angenommen, ergänzt `0001-architektur.md` (dort war der Laptop der zentrale KI-Rechner)

## Rechner
- **Desktop**: Ryzen 9 7800X3D, RTX 3080 mit 10 GB. Entwicklung, FreeCAD, Training der Modelle, lokales Sprachmodell.
- **Laptop (am Tisch)**: Aorus mit mobiler RTX 3070 (vermutlich 8 GB, prüfen). Echtzeit-Erkennung, Anzeige, Bedienung.
- **Raspberry Pi**: Kameras, Bahnplanung, Brücke zu den Rechnern.
- **ESP32**: Motoren, Licht, Sensoren.

## Aufgabenteilung
| Aufgabe | Rechner |
|---|---|
| Entwicklung, Repo, FreeCAD, Claude Code | Desktop |
| Training und Feintuning (z. B. YOLO) | Desktop |
| Lokales Sprachmodell als Assistent (ca. 7 bis 8 Mrd. Parameter, 4 Bit) | Desktop, Zugriff über das lokale Netz |
| Echtzeit-Erkennung (kleines Bildmodell, OCR) | Laptop |
| Kamerabilder aufnehmen und weiterleiten | Raspberry Pi |

## Hinweise
- Sprachmodell und Bildmodelle nicht gleichzeitig auf derselben Karte betreiben (10 GB bzw. 8 GB Grafikspeicher).
- Der Tisch soll ohne Desktop nutzbar bleiben; der Assistent ist eine Erweiterung.
- Abgleich: Git für Code und Dokumentation, Nextcloud für Herstellerdateien und große Daten.

## Offen
- Grafikspeicher des Laptops bestätigen.
- Netzwerk und Protokoll zwischen den Rechnern (MQTT, später ggf. ROS 2).
