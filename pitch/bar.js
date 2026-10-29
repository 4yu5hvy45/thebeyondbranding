/*!
 * Beyond Branding pitch bar
 * Drop into any speculative pitch site with one line:
 *
 *   <script src="https://thebeyondbranding.com/pitch/bar.js" defer
 *     data-client="Shama Lakeview Asoke"
 *     data-offer="Save 25% on your hotel website redesign"
 *     data-note="For a limited number of hospitality projects · Enquire for details"
 *     data-sector="hospitality"></script>
 *
 * Every data-* attribute is optional. The bar is fixed to the bottom, adds matching
 * bottom padding to <body>, collapses to one line on phones, and can be minimised.
 */
(function () {
  if (window.__bbBar) return; window.__bbBar = 1;
  var s = document.currentScript || document.querySelector('script[src*="pitch/bar.js"]') || {};
  var d = (s && s.dataset) || {};
  var BASE = (d.base || 'https://thebeyondbranding.com').replace(/\/$/, '');
  var client = d.client || '';
  var offer = d.offer || 'Save 25% on your website redesign';
  var note = d.note || 'Limited projects each month · Enquire for details';
  var sector = d.sector || 'pitch';
  var wa = d.whatsapp || '19108301588';
  var utm = 'utm_source=pitch&utm_medium=bar&utm_campaign=' + encodeURIComponent((client || sector).toLowerCase().replace(/[^a-z0-9]+/g, '-'));
  var work = BASE + '/portfolio.html?' + utm;
  var msg = 'Hi Ayush, I saw the concept you made' + (client ? ' for ' + client : '') + '. I would like to talk about it.';
  var talk = 'https://wa.me/' + wa + '?text=' + encodeURIComponent(msg);
  var logos = (d.logos || 'marriott,radisson,dubai-media-office,esperti,soul-av,aiolec,wazirx,wemasy').split(',');
  var names = { 'marriott': 'Marriott', 'radisson': 'Radisson', 'dubai-media-office': 'Government of Dubai Media Office', 'esperti': 'ESPERTI', 'soul-av': 'Soul AV', 'aiolec': 'Aiolec', 'wazirx': 'WazirX', 'wemasy': 'Wemasy' };

  var css = '' +
    '.bbbar{position:fixed;left:0;right:0;bottom:0;z-index:2147483000;background:#D91C2B;color:#fff;font:400 14px/1.35 Inter,"Helvetica Neue",Arial,sans-serif;box-shadow:0 -10px 30px rgba(0,0,0,.18);' +
    'padding:12px max(18px,env(safe-area-inset-right,0px)) calc(12px + env(safe-area-inset-bottom,0px)) max(18px,env(safe-area-inset-left,0px));transition:transform .35s cubic-bezier(.2,.8,.2,1)}' +
    '.bbbar *{box-sizing:border-box}' +
    '.bbbar-in{max-width:1320px;margin:0 auto;display:grid;grid-template-columns:auto minmax(0,1fr) minmax(0,1.1fr) auto;align-items:center;gap:22px}' +
    '.bbbar-brand{display:flex;align-items:center;gap:10px;text-decoration:none;color:#fff;white-space:nowrap}' +
    '.bbbar-mark{width:30px;height:30px;border-radius:8px;background:#fff;color:#D91C2B;display:grid;place-items:center;font:800 13px/1 Inter,Arial,sans-serif;letter-spacing:-.04em}' +
    '.bbbar-brand b{display:block;font-weight:700;font-size:14px;letter-spacing:-.01em}.bbbar-brand small{display:block;font-size:11px;opacity:.8}' +
    '.bbbar-copy{min-width:0}.bbbar-copy b{display:block;font-weight:700;font-size:16px;letter-spacing:-.01em;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.bbbar-copy span{display:block;font-size:12px;opacity:.85;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}' +
    '.bbbar-logos{min-width:0;display:flex;align-items:center;gap:6px;overflow:hidden;-webkit-mask-image:linear-gradient(90deg,transparent,#000 8%,#000 92%,transparent);mask-image:linear-gradient(90deg,transparent,#000 8%,#000 92%,transparent)}' +
    '.bbbar-lbl{flex:none;font-size:10px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;opacity:.75;margin-right:6px}' +
    '.bbbar-trk{display:flex;align-items:center;gap:26px;animation:bbscroll 28s linear infinite;width:max-content}' +
    '.bbbar-trk img{height:18px;width:auto;filter:brightness(0) invert(1);opacity:.92;flex:none}' +
    '.bbbar-trk img.t{height:26px}' +
    '@keyframes bbscroll{to{transform:translateX(-50%)}}' +
    '.bbbar:hover .bbbar-trk{animation-play-state:paused}' +
    '.bbbar-act{display:flex;align-items:center;gap:8px}' +
    '.bbbar-act a{display:inline-flex;align-items:center;justify-content:center;min-height:40px;padding:0 16px;border-radius:999px;font-weight:700;font-size:14px;text-decoration:none;white-space:nowrap}' +
    '.bbbar-a1{color:#fff;box-shadow:inset 0 0 0 1.5px rgba(255,255,255,.6)}.bbbar-a1:hover{box-shadow:inset 0 0 0 1.5px #fff}' +
    '.bbbar-a2{background:#fff;color:#D91C2B}.bbbar-a2:hover{background:#FFE9EB}' +
    '.bbbar-x{width:32px;height:32px;border-radius:50%;border:0;background:rgba(0,0,0,.16);color:#fff;cursor:pointer;font:600 16px/1 Arial,sans-serif;display:grid;place-items:center}' +
    '.bbbar a:focus-visible,.bbbar button:focus-visible{outline:2px solid #fff;outline-offset:2px}' +
    '.bbbar.min{transform:translateY(calc(100% - 6px))}' +
    '.bbbar-tab{position:fixed;right:max(14px,env(safe-area-inset-right,0px));bottom:calc(14px + env(safe-area-inset-bottom,0px));z-index:2147483001;display:none;border:0;border-radius:999px;background:#D91C2B;color:#fff;font:700 13px/1 Inter,Arial,sans-serif;padding:12px 16px;box-shadow:0 8px 24px rgba(0,0,0,.25);cursor:pointer}' +
    '.bbbar.min + .bbbar-tab{display:block}' +
    '@media(max-width:1100px){.bbbar-in{grid-template-columns:auto minmax(0,1fr) auto}.bbbar-logos{display:none}}' +
    '@media(max-width:680px){.bbbar{padding-top:10px;padding-bottom:calc(10px + env(safe-area-inset-bottom,0px))}.bbbar-in{grid-template-columns:minmax(0,1fr) auto;gap:10px}.bbbar-brand small,.bbbar-brand b,.bbbar-copy span,.bbbar-act .bbbar-a1{display:none}.bbbar-brand{display:none}.bbbar-copy b{font-size:14px;white-space:normal}.bbbar-act a{min-height:38px;padding:0 14px}}' +
    '@media(prefers-reduced-motion:reduce){.bbbar-trk{animation:none}.bbbar{transition:none}}';

  function img(k) { var t = k === 'dubai-media-office' || k === 'radisson'; return '<img class="' + (t ? 't' : '') + '" src="' + BASE + '/assets/client-' + k + '.svg" alt="' + (names[k] || k) + '" loading="lazy">'; }
  var row = logos.map(img).join('');

  function mount() {
    var st = document.createElement('style'); st.textContent = css; document.head.appendChild(st);
    var bar = document.createElement('aside');
    bar.className = 'bbbar'; bar.setAttribute('aria-label', 'Beyond Branding: about this concept');
    bar.innerHTML =
      '<div class="bbbar-in">' +
        '<a class="bbbar-brand" href="' + BASE + '/?' + utm + '" target="_blank" rel="noopener"><span class="bbbar-mark">BB</span><span><b>Beyond Branding</b><small>' + (client ? 'Concept for ' + client : 'Design concept') + '</small></span></a>' +
        '<div class="bbbar-copy"><b>' + offer + '</b><span>' + note + '</span></div>' +
        '<div class="bbbar-logos" aria-label="Selected clients"><span class="bbbar-lbl">Trusted by</span><div class="bbbar-trk">' + row + row + '</div></div>' +
        '<div class="bbbar-act"><a class="bbbar-a1" href="' + work + '" target="_blank" rel="noopener">Explore our work</a><a class="bbbar-a2" href="' + talk + '" target="_blank" rel="noopener">Let’s talk</a><button class="bbbar-x" type="button" aria-label="Minimise">×</button></div>' +
      '</div>';
    var tab = document.createElement('button');
    tab.className = 'bbbar-tab'; tab.type = 'button'; tab.textContent = 'Beyond Branding';
    document.body.appendChild(bar); document.body.appendChild(tab);
    var pad = function () { document.body.style.paddingBottom = bar.classList.contains('min') ? '' : (bar.offsetHeight + 'px'); };
    bar.querySelector('.bbbar-x').addEventListener('click', function () { bar.classList.add('min'); pad(); tab.focus(); });
    tab.addEventListener('click', function () { bar.classList.remove('min'); pad(); });
    window.addEventListener('resize', pad); pad();
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', mount); else mount();
})();
