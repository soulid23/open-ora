# 0003: Rack-Einbauten von Adam Hall und Neutrik

Status: angenommen (Teilenummern und Maße vor Bestellung gegen Datenblatt/2D-Zeichnung prüfen)

## Entscheidung

| Einheit | Hinten | Vorn |
|---|---|---|
| 3. HE (oben) | Adam Hall **RACK U PAN 01 D12 TIE BAR** (872215) | gleiche Blende |
| 2. HE | frei | frei |
| 1. HE (unten) | Adam Hall **RACK TRAY 01 PULLOUT** (87556), Auszugschublade | frei |

**Blende 872215**: 1 HE, U-förmig, Stahl 1,5 mm, pulverbeschichtet, 484 mm breit, 12 D-Löcher (ca. 24 mm),
integrierte Zugentlastungsleiste mit Kabelbindern.

**Schublade 87556**: 1 HE, Stahl 1,6 mm, Vollauszug, Traglast 25 kg, nutzbare Fläche ca. 412 x 380 mm,
Einbautiefe 360 bis 480 mm einstellbar. Die Schublade wird hinten an den hinteren Schienen und an den vorderen Schienen befestigt.

### Belegung der hinteren D12-Blende (Blick von hinten, von links)
1. Neutrik **powerCON blau** (IN, Netzeingang)
2. Neutrik **powerCON weiß** (OUT, Netzausgang)
3. Netzwerkdurchführung (Cat, etherCON-Familie)
4 bis 12: Blindkappen

### Belegung der vorderen D12-Blende
1 bis 12: Blindkappen, später Kleinspannungsanschlüsse (BNC, USB, XLR D-Serie nach Bedarf)

## Hinweise
- **Neutrik**: D-Format mit genormtem 24-mm-Ausschnitt, Plattenstärke 1 bis 3 mm, Befestigung mit M3.
  Zu den Produkten gibt es DXF-Dateien. Blindkappen z. B. Neutrik DBA-BL (Abdeckplatte für D-Ausschnitte).
- **Pulverlack isoliert.** Die Neutrik-Metallgehäuse sollen über die Blende an PE liegen: Kontaktstellen blank
  machen oder Zahnscheiben verwenden, Durchgang messen (Elektrofachkraft, siehe `SAFETY.md`).
- **powerCON OUT** führt Netzspannung. Absicherung, Berührungsschutz und die Frage, ob das Trennen unter Last
  zulässig ist, klärt die Elektrofachkraft anhand des Neutrik-Datenblatts.
- Die Teilenummern der Neutrik-Einbauteile sind im Makro nur als Beispiele eingetragen und noch zu bestätigen.
- Offen: genauer Lochabstand der 12 D-Löcher (aus der 2D-Zeichnung 872215), Lochbild der Ohren,
  Körpermaße der Schublade (2D-Zeichnung 87556). Die Werte im Modell sind Platzhalter.
