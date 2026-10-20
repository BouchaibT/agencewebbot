/* Statistiques sans cookie (Umami auto-hébergé sur stats.agencewebbot.com, 20/10/2026).
   Les pages vues, la durée de visite, les sources et les liens utm_* sont comptés par Umami lui-même.
   Ce fichier ajoute les actions qui comptent : clic WhatsApp, inscription, e-mail, liens sortants,
   et la profondeur de lecture des guides (50 % / 90 %). Chaque événement porte le type de page
   (guide ou page commerciale) et la provenance (?src=… ou utm_source, gardée pour la visite). */
(function () {
  var GUIDES = /^(assurance|conciergerie|contrat|guide|menage|rentabilite|rokhsat|serrure|taxe|teledeclaration)/;
  var page = location.pathname.replace(/^\/|\.html$/g, '') || 'accueil';
  if (page === 'index') page = 'accueil';
  var type = GUIDES.test(page) ? 'guide' : (/^(cgu|confidentialite|mentions|suppression)/.test(page) ? 'legal' : 'commercial');

  function provenance() {
    try {
      var g = JSON.parse(sessionStorage.getItem('awb-source') || 'null');
      if (g && g.s) return g.s + (g.c ? ' ' + g.c : '');
    } catch (e) {}
    var p = new URLSearchParams(location.search);
    return p.get('src') || p.get('utm_source') || 'aucune';
  }

  function envoyer(nom, donnees) {
    var d = donnees || {};
    d.page = page; d.type = type; d.source = provenance();
    if (window.umami && umami.track) { umami.track(nom, d); return; }
    // Umami pas encore chargé (clic très rapide) : on réessaie une fois.
    setTimeout(function () { if (window.umami && umami.track) umami.track(nom, d); }, 800);
  }

  // Arrivée avec une provenance marquée (?src=tiktok, lien d'une vidéo…) : un événement par visite.
  try {
    var p = new URLSearchParams(location.search);
    var src = p.get('src') || p.get('utm_source');
    if (src && !sessionStorage.getItem('awb-arrivee')) {
      sessionStorage.setItem('awb-arrivee', '1');
      window.addEventListener('load', function () {
        envoyer('arrivee', { campagne: p.get('c') || p.get('utm_campaign') || '', support: p.get('utm_medium') || '' });
      });
    }
  } catch (e) {}

  document.addEventListener('click', function (ev) {
    var a = ev.target.closest && ev.target.closest('a[href], button');
    if (!a) return;
    var href = a.getAttribute('href') || '';
    var texte = (a.textContent || '').trim().replace(/\s+/g, ' ').slice(0, 40);
    var emplacement = (a.className && String(a.className).split(' ')[0]) || a.id || 'lien';
    if (/wa\.me\//.test(href)) envoyer('whatsapp', { bouton: texte || 'icone', emplacement: emplacement });
    else if (/inscription(\.html)?/.test(href)) envoyer('vers-inscription', { bouton: texte });
    else if (/essai(\.html)?/.test(href)) envoyer('vers-essai', { bouton: texte });
    else if (/^mailto:/.test(href)) envoyer('email', {});
    else if (/^tel:/.test(href)) envoyer('telephone', {});
    else if (a.tagName === 'BUTTON' && page === 'inscription') envoyer('inscription-bouton', { bouton: texte });
    else if (/^https?:/.test(href) && a.hostname && a.hostname.replace(/^www\./, '') !== location.hostname.replace(/^www\./, '')) {
      envoyer('lien-sortant', { vers: a.hostname });
    }
  }, true);

  // Profondeur de lecture des guides.
  if (type === 'guide') {
    var paliers = [50, 90], vus = {};
    var mesurer = function () {
      var h = document.documentElement;
      var pct = (h.scrollTop + window.innerHeight) / h.scrollHeight * 100;
      for (var i = 0; i < paliers.length; i++) {
        if (pct >= paliers[i] && !vus[paliers[i]]) { vus[paliers[i]] = 1; envoyer('lecture', { palier: paliers[i] + '%' }); }
      }
    };
    window.addEventListener('scroll', function () { clearTimeout(mesurer.t); mesurer.t = setTimeout(mesurer, 250); }, { passive: true });
  }
})();
