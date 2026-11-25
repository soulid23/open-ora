# 0001: Systemarchitektur

Status: angenommen. Rechnerrollen ergänzt durch `0005-rechnerrollen.md` (KI-Training und Sprachmodell auf dem Desktop,
der Laptop nur für die Echtzeit-Erkennung am Tisch).

- Laptop (RTX 3070): Bildverarbeitung und KI
- Raspberry Pi: Kameras, Bahnplanung, Brücke zum Laptop
- ESP32: Motoren, Licht, Sensoren (echtzeitnah)
- Kommunikation: MQTT, später ggf. ROS 2
- CAD: FreeCAD 1.1, parametrisch per Python-Skript
- Zwei Manipulatoren: Halter (Nutzlast) und Prober (Präzision)
