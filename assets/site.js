/* amrmagdy.com: dark mode, phone menu, the before/after switch, the phone call-to-action bar, forms and GA4 events
   (before_after_toggle, faq_open, video_play, bio_copy, and generate_lead with method form / form_mailto / booking).
   The booking link a form shows after sending carries the same UTM tags as booking.js (utm_content form-success or form-error).
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
    try{document.cookie='theme='+(dark?'dark':'light')+';path=/;max-age=31536000;SameSite=Lax';}catch(e){}
    /* last resorts for browsers that block storage and cookies: this tab's session storage and its window name */
    try{sessionStorage.setItem('theme',dark?'dark':'light');}catch(e){}
    try{if(!window.name||/^theme-/.test(window.name))window.name='theme-'+(dark?'dark':'light');}catch(e){}
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

  /* the before/after switch: one class on <body> flips every pair on the page */
  var btns=[].slice.call(d.querySelectorAll('.sw button')), live=d.getElementById('sw-live');
  var sayOn=body.getAttribute('data-say-on')||'Showing a change done this week.';
  var sayOff=body.getAttribute('data-say-off')||'Showing a change waiting on a ticket.';
  var touched=false;
  function set(on,source,quiet){
    if(on===body.classList.contains('with')) return;
    body.classList.toggle('with',on);
    btns.forEach(function(b){ b.setAttribute('aria-pressed',String((b.getAttribute('data-state')==='with')===on)); });
    if(quiet) return;
    if(live) live.textContent=on?sayOn:sayOff;
    ev('before_after_toggle',{state:on?'with':'without',source:source});
  }
  function touch(){ touched=true; body.classList.add('touched'); }
  btns.forEach(function(b){ b.addEventListener('click',function(){ touch(); set(b.getAttribute('data-state')==='with','switch'); }); });
  [].forEach.call(d.querySelectorAll('[data-flip]'),function(b){ b.addEventListener('click',function(){ touch(); set(!body.classList.contains('with'),'button'); }); });

  /* a short preview for visitors who haven't found the switch: after a few seconds on the first screen it flips to
     "done this week" for a moment and back, with no announcement and no analytics event. It never runs for visitors
     who asked for less motion, scrolled, pressed a key or touched anything, and runs once per browser tab. */
  if(btns.length&&d.getElementById('monday')&&!(window.matchMedia&&window.matchMedia('(prefers-reduced-motion: reduce)').matches)){
    var seen=false; try{ seen=sessionStorage.getItem('ba_demo')==='1'; }catch(e){}
    if(!seen){
      var busy=false, stopDemo=function(){ busy=true; };
      ['wheel','touchstart','keydown','pointerdown','scroll'].forEach(function(n){ window.addEventListener(n,stopDemo,{passive:true,once:true}); });
      setTimeout(function(){
        if(busy||touched||d.hidden||(window.scrollY||root.scrollTop)>8) return;
        try{ sessionStorage.setItem('ba_demo','1'); }catch(e){}
        set(true,'demo',true);
        setTimeout(function(){ if(!touched) set(false,'demo',true); },2600);
      },5000);
    }
  }

  /* if the visitor reaches the proof without touching the switch, flip it once so the "with" side isn't missed.
     Only for visitors scrolling with a mouse or a finger who haven't asked for less motion. Keyboard and
     screen-reader visitors get the nudge alone, so the text doesn't change under them while they read. */
  var auto=body.getAttribute('data-autoflip'), target=auto&&d.querySelector(auto);
  if(target&&'IntersectionObserver' in window){
    var timer=0, scrolled=false;
    var still=!!(window.matchMedia&&window.matchMedia('(prefers-reduced-motion: reduce)').matches);
    var mark=function(){ scrolled=true; };
    window.addEventListener('wheel',mark,{passive:true,once:true});
    window.addEventListener('touchmove',mark,{passive:true,once:true});
    var io=new IntersectionObserver(function(entries){
      entries.forEach(function(e){
        if(touched){ io.disconnect(); return; }
        if(e.isIntersecting&&!timer){
          timer=setTimeout(function(){
            io.disconnect();
            if(touched) return;
            if(scrolled&&!still){ touch(); set(true,'auto'); }
            var sw=d.querySelector('.sw');
            if(sw){ sw.classList.add('nudge'); setTimeout(function(){ sw.classList.remove('nudge'); },1800); }
          },900);
        } else if(!e.isIntersecting&&timer){ clearTimeout(timer); timer=0; }
      });
    },{rootMargin:'0px 0px -40% 0px'});
    io.observe(target);
  }

  /* phone call-to-action bar: after a short scroll, until the contact or request section */
  var bar=d.getElementById('mcta');
  if(bar){
    var stop=d.querySelector(bar.getAttribute('data-stop')||'#contact'), ticking=false;
    /* guides and tools: the bar shows after a short scroll, so a booking button is never far away on a phone. Pages whose first screen already has one set data-after="0.85" */
    var after=parseFloat(bar.getAttribute('data-after'))||0.4;
    var upd=function(){
      ticking=false;
      var y=window.scrollY||root.scrollTop;
      var on=y>window.innerHeight*after&&!(stop&&stop.getBoundingClientRect().top<window.innerHeight);
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
  /* a booking link tagged the way booking.js tags the others, so Calendly shows where the booking came from */
  function book(text,position){
    var pg=(location.pathname.split('/').pop().replace(/\.html$/,'').replace(/^index$/,'')||'home').replace(/-/g,'_');
    var a=link(BOOK+'?utm_source=amrmagdy.com&utm_medium=website&utm_campaign='+encodeURIComponent(pg)+'&utm_content='+encodeURIComponent(position),text,true);
    a.addEventListener('click',function(){ ev('generate_lead',{method:'booking',position:position}); });
    return a;
  }
  var FIELDS={name:'Name',email:'Email',company:'Company',phone:'Phone',crm:'CRM'};
  [].forEach.call(d.querySelectorAll('form[data-w3f]'),function(form){
    var name=form.getAttribute('data-w3f'), st=form.querySelector('.status'), btn=form.querySelector('button[type="submit"]'), busy=false;
    if(!st){ st=d.createElement('p'); st.className='status'; st.setAttribute('role','status'); form.appendChild(st); }
    /* the email fallback carries everything the visitor typed */
    function fail(fd){
      var subject=form.querySelector('input[name="subject"]'), lines=[];
      Object.keys(FIELDS).forEach(function(k){ var v=fd.get(k); if(v) lines.push(FIELDS[k]+': '+v); });
      if(fd.get('message')) lines.push('',fd.get('message'));
      st.className='status err'; st.textContent='That didn’t go through. Please ';
      var mail=link('mailto:info@AmrMagdy.com?subject='+encodeURIComponent(subject?subject.value:'Website inquiry')+'&body='+encodeURIComponent(lines.join('\n')),'email it to me instead');
      /* counted as a form lead, not as a plain email click from the page-wide listener */
      mail.addEventListener('click',function(e){ e.stopPropagation(); ev('generate_lead',{method:'form_mailto',form:name}); });
      st.appendChild(mail);
      st.appendChild(d.createTextNode(' (your message is already in it), or '));
      st.appendChild(book('book a call','form-error'));
      st.appendChild(d.createTextNode('.'));
    }
    form.addEventListener('submit',function(e){
      e.preventDefault();
      if(busy) return;
      var fd=new FormData(form);
      /* the hidden field is filled: a bot, or an autofill tool. Offer the email route rather than drop a real message. */
      if(fd.get('website')){ fail(fd); return; }
      fd.delete('website');
      /* aria-disabled rather than disabled, so focus stays on the button */
      busy=true; if(btn) btn.setAttribute('aria-disabled','true');
      st.className='status'; st.textContent='Sending…';
      fetch('https://api.web3forms.com/submit',{method:'POST',headers:{Accept:'application/json'},body:fd})
        .then(function(r){ return r.json(); })
        .then(function(j){
          if(!(j&&j.success)) throw new Error('send');
          st.className='status ok'; st.textContent='Thanks, got it. I’ll reply within one working day. Want to move faster? ';
          st.appendChild(book('Pick a time for a free 30-minute call','form-success'));
          st.appendChild(d.createTextNode('.'));
          ev('generate_lead',{method:'form',form:name});
          form.reset();
        })
        .catch(function(){ fail(fd); })
        .then(function(){ busy=false; if(btn) btn.removeAttribute('aria-disabled'); });
    });
  });

  /* copy buttons (about page bios): shown only when the clipboard is available; if copying is blocked, the text is selected instead */
  var copyLive=d.getElementById('copy-live');
  /* cleared first, so copying the same bio twice is announced twice */
  function say(m){ if(!copyLive) return; copyLive.textContent=''; setTimeout(function(){ copyLive.textContent=m; },100); }
  [].forEach.call(d.querySelectorAll('[data-copy]'),function(b){
    var t=d.querySelector(b.getAttribute('data-copy'));
    if(!t||!navigator.clipboard) return;
    b.hidden=false;
    b.addEventListener('click',function(){
      navigator.clipboard.writeText(t.textContent.trim()).then(function(){
        say(b.getAttribute('data-done')||'Copied');
        ev('bio_copy',{bio:b.getAttribute('data-copy').slice(1)});
      },function(){
        var r=d.createRange(); r.selectNodeContents(t);
        var sel=window.getSelection(); sel.removeAllRanges(); sel.addRange(r);
        say('Text selected. Use your device’s Copy command.');
      });
    });
  });

  [].forEach.call(d.querySelectorAll('[data-year]'),function(el){ el.textContent=new Date().getFullYear(); });
})();
