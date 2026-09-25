# Karriereseite AO Consulting

Die Karriereseite der AO Consulting GmbH: **ao-karriere.de**

Sie ersetzt die bisherige WordPress-Seite (Divi, gehostet bei Raidboxes) durch
eine reine HTML-Seite ohne Baukasten, ohne Datenbank und ohne fremde Tracker.

---

## Zwei Adressen, zwei Zweige

| Zweig | Wohin | Adresse |
|---|---|---|
| `main` | Vorschau bei GitHub Pages | https://ao-karriere.vorschau.ao-consult.de |
| `live` | echter Server bei All-Inkl | https://ao-karriere.de |

**Nichts geht ohne Freigabe live.** Änderungen landen zuerst auf `main`.
Erst wenn `live` auf den Stand von `main` gesetzt wird, lädt GitHub die Dateien
per verschlüsseltem FTP zum Hoster.

Die Vorschau sperrt sich selbst gegen Google aus: der Ablauf
`.github/workflows/vorschau.yml` setzt beim Bauen in jede Seite einen
`noindex`-Hinweis und ersetzt die `robots.txt`. **In den Quelldateien steht
kein `noindex`** – sonst wäre auch die echte Seite für Google unsichtbar.

---

## Aufbau

```
website/            die Seite. Nur was hier liegt, geht online.
  index.html        die Karriereseite selbst
  stellen/          eine Seite je Stelle, erzeugt aus doku/werkzeug/
  rechtliches/      Impressum, Datenschutz, Gleichstellungshinweis
  assets/           CSS und JavaScript
  img/ fonts/       Bilder und Schriften, alles lokal
  bewerbung.php     nimmt Bewerbungen entgegen und mailt sie weiter
  indeed.xml        Stellen-Feed für Indeed
  talent.xml        Stellen-Feed für Talent.com
  sitemap.xml       für Google
  .htaccess         Weiterleitungen, Zwischenspeicher, HTTPS
doku/               Unterlagen, gehen NICHT online
  werkzeug/         die Skripte, mit denen die Stellenseiten erzeugt werden
  projektstand.md   Ovis Arbeitsprotokoll
  projektregeln.md  die Schreib- und Bauregeln des Projekts
```

### Wichtig: die Stellenseiten sind erzeugt, nicht getippt

`website/stellen/*.html`, die Stellenliste auf der Startseite, `sitemap.xml`,
`indeed.xml` und `talent.xml` werden von `doku/werkzeug/bauen-stellen.py` aus
`doku/werkzeug/stellen-daten.py` erzeugt.

**Änderungen an einer Stelle gehören in `stellen-daten.py`**, nicht in die
fertige HTML-Datei. Sonst sind sie beim nächsten Lauf des Generators weg.
Für reine Textkorrekturen an `index.html` außerhalb der Stellenliste gilt das
nicht, die kann man direkt ändern.

---

## Was diese Seite bewusst NICHT tut

- kein Google Analytics, kein Google Ads Tracking, kein Meta-Pixel
- keine Schriften von fremden Servern, kein Google Fonts
- kein reCAPTCHA
- keine Cookies außer dem Speicher für die Einwilligungs-Entscheidung
  (und das ist ein lokaler Speichereintrag, kein Cookie)

Zwei Inhalte kommen von außen und werden **erst nach Zustimmung** geladen:
die Vorstellungsvideos (Wistia, USA) und das kununu-Siegel (New Work SE).
Vorher geht keine einzige Anfrage dorthin.

Die Datenschutzerklärung unter `website/rechtliches/datenschutz.html`
beschreibt genau das. Sie ist **nicht** die alte WordPress-Erklärung: die
beschrieb Google Analytics, Google Ads, AdSense, Meta-Pixel, Borlabs Cookie,
reCAPTCHA, Brevo und Zapier – nichts davon gibt es auf dieser Seite. Eine
Datenschutzerklärung, die Dienste nennt, die es nicht gibt, ist genauso falsch
wie eine, die welche verschweigt.

---

## Vor dem Livegang zu erledigen

Diese Punkte stehen noch offen. Sie stammen aus Ovis Projektstand
(`doku/projektstand.md`) und aus der Durchsicht vom 25.09.2026.

### Muss

- [ ] **Postfach `jobs@ao-karriere.de`** muss erreichbar sein und eine echte
      Testbewerbung muss ankommen, nicht im Spam. Die Post liegt bei
      mailbox.org, die Seite kommt zu All-Inkl – das ist der Test, der am
      wichtigsten ist.
- [ ] **SPF-Eintrag prüfen.** `bewerbung.php` verschickt ab jetzt mit dem
      Absender `jobs@ao-karriere.de` vom All-Inkl-Server. Im SPF von
      ao-karriere.de steht bisher nur mailbox.org und Raidboxes. Ohne die
      All-Inkl-Bereiche (`ip4:85.13.128.0/18 ip4:185.3.40.0/22`) landen die
      Bewerbungsmails im Spam.
- [ ] **Anschrift des Hosters im Datenschutz bestätigen**
      (ALL-INKL.COM – Neue Medien Münnich, Hauptstraße 68, 02742 Friedersdorf)
      und prüfen, ob der Auftragsverarbeitungsvertrag mit All-Inkl vorliegt.
- [ ] **Öffnungszeiten** in `doku/werkzeug/stellen-daten.py` sind leer. Der
      Generator weist bei jedem Lauf darauf hin.
- [ ] **Telefon und WhatsApp von Admir Renz** fehlen. Bei Vertriebsstellen ist
      er der Ansprechpartner, seine Karte zeigt bis dahin nur die E-Mail.
- [ ] **Fachliche Freigabe der drei Stellentexte** durch Ovi.

### Sollte

- [ ] **Gehaltsangabe**: bewusst weggelassen. Google for Jobs stuft Anzeigen
      ohne Gehalt schlechter ein. Entscheidung liegt bei Ovi.
- [ ] **Initiativ-Stellen als `JobPosting`**: zwei der drei Stellen tragen den
      Status „initiativ". Google erlaubt `JobPosting` nur für tatsächlich
      offene Stellen. Das Risiko ist bekannt und in
      `doku/seo-geo-pruefung-2026-09-25.md` festgehalten.
- [ ] **Indeed-Konto** und Anmeldung des Feeds `indeed.xml` bei Indeed.
- [ ] **Bundesagentur für Arbeit**: Arbeitgeberkonto und
      Kooperationsvereinbarung, dann läuft der Feed auch dorthin.
- [ ] **Search Console**: Property `https://ao-karriere.de/` anlegen,
      `sitemap.xml` einreichen.

### Nach dem Livegang

- [ ] Prüfen, ob die alten Adressen weiterleiten (siehe `.htaccess`).
- [ ] Eine Woche später: Raidboxes-Box kündigen. **Nur die Box**, nicht die
      Domain – die DNS-Verwaltung für ao-karriere.de liegt dort, und die
      Vorschau-Adressen aller Kundenprojekte hängen an derselben Stelle.

---

## Wenn etwas kaputt ist

**Die Vorschau zeigt die alte Seite.** Erst messen, dann erklären: im Browser
`Strg + Umschalt + R`, und wenn das nicht hilft, im Ablauf unter „Actions"
nachsehen, ob der letzte Lauf grün war.

**Der Livegang-Ablauf ist rot.** Meistens stimmt eines der vier Secrets nicht.
GitHub → Settings → Secrets and variables → Actions.

**Nach dem Hochladen kommt die alte Seite.** Die `.htaccess` hat ganz oben eine
Ausnahme für die Übergangsadresse des Hosters. Ohne sie schickt die eigene
www-Umleitung jeden Testaufruf zurück auf die alte Seite.

---

*Angelegt am 25.09.2026 von Admir Renz. Entwurf und Inhalt: Ovidiu Rieger.*
