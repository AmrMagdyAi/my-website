/* amrmagdy.com, the guide, tool and blog pages (the ones on styles.css): the same header, dark mode, phone menu and
   phone call-to-action bar as the main site (assets/site.js), without the before/after switch.
   No dependencies. Loaded with defer at the end of each of those pages; scripts/guide_look.py adds it. */
(function(){
  'use strict';
  var d=document, root=d.documentElement, body=d.body;

  /* dark mode: same storage key as the rest of the site */
  var tbtn=d.getElementById('theme-toggle'), tmeta=d.querySelector('meta[name="theme-color"]');
  function paint(){
    var dark=root.getAttribute('data-theme')==='dark';
    if(tbtn) tbtn.setAttribute('aria-pressed',dark?'true':'false');
    if(tmeta) tmeta.setAttribute('content',dark?'#161412':'#f7f4ef');
  }
  if(tbtn) tbtn.addEventListener('click',function(){
    var dark=root.getAttribute('data-theme')!=='dark';
    if(dark) root.setAttribute('data-theme','dark'); else root.removeAttribute('data-theme');
    try{localStorage.setItem('theme',dark?'dark':'light');}catch(e){}
    paint();
  });
  paint();

  /* phone menu */
  var mbtn=d.getElementById('menu-btn'), nav=d.getElementById('nav');
  function closeMenu(focusBtn){
    if(!mbtn||mbtn.getAttribute('aria-expanded')!=='true') return;
    mbtn.setAttribute('aria-expanded','false');
    body.classList.remove('menu-open');
    if(focusBtn) mbtn.focus();
  }
  if(mbtn&&nav){
    var topbar=d.querySelector('.top');
    mbtn.addEventListener('click',function(){
      var open=mbtn.getAttribute('aria-expanded')!=='true';
      mbtn.setAttribute('aria-expanded',String(open));
      body.classList.toggle('menu-open',open);
      /* the nav comes before the button in the page, so take focus into it */
      if(open){ var first=nav.querySelector('a'); if(first) first.focus(); }
    });
    nav.addEventListener('click',function(e){ if(e.target.closest('a')) closeMenu(false); });
    d.addEventListener('keydown',function(e){ if(e.key==='Escape') closeMenu(true); });
    /* pointerdown where available: iOS Safari sends no click for taps on plain text */
    d.addEventListener(window.PointerEvent?'pointerdown':'click',function(e){ if(!e.target.closest('.top')) closeMenu(false); });
    /* tabbing out of the header closes the menu, so the open panel never covers the focused control */
    if(topbar) topbar.addEventListener('focusout',function(e){ if(e.relatedTarget&&!topbar.contains(e.relatedTarget)) closeMenu(false); });
    window.addEventListener('resize',function(){ if(window.innerWidth>900) closeMenu(false); });
  }

  /* phone call-to-action bar: after the first screen, until the page's own call-to-action box or the footer */
  var bar=d.getElementById('mcta');
  if(bar){
    var stop=d.querySelector(bar.getAttribute('data-stop')||'footer'), ticking=false;
    var upd=function(){
      ticking=false;
      var y=window.scrollY||root.scrollTop;
      var on=y>window.innerHeight*0.85&&!(stop&&stop.getBoundingClientRect().top<window.innerHeight);
      bar.classList.toggle('on',on);
    };
    window.addEventListener('scroll',function(){ if(!ticking){ ticking=true; requestAnimationFrame(upd); } },{passive:true});
    window.addEventListener('resize',upd);
    upd();
  }

  [].forEach.call(d.querySelectorAll('[data-year]'),function(el){ el.textContent=new Date().getFullYear(); });
})();
