# Plan: open-ora

Soll-Zustand des Projekts. Die Statusdateien in `docs/status/` beschreiben das Ist,
diese Datei das Soll. `_projektleitung/pm.py` vergleicht beides.

> **Stand 2026-11-25.** Umfang und Grundsätze sind bestätigt (ADR 0008). Die Meilensteine sind ein Vorschlag:
> bitte Soll-Daten eintragen. Jeder Meilenstein soll in wenigen Wochen schaffbar sein und endet mit einem kurzen Baubericht.

Format für Aufgaben: `- [ ] baustelle: Text` (Baustelle = Name der Statusdatei),
erledigt: `- [x]`. Soll-Datum im Meilenstein-Titel: `(Soll: JJJJ-MM-TT)`.

Zuletzt abgeglichen: 2026-11-25.

## Ziel
Eine offene, nachbaubare und modulare Tischplattform (1000 × 1000 mm), deren erste Anwendung ein
Reparatur-Assistent für Elektronik ist: Licht, Kameras und Wärmebild über dem Tisch, eine lokale KI hilft bei
der Fehlersuche. Dieselbe Plattform trägt auch andere Module, z. B. einen 3D-Drucker oben und Trockeneinheiten
für Filament darunter. Konstruktion und Nachweise sind von Anfang an so angelegt, dass die einschlägigen Normen
mit Reserve erfüllt werden. Alles dokumentiert unter CERN-OHL-W / Apache-2.0.

**Version 1**: Tisch, Licht- und Sensorrahmen, Kamera, Wärmebild, KI-Auswertung.
**Version 2**: Arme (Halter, Prober).

## Nicht-Ziele
- Kein Industrieprodukt in Version 1; Nachbau auf eigene Verantwortung (`SAFETY.md`).
- Keine Cloud-Abhängigkeit: KI läuft lokal.
- Netzspannungsseite wird nicht von Laien gebaut (Elektrofachkraft).
- Keine Arme in Version 1.

## Meilensteine Version 1

### M0: Projektbasis einheitlich (Soll: offen)
- [x] Alte Kopie `C:\dev\open-ora_al` archivieren oder löschen
- [x] README auf Stand 1000 × 1000 mm bringen (offene Frage 4)
- [x] Umfang Version 1 festlegen (ADR 0008)
- [ ] Alle Statusdateien mit Ziel und aktuellem Stand füllen
- [ ] Soll-Daten für die Meilensteine festlegen
- [ ] Webseite an Version 1 anpassen (Arme folgen in Version 2)

### M1: KI-Test provisorisch (Soll: offen)
Erfolgskriterium (Vorschlag): Auf mindestens 5 Platinen mit bekanntem Defekt zeigt der Aufbau den Fehler
(heißes Bauteil, Kurzschluss oder sichtbarer Schaden) in mindestens 4 Fällen an.
- [ ] sensorik-ki: Testaufbau planen (Stativ, Kamera, Wärmebildmodul, Beleuchtung, Testplatinen)
- [ ] sensorik-ki: Testplatinen mit bekanntem Defekt sammeln und beschreiben
- [ ] sensorik-ki: Wärmebild auswerten (heiße Bauteile, Kurzschluss) auf der RTX 3080
- [ ] sensorik-ki: Kamerabild auswerten (sichtbare Schäden)
- [ ] sensorik-ki: Ergebnis gegen das Erfolgskriterium dokumentieren, Baubericht

### M2: Tisch bestellbereit (Soll: offen)
- [x] tisch: Anschluss Arm 1 klären (Außenmodul statt Eckausschnitt, ADR 0007 Nachtrag)
- [ ] tisch: offene Punkte nach „blockiert Bestellung ja/nein“ sortieren
- [x] tisch: Anwendungsliste, Zonen und Belegungsplan als Entwurf anlegen (`docs/interfaces/module.md`)
- [ ] tisch: Lastannahmen je Anwendung festlegen (Anwendungsliste, offene Frage 8)
- [ ] tisch: Belegungsplan bestätigen, Konflikte lösen (offene Fragen 5 und 11)
- [ ] tisch: Tischverbund klären: Pfosten-Verbinder, Strom durchschleifen, Datenleitungen (offene Frage 10)
- [ ] tisch: Module im CAD gegen die Zonen prüfen (Platzhalter Drucker, Fach-Modul, Nachbartisch)
- [ ] tisch: Unterbau-Fach als Modul vorsehen (Knieraum oder Fach), ohne den Grundrahmen zu ändern
- [ ] tisch: Ort des Prüf-/Tastinterface festlegen (offene Frage 6)
- [ ] tisch: Alternative Bezugsquelle für Profil und Rack-Einschübe in die Stückliste
- [ ] tisch: Bestellliste Alux mit Artikelnummern und Preisen füllen

### M3: Tisch steht (Soll: offen)
- [ ] tisch: Rahmen bestellen und montieren, Platte als Scheibe verschrauben
- [ ] tisch: Steifigkeit messen (100 N seitlich) und mit `frame_stiffness.py` vergleichen
- [ ] tisch: Standsicherheit und Festigkeit nach EN 1730 prüfen (Messlatte EN 527-2, mit Reserve)
- [ ] tisch: ESD-Ableitung der Arbeitsfläche messen (DIN EN IEC 61340-5-1)
- [ ] tisch: Baubericht

### M4: Licht und Sensorik am Tisch (Soll: offen)
- [ ] tisch: Konflikt Lichtrahmen-Stütze mit Arm-Außenmodul lösen (offene Frage 5)
- [x] sensorik-ki: Makro `light_frame.py` (v2) ins Repo
- [ ] sensorik-ki: Höhe und Lage des Kameraportals entscheiden (offene Frage 1), Verbinder Stütze/Seitenholm wählen
- [ ] sensorik-ki: Licht- und Sensorrahmen bauen, Kamera und Wärmebild aus M1 montieren
- [ ] sensorik-ki: Auswertung aus M1 am Tisch wiederholen
- [ ] elektronik: Raspberry Pi für Kameras, Verbindung zum Laptop am Tisch

### M5: Elektrik Version 1 (Soll: offen)
- [ ] stromversorgung: Umfang festlegen (Netzteile, Verteilung, Not-Aus ja/nein in Version 1)
- [ ] elektronik: Schnittstellen-Abschnitte „Elektrik“ und „Daten und Protokolle“ füllen
- [ ] sicherheit: Abnahme der Netzseite durch Elektrofachkraft, Prüfprotokoll

### Q: Normen und Nachweise, laufend (Soll: offen)
- [ ] sicherheit: Normenlandkarte `docs/normen.md` anlegen (Anforderung, Grenzwert, Zielwert, Nachweis)
- [ ] sicherheit: Normenlandkarte mit einer Fachstelle abgleichen (offene Frage 7)

## Meilensteine Version 2

### V2: Arme (Soll: offen, nach Version 1)
- [ ] arm1-halter: Annahmen bestätigen, ADR 0007 auf "angenommen"
- [ ] arm2-prober: Montageort und Bauart entscheiden (offene Frage 2), ADR schreiben
- [ ] arm2-prober: Tastkraft festlegen (Schnittstelle "Tastkraft Prober")
- [ ] sicherheit: Sicherheitskonzept für die Arme nach Maschinenverordnung (EU) 2023/1230
- [ ] arm1-halter: Prototyp Handgelenk J5/J6 drucken und testen
- [ ] arm1-halter: J1 und Hubsäule aufbauen, Platine in die Präsentationszone fahren
- [ ] elektronik: Motortreiber, Geber, ESP32-Belegung, MQTT Pi ↔ ESP32 ↔ Laptop
