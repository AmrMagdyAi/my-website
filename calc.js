/* Shared helpers for amrmagdy.com calculators: currency, formatting, embed mode, embed code. */
(function(){
var CUR={USD:{s:'$',l:'en-US'},CAD:{s:'CA$',l:'en-CA'},GBP:{s:'£',l:'en-GB'},EUR:{s:'€',l:'de-DE'}};
function guess(){try{var s=localStorage.getItem('cur');if(s&&CUR[s])return s}catch(e){}
 var L=(navigator.language||'en-US');if(/-CA$/i.test(L)||/^fr-CA/i.test(L))return 'CAD';if(/-GB$/i.test(L))return 'GBP';if(/-IE$/i.test(L))return 'EUR';
 if(/^(de|fr|es|it|nl|pt|fi|el|sk|sl|et|lv|lt|mt)\b/i.test(L))return 'EUR';return 'USD';}
var C={cur:guess()};
C.money=function(x){if(!isFinite(x))return '—';var c=CUR[C.cur],neg=x<0,v=Math.abs(Math.round(x)).toLocaleString(c.l);return (neg?'−':'')+c.s+v;};
C.pct=function(x,d){if(!isFinite(x))return '—';return (x*100).toFixed(d==null?1:d)+'%';};
C.num=function(id){var e=document.getElementById(id);if(!e)return 0;var v=parseFloat(e.value);return isFinite(v)?v:0;};
C.set=function(id,t,cls){var e=document.getElementById(id);if(!e)return;e.textContent=t;if(cls!=null)e.className=cls;};
C.pmt=function(principal,annualRate,years){var n=years*12,r=annualRate/12;if(principal<=0||n<=0)return 0;if(r===0)return principal/n;return principal*r/(1-Math.pow(1+r,-n));};
var used=false;C.track=function(tool){if(!used&&window.gtag){used=true;gtag('event','calculator_used',{tool:tool,currency:C.cur});}};
C.init=function(tool,compute){
 var sel=document.getElementById('cur');
 function sym(){document.querySelectorAll('.cs').forEach(function(e){e.textContent=CUR[C.cur].s});}
 if(sel){sel.value=C.cur;sel.addEventListener('change',function(){C.cur=sel.value;try{localStorage.setItem('cur',C.cur)}catch(e){}sym();compute();});}
 sym();
 document.querySelectorAll('.fld input,.fld select').forEach(function(i){if(i.id!=='cur'){i.addEventListener('input',function(){compute();C.track(tool);});i.addEventListener('change',compute);}});
 var run=compute;compute=function(){run();var h=document.getElementById('hl'),m=document.getElementById('mbar-v');if(h&&m)m.textContent=h.textContent;};
 compute();
 // embed mode
 var q=new URLSearchParams(location.search);
 if(q.get('embed')==='1'){document.documentElement.classList.add('embed');
  var a=document.createElement('p');a.className='embed-by';a.innerHTML='Free calculator by <a href="'+location.origin+location.pathname+'" target="_blank" rel="noopener">Amr Magdy</a>';document.querySelector('main .pg-w').appendChild(a);}
 var box=document.getElementById('embed-code');
 if(box){var url=location.origin+location.pathname,t=document.querySelector('h1').textContent.replace(/\.$/,'');
  box.value='<iframe src="'+url+'?embed=1" title="'+t+'" width="100%" height="760" style="border:0;max-width:960px" loading="lazy"></iframe>\n<p style="font-size:13px">'+t+' by <a href="'+url+'">Amr Magdy</a></p>';
  var b=document.getElementById('embed-copy');if(b)b.addEventListener('click',function(){box.select();try{navigator.clipboard.writeText(box.value)}catch(e){document.execCommand('copy')}b.textContent='Copied';if(window.gtag)gtag('event','embed_code_copied',{tool:tool});});}
};
window.CALC=C;
})();
