/* ===== Unit conversion ===== */
function fv(x,d){if(!isFinite(x))return '—';if(x===0)return '0';var a=Math.abs(x);if(a>=1e15||a<1e-9)return x.toExponential(4);return N(x,a<1?8:Math.max(d,2))}

C.conv=function(v){
 var c=window.CV,f=c.f,d=c.d,fx,rx,a=c.a,b=c.b,x=v.v,st=[],ex='';
 if(c.fn==='c2f'){fx=function(t){return t*9/5+32};rx=function(t){return (t-32)*5/9}}
 else if(c.fn==='f2c'){fx=function(t){return (t-32)*5/9};rx=function(t){return t*9/5+32}}
 else{fx=function(t){return t*f};rx=function(t){return t/f}}
 var ftFrom=c.ftin&&a[1]==='ft',cmFrom=c.ftin&&a[1]==='cm';
 if(ftFrom){var tot=v.v*12+(v.i||0);if(tot<0)return bad('Please enter positive values.');x=tot/12}
 if(!isFinite(x))return bad();
 if(c.fn==='lin'&&x<0)return bad('Please enter a positive value.');
 var y=fx(x);
 if(ftFrom){st.push(S(N(v.v,2)+' ft '+N(v.i||0,2)+' in',fv(y,d)+' '+b[1],1));st.push(S('Total inches',fv(tot,2)+' in'))}
 else if(cmFrom){var ti=x/2.54,ft=Math.floor(ti/12+1e-9),ins=ti-ft*12;st.push(S(fv(x,d)+' cm',fv(y,d)+' ft',1));st.push(S('Feet and inches',ft+' ft '+N(ins,1)+' in'));st.push(S('Total inches',fv(ti,2)+' in'))}
 else{st.push(S(fv(x,d)+' '+a[1],fv(y,d)+' '+b[1],1));st.push(S('Reverse: '+fv(x,d)+' '+b[1],fv(rx(x),d)+' '+a[1]))}
 if(c.alt)st.push(S(b[0]==='US gallons'?'UK (imperial) gallons':c.alt[0],fv(x*c.alt[1],d)));
 if(c.fn==='lin'&&!ftFrom&&!cmFrom)st.push(S('1 '+a[1],fv(f,6)+' '+b[1]));
 var rows=c.vals.map(function(t){var o=[fv(t,d)+' '+(ftFrom?'ft':a[1]),fv(fx(t),d)+' '+b[1]];if(c.alt)o.push(fv(t*c.alt[1],d));return o});
 var head=[a[0]+' ('+a[1]+')',b[0]+' ('+b[1]+')'];if(c.alt)head.push(c.alt[0]);
 return {stats:st,table:{head:head,rows:rows}}};

C.bigha=function(v){
 var S0=window.CV.states[+v.st],sz=S0[1],ac=v.v;
 if(!(ac>=0))return bad('Please enter a positive value.');
 var big=v.dir==='ab',res=big?ac*43560/sz:ac*sz/43560;
 var st=[S(big?N(ac,4)+' acre in '+S0[0]:N(ac,4)+' bigha in '+S0[0],N(res,4)+(big?' bigha':' acres'),1),S('1 bigha ('+S0[0]+')',N(sz,0)+' sq ft'),S('Area in sq ft',N(big?ac*43560:ac*sz,0)+' sq ft'),S('Area in sq m',N((big?ac*43560:ac*sz)*0.09290304,1)+' sq m')];
 var rows=window.CV.states.map(function(s){return [s[0],N(s[1],0),big?N(ac*43560/s[1],4)+' bigha':N(ac*s[1]/43560,4)+' acres']});
 return {stats:st,table:{head:['State','Sq ft per bigha',big?'Bigha in '+N(ac,2)+' acre':'Acres in '+N(ac,2)+' bigha'],rows:rows},
  note:'Bigha size varies by state, district and even village. Always confirm the size in your local land records.'}};

C.uc=function(v){
 var U=window.CV.units,k=v.cat,lst=U[k][1],fs=v['f_'+k],ts=v['t_'+k],x=v.v;
 if(!isFinite(x))return bad('Please enter a value.');
 function find(s){for(var i=0;i<lst.length;i++)if(lst[i][1]===s)return lst[i]}
 var f=find(fs),t=find(ts);if(!f||!t)return bad();
 function conv(val,from,to){
  if(k==='temperature'){var c=from[1]==='°C'?val:from[1]==='°F'?(val-32)*5/9:val-273.15;return to[1]==='°C'?c:to[1]==='°F'?c*9/5+32:c+273.15}
  return val*from[2]/to[2]}
 var y=conv(x,f,t);
 if(k==='temperature'&&((f[1]==='K'&&x<0)||(f[1]==='°C'&&x<-273.15)||(f[1]==='°F'&&x<-459.67)))return bad('That is below absolute zero.');
 var rows=lst.map(function(u){return [u[0]+' ('+u[1]+')',fv(conv(x,f,u),6)]});
 return {stats:[S(fv(x,6)+' '+f[1],fv(y,6)+' '+t[1],1),S('Reverse: '+fv(x,6)+' '+t[1],fv(conv(x,t,f),6)+' '+f[1])],table:{head:['Unit','Value of '+fv(x,6)+' '+f[1]],rows:rows}}};
C.uc.init=function(box,run){
 var host=box.querySelector('.row'),w=document.createElement('div');w.className='fld';w.style.alignSelf='end';
 var b=document.createElement('button');b.type='button';b.className='btn sm';b.textContent='Swap units';w.appendChild(b);host.appendChild(w);
 b.onclick=function(){var k=box.querySelector('#cat').value,f=box.querySelector('#f_'+k),t=box.querySelector('#t_'+k),tmp=f.value;f.value=t.value;t.value=tmp;run()}};
