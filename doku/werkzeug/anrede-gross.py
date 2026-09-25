#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Schreibt die Anrede gross: Du, Dich, Dir, Dein und alle Beugungen.
Regel der AO Consulting GmbH fuer alle Texte an Bewerber und Kunden.

Angefasst wird nur sichtbarer Text und die Inhalte von alt, title, aria-label,
placeholder und content. Tags, Adressen, Klassennamen, Skripte und Stilvorlagen
bleiben unberuehrt, sonst wird aus einem Verweis schnell ein toter Verweis.

Aufruf:  python3 ../werkzeug/anrede-gross.py datei [datei ...]
"""
import re, sys, io

WOERTER = r'(?:du|dich|dir|dein|deine|deinem|deinen|deiner|deines|deins)'
MUSTER = re.compile(r'\b' + WOERTER + r'\b')

def gross(m):
    return m.group(0)[0].upper() + m.group(0)[1:]

def text_bearbeiten(t):
    return MUSTER.sub(gross, t)

def html_bearbeiten(s):
    teile = re.split(r'(<script\b.*?</script>|<style\b.*?</style>|<[^>]+>)', s, flags=re.S | re.I)
    raus = []
    for teil in teile:
        if not teil:
            continue
        if teil.startswith('<'):
            # In Tags nur die Werte der Attribute anfassen, die der Mensch liest.
            def attr(m):
                return '%s="%s"' % (m.group(1), text_bearbeiten(m.group(2)))
            teil = re.sub(r'\b(alt|title|aria-label|placeholder|content)="([^"]*)"', attr, teil)
            raus.append(teil)
        else:
            raus.append(text_bearbeiten(teil))
    return ''.join(raus)

def python_bearbeiten(s):
    # Nur Zeichenketten in einfachen Anfuehrungszeichen, das ist das Format der
    # Stellendaten. Schluessel und Feldnamen enthalten die Woerter nicht.
    return re.sub(r"'([^'\\\n]*)'", lambda m: "'" + text_bearbeiten(m.group(1)) + "'", s)

if __name__ == '__main__':
    for pfad in sys.argv[1:]:
        s = io.open(pfad, encoding='utf-8').read()
        neu = python_bearbeiten(s) if pfad.endswith('.py') else html_bearbeiten(s)
        if neu != s:
            io.open(pfad, 'w', encoding='utf-8').write(neu)
            n = sum(1 for _ in MUSTER.finditer(s))
            print('%-52s %d Stellen' % (pfad.split('/')[-1], n))
        else:
            print('%-52s unveraendert' % pfad.split('/')[-1])
