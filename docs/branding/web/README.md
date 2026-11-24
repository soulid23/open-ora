# open-ora Logo für die Webseite

Alle Logos sind reine Vektorpfade (Schrift in Umrisse umgewandelt), sie brauchen keine installierte Schrift.

| Datei | Wofür |
|---|---|
| `open-ora-logo.svg` | Logo auf hellem Grund (Ink #16181B, Unterzeile #5B5E63) |
| `open-ora-logo-hell.svg` | Logo auf dunklem Grund (Off-White #F4F2EE, Unterzeile #C9C6C0) |
| `open-ora-favicon.svg` | Favicon (Zeichen auf dunklem Quadrat) |
| `open-ora-app-icon.svg` | App-Icon / Avatar (Zeichen auf Kupfer) |

## Einbinden

```html
<link rel="icon" href="/open-ora-favicon.svg" type="image/svg+xml">

<header class="site-header">
  <a href="/" class="logo" aria-label="open-ora Startseite">
    <img src="/open-ora-logo-hell.svg" alt="open-ora – offener Reparatur-Assistent" height="56">
  </a>
</header>
```

Mindestgröße: Logo nicht kleiner als 40 px hoch, sonst wird die Unterzeile unlesbar.
Darunter das Zeichen allein (`open-ora-favicon.svg`) verwenden.

## Farben

```css
:root {
  --ora-ink:    #16181B;
  --ora-light:  #F4F2EE;
  --ora-accent: #E8743B;
  --ora-grey:   #5B5E63;  /* Text auf Hell */
  --ora-grey-2: #C9C6C0;  /* Text auf Dunkel */
}
```

Schrift für Fließtext und Überschriften: Space Grotesk (Google Fonts oder `../fonts/`).

Neu erzeugen: `python docs/branding/tools/gen_logo.py` (Logo-SVGs) und
`python docs/branding/tools/gen_forex.py` (Druckvorlagen + `forex_layout.json` für das FreeCAD-Makro); benötigt `fontTools`.

## Webseite (www.open-ora.de)

`index.html` ist die Startseite, `.htaccess` leitet alles auf `https://www.open-ora.de` um
(nur hochladen, wenn das SSL-Zertifikat aktiv ist, wegen HSTS).

Auf den Server (Hetzner, Webroot) kommen:

```
/index.html
/.htaccess
/open-ora-logo-hell.svg
/open-ora-favicon.svg
/open-ora-tisch-v1.png             (Bild Tisch V1, aus docs/images/open-oratischV1.png)
/fonts/SpaceGrotesk-Medium.ttf     (aus docs/branding/fonts/)
/fonts/SpaceGrotesk-SemiBold.ttf   (aus docs/branding/fonts/)
```

Keine Google Fonts, keine Cookies, keine externen Inhalte (Datenschutz). Impressum und
Datenschutz stehen unten in `index.html`.
