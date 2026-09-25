---
titel: CLAUDE.md — Projekt AO Karriereseite
kategorie: Steuerung
kurzbeschreibung: Einstieg für jede Session an ao-karriere.de. Was gebaut wird, wo was liegt, welche Regeln gelten.
schlagworte: [Steuerung, ao-karriere.de, Karriereseite, Landeseite]
stand: 2026-09-18
version: 1.0
---

# Projekt AO Karriereseite

## Was gebaut wird

`ao-karriere.de` wird neu gebaut. Ziel ist **eine einzelne HTML-Landeseite**, kein
mehrseitiger Auftritt. Die Seite soll später als eigenständige Landeseite laufen und
kann dann um weitere Seiten wachsen, zum Beispiel eine Seite je Stelle.

Heute läuft die Seite auf WordPress mit Divi. Der Neubau ist statisches HTML in der
Handschrift der neuen Hauptseite („Editorial Navy"), damit beide Auftritte
zusammengehören.

## Warum das Projekt wichtig ist

AO verkauft Karriereportale an Praxen und Kliniken. Die eigene Karriereseite ist die
Arbeitsprobe, die jeder Bewerber und jeder Interessent zuerst sieht. Was auf der
Hauptseite als Leistung steht, muss hier sichtbar eingelöst sein.

## Ordner

| Pfad | Inhalt |
|---|---|
| `00_projekt/` | Diese Datei, `status.md` |
| `input/bestandsaufnahme/` | Ist-Analyse der heutigen Seite |
| `input/fotos/` | Bildmaterial |
| `website/` | Die gebaute Seite: `index.html`, `assets/`, `fonts/`, `img/` |
| `doku/` | Bildschirmfotos, Prüfprotokolle |

## Regeln

1. **Der Skill `ao-webdesign-qa` gilt für jeden Entwurf.** Barrierefreiheits-Knopf,
   Einwilligungsbanner, lokale Schriften, WebP-Bilder mit sprechenden Dateinamen,
   saubere Überschriftenfolge, Hover-Zustände, kein seitliches Scrollen.
2. **Der Skill `ao-schreibstil` gilt für jeden Text.** Keine Gedankenstriche im Fließtext.
3. **Gestaltung und Bausteine kommen aus der neuen Hauptseite**
   (`Projekt-AO-Consulting-Webseite/04_.../output/entwurf-v4-editorial-frisch/`). Farben,
   Schriften, Kopf, Fuß, Einwilligungsbanner und Barrierefreiheits-Knopf werden von dort
   übernommen, nicht neu erfunden.
4. **Nichts behaupten, was nicht belegt ist.** Zahlen zu Team, Bewertungen und
   Rückmeldezeiten stammen aus dem Projekt der Hauptseite oder werden bei Ovidiu erfragt.
5. **Der Projektordner ist die führende Quelle**, nicht ein GitHub-Projekt. Veröffentlicht
   wird von hier aus, so wie es der Skill `webseite-veroeffentlichen` beschreibt.
6. **Ansprechpartner je Stelle (Vorgabe Ovidiu, 25.09.2026):** Für **alle Vertriebsstellen
   ist Admir Renz** der Ansprechpartner, für **alle anderen Stellen Ovidiu Rieger**. Umgesetzt
   in `werkzeug/stellen-daten.py`: jede Stelle trägt `'bereich'`, die Zuordnung steht in
   `ANSPRECHPARTNER_NACH_BEREICH`. Eine neue Vertriebsstelle bekommt `'bereich': 'vertrieb'`
   und damit automatisch Admir, in der Karte rechts und im Formularkasten. Die Startseite
   und das Kontaktband bleiben bei Ovidiu. Für Admir fehlen noch Telefon und WhatsApp.
7. **Belege vor Behauptungen, auch bei Kleinigkeiten.** In diesem Projekt sind schon
   erfundene Öffnungszeiten, eine erfundene Herkunft von Stellen aus Initiativbewerbungen
   und ein erfundenes „unbefristet" aufgefallen. Jede Tatsachenaussage im Text braucht eine
   Quelle in den Projektdateien oder eine Bestätigung von Ovidiu.
8. **Das Bewerbungsformular gehört zur Stelle.** Auf einer Stellenseite gibt es kein
   Auswahlfeld, die Stelle steht fest im Formular.

## Vor dem Bau zu klären

1. Welche Bewerbungsadresse gilt, `jobs@ao-karriere.de` oder `jobs@ao-consult.de`?
2. Soll die Seite ein echtes Bewerbungsformular mit Dateianhang bekommen, oder bleibt es
   bei der Bewerbung per Mail?
3. Welche Stellen sind aktuell offen? Heute stehen drei auf der Seite, zwei davon initiativ.
4. Bekommt jede Stelle später eine eigene Adresse, damit Google sie als Stellenanzeige
   versteht? Das ist genau die Leistung, die AO verkauft.
5. Welche Fotos dürfen verwendet werden? Auf der heutigen Seite liegen rund vierzig Bilder
   aus zwei Aufnahmetagen.
6. Bleibt das kununu-Widget, oder wird die Bewertung als eigener Baustein gezeigt?
