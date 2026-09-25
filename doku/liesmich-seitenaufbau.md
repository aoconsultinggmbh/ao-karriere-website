---
titel: LIESMICH — Karriereseite ao-karriere.de, Entwurf v2.2
kategorie: Projekt-Output
kurzbeschreibung: Was gebaut wurde, woher die Bausteine kommen, was geprüft ist und was noch offen ist.
schlagworte: [Karriereseite, ao-karriere.de, Landeseite, Bewerbungsformular, Wistia]
stand: 2026-09-25
erstellt-von: Claude auf Anweisung Ovidiu
---

# Karriereseite ao-karriere.de, Entwurf v2.2

Eine einzelne HTML-Landeseite. `index.html` ist die gesamte Seite, alles andere sind
Bausteine. Öffnen per Doppelklick geht, besser ist ein kleiner Server im Ordner
(`python3 -m http.server 8790`), weil Schriften und Formular über `file://` anders laufen.

## Was drauf ist

| Abschnitt | Inhalt |
|---|---|
| Hero | „Du musst nichts mitbringen außer dem Willen, es zu können", drei Punkte, zwei Knöpfe, rechts der Recruitingfilm `nvkmwnlpvt` mit der kununu-Karte davor. Kein Gesichterband mehr |
| Elf Leute | Kultur in drei Blöcken, Bildmosaik mit zwei Zahlenkacheln |
| Frag nicht uns | drei Videos aus dem Team, die im Band von selbst laufen: Alexandra `3u6zmzx7uz`, Daniel `gfxc0jyl38`, Nicole `aec9aik5se` |
| Neun Dinge | die neun Benefits der heutigen Seite, ausformuliert |
| Drei Wege zu uns | die drei offenen Stellen, jede mit eigenem Bewerbungsknopf |
| Drei Schritte | Unterlagencheck, Telefonat, Kennenlernen, mit der Zusage „48 bis 72 Stunden", daneben ein Bild aus dem Büro |
| Vier Dinge, die du dir sparen kannst | die Bewerbungstipps, umgedreht formuliert |
| Häufige Fragen | sieben Fragen, davon eine mit Ortsbezug. Öffnungszeiten stehen erst drin, wenn sie in `stellen-daten.py` eingetragen sind |
| Bewerben | Formular mit Dateianhang |

## v2.2, Nachtrag: Feed für Talent.com

Zusätzlich zu `indeed.xml` schreibt der Generator `talent.xml`, Aufbau nach dem
Integration Guide von Talent.com. Gleiche Stellen, gleiche Beschreibung, dazu ein Logo als
PNG in 128 × 128 (`img/ao-consulting-logo-128.png`). Keine Angabe `cpc`, das wäre bezahlte
Platzierung. Eine Talent-Pool-Markierung wie bei Indeed kennt Talent.com nicht, die gelben
Stellen stehen deshalb normal drin.

Monster.de ist seit Ende Juli 2025 für Arbeitgeber in Deutschland abgeschaltet und fällt
als Kanal weg.

## v2.2 vom 25.09.2026: Schnittstelle zu Indeed

Der Generator schreibt bei jedem Lauf zusätzlich `indeed.xml`. Das ist der Weg, den Indeed
für Arbeitgeber ohne eigenes Bewerbermanagement-System vorsieht: Indeed holt die Datei von
einer festen Adresse ab, laut Indeed viermal am Tag. Eine neue oder geänderte Stelle in
`stellen-daten.py` landet damit ohne Handarbeit bei Indeed.

- Aufbau nach der Vorgabe von Indeed (docs.indeed.com, Job Sync XML Feed): Titel, Datum,
  Kennung, Adresse der Stellenseite, Firma, Ort mit Straße und PLZ, Kontaktadresse,
  vollständige Beschreibung als HTML, Vollzeit oder Teilzeit, Ablaufdatum, Kategorie.
- Die Beschreibung ist dieselbe wie für Google for Jobs.
- Bewerbungen laufen weiter über unser Formular: Indeed verlinkt auf die Stellenseite, die
  Bewerbung kommt an jobs@ao-karriere.de.
- **Gelbe Stellen stehen im Feed, sind aber als `TALENT_POOL` markiert.** Indeed verlangt einen
  vollständigen Feed und schreibt ausdrücklich, dass Stellen, die nur Bewerber für später
  sammeln, nicht in der Suche erscheinen sollen. Anders als bei Google gibt es hier also
  einen vorgesehenen Weg. Der Schalter heißt `INDEED_GELB_ALS_TALENTPOOL`.
- Besetzte Stellen fehlen im Feed.

## v2.1 vom 25.09.2026: SEO- und GEO-Prüfung, Route planen

Die ganze Prüfung steht in `doku/seo-geo-pruefung-2026-09-25.md`. Umgesetzt ist, was
keine Entscheidung braucht: kürzere Seitentitel der Stellen, Beschreibung ohne fehlenden
Punkt, `JobPosting` beginnt mit der Stelle, Anforderungsfelder „no requirements" dort, wo
der Text es hergibt, echtes Änderungsdatum in der Sitemap, „Route planen" als Verweis auf
Google Maps an drei Stellen. Der Umbruch „mitbrin-gen" in der großen Zeile ist behoben.

Entschieden von Ovidiu: alle drei Stellen werden weiter an Google gemeldet (Risiko bewusst
in Kauf genommen), die kleine Zeile ist jetzt die H1 mit Region, Backoffice heißt
„Kaufmännische Assistenz im Backoffice (m/w/d)", Webdesign „Webdesigner WordPress (m/w/d)",
kein Gehalt. Einzelheiten in der SEO-Prüfung.

## v2.0 vom 25.09.2026: Telefon Pflicht, richtige Rechtsseiten, Gleichstellungshinweis

### Telefon ist Pflichtfeld

Vorgabe Ovidiu. Das Feld trägt ein Sternchen und `required`, darunter steht bei leerem
Feld „Bitte gib eine Telefonnummer an, damit wir Dich anrufen können." Browser und
`bewerbung.php` verlangen mindestens sechs Ziffern, damit ein Leerzeichen oder ein Strich
nicht durchgeht. Geprüft: leer und „12-3" werden abgewiesen, „0176 1234567" geht raus.

### Datenschutz und Impressum der Karriereseite

Alle Verweise zeigten auf die Rechtsseiten der Agentur (`ao-consult.de`). Sie zeigen jetzt
auf die der Karriereseite, so wie sie im Fuß der heutigen ao-karriere.de stehen:
`https://ao-karriere.de/datenschutzerklaerung/` und `https://ao-karriere.de/impressum/`.
Betroffen waren Fuß, Einwilligungsbanner, Hinweise bei Videos und kununu sowie die
Einwilligung im Formular.

**Beim Livegang beachten:** Diese beiden Seiten liegen heute im WordPress. Wird es
abgeschaltet, müssen sie vorher als eigene Dateien in den neuen Auftritt, sonst laufen die
Verweise ins Leere.

### Gleichstellungshinweis

Neue Unterseite `rechtliches/hinweis-zur-gleichstellung.html`, der Text ist wortgleich von
der heutigen Seite übernommen. Verlinkt im Fuß jeder Seite neben Impressum und Datenschutz.
Beim Livegang die alte Adresse `/hinweis-zur-gleichstellung/` auf die neue Datei umleiten.
Der Generator erzeugt die Seite bei jedem Lauf mit, das Prüfskript prüft sie mit.

## v1.9 vom 25.09.2026: Stellenseiten überarbeitet, Admir für den Vertrieb

### Ansprechpartner je Stelle

**Vorgabe Ovidiu:** Für alle Vertriebsstellen ist Admir Renz der Ansprechpartner, für alle
anderen Stellen Ovidiu Rieger. In `stellen-daten.py` stehen beide unter `PERSONEN`, jede
Stelle trägt ein Feld `bereich`, und `ANSPRECHPARTNER_NACH_BEREICH` ordnet `vertrieb` Admir
zu. Die Karte rechts und der Kasten neben dem Formular folgen dieser Regel. Startseite und
Kontaktband bleiben bei Ovidiu.

**Offen:** Für Admir fehlen Telefonnummer und WhatsApp. Sie stehen nirgends in den
Projektdateien. Bis sie eingetragen sind, zeigt seine Karte nur die Mailadresse, und der
Generator meldet das bei jedem Lauf.

### Stellenseiten

| Rückmeldung Ovidiu | Umsetzung |
|---|---|
| Bilder viel zu groß | flaches Band 12 zu 5 statt 3 zu 2, 864 × 360 px statt 864 × 576. Jede Stelle hat einen eigenen Bildausschnitt (`bild_fokus`), damit keine Köpfe abgeschnitten werden |
| Vertrieb: Köpfe wieder angeschnitten, Bild von Dennis nehmen | Vertrieb zeigt jetzt Dennis im Profil am Telefon. Das Backoffice, das bisher dieses Bild hatte, zeigt die Abstimmung am Tablet |
| Stellentitel übertrieben groß | 37,6 statt 59 px bei 1512. Die Formularüberschrift hat dieselbe Größe bekommen, sie war sonst größer als der Titel |
| Mal volle Breite, mal weniger, Schriften unterschiedlich | Absätze und Listen laufen bis zur gleichen Kante und haben dieselbe Schriftgröße (17 px) und Farbe. Der Inhalt der Stellenseiten hat 1240 px Breite, Kopf und Fuß bleiben wie auf der Startseite |
| Überschriften mit einer Unterstreichung hervorheben | dieselbe blaue Markierung wie auf der Startseite unter „Über uns", „Aufgaben", „Qualifikationen", „Das bieten wir" |
| Formular soll an die Stelle gebunden sein | kein Auswahlfeld mehr. Unter „Deine Bewerbung" steht fest „für …", die Stelle geht als verstecktes Feld mit. Bei Stellen auf Gelb steht in der Mail „(Initiativbewerbung)" dahinter |

### Die Ampel war auf den Stellenseiten grau

Die Farben hingen an `.stelle[data-status]`, der Karte in der Liste. Auf der Unterseite
heißt der Behälter `.stelle-seite`, deshalb blieb die Ampel dort grau. Beide Selektoren
stehen jetzt in `stellen-ampel.css`.

**Eigener Fehler dabei:** Beim ersten Versuch waren die Selektorlisten falsch
zusammengesetzt, und die Puls-Animation des Ampelpunkts traf die Stellenkarte selbst. Die
Startseite scrollte dadurch seitlich. Die Prüfung hat es sofort gemeldet, korrigiert.

### FAQ

Die Antwort zur Initiativbewerbung verwies auf die Auswahl „Initiativbewerbung" im
Formular, die es nicht mehr gibt. Sie nennt jetzt die Stellen mit gelbem Punkt, die
Mailadresse und das Telefon.

## v1.8 vom 25.09.2026: kompakte Stellenliste, Köpfe wieder ganz

### Köpfe im Mosaik

Seit die Seite breiter ist, waren die Kacheln bei fester Höhe von 230 px sehr quer
geworden, und bei den Hochformat-Fotos fielen oben die Köpfe weg. Die Kacheln wachsen jetzt
im Verhältnis 4 zu 3 mit (342 × 260 px bei 1512, 379 × 288 bei 1920). Die drei
Hochformat-Fotos haben dazu einen eigenen Bildausschnitt, der auf die Köpfe zielt.

### Stellenliste ohne Bilder

Drei Stellen füllten fast eine ganze Bildschirmseite, und in den schmalen Bildspalten der
Karten waren ebenfalls Köpfe angeschnitten. Die Karten zeigen jetzt nur noch den Status,
den Titel, einen Satz und den Knopf. Sie stehen nebeneinander, ab 1024 px alle drei in
einer Reihe. Die Liste ist bei 1512 px 297 px hoch statt gut 1100. Die Aufgaben und das
Bild stehen weiter auf der jeweiligen Stellenseite.

Die Etiketten „Bruchsal" und „Vollzeit" standen auf jeder Karte und zugleich im Satz
darüber. Der Generator zeigt ein Etikett für den Umfang jetzt nur noch, wenn sich die
Stellen darin unterscheiden. Der Einleitungssatz entsteht ebenfalls aus den Daten.

### ⚠️ „unbefristet" war nicht belegt

Im Einleitungssatz stand „Alle Stellen sind in Bruchsal, in Vollzeit und unbefristet". In
den Stellendaten steht nichts zu einer Befristung, auf der heutigen Seite nur „Vollzeit,
ab sofort". Das Wort ist raus. Der Satz verweist stattdessen auf die Zusage, die belegt
ist: Antwort in 48 bis 72 Stunden.

## v1.7, Nachtrag vom selben Tag: Breite, Reihenfolge, PDF, kununu

| Rückmeldung Ovidiu | Umsetzung |
|---|---|
| Seite soll mehr Bildschirmbreite nutzen | Inhaltsbreite von 1240 auf 1560 px, nur auf der Karriereseite. Der Rand wächst mit: 24 px auf dem Handy, 48 px bei 1512, 180 px bei 1920. Lesetexte bleiben schmal |
| „Fehler sind eingeplant" ist keine gute Überschrift | jetzt „Niemand muss perfekt anfangen" |
| Sätze klingen gesetzlich | Urlaub: „Sechs Wochen im Jahr. Genug, um auch mal richtig wegzufahren." Fahrtkosten: „Zum Weg nach Bruchsal legen wir etwas dazu. Was genau, sagen wir Dir im Gespräch." |
| Ansprechpartner gehört nach die Stellen | Kontaktband steht jetzt direkt nach den Stellen. Damit nicht zwei dunkle Abschnitte aneinanderstoßen, kommen danach die Tipps (hell), dann die drei Schritte (dunkel), dann die Fragen |
| Grundsätzlich PDF | Tipp „Die Formatfrage" bittet um PDF und nennt den Weg vom Handy. Formular, Prüfung im Browser und `bewerbung.php` nehmen nur noch PDF. Der Server prüft zusätzlich, ob die Datei wirklich mit `%PDF-` beginnt, eine umbenannte Word-Datei kommt nicht durch |
| WhatsApp-Icon verschwindet beim Hover | Das Icon war WhatsApp-grün, der Knopf beim Hover auch. Jetzt wird es beim Hover weiß, in der Ansprechpartner-Karte der Stellenseiten und im Kontaktband |
| kununu-Banner wie im Einbettungscode | Verweis mit den Kennungen aus dem Code von kununu und `rel="nofollow noopener"`. Auf der Startseite steht das Banner jetzt in der Karte vor dem Film, auf den Stellenseiten wie bisher rechts |

### kununu und die Einwilligung

Das Banner ist ein Bild vom Server von kununu, beim Laden geht die IP-Adresse dorthin. Es
steht deshalb weiter hinter der Einwilligung: vorher die eigene Karte mit 4,9 von 5,0,
nach „Alles erlauben" das echte Banner. Ohne Einwilligung ginge es nur mit einer örtlichen
Kopie der Grafik. Der Abruf ist aus dieser Arbeitsumgebung gesperrt (Proxy 403), die Datei
müsste also einmal von Hand heruntergeladen und in `img/` gelegt werden.

### Zwei eigene Fehler beim Einbau

Die alte Regel `.hero-hell__bild img` für das frühere Hero-Foto traf jetzt auch das
kununu-Banner und schnitt es auf 3 zu 2 zu. Sie gilt jetzt nur für `picture img`. Und die
eigene Karte blieb nach dem Laden stehen, weil `display:grid` das `hidden`-Attribut
schlägt. Dieselbe Falle steckte auf den Stellenseiten in `stelle.css`. Beide Stellen
haben jetzt `[hidden]{display:none}`.

## v1.7 vom 25.09.2026: Zahlen stimmen wieder, doppelte Bilder raus

### Zwei Bilder waren dasselbe Motiv

Im Mosaik standen `erstgespraech-im-buero` und `praxisauftritt-abstimmung` nebeneinander.
Das ist derselbe Moment, nur unterschiedlich beschnitten, und im engeren Ausschnitt war
der Kopf der stehenden Person oben abgeschnitten. Der enge Ausschnitt ist überall durch
den vollständigen ersetzt und liegt jetzt in `img/_unbenutzt/`.

Bei der Gelegenheit ist die ganze Seite auf doppelte Bilder durchgegangen worden. Drei
Bilder standen zweimal da, weil die Stellenkarten dieselben Fotos nutzten wie das Mosaik.
Das Mosaik hat jetzt acht Kacheln statt zehn, das ergibt zwei saubere Viererreihen, und
**jedes sichtbare Bild der Startseite kommt genau einmal vor.** Ein Prüfschritt zählt das
nach.

### Die Zahlen im Text kommen jetzt aus den Daten

Oben stand „Drei offene Stellen ansehen" und darunter „Drei Wege zu uns, alle drei offen".
Offen ist aber nur eine Stelle, die beiden anderen stehen auf Gelb. Diese Sätze standen
fest im HTML und wären bei jeder Statusänderung wieder falsch geworden. `bauen-stellen.py`
schreibt sie jetzt bei jedem Lauf aus `stellen-daten.py`:

| Lage | Knopf oben | Überschrift |
|---|---|---|
| keine Stelle aktiv | Initiativ bewerben | Gerade keine Stelle offen, initiativ geht immer |
| genau eine aktiv | Die offene Stelle ansehen | Eine Stelle ist offen, initiativ geht immer |
| mehrere aktiv | Drei offene Stellen ansehen | Drei offene Stellen, dazu jederzeit initiativ |

Der Einleitungssatz der Stellensektion zählt ebenfalls aus den Daten, wie viele auf Gelb
stehen.

### ⚠️ Eine Behauptung im FAQ war nicht belegt

Im FAQ stand: „Zwei der drei aktuell ausgeschriebenen Stellen sind aus Initiativbewerbungen
entstanden." In der Bestandsaufnahme steht nur, dass zwei der drei Stellen den **Status**
initiativ tragen. Das ist etwas anderes, und über die Herkunft der Mitarbeitenden sagt es
nichts. Der Satz ist raus. Wenn er stimmt, kann er zurück, dann aber als bestätigte Angabe.

### Fahrtkostenzuschuss

Die Kachel „Fahrtkostenzuschuss" trug den Text „Dazu Kaffee, Wasser, Cola Zero, Paulaner
Spezi, Obst und Süßes im Haus." Das passte weder zur Überschrift noch zur Einleitung der
Sektion, die ausdrücklich „keine Obstkorb-Poesie" verspricht. Der Text lautet jetzt: „Der
Weg nach Bruchsal wird bezuschusst. Die Höhe besprechen wir beim Kennenlernen." **Bitte
prüfen**, ob das so stimmt.

### Gesichterband raus

Von Iwan gibt es kein Foto, zehn von elf Gesichtern wären falsch gewesen. Das Band unter
dem Hero ist entfernt, der Hero hat dafür unten eine eigene Fußhöhe bekommen. Die zehn
Porträts bleiben im Bilderordner, für den Fall, dass das elfte dazukommt.

### Daniel

Im Videoband steht bei Daniel jetzt „Leitung Vertrieb" statt „Vertrieb".

## v1.6 vom 24.09.2026: der Film steht oben, die eigene Videosektion entfällt

Ovidiu wollte den Recruitingfilm dort haben, wo im Hero bisher das Bild mit der
Sternebewertung stand. Genau da sitzt er jetzt, im gleichen Rahmen, 16 zu 9 statt 3 zu 2,
weil das Videoformat so ist und sonst schwarze Balken entstünden. Er läuft nach der
Einwilligung von selbst, stumm und in Schleife, wie die drei Filme im Karussell. Die
kununu-Karte mit den Sternen bleibt davor, sie ist nur weiter aus dem Rahmen gerückt,
damit sie keine Gesichter verdeckt.

Der Abschnitt „So sieht ein Tag bei uns aus" ist damit überflüssig und komplett raus.
Die Seite hat jetzt acht statt neun Abschnitte und wird oben schneller konkret.

### Wohin die freigewordenen Bilder gegangen sind

| Bild | vorher | jetzt |
|---|---|---|
| `ao-consulting-team-bruchsal-zusammenarbeit` | im Hero und im Mosaik | neben den drei Schritten, der Abschnitt hatte vorher gar kein Bild |
| `ao-consulting-gruender-im-buero-bruchsal` | ungenutzt | an der frei gewordenen Stelle im Mosaik |
| `ao-consulting-erstgespraech-im-buero` | Vorschaubild des Films und im Mosaik | bleibt im Mosaik und auf den Stellenseiten |

Kein Bild steht dadurch zweimal auf derselben Seite. Neben dem Bild wäre für drei
Spalten kein Platz, deshalb stehen die drei Schritte dort untereinander statt nebeneinander.

### Eine Änderung an der gemeinsamen `skript.js`

`skript.js` verdrahtete bisher stur das erste `.video__box` einer Seite mit dem
Vorschaubild-Verhalten. Auf der Karriereseite ist das jetzt der Hero-Film, der von selbst
laufen soll. Der Selektor heißt deshalb `.video__box:not([data-eigen])`, und alle vier
Kästen dieser Seite tragen `data-eigen`. Für die Hauptseite ändert sich nichts, dort gibt
es kein `data-eigen`.

## v1.5 vom 24.09.2026: die Videos laufen, kein Vorschaubild mehr

### Was Ovidiu wollte

Kein Standbild, vor das man klicken muss. Der Wistia-Rahmen soll direkt dort sitzen
und das Video im Hintergrund laufen. Die Namen der Leute stehen einfach darunter.

### Was jetzt passiert

| Vorher | Jetzt |
|---|---|
| Vorschaubild, darauf ein Knopf „Video abspielen" | der Wistia-Rahmen sitzt direkt im Feld |
| Video startet erst nach einem Klick | Video läuft stumm und in Schleife, ohne Bedienleiste |
| Name über dem Video | Name unter dem Video |
| ein Bild je Karte, alle gleich still | die mittlere Karte und die beiden Nachbarn laufen |

Der Rahmen bekommt `autoPlay=true`, `muted=true` und `endVideoBehavior=loop`, dazu
sind Bedienleiste, Abspielknopf, Vollbild und Einstellungen abgeschaltet. Das ist die
Hintergrundfilm-Einstellung von Wistia. Ton gibt es erst, wenn jemand wirklich
hineinklickt.

### Höchstens drei Videos gleichzeitig

Das Karussell legt für die Schleife Kopien der Karten an, insgesamt neun Felder. Neun
laufende Videos wären unsinnig. Deshalb bespielt das Skript nur die Mitte und die
beiden direkten Nachbarn. Wer weiterklickt, bekommt den Rahmen an der neuen Stelle,
und der Rahmen, der aus dem Blick rückt, wird entfernt. Es sind also immer höchstens
drei, egal wie oft man klickt.

### Die Einschränkung, die bleibt

Vor der Einwilligung darf keine Anfrage an Wistia gehen, das ist § 25 TDDDG und die
Planet49-Entscheidung des EuGH. Solange niemand zugestimmt hat, steht in der mittleren
Karte deshalb weiter der Ladeknopf. Erst mit der Zustimmung laufen die Videos, und dann
sofort und ohne weiteren Klick. Wer will, dass der Film vom ersten Moment an für jeden
läuft, muss die Videodateien selbst auf den eigenen Server legen. Dann ist es kein
fremder Dienst mehr und die Einwilligung entfällt. Das ist der einzige saubere Weg.

### Pfeile auf dem Handy

Bei 390 px saßen die Pfeile auf dem Video und haben das Gesicht verdeckt. Unter 640 px
stehen sie jetzt unter dem Video und bilden mit den Punkten eine Bedienzeile.

### Prüfskript liegt jetzt im Projekt

`werkzeug/pruef-karriere.js` prüft die Startseite und alle Stellenseiten in neun
Breiten: eine h1, keine Lücke in den Überschriften, jedes Bild mit alt, keine toten
Sprungmarken, Anrede durchgehend groß, kein Querscrollen, keine Skript- und
Konsolenfehler, vor der Einwilligung kein fremder Host, und auf den Stellenseiten die
Pflichtfelder von `JobPosting` samt `BreadcrumbList`. Vorher im Ordner
`python3 -m http.server 8321` starten, dann `node werkzeug/pruef-karriere.js website`.

## v1.4 vom 21.09.2026: Karussell wie auf der heutigen Seite, kununu-Siegel

### Karussell statt Reihe

Ovidiu hat einen Ausschnitt der heutigen Karriereseite geschickt: die mittlere Karte groß
in der Mitte, die Nachbarn links und rechts als kleine Vorschau angeschnitten, Pfeile
außen, Punkte darunter, der Name über dem Video. Genau so ist es jetzt gebaut.

| Vorher | Jetzt |
|---|---|
| drei gleich große Karten nebeneinander | eine große in der Mitte, zwei als Vorschau daneben |
| Pfeile nur bei Platzmangel | Pfeile immer, außen am Rand |
| keine Positionsanzeige | drei Punkte, der aktuelle breiter und blau |
| Name unter dem Video | Name über dem Video, „Alexandra, Marketing" |

**Die Schleife entsteht aus Kopien.** Damit links vom ersten Feld nicht einfach nichts
steht, legt das Skript je eine Kopie der Reihe davor und dahinter an. Kommt das Scrollen
in einer Kopie zur Ruhe, springt es unsichtbar zurück in die Mitte. Die Kopien tragen
`aria-hidden` und `inert` und haben `tabindex="-1"` auf allen Bedienelementen, für
Tastatur und Screenreader existieren sie also nicht. Sonst zählte jedes Video dreimal.

Gescrollt wird weiterhin echt, die Pfeile schieben nur. Wischen auf dem Handy, Tastatur
und Screenreader funktionieren damit ohne Zusatzarbeit.

### kununu-Siegel, aber hinter dem Einwilligungstor

Das Siegel liegt auf `widgets.kununu.com` und überträgt beim Laden die IP-Adresse des
Besuchers dorthin. Ungefragt eingebunden widerspräche das dem QA-Standard und der eigenen
Datenschutzerklärung. Deshalb:

1. Vor der Einwilligung steht die Bewertung als eigener Baustein da, mit Note,
   Weiterempfehlung und Verweis auf das Profil. Kein fremder Aufruf, nachgemessen.
2. Daneben ein Knopf „Siegel von kununu laden" mit dem Hinweis, was dabei passiert.
3. Nach der Einwilligung, über den Knopf oder über das Banner, erscheint das echte Siegel.
4. Lädt es nicht, bleibt der eigene Baustein stehen. Kein Loch in der Seite.

kununu steht dafür als eigener Dienst in der Einwilligung, mit Anbieter, Zweck, Art der
Verarbeitung und Dauer.

**Der einfachere Weg ohne Tor:** die Grafik einmal herunterladen, unter `img/` ablegen und
in `stellen-daten.py` bei `KUNUNU['widget']` den örtlichen Pfad eintragen. Dann ist es kein
fremder Aufruf mehr und das Tor entfällt. Der Preis: die Note aktualisiert sich nicht von
selbst. Aus dieser Umgebung heraus ging der Download nicht, `widgets.kununu.com` ist hier
gesperrt.

### Ein Fehler, den erst die Konsole zeigte

Die unscharfe Füllung hinter den Porträts steckte zuerst in einer CSS-Variablen
(`--poster:url(img/…)`). Eine Adresse in einer Variablen wird aber gegen die **Stilvorlage**
aufgelöst, nicht gegen die Seite. Daraus wurde `assets/img/…`, und drei Bilder liefen ins
Leere: drei 404 in der Konsole, sichtbar war davon nichts. Die Füllung ist jetzt ein echtes
`<img>`, dessen Adresse gegen die Seite aufgelöst wird und die der Generator für die
Unterseiten ohnehin umschreibt.

## v1.3 vom 21.09.2026: Band statt Raster, Anrede groß, erfundene Öffnungszeiten raus

### Die drei Videos laufen jetzt als Band

Vorher ein starres Dreier-Raster mit quadratischen Vorschaubildern. Zwei Fehler steckten
darin: das geladene Video ist 16 zu 9, das Feld war 1 zu 1, also sprang die Kachel beim
Laden von quadratisch auf länglich. Und bei wenig Platz brachen die drei Felder um, statt
nebeneinander zu bleiben.

Jetzt ein Band, wiederverwendbar für jede Karriereseite:

```
<div class="band" data-band>
  <button data-band-zurueck hidden>…</button>
  <ul class="band__spur" data-band-spur><li class="band__feld">…</li></ul>
  <button data-band-vor hidden>…</button>
</div>
```

Es scrollt **echt**, nicht per Umrechnung. Damit bleiben Wischen auf dem Handy, Tastatur
und Screenreader ohne Zusatzarbeit erhalten, die Pfeile schieben nur. Passt alles
nebeneinander, verschwinden die Pfeile und es wird nicht gescrollt. Gemessen: bei 1440 und
1100 px passen alle drei, ab 820 px erscheinen die Pfeile und das Band rückt um genau ein
Feld weiter.

**Das Vorschaubild wird nicht mehr beschnitten.** Die Porträts sind quadratisch, das
Videofeld ist 16 zu 9. Ein Zuschnitt auf 16 zu 9 hat die Gesichter zerstört, im Entwurf
sahen alle drei gleich aus. Jetzt steht das Porträt vollständig in der Mitte und eine
unscharfe Kopie desselben Bildes füllt die Ränder.

### Anrede groß

Regel von Ovidiu vom 21.09.: **Du, Dich, Dir, Dein** und alle Beugungen werden groß
geschrieben. Umgesetzt mit `werkzeug/anrede-gross.py`, das nur sichtbaren Text und die
Inhalte von `alt`, `title`, `aria-label`, `placeholder` und `content` anfasst. Tags,
Adressen, Klassennamen, Skripte und Stilvorlagen bleiben unberührt, sonst wird aus einem
Verweis schnell ein toter Verweis. Bei neuen Texten mitlaufen lassen:

```
python3 ../werkzeug/anrede-gross.py index.html ../werkzeug/formular.html ../werkzeug/stellen-daten.py
```

### ⚠️ Erfundene Öffnungszeiten in der FAQ

In der FAQ-Antwort mit dem Ortsbezug stand: „Das Büro ist montags bis donnerstags von
08:00 bis 17:30 Uhr und freitags von 08:00 bis 16:00 Uhr besetzt." **Diese Zeiten sind
erfunden.** Sie stammen aus dem Skill `ao-schreibstil`, wo „Mo–Do 08:00–17:30 Uhr" und
„Fr 08:00–16:00 Uhr" als Beispiel dafür stehen, wann ein Bis-Strich erlaubt ist. Ich habe
eine Illustration aus einer Schreibregel als Tatsache übernommen. Ovidiu hat es gemeldet,
die Zeiten stimmen nicht.

Behoben und abgesichert: Die Zeiten stehen jetzt als Feld `oeffnungszeiten` in
`stellen-daten.py`, derzeit auf `None`. Der Generator setzt sie in die FAQ-Antwort ein und
lässt den Satzteil weg, solange nichts eingetragen ist. Er weist bei jedem Lauf darauf hin.
Sobald die echten Zeiten feststehen, ist es eine Zeile:

```python
'oeffnungszeiten': 'Mo bis Fr von 08:00 bis 17:00 Uhr',
```

Die Angabe „08:00 bis 17:00 Uhr" auf den Stellenseiten ist davon unberührt, sie stammt aus
der JobPosting-Auszeichnung der heutigen Seite. Auch die gehört vor dem Livegang bestätigt.

## v1.2 vom 21.09.2026: heller Kopfbereich, mehr Bilder, kein Formular auf der Startseite

**Das Bewerbungsformular ist von der Startseite verschwunden.** Beworben wird je Stelle,
also gehört das Formular auf die Stellenseite und nirgends sonst hin. Unten steht jetzt
ein Kontaktband: Ansprechpartner, Telefon, WhatsApp, E-Mail. Für den, der erst fragen
will, ohne sich gleich zu bewerben. Alle Knöpfe, die vorher auf `#bewerben` zeigten,
führen jetzt zur Stellenliste.

Das Formular liegt seitdem als eigener Baustein in `werkzeug/formular.html`. Der
Generator holt es von dort, nicht mehr aus der Startseite.

**Der Kopfbereich ist hell statt dunkel.** Der alte Hero war der Vollbild-Hero der
Agenturseite: dunkles Foto, dunkler Schleier, viel Text. Auf einer Karriereseite arbeitet
das gegen den Zweck. Wer hier landet, kommt meist aus einer Stellenanzeige und weiß
schon, worum es geht. Er muss nicht überzeugt werden, er muss sehen, wer hier arbeitet,
und schnell zu den Stellen kommen. Jetzt: heller Verlauf, Text links, Foto rechts mit der
kununu-Note als aufgesetzter Karte, darunter ein **Gesichterband** mit den zehn Porträts
aus dem Shooting.

**Mehr Bilder an drei Stellen:**

| Wo | Was |
|---|---|
| Gesichterband im Hero | zehn runde Porträts über die volle Breite |
| Bildmosaik bei „Elf Leute" | von fünf auf zehn Kacheln, acht Fotos und zwei Zahlen |
| Stellenliste | jede Karte hat links ein Foto, dasselbe wie auf ihrer Unterseite |

Auf Fotos in den Benefit-Kacheln habe ich verzichtet. Für neun Benefits gibt es keine
neun passenden Motive, und erfundene Bezüge wären schlechter als die Symbole.

**Die Porträts heißen jetzt ehrlich.** Sie liegen als
`ao-consulting-team-bruchsal-portraet-01` bis `-10` vor, der Alt-Text lautet „Mitglied des
Teams der AO Consulting GmbH in Bruchsal". Wer darauf zu sehen ist, weiß ich nicht, also
behaupte ich es auch nicht. Auf 640 px verkleinert, das spart gegenüber den Originalen
rund die Hälfte und reicht für die Darstellung als Kreis.

### Zwei Fehler, die der helle Hero aufgedeckt hat

1. **Kopfbereich unsichtbar.** Der Kopf war die durchsichtige Fassung mit weißem Logo,
   gedacht für die dunkle Bühne darunter. Auf hellem Grund stand damit ein weißes Logo auf
   Weiß und das Menü war nicht zu lesen. Die Startseite trägt jetzt `kopf--hell`, wie die
   Stellenseiten seit dem 18.09.
2. **Die drei Chips waren weiß auf weiß.** Sie stammen aus dem dunklen Hero und hatten
   weiße Schrift auf halbdurchsichtigem Weiß. Jetzt weiße Fläche, dunkle Schrift, blaues
   Häkchen.

Beides wäre mir ohne den Blick auf das fertige Bildschirmfoto nicht aufgefallen: die
Prüfskripte melden kein Problem, wenn Text vorhanden und nur unsichtbar ist.

## Was gegenüber der heutigen Seite anders ist

1. **Die Überschrift ist ein Satz, keine Schlagwortkette.** Heute steht dort
   „QUEREINSTEIGER I BÜRO I HOTEL I KAUFMANN JOBS IN BRUCHSAL I …". Das ist an eine
   Suchmaschine gerichtet, nicht an den Menschen, der die Seite öffnet. Die Orte und
   Berufe stehen jetzt in der Vorzeile, im Fließtext und in der FAQ, wo sie für die
   Suche genauso zählen und für Bewerber lesbar sind.
2. **Man kann sich auf der Seite bewerben.** Heute öffnet jeder Weg ein Mailprogramm,
   was auf dem Handy regelmäßig abbricht. Jetzt: Formular mit Anhang, Versand über
   `bewerbung.php`.
3. **Jede Stelle hat einen eigenen Bewerbungsknopf**, der die Auswahl im Formular
   vorbelegt.
4. **Die Videos laden erst nach Einwilligung**, vorher geht keine Anfrage an Wistia.

## Bausteine und woher sie kommen

`assets/stil.css`, `skript.js`, `einwilligung.*` und `barrierefreiheit.*` sowie die
Schriften und das Symbolblatt stammen unverändert aus dem Entwurf „Editorial Navy"
der Hauptseite (`Projekt-AO-Consulting-Webseite/04_.../entwurf-v4-editorial-frisch`).
Wird dort etwas geändert, gehört es auch hierher.

Eigen sind nur zwei Dateien:

- `assets/karriere.css`: Stimmen-Raster, Benefit-Kacheln, Stellenliste, Datei- und Auswahlfeld
- `assets/karriere.js`: die Videos ab dem zweiten (`skript.js` verdrahtet nur das erste),
  der Stellenknopf, die Dateiprüfung und der Versand an `bewerbung.php`

## Das Bewerbungsformular

`bewerbung.php` nimmt die Bewerbung an und schickt sie an **jobs@ao-karriere.de**.
Es speichert nichts auf dem Server, die Anhänge gehen direkt in die Mail.

| Regel | Wert |
|---|---|
| Anhänge | höchstens drei Dateien, zusammen höchstens 10 MB |
| Erlaubt | PDF, DOC, DOCX, JPG, JPEG, PNG |
| Pflichtfelder | Name, E-Mail, Stelle, Einwilligung |
| Bots | unsichtbares Feld „webseite", ausgefüllt heißt still verwerfen |
| Antwort an | Reply-To ist die Adresse des Bewerbers |

**In der Vorschau verschickt es nichts.** Ohne PHP antwortet der Server mit einem Fehler,
und die Seite zeigt dafür einen eigenen Satz statt einer Fehlermeldung. Erst auf dem
echten Hoster läuft der Versand.

## Eine Seite je Stelle, ausgelegt auf Google for Jobs

Jede Stelle hat eine eigene Adresse unter `stellen/<schluessel>.html`. Das ist die
Voraussetzung dafür, dass Google sie als Stellenanzeige versteht und in der Jobs-Leiste
zeigt. Eine Sammelseite mit Ankersprüngen reicht dafür ausdrücklich nicht.

### Gepflegt wird an genau einer Stelle

`werkzeug/stellen-daten.py`. Dort steht je Stelle Titel, Status, Aufgaben,
Qualifikationen, Benefits, Zeiten und Datum. Danach:

```
cd website && python3 ../werkzeug/bauen-stellen.py
```

Das erzeugt in einem Lauf: die Unterseiten, die Stellenliste auf der Startseite, das
Auswahlfeld im Bewerbungsformular aller Seiten und die `sitemap.xml`. Auf der Unterseite
ist die passende Stelle im Formular schon vorgewählt.

### Was in der JobPosting-Auszeichnung steht

Alle Pflichtfelder von Google sind belegt: `title`, `description`, `datePosted`,
`hiringOrganization`, `jobLocation`. Dazu die empfohlenen `employmentType`,
`validThrough`, `identifier` und `directApply`. Die Beschreibung ist echtes HTML mit
Aufgaben, Qualifikationen und Benefits und deckt sich mit dem, was der Besucher sieht.
Zusätzlich liegt auf jeder Seite eine `BreadcrumbList`.

### Fünf Fehler der heutigen Divi-Seiten, die hier nicht wiederkehren

Die bestehenden Stellenseiten auf `ao-karriere.de` tragen bereits JobPosting-Daten. Beim
Nachmessen sind fünf Punkte aufgefallen, die Google entweder ignoriert oder beanstandet:

| Heute auf ao-karriere.de | Warum das ein Problem ist | Hier |
|---|---|---|
| `"currency": "€"` | Google erwartet den ISO-Code, das Zeichen wird verworfen | `EUR` |
| `"addressCountry": "Deutschland"` | Erwartet wird das zweistellige Länderkürzel | `DE` |
| `&lt;ul&gt;` in Beschreibung, Aufgaben und Benefits | Die Listen sind doppelt entwertet und erscheinen als roher Text | echtes HTML |
| `hiringOrganization.name`: „AO Consulting GmbH \| Karriere" | Der Seitentitel steht im Firmennamen | „AO Consulting GmbH" |
| `identifier.value`: der Firmenname | Die Kennung soll je Stelle verschieden sein | der Schlüssel der Stelle |

Dazu: die heutigen Seiten haben **keine einzige Überschrift** im Quelltext, weder h1 noch
h2. Für Google und für Screenreader ist die Seite damit strukturlos. Und die Felder
`responsibilities`, `qualifications`, `jobBenefits`, `skills`, `industry`, `workHours` und
`salaryCurrency` wertet Google bei JobPosting nicht aus. Sie schaden nicht, sie bringen
aber nichts. Hier steht alles dort, wo es gelesen wird: in `description` und sichtbar auf
der Seite.

### Ein Fehler im Generator, der die Startseite zerlegt hat

`liste_einsetzen()` hat die alte Stellenliste vom öffnenden `<ul class="stellen__liste">`
bis zum **ersten** `</ul>` herausgeschnitten. Solange die Karten keine Aufzählung
enthielten, war das richtig. Seit jede Karte eine eigene `<ul class="stelle__punkte">`
hat, trifft die Suche das schließende Tag dieser inneren Liste. Der Rest der alten Liste
blieb stehen, und jeder Lauf hängte eine neue Fassung davor: aus drei Karten wurden
dreizehn, mit doppelten Knöpfen und sichtbaren Aufzählungspunkten.

Behoben an zwei Stellen:

1. `ende_der_liste()` zählt die Verschachtelung mit und findet das wirklich zugehörige
   `</ul>`.
2. Nach dem Einsetzen zählt der Generator die Karten und bricht ab, wenn es nicht genau
   so viele sind wie Stellen in `stellen-daten.py`. Derselbe Fehler fällt damit beim
   nächsten Mal sofort auf, statt still in die Seite zu laufen.

Der Lauf ist jetzt wiederholbar: dreimal hintereinander ausgeführt bleiben es drei Karten.

### Gehalt

Im heutigen Markup steht bei **allen drei** Stellen dieselbe Spanne, 2500 bis 3500 Euro im
Monat. Dass sie überall gleich ist, spricht dafür, dass es ein Vorgabewert des Plugins ist
und keine geprüfte Angabe. Deshalb steht sie hier zunächst **nicht** drin: Google verlangt
echte Zahlen des Arbeitgebers, keine Schätzungen. Eine Gehaltsangabe verbessert die
Darstellung in der Jobs-Leiste spürbar. Sobald die Zahlen bestätigt sind, genügt in
`stellen-daten.py` je Stelle eine Zeile:

```python
'gehalt': (2500, 3500, 'MONTH'),
```

Dann erscheint sie zugleich in der Auszeichnung und sichtbar in den Eckdaten. Beides muss
übereinstimmen, sonst beanstandet Google es.

### Die Ampel entscheidet auch über Google

`status` steuert nicht nur die Farbe:

| Status | Seite | Google |
|---|---|---|
| `aktiv` | grüner Punkt, blinkt, „Online" | läuft bis `gueltig_bis` |
| `initiativ` | gelber Punkt, „Initiativ bewerben" | läuft bis `gueltig_bis` |
| `besetzt` | roter Punkt, Knopf stillgelegt | `validThrough` auf gestern, fällt aus dem Index, fehlt in der sitemap.xml |

Eine besetzte Stelle darf nicht einfach stehen bleiben. Google wertet abgelaufene Anzeigen
als Verstoß, im Wiederholungsfall bis zum Ausschluss aus der Jobs-Leiste.

### Vor dem Livegang zwingend

1. **`noindex` entfernen.** Solange die Seiten „noindex, nofollow" tragen, sieht Google die
   Stellen nie. Das gilt für die Startseite und jede Unterseite.
2. **Adressen festlegen und nicht mehr ändern.** Eine geänderte Adresse ist für Google eine
   neue Stelle, die alte gilt als verschwunden.
3. **`sitemap.xml` in der Search Console einreichen**, `robots.txt` liegt bereit.
4. **Rich-Results-Test** je Seite laufen lassen, bevor die Seiten öffentlich werden.
5. **`gueltig_bis` pflegen.** Steht dort ein Datum in der Vergangenheit, verschwindet die
   Anzeige von selbst. Das ist gewollt und besser als eine tote Anzeige.

### Aufbau der Unterseite

Links die Anzeige: Bild, Ampel, Titel, Kurzfassung, Knopf, Über uns, Aufgaben,
Qualifikationen, Das bieten wir. Rechts eine mitlaufende Spalte mit dem Ansprechpartner
(Foto, Telefon, WhatsApp, E-Mail), den Eckdaten und der kununu-Bewertung. Darunter das
Bewerbungsformular mit vorgewählter Stelle.

**Die kununu-Bewertung ist bewusst kein Widget.** Das Widget von `widgets.kununu.com` würde
bei jedem Aufruf Daten an einen Dritten übertragen, noch vor der Einwilligung. Hier steht
die Note als eigener Baustein mit Verweis auf das Profil. Kein Fremdaufruf, gleiche Aussage.
Die Zahlen (4,9 bei 11 Bewertungen, 100 Prozent Weiterempfehlung) stammen aus dem Projekt
der Hauptseite, Stand 09.09.2026, und gehören vor dem Livegang nachgesehen.

## Einzeldatei zum Weitergeben

`AO-Karriereseite.html` ist die ganze Seite in einer Datei: Bilder, Schriften, Stilvorlagen
und Skripte eingebettet, kein Fremdserver, läuft per Doppelklick. Gebaut mit
`werkzeug/bauen-einzeldatei.py`, aufgerufen im Ordner `website/`:

```
python3 ../werkzeug/bauen-einzeldatei.py AO-Karriereseite.html
```

Nach jeder Änderung an `index.html`, den Stilvorlagen oder den Skripten neu bauen, sonst
zeigt die Einzeldatei einen alten Stand.

**Das Bewerbungsformular verschickt in der Einzeldatei nichts.** Es gibt dort kein PHP.
Die Seite sagt das auch: statt einer Fehlermeldung erscheint der Satz, dass es die Vorschau
ist. Das Band oben auf der Seite weist ebenfalls darauf hin.

### Zwei Fallen beim Bauen der Einzeldatei

1. **Reihenfolge.** Die Listen der Stilvorlagen und Skripte werden aus der unveränderten
   Seite gezogen, bevor irgendetwas eingebettet wird. In den CSS-Dateien stehen in
   Kommentaren Beispielzeilen wie `<script src="assets/einwilligung.js" defer></script>`.
   Sammelt man die Skripte erst nach dem Einbetten des CSS, werden diese Beispielzeilen
   mitgezählt, und Einwilligungsbanner und Barrierefreiheits-Knopf entstehen doppelt. Das
   Skript prüft die Listen jetzt zusätzlich auf Dubletten und bricht sonst ab.
2. **Keine Schriften-Vorlader.** Die `preload`-Zeilen werden entfernt. In einer Einzeldatei
   gibt es nichts vorzuladen, und unter `file://` melden sie sonst einen CORS-Fehler.

## Geprüft

Über neun Breiten von 1920 bis 390 px, automatisiert mit Playwright:

- genau eine H1, lückenlose Überschriftenfolge, kein Sprung
- kein Bild ohne Alt-Text, kein defektes Bild, alle mit `width` und `height`
- kein toter Anker, kein leerer Verweis, JSON-LD parst
- kein seitliches Scrollen bei keiner Breite
- kein Konsolenfehler, kein fremder Host vor der Einwilligung
- Einwilligungsbanner: „Alles erlauben" und „Nur notwendige" gleich groß (282 × 50 px)
  und auf derselben Höhe
- Burger-Menü greift ab 1240 px, Escape schließt, Logo und Burger bleiben sichtbar,
  alle Bedienelemente mindestens 44 px hoch
- alle vier Wistia-IDs stimmen, vor dem Klick geht keine Anfrage an Wistia
- Formular: Ziel und Versandart stehen, Honigtopf liegt außerhalb des Bildes, Pflichtfelder
  melden sich, falsche E-Mail und falscher Dateityp werden abgefangen, die Dateiliste
  erscheint, in der Vorschau kommt die dafür vorgesehene Meldung
- `bewerbung.php` gegen alle Abbruchgründe getestet: Honigtopf, fehlender Name, ungültige
  Mail, fehlende Einwilligung, fehlende Stelle, falscher Dateityp, zu viele Dateien, GET

## Offen, bevor die Seite live geht

- **Talent.com:** Adresse `https://ao-karriere.de/talent.xml` bei Talent.com anmelden und dabei bestätigen lassen, dass die Aufnahme kostenlos ist. Wie man den Feed einreicht, steht nicht in deren Anleitung.
- **Bundesagentur für Arbeit:** Arbeitgeberkonto prüfen oder anlegen (0800 4 555520), dann Kooperationsvereinbarung per Mail anfordern (Entwurf liegt im Chat vom 25.09.). Danach baue ich die HR-BA-XML-Schnittstelle.

- **Indeed:** Arbeitgeberkonto bei Indeed, dort die Adresse `https://ao-karriere.de/indeed.xml` als Feed anmelden (über den Ansprechpartner bei Indeed). Die Mailadresse im Feed (`INDEED_MAIL`, derzeit jobs@ao-karriere.de) muss die des Indeed-Kontos sein.

- **Indexing API** für die Stellenseiten einrichten, **Bing Webmaster Tools** und **IndexNow** anmelden (siehe SEO-Prüfung).

- **Datenschutz und Impressum** aus dem WordPress als eigene Seiten übernehmen, bevor es abgeschaltet wird. Alte Adresse `/hinweis-zur-gleichstellung/` auf `rechtliches/hinweis-zur-gleichstellung.html` umleiten.

- **Admir Renz:** Telefonnummer und WhatsApp für die Vertriebsstellen fehlen.

- **Fahrtkostenzuschuss:** stimmt „Der Weg nach Bruchsal wird bezuschusst, die Höhe
  besprechen wir beim Kennenlernen"? Der alte Text der Kachel gehörte nicht dazu.
- **Getränke, Obst und Süßes** stehen nicht mehr auf der Seite, weil die Sektion
  „keine Obstkorb-Poesie" verspricht. Sollen sie zurück, braucht es eine eigene Kachel.
- **FAQ Initiativbewerbung:** soll der Satz zurück, dass Stellen aus Initiativbewerbungen
  entstanden sind? Dann bitte bestätigen, wie viele.
- **Elftes Porträt (Iwan):** sobald es vorliegt, kann das Gesichterband zurück.

1. **Rechtsseiten.** Impressum und Datenschutz verweisen heute auf `ao-consult.de`.
   Eine eigene Domain braucht ein eigenes Impressum, und die Datenschutzerklärung muss
   das Bewerbungsformular und Wistia nennen. **Nicht erfunden, bitte klären.**
2. **Die Stellenanzeigen sind meine Formulierung.** Auf der heutigen Seite stehen nur
   die Titel. Was ich zu Aufgaben, Festgehalt und Einarbeitung geschrieben habe, ist
   plausibel, aber nicht belegt. **Vor dem Livegang fachlich durchgehen.**
3. **„Elf Leute" und „4,9 bei kununu"** stammen aus dem Projekt der Hauptseite
   (Stand 09.09.2026). Wenn sich die Teamgröße geändert hat, hier nachziehen.
4. **Jede Stelle mit eigener Adresse.** Heute sind es Abschnitte einer Seite, damit
   liest Google sie nicht als Stellenanzeige. Genau das verkauft AO an Kunden. Der
   nächste sinnvolle Ausbauschritt ist eine Seite je Stelle mit `JobPosting`-Markup.
5. **Fotos.** Die Bilder stammen aus dem Projekt der Hauptseite, weil die Bilder von
   ao-karriere.de vom Netz dieser Umgebung nicht abgerufen werden können. Wenn bestimmte
   Fotos von der heutigen Seite gewünscht sind, in `input/fotos/` legen.
6. **Der Recruitingfilm im Hero-Bereich** trägt derzeit ein Standbild aus dem Büro. Wenn
   es zu dem Film ein passendes Vorschaubild gibt, tauschen.

## Bekannte Eigenart

Unter `file://` meldet der Browser beim Absenden des Formulars einen Netzwerkfehler in der
Entwicklerkonsole. Das ist erwartbar, es gibt dort kein PHP. Für den Besucher sichtbar ist
nur der Hinweis, dass es die Vorschau ist.
