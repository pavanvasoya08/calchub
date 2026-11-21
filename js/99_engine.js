/* ---------------- Engine (runs the calculator on the page) ---------------- */
var calcName=B.dataset.calc;
if(calcName&&C[calcName]){
 var box=byId('calc'),out=byId('out'),fn=C[calcName];
 var fields=box.querySelectorAll('input,select,textarea');
 var todayStr=(function(){var t=new Date();return t.getFullYear()+'-'+pad(t.getMonth()+1)+'-'+pad(t.getDate())})();
 box.querySelectorAll('[data-today]').forEach(function(e){e.value=todayStr});
 function read(){var v={};fields.forEach(function(e){if(!e.id)return;
  v[e.id]=e.type==='number'?(parseFloat(e.value)||0):e.type==='checkbox'?e.checked:e.value});return v}
 function toggle(v){box.querySelectorAll('[data-when]').forEach(function(w){var p=w.dataset.when.split('='),ok=p[1].split('|').indexOf(String(v[p[0]]))>-1;w.classList.toggle('hidden',!ok)})}
 function copyText(t,btn){var done=function(){var o=btn.textContent;btn.textContent='Copied';setTimeout(function(){btn.textContent=o},1200)};
  try{navigator.clipboard.writeText(t).then(done,function(){fallback()})}catch(e){fallback()}
  function fallback(){var ta=document.createElement('textarea');ta.value=t;document.body.appendChild(ta);ta.select();try{document.execCommand('copy');done()}catch(e){}ta.remove()}}
 function render(r){
  if(r.err){out.innerHTML='<div class="note err">'+esc(r.err)+'</div>';return}
  var h='';
  if(r.stats&&r.stats.length)h+='<div class="stats">'+r.stats.map(function(s){return '<div class="stat'+(s[2]?' hi':'')+'"><small>'+s[0]+'</small><b>'+s[1]+'</b></div>'}).join('')+'</div>';
  if(r.bar){var a=r.bar[0],b=r.bar[1],p=a+b>0?Math.max(0,Math.min(100,a/(a+b)*100)):0;
   h+='<div class="bar"><i style="width:'+p.toFixed(1)+'%"></i></div><div class="legend"><span><s style="background:#8bb494"></s>'+r.bar[2]+' '+p.toFixed(0)+'%</span><span><s style="background:#ffe066"></s>'+r.bar[3]+' '+(100-p).toFixed(0)+'%</span></div>'}
  if(r.table){h+='<div class="tblwrap"><table><tr>'+r.table.head.map(function(x){return '<th>'+x+'</th>'}).join('')+'</tr>'+r.table.rows.map(function(row){return '<tr>'+row.map(function(c){return '<td>'+c+'</td>'}).join('')+'</tr>'}).join('')+'</table></div>'}
  if(r.blocks)h+=r.blocks.map(function(b,i){return '<div class="blk"><div class="bh"><small>'+esc(b[0])+'</small><button type="button" class="btn sm cp" data-i="'+i+'">Copy</button></div><textarea readonly rows="'+Math.min(8,Math.max(2,String(b[1]).split('\n').length))+'"></textarea></div>'}).join('');
  if(r.note)h+='<p class="note">'+r.note+'</p>';
  out.innerHTML=h;
  if(r.blocks)out.querySelectorAll('.blk').forEach(function(el,i){var ta=el.querySelector('textarea');ta.value=r.blocks[i][1];el.querySelector('.cp').onclick=function(){copyText(r.blocks[i][1],this)}})}
 function run(){var v=read();toggle(v);var res;try{res=fn(v)}catch(e){res=bad()}render(res)}
 fields.forEach(function(e){e.addEventListener('input',run);e.addEventListener('change',run)});
 box.querySelectorAll('[data-run]').forEach(function(b){b.addEventListener('click',run)});
 if(fn.init)fn.init(box,run);
 run();
 if(fn.tick)setInterval(run,1000)}

/* ---------------- Home page quick EMI ---------------- */
var qp=byId('qp');
if(qp){var qf=function(){var P=parseFloat(byId('qp').value)||0,r=parseFloat(byId('qr').value)||0,m=Math.round((parseFloat(byId('qy').value)||0)*12),o=byId('qout');
 if(P<=0||m<1||r<0){o.innerHTML='<div class="note err">Enter valid values.</div>';return}
 var e=emiOf(P,r/1200,m);o.innerHTML='<div class="stats">'+[['Monthly EMI',M(e),1],['Total interest',M(e*m-P)],['Total payment',M(e*m)]].map(function(s){return '<div class="stat'+(s[2]?' hi':'')+'"><small>'+s[0]+'</small><b>'+s[1]+'</b></div>'}).join('')+'</div>'};
 ['qp','qr','qy'].forEach(function(i){byId(i).addEventListener('input',qf)});qf()}

/* ---------------- Category carousel ---------------- */
var cr=byId('catRow');
if(cr){byId('catPrev').addEventListener('click',function(){cr.scrollBy({left:-420,behavior:'smooth'})});byId('catNext').addEventListener('click',function(){cr.scrollBy({left:420,behavior:'smooth'})})}

/* ---------------- Site search (uses window.IDX from index.js) ---------------- */
function bindSearch(inputId,resId){
 var inp=byId(inputId),res=byId(resId);if(!inp||!res||!window.IDX)return;
 function show(){var q=inp.value.toLowerCase().trim();
  if(!q){res.classList.add('hidden');res.innerHTML='';return}
  var words=q.split(/\s+/),sc=[];
  window.IDX.forEach(function(c){var n=c[0].toLowerCase(),hay=(c[0]+' '+c[2]+' '+c[3]+' '+c[4]).toLowerCase(),s=0,ok=true;
   words.forEach(function(w){if(hay.indexOf(w)<0)ok=false});if(!ok)return;
   if(n.indexOf(q)===0)s+=5;else if(n.indexOf(q)>-1)s+=3;sc.push([s,c])});
  sc.sort(function(a,b){return b[0]-a[0]});
  res.innerHTML=sc.length?sc.slice(0,12).map(function(x){var c=x[1];return '<a href="'+c[1]+'"><b>'+esc(c[0])+'</b><small>'+esc(c[3])+'</small></a>'}).join(''):'<p class="none">No calculators found. Try another word.</p>';
  res.classList.remove('hidden')}
 inp.addEventListener('input',show);inp.addEventListener('focus',show);
 inp.addEventListener('keydown',function(e){if(e.key==='Escape'){res.classList.add('hidden');inp.blur()}if(e.key==='Enter'){var a=res.querySelector('a');if(a)location.href=a.getAttribute('href')}});
 document.addEventListener('click',function(e){if(!res.contains(e.target)&&e.target!==inp)res.classList.add('hidden')})}
bindSearch('hq','hres');bindSearch('q','qres');
document.addEventListener('click',function(e){document.querySelectorAll('details.dd[open]').forEach(function(d){if(!d.contains(e.target))d.removeAttribute('open')})});
})();
