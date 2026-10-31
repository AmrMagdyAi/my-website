/* Direct booking and deposit links for amrmagdy.com. Set the two URLs below; leave one empty and the site falls back to the contact form. */
(function(){
var BOOK_URL='https://calendly.com/amr-magdy-crm/30min';     // Calendly / Cal.com link for the free 30-minute call
var DEPOSIT_URL='';  // $750 CRM Revenue Audit deposit payment link
window.AMR_LINKS={book:BOOK_URL,deposit:DEPOSIT_URL};
var CALL=/free (30-minute )?call|book free audit/i;
function ev(m,p){if(window.gtag)gtag('event','generate_lead',{method:m,position:p,page_path:location.pathname});}
function ext(a,u,m,p){a.href=u;a.target='_blank';a.rel='noopener';a.addEventListener('click',function(){ev(m,p);});}
// where on the page the link sits: data-book="name" if set, otherwise the nearest section, header, footer or bar
function pos(a){var v=a.getAttribute('data-book');if(v)return v;var s=a.closest&&a.closest('#nav,.mcta,.switchbar,footer,header,section,article,aside');return s?(s.id||String(s.className).split(' ')[0]||s.tagName.toLowerCase()):'page';}
// Calendly keeps UTM tags on each booking, so every booked call shows the page and button it came from.
// The page name uses underscores so the pages' own click listeners (which match "crm-revenue-audit" etc. in hrefs) don't count booking clicks as other clicks.
function utm(u,p){var pg=(location.pathname.split('/').pop().replace(/\.html$/,'').replace(/^index$/,'')||'home').replace(/-/g,'_');return u+(u.indexOf('?')<0?'?':'&')+'utm_source=amrmagdy.com&utm_medium=website&utm_campaign='+encodeURIComponent(pg)+'&utm_content='+encodeURIComponent(p);}
function run(){
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
