#!/usr/bin/env python3
"""Packt die Karriereseite zu einer einzigen HTML-Datei: Bilder, Schriften,
Stilvorlagen und Skripte eingebettet, kein Fremdserver, laeuft per Doppelklick.
Aufruf im Ordner website/:  python3 ../werkzeug/bauen-einzeldatei.py ZIEL.html"""
import re, base64, os, sys, pathlib

ziel = sys.argv[1] if len(sys.argv) > 1 else 'AO-Karriereseite.html'
s = open('index.html', encoding='utf-8').read()
gesamt = 0

CSS_LISTE = re.findall(r'<link rel="stylesheet" href="(assets/[^"?]+)[^"]*"', s)
JS_LISTE  = re.findall(r'<script src="(assets/[^"?]+)[^"]*"[^>]*></script>', s)
assert len(CSS_LISTE) == len(set(CSS_LISTE)) and len(JS_LISTE) == len(set(JS_LISTE)), 'doppelte Bausteine'
TYPEN = {'.webp':'image/webp', '.jpg':'image/jpeg', '.jpeg':'image/jpeg',
         '.png':'image/png', '.svg':'image/svg+xml', '.woff2':'font/woff2'}

def datauri(pfad):
    global gesamt
    with open(pfad, 'rb') as f:
        b = f.read()
    gesamt += len(b)
    return 'data:%s;base64,%s' % (TYPEN[pathlib.Path(pfad).suffix.lower()],
                                  base64.b64encode(b).decode())

# 1) In <picture> nur das WebP behalten, das JPG waere doppeltes Gewicht
def nur_webp(m):
    block = m.group(0)
    q = re.search(r'<source srcset="(img/[^"]+\.webp)" type="image/webp">\s*', block)
    if not q:
        return block
    webp = q.group(1)
    block = block.replace(q.group(0), '')
    return re.sub(r'(<img[^>]*?)src="img/[^"]+"',
                  lambda mm: mm.group(1) + 'src="%s"' % webp, block, count=1)
s = re.sub(r'<picture[^>]*>.*?</picture>', nur_webp, s, flags=re.S)

# 2) Alle uebrigen Bildverweise einbetten
def bild(m):
    pfad = m.group(2).split('?')[0]
    return '%s="%s"' % (m.group(1), datauri(pfad)) if os.path.exists(pfad) else m.group(0)
s = re.sub(r'(src|href)="(img/[^"]+)"', bild, s)

# 3) Stilvorlagen in der Reihenfolge, in der sie in der Seite stehen,
#    samt Schriften und Hintergrundbildern darin
def css_inline(pfad):
    c = open(pfad, encoding='utf-8').read()
    def u(m):
        rel = m.group(1).replace('../', '')
        return 'url("%s")' % datauri(rel) if os.path.exists(rel) else m.group(0)
    return re.sub(r'url\("(\.\./(?:fonts|img)/[^"]+)"\)', u, c)

css = '\n'.join(css_inline(pfad) for pfad in CSS_LISTE)
s = re.sub(r'<link rel="stylesheet"[^>]*>\s*', '', s)
s = re.sub(r'<link rel="preload"[^>]*>\s*', '', s)
s = s.replace('</head>', '<style>\n' + css + '\n</style>\n</head>')

# 4) Skripte in der Reihenfolge der Seite. </script in Zeichenketten maskieren,
#    sonst schliesst der Browser den Block zu frueh.
js = [open(pfad, encoding='utf-8').read().replace('</script', r'<\/script')
      for pfad in JS_LISTE]
s = re.sub(r'<script src="assets/[^"]*"[^>]*></script>\s*', '', s)
s = s.replace('</body>', '<script>\n' + '\n;\n'.join(js) + '\n</script>\n</body>', 1)

# 5) Hinweis im Band: eine Einzeldatei kann nichts verschicken
s = s.replace('interne Vorschau',
              'Einzeldatei zum Weitergeben · das Bewerbungsformular verschickt hier nichts')

open(ziel, 'w', encoding='utf-8').write(s)
print('eingebettet: %.1f MB Rohdaten, Datei: %.1f MB' % (gesamt/1e6, len(s.encode())/1e6))
