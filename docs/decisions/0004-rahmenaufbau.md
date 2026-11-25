# 0004: Rahmenaufbau, Pfosten als Füße

Status: angenommen als Bauprinzip (obere Ebene über die volle Breite, Pfosten als Füße), **Maße ersetzt durch
`0006-tisch-1x1-verstrebung.md`**.

> **Stand heute (ADR 0006, Tisch Version 1):** 1000 x 1000 mm, Oberkante ESD-Matte 740 mm, Pfosten 630 mm mit
> eingeschraubten Gelenkstellfüßen, Zuschnitte 4040: 2 x 1000, 10 x 920, 4 x 630, 6 x 283,6 mm (siehe `bom/frame_bom.csv`).
> Die Maße unten gehören zum früheren Tisch 600 x 500 mm.

## Entscheidung
- **Obere Ebene**: Die langen X-Träger (600 mm) liegen vorn und hinten über die komplette Breite,
  die Y-Träger (420 mm) sitzen dazwischen.
- **Untere Ebene**: Alle Träger enden an den Pfosten: X 520 mm, Y 420 mm.
- **Pfosten** (4 Stück) laufen vom Boden bis unter den oberen Rahmen und dienen unten als **Füße**
  (Parameter `FOOT_H`, derzeit 40 mm, darunter Stellfüße).
- Rack-Raum zwischen den Ebenen: 3 HE (siehe `0002`).
- Pfostenlänge 214,4 mm, Rahmenoberkante 254,4 mm über dem Boden, Platte oben ca. 268 mm (mit ESD-Matte).

## Zuschnitt Alux 4040
2 x 600, 2 x 520, 4 x 420, 4 x 214,4 mm. Gesamt ca. 4,78 m, ca. 6,7 kg.
