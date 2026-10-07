/* Besucherzählung mit Matomo, cookiefrei (Standard der AO Consulting).
   Keine Cookies, kein Browser-Speicher, IP gekürzt, Do Not Track wird respektiert.
   SEITE: Kennung aus statistik.ao-consult.de eintragen. Leer = keine Messung. */
(function () {
  'use strict';
  var adresse = 'https://statistik.ao-consult.de/';
  var seite = '8';
  if (!seite || /vorschau\.ao-consult\.de$|localhost|github\.io$/.test(location.hostname)) return;
  var _paq = (window._paq = window._paq || []);
  _paq.push(['disableCookies']); _paq.push(['setDoNotTrack', true]);
  _paq.push(['trackPageView']); _paq.push(['enableLinkTracking']);
  _paq.push(['setTrackerUrl', adresse + 'matomo.php']); _paq.push(['setSiteId', seite]);
  var s = document.createElement('script'); s.async = true; s.src = adresse + 'matomo.js';
  document.head.appendChild(s);
})();
