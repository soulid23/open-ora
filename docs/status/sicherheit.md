# Status: sicherheit

## Ziel
Der Aufbau ist sicher zu bauen und zu benutzen und erfüllt die einschlägigen Normen mit Reserve. Konstruktion,
Prüfung und Dokumentation sind so angelegt, dass eine Konformitätsbewertung (CE) später möglich ist (ADR 0008).

## Aktueller Stand (2026-11-25)
- Grundregeln in `SAFETY.md`: Netzseite nur durch Elektrofachkraft, Netzspannung nur hinten im Rack,
  Prüfinterface nur Kleinspannung, Schutzleiter an allen leitenden Teilen, ESD-Matte über 1 MΩ an Erde.
- Grundsatz „Normen von Anfang an“ beschlossen (ADR 0008), erste Liste bekannter Vorgaben dort.
- Normenlandkarte `docs/normen.md` noch nicht angelegt.

## Entscheidungen (Verweise auf docs/decisions/)
- `0008-version1-modularer-tisch-normen.md` (angenommen, Grundsätze)

## Offene Fragen
- Welche Vorgaben gelten für Version 1 als Selbstbau und welche erst für Bausätze oder Geräte (offene Frage 7)?
- Not-Aus schon in Version 1 (Licht, Netzteile) oder erst mit den Armen in Version 2?
- Wärme im Unterbau (Trockeneinheiten, Netzteile) gegen Forex und Elektronik (offene Frage 8).

## Nächste Schritte
1. `docs/normen.md` anlegen: je Anforderung Quelle, Grenzwert, eigener Zielwert, Nachweis (Rechnung/Messung), Stand.
2. Prüfungen für M3 festlegen: Standsicherheit/Festigkeit nach EN 1730 (Messlatte EN 527-2), ESD-Ableitung nach
   DIN EN IEC 61340-5-1, Schutzleiter.
3. Normenlandkarte mit einer Fachstelle abgleichen.

## Abhängigkeiten zu anderen Baustellen
- **Tisch**: Standsicherheit, Festigkeit, ESD, Lastannahmen für weitere Anwendungen.
- **Stromversorgung**: Netzseite, Schutzleiter, Abnahme durch Elektrofachkraft.
- **Arm 1 / Arm 2** (Version 2): Maschinenverordnung (EU) 2023/1230, Not-Aus, Geschwindigkeit, Quetschstellen.
