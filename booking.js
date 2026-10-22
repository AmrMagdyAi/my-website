/* Direct booking and deposit links for amrmagdy.com. Set the two URLs below; leave one empty and the site falls back to the contact form. */
(function(){
var BOOK_URL='https://calendly.com/amr-magdy-crm/30min';     // Calendly / Cal.com link for the free 30-minute call
var DEPOSIT_URL='';  // $750 CRM Revenue Audit deposit payment link
window.AMR_LINKS={book:BOOK_URL,deposit:DEPOSIT_URL};
var CALL=/free (30-minute )?call|book free audit/i;
function ev(m){if(window.gtag)gtag('event','generate_lead',{method:m,page_path:location.pathname});}
function ext(a,u,m){a.href=u;a.target='_blank';a.rel='noopener';a.addEventListener('click',function(){ev(m);});}
function run(){
 if(BOOK_URL){
  document.querySelectorAll('a[href]').forEach(function(a){
   var h=a.getAttribute('href');
   if(a.hasAttribute('data-book')||(/(^|index\.html)#contact$/.test(h)&&CALL.test(a.textContent)))ext(a,BOOK_URL,'booking');
  });
 }
 document.querySelectorAll('[data-book-only],[data-deposit-only]').forEach(function(el){
  var u=el.hasAttribute('data-book-only')?BOOK_URL:DEPOSIT_URL;
  if(u)el.style.display="";
 });
 if(DEPOSIT_URL)document.querySelectorAll('a[data-deposit]').forEach(function(a){ext(a,DEPOSIT_URL,'deposit');});
}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',run);else run();
})();
