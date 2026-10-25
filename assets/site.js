/* amrmagdy.com: dark mode, phone menu, the before/after switch, the phone call-to-action bar, forms and GA4 events
   (before_after_toggle, faq_open, video_play, bio_copy, and generate_lead with method form / form_mailto / booking).
   No dependencies. Loaded with defer on index.html, crm-revenue-audit.html and about.html. */
(function(){
  'use strict';
  var d=document, root=d.documentElement, body=d.body;
  var BOOK='https://calendly.com/amr-magdy-crm/30min';
  function ev(name,params){
    if(!window.gtag) return;
    params=params||{}; params.page_path=location.pathname;
    window.gtag('event',name,params);
  }

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
    mbtn.addEventListener('click',function(){
      var open=mbtn.getAttribute('aria-expanded')!=='true';
      mbtn.setAttribute('aria-expanded',String(open));
      body.classList.toggle('menu-open',open);
    });
    nav.addEventListener('click',function(e){ if(e.target.closest('a')) closeMenu(false); });
    d.addEventListener('keydown',function(e){ if(e.key==='Escape') closeMenu(true); });
    d.addEventListener('click',function(e){ if(!e.target.closest('.top')) closeMenu(false); });
    window.addEventListener('resize',function(){ if(window.innerWidth>900) closeMenu(false); });
  }

  /* the before/after switch: one class on <body> flips every pair on the page */
  var btns=[].slice.call(d.querySelectorAll('.sw button')), live=d.getElementById('sw-live');
  var sayOn=body.getAttribute('data-say-on')||'Showing the Monday with a system.';
  var sayOff=body.getAttribute('data-say-off')||'Showing the Monday without a system.';
  var touched=false;
  function set(on,source){
    if(on===body.classList.contains('with')) return;
    body.classList.toggle('with',on);
    btns.forEach(function(b){ b.setAttribute('aria-pressed',String((b.getAttribute('data-state')==='with')===on)); });
    if(live) live.textContent=on?sayOn:sayOff;
    ev('before_after_toggle',{state:on?'with':'without',source:source});
  }
  btns.forEach(function(b){ b.addEventListener('click',function(){ touched=true; set(b.getAttribute('data-state')==='with','switch'); }); });
  [].forEach.call(d.querySelectorAll('[data-flip]'),function(b){ b.addEventListener('click',function(){ touched=true; set(!body.classList.contains('with'),'button'); }); });

  /* if the visitor reaches the proof without touching the switch, flip it once so the "with" side isn't missed */
  var auto=body.getAttribute('data-autoflip'), target=auto&&d.querySelector(auto);
  if(target&&'IntersectionObserver' in window){
    var timer=0;
    var io=new IntersectionObserver(function(entries){
      entries.forEach(function(e){
        if(touched){ io.disconnect(); return; }
        if(e.isIntersecting&&!timer){
          timer=setTimeout(function(){
            io.disconnect();
            if(touched) return;
            touched=true; set(true,'auto');
            var sw=d.querySelector('.sw');
            if(sw){ sw.classList.add('nudge'); setTimeout(function(){ sw.classList.remove('nudge'); },1800); }
          },900);
        } else if(!e.isIntersecting&&timer){ clearTimeout(timer); timer=0; }
      });
    },{rootMargin:'0px 0px -40% 0px'});
    io.observe(target);
  }

  /* phone call-to-action bar: after the first screen, until the contact or request section */
  var bar=d.getElementById('mcta');
  if(bar){
    var stop=d.querySelector(bar.getAttribute('data-stop')||'#contact'), ticking=false;
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

  /* events: questions opened, videos played */
  [].forEach.call(d.querySelectorAll('.faq details'),function(det){
    det.addEventListener('toggle',function(){
      if(!det.open) return;
      var s=det.querySelector('summary');
      ev('faq_open',{question:s?s.textContent.trim().slice(0,100):''});
    });
  });
  [].forEach.call(d.querySelectorAll('video[data-video]'),function(v){
    var sent=false;
    v.addEventListener('play',function(){ if(sent) return; sent=true; ev('video_play',{video:v.getAttribute('data-video')}); });
  });

  /* forms: Web3Forms over fetch, with a plain email fallback. Without JavaScript the form posts normally. */
  function link(href,text,ext){
    var a=d.createElement('a'); a.href=href; a.textContent=text;
    if(ext){ a.target='_blank'; a.rel='noopener'; }
    return a;
  }
  [].forEach.call(d.querySelectorAll('form[data-w3f]'),function(form){
    var name=form.getAttribute('data-w3f'), st=form.querySelector('.status'), btn=form.querySelector('button[type="submit"]');
    form.addEventListener('submit',function(e){
      e.preventDefault();
      var fd=new FormData(form);
      if(fd.get('website')){ form.reset(); return; }
      fd.delete('website');
      if(btn) btn.disabled=true;
      st.className='status'; st.textContent='Sending…';
      fetch('https://api.web3forms.com/submit',{method:'POST',headers:{Accept:'application/json'},body:fd})
        .then(function(r){ return r.json(); })
        .then(function(j){
          if(!(j&&j.success)) throw new Error('send');
          st.className='status ok'; st.textContent='Thanks, got it. I’ll reply within one working day. Want to move faster? ';
          var a=link(BOOK,'Pick a time for a free 30-minute call',true);
          a.addEventListener('click',function(){ ev('generate_lead',{method:'booking'}); });
          st.appendChild(a); st.appendChild(d.createTextNode('.'));
          ev('generate_lead',{method:'form',form:name});
          form.reset();
        })
        .catch(function(){
          var subject=form.querySelector('input[name="subject"]');
          var text='Name: '+(fd.get('name')||'')+'\nEmail: '+(fd.get('email')||'')+'\n\n'+(fd.get('message')||'');
          st.className='status err'; st.textContent='That didn’t go through. Please ';
          var mail=link('mailto:info@AmrMagdy.com?subject='+encodeURIComponent(subject?subject.value:'Website inquiry')+'&body='+encodeURIComponent(text),'email it to me instead');
          /* counted as a form lead, not as a plain email click from the page-wide listener */
          mail.addEventListener('click',function(e){ e.stopPropagation(); ev('generate_lead',{method:'form_mailto',form:name}); });
          st.appendChild(mail);
          st.appendChild(d.createTextNode(' (your message is already in it), or '));
          st.appendChild(link(BOOK,'book a call',true));
          st.appendChild(d.createTextNode('.'));
        })
        .then(function(){ if(btn) btn.disabled=false; });
    });
  });

  /* copy buttons (about page bios): shown only when the clipboard is available; if copying is blocked, the text is selected instead */
  var copyLive=d.getElementById('copy-live');
  [].forEach.call(d.querySelectorAll('[data-copy]'),function(b){
    var t=d.querySelector(b.getAttribute('data-copy'));
    if(!t||!navigator.clipboard) return;
    b.hidden=false;
    b.addEventListener('click',function(){
      navigator.clipboard.writeText(t.textContent.trim()).then(function(){
        if(copyLive) copyLive.textContent=b.getAttribute('data-done')||'Copied';
        ev('bio_copy',{bio:b.getAttribute('data-copy').slice(1)});
      },function(){
        var r=d.createRange(); r.selectNodeContents(t);
        var sel=window.getSelection(); sel.removeAllRanges(); sel.addRange(r);
        if(copyLive) copyLive.textContent='Text selected. Press Ctrl+C or Cmd+C to copy.';
      });
    });
  });

  [].forEach.call(d.querySelectorAll('[data-year]'),function(el){ el.textContent=new Date().getFullYear(); });
})();
