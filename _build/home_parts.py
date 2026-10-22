"""New homepage + shared website cards (one light canvas, cards instead of alternating black/white tiles).

Apple-inspired: white page, #F5F5F7 cards with large radii, one idea per card, big tight type,
filled pill + text link, one contained dark moment (the founder card). Motion is quiet: Lenis smooth
scroll, fade-up reveals, a hero stage that settles into place on scroll, and live screens that
crossfade inside each browser frame.
"""

CSS2 = r"""
/* ---------- hero: original copy + scrolling gallery ---------- */
.bbh{position:relative;display:grid;grid-template-columns:minmax(0,1.15fr) minmax(0,1fr);height:calc(100svh - 48px);min-height:640px;max-height:1000px;background:#FAFAF8;overflow:hidden}
.bbh-copy{display:flex;flex-direction:column;justify-content:center;padding:clamp(40px,5vw,72px) clamp(24px,4vw,40px) clamp(40px,5vw,72px) max(24px,calc((100vw - 1240px)/2 + 3vw));position:relative;z-index:3}
.bbh h1{position:relative;font-family:'Bebas Neue',sans-serif;font-weight:400;font-size:clamp(2.6rem,4.3vw,4rem);line-height:1.02;letter-spacing:.005em;white-space:nowrap;color:#131113;margin-bottom:26px}
.bbh h1 .r{color:var(--red)}
.bbh .shine{position:absolute;inset:0;pointer-events:none;background-image:linear-gradient(100deg,transparent 30%,rgba(255,255,255,.85) 46%,rgba(255,255,255,.95) 50%,rgba(255,255,255,.85) 54%,transparent 70%);
  background-size:300% 100%;background-position:160% 0;background-repeat:no-repeat;-webkit-background-clip:text;background-clip:text;color:transparent;-webkit-text-fill-color:transparent;mix-blend-mode:overlay;animation:bbShine 6.5s ease-in-out 2.4s infinite}
@keyframes bbShine{0%{background-position:160% 0}22%,100%{background-position:-60% 0}}
.bbh p{font-family:'IBM Plex Mono',ui-monospace,monospace;font-size:clamp(.86rem,1.1vw,1rem);line-height:1.75;color:#5c5a5d;max-width:54ch;margin-bottom:34px}
.bbcta{display:inline-flex;align-items:center;gap:14px;background:#131113;color:#fff;font:700 clamp(.82rem,1vw,.95rem)/1 'Archivo',sans-serif;letter-spacing:.14em;text-transform:uppercase;padding:22px 40px;border-radius:99px;transition:background .3s,transform .4s cubic-bezier(.19,1,.22,1)}
.bbcta:hover{background:var(--red);transform:translateY(-2px)}
.bbcta span{font-size:1.1em;font-weight:400}
.bbrule{width:64px;height:3px;background:var(--red);margin:34px 0 30px}
.bblogos{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:22px 30px;align-items:center;max-width:520px;padding-top:26px;border-top:1px solid #e3e1dd}
.bblogos img{height:34px;width:auto;max-width:100%;filter:grayscale(1) brightness(.25);opacity:.62}
.bbh-gal{position:relative;display:flex;gap:clamp(8px,1vw,14px);padding:0 clamp(16px,2.2vw,30px) 0 clamp(8px,1vw,14px);height:100%;overflow:hidden;
  -webkit-mask-image:linear-gradient(180deg,transparent,#000 7%,#000 93%,transparent);mask-image:linear-gradient(180deg,transparent,#000 7%,#000 93%,transparent)}
.gcol{flex:1 1 0;overflow:hidden;height:100%}
.gtrk{display:flex;flex-direction:column;gap:clamp(8px,1vw,14px);animation:gUp 90s linear infinite}
.gtrk.rev{animation:gDown 104s linear infinite}
.bbh-gal:hover .gtrk{animation-play-state:paused}
.gi{display:block;aspect-ratio:4/5;border-radius:22px;overflow:hidden;background:#EFEDE9;flex-shrink:0}
.gi img{width:100%;height:100%;object-fit:cover;transition:transform 1.2s cubic-bezier(.19,1,.22,1)}
.gi:hover img{transform:scale(1.04)}
@keyframes gUp{to{transform:translateY(-50%)}}
@keyframes gDown{from{transform:translateY(-50%)}to{transform:translateY(0)}}
.bbexplore{position:absolute;left:50%;bottom:28px;transform:translateX(-50%);z-index:4;display:inline-flex;align-items:center;gap:12px;background:var(--red);color:#fff;font:700 .9rem/1 'Archivo',sans-serif;letter-spacing:.14em;text-transform:uppercase;padding:20px 34px;border-radius:99px;box-shadow:0 14px 34px -10px rgba(217,28,43,.55);white-space:nowrap;transition:background .3s}
.bbexplore:hover{background:var(--red-h)}
.bbh-row{display:none}.bbh-mcta{display:none}
@media(max-width:1100px){.bbh h1{white-space:normal}}
@media(max-width:900px){
  .bbh{grid-template-columns:1fr;height:auto;max-height:none;min-height:0}
  .bbh-copy{padding:56px 20px 36px}
  .bbh h1{font-size:clamp(2.9rem,14vw,4.4rem);line-height:.96;margin-bottom:18px}
  .bbh p{margin-bottom:26px}
  .bbcta{padding:19px 30px}
  .bbrule{margin:28px 0 24px;width:40px}
  .bblogos{gap:18px 22px}.bblogos img{height:28px}
  .bbh-gal{display:none}
  .bbh-row{display:block;overflow:hidden;padding:0 0 40px;-webkit-mask-image:linear-gradient(90deg,transparent,#000 5%,#000 95%,transparent);mask-image:linear-gradient(90deg,transparent,#000 5%,#000 95%,transparent)}
  .bbh-row .trk{display:flex;gap:10px;width:max-content;animation:gLeft 80s linear infinite}
  .bbh-row .gi{width:58vw;max-width:260px;border-radius:18px}
  .bbh-row{padding-bottom:20px}.bbh-mcta{display:flex;justify-content:center;padding:6px 20px 8px}.bbh-mcta .bbexplore{position:static;transform:none}
}
@keyframes gLeft{to{transform:translateX(-50%)}}
@media(prefers-reduced-motion:reduce){.gtrk,.bbh-row .trk{animation:none}.bbh .shine{display:none}}

/* ---------- v6: one light canvas ---------- */
html.lenis,html.lenis body{height:auto}
.lenis.lenis-smooth{scroll-behavior:auto!important}
.wrap{max-width:1240px;margin:0 auto;padding:0 max(16px,3vw)}
.sec2{padding-top:clamp(88px,11vw,150px)}
.head2{text-align:center;max-width:820px;margin:0 auto clamp(36px,5vw,56px);padding:0 max(16px,3vw)}
.head2 h2{font-size:clamp(2.3rem,5.2vw,4.2rem);font-weight:700;letter-spacing:-.032em;line-height:1.04}
.head2 p{font-size:clamp(1.05rem,1.7vw,1.35rem);color:var(--muted);margin-top:14px;line-height:1.4;letter-spacing:-.01em}
.head2 .ctas{margin-top:18px}

/* hero */
.hero2{text-align:center;padding:clamp(64px,9vw,120px) 0 0;overflow:hidden}
.hero2 .eyebrow{font-size:.95rem}
.hero2 h1{font-size:clamp(3rem,8.4vw,7rem);font-weight:700;letter-spacing:-.045em;line-height:.98;max-width:12ch;margin:0 auto;padding:0 max(16px,3vw)}
.hero2 h1 .w{display:inline-block;opacity:0;transform:translateY(.32em);transition:opacity 1s cubic-bezier(.19,1,.22,1),transform 1.1s cubic-bezier(.19,1,.22,1)}
.hero2.on h1 .w{opacity:1;transform:none}
.hero2 .sub{max-width:34ch;margin:18px auto 0;color:var(--muted);padding:0 16px}
.stage{position:relative;max-width:1180px;margin:clamp(48px,7vw,84px) auto 0;padding:0 max(16px,3vw);
  transform:scale(var(--s,.9)) translateY(var(--y,0px));transform-origin:50% 0;will-change:transform}
.stage .browser{width:100%;border-radius:18px;box-shadow:0 50px 120px -40px rgba(0,0,0,.45),0 0 0 1px rgba(0,0,0,.06)}
.stage .phone{position:absolute;bottom:-6%;width:clamp(110px,17%,200px);border-radius:28px;padding:7px;background:#111;box-shadow:0 40px 80px -30px rgba(0,0,0,.55)}
.stage .phone img{border-radius:22px;aspect-ratio:9/19.5;object-fit:cover;object-position:top;width:100%}
.stage .phone.l{left:-1%}.stage .phone.r{right:-1%}
.stage .tag{position:absolute;top:-14px;left:50%;transform:translateX(-50%);z-index:3;background:#fff;border-radius:99px;padding:7px 14px 7px 12px;font-size:.8rem;font-weight:500;box-shadow:0 8px 24px rgba(0,0,0,.1);white-space:nowrap;display:flex;align-items:center;gap:8px}
.live:before,.stage .tag:before{content:"";width:7px;height:7px;border-radius:50%;background:#1DB954;box-shadow:0 0 0 3px rgba(29,185,84,.18);animation:pulse 2.4s ease-in-out infinite}
@keyframes pulse{50%{box-shadow:0 0 0 6px rgba(29,185,84,0)}}
@media(max-width:700px){.stage .phone{width:23%;bottom:-8%;padding:4px;border-radius:16px}.stage .phone img{border-radius:13px}.stage .phone.l{left:2%}.stage .phone.r{right:2%}}
.trust2{margin-top:clamp(80px,10vw,120px);text-align:center}
.trust2 small{display:block;font-size:.8rem;color:var(--muted);margin-bottom:18px}
.trust2 .row{display:flex;justify-content:center;align-items:center;gap:clamp(22px,5vw,64px);flex-wrap:wrap;padding:0 16px}
.trust2 img{height:38px;width:auto;filter:grayscale(1) brightness(.2);opacity:.5}

/* browser frame with crossfading screens */
.browser{position:relative}
.browser .scr{position:relative;aspect-ratio:16/10;overflow:hidden;background:#111}
.browser .scr img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:top;aspect-ratio:auto;opacity:0;transition:opacity 1.2s ease}
.browser .scr img.on{opacity:1}
.browser .c{position:relative;z-index:2}
.browser.light{background:#e8e8ed}.browser.light .c{background:#ececf0}.browser.light .c i{background:#c7c7cc}.browser.light .url{background:#fff;color:#6e6e73}

/* cards */
.grid{display:grid;grid-template-columns:repeat(12,minmax(0,1fr));gap:16px}
.card{position:relative;background:var(--tile);border-radius:28px;overflow:hidden;display:flex;flex-direction:column;isolation:isolate;
  transition:transform .6s cubic-bezier(.19,1,.22,1),box-shadow .6s}
a.card:hover,.card.hov:hover{transform:translateY(-4px);box-shadow:0 24px 50px -24px rgba(0,0,0,.22)}
.card .cp{padding:clamp(28px,3.4vw,44px) clamp(24px,3.4vw,44px) 0;position:relative;z-index:2}
.card .ey{font-size:.82rem;font-weight:600;color:var(--muted);display:flex;align-items:center;gap:8px;flex-wrap:wrap}
.card .ey .live{color:#1a7f3c;display:inline-flex;align-items:center;gap:7px}
.card h3{font-size:clamp(1.7rem,2.9vw,2.6rem);font-weight:700;letter-spacing:-.03em;line-height:1.05;margin-top:8px}
.card p.d{font-size:clamp(1rem,1.3vw,1.12rem);color:var(--muted);margin-top:10px;line-height:1.45;max-width:44ch}
.card .ctas{justify-content:flex-start;margin-top:18px}
.card .md{margin-top:auto;padding:clamp(26px,3vw,40px) clamp(24px,3.4vw,44px) 0}
.card .md .browser{border-radius:14px 14px 0 0;box-shadow:0 30px 60px -30px rgba(0,0,0,.4)}
.card .md .par{transform:translateY(var(--p,0px));will-change:transform}
.c6{grid-column:span 6}.c4{grid-column:span 4}.c8{grid-column:span 8}.c12{grid-column:span 12}
.card.big{min-height:clamp(560px,52vw,700px)}
.card.sm{min-height:clamp(440px,36vw,520px)}
.card.sm h3{font-size:clamp(1.5rem,2.2vw,2rem)}
.card.sm .md{padding-left:24px;padding-right:24px}
.card.dk{background:#0b0b0d;color:#f5f5f7}.card.dk .ey,.card.dk p.d{color:#a1a1a6}.card.dk .lk{color:#ff5a66}
/* image cards (brand work) */
.card.im{min-height:clamp(380px,34vw,520px);color:#fff;background:#ddd}
.card.im img.bg{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;z-index:-2;transition:transform 1.4s cubic-bezier(.19,1,.22,1)}
.card.im:hover img.bg{transform:scale(1.04)}
.card.im:after{content:"";position:absolute;inset:0;z-index:-1;background:linear-gradient(180deg,rgba(0,0,0,0) 45%,rgba(0,0,0,.62))}
.card.im .cp{margin-top:auto;padding-bottom:clamp(24px,3vw,36px)}
.card.im .ey{color:rgba(255,255,255,.8)}.card.im p.d{color:rgba(255,255,255,.86)}
.card.im h3{font-size:clamp(1.5rem,2.4vw,2.2rem)}
.card.tall{min-height:clamp(520px,48vw,680px)}
.more{text-align:center;margin-top:30px}
@media(max-width:900px){.c4{grid-column:span 6}.c8{grid-column:span 12}}
@media(max-width:700px){.grid{gap:12px}.c6,.c4,.c8{grid-column:span 12}.card.big{min-height:0}.card.sm{min-height:0}.card.im{min-height:380px}.card{border-radius:22px}}

/* founder card */
.founder2{display:grid;grid-template-columns:minmax(0,.85fr) minmax(0,1.15fr);background:#0b0b0d;color:#f5f5f7;border-radius:28px;overflow:hidden}
.founder2 .ph{position:relative;min-height:440px}
.founder2 .ph img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:center 28%}
.founder2 .copy{padding:clamp(36px,5vw,80px);display:flex;flex-direction:column;justify-content:center}
.founder2 .eyebrow{font-size:.9rem}
.founder2 q{font-size:clamp(1.6rem,3vw,2.6rem);font-weight:700;letter-spacing:-.025em;line-height:1.1;quotes:none}
.founder2 p{color:#a1a1a6;line-height:1.6;margin-top:18px;max-width:46ch}
.founder2 .who{margin-top:22px;font-size:.95rem}
.founder2 .ctas{justify-content:flex-start}
.founder2 .pill.o{color:#fff;box-shadow:inset 0 0 0 1.5px rgba(255,255,255,.6)}
@media(max-width:760px){.founder2{grid-template-columns:1fr;border-radius:22px}.founder2 .ph{min-height:360px}}

/* stats strip */
.stats{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:16px;text-align:center}
.stats div{padding:6px 10px}
.stats b{display:block;font-size:clamp(2.2rem,4.6vw,3.6rem);font-weight:700;letter-spacing:-.04em;line-height:1}
.stats span{display:block;color:var(--muted);font-size:.95rem;margin-top:8px}
@media(max-width:700px){.stats{grid-template-columns:1fr 1fr;row-gap:28px}}

.js .rv{transition-delay:var(--d,0s)}
@media(prefers-reduced-motion:reduce){.stage{transform:none!important}.hero2 h1 .w{opacity:1;transform:none}.browser .scr img{transition:none}.card .md .par{transform:none!important}}
"""

JS2 = r"""
(function(){
  var reduce=window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  // smooth scroll
  var lenis=null;
  if(!reduce&&window.Lenis){lenis=new Lenis({duration:1.15,easing:function(t){return Math.min(1,1.001-Math.pow(2,-10*t))},smoothWheel:true});
    (function raf(t){lenis.raf(t);requestAnimationFrame(raf)})(0);
    document.querySelectorAll('a[href^="#"],a[href*=".html#"]').forEach(function(a){a.addEventListener('click',function(e){var h=a.getAttribute('href'),i=h.indexOf('#');if(i<0)return;var p=h.slice(0,i);if(p&&location.pathname.split('/').pop()!==p)return;var t=document.querySelector(h.slice(i));if(t){e.preventDefault();lenis.scrollTo(t,{offset:-56})}})});}
  // reveals
  var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}})},{rootMargin:'0px 0px -8% 0px'});
  document.querySelectorAll('.rv').forEach(function(el){io.observe(el)});
  // hero words
  var h=document.querySelector('.hero2');if(h){requestAnimationFrame(function(){setTimeout(function(){h.classList.add('on')},60)})}
  // scroll-linked: hero stage settles, media drifts
  var stage=document.querySelector('.stage'),pars=[].slice.call(document.querySelectorAll('.par'));
  function tick(){var vh=innerHeight;
    if(stage){var r=stage.getBoundingClientRect();var k=Math.min(1,Math.max(0,(vh-r.top)/(vh*0.9)));stage.style.setProperty('--s',(0.9+0.1*k).toFixed(4))}
    pars.forEach(function(el){var r=el.getBoundingClientRect();if(r.bottom<0||r.top>vh)return;var c=(r.top+r.height/2-vh/2)/vh;el.style.setProperty('--p',(c*-26).toFixed(1)+'px')});}
  if(!reduce){if(lenis)lenis.on('scroll',tick);addEventListener('scroll',tick,{passive:true});addEventListener('resize',tick);tick()}
  // crossfading screens inside browser frames (only while visible)
  document.querySelectorAll('.scr[data-cycle]').forEach(function(s){var im=s.querySelectorAll('img');if(im.length<2||reduce)return;var i=0,vis=false;
    new IntersectionObserver(function(es){vis=es[0].isIntersecting}).observe(s);
    setInterval(function(){if(!vis||document.hidden)return;im[i].classList.remove('on');i=(i+1)%im.length;im[i].classList.add('on')},3600)});
  // why scroller
  var why=document.querySelector('.why');
  document.querySelectorAll('.why-nav button').forEach(function(b){b.addEventListener('click',function(){why.scrollBy({left:(b.dataset.d==='r'?1:-1)*why.clientWidth*.8,behavior:'smooth'})})});
})();
"""
