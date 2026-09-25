/* Karriereseite: alles, was skript.js nicht abdeckt.
   1. Die Videos ab dem zweiten (skript.js kümmert sich nur um das erste)
   2. "Auf diese Stelle bewerben" füllt die Auswahl im Formular vor
   3. Dateiauswahl prüfen und anzeigen
   4. Versand der Bewerbung an bewerbung.php                                   */
(function () {
  'use strict';

  /* ---------- 1. Weitere Videos, gleiche Regel wie auf der Hauptseite ---------- */
  var MEDIEN = 'medien';
  var darfMedien = function () {
    return !!(window.aoEinwilligung && window.aoEinwilligung.erlaubt(MEDIEN));
  };
  /* Die Videofelder im Karussell zeigen kein Vorschaubild mehr. Sobald die
     Einwilligung vorliegt, sitzt dort der Wistia-Rahmen und das Video laeuft
     stumm und in Schleife, wie ein Hintergrundfilm. Ohne Einwilligung steht
     dort nur der Ladeknopf: vorher darf keine Anfrage an Wistia gehen.       */
  function rahmenBauen(box, hintergrund) {
    var id = box.dataset.video;
    if (!id || box.dataset.geladen === '1') return;
    box.dataset.geladen = '1';
    var teile = ['videoFoam=true'];
    if (hintergrund) {
      // Stumm, von selbst, in Schleife und ohne Bedienleiste: das ist der
      // Hintergrundfilm. Ton gibt es erst, wenn jemand wirklich hineinklickt.
      teile.push('autoPlay=true', 'muted=true', 'endVideoBehavior=loop',
                 'playbar=false', 'smallPlayButton=false', 'fullscreenButton=false',
                 'settingsControl=false', 'playButton=false');
    }
    var rahmen = document.createElement('iframe');
    rahmen.src = 'https://fast.wistia.net/embed/iframe/' + encodeURIComponent(id) + '?' + teile.join('&');
    rahmen.title = box.getAttribute('data-titel') || 'Video von AO Consulting';
    rahmen.allow = 'autoplay; fullscreen';
    rahmen.setAttribute('allowfullscreen', '');
    box.innerHTML = '';
    box.appendChild(rahmen);
  }

  function videoVerdrahten(box) {
    if (box.dataset.verdrahtet === '1') return;
    box.dataset.verdrahtet = '1';
    var imBand = !!box.closest('[data-band]');
    var knopf = box.querySelector('[data-video-laden]');
    if (knopf) knopf.addEventListener('click', function () {
      if (window.aoEinwilligung) window.aoEinwilligung.setze(MEDIEN, true);
      rahmenBauen(box, imBand || box.hasAttribute('data-hintergrund'));
    });
    var pruefe = function () {
      if (!darfMedien() || box.dataset.geladen === '1') return;
      // Im Karussell entscheidet das Karussell, welches Feld laeuft: immer nur
      // die Mitte. Neun gleichzeitig laufende Videos waeren sinnlos und schwer.
      if (imBand) return;
      // Der Film im Hero laeuft wie im Karussell von selbst, stumm und in Schleife.
      if (box.hasAttribute('data-hintergrund')) { rahmenBauen(box, true); return; }
      // Ausserhalb bleibt das Vorschaubild stehen, nur der Hinweis entfaellt.
      if (knopf) knopf.textContent = 'Video abspielen';
      var text = box.querySelector('.video__hinweis p');
      if (text) text.hidden = true;
    };
    document.addEventListener('ao:einwilligung', pruefe);
    pruefe();
  }
  // Auf der Karriereseite tragen alle Kaesten data-eigen, skript.js haelt sich
  // heraus. Auf anderen Seiten bleibt das erste bei skript.js.
  var kaesten = Array.prototype.slice.call(document.querySelectorAll('.video__box'));
  if (!document.querySelector('.video__box[data-eigen]')) kaesten = kaesten.slice(1);
  kaesten.forEach(videoVerdrahten);

  /* ---------- 1b. Karussell ----------
     Die mittlere Karte gross, die Nachbarn als kleine Vorschau daneben.
     Gescrollt wird echt, die Pfeile schieben nur: Wischen, Tastatur und
     Screenreader bleiben damit ohne Zusatzarbeit erhalten.                 */
  Array.prototype.forEach.call(document.querySelectorAll('[data-band]'), function (band) {
    var spur = band.querySelector('[data-band-spur]');
    if (!spur) return;
    var zurueck = band.querySelector('[data-band-zurueck]');
    var vor = band.querySelector('[data-band-vor]');
    var punkteliste = band.querySelector('[data-band-punkte]');
    var schleife = band.hasAttribute('data-band-schleife');

    var echte = Array.prototype.slice.call(spur.children);
    var anzahl = echte.length;
    if (!anzahl) return;

    // Schleife: je eine Kopie der Reihe davor und dahinter. Die Kopien sind
    // fuer Tastatur und Screenreader nicht vorhanden, sonst zaehlt jedes
    // Video dreimal. Ohne Schleife stuende links vom ersten Feld nichts.
    if (schleife && anzahl > 1) {
      var vorne = document.createDocumentFragment(), hinten = document.createDocumentFragment();
      echte.forEach(function (feld) {
        [vorne, hinten].forEach(function (ziel) {
          var k = feld.cloneNode(true);
          // cloneNode kopiert auch data-verdrahtet und data-geladen. Ohne das
          // Zuruecksetzen haelt das Skript die Kopie fuer fertig und ihr Tor
          // bliebe stehen, waehrend die Mitte laeuft.
          Array.prototype.forEach.call(k.querySelectorAll('.video__box'), function (vb) {
            delete vb.dataset.verdrahtet;
            delete vb.dataset.geladen;
          });
          k.setAttribute('data-klon', '');
          k.setAttribute('aria-hidden', 'true');
          k.setAttribute('inert', '');
          Array.prototype.forEach.call(k.querySelectorAll('button, a, input'), function (el) {
            el.tabIndex = -1;
          });
          ziel.appendChild(k);
        });
      });
      spur.insertBefore(vorne, spur.firstChild);
      spur.appendChild(hinten);
    }

    // Die Kopien tragen eigene Videokaestchen, die noch niemand verdrahtet hat.
    Array.prototype.forEach.call(spur.querySelectorAll('.video__box'), videoVerdrahten);
    var torVorlage = spur.querySelector('.video__tor');
    torVorlage = torVorlage ? torVorlage.cloneNode(true) : null;
    function videoTorVerdrahten(box) {
      var k = box.querySelector('[data-video-laden]');
      if (!k) return;
      k.addEventListener('click', function () {
        if (window.aoEinwilligung) window.aoEinwilligung.setze(MEDIEN, true);
        rahmenBauen(box, true);
      });
    }

    var felder = Array.prototype.slice.call(spur.children);

    function mitteVon(feld) {
      return feld.offsetLeft + feld.offsetWidth / 2 - spur.clientWidth / 2;
    }
    function naechstesFeld() {
      var mitte = spur.scrollLeft + spur.clientWidth / 2;
      var beste = 0, kleinster = Infinity;
      felder.forEach(function (f, i) {
        var d = Math.abs(f.offsetLeft + f.offsetWidth / 2 - mitte);
        if (d < kleinster) { kleinster = d; beste = i; }
      });
      return beste;
    }
    function springe(i, weich) {
      spur.scrollTo({ left: mitteVon(felder[i]),
        behavior: (weich && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) ? 'smooth' : 'auto' });
    }

    // Punkte: einer je echtem Feld, nicht je Kopie.
    var punkte = [];
    if (punkteliste) {
      punkteliste.innerHTML = '';
      echte.forEach(function (feld, i) {
        var li = document.createElement('li');
        var b = document.createElement('button');
        b.type = 'button';
        var name = feld.querySelector('.stimme__name');
        b.setAttribute('aria-label', 'Zu ' + (name ? name.textContent.trim() : 'Feld ' + (i + 1)));
        b.addEventListener('click', function () {
          springe(schleife && anzahl > 1 ? anzahl + i : i, true);
        });
        li.appendChild(b); punkteliste.appendChild(li); punkte.push(b);
      });
    }

    var letzteMitte = -1;
    function mitteBespielen(i) {
      if (!darfMedien() || i === letzteMitte) return;
      letzteMitte = i;
      felder.forEach(function (f, k) {
        var box = f.querySelector('.video__box');
        if (!box) return;
        // Die Mitte und die beiden Nachbarn laufen. Das ist das Band, das
        // Ovidiu wollte: man sieht links und rechts, dass es weitergeht.
        if (Math.abs(k - i) <= 1) {
          rahmenBauen(box, true);
        } else if (box.dataset.geladen === '1') {
          // Aus dem Blickfeld heisst aus dem Speicher: der Rahmen kommt raus,
          // sonst laufen nach ein paar Klicks neun Videos gleichzeitig. So
          // sind es immer hoechstens drei.
          var rahmen = box.querySelector('iframe');
          if (rahmen) rahmen.remove();
          box.dataset.geladen = '';
          if (!box.querySelector('.video__tor') && torVorlage) {
            box.appendChild(torVorlage.cloneNode(true));
            videoTorVerdrahten(box);
          }
        }
      });
    }

    function zustand() {
      var i = naechstesFeld();
      felder.forEach(function (f, k) {
        if (k === i) { f.removeAttribute('data-nebenan'); } else { f.setAttribute('data-nebenan', ''); }
      });
      var echt = schleife && anzahl > 1 ? ((i % anzahl) + anzahl) % anzahl : i;
      punkte.forEach(function (b, k) { b.setAttribute('aria-current', k === echt ? 'true' : 'false'); });
      if (!schleife) {
        var ueberhang = spur.scrollWidth - spur.clientWidth;
        var passt = ueberhang <= 2;
        if (zurueck) { zurueck.hidden = passt; zurueck.disabled = spur.scrollLeft <= 2; }
        if (vor) { vor.hidden = passt; vor.disabled = spur.scrollLeft >= ueberhang - 2; }
      }
    }

    // Am Rand der Kopien unsichtbar zurueck in die Mitte setzen. Das passiert
    // erst, wenn das Scrollen zur Ruhe gekommen ist, sonst ruckelt es.
    var ruhe = null;
    function nachfassen() {
      mitteBespielen(naechstesFeld());
      if (!schleife || anzahl < 2) return;
      var i = naechstesFeld();
      if (i < anzahl) springe(i + anzahl, false);
      else if (i >= anzahl * 2) springe(i - anzahl, false);
    }
    spur.addEventListener('scroll', function () {
      zustand();
      clearTimeout(ruhe);
      ruhe = setTimeout(nachfassen, 200);
    }, { passive: true });

    function schiebe(richtung) {
      springe(Math.min(felder.length - 1, Math.max(0, naechstesFeld() + richtung)), true);
    }
    if (zurueck) zurueck.addEventListener('click', function () { schiebe(-1); });
    if (vor) vor.addEventListener('click', function () { schiebe(1); });

    function start() {
      if (schleife && anzahl > 1) springe(anzahl, false);
      zustand();
      mitteBespielen(naechstesFeld());
    }
    // Die Einwilligung kann lange nach dem Aufbau der Seite kommen. Dann faengt
    // die mittlere Karte von selbst an zu laufen, ohne dass jemand klicken muss.
    document.addEventListener('ao:einwilligung', function () {
      letzteMitte = -1;
      mitteBespielen(naechstesFeld());
    });
    start();
    window.addEventListener('load', start);
    window.addEventListener('resize', function () { springe(naechstesFeld(), false); zustand(); });
    setTimeout(start, 400);
  });

  /* ---------- 1c. kununu-Siegel, erst nach Einwilligung ----------
     Die Grafik liegt auf dem Server von kununu und traegt beim Laden die
     IP-Adresse des Besuchers dorthin. Vorher steht die Bewertung als eigener
     Baustein da, danach das echte Siegel. Wer es ganz ohne Tor will, laedt die
     Grafik einmal herunter und traegt in stellen-daten.py einen oertlichen
     Pfad ein.                                                              */
  Array.prototype.forEach.call(document.querySelectorAll('[data-kununu]'), function (kasten) {
    var adresse = kasten.getAttribute('data-kununu');
    var hinweis = kasten.querySelector('.kununu__hinweis');
    var knopf = kasten.querySelector('[data-kununu-laden]');
    if (!adresse) return;

    function lade() {
      if (kasten.dataset.geladen === '1') return;
      kasten.dataset.geladen = '1';
      var bild = new Image();
      bild.className = 'kununu__siegel';
      bild.alt = 'Arbeitgeberbewertung der AO Consulting GmbH auf kununu';
      bild.loading = 'lazy';
      bild.referrerPolicy = 'no-referrer';
      bild.onerror = function () {
        // Kein Drama: der eigene Baustein steht ja schon da.
        kasten.dataset.geladen = '';
        if (hinweis) hinweis.hidden = true;
      };
      bild.onload = function () {
        var kern = kasten.querySelector('.kununu__kern');
        if (kern) kern.hidden = true;
        if (hinweis) hinweis.hidden = true;
      };
      bild.src = adresse;
      var verweis = document.createElement('a');
      verweis.href = kasten.querySelector('.kununu__kern').getAttribute('href');
      verweis.target = '_blank'; verweis.rel = 'nofollow noopener';
      verweis.appendChild(bild);
      kasten.insertBefore(verweis, hinweis || null);
    }

    if (knopf) knopf.addEventListener('click', function () {
      if (window.aoEinwilligung) window.aoEinwilligung.setze(MEDIEN, true);
      lade();
    });
    var pruefe = function () { if (darfMedien()) lade(); };
    document.addEventListener('ao:einwilligung', pruefe);
    pruefe();
  });

  /* ---------- 2. Stellenknopf füllt die Auswahl vor ---------- */
  var auswahl = document.getElementById('b-stelle');
  Array.prototype.forEach.call(document.querySelectorAll('[data-stelle]'), function (a) {
    a.addEventListener('click', function () {
      if (!auswahl) return;
      var wunsch = a.getAttribute('data-stelle');
      Array.prototype.forEach.call(auswahl.options, function (o) {
        if (o.value === wunsch || o.textContent.trim() === wunsch) auswahl.value = o.value || o.textContent.trim();
      });
    });
  });

  /* ---------- 3. und 4. Bewerbungsformular ---------- */
  var f = document.getElementById('bewerbung-formular');
  if (!f) return;
  var datei = document.getElementById('b-datei'),
      dateiFehler = document.getElementById('b-datei-fehler'),
      mailFehler = document.getElementById('b-mail-fehler'),
      versandFehler = document.getElementById('bewerbung-versand-fehler'),
      danke = f.querySelector('.danke'),
      knopf = f.querySelector('button[type=submit]'),
      mail = document.getElementById('b-mail'),
      tel = document.getElementById('b-tel'),
      telFehler = document.getElementById('b-tel-fehler');

  var MAX_GESAMT = 10 * 1024 * 1024, MAX_ANZAHL = 3;
  // Ovidiu 25.09.2026: Bewerbungen grundsaetzlich als PDF.
  var ERLAUBT = ['pdf'];

  function dateienOk() {
    if (!datei || !datei.files || !datei.files.length) return true; // Anhang ist freiwillig
    var summe = 0, namen = [];
    for (var i = 0; i < datei.files.length; i++) {
      var d = datei.files[i];
      summe += d.size;
      namen.push(d.name);
      var endung = (d.name.split('.').pop() || '').toLowerCase();
      if (ERLAUBT.indexOf(endung) === -1) {
        return fehlerDatei('„' + d.name + '" ist kein PDF. Bitte speichere die Datei als PDF und lade sie dann hoch.');
      }
    }
    if (datei.files.length > MAX_ANZAHL) return fehlerDatei('Bitte höchstens drei Dateien anhängen.');
    if (summe > MAX_GESAMT) {
      return fehlerDatei('Die Dateien sind zusammen ' + (summe / 1048576).toFixed(1) +
        ' MB groß, mehr als 10 MB gehen nicht. Schick die größte gern per Mail nach.');
    }
    if (dateiFehler) dateiFehler.hidden = true;
    zeigeListe(namen);
    return true;
  }
  function fehlerDatei(text) {
    if (dateiFehler) { dateiFehler.textContent = text; dateiFehler.hidden = false; }
    return false;
  }
  function zeigeListe(namen) {
    var alt = f.querySelector('.datei__liste');
    if (alt) alt.parentNode.removeChild(alt);
    if (!namen.length) return;
    var ul = document.createElement('ul');
    ul.className = 'datei__liste';
    namen.forEach(function (n) {
      var li = document.createElement('li');
      li.innerHTML = '<svg aria-hidden="true"><use href="#ic-haken"/></svg>';
      li.appendChild(document.createTextNode(n));
      ul.appendChild(li);
    });
    datei.parentNode.appendChild(ul);
  }
  if (datei) datei.addEventListener('change', dateienOk);

  // Telefon ist Pflicht (Ovidiu 25.09.2026). Mindestens sechs Ziffern, damit
  // nicht jemand nur ein Leerzeichen oder "-" eintraegt.
  function telOk() {
    if (!tel) return true;
    var ok = (tel.value.match(/\d/g) || []).length >= 6;
    if (telFehler) telFehler.hidden = ok;
    if (ok) tel.removeAttribute('aria-invalid'); else tel.setAttribute('aria-invalid', 'true');
    return ok;
  }

  function mailOk() {
    var v = mail ? mail.value.trim() : '';
    var ok = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v);
    if (mailFehler) mailFehler.hidden = ok;
    return ok;
  }

  // skript.js prüft die Pflichtfelder und setzt bei Erfolg die Klasse "gesendet".
  // Erst dann gehen die Daten an bewerbung.php.
  var beobachter = new MutationObserver(function () {
    if (!f.classList.contains('gesendet') || f.dataset.laeuft) return;
    var mOk = mailOk(), tOk = telOk();
    if (!mOk || !tOk || !dateienOk()) {
      f.classList.remove('gesendet');
      if (danke) danke.hidden = true;
      (!mOk ? mail : !tOk ? tel : datei).focus();
      return;
    }
    f.dataset.laeuft = '1';
    if (danke) danke.hidden = true;
    if (versandFehler) versandFehler.hidden = true;
    if (knopf) { knopf.disabled = true; knopf.textContent = 'Wird gesendet …'; }
    fetch(f.getAttribute('action'), { method: 'POST', body: new FormData(f), headers: { 'Accept': 'application/json' } })
      .then(function (r) { return r.ok ? r.json() : Promise.reject(new Error(String(r.status))); })
      .then(function (d) {
        if (!d || !d.ok) throw new Error((d && d.fehler) || 'unbekannt');
        Array.prototype.forEach.call(f.querySelectorAll('input, select, textarea'), function (el) { el.disabled = true; });
        if (knopf) knopf.hidden = true;
        if (danke) {
          danke.hidden = false;
          var h = danke.querySelector('h3');
          if (h) { h.setAttribute('tabindex', '-1'); h.focus(); }
        }
      })
      .catch(function (e) {
        f.classList.remove('gesendet');
        delete f.dataset.laeuft;
        if (knopf) { knopf.disabled = false; knopf.textContent = 'Bewerbung absenden'; }
        // Auch die Einzeldatei (file://) und der lokale Server zaehlen als Vorschau.
        // Dort gibt es kein PHP, der Versand scheitert erwartbar und ohne Aussagekraft.
        var vorschau = location.protocol === 'file:' ||
                       /vorschau|github\.io|localhost|^127\./.test(location.hostname) ||
                       ['404', '405', '501', 'Failed to fetch'].indexOf(e.message) !== -1;
        if (versandFehler) {
          versandFehler.textContent = vorschau
            ? 'Das ist die Vorschau. Hier wird nichts verschickt, der Versand funktioniert erst auf der echten Adresse.'
            : 'Die Bewerbung konnte gerade nicht übertragen werden. Bitte versuch es noch einmal oder schreib an jobs@ao-karriere.de.';
          versandFehler.hidden = false;
        }
      });
  });
  beobachter.observe(f, { attributes: true, attributeFilter: ['class'] });
})();
