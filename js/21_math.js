(function(){
function gcd(a,b){a=Math.abs(a);b=Math.abs(b);while(b){var t=a%b;a=b;b=t}return a}
function P(x){return N(x,4)}

/* ---- Percentage ---- */
C.m_pct=function(v){var m=v.m;
 if(m==='of'){var r=v.of_p/100*v.of_v;return {stats:[S(N(v.of_p,4)+'% of '+N(v.of_v,4),P(r),1)],note:'Formula: percentage / 100 x value.'}}
 if(m==='is'){if(!v.is_y)return bad('The total cannot be zero.');var r2=v.is_x/v.is_y*100;return {stats:[S(N(v.is_x,4)+' is what % of '+N(v.is_y,4),P(r2)+' %',1)],note:'Formula: part / total x 100.'}}
 if(m==='chg'){if(!v.ch_a)return bad('The starting value cannot be zero.');var d=v.ch_b-v.ch_a,p=d/Math.abs(v.ch_a)*100;
  return {stats:[S(d>=0?'Percentage increase':'Percentage decrease',P(Math.abs(p))+' %',1),S('Change',P(d))],note:'Formula: (new - old) / old x 100.'}}
 var f=v.ad_p/100,r3=m==='add'?v.ad_v*(1+f):v.ad_v*(1-f);
 return {stats:[S(m==='add'?'Value after adding '+N(v.ad_p,4)+'%':'Value after subtracting '+N(v.ad_p,4)+'%',P(r3),1),S('Amount of change',P(Math.abs(r3-v.ad_v)))]}};

/* ---- Average ---- */
C.m_avg=function(v){var a=nums(v.list);if(!a||!a.length)return bad('Enter numbers separated by commas or spaces.');
 var n=a.length,sum=a.reduce(function(x,y){return x+y},0),s=a.slice().sort(function(x,y){return x-y}),
 med=n%2?s[(n-1)/2]:(s[n/2-1]+s[n/2])/2,cnt={},best=0;a.forEach(function(x){cnt[x]=(cnt[x]||0)+1;if(cnt[x]>best)best=cnt[x]});
 var modes=best>1?Object.keys(cnt).filter(function(k){return cnt[k]===best}).map(Number).sort(function(x,y){return x-y}).map(P).join(', '):'No repeated value';
 return {stats:[S('Average (mean)',P(sum/n),1),S('Median',P(med)),S('Mode',modes),S('Sum',P(sum)),S('Count',String(n)),S('Smallest',P(s[0])),S('Largest',P(s[n-1])),S('Range',P(s[n-1]-s[0]))]}};

/* ---- Scientific (safe parser, no eval) ---- */
function parse(src,deg){var s=src.replace(/\s+/g,'').replace(/×/g,'*').replace(/÷/g,'/').replace(/π/g,'pi').replace(/√/g,'sqrt'),i=0;
 function fail(){throw new Error('x')}
 function toR(x){return deg?x*Math.PI/180:x}function fromR(x){return deg?x*180/Math.PI:x}
 function fact(n){if(n<0||n!==Math.floor(n)||n>170)fail();var r=1;for(var k=2;k<=n;k++)r*=k;return r}
 var F={sin:function(x){return Math.sin(toR(x))},cos:function(x){return Math.cos(toR(x))},tan:function(x){return Math.tan(toR(x))},
  asin:function(x){return fromR(Math.asin(x))},acos:function(x){return fromR(Math.acos(x))},atan:function(x){return fromR(Math.atan(x))},
  sqrt:Math.sqrt,cbrt:Math.cbrt,log:Math.log10,ln:Math.log,exp:Math.exp,abs:Math.abs,fact:fact};
 function expr(){var x=term();while(s[i]==='+'||s[i]==='-'){var o=s[i++],y=term();x=o==='+'?x+y:x-y}return x}
 function term(){var x=unary();while(s[i]==='*'||s[i]==='/'){var o=s[i++],y=unary();x=o==='*'?x*y:x/y}return x}
 function unary(){if(s[i]==='-'){i++;return -unary()}if(s[i]==='+'){i++;return unary()}return power()}
 function power(){var b=post();if(s[i]==='^'){i++;var e=unary();return Math.pow(b,e)}return b}
 function post(){var x=atom();while(s[i]==='!'||s[i]==='%'){if(s[i++]==='!')x=fact(x);else x=x/100}return x}
 function atom(){var m;
  if(s[i]==='('){i++;var x=expr();if(s[i]!==')')fail();i++;return x}
  if((m=/^(\d+\.?\d*|\.\d+)(e[+-]?\d+)?/i.exec(s.slice(i)))){i+=m[0].length;return parseFloat(m[0])}
  if((m=/^[a-z]+/.exec(s.slice(i)))){var w=m[0];i+=w.length;
   if(w==='pi')return Math.PI;if(w==='e')return Math.E;
   if(F[w]&&s[i]==='('){i++;var a=expr();if(s[i]!==')')fail();i++;return F[w](a)}}
  fail()}
 var r=expr();if(i<s.length)fail();return r}
C.m_sci=function(v){var ex=(v.ex||'').trim();if(!ex)return bad('Type an expression.');
 var r;try{r=parse(ex,v.ang==='deg')}catch(e){return bad('Check the expression. Use numbers, + - * / ^ ( ) and functions such as sin(30).')}
 if(!isFinite(r))return bad('The result is undefined or too large.');
 return {stats:[S(esc(ex),N(Math.round(r*1e10)/1e10,10),1)],note:'Angles are in '+(v.ang==='deg'?'degrees':'radians')+'. Functions: sin cos tan asin acos atan sqrt cbrt log (base 10) ln exp abs fact. Constants: pi, e. Postfix ! is factorial and % divides by 100.'}};
C.m_sci.init=function(box,run){var pad=box.querySelector('#pad'),inp=box.querySelector('#ex');if(!pad)return;
 var keys=['7','8','9','/','(',')','4','5','6','*','^','!','1','2','3','-','sqrt(','pi','0','.','%','+','sin(','cos(','tan(','log(','ln(','e','DEL','CLR'];
 keys.forEach(function(k){var b=document.createElement('button');b.type='button';b.className='btn sm pk';b.textContent=k==='*'?'×':k==='/'?'÷':k;
  b.addEventListener('click',function(){
   if(k==='CLR'){inp.value=''}else if(k==='DEL'){inp.value=inp.value.slice(0,-1)}
   else{var a=inp.selectionStart==null?inp.value.length:inp.selectionStart,z=inp.selectionEnd==null?a:inp.selectionEnd;inp.value=inp.value.slice(0,a)+k+inp.value.slice(z);
    try{inp.focus();inp.setSelectionRange(a+k.length,a+k.length)}catch(e){}}
   run()});pad.appendChild(b)})};

/* ---- Fraction ---- */
function fr(n,d){if(d<0){n=-n;d=-d}var g=gcd(n,d)||1;return [n/g,d/g]}
function fstr(f){return f[1]===1?String(f[0]):f[0]+'/'+f[1]}
function mixed(f){var n=f[0],d=f[1];if(d===1||Math.abs(n)<d)return fstr(f);var w=Math.trunc(n/d),r=Math.abs(n)%d;return w+(r?' '+r+'/'+d:'')}
C.m_frac=function(v){var a=Math.round(v.n1),b=Math.round(v.d1),c=Math.round(v.n2),d=Math.round(v.d2);
 if(!b||!d)return bad('A denominator cannot be zero.');
 var r;if(v.op==='+')r=[a*d+c*b,b*d];else if(v.op==='-')r=[a*d-c*b,b*d];else if(v.op==='*')r=[a*c,b*d];else{if(!c)return bad('Cannot divide by a fraction equal to zero.');r=[a*d,b*c]}
 if(!r[1])return bad();var f=fr(r[0],r[1]);
 return {stats:[S('Result',fstr(f),1),S('Mixed number',mixed(f)),S('Decimal',N(f[0]/f[1],6)),S('Percentage',N(f[0]/f[1]*100,4)+' %')],note:'Unsimplified: '+r[0]+'/'+r[1]+'.'}};

/* ---- Square root ---- */
C.m_sqrt=function(v){var x=v.x,k=v.k,n=k==='sqrt'?2:k==='cbrt'?3:Math.round(v.n),r;
 if(n<2)return bad('The root index must be 2 or more.');
 if(x<0&&n%2===0)return bad('An even root of a negative number is not a real number.');
 r=x<0?-Math.pow(-x,1/n):Math.pow(x,1/n);if(!isFinite(r))return bad();
 var rr=Math.round(r),perfect=Math.abs(Math.pow(rr,n)-x)<1e-9*Math.max(1,Math.abs(x)),st=[S('Result',N(r,8),1),S('Perfect power?',perfect?'Yes ('+rr+'^'+n+' = '+N(x,4)+')':'No')];
 if(n===2&&x>=0){var lo=Math.floor(r);st.push(S('Nearest perfect squares',lo*lo+' and '+(lo+1)*(lo+1)),S('Result squared',N(r*r,4)))}
 return {stats:st}};

/* ---- Ratio ---- */
C.m_ratio=function(v){
 if(v.m==='s'){var a=v.s_a,b=v.s_b;if(!(a>0&&b>0))return bad('Enter positive values.');
  var k=1;while((a*k!==Math.round(a*k)||b*k!==Math.round(b*k))&&k<1e6)k*=10;var A=Math.round(a*k),B=Math.round(b*k),g=gcd(A,B);
  return {stats:[S('Simplified ratio',A/g+' : '+B/g,1),S('A as a fraction of the total',N(a/(a+b)*100,2)+' %'),S('B as a fraction of the total',N(b/(a+b)*100,2)+' %'),S('Decimal (A / B)',N(a/b,4))]}}
 if(!v.p_a)return bad('The first value cannot be zero.');var x=v.p_b*v.p_c/v.p_a;
 return {stats:[S('Missing value x',N(x,4),1),S('Proportion',N(v.p_a,4)+' : '+N(v.p_b,4)+' = '+N(v.p_c,4)+' : '+N(x,4))],note:'Formula: x = B x C / A.'}};

/* ---- Probability ---- */
C.m_prob=function(v){
 if(v.m==='s'){if(!(v.s_t>0)||v.s_f<0||v.s_f>v.s_t)return bad('Favourable outcomes must be between 0 and the total outcomes.');
  var p=v.s_f/v.s_t;return {stats:[S('Probability',N(p,6),1),S('As a percentage',N(p*100,3)+' %'),S('As a fraction',fstr(fr(Math.round(v.s_f),Math.round(v.s_t)))),S('Probability of not happening',N(1-p,6)),S('Odds in favour',N(v.s_f,0)+' to '+N(v.s_t-v.s_f,0))]}}
 if(v.c_a<0||v.c_a>100||v.c_b<0||v.c_b>100)return bad('Probabilities must be between 0 and 100 %.');
 var a=v.c_a/100,b=v.c_b/100;
 return {stats:[S('A and B both happen',N(a*b*100,4)+' %',1),S('A or B (at least one)',N((a+b-a*b)*100,4)+' %'),S('Neither happens',N((1-a)*(1-b)*100,4)+' %'),S('Exactly one happens',N((a*(1-b)+b*(1-a))*100,4)+' %')],note:'Assumes the two events are independent.'}};
})();
