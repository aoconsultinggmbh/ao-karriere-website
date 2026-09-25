---
titel: SEO- und GEO-Prüfung der Karriereseite
kategorie: Projekt-Output
kurzbeschreibung: Google for Jobs, KI-Suchmaschinen, Stellentitel, H1 und Region. Was geprüft wurde, was umgesetzt ist, was entschieden werden muss.
stand: 2026-09-25
erstellt-von: Claude auf Anweisung Ovidiu
---

# SEO- und GEO-Prüfung der Karriereseite

Geprüft am 25.09.2026 gegen die Vorgaben von Google, OpenAI, Anthropic und Perplexity
(Quellen am Ende). Grundlage ist der Stand v2.0 im Projektordner.

## 1. Werden die Stellen bei Google for Jobs eingepflegt?

**Technisch ja, sobald die Seite live ist.** Jede Stelle hat eine eigene Seite mit genau
einer `JobPosting`-Auszeichnung. Alle Pflichtfelder von Google sind da (`title`,
`description`, `datePosted`, `hiringOrganization`, `jobLocation` mit Land), dazu die
empfohlenen `validThrough`, `employmentType`, `identifier` und `directApply`. Das Logo
liegt im erlaubten Seitenverhältnis (1,22, erlaubt 0,75 bis 2,5).

**Zwei Dinge verhindern es heute noch:**

- Alle Seiten tragen `noindex`, weil sie Vorschau sind. Das muss beim Livegang raus.
- Die Seite liegt noch nicht auf ao-karriere.de.

**⚠️ Ein Risiko mit den Initiativ-Stellen:** Google erlaubt Bewerbungen einzusammeln nur
für offene Stellen („Publishers may solicit resume collections for open positions only").
Backoffice und Webdesign stehen auf Gelb, sind also nicht offen, werden aber als
`JobPosting` gemeldet. Das kann eine manuelle Maßnahme gegen die Stellenanzeigen der ganzen
Domain auslösen. **Entscheidung nötig.**

## 2. Können Stellentitel und Qualifikationen besser werden?

**Titel:** Google verlangt im Feld `title` nur die Berufsbezeichnung, ohne Firma, Ort,
Gehalt oder Kennziffern. „(m/w/d)" ist erlaubt. Das halten alle drei Titel ein.

| Stelle | heute | Einschätzung |
|---|---|---|
| Vertrieb | Vertriebsmitarbeiter im Innendienst (m/w/d) | gut, so wird gesucht. Bleibt |
| Backoffice | Assistenz im Backoffice (m/w/d) | „Assistenz" allein ist vage. Vorschlag: Kaufmännische Assistenz im Backoffice (m/w/d) |
| Webdesign | Webdesigner für WordPress und Divi (m/w/d) | „Divi" sucht kaum jemand, der Titel wird lang. Vorschlag: Webdesigner WordPress (m/w/d), Divi bleibt in den Qualifikationen |

**Qualifikationen:** Umgesetzt sind die Felder `educationRequirements` und
`experienceRequirements` mit „no requirements", genau dort, wo der Text es hergibt:
Ausbildung ist bei allen drei kein Muss, Erfahrung nur bei Vertrieb und Backoffice nicht.
Beim Webdesign steht „erste Erfahrung mit WordPress", dort steht deshalb nichts. Damit kann
Google die Stellen bei Suchen wie „ohne Erfahrung" oder „Quereinsteiger" zuordnen.

Die Aufgaben sind unverändert.

**Gehalt:** `baseSalary` ist das wichtigste empfohlene Feld, das noch fehlt. Ohne Angabe
schätzt Google oder zeigt nichts. **Entscheidung nötig.** Hinweis: Die EU-Richtlinie zur
Entgelttransparenz (2023/970) war bis Juni 2026 umzusetzen. Wie weit das für Stellenanzeigen
in Deutschland schon gilt, bitte rechtlich prüfen lassen, ich bin kein Anwalt.

## 3. Finden KI-Suchmaschinen die Stellen?

**Ja, sobald die Seite live und indexiert ist.** Die Inhalte stehen als fertiges HTML in
der Seite, nichts wird erst per Skript nachgeladen. KI-Crawler lesen das direkt.

| Dienst | Crawler für die Suche | Stand |
|---|---|---|
| ChatGPT | OAI-SearchBot | erlaubt (`User-agent: *`) |
| Claude | Claude-SearchBot | erlaubt |
| Perplexity | PerplexityBot | erlaubt |
| Google AI Overviews / AI Mode | normaler Googlebot | erlaubt, braucht laut Google keine Sonderdatei |

Eine `llms.txt` bringt laut Google nichts für AI Overviews. Die anderen Dienste
dokumentieren sie nicht als Voraussetzung. Sie ist deshalb nicht angelegt.

## 4. Kann die Seite an sich besser werden?

**Umgesetzt:**

- Seitentitel der Stellen kürzer: „… in Bruchsal | AO Consulting" statt „| Karriere bei AO Consulting GmbH" (vorher 77 bis 89 Zeichen)
- Beschreibung der Stellen: der fehlende Punkt nach dem Titel ist ergänzt, der Satz beginnt mit Titel, Ort und Umfang
- `JobPosting`-Beschreibung beginnt mit der Stelle, nicht mehr zweimal mit dem Text über das Team
- `sitemap.xml`: das Änderungsdatum der Stellen ist jetzt das echte Datum statt jeder Bau-Tag. Google wertet es nur, wenn es stimmt
- Route planen: Verweis auf Google Maps im Kontaktband, bei der Stelle unter „Arbeitsort" und im Formularkasten. Es wird nichts eingebettet, deshalb braucht es keine Einwilligung

**Für den Livegang (Liste in LIESMICH):**

- `noindex` raus, Seite in der Google Search Console anmelden, Sitemap einreichen
- Stellen über die **Indexing API** melden. Google empfiehlt das ausdrücklich für Stellenseiten, weil sie damit schneller gecrawlt werden
- **Bing Webmaster Tools** und **IndexNow** einrichten. Bing, Amazon und andere nehmen neue und geänderte Seiten damit sofort auf
- Impressum und Datenschutz aus dem WordPress übernehmen

## 5. Hat die Seite eine gute H1 für Bruchsal und die Umgebung?

**Nein.** Die H1 heißt „Du musst nichts mitbringen außer dem Willen, es zu können." Kein
Ort, kein „Jobs". Die kleine Zeile darüber („Jobs bei AO Consulting in Bruchsal") ist nur
ein Absatz. Die Umgebung steht einmal im Kleingedruckten (Bretten, Untergrombach, Forst,
Weingarten). Karlsruhe fehlt ganz.

**Vorschlag:** Die kleine Zeile wird zur H1 und nennt die Region, der Spruch bleibt genau so
groß stehen, ist technisch aber keine Überschrift mehr. Optisch ändert sich nichts. Dazu
Seitentitel und Beschreibung mit Region. **Entscheidung nötig.**

Für Google for Jobs selbst zählt die Adresse in der Stellenauszeichnung. Google zeigt eine
Stelle in Bruchsal auch bei Suchen in der Umgebung. Mehrere Orte einzutragen, an denen gar
nicht gearbeitet wird, wäre falsch und verstößt gegen die Vorgaben.

## Nebenbei behoben

Der Umbruch „mitbrin-gen" in der großen Zeile kam von automatischer Silbentrennung plus
festem Zeilenumbruch. Beides ist raus, die Zeilen verteilt der Browser jetzt gleichmäßig.

## Entscheidungen von Ovidiu (25.09.2026)

| Frage | Entscheidung | umgesetzt |
|---|---|---|
| Initiativ-Stellen an Google melden | **alle drei weiter melden** | bleibt wie es ist. ⚠️ Das Risiko einer manuellen Maßnahme durch Google ist damit bewusst in Kauf genommen. Wird eine Stelle besetzt, läuft sie über `validThrough` ab |
| H1 mit Region | kleine Zeile wird H1 | H1 „Jobs in Bruchsal und Umgebung bei AO Consulting", der Spruch bleibt gleich groß als Absatz. Seitentitel „Jobs in Bruchsal und Umgebung für Quereinsteiger \| AO Consulting", Beschreibung und Erreichbarkeit mit Karlsruhe, Bretten, Stutensee, Ubstadt-Weiher, Forst und Weingarten |
| Stellentitel | beide ändern | „Kaufmännische Assistenz im Backoffice (m/w/d)", „Webdesigner WordPress (m/w/d)". Adressen der Seiten unverändert |
| Gehalt | ohne Gehalt | Feld bleibt leer |

## Quellen

- [Google: Job posting structured data](https://developers.google.com/search/docs/appearance/structured-data/job-posting)
- [Google: AI features and your website](https://developers.google.com/search/docs/appearance/ai-features)
- [Google: common crawlers, Google-Extended](https://developers.google.com/search/docs/crawling-indexing/google-common-crawlers)
- [OpenAI: Overview of OpenAI crawlers](https://developers.openai.com/api/docs/bots)
- [Anthropic: Does Anthropic crawl data from the web](https://support.claude.com/en/articles/8896518-does-anthropic-crawl-data-from-the-web-and-how-can-site-owners-block-the-crawler)
- [Perplexity: Perplexity crawlers](https://docs.perplexity.ai/guides/bots)
- [IndexNow FAQ](https://www.indexnow.org/faq)
