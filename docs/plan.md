# Plan: open-ora

Soll-Zustand des Projekts. Die Statusdateien in `docs/status/` beschreiben das Ist,
diese Datei das Soll. `_projektleitung/pm.py` vergleicht beides.

> **Entwurf der Projektleitung (2026-11-24).** Ziele und Meilensteine sind Vorschläge aus dem
> bisherigen Stand (README, ADRs 0001 bis 0007, offene Fragen). Bitte bestätigen, ändern
> und Soll-Daten eintragen.

Format für Aufgaben: `- [ ] baustelle: Text` (Baustelle = Name der Statusdatei),
erledigt: `- [x]`. Soll-Datum im Meilenstein-Titel: `(Soll: JJJJ-MM-TT)`.

## Ziel
Ein offener, nachbaubarer Reparaturtisch für Elektronik (1000 × 1000 mm), auf dem ein Halter-Arm
eine Platine in eine Präsentationszone bringt und ruhig hält, Kameras mit lokaler KI sie erkennen
und ein Prober Testpunkte antastet. Alles dokumentiert unter CERN-OHL-W / Apache-2.0.

## Nicht-Ziele
- Kein Industrieprodukt, keine Zertifizierung; Nachbau auf eigene Verantwortung (`SAFETY.md`).
- Keine Cloud-Abhängigkeit: KI läuft lokal.
- Netzspannungsseite wird nicht von Laien gebaut (Elektrofachkraft).

## Meilensteine

### M0: Projektbasis einheitlich (Soll: offen)
- [ ] Alte Kopie `C:\dev\open-ora_al` archivieren oder löschen
- [ ] README auf Stand 1000 × 1000 mm bringen (offene Frage 4)
- [ ] Alle Statusdateien mit Ziel und aktuellem Stand füllen
- [ ] Soll-Daten für M1 bis M4 festlegen

### M1: Tisch steht (Soll: offen)
- [ ] tisch: Eckausschnitt 170 × 170 mm für Arm 1 entscheiden (offene Frage 3)
- [ ] tisch: BOM Rahmen (`bom/frame_bom.csv`) prüfen und bestellen
- [ ] tisch: Rahmen montieren, Platte als Scheibe verschrauben
- [ ] tisch: Steifigkeit am fertigen Tisch messen und mit `frame_stiffness.py` vergleichen

### M2: Konzepte beider Arme angenommen (Soll: offen)
- [ ] arm1-halter: Annahmen bestätigen, ADR 0007 auf "angenommen"
- [ ] arm2-prober: Montageort und Bauart entscheiden (offene Frage 2), ADR schreiben
- [ ] arm2-prober: Tastkraft festlegen (Schnittstelle "Tastkraft Prober")
- [ ] sensorik-ki: Höhe und Lage des Kameraportals entscheiden (offene Frage 1)
- [ ] sicherheit: Sicherheitskonzept für die Arme (Not-Aus, Geschwindigkeit, Quetschstellen)

### M3: Elektrik und Steuerung festgelegt (Soll: offen)
- [ ] stromversorgung: Spannungen, Netzteile, Not-Aus-Kette festlegen
- [ ] elektronik: Motortreiber, Geber, ESP32-Belegung festlegen
- [ ] elektronik: Schnittstellen-Abschnitte "Elektrik" und "Daten und Protokolle" füllen
- [ ] sicherheit: Abnahme der Netzseite durch Elektrofachkraft einplanen

### M4: Erste Bewegung (Soll: offen)
- [ ] arm1-halter: Prototyp Handgelenk J5/J6 drucken und testen
- [ ] arm1-halter: J1 und Hubsäule aufbauen, Platine in die Präsentationszone fahren
- [ ] sensorik-ki: Kamera erkennt den Träger anhand der Marker
- [ ] elektronik: MQTT-Verbindung Pi ↔ ESP32 ↔ Laptop steht
