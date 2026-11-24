/* Direct booking and deposit links for amrmagdy.com. Set the two URLs below; leave one empty and the site falls back to the contact form. */
(function(){
var BOOK_URL='https://calendly.com/amr-magdy-crm/15-minute-climbmark-setup-help';     // Calendly / Cal.com link for the free 15-minute call
var DEPOSIT_URL='';  // payment link for a paid project deposit; empty on purpose
window.AMR_LINKS={book:BOOK_URL,deposit:DEPOSIT_URL};
var CALL=/free (\d+[- ]?min(ute)?s? )?call/i;
function ev(m,p){if(window.gtag)gtag('event','generate_lead',{method:m,position:p,page_path:location.pathname});}
function ext(a,u,m,p){a.href=u;a.target='_blank';a.rel='noopener';a.addEventListener('click',function(){ev(m,p);});}
// where on the page the link sits: data-book="name" if set, otherwise the nearest section, header, footer or bar
function pos(a){var v=a.getAttribute('data-book');if(v)return v;var s=a.closest&&a.closest('#nav,.mcta,.switchbar,footer,header,section,article,aside');return s?(s.id||String(s.className).split(' ')[0]||s.tagName.toLowerCase()):'page';}
// Calendly keeps UTM tags on each booking, so every booked call shows the page and button it came from.
// The page name uses underscores so the pages' own click listeners (which match "crm-revenue-audit" etc. in hrefs) don't count booking clicks as other clicks.
// Campaign tags (utm_*) on the landing address are kept for this tab only (sessionStorage, cleared when the tab closes), so a booking made pages later still shows which post, message or group brought the visitor in.
var TAGS=['utm_source','utm_medium','utm_campaign','utm_content'];
function clean(v){v=(v||'').slice(0,64);return /^[A-Za-z0-9._ -]+$/.test(v)?v:'';}
function landing(){var t={},q;try{q=new URLSearchParams(location.search);}catch(e){return t;}TAGS.forEach(function(k){var v=clean(q.get(k));if(v)t[k]=v;});if(t.utm_source){try{sessionStorage.setItem('amr_utm',JSON.stringify(t));}catch(e){}}return t;}
function saved(){var t=landing();if(t.utm_source)return t;try{var o=JSON.parse(sessionStorage.getItem('amr_utm')||'{}');TAGS.forEach(function(k){if(o[k])t[k]=clean(o[k]);});}catch(e){}return t;}
function utm(u,p){var pg=(location.pathname.split('/').pop().replace(/\.html$/,'').replace(/^index$/,'')||'home').replace(/-/g,'_');var t=saved(),q;
 if(t.utm_source){q={utm_source:t.utm_source,utm_medium:t.utm_medium||'social',utm_campaign:t.utm_campaign||pg,utm_content:pg+':'+p};if(t.utm_content)q.utm_term=t.utm_content;}
 else q={utm_source:'amrmagdy.com',utm_medium:'website',utm_campaign:pg,utm_content:p};
 return u+(u.indexOf('?')<0?'?':'&')+Object.keys(q).map(function(k){return k+'='+encodeURIComponent(q[k]);}).join('&');}
function run(){
 landing();
 if(BOOK_URL){
  document.querySelectorAll('a[href]').forEach(function(a){
   var h=a.getAttribute('href');
   if(a.hasAttribute('data-book')||(/(^|index\.html|\.\/)#contact$/.test(h)&&CALL.test(a.textContent))){var p=pos(a);ext(a,utm(BOOK_URL,p),'booking',p);}
  });
 }
 document.querySelectorAll('[data-book-only],[data-deposit-only]').forEach(function(el){
  var u=el.hasAttribute('data-book-only')?BOOK_URL:DEPOSIT_URL;
  if(u)el.style.display="";
 });
 if(DEPOSIT_URL)document.querySelectorAll('a[data-deposit]').forEach(function(a){ext(a,DEPOSIT_URL,'deposit',pos(a));});
}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',run);else run();
})();
