/* Cookie choice for visitors in the UK, the EU, the EEA and Switzerland.
   Each page's inline gtag snippet sets Google's consent default first: analytics and ad cookies stay off for
   visitors whose IP is in those regions, and a saved choice (localStorage "ga_consent") is applied before the
   config call. This script asks visitors whose device is set to a European time zone, saves the answer and
   passes it to Google; "Cookie choices" in the footer asks again. Everyone else sees nothing, except the
   button on the privacy page (data-cc-open), which lets anyone switch analytics cookies off or back on. */
(function(){
  'use strict';
  var d=document, KEY='ga_consent', banner=null, live=null, opener=null;
  var tz=''; try{ tz=Intl.DateTimeFormat().resolvedOptions().timeZone||''; }catch(e){}
  var europe=/^Europe\//.test(tz)||/^(Atlantic\/(Canary|Madeira|Azores|Reykjavik|Faroe)|Africa\/Ceuta)$/.test(tz);

  function saved(){ try{ return localStorage.getItem(KEY); }catch(e){ return null; } }
  /* after No thanks, also remove the Google Analytics cookies set earlier (_ga, _ga_<id>) */
  function dropCookies(){
    var h=location.hostname, doms=['',h,h.replace(/^www\./,'')];
    d.cookie.split(';').forEach(function(c){
      var n=c.split('=')[0].trim();
      if(/^_ga(_|$)/.test(n)) doms.forEach(function(dm){ d.cookie=n+'=; Max-Age=0; path=/'+(dm?'; domain='+dm:''); });
    });
  }
  function choose(v){
    try{ localStorage.setItem(KEY,v); }catch(e){}
    if(window.gtag) gtag('consent','update',{analytics_storage:v});
    if(v==='denied') dropCookies();
    banner.hidden=true;
    live.textContent='';
    setTimeout(function(){ live.textContent=(v==='granted'?'Analytics cookies on.':'Analytics cookies off.')+' You can change this under Cookie choices at the bottom of the page.'; },50);
    if(opener){ opener.focus(); opener=null; }
  }

  function setup(){
    var css=d.createElement('style');
    css.textContent='.cc{position:fixed;left:12px;right:12px;bottom:calc(12px + env(safe-area-inset-bottom,0px));z-index:1000;max-width:560px;margin:0 auto;box-sizing:border-box;'+
      'padding:16px 18px;border-radius:14px;background:#22201d;color:#f7f4ef;border:1px solid rgba(255,255,255,.18);box-shadow:0 10px 30px rgba(0,0,0,.28);font-size:15px;line-height:1.5;text-align:left}'+
      '.cc[hidden]{display:none}.cc p{margin:0}.cc a{color:#9fe0d6;text-decoration:underline;text-underline-offset:2px}'+
      '.cc-b{display:flex;flex-wrap:wrap;gap:10px;margin-top:12px}'+
      '.cc-b button{flex:1 1 140px;min-height:44px;padding:0 18px;border:0;border-radius:999px;background:#f7f4ef;color:#22201d;font:inherit;font-weight:600;cursor:pointer}'+
      '.cc:focus{outline:none}.cc:focus-visible,.cc a:focus-visible,.cc-b button:focus-visible{outline:2px solid #4fc4b6;outline-offset:2px}'+
      '.cc-open{padding:0;border:0;background:none;color:inherit;font:inherit;text-decoration:underline;text-underline-offset:2px;cursor:pointer}'+
      '.fl .cc-open{padding:4px 0;text-decoration:none;transition:color .2s}.fl .cc-open:hover{color:var(--gold)}'+
      '.cc-foot{margin:16px 0 0;font-size:.85rem}'+
      '.cc-live{position:absolute;width:1px;height:1px;margin:-1px;padding:0;overflow:hidden;clip:rect(0,0,0,0);white-space:nowrap;border:0}'+
      '@media print{.cc,.cc-foot,.cc-open,[data-cc-open]{display:none!important}}';
    d.head.appendChild(css);
    live=d.createElement('p');
    live.className='cc-live';
    live.setAttribute('role','status');
    d.body.appendChild(live);
  }

  function show(){
    if(!banner){
      banner=d.createElement('section');
      banner.className='cc';
      banner.setAttribute('aria-label','Cookie choice');
      banner.tabIndex=-1;
      banner.innerHTML='<p>Can I use Google Analytics cookies to see which pages help visitors? They don\'t tell me who you are. <span class="cc-now"></span><a href="/privacy#cookies">More about cookies</a></p>'+
        '<div class="cc-b"><button type="button" data-v="granted">Accept</button><button type="button" data-v="denied">No thanks</button></div>';
      banner.addEventListener('click',function(e){ var b=e.target.closest('button[data-v]'); if(b) choose(b.getAttribute('data-v')); });
      banner.addEventListener('keydown',function(e){ if(e.key==='Escape'&&opener){ banner.hidden=true; opener.focus(); opener=null; } });
      /* at the top of the page, right after the skip link, so keyboard and screen-reader visitors reach it early */
      var top=d.body.firstElementChild, skip=top&&top.matches('a[href="#main"],a.skip')?top:null;
      d.body.insertBefore(banner,skip?skip.nextSibling:d.body.firstChild);
    }
    var v=saved();
    banner.querySelector('.cc-now').textContent=v==='granted'?'Right now they\'re on. ':v==='denied'?'Right now they\'re off. ':'';
    banner.hidden=false;
  }

  /* a control that asks again: the footer's "Cookie choices" or the privacy page's button */
  function wire(el){
    var b=el.tagName==='BUTTON'?el:el.querySelector('button'); if(!b) return;
    el.hidden=false;
    b.addEventListener('click',function(){ opener=b; show(); banner.focus(); });
  }
  /* "Cookie choices" goes after the footer's Privacy link, or at the end of a footer without one */
  function footerControl(){
    var f=d.querySelector('footer'); if(!f) return;
    var b=d.createElement('button');
    b.type='button'; b.className='cc-open'; b.textContent='Cookie choices';
    var p=f.querySelector('a[href$="privacy"]');
    if(p){
      var prev=p.previousSibling, dot=prev&&prev.nodeType===3&&/\u00b7\s*$/.test(prev.nodeValue);
      p.parentNode.insertBefore(b,p.nextSibling);
      if(dot) p.parentNode.insertBefore(d.createTextNode(' \u00b7 '),b);
    }else{ var w=d.createElement('p'); w.className='cc-foot'; w.appendChild(b); (f.querySelector('.wrap')||f).appendChild(w); }
    wire(b);
  }

  function run(){
    var own=d.querySelectorAll('[data-cc-open]');
    if(!europe&&!own.length) return;
    setup();
    [].forEach.call(own,wire);
    if(!europe) return;
    footerControl();
    var v=saved();
    if(v!=='granted'&&v!=='denied') show();
  }
  if(d.readyState==='loading') d.addEventListener('DOMContentLoaded',run); else run();
})();
