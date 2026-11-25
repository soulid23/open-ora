# 0002: 19-Zoll-Rack auf den langen Seiten

Status: angenommen, **teilweise ersetzt durch `0006-tisch-1x1-verstrebung.md`**.

> **Stand heute (ADR 0006):** Der Tisch ist 1000 x 1000 mm groß und 740 mm hoch. Das 19"-Rack (3 HE) gibt es nur
> noch **hinten**; vorn ist der Sitzplatz frei (`FRONT_RACK = False`). Maße und Aufteilung unten gelten für den
> früheren Tisch 600 x 500 mm und sind nur noch als Herleitung der Rack-Schienen (2020, Nutabstand 465,1 mm) gültig.

## Kontext
Der Tisch (600 x 500 x 220 mm, Alux 4040) bekommt vorn und hinten Schnittstellen:
- Rückseite: feste Anschlüsse (Netz, Netzwerk, USB, Erdung)
- Vorderseite: wechselnde Schnittstellen (Prüfspitzen, Analysewerkzeuge)

Zwischen den Pfosten der 600-mm-Seiten bleiben 520 mm lichte Breite. Auf den 500-mm-Seiten wären es nur 420 mm,
zu wenig für 19 Zoll (450 mm).

## Entscheidung
- Die **600-mm-Seiten sind Vorder- und Rückseite**.
- Pro Seite zwei senkrechte **2020-Nutprofile** als Rack-Schienen, Nutmitte im Abstand 465,1 mm
  (Lochabstand der 19-Zoll-Winkel), bündig mit der Rahmenaußenfläche. Lichte Weite zwischen den Schienen: 445,1 mm.
- Höhe: **3 HE** (133,35 mm) passt in die lichte Rahmenhöhe von 140 mm.
- Frontplatten aus Aluminium (482,6 x 133,35 mm, 3 mm), geerdet.
- Einbautiefe hinter der Platte: ca. 420 mm.

## Folgen
- Geräte mit mehr als ca. 440 mm Gehäusebreite passen nicht zwischen die Schienen. Für 450 mm lichte Weite
  wäre ein Nutabstand von 470 mm nötig; die Bohrungen der 19-Zoll-Winkel (465,1 mm) lägen dann 2,45 mm neben der Nutmitte.
- Netzseite nur durch Elektrofachkraft, siehe `SAFETY.md`.
- Offen: genaues 2020-Profil (Alux-Artikel mit 6-mm-Nut prüfen) und Ausschnittliste je Platte.
