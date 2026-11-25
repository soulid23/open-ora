# 0008: Version 1 ohne Arme, Tisch als modulare Plattform, Normen von Anfang an

Status: angenommen (Grundsätze, 2026-11-25). Die Einzelheiten unter „Offen“ sind noch zu klären.
Ändert den Umfang aus `docs/plan.md` (Entwurf 2026-11-24). Ergänzt `0006` (Tisch) und `0007` (Arm 1).

## Kontext
Auswertung gescheiterter Hardware- und Open-Source-Projekte (Protokoll der Projektleitung, 2026-11-25):
Häufigste Ursachen sind wachsender Umfang, unerprobte Technik, Konstruktionsfehler, Abhängigkeit von einer Person,
Beschaffung und eine zu spät bedachte Zertifizierung. Bei der Planung des Tisches hat sich außerdem gezeigt, dass er
sehr steif ausgelegt werden kann und sich auch für andere Anwendungen eignet.

## Entscheidung

### 1. Umfang Version 1
- **Version 1** = Tisch + Licht- und Sensorrahmen + Kamera + Wärmebild + KI-Auswertung. **Keine Arme.**
- **Version 2** = Arm 1 (Halter) und Arm 2 (Prober). ADR 0007 und das Makro `arm_holder.py` bleiben gültig;
  der Tisch behält den Anschluss für das Arm-Außenmodul hinten rechts als Reserve.
- **Größtes Risiko zuerst**: Die KI-Fehlersuche wird vor dem Tischbau mit einem provisorischen Aufbau getestet
  (Kamera und Wärmebild auf Stativ über Platinen mit bekanntem Defekt, Auswertung auf der RTX 3080).
- Kleine Meilensteine von wenigen Wochen, je mit kurzem Baubericht.

### 2. Tisch als modulare Plattform
- Der Tisch ist eine **Grundplattform**; der Reparatur-Assistent ist die erste Anwendung, nicht die einzige.
- Weitere Anwendungen, für die er ausgelegt wird: **3D-Drucker auf der Platte**, **Trockeneinheiten für Filament
  im Unterbau**, allgemeiner Werkstatt- und Elektronikarbeitsplatz.
- Grundsatz: Alles, was anwendungsspezifisch ist, wird als **Modul** von außen oder in definierte Bereiche geschraubt
  (Nutprofil 4040, Nutensteine), ohne den Grundrahmen zu ändern. Beispiele: Arm-Außenmodul, Licht- und Sensorrahmen,
  Rack-Einschübe hinten, Unterbau-Fach statt Knieraum.
- Lasten werden für die **ungünstigste Anwendung** ausgelegt, nicht nur für den Reparaturtisch
  (z. B. Drucker mit schnell bewegtem Kopf: Schwingung und Wechsellast).

### 3. Normen von Anfang an
- Konstruktion, Prüfung und Dokumentation werden so angelegt, dass eine **Konformitätsbewertung (CE)** später möglich
  ist, auch wenn Version 1 ein offenes Selbstbau-Projekt bleibt.
- Ziel ist, die Anforderungen der einschlägigen Normen **mit Reserve zu erfüllen** (Messwerte mit Abstand zum
  Grenzwert, Sicherheitsfaktoren dokumentiert).
- Jede Anforderung wird mit Quelle, Grenzwert, eigenem Zielwert und Nachweis (Rechnung oder Messung) in
  `docs/normen.md` geführt (Normenlandkarte, Baustelle Sicherheit).

### Bekannte Vorgaben (Ausgangspunkt, noch vollständig zu prüfen)
| Bereich | Vorgabe | betrifft | Bemerkung |
|---|---|---|---|
| Standsicherheit, Festigkeit Tisch | EN 1730 (Prüfverfahren Tische) | Tisch | enthält nur Prüfverfahren; Anforderungen z. B. aus EN 527-2 (Büro-Arbeitstische) als Messlatte |
| ESD-Arbeitsplatz | DIN EN IEC 61340-5-1 | Tisch, Sicherheit | Arbeitsfläche gegen Erde < 1 · 10⁹ Ω; aktuelle Ausgabe 2025-06 prüfen |
| Elektrische Installation, Prüfung | DIN VDE 0100-600, DIN VDE 0701-0702 | Stromversorgung | siehe `SAFETY.md` |
| Elektrische Betriebsmittel | Niederspannungsrichtlinie 2014/35/EU, EMV-Richtlinie 2014/30/EU, RoHS | Stromversorgung, Elektronik | erst relevant, wenn Geräte oder Bausätze in Verkehr gebracht werden |
| Maschinen (Version 2, Arme) | Maschinenverordnung (EU) 2023/1230, gilt ab 20.01.2027 und ersetzt die Maschinenrichtlinie 2006/42/EG | Arme, Sicherheit | gilt auch für Steuerungen und Software; Arme kommen voraussichtlich erst danach |

Diese Liste ist kein Rechtsrat. Welche Vorgaben im Einzelfall gelten, hängt davon ab, ob und wie etwas in Verkehr
gebracht wird (Selbstbau, Bausatz, fertiges Gerät); das klärt eine fachkundige Stelle.

## Folgen
- `docs/plan.md`: neuer Meilenstein „KI-Test provisorisch“ vor dem Tischbau, Arme in „Version 2“, kleinere Meilensteine.
- Tisch: Lastannahmen für 3D-Drucker und Unterbau-Fach ergänzen; Steifigkeit gegen Wechsellast prüfen
  (Drucker und Kamera nicht gleichzeitig auf derselben Platte oder Schwingung messen).
- Wärme: Trockeneinheiten unter der Platte und Netzteile im Rack geben Wärme ab; Forex erweicht ab ca. 70 bis 80 °C (0006).
- Webseite: Text an Version 1 anpassen (Arme folgen in Version 2).

## Offen
- Normenlandkarte `docs/normen.md` erstellen und mit einer Fachstelle abgleichen.
- Lastannahmen: Masse und Wechsellast typischer 3D-Drucker, Masse der Trockeneinheiten, Lage des Unterbau-Fachs.
- Modul-Schnittstelle festlegen: Raster der Befestigungspunkte, zulässige Lasten je Punkt, Kabelführung, Erdung.
- Wie weit Version 1 elektrisch geht (nur Steckdosenleiste und Netzteile oder eigene Verteilung mit Not-Aus).
