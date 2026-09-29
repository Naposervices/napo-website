# 🚀 Performance-Optimierungen - Naposervices Katalog

## ✅ Implementierte Verbesserungen

### 1. **Timeout erhöht (10s → 30s)**
- Gibt mehr Zeit für große JSON-Dateien (927KB)
- Verhindert vorzeitige Timeouts bei langsamen Verbindungen

### 2. **Progress-Anzeige**
- Visueller Fortschrittsbalken zeigt Ladestatus
- Status-Updates: "Verbinde...", "Lade Daten...", "Verarbeite JSON...", "Fertig!"
- Prozentanzeige für besseres User-Feedback

### 3. **Besseres Error-Handling**
- Unterscheidet zwischen Timeout, Netzwerkfehler und JSON-Fehler
- Detaillierte Debug-Informationen (URL, Protokoll, Fehlertyp)
- Kontextspezifische Lösungsvorschläge
- Stack-Traces in der Konsole für Entwickler

### 4. **Browser-Cache**
- `cache: 'default'` nutzt Browser-Cache
- Schnelleres Neuladen beim zweiten Besuch
- Reduziert Server-Last

### 5. **RequestAnimationFrame**
- Lazy Loading verwendet jetzt `requestAnimationFrame()` statt `setTimeout()`
- Bessere Performance und flüssigere Animationen
- Synchronisiert mit Browser-Rendering-Zyklus

### 6. **Robustere JSON-Verarbeitung**
- Content-Type-Check warnt bei falschen MIME-Types
- Validierung der Katalog-Struktur
- Bessere Fehlerbehandlung mit Stack-Traces

### 7. **Sichere Produkt-Darstellung**
- `encodeURIComponent()` für JSON-Daten im HTML
- Verhindert XSS und Parsing-Fehler
- Null-Checks für alle Produkt-Eigenschaften:
  - `product.images?.length || 0`
  - `product.product_number || '#' + product.id`
  - `product.price_euro || '—'`

### 8. **Debug-Verbesserungen**
- Console-Logs mit Emojis für bessere Lesbarkeit:
  - 🚀 Starte Katalog-Laden
  - ✓ Response erhalten
  - 📦 Parse JSON
  - ❌ Fehler
- Detaillierte Statistiken beim erfolgreichen Laden
- Hilfreiche Fehlermeldungen mit Lösungsvorschlägen

## 📊 Performance-Metriken

- **Timeout**: 30 Sekunden (vorher 10s)
- **Lazy Loading Margin**: 100px (vorher 50px)
- **Intersection Threshold**: 0.01 für früheres Laden
- **Thumbnail Preload**: Nur 5 sichtbare Bilder

## 🔧 Technische Details

### Fehlertypen und Lösungen:

1. **Timeout-Fehler**
   - Prüfe Internetverbindung
   - Datei möglicherweise zu groß
   - Browser-Cache hilft beim zweiten Versuch

2. **Netzwerkfehler**
   - Öffne über `http://localhost:8000`
   - Nicht per Doppelklick (file://)
   - Server muss laufen: `python -m http.server 8000`

3. **JSON-Fehler**
   - catalog_master.json beschädigt
   - Datei neu generieren
   - Syntax-Fehler prüfen

## 🎯 Nächste Schritte

1. Seite über `http://localhost:8000` öffnen
2. Browser-Konsole (F12) öffnen für Debug-Info
3. Bei Problemen: Fehlermeldung und Console-Logs prüfen

## 📝 Hinweise

- Server läuft auf Port 8000
- Erste Ladung kann 2-5 Sekunden dauern
- Zweite Ladung ist dank Cache deutlich schneller
- Alle Bilder werden lazy geladen für bessere Performance

---

## 🆕 Update (September 2026): Echte Seiten, SEO, Suche & Filter

Die Seite war bisher eine einzige HTML-Datei ohne eigene URLs pro Ansicht - jeder
Klick hat nur den Inhalt ausgetauscht, die Adresszeile blieb immer gleich. Das ist
jetzt nachgerüstet, weiterhin als eine einzige `index.html` (kein Build-Prozess,
kein Server nötig - läuft unverändert auf GitHub Pages):

### 9. **Hash-Routing (echte, teilbare URLs)**
- Jede Ansicht bekommt jetzt eine eigene URL, z.B.:
  - `#/Kleidung` → Marken-Übersicht
  - `#/Kleidung/Nike` → Produkte dieser Marke
  - `#/Kleidung/Nike/123` → Produkt-Galerie direkt geöffnet
  - `#/suche?q=Nike` → Suchergebnisse
- Links lassen sich jetzt direkt teilen (z.B. per Telegram/Instagram-DM: "schau dir
  #/Kleidung/Nike an") und führen beim Öffnen direkt zur richtigen Ansicht.
- Der Zurück/Vorwärts-Button des Browsers funktioniert jetzt wie erwartet.
- Ein Reload der Seite bleibt auf der aktuellen Ansicht, statt auf die Startseite
  zurückzuspringen.
- Technisch über `location.hash` + `history.pushState`/`popstate` gelöst - braucht
  keine Server-Konfiguration und funktioniert damit 1:1 weiter mit GitHub Pages.

### 10. **SEO pro Seite**
- `<title>` und Meta-Description werden pro Marke/Kategorie/Suche dynamisch gesetzt
  (z.B. "Nike - Kleidung - Naposervices" statt immer nur "Naposervices").
- Open-Graph- und Twitter-Card-Tags werden mitaktualisiert, damit geteilte Links
  (Instagram/Telegram) eine sinnvolle Vorschau zeigen.
- `preconnect`/`dns-prefetch` zum R2-Bucket, damit Bilder & Katalog-JSON schneller
  laden.

### 11. **Suche & Preisfilter**
- Neues Suchfeld im Header (Produktnummer, Marke oder Kategorie), live mit 300ms
  Debounce - kein Netzwerk-Overhead, sucht direkt im bereits geladenen Katalog.
- Preisfilter (< 50€ / 50-100€ / 100-200€ / 200€+) sowohl in der Produktliste einer
  Marke als auch in den Suchergebnissen.
- Ergebnis landet in der URL (`#/suche?q=...&filter=...`), ist also auch direkt
  verlinkbar.

### 12. **Katalog-Cache (Stale-While-Revalidate)**
- Der Katalog wird jetzt zusätzlich in `localStorage` zwischengespeichert.
- Bei einem erneuten Besuch wird sofort die zwischengespeicherte Version gezeigt
  (kein Lade-Bildschirm mehr), während im Hintergrund lautlos auf neue Daten
  geprüft wird (Cache gilt 30 Minuten als "frisch").
- Schlägt der Hintergrund-Refresh fehl (z.B. kurzzeitig kein Netz), bleibt einfach
  die zwischengespeicherte Version sichtbar - kein Fehlerbildschirm.
- Kleiner Bugfix nebenbei: fehlgeschlagene Bild-Ladevorgänge beim Lazy Loading
  lösten bisher einen unbehandelten Promise-Fehler aus (sichtbar in der Konsole) -
  ist jetzt sauber abgefangen.

### Bekannte Einschränkung
- Die Routen sind reines Client-Side-Routing (Hash-basiert). Für Suchmaschinen wie
  Google, die JavaScript ausführen, funktioniert das gut; ein direkter `curl` auf
  `.../#/Kleidung/Nike` liefert aber immer die gleiche `index.html` zurück (das ist
  bei GitHub Pages ohne eigenen Server normal und für diese Seitengröße die
  pragmatischste Lösung).

## 🆕 Update (September 2026): Automatische Modell-Unterkategorien

Nachfrage: Marken wie Nike zusammenfassen zwar Hunderte Produkte, aber ohne
Aufteilung nach Modell (Air Force, Air Max 90/95/97 usw.) - manuell durchsuchen
war mühsam.

### Was geprüft wurde
Ein Blick in die echten Live-Daten (`catalogData`, direkt im Browser) zeigte:
kein Produkt hat ein echtes "Modell"-Feld. Es gibt nur ein grobes `category`-Feld,
das bei fast allen Marken nur der Markenname selbst ist. Das einzig nutzbare
Signal ist das rohe `name`-Feld (der ursprüngliche Angebotstitel vom Lieferanten,
z.B. `"380 ¥ EM batch Air Max 95 CI0999-600 40-47"`) - unübersichtlich, aber mit
genug Substanz für eine Texterkennung.

### Umsetzung
- Ein Regelwerk (`MODEL_RULES` in `index.html`) erkennt per Muster-Abgleich aus
  dem `name`-Feld, zu welchem Modell ein Produkt gehört - komplett im Browser
  berechnet, keine Änderung an der großen JSON-Datei nötig.
- Aktuell abgedeckt (gegen die echten Live-Daten getestet):
  - **Nike** (445 Produkte, Schuhe): 96% automatisch erkannt, 25 Modell-Gruppen
    (Air Force 1, Air Max 90/95/97/98/Plus(TN)/VaporMax, Dunk Low/High, Jordan,
    Kobe, Alphafly, Vomero, Pegasus, Shox, P-6000, Blazer, Cortez, Rover u.a.)
  - **New Balance** (199 Produkte): 98% erkannt, 17 Gruppen (530, 550, 574, 740,
    990-997, 1906, 2000, 2002R, 2010, 9060 usw.)
  - **Asics** (101 Produkte): 100% erkannt (Gel-Kayano 14, Gel-NYC, Gel-1130,
    Mexico 66, Metaspeed)
  - **Salomon** (26 Produkte): 100% erkannt (XT-6, XT-Q, XA Pro 3D)
  - **Hoka** (5 Produkte): 100% erkannt (Bondi, Hopara)
- Nicht erkannte Produkte landen sichtbar in einer "Weitere Modelle"-Gruppe am
  Ende - nichts wird versteckt oder geht verloren.
- Sortierung ist "natürlich"/numerisch (Air Max 90 vor 95 vor 97 vor 98, NB 530
  vor 990 vor 9060 usw.), nicht alphabetisch.
- Andere Marken mit demselben Namen in einer anderen Kategorie (z.B. "Nike" unter
  Kleidung) sind bewusst **nicht** betroffen - die Regeln sind pro
  Kategorie+Marke gebunden, nicht nur pro Markenname.

### Bewusst ausgeschlossen
Birkenstock (483 Produkte), UGG (45) und Veja (13) wurden geprüft, aber die
Produktnamen bestehen dort fast nur aus Preis + interner Bestellnummer (z.B.
`"￥225 BK-000045"`) ohne erkennbaren Modellnamen im Text - eine automatische
Zuordnung wäre bei über 90% der Produkte nur geraten. Für diese Marken bleibt es
bei der normalen Produktliste, bis es eine bessere Datenquelle gibt (z.B. eine
Style-Code-zu-Modell-Tabelle).

### Wie man weitere Marken/Modelle hinzufügt
In `index.html` nach `const MODEL_RULES = {` suchen. Unter `Schuhe: { ... }` eine
neue Marke mit einer Liste aus `[Regex, "Anzeigename"]`-Paaren ergänzen -
Reihenfolge ist wichtig (spezifischere Muster zuerst). Am besten vorher ein paar
echte `name`-Werte der Marke ansehen (Browser-Konsole: `catalogData.categories.
Schuhe.<Marke>.map(p => p.name)`), um passende Muster zu finden.
