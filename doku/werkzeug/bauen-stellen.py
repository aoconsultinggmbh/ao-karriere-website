#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Erzeugt aus stellen-daten.py:
     stellen/<schluessel>.html   eine Unterseite je Stelle, mit JobPosting
     index.html                  die Stellenliste zwischen den Marken
     sitemap.xml                 alle Seiten
Aufruf im Ordner website/:  python3 ../werkzeug/bauen-stellen.py
"""
import os, re, json, html, datetime, importlib.util, sys

BASIS = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location('daten', os.path.join(BASIS, 'stellen-daten.py'))
d = importlib.util.module_from_spec(spec); spec.loader.exec_module(d)
FIRMA, AP, KUNUNU, STELLEN = d.FIRMA, d.ANSPRECHPARTNER, d.KUNUNU, d.STELLEN

def ansprechpartner_fuer(s):
    # Regel aus stellen-daten.py: Vertrieb -> Admir, alles andere -> Ovidiu.
    schluessel = s.get('ansprechpartner') or d.ANSPRECHPARTNER_NACH_BEREICH.get(
        s.get('bereich'), d.ANSPRECHPARTNER_STANDARD)
    return d.PERSONEN[schluessel]

FEHLT = []   # Hinweise, die am Ende des Laufs ausgegeben werden

# Route planen: nur ein Verweis auf Google Maps (Maps URLs), keine Einbettung.
# Dadurch geht beim Laden keine Anfrage an Google und es braucht keine Einwilligung.
ROUTE = ('https://www.google.com/maps/dir/?api=1&amp;destination='
         'AO%20Consulting%20GmbH%2C%20Zeiloch%2013%2C%2076646%20Bruchsal')
ADRESSE = 'https://ao-karriere.de/'

def e(t):
    return html.escape(str(t), quote=False)

HAKEN = '<svg aria-hidden="true"><use href="#ic-haken"/></svg>'

def li(punkte, klasse='', haken=True):
    k = ' class="%s"' % klasse if klasse else ''
    z = HAKEN if haken else ''
    return '\n'.join('      <li%s>%s%s</li>' % (k, z, e(p)) for p in punkte)

AMPEL_TEXT = {'aktiv': 'Online', 'initiativ': 'Initiativ bewerben', 'besetzt': 'Nicht mehr offen'}
KNOPF_TEXT = {'aktiv': 'Jetzt bewerben', 'initiativ': 'Initiativ bewerben', 'besetzt': 'Stelle ist besetzt'}

# ---------------------------------------------------------------- JobPosting
def jobposting(s):
    """Die Auszeichnung für Google for Jobs. Bewusst nur die Felder, die Google
    auswertet. Alles andere landet im Text, nicht in erfundenen Feldern."""
    beschreibung = ''.join(
        ['<p>%s</p>' % e(s['kurz'])] +
        ['<h3>Aufgaben</h3><ul>'] + ['<li>%s</li>' % e(x) for x in s['aufgaben']] + ['</ul>'] +
        ['<h3>Qualifikationen</h3><ul>'] + ['<li>%s</li>' % e(x) for x in s['qualifikationen']] + ['</ul>'] +
        ['<h3>Das bieten wir</h3><ul>'] + ['<li>%s</li>' % e(x) for x in s['benefits']] + ['</ul>'] +
        ['<h3>Über uns</h3>'] + ['<p>%s</p>' % e(a) for a in d.EINSTIEG] +
        ['<p>Arbeitszeit: %s, %s. Arbeitsort: %s, %s %s.</p>'
         % (e(s['pensum']), e(s['zeiten']), e(FIRMA['strasse']), e(FIRMA['plz']), e(FIRMA['ort']))])

    j = {
        '@context': 'https://schema.org',
        '@type': 'JobPosting',
        'title': s['titel'],
        'description': beschreibung,
        'identifier': {'@type': 'PropertyValue', 'name': FIRMA['name'], 'value': s['schluessel']},
        'datePosted': s['veroeffentlicht'],
        'employmentType': 'FULL_TIME' if s['pensum'].lower().startswith('voll') else 'PART_TIME',
        'hiringOrganization': {
            '@type': 'Organization',
            'name': FIRMA['name'],
            'sameAs': FIRMA['seite'],
            'logo': FIRMA['logo'],
        },
        'jobLocation': {
            '@type': 'Place',
            'address': {
                '@type': 'PostalAddress',
                'streetAddress': FIRMA['strasse'],
                'addressLocality': FIRMA['ort'],
                'addressRegion': FIRMA['region'],
                'postalCode': FIRMA['plz'],
                'addressCountry': FIRMA['land'],
            },
        },
        'directApply': True,
    }
    # Eine besetzte Stelle laeuft gegenueber Google ab, sonst bleibt sie im Index.
    if s['status'] == 'besetzt':
        j['validThrough'] = (datetime.date.today() - datetime.timedelta(days=1)).isoformat()
    elif s.get('gueltig_bis'):
        j['validThrough'] = s['gueltig_bis']
    # Anforderungen (von Google als Beta ausgewertet). Passt genau zu
    # Quereinsteigern: "keine Voraussetzungen" statt Schweigen.
    if s.get('ausbildung_noetig') is False:
        j['educationRequirements'] = 'no requirements'
    if s.get('erfahrung_noetig') is False:
        j['experienceRequirements'] = 'no requirements'
    if s.get('gehalt'):
        mn, mx, einheit = s['gehalt']
        j['baseSalary'] = {'@type': 'MonetaryAmount', 'currency': 'EUR',
                           'value': {'@type': 'QuantitativeValue', 'minValue': mn,
                                     'maxValue': mx, 'unitText': einheit}}
    return json.dumps(j, ensure_ascii=False, indent=2)

def brotkrume(s):
    return json.dumps({
        '@context': 'https://schema.org', '@type': 'BreadcrumbList',
        'itemListElement': [
            {'@type': 'ListItem', 'position': 1, 'name': 'Karriere bei AO Consulting', 'item': ADRESSE},
            {'@type': 'ListItem', 'position': 2, 'name': 'Offene Stellen', 'item': ADRESSE + '#stellen'},
            {'@type': 'ListItem', 'position': 3, 'name': s['titel'],
             'item': ADRESSE + 'stellen/' + s['schluessel'] + '.html'},
        ]}, ensure_ascii=False, indent=2)

# ------------------------------------------------------- Bausteine aus index.html
QUELLE = open('index.html', encoding='utf-8').read()

def hol(start, ende, text=None):
    t = text if text is not None else QUELLE
    i = t.find(start); assert i != -1, start
    j = t.find(ende, i); assert j != -1, ende
    return t[i:j + len(ende)]

SPRITE   = hol('<svg class="sprite"', '</svg>') if '<svg class="sprite"' in QUELLE else hol('<svg', '</svg>')
# Ohne schliessendes Anfuehrungszeichen suchen: die Startseite traegt seit
# 21.09. 'kopf kopf--hell' und die alte Suche lief ins Leere.
KOPF     = hol('<header class="kopf', '</header>')
FUSS     = hol('<footer class="fuss"', '</footer>')
MOBIL    = hol('<div class="mobil-leiste', '</div>')
EINWILL  = hol('<script>\nwindow.AO_EINWILLIGUNG', '</script>')
# Das Bewerbungsformular steht seit 21.09. nicht mehr auf der Startseite: beworben
# wird je Stelle. Es liegt deshalb als eigener Baustein im Werkzeugordner.
FORMULAR = open(os.path.join(BASIS, 'formular.html'), encoding='utf-8').read()

def kopf_hell(block):
    """Die Unterseite hat keine dunkle Buehne oben. Ohne kopf--hell stuende ein
    weisses Logo auf weissem Grund. Traegt die Vorlage die Klasse schon, bleibt
    sie unberuehrt."""
    if 'kopf--hell' in block:
        return block
    return block.replace('class="kopf"', 'class="kopf kopf--hell"', 1)

def auf_startseite(block):
    """Verweise, die auf der Startseite Anker sind, zeigen von der Unterseite
    aus auf die Startseite. Sonst laufen sie ins Leere."""
    block = re.sub(r'href="#(top|stellen|team|benefits|ablauf|faq)"', r'href="../index.html#\1"', block)
    block = block.replace('href="#bewerben"', 'href="#bewerben"')
    block = re.sub(r'(src|href)="(img/|assets/|fonts/)', r'\1="../\2', block)
    block = block.replace('href="rechtliches/', 'href="../rechtliches/')
    return block

# ----------------------------------------------------------------- Unterseite
def seite(s):
    ampel = ('<span class="ampel"><span class="ampel__punkt" aria-hidden="true"></span>%s</span>'
             % e(AMPEL_TEXT[s['status']]))
    gehalt_zeile = ''
    if s.get('gehalt'):
        mn, mx, einheit = s['gehalt']
        wort = 'im Monat' if einheit == 'MONTH' else 'im Jahr'
        gehalt_zeile = '<div><dt>Gehalt</dt><dd>%s bis %s Euro %s</dd></div>' % (e(mn), e(mx), wort)

    # Das Auswahlfeld kommt aus den Stellendaten, nicht aus dem HTML der
    # Startseite. Nur so passt die Vorauswahl immer zur Unterseite.
    ap = ansprechpartner_fuer(s)
    ap_tel_zeile = ap_wa_zeile = ''
    if ap.get('telefon'):
        ap_tel_zeile = ('          <li><a href="tel:%s"><svg aria-hidden="true"><use href="#ic-tel"/></svg>%s</a></li>\n'
                        % (ap['telefon'], e(ap['telefon_sichtbar'])))
    else:
        FEHLT.append('%s: keine Telefonnummer fuer %s' % (s['schluessel'], ap['name']))
    if ap.get('whatsapp'):
        ap_wa_zeile = ('          <li><a class="ist-wa" href="%s" target="_blank" rel="noopener"><svg aria-hidden="true"><use href="#ic-whatsapp"/></svg>WhatsApp schreiben</a></li>\n'
                       % ap['whatsapp'])
    else:
        FEHLT.append('%s: kein WhatsApp fuer %s' % (s['schluessel'], ap['name']))

    # Ovidiu 25.09.2026: Wer auf der Stellenseite ist, bewirbt sich auf genau
    # diese Stelle. Kein Auswahlfeld, die Stelle steht sichtbar oben im Formular
    # und geht als verstecktes Feld mit, weil bewerbung.php sie braucht.
    wert = s['titel'] + (' (Initiativbewerbung)' if s['status'] == 'initiativ' else '')
    formular = FORMULAR.replace('<!--STELLE-KOPF-->',
        '      <p class="formular__stelle">für <b>%s</b></p>' % e(s['titel']))
    formular = formular.replace('<!--STELLE-->',
        '      <input type="hidden" name="stelle" value="%s">' % e(wert))
    assert 'name="stelle"' in formular, 'verstecktes Feld fuer die Stelle fehlt'
    assert '<!--STELLE' not in formular, 'Platzhalter im Formular nicht ersetzt'
    # Im Formularkasten steht derselbe Ansprechpartner wie in der Karte rechts.
    formular = formular.replace('<dt>Ansprechpartner</dt><dd>Ovidiu Rieger</dd>',
                                '<dt>Ansprechpartner</dt><dd>%s</dd>' % e(ap['name']))
    tel_alt = '<dt>Telefon</dt><dd><a href="tel:+4917685933551">0176 85933551</a></dd>'
    assert tel_alt in formular, 'Telefonzeile im Formular nicht gefunden'
    formular = formular.replace(tel_alt, ('<dt>Telefon</dt><dd><a href="tel:%s">%s</a></dd>'
                                          % (ap['telefon'], e(ap['telefon_sichtbar'])))
                                if ap.get('telefon') else '')
    formular = auf_startseite(formular)
    formular = formular.replace('action="bewerbung.php"', 'action="../bewerbung.php"')
    formular = formular.replace('<h2 id="bewerben-titel">Bewerben dauert <span class="hl">zwei Minuten</span></h2>',
                                '<h2 id="bewerben-titel">Bewirb Dich auf <span class="hl">diese Stelle</span></h2>')

    # Titel: die Stelle zuerst, die Marke kurz dahinter. Vorher 77 bis 89 Zeichen.
    titel_seite = '%s in %s | AO Consulting' % (s['titel'], FIRMA['ort'])
    # Beschreibung: vorher fehlte nach dem Titel der Punkt ("(m/w/d) Du rufst ...").
    beschr = '%s in %s, %s. %s Bewerbung ohne Anschreiben.' % (
        s['titel'], FIRMA['ort'], s['pensum'], s['kurz'])

    return '''<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%(titel_seite)s</title>
<meta name="description" content="%(beschr)s">
<meta name="robots" content="noindex, nofollow">
<meta name="theme-color" content="#2b87da">
<link rel="canonical" href="%(adresse)sstellen/%(schluessel)s.html">
<meta property="og:type" content="website">
<meta property="og:title" content="%(titel_og)s">
<meta property="og:description" content="%(beschr)s">
<meta property="og:image" content="%(adresse)simg/%(bild)s.jpg">
<meta property="og:url" content="%(adresse)sstellen/%(schluessel)s.html">
<meta property="og:site_name" content="AO Consulting">
<meta property="og:locale" content="de_DE">
<link rel="icon" href="../img/favicon.svg?v=1" type="image/svg+xml">
<link rel="icon" href="../img/favicon-32.png?v=1" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="../img/apple-touch-icon.png?v=1">
<link rel="stylesheet" href="../assets/stil.css?v=1">
<link rel="stylesheet" href="../assets/einwilligung.css?v=1">
<link rel="stylesheet" href="../assets/barrierefreiheit.css?v=1">
<link rel="stylesheet" href="../assets/stellen-ampel.css?v=1">
<link rel="stylesheet" href="../assets/karriere.css?v=1">
<link rel="stylesheet" href="../assets/stelle.css?v=1">
%(einwilligung)s
<script type="application/ld+json">
%(jobposting)s
</script>
<script type="application/ld+json">
%(brotkrume)s
</script>
</head>
<body>
%(sprite)s

<a class="sprung" href="#inhalt">Zum Inhalt springen</a>
<a class="sprung" href="#bewerben">Zur Bewerbung springen</a>

<div class="entwurf-band" role="note">Entwurf Karriereseite &middot; Stand 18.09.2026 &middot; interne Vorschau</div>

%(kopf)s

<main id="inhalt" tabindex="-1">

<nav class="krume" aria-label="Sie sind hier">
  <div class="innen">
    <ol>
      <li><a href="../index.html">Karriere</a></li>
      <li><a href="../index.html#stellen">Offene Stellen</a></li>
      <li><span aria-current="page">%(titel)s</span></li>
    </ol>
  </div>
</nav>

<section class="stelle-seite" data-status="%(status)s" aria-labelledby="stelle-titel">
  <div class="innen stelle-seite__raster">

    <article class="stelle-seite__inhalt">
      <picture class="stelle-seite__bild">
        <source srcset="../img/%(bild)s.webp" type="image/webp">
        <img src="../img/%(bild)s.jpg" alt="%(bild_alt)s" width="1800" height="1200" style="object-position:%(bild_fokus)s" fetchpriority="high" decoding="async">
      </picture>

      <p class="stelle-seite__marken">%(ampel)s<span class="marker">%(ort)s</span><span class="marker">%(pensum)s</span></p>
      <h1 id="stelle-titel">%(titel)s</h1>
      <p class="einleitung">%(kurz)s</p>
      <p class="stelle-seite__auch">Passt auch für: %(auch_fuer)s.</p>
      <a class="knopf knopf--primaer knopf--gross" href="#bewerben">%(knopf)s</a>

      <h2><span class="hl gezeichnet">Über uns</span></h2>
      %(einstieg)s

      <h2><span class="hl gezeichnet">Aufgaben</span></h2>
      <ul class="stelle__punkte">
%(aufgaben)s
      </ul>

      <h2><span class="hl gezeichnet">Qualifikationen</span></h2>
      <ul class="stelle__punkte">
%(qualifikationen)s
      </ul>

      <h2><span class="hl gezeichnet">Das bieten wir</span></h2>
      <ul class="stelle__punkte">
%(benefits)s
      </ul>
    </article>

    <aside class="stelle-seite__spalte" aria-labelledby="ap-titel">
      <div class="ap">
        <h2 class="ap__titel" id="ap-titel">Dein Ansprechpartner</h2>
        <img class="ap__bild" src="../img/%(ap_bild)s.webp" alt="%(ap_name)s, %(ap_rolle)s der %(firma)s" width="360" height="360" loading="lazy" decoding="async">
        <p class="ap__name">%(ap_name)s</p>
        <p class="ap__rolle">%(ap_rolle)s</p>
        <ul class="ap__wege">
%(ap_tel_zeile)s%(ap_wa_zeile)s          <li><a href="mailto:%(ap_mail)s"><svg aria-hidden="true"><use href="#ic-mail"/></svg>%(ap_mail)s</a></li>
        </ul>
      </div>

      <dl class="eckdaten">
        <div><dt>Arbeitspensum</dt><dd>%(pensum)s</dd></div>
        <div><dt>Arbeitszeiten</dt><dd>%(zeiten)s</dd></div>
        <div><dt>Branche</dt><dd>Agentur für das Gesundheitswesen</dd></div>
        <div><dt>Arbeitsort</dt><dd>%(strasse)s<br>%(plz)s %(ort)s<br>%(region)s<br><a class="route" href="%(route)s" target="_blank" rel="noopener"><svg aria-hidden="true"><use href="#ic-pin"/></svg>Route planen</a></dd></div>
        %(gehalt_zeile)s
      </dl>

      <div class="kununu" data-kununu="%(kununu_widget)s">
        <a class="kununu__kern" href="%(kununu_link)s" target="_blank" rel="nofollow noopener">
          <span class="kununu__note"><b>%(kununu_note)s</b><span aria-hidden="true">von 5</span></span>
          <span class="kununu__text"><b>Bewertet auf kununu</b><span>%(kununu_prozent)s Prozent Weiterempfehlung bei %(kununu_anzahl)s Bewertungen</span></span>
        </a>
        <p class="kununu__hinweis">
          <button type="button" class="kununu__laden" data-kununu-laden>Siegel von kununu laden</button>
          <span>Dabei wird Deine IP-Adresse an kununu übertragen.</span>
        </p>
      </div>
    </aside>

  </div>
</section>

%(formular)s

</main>

%(fuss)s

%(mobil)s

<script src="../assets/einwilligung.js?v=1" defer></script>
<script src="../assets/barrierefreiheit.js?v=1" defer></script>
<script src="../assets/skript.js?v=1" defer></script>
<script src="../assets/karriere.js?v=1" defer></script>
</body>
</html>
''' % {
        'titel_seite': e(titel_seite), 'titel_og': e('%s in %s' % (s['titel'], FIRMA['ort'])),
        'beschr': e(beschr), 'adresse': ADRESSE, 'schluessel': s['schluessel'],
        'einwilligung': EINWILL, 'jobposting': jobposting(s), 'brotkrume': brotkrume(s),
        'sprite': SPRITE,
        # Die Unterseite hat keine dunkle Buehne oben. Ohne kopf--hell stuende
        # ein weisses Logo auf weissem Grund und die Brotkrume liefe darunter.
        'kopf': kopf_hell(auf_startseite(KOPF)),
        'fuss': auf_startseite(FUSS),
        'mobil': auf_startseite(MOBIL), 'formular': formular,
        'status': s['status'], 'ampel': ampel, 'knopf': e(KNOPF_TEXT[s['status']]),
        'titel': e(s['titel']), 'kurz': e(s['kurz']), 'auch_fuer': e(s['auch_fuer']),
        'bild': s['bild'], 'bild_alt': e(s['bild_alt']), 'bild_fokus': s.get('bild_fokus', '50% 30%'),
        'einstieg': '\n      '.join('<p>%s</p>' % e(a) for a in d.EINSTIEG),
        'aufgaben': li(s['aufgaben']), 'qualifikationen': li(s['qualifikationen']),
        'benefits': li(s['benefits']),
        'pensum': e(s['pensum']), 'zeiten': e(s['zeiten']), 'gehalt_zeile': gehalt_zeile,
        'route': ROUTE,
        'strasse': e(FIRMA['strasse']), 'plz': e(FIRMA['plz']), 'ort': e(FIRMA['ort']),
        'region': e(FIRMA['region']), 'firma': e(FIRMA['name']),
        'ap_bild': ap['bild'], 'ap_name': e(ap['name']), 'ap_rolle': e(ap['rolle']),
        'ap_tel_zeile': ap_tel_zeile, 'ap_wa_zeile': ap_wa_zeile, 'ap_mail': e(ap['mail']),
        'kununu_link': KUNUNU['link'].replace('&', '&amp;'), 'kununu_note': e(KUNUNU['note']), 'kununu_widget': KUNUNU['widget'],
        'kununu_prozent': e(KUNUNU['weiterempfehlung']), 'kununu_anzahl': e(KUNUNU['anzahl']),
    }

# ------------------------------------------------- Zahlen im Text der Startseite
# Frueher standen "Drei offene Stellen ansehen" und "alle drei offen" fest im
# HTML. Sobald eine Stelle auf initiativ sprang, log die Seite. Jetzt schreibt
# der Generator diese Saetze aus den Daten, sie koennen gar nicht mehr abweichen.
ZAHLWORT = {1:'Eine', 2:'Zwei', 3:'Drei', 4:'Vier', 5:'Fuenf', 6:'Sechs'}

def _wort(n, gross=True):
    w = ZAHLWORT.get(n, str(n))
    return w if gross else w.lower()

def texte_einsetzen(s):
    offen = [x for x in STELLEN if x['status'] == 'aktiv']
    initiativ = [x for x in STELLEN if x['status'] == 'initiativ']
    n, m = len(offen), len(initiativ)

    if n == 0:
        knopf = 'Initiativ bewerben'
        titel = 'Gerade keine Stelle offen, <span class="hl">initiativ geht immer</span>'
    elif n == 1:
        knopf = 'Die offene Stelle ansehen'
        titel = 'Eine Stelle ist offen, <span class="hl">initiativ geht immer</span>'
    else:
        knopf = '%s offene Stellen ansehen' % _wort(n)
        titel = '%s offene Stellen, <span class="hl">dazu jederzeit initiativ</span>' % _wort(n)

    # Kurz halten: die Ampel traegt ihre Beschriftung selbst, und wie viele
    # Stellen offen sind, sagt schon die Ueberschrift.
    umfang = {x['pensum'] for x in STELLEN}
    if len(umfang) == 1:
        teile = ['Alle Stellen sind in %s und in %s.' % (FIRMA['ort'], next(iter(umfang)))]
    else:
        teile = ['Alle Stellen sind in %s.' % FIRMA['ort']]
    if m:
        teile.append('Auch wenn eine Stelle gerade nicht ausgeschrieben ist, bewirb Dich '
                     'trotzdem. Eine Antwort bekommst Du in 48 bis 72 Stunden.')
    einleitung = ' '.join(teile)

    import re as _re
    for marke in ['<a class="knopf knopf--primaer knopf--gross" href="#stellen">',
                  '<h2 id="stellen-titel">']:
        assert marke in s, 'Auf der Startseite fehlt: ' + marke
    s = _re.sub(r'(<a class="knopf knopf--primaer knopf--gross" href="#stellen">)[^<]*(</a>)',
                lambda mm: mm.group(1) + knopf + mm.group(2), s, count=1)
    s = _re.sub(r'(<h2 id="stellen-titel">).*?(</h2>)',
                lambda mm: mm.group(1) + titel + mm.group(2), s, count=1, flags=_re.S)
    s = _re.sub(r'(<h2 id="stellen-titel">.*?</h2>\s*<p class="einleitung">).*?(</p>)',
                lambda mm: mm.group(1) + einleitung + mm.group(2), s, count=1, flags=_re.S)
    return s

# ------------------------------------------------- Stellenliste auf der Startseite
def liste_html():
    teile = []
    for s in STELLEN:
        ampel = ('<span class="ampel"><span class="ampel__punkt" aria-hidden="true"></span>%s</span>'
                 % e(AMPEL_TEXT[s['status']]))
        # Ort und Umfang stehen im Satz ueber der Liste, solange alle Stellen
        # gleich sind. Dann waeren sie auf jeder Karte doppelt. Nur wenn sich
        # der Umfang unterscheidet, bekommt die Karte ein Etikett dafuer.
        marken = [ampel]
        if len({x['pensum'] for x in STELLEN}) > 1:
            marken.append('<span class="marker">%s</span>' % e(s['pensum']))
        ziel = 'stellen/%s.html' % s['schluessel']
        # Ovidiu 25.09.2026: drei Stellen fuellten fast eine ganze Bildschirmseite.
        # Die Karte zeigt jetzt nur noch Status, Titel, einen Satz und den Knopf,
        # ohne Bild und ohne Aufgabenliste. Die Einzelheiten stehen auf der
        # Stellenseite. Mehrere Karten stehen nebeneinander.
        teile.append('''      <li class="stelle stelle--kompakt" data-status="%s">
        <p class="stelle__marken">
          %s
        </p>
        <h3><a href="%s">%s</a></h3>
        <p>%s</p>
        <a class="knopf knopf--primaer" href="%s">%s</a>
      </li>''' % (s['status'], '\n          '.join(marken), ziel, e(s['titel']),
                  e(s['kurz']), ziel, e('Stelle ansehen')))
    return '<ul class="stellen__liste reveal">\n' + '\n'.join(teile) + '\n    </ul>'

def auswahl_html(aktiv=None):
    """Das Auswahlfeld des Bewerbungsformulars. Eine Quelle fuer Startseite und
    alle Unterseiten, sonst laufen die Bezeichnungen auseinander."""
    zeilen = ['<option value="">Bitte auswählen</option>']
    for x in STELLEN:
        gewaehlt = ' selected' if aktiv and x['schluessel'] == aktiv else ''
        zeilen.append('<option%s>%s</option>' % (gewaehlt, e(x['titel'])))
    zeilen.append('<option>Initiativbewerbung</option>')
    return zeilen

def auswahl_einsetzen(text, aktiv=None):
    return re.sub(r'(<select id="b-stelle"[^>]*>).*?(</select>)',
                  lambda m: m.group(1) + '\n' + '\n'.join('          ' + o for o in auswahl_html(aktiv))
                            + '\n        ' + m.group(2),
                  text, flags=re.S)

def ende_der_liste(text, start):
    """Sucht das schliessende </ul> der Stellenliste und zaehlt dabei die
    verschachtelten Listen mit. Ohne das Mitzaehlen trifft die Suche das erste
    </ul> der Aufzaehlung INNERHALB der ersten Karte, und bei jedem Lauf bleibt
    ein Teil der alten Liste stehen. Genau das ist am 18.09. passiert: aus drei
    Karten wurden dreizehn."""
    tiefe = 0
    i = start
    while i < len(text):
        auf = text.find('<ul', i)
        zu = text.find('</ul>', i)
        if zu == -1:
            raise AssertionError('Stellenliste hat kein schliessendes </ul>')
        if auf != -1 and auf < zu:
            tiefe += 1
            i = auf + 3
            continue
        tiefe -= 1
        if tiefe == 0:
            return zu + 5
        i = zu + 5
    raise AssertionError('Stellenliste hat kein schliessendes </ul>')

def firmendaten_einsetzen(s):
    """Fuellt die markierten Stellen in der Startseite aus den Firmendaten.
    Aktuell nur die Buerozeiten in der FAQ-Antwort mit dem Ortsbezug.
    Steht dort None, faellt der Satzteil ersatzlos weg, statt eine Zahl zu
    erfinden."""
    z = FIRMA.get('oeffnungszeiten')
    satz = (' Das Büro ist %s besetzt,' % z) if z else ''
    return re.sub(r'<span data-firma="zeiten">.*?</span>',
                  '<span data-firma="zeiten">%s</span>' % satz, s, flags=re.S)

def liste_einsetzen():
    s = open('index.html', encoding='utf-8').read()
    i = s.find('<ul class="stellen__liste')
    assert i != -1, 'Stellenliste in index.html nicht gefunden'
    j = ende_der_liste(s, i)
    s = s[:i] + liste_html() + s[j:]
    if 'id="b-stelle"' in s:      # nur falls die Startseite doch ein Formular hat
        s = auswahl_einsetzen(s)
    s = firmendaten_einsetzen(s)
    s = texte_einsetzen(s)
    if not FIRMA.get('oeffnungszeiten'):
        print('Hinweis: Buerozeiten stehen nicht in stellen-daten.py, '
              'die FAQ-Antwort nennt sie deshalb nicht.')
    open('index.html', 'w', encoding='utf-8').write(s)
    # Gegenprobe: genau so viele Karten wie Stellen, sonst ist etwas stehengeblieben.
    n = len(re.findall(r'<li class="stelle[ "]', s))
    assert n == len(STELLEN), 'Stellenliste hat %d Karten statt %d' % (n, len(STELLEN))

# --------------------------------------------------------------------- sitemap
def sitemap():
    heute = datetime.date.today().isoformat()
    # Google wertet lastmod nur, wenn es stimmt. Bei den Stellen gilt deshalb das
    # Datum der Veroeffentlichung oder, falls eingetragen, der letzten Aenderung.
    eintraege = [(ADRESSE, '1.0', heute)] + [
        (ADRESSE + 'stellen/' + s['schluessel'] + '.html', '0.9', s.get('geaendert') or s['veroeffentlicht'])
        for s in STELLEN if s['status'] != 'besetzt']
    zeilen = ['<?xml version="1.0" encoding="UTF-8"?>',
              '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for adr, prio, datum in eintraege:
        zeilen += ['  <url>', '    <loc>%s</loc>' % adr,
                   '    <lastmod>%s</lastmod>' % datum,
                   '    <priority>%s</priority>' % prio, '  </url>']
    zeilen.append('</urlset>')
    open('sitemap.xml', 'w', encoding='utf-8').write('\n'.join(zeilen) + '\n')

# ------------------------------------------------------------ Gleichstellung
# Ovidiu 25.09.2026: "unsere klassische Gleichstellungshinweis-Unterseite".
# Der Text ist wortgleich von https://ao-karriere.de/hinweis-zur-gleichstellung/
# uebernommen. Beim Livegang die alte Adresse auf diese Datei umleiten.
GLEICHSTELLUNG_TEXT = ('Aus Gründen der besseren Lesbarkeit wird bei Personenbezeichnungen und '
    'personenbezogenen Hauptwörtern auf unserer Webseite und externen Stellenausschreibungen '
    'sowie Social Media Beiträgen die männliche Form verwendet. Entsprechende Begriffe gelten '
    'im Sinne der Gleichbehandlung grundsätzlich für alle Geschlechter.')

def gleichstellung():
    return """<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Hinweis zur Gleichstellung | Karriere bei AO Consulting</title>
<meta name="description" content="Hinweis zur Gleichstellung der AO Consulting GmbH: Personenbezeichnungen gelten für alle Geschlechter.">
<meta name="robots" content="noindex, nofollow">
<meta name="theme-color" content="#2b87da">
<link rel="canonical" href="%(adresse)srechtliches/hinweis-zur-gleichstellung.html">
<link rel="icon" href="../img/favicon.svg?v=1" type="image/svg+xml">
<link rel="icon" href="../img/favicon-32.png?v=1" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="../img/apple-touch-icon.png?v=1">
<link rel="stylesheet" href="../assets/stil.css?v=1">
<link rel="stylesheet" href="../assets/einwilligung.css?v=1">
<link rel="stylesheet" href="../assets/barrierefreiheit.css?v=1">
<link rel="stylesheet" href="../assets/karriere.css?v=1">
%(einwilligung)s
</head>
<body>
%(sprite)s
<a class="sprung" href="#inhalt">Zum Inhalt springen</a>
%(kopf)s
<main id="inhalt" tabindex="-1">

<section class="rechtstext" aria-labelledby="gl-titel">
  <div class="innen rechtstext__innen">
    <p class="kicker">Rechtliches</p>
    <h1 id="gl-titel">Hinweis zur <span class="hl gezeichnet">Gleichstellung</span></h1>
    <div class="rechtstext__block">
      <h2>Gleichstellungshinweis</h2>
      <p>%(text)s</p>
    </div>
    <p><a class="knopf knopf--primaer" href="../index.html#stellen">Zu den Stellen</a></p>
  </div>
</section>

</main>

%(fuss)s

%(mobil)s

<script src="../assets/einwilligung.js?v=1" defer></script>
<script src="../assets/barrierefreiheit.js?v=1" defer></script>
<script src="../assets/skript.js?v=1" defer></script>
</body>
</html>
""" % {'adresse': ADRESSE, 'einwilligung': EINWILL, 'sprite': SPRITE,
       'kopf': kopf_hell(auf_startseite(KOPF)), 'fuss': auf_startseite(FUSS),
       'mobil': auf_startseite(MOBIL), 'text': e(GLEICHSTELLUNG_TEXT)}

# ------------------------------------------------------------------ Indeed
# Offizieller Weg fuer Arbeitgeber ohne Bewerbermanagement-System: ein XML-Feed,
# den Indeed von einer festen Adresse abholt (laut docs.indeed.com viermal am Tag).
# Aufbau nach https://docs.indeed.com/job-sync-xml/xml-feed, Stand 25.09.2026.
# Regeln von Indeed, die hier umgesetzt sind:
#  - Der Feed muss ALLE Stellen der Karriereseite enthalten, Teilmengen nimmt
#    Indeed nicht an. Besetzte Stellen fehlen, sie sind nicht mehr ausgeschrieben.
#  - Stellen, die nur Bewerber fuer spaeter sammeln, markiert Indeed mit
#    TALENT_POOL: sie stehen im Feed, erscheinen aber nicht in der Suche. Das
#    sind bei uns die gelben Stellen. Wer das anders will, stellt den Schalter um.
#  - Alle Texte in CDATA, Datum im Format ISO 8601.
#  - <email> muss die Adresse des Arbeitgeberkontos bei Indeed sein.
INDEED_DATEI = 'indeed.xml'
INDEED_MAIL = 'jobs@ao-karriere.de'          # OFFEN: Adresse des Indeed-Kontos bestaetigen
INDEED_GELB_ALS_TALENTPOOL = True            # Indeed-Regel, siehe oben
INDEED_KATEGORIE = {'vertrieb': 'Vertrieb', 'backoffice': 'Büro, Verwaltung',
                    'webdesign': 'Webdesign, IT'}

def _cdata(text):
    return '<![CDATA[%s]]>' % str(text).replace(']]>', ']]]]><![CDATA[>')

def indeed_feed():
    zeilen = ['<?xml version="1.0" encoding="utf-8"?>', '<source>']
    for s in STELLEN:
        if s['status'] == 'besetzt':
            continue
        # Dieselbe Beschreibung wie fuer Google for Jobs, damit beide gleich lauten.
        beschreibung = json.loads(jobposting(s))['description']
        felder = [
            ('title', s['titel']),
            ('date', s['veroeffentlicht'] + 'T08:00:00Z'),
            ('referencenumber', s['schluessel']),
            ('requisitionid', s['schluessel']),
            ('url', ADRESSE + 'stellen/' + s['schluessel'] + '.html'),
            ('company', FIRMA['name']),
            ('sourcename', FIRMA['name']),
            ('city', FIRMA['ort']),
            ('state', FIRMA['region']),
            ('country', FIRMA['land']),
            ('postalcode', FIRMA['plz']),
            ('streetaddress', FIRMA['strasse']),
            ('email', INDEED_MAIL),
            ('description', beschreibung),
            ('jobtype', 'fulltime' if s['pensum'].lower().startswith('voll') else 'parttime'),
        ]
        if s.get('gehalt'):
            mn, mx, einheit = s['gehalt']
            felder.append(('salary', '%s bis %s EUR %s' % (mn, mx, 'im Monat' if einheit == 'MONTH' else 'im Jahr')))
        if s.get('gueltig_bis'):
            felder.append(('expirationdate', s['gueltig_bis']))
        if INDEED_KATEGORIE.get(s.get('bereich')):
            felder.append(('category', INDEED_KATEGORIE[s['bereich']]))
        if s['status'] == 'initiativ' and INDEED_GELB_ALS_TALENTPOOL:
            felder.append(('hide_from_indeed_search', 'TALENT_POOL'))
        zeilen.append('  <job>')
        zeilen += ['    <%s>%s</%s>' % (k, _cdata(v), k) for k, v in felder]
        zeilen.append('  </job>')
    zeilen.append('</source>')
    open(INDEED_DATEI, 'w', encoding='utf-8').write('\n'.join(zeilen) + '\n')
    return len([x for x in STELLEN if x['status'] != 'besetzt'])

# --------------------------------------------------------------- Talent.com
# Zweiter Feed, gleiche Daten. Aufbau nach https://www.talent.com/integrations,
# Stand 25.09.2026. Unterschiede zu Indeed: <dateposted> statt <date>, Ablauf im
# Format MM-dd-yyyyTHH:mm:ssZ, jobtype "Full time", Logo als PNG (128 x 128).
# Kein <cpc>: das waere bezahlte Platzierung, wir wollen die kostenlose.
# Eine Talent-Pool-Markierung wie bei Indeed kennt Talent.com nicht, die gelben
# Stellen stehen deshalb normal drin (wie bei Google, Entscheidung Ovidiu).
TALENT_DATEI = 'talent.xml'

def talent_feed():
    jetzt = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    zeilen = ['<?xml version="1.0" encoding="utf-8"?>', '<source>',
              '  <lastbuilddate>%s</lastbuilddate>' % _cdata(jetzt)]
    for s in STELLEN:
        if s['status'] == 'besetzt':
            continue
        beschreibung = json.loads(jobposting(s))['description']
        felder = [
            ('referencenumber', s['schluessel']),
            ('title', s['titel']),
            ('company', FIRMA['name']),
            ('city', FIRMA['ort']),
            ('state', FIRMA['region']),
            ('country', FIRMA['land']),
            ('dateposted', s['veroeffentlicht'] + 'T08:00:00Z'),
            ('url', ADRESSE + 'stellen/' + s['schluessel'] + '.html'),
            ('description', beschreibung),
            ('streetaddress', FIRMA['strasse']),
            ('postalcode', FIRMA['plz']),
            ('jobtype', 'Full time' if s['pensum'].lower().startswith('voll') else 'Part time'),
            ('isremote', 'no'),
            ('logo', ADRESSE + 'img/ao-consulting-logo-128.png'),
        ]
        if s.get('gueltig_bis'):
            j, m, t = s['gueltig_bis'].split('-')
            felder.append(('expirationdate', '%s-%s-%sT23:59:59Z' % (m, t, j)))
        zeilen.append('  <job>')
        zeilen += ['    <%s>%s</%s>' % (k, _cdata(v), k) for k, v in felder]
        if s.get('gehalt'):
            mn, mx, einheit = s['gehalt']
            zeilen += ['    <salary>',
                       '      <salary_max>%s</salary_max>' % _cdata(mx),
                       '      <salary_min>%s</salary_min>' % _cdata(mn),
                       '      <salary_currency>%s</salary_currency>' % _cdata('EUR'),
                       '      <period>%s</period>' % _cdata('month' if einheit == 'MONTH' else 'year'),
                       '      <type>%s</type>' % _cdata('BASE_SALARY'),
                       '    </salary>']
        zeilen.append('  </job>')
    zeilen.append('</source>')
    open(TALENT_DATEI, 'w', encoding='utf-8').write('\n'.join(zeilen) + '\n')
    return len([x for x in STELLEN if x['status'] != 'besetzt'])

# ------------------------------------------------------------------------ Lauf
if __name__ == '__main__':
    os.makedirs('stellen', exist_ok=True)
    for s in STELLEN:
        ziel = os.path.join('stellen', s['schluessel'] + '.html')
        open(ziel, 'w', encoding='utf-8').write(seite(s))
        print('%-46s %s  %6d Zeichen' % (ziel, s['status'].ljust(9), os.path.getsize(ziel)))
    liste_einsetzen(); print('index.html: Stellenliste eingesetzt')
    os.makedirs('rechtliches', exist_ok=True)
    open(os.path.join('rechtliches', 'hinweis-zur-gleichstellung.html'), 'w', encoding='utf-8').write(gleichstellung())
    print('rechtliches/hinweis-zur-gleichstellung.html: erzeugt')
    sitemap(); print('sitemap.xml: %d Adressen' % (1 + len([x for x in STELLEN if x['status'] != 'besetzt'])))
    n = indeed_feed(); print('%s: %d Stellen fuer Indeed' % (INDEED_DATEI, n))
    n = talent_feed(); print('%s: %d Stellen fuer Talent.com' % (TALENT_DATEI, n))
    if INDEED_MAIL == 'jobs@ao-karriere.de':
        FEHLT.append('indeed.xml: Mailadresse des Indeed-Kontos noch nicht bestaetigt')
    for f in FEHLT: print('Hinweis:', f)
