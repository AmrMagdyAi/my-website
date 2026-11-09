/* Homepage "What's stuck?" picker: one pane shows at a time; each pick sends a stuck_pick event so we learn what visitors come for. */
(function(d){
  var chips=[].slice.call(d.querySelectorAll('.chip-pick')), panes=[].slice.call(d.querySelectorAll('.pane'));
  chips.forEach(function(b){ b.addEventListener('click',function(){
    var k=b.getAttribute('data-k');
    chips.forEach(function(x){ x.setAttribute('aria-pressed',x===b?'true':'false'); });
    panes.forEach(function(p){ p.hidden=p.getAttribute('data-k')!==k; });
    try{ if(window.gtag) gtag('event','stuck_pick',{problem:k}); }catch(e){}
  }); });
})(document);
