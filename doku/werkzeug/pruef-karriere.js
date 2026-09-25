/* Abnahmepruefung der Karriereseite.
   Aufruf:  node pruef.js <ordner-mit-index.html>
   Geprueft wird jede Seite in mehreren Breiten. Der Lauf endet mit Code 1,
   sobald ein Punkt rot ist, damit man ihn nicht uebersehen kann.            */
const { chromium } = require('/opt/node-tools/node_modules/playwright');
const fs = require('fs'), path = require('path');

const wurzel = process.argv[2] || process.cwd();
// Ueber http pruefen, nicht ueber file://. Unter file:// meldet der Browser
// Schriften als CORS-Fehler, die es auf dem Server nicht gibt.
// Vorher im Ordner starten:  python3 -m http.server 8321
const EIGEN = '127.0.0.1:8321';
const BASIS = 'http://' + EIGEN + '/';
const seiten = ['index.html'].concat(...['stellen', 'rechtliches'].map(o =>
  fs.existsSync(path.join(wurzel, o))
    ? fs.readdirSync(path.join(wurzel, o)).filter(f => f.endsWith('.html')).map(f => o + '/' + f)
    : []));
const breiten = [1920, 1512, 1440, 1280, 1241, 1240, 1024, 768, 390];

let rot = 0;
const sage = (ok, text) => { if (!ok) rot++; console.log((ok ? '  ok   ' : '  ROT  ') + text); };

(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });

  for (const seite of seiten) {
    console.log('\n=== ' + seite + ' ===');
    const ctx = await b.newContext({ viewport: { width: 1512, height: 950 } });
    const p = await ctx.newPage();
    const fremdVorher = new Set(), fehler = [], konsole = [];
    p.on('request', r => {
      const u = new URL(r.url());
      if (u.protocol.startsWith('http') && u.host !== EIGEN) fremdVorher.add(u.host);
    });
    p.on('pageerror', e => fehler.push(String(e)));
    p.on('console', m => { if (m.type() === 'error') konsole.push(m.text()); });

    await p.goto(BASIS + seite, { waitUntil: 'load' });
    await p.waitForTimeout(800);

    sage(fremdVorher.size === 0, 'vor der Einwilligung keine fremden Hosts ' + JSON.stringify([...fremdVorher]));

    const struktur = await p.evaluate(() => {
      const stufen = [...document.querySelectorAll('h1,h2,h3,h4,h5,h6')]
        .map(h => +h.tagName[1]);
      let luecke = null;
      for (let i = 1; i < stufen.length; i++) {
        if (stufen[i] - stufen[i - 1] > 1) { luecke = stufen[i - 1] + ' -> ' + stufen[i]; break; }
      }
      const bilder = [...document.querySelectorAll('img')];
      const ziele = new Set([...document.querySelectorAll('[id]')].map(e => e.id));
      const tote = [...document.querySelectorAll('a[href^="#"]')]
        .map(a => a.getAttribute('href')).filter(h => h.length > 1 && !ziele.has(h.slice(1)));
      const text = document.body.innerText;
      const klein = (text.match(/\b(du|dich|dir|dein|deine|deiner|deinen|deinem|deines)\b/g) || []);
      const jsonld = [...document.querySelectorAll('script[type="application/ld+json"]')]
        .map(s => { try { return JSON.parse(s.textContent); } catch (e) { return { FEHLER: String(e) }; } });
      return {
        h1: document.querySelectorAll('h1').length,
        luecke,
        ohneAlt: bilder.filter(i => !i.hasAttribute('alt')).length,
        leerAlt: bilder.filter(i => i.getAttribute('alt') === '' && !i.closest('figure,[aria-hidden]')).length,
        tote, klein: [...new Set(klein)], jsonld
      };
    });

    sage(struktur.h1 === 1, 'genau eine h1 (gefunden: ' + struktur.h1 + ')');
    sage(!struktur.luecke, 'keine Luecke in den Ueberschriften ' + (struktur.luecke || ''));
    sage(struktur.ohneAlt === 0, 'jedes Bild hat alt (ohne: ' + struktur.ohneAlt + ')');
    sage(struktur.tote.length === 0, 'keine toten Sprungmarken ' + JSON.stringify(struktur.tote));
    sage(struktur.klein.length === 0, 'Anrede durchgehend gross ' + JSON.stringify(struktur.klein));

    if (seite.startsWith('stellen/')) {
      const jp = struktur.jsonld.find(o => o && o['@type'] === 'JobPosting');
      sage(!!jp, 'JobPosting vorhanden');
      if (jp) {
        for (const feld of ['title', 'description', 'datePosted', 'validThrough',
          'hiringOrganization', 'jobLocation', 'employmentType', 'directApply']) {
          sage(jp[feld] !== undefined && jp[feld] !== null, 'JobPosting.' + feld);
        }
        const ort = jp.jobLocation && jp.jobLocation.address;
        sage(!!ort && /^[A-Z]{2}$/.test(ort.addressCountry || ''), 'Laenderkuerzel zweistellig: ' + (ort && ort.addressCountry));
        sage(!isNaN(Date.parse(jp.validThrough)) && Date.parse(jp.validThrough) > Date.now(),
          'validThrough liegt in der Zukunft: ' + jp.validThrough);
      }
      sage(!!struktur.jsonld.find(o => o && o['@type'] === 'BreadcrumbList'), 'BreadcrumbList vorhanden');
    }

    for (const w of breiten) {
      await p.setViewportSize({ width: w, height: 900 });
      await p.waitForTimeout(250);
      const quer = await p.evaluate(() =>
        document.documentElement.scrollWidth - document.documentElement.clientWidth);
      sage(quer <= 1, 'kein Querscrollen bei ' + w + ' px (' + quer + ')');
    }

    sage(fehler.length === 0, 'keine Skriptfehler ' + JSON.stringify(fehler));
    sage(konsole.length === 0, 'keine Konsolenfehler ' + JSON.stringify(konsole.slice(0, 3)));
    await ctx.close();
  }

  await b.close();
  console.log(rot === 0 ? '\nAlles gruen.' : '\n' + rot + ' Punkt(e) rot.');
  process.exit(rot === 0 ? 0 : 1);
})();
