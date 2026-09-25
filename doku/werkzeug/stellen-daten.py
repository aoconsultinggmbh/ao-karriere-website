# -*- coding: utf-8 -*-
"""Die Stellen. Nur diese Datei wird gepflegt, alles andere erzeugt der Generator.

Ein neuer Eintrag hier erzeugt eine eigene Unterseite, einen Eintrag in der
Stellenliste der Startseite, einen Eintrag in der sitemap.xml und die
JobPosting-Auszeichnung für Google for Jobs.

Feldkunde
---------
schluessel   Dateiname und Adresse der Unterseite. Klein, mit Bindestrichen,
             mit dem Suchbegriff vorn und dem Ort hinten. Wird nie geändert,
             sobald die Seite einmal veröffentlicht ist: eine geänderte Adresse
             ist für Google eine neue Stelle und die alte gilt als verschwunden.
status       'aktiv'      grün, blinkend, wird gerade besetzt
             'initiativ'  gelb, gerade nicht ausgeschrieben
             'besetzt'    rot, nicht mehr offen. Google gegenüber gilt sie
                          dann als abgelaufen (validThrough wird zurückgesetzt).
titel        Der Stellentitel, wie ihn ein Mensch sucht. Ohne Ort, ohne Gehalt,
             ohne Kürzel. Das verlangt Google ausdrücklich.
veroeffentlicht / gueltig_bis
             ISO-Datum. 'gueltig_bis' ist das Datum, an dem die Anzeige von
             selbst aus Google verschwindet. Ohne Datum bleibt sie stehen, bis
             jemand sie entfernt.
gehalt       None oder (min, max, 'MONTH'|'YEAR'). Nur echte Zahlen des
             Arbeitgebers, keine Schätzung. Steht sie hier, steht sie auch
             sichtbar auf der Seite, sonst widersprechen sich Seite und
             Auszeichnung.
"""

FIRMA = {
    'name': 'AO Consulting GmbH',
    'strasse': 'Zeiloch 13',
    'plz': '76646',
    'ort': 'Bruchsal',
    'region': 'Baden-Württemberg',
    'land': 'DE',
    # Buerozeiten. Erscheinen so in der FAQ-Antwort mit dem Ortsbezug, die
    # Google und KI-Antworten gern zitieren. None heisst: der Satz laesst die
    # Zeiten weg. Bitte nur eintragen, was stimmt.
    # ACHTUNG 21.09.2026: hier standen "Mo bis Do 08:00 bis 17:30, Fr 08:00 bis
    # 16:00". Die Zeiten stammten aus einem Beispiel im Skill ao-schreibstil und
    # waren nie geprueft. Ovidiu hat widersprochen, deshalb jetzt leer.
    'oeffnungszeiten': None,
    'seite': 'https://ao-consult.de/',
    'karriere': 'https://ao-karriere.de/',
    'logo': 'https://ao-karriere.de/img/ao-consulting-logo.svg',
    'kanaele': [
        'https://www.instagram.com/ao_consulting_gmbh/',
        'https://www.facebook.com/aoconsultinggmbh/',
        'https://de.linkedin.com/company/aoconsult',
        'https://www.youtube.com/@aoconsultinggmbh',
        'https://www.tiktok.com/@ao.consulting.gmbh',
        'https://kununu.com/de/ao-consulting',
    ],
}

# Ansprechpartner. REGEL von Ovidiu (25.09.2026): Fuer alle Vertriebsstellen
# ist Admir der Ansprechpartner, fuer alle anderen Stellen Ovidiu. Jede Stelle
# traegt dazu ein Feld 'bereich'. Wer abweichen will, setzt bei der Stelle
# 'ansprechpartner' ausdruecklich.
# Fehlt eine Angabe (None), laesst der Generator den Knopf weg und meldet es.
PERSONEN = {
    'ovidiu': {
        'name': 'Ovidiu Rieger',
        'rolle': 'Geschäftsführer',
        'telefon': '+4917685933551',
        'telefon_sichtbar': '0176 85933551',
        'whatsapp': 'https://wa.me/4917685933551',
        'mail': 'jobs@ao-karriere.de',
        'bild': 'team-ovidiu-rieger',
    },
    'admir': {
        'name': 'Admir Renz',
        'rolle': 'Geschäftsführer',     # so auf der Agenturseite
        'telefon': None,                # OFFEN: Nummer von Admir fehlt noch
        'telefon_sichtbar': None,
        'whatsapp': None,               # OFFEN: WhatsApp von Admir fehlt noch
        'mail': 'jobs@ao-karriere.de',
        'bild': 'team-admir-renz',
    },
}
ANSPRECHPARTNER_NACH_BEREICH = {'vertrieb': 'admir'}
ANSPRECHPARTNER_STANDARD = 'ovidiu'
# Fuer Stellen gleich, fuer die Startseite und das Kontaktband: Ovidiu.
ANSPRECHPARTNER = PERSONEN[ANSPRECHPARTNER_STANDARD]


# Das Siegel von kununu liegt auf deren Server und ueberträgt beim Laden die
# IP-Adresse des Besuchers. Es laedt deshalb erst nach der Einwilligung, vorher
# steht die Bewertung als eigener Baustein da. Wer das Siegel ohne Tor will,
# laedt die Grafik einmal herunter, legt sie unter img/ ab und traegt hier den
# oertlichen Pfad ein: dann ist es kein fremder Aufruf mehr.
KUNUNU = {'note': '4,9', 'weiterempfehlung': '100', 'anzahl': '11',
          # Genau der Verweis aus dem Einbettungscode, den kununu fuer das Widget ausgibt.
          'link': 'https://kununu.com/de/ao-consulting?utm_medium=affiliate&utm_source=widget&utm_content=widget_score_review_count_logo_small&rfr=affiliate_widget',
          'widget': 'https://widgets.kununu.com/widget_score_review_count_logo_small/profiles/e6697b32-215e-44a2-bced-332cfab9403a'}

# Der Einstieg steht auf jeder Stellenseite gleich, er beschreibt das Haus.
EINSTIEG = [
    'Gute Laune, Motivation, Freundlichkeit und Dynamik zeichnen unser Team und unseren Alltag aus. Die Stimmung im ganzen Unternehmen sorgt für eine ausgeglichene und geregelte Arbeitsweise.',
    'Regelmäßige gemeinsame Aktivitäten schweißen uns zusammen, dadurch bewahren wir auch in schwierigen Zeiten einen kühlen Kopf. Wir reagieren schnell auf Wünsche und sind offen für Neues, denn nur so wird die Zusammenarbeit besser.',
]

BENEFITS_STANDARD = [
    'Attraktive Bezahlung',
    'Kaffee, Wasser, Cola Zero, Paulaner Spezi, Obst und Süßigkeiten sind selbstverständlich',
    'Fahrtkostenzuschüsse',
    'Ergonomischer und klimatisierter Arbeitsplatz mit höhenverstellbaren Tischen',
    'Digitaler Einarbeitungsplan',
    'Arbeiten auf modernen Apple-Geräten',
    'Mitarbeiterevents, Teamevents, After-Work',
    '30 Tage Urlaub',
    'Weiterbildungsmöglichkeiten',
]

STELLEN = [
    {
        'schluessel': 'vertriebsmitarbeiter-innendienst-bruchsal',
        'ausbildung_noetig': False,   # Google for Jobs: False = "no requirements"
        'erfahrung_noetig': False,    # Google for Jobs: False = "no requirements"
        'bereich': 'vertrieb',
        'status': 'aktiv',
        'titel': 'Vertriebsmitarbeiter im Innendienst (m/w/d)',
        'kurz': 'Du rufst Praxen und Labore an, hörst zu und findest heraus, wo es klemmt. Verkaufen lernst Du bei uns.',
        'auch_fuer': 'Hotelfachmann, Bürokaufmann und Quereinsteiger',
        'veroeffentlicht': '2026-08-26',
        'gueltig_bis': '2026-11-26',
        'pensum': 'Vollzeit',
        'zeiten': '08:00 bis 17:00 Uhr',
        'gehalt': None,   # im heutigen Markup steht 2500 bis 3500 EUR im Monat, siehe LIESMICH
        'bild': 'ao-consulting-bewerbermanagement-am-telefon',   # Dennis am Telefon, Wunsch Ovidiu 25.09.
        'bild_alt': 'Dennis von AO Consulting telefoniert mit Headset am Schreibtisch im Büro in Bruchsal',
        # Bildausschnitt im flachen Band der Stellenseite: Dennis sitzt rechts, der Kopf weit oben.
        'bild_fokus': '70% 10%',
        'aufgaben': [
            'Telefonische Akquise potenzieller Neukunden',
            'Durchführung von Erstgesprächen zur Bedarfsanalyse',
            'Telefonische Kontaktaufnahme zu bereits vorhandenen Kontakten im System',
            'Planung sowie Vor- und Nachbereitung der Termine unserer Strategieberater',
            'Gelegentlicher Besuch von Messen, Seminaren und ähnlichen Veranstaltungen zur Neukundengewinnung',
        ],
        'qualifikationen': [
            'Eine abgeschlossene kaufmännische Ausbildung als Einzelhandelskaufmann, Bürokaufmann oder Groß- und Außenhandelskaufmann (m/w/d) ist von Vorteil, aber nicht notwendig',
            'Quereinsteiger aus Hotellerie, Gastronomie, Pflege oder Handwerk sind willkommen',
            'Grundkenntnisse in den gängigen Microsoft-Programmen wie Outlook und Excel sind vorteilhaft',
            'Gute Deutschkenntnisse in Wort und Schrift',
            'Führerschein Klasse B',
        ],
    },
    {
        'schluessel': 'assistenz-backoffice-bruchsal',
        'ausbildung_noetig': False,   # Google for Jobs: False = "no requirements"
        'erfahrung_noetig': False,    # Google for Jobs: False = "no requirements"
        'bereich': 'backoffice',
        'status': 'initiativ',
        'titel': 'Kaufmännische Assistenz im Backoffice (m/w/d)',   # suchfreundlicher, Ovidiu 25.09.
        'kurz': 'Du hältst den Laden zusammen: Termine, Unterlagen, Rückfragen, Abstimmung zwischen Vertrieb und Umsetzung.',
        'auch_fuer': 'Hotelfachfrau, Bürokauffrau und Quereinsteiger',
        'veroeffentlicht': '2026-08-26',
        'gueltig_bis': '2026-11-26',
        'pensum': 'Vollzeit',
        'zeiten': '08:00 bis 17:00 Uhr',
        'gehalt': None,
        'bild': 'ao-consulting-praxisauftritt-abstimmung',
        'bild_alt': 'Zwei Mitarbeitende der AO Consulting stimmen sich am Schreibtisch mit einem Tablet ab',
        'bild_fokus': '50% 40%',
        'aufgaben': [
            'Schriftlicher Kundensupport über E-Mail, Messenger und Gruppen',
            'Stellenanzeigen aktualisieren und Unterstützung bei Bewerbungsprozessen',
            'Unterstützung beim Erstellen digitaler Werbeanzeigen',
            'Assistenztätigkeiten für die Geschäftsführung',
            'Mitarbeit im Backoffice beim Onboarding neuer Kunden',
            'Unterstützung im Social-Media-Marketing',
        ],
        'qualifikationen': [
            'Eine abgeschlossene Berufsausbildung, etwa als Bürokauffrau, Hotelfachfrau, Kauffrau für Büromanagement oder Einzelhandelskauffrau (m/w/d), ist von Vorteil, aber nicht zwingend erforderlich',
            'Quereinsteiger, zum Beispiel aus der Gastronomie, sind willkommen',
            'Erfahrung mit Microsoft-Programmen wie Outlook ist vorteilhaft, aber nicht zwingend erforderlich',
            'Führerschein Klasse B',
        ],
    },
    {
        'schluessel': 'webdesigner-wordpress-bruchsal',
        'ausbildung_noetig': False,   # Google for Jobs: False = "no requirements"
        'bereich': 'webdesign',
        'status': 'initiativ',
        'titel': 'Webdesigner WordPress (m/w/d)',   # kuerzer, Divi steht in den Qualifikationen, Ovidiu 25.09.
        'kurz': 'Du baust Praxiswebseiten und Karriereportale, die wirklich Bewerbungen bringen.',
        'auch_fuer': 'Quereinsteiger',
        'veroeffentlicht': '2026-08-26',
        'gueltig_bis': '2026-11-26',
        'pensum': 'Vollzeit',
        'zeiten': '08:00 bis 17:00 Uhr',
        'gehalt': None,
        'bild': 'ao-consulting-karriereportal-am-bildschirm',
        'bild_alt': 'Zwei Mitarbeitende der AO Consulting arbeiten gemeinsam an einem Karriereportal am Bildschirm',
        'bild_fokus': '50% 30%',
        'aufgaben': [
            'Aufbau und Pflege von Webseiten auf WordPress-Basis, hauptsächlich mit dem Divi-Theme',
            'Erstellung neuer Karriereportale und Unterseiten nach bestehenden Vorlagen',
            'Anpassung von Layouts, Modulen, Texten und Bildern',
            'Technische Grundprüfungen: Ladezeiten, mobile Darstellung, einfache Fehlerbehebung und das Testen auf verschiedenen Geräten',
            'Gelegentliche Unterstützung bei internen digitalen Projekten',
        ],
        'qualifikationen': [
            'Erste Erfahrung mit WordPress, vorzugsweise mit dem Divi-Theme, sowie ein Grundverständnis für Aufbau und Struktur von Webseiten',
            'Lust, Neues zu lernen und sich in WordPress-Themen einzuarbeiten',
            'Zuverlässigkeit, Eigenständigkeit und ein gutes Auge für Layouts',
            'Quereinsteiger sind willkommen, solange Motivation und Lernbereitschaft da sind',
        ],
        'benefits_extra': ['Homeoffice nach der Einarbeitung'],
    },
]

for _s in STELLEN:
    _s.setdefault('benefits', BENEFITS_STANDARD + _s.get('benefits_extra', []))
