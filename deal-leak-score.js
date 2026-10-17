(function(){
var cards=[].slice.call(document.querySelectorAll('.qc')),N=cards.length;
var LEAKS=['Spend','Answer','Follow-up','Offer','Keep'];
var ans=new Array(N).fill(null),done=false;
var theirs=null;
try{var p=new URLSearchParams(location.search).get('r');if(p&&/^[01]{10}$/.test(p))theirs=p.split('').map(Number);}catch(e){}
if(theirs){var s=theirs.reduce(function(a,b){return a+b},0)*10,ban=document.getElementById('ban');
 ban.style.display='block';ban.innerHTML='<strong>A teammate scored '+s+' / 100 and sent you this.</strong> Answer the ten checks yourself. Each one will show whether you agree.';}
function band(s){return s>=80?'Tight':s>=50?'Patched':'Leaking'}
function nextStep(){for(var i=0;i<N;i++)if(ans[i]===0)return i;return -1}
function render(){
 var a=ans.filter(function(x){return x!==null}).length,s=ans.reduce(function(t,x){return t+(x||0)},0)*10;
 document.getElementById('prog').textContent=a<N?a+' of '+N+' answered':'All 10 answered';
 cards.forEach(function(c,i){c.classList.toggle('no',ans[i]===0);
  var m=c.querySelector('.cmp');if(theirs&&ans[i]!==null){m.hidden=false;var same=theirs[i]===ans[i];m.className='cmp '+(same?'same':'diff');m.textContent=same?'Matches your teammate':'Your teammate said '+(theirs[i]?'Yes':'No');}});
 var res=document.getElementById('res');if(a<N){res.classList.remove('on');return}
 res.classList.add('on');
 document.getElementById('sc').textContent=s;document.getElementById('band').textContent='· '+band(s);
 document.getElementById('bar').style.width=s+'%';
 var row='';for(var k=0;k<5;k++){var v=(ans[2*k]+ans[2*k+1]);row+='<div class="lkc '+(v===2?'ok':v===1?'mid':'bad')+'"><b>'+v+'/2</b>'+LEAKS[k]+'</div>'}
 document.getElementById('lkrow').innerHTML=row;
 var n=nextStep();document.getElementById('nx').innerHTML=n<0?'All ten checks are in place. Keep reviewing the numbers behind them every Monday.':'Start with check '+(n+1)+' ('+LEAKS[Math.floor(n/2)]+'). It sits closest to the money of the ones still open. The note under it links a free tool for it.';
 if(theirs){var d=0;for(var i=0;i<N;i++)if(theirs[i]!==ans[i])d++;var cn=document.getElementById('cmpnote');cn.hidden=false;
  cn.innerHTML='<strong>You and your teammate disagree on '+d+' of 10 checks.</strong> '+(d?'Those are the processes that live in someone\'s head instead of the CRM. Start there.':'Same answers on every check. Your team sees the business the same way.');}
 var url=location.origin+location.pathname+'?r='+ans.join('');
 document.getElementById('li').href='https://www.linkedin.com/sharing/share-offsite/?url='+encodeURIComponent(location.origin+location.pathname);
 document.getElementById('cp').dataset.url=url;
 if(!done&&window.gtag){done=true;gtag('event','deal_leak_score_completed',{score:s,compared:!!theirs});}
}
cards.forEach(function(c,i){c.querySelectorAll('button').forEach(function(b){b.addEventListener('click',function(){
 c.querySelectorAll('button').forEach(function(x){x.classList.remove('on')});b.classList.add('on');ans[i]=+b.dataset.v;render();
 var nx=cards[i+1];if(nx&&ans[i+1]===null&&window.innerWidth<900)setTimeout(function(){nx.scrollIntoView({behavior:'smooth',block:'center'})},150);
 if(i===N-1||ans.every(function(x){return x!==null}))setTimeout(function(){document.getElementById('res').scrollIntoView({behavior:'smooth',block:'center'})},200);
});});});
document.getElementById('cp').addEventListener('click',function(){var u=this.dataset.url,btn=this;
 function ok(){btn.textContent='Link copied. Send it to your team.';if(window.gtag)gtag('event','deal_leak_score_share',{method:'link'});}
 if(navigator.clipboard)navigator.clipboard.writeText(u).then(ok,function(){prompt('Copy this link',u)});else prompt('Copy this link',u);});
document.getElementById('li').addEventListener('click',function(){if(window.gtag)gtag('event','deal_leak_score_share',{method:'linkedin'});});
document.getElementById('dl').addEventListener('click',function(){
 var s=ans.reduce(function(t,x){return t+(x||0)},0)*10,W=1080,H=1350,c=document.createElement('canvas');c.width=W;c.height=H;var g=c.getContext('2d');
 g.fillStyle='#f7f4ee';g.fillRect(0,0,W,H);
 g.fillStyle='#0b1f3a';g.fillRect(0,0,W,120);g.fillStyle='#d4a23e';g.font='600 34px "Plus Jakarta Sans",Arial';g.fillText('DEAL LEAK SCORE',70,74);
 g.fillStyle='#13243d';g.font='500 300px Fraunces,Georgia,serif';g.fillText(String(s),70,470);
 g.fillStyle='#5b6b80';g.font='500 64px Fraunces,Georgia,serif';g.fillText('/ 100  ·  '+band(s),80,560);
 for(var k=0;k<5;k++){var v=ans[2*k]+ans[2*k+1],y=660+k*112;
  g.fillStyle='#ffffff';g.fillRect(70,y,940,90);g.strokeStyle=v===2?'#1f8a4c':v===1?'#b8862f':'#c0392b';g.lineWidth=4;g.strokeRect(70,y,940,90);
  g.fillStyle='#13243d';g.font='600 40px "Plus Jakarta Sans",Arial';g.fillText(LEAKS[k],110,y+60);
  g.textAlign='right';g.fillText(v+' / 2',970,y+60);g.textAlign='left';}
 g.fillStyle='#0b6bce';g.font='600 36px "Plus Jakarta Sans",Arial';g.fillText('Take it: amrmagdy.com/deal-leak-score',70,1290);
 var a=document.createElement('a');a.download='deal-leak-score-'+s+'.png';a.href=c.toDataURL('image/png');a.click();
 if(window.gtag)gtag('event','deal_leak_score_share',{method:'card'});
});
})();
