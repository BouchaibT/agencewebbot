/* Suivi de provenance sans outil payant ni cookie tiers.
   Le lien partagé porte ?src=tiktok (ou instagram, facebook…) ; à défaut, on lit le site d'origine.
   La provenance et la page sont ajoutées à la fin du message WhatsApp pré-rempli :
   chaque contact arrive donc avec une référence du type « (réf. TikTok · accueil) ». */
(function () {
  var NOMS = {
    tiktok: 'TikTok', tt: 'TikTok',
    instagram: 'Instagram', insta: 'Instagram', ig: 'Instagram',
    facebook: 'Facebook', fb: 'Facebook',
    youtube: 'YouTube', yt: 'YouTube',
    google: 'Google', gmb: 'Google Maps',
    whatsapp: 'WhatsApp', wa: 'WhatsApp',
    linkedin: 'LinkedIn', email: 'E-mail', prospection: 'Prospection'
  };
  var REFERENTS = [
    [/tiktok\./, 'TikTok'], [/instagram\./, 'Instagram'],
    [/facebook\.|fb\.com|messenger\./, 'Facebook'], [/youtube\.|youtu\.be/, 'YouTube'],
    [/google\./, 'Google'], [/bing\./, 'Bing'], [/linkedin\./, 'LinkedIn']
  ];
  var CLE = 'awb-source';

  function nettoyer(v) {
    return String(v || '').toLowerCase().replace(/[^a-z0-9_-]/g, '').slice(0, 30);
  }

  var params = new URLSearchParams(location.search);
  var brut = nettoyer(params.get('src') || params.get('utm_source'));
  var campagne = nettoyer(params.get('c') || params.get('utm_campaign'));
  var source = brut ? (NOMS[brut] || brut) : '';

  if (!source && document.referrer) {
    try {
      var hote = new URL(document.referrer).hostname;
      if (hote !== location.hostname) {
        for (var i = 0; i < REFERENTS.length; i++) {
          if (REFERENTS[i][0].test(hote)) { source = REFERENTS[i][1]; break; }
        }
      }
    } catch (e) {}
  }

  // La première provenance de la visite est gardée d'une page à l'autre.
  try {
    var garde = sessionStorage.getItem(CLE);
    if (garde) {
      var g = JSON.parse(garde);
      source = g.s; campagne = g.c;
    } else if (source) {
      sessionStorage.setItem(CLE, JSON.stringify({ s: source, c: campagne }));
    }
  } catch (e) {}

  var page = location.pathname.replace(/^\/|\.html$/g, '') || 'accueil';
  if (page === 'index') page = 'accueil';
  var ref = '(réf. ' + (source || 'site') + (campagne ? ' ' + campagne : '') + ' · ' + page + ')';
  var DEFAUT = 'Bonjour, je voudrais tester l\'assistant.';

  var liens = document.querySelectorAll('a[href*="wa.me/"]');
  for (var j = 0; j < liens.length; j++) {
    try {
      var url = new URL(liens[j].href);
      var texte = url.searchParams.get('text') || DEFAUT;
      if (texte.indexOf('(réf.') !== -1) continue;
      url.searchParams.set('text', texte + ' ' + ref);
      liens[j].href = url.toString();
    } catch (e) {}
  }
})();
