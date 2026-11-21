# Sicherheit und Haftung

open-ora ist ein Bastel- und Entwicklungsprojekt. Der Nachbau erfolgt **auf eigene Verantwortung**.
Die Hardware-Lizenz (CERN-OHL-W) und die Software-Lizenz (Apache-2.0) schließen jede Gewährleistung aus.

## Elektrische Arbeiten: nur durch eine Elektrofachkraft

Alle Arbeiten an Netzspannung (230 V) dürfen **nur von einer Elektrofachkraft** ausgeführt und abgenommen werden.
Das betrifft insbesondere:

- Netzeingang (Kaltgerätebuchse, Netzfilter, Sicherung, Hauptschalter, Not-Aus)
- Verdrahtung und Anschluss von Netzteilen
- Schutzleiteranbindung aller leitenden Teile (Rahmen, Frontplatten, Arbeitsfläche, ESD-Matte)
- Erst- und Wiederholungsprüfung nach den geltenden Vorschriften und Normen

Wer keine Elektrofachkraft ist, baut nur die mechanischen Teile und die Kleinspannungsseite (SELV) nach
und lässt den Netzteil des Aufbaus von einer Fachkraft anschließen und prüfen.

## Grundregeln für den Aufbau

- **Trennung**: Netzspannung nur auf der Rückseite (feste Anschlüsse), nie an der vorderen Schnittstellenplatte.
  Die Vorderseite führt ausschließlich Kleinspannung (SELV).
- **Schutzleiter**: Alle berührbaren leitenden Teile liegen auf PE. Die ESD-Matte wird über einen
  1-MΩ-Widerstand (ESD-gerecht) mit dem Erdungspunkt verbunden.
- **Absicherung**: Netzseitig Sicherung und Fehlerstrom-Schutzeinrichtung (RCD) laut Elektrofachkraft.
- **Not-Aus**: Sobald Roboterarme oder Portale bewegt werden, ist ein Not-Aus Pflicht, der die Antriebe
  zuverlässig stromlos macht, unabhängig von Software und ESP32.
- **Antriebe**: Software darf Sicherheitsfunktionen nicht allein übernehmen (Endschalter, Strombegrenzung,
  Not-Aus in Hardware).
- **Wärme**: Netzteile hinten mit ausreichender Belüftung, Druckteile in Wärmenähe aus PETG, ASA oder PA-CF.
  Lötarbeiten nur mit Absaugung.
- **Nicht unbeaufsichtigt**: Heißluft, Lötkolben und Netzteile nicht unbeaufsichtigt betreiben.

## Hinweise zu Frontplatten und Steckverbindern

- **Pulverbeschichtete Platten isolieren.** Metallgehäuse der Steckverbinder und die Platte selbst werden
  nur dann sicher mit PE verbunden, wenn die Kontaktstellen blank sind oder Zahnscheiben verwendet werden.
  Durchgang nach dem Einbau messen.
- **Steckverbinder nach Bemessungsdaten einsetzen.** XLR-Einbauteile der Neutrik D-Serie sind laut Datenblatt
  für Spannungen unter 50 V ausgelegt, sie sind nur für die Kleinspannungsseite (vorn) vorgesehen.
  Netzspannung führen ausschließlich dafür freigegebene Steckverbinder (z. B. powerCON-Familie), hinten.
- **Verwechslung ausschließen**: Netzsteckverbinder und Kleinspannungssteckverbinder nie vom selben Typ,
  nie auf derselben Platte.

## Prüfung und Dokumentation (Vorschlag)

Vor der ersten Inbetriebnahme und nach jeder Änderung an der Netzseite prüft die Elektrofachkraft mit
geeignetem Prüfgerät, mindestens:

- Sichtprüfung
- Schutzleiterverbindung zu allen leitenden Teilen
- Isolationswiderstand
- Ableit- und Berührungsstrom
- Funktion von RCD und Not-Aus

Die Messwerte und Grenzwerte richten sich nach den jeweils gültigen Normen (z. B. DIN VDE 0100-600,
DIN VDE 0701-0702, DIN EN 61010-1 für Labor- und Messgeräte). Die Fachkraft legt das fest.
Das Prüfprotokoll gehört **nicht** ins öffentliche Repo, sondern in die persönliche Ablage
(z. B. Nextcloud-Ordner `open-ora-assets/pruefprotokolle`).

## Hinweis für Mitwirkende

Pull Requests, die die Netzseite oder Sicherheitsfunktionen ändern, werden als solche gekennzeichnet
und brauchen vor dem Merge eine Prüfung durch eine Elektrofachkraft.
