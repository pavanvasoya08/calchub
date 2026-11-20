
(function(){
"use strict";
var B=document.body,CUR=B.dataset.cur||'₹',LOC=B.dataset.loc||'en-IN';
var byId=function(i){return document.getElementById(i)};
function M(n,d){d=d||0;return isFinite(n)?CUR+n.toLocaleString(LOC,{minimumFractionDigits:d,maximumFractionDigits:d}):'—'}
function N(n,d){d=d==null?2:d;return isFinite(n)?n.toLocaleString(LOC,{maximumFractionDigits:d}):'—'}
function S(l,v,h){return [l,v,!!h]}
function bad(m){return {err:m||'Please enter valid values.'}}
function emiOf(P,i,m){return i===0?P/m:P*i*Math.pow(1+i,m)/(Math.pow(1+i,m)-1)}
function pd(s){return new Date(s+'T00:00:00')}
function fdate(d){return d.toLocaleDateString('en-GB',{day:'numeric',month:'long',year:'numeric'})}
function addDays(d,n){var x=new Date(d.getTime());x.setDate(x.getDate()+n);return x}
function nums(s){var a=(s||'').split(/[\s,;]+/).filter(Boolean).map(Number);return a.some(isNaN)?null:a}
function ymd(a,b){var y=b.getFullYear()-a.getFullYear(),m=b.getMonth()-a.getMonth(),d=b.getDate()-a.getDate();
 if(d<0){m--;d+=new Date(b.getFullYear(),b.getMonth(),0).getDate()}if(m<0){y--;m+=12}return [y,m,d]}

var C={};
/* ---------------- Loans & investments ---------------- */
C.emi=function(v){var P=v.p,m=Math.round(v.y*12);if(P<=0||m<1||v.r<0)return bad();
 var i=v.r/1200,e=emiOf(P,i,m),tot=e*m,it=tot-P,bal=P,rows=[];
 for(var y=1;y<=Math.ceil(m/12);y++){var pa=0,ia=0;for(var k=0;k<12&&(y-1)*12+k<m;k++){var x=bal*i,p=e-x;ia+=x;pa+=p;bal-=p}rows.push([y,M(pa),M(ia),M(Math.max(bal,0))])}
 return{stats:[S('Monthly EMI',M(e),1),S('Total interest',M(it)),S('Total payment',M(tot))],bar:[P,it,'Principal','Interest'],table:{head:['Year','Principal paid','Interest paid','Balance'],rows:rows}}};
C.elig=function(v){var m=Math.round(v.y*12),i=v.r/1200,mx=v.inc*v.foir/100-v.ex;if(v.inc<=0||m<1||v.r<0||v.foir<=0)return bad();
 if(mx<=0)return bad('Your existing EMIs already use up the share of income that lenders usually allow for repayments.');
 var L=mx/emiOf(1,i,m);return{stats:[S('Estimated eligible loan',M(L),1),S('Maximum affordable EMI',M(mx)),S('Total interest on this loan',M(mx*m-L))],note:'This is an estimate. Lenders also look at your credit score, age, job stability and property value.'}};
C.sip=function(v){var P=v.p,m=Math.round(v.y*12);if(P<=0||m<1||v.r<0)return bad();
 var i=v.r/1200,fv=i===0?P*m:P*((Math.pow(1+i,m)-1)/i)*(1+i),inv=P*m;
 return{stats:[S('Expected value',M(fv),1),S('Amount invested',M(inv)),S('Estimated returns',M(fv-inv))],bar:[inv,fv-inv,'Invested','Returns'],note:'Market returns are not guaranteed. This is only an estimate.'}};
C.lump=function(v){if(v.p<=0||v.y<=0||v.r<0)return bad();var fv=v.p*Math.pow(1+v.r/100,v.y);
 return{stats:[S('Future value',M(fv),1),S('Amount invested',M(v.p)),S('Estimated returns',M(fv-v.p))],bar:[v.p,fv-v.p,'Invested','Returns']}};
C.fd=function(v){var n=+v.n;if(v.p<=0||v.y<=0||v.r<0)return bad();var A=v.p*Math.pow(1+v.r/(100*n),n*v.y);
 return{stats:[S('Maturity amount',M(A),1),S('Amount invested',M(v.p)),S('Total interest',M(A-v.p))],bar:[v.p,A-v.p,'Principal','Interest']}};
C.rd=function(v){if(v.p<=0||v.y<=0||v.r<0)return bad();var i=v.r/400,n=v.y*4,mat=i===0?v.p*12*v.y:v.p*(Math.pow(1+i,n)-1)/(1-Math.pow(1+i,-1/3)),dep=v.p*12*v.y;
 return{stats:[S('Maturity amount',M(mat),1),S('Total deposited',M(dep)),S('Interest earned',M(mat-dep))],bar:[dep,mat-dep,'Deposited','Interest']}};
C.ppf=function(v){if(v.p<=0||v.y<1||v.r<0)return bad();var i=v.r/100,bal=0,rows=[],dep=0,yrs=Math.round(v.y);
 for(var y=1;y<=yrs;y++){var open=bal+v.p,it=open*i;bal=open+it;dep+=v.p;rows.push([y,M(v.p),M(it),M(bal)])}
 return{stats:[S('Maturity value',M(bal),1),S('Total deposited',M(dep)),S('Total interest',M(bal-dep))],bar:[dep,bal-dep,'Deposited','Interest'],table:{head:['Year','Deposit','Interest','Closing balance'],rows:rows},
 note:v.p>150000?'The yearly deposit limit for PPF is currently ₹1,50,000. Check the latest rules.':'Assumes the deposit is made before the 5th of April each year, with interest compounded annually.'}};
C.ci=function(v){var n=+v.n;if(v.p<=0||v.y<=0||v.r<0)return bad();var A=v.p*Math.pow(1+v.r/(100*n),n*v.y);
 return{stats:[S('Final amount',M(A,2),1),S('Principal',M(v.p,2)),S('Compound interest',M(A-v.p,2))],bar:[v.p,A-v.p,'Principal','Interest']}};
C.si=function(v){if(v.p<=0||v.y<=0||v.r<0)return bad();var I=v.p*v.r*v.y/100;
 return{stats:[S('Simple interest',M(I,2),1),S('Principal',M(v.p,2)),S('Total amount',M(v.p+I,2))],bar:[v.p,I,'Principal','Interest']}};
C.cagr=function(v){if(v.a<=0||v.b<=0||v.y<=0)return bad('Enter values greater than zero.');var g=Math.pow(v.b/v.a,1/v.y)-1;
 return{stats:[S('CAGR',N(g*100,2)+'%',1),S('Absolute return',N((v.b/v.a-1)*100,2)+'%'),S('Total gain / loss',M(v.b-v.a))]}};
C.swp=function(v){var B0=v.p,W=v.w,m=Math.round(v.y*12),i=v.r/1200;if(B0<=0||W<=0||m<1||v.r<0)return bad();
 var bal=B0,tw=0,rows=[],dep=false,last=m,yw=0,ys=B0;
 for(var k=1;k<=m;k++){var w=Math.min(W,bal);bal=(bal-w)*(1+i);tw+=w;yw+=w;if(bal<=0.005){dep=true;last=k;bal=0}
  if(k%12===0||k===m||dep){rows.push([Math.ceil(k/12),M(ys),M(yw),M(bal)]);ys=bal;yw=0;if(dep)break}}
 var ly=Math.floor(last/12),lm=last%12,lasts=dep?((ly?ly+(ly>1?' years':' year'):'')+(ly&&lm?' ':'')+(lm?lm+(lm>1?' months':' month'):'')):'Entire period';
 return{stats:[S('Final balance',M(bal),1),S('Total withdrawn',M(tw)),S('Money lasts',lasts)],table:{head:['Year','Opening balance','Withdrawn','Closing balance'],rows:rows},
 note:dep?'Your money runs out before the period ends. Try a smaller withdrawal.':''}};
C.infl=function(v){if(v.a<=0||v.y<=0||v.r<0)return bad();var f=Math.pow(1+v.r/100,v.y);
 return{stats:[S('Future cost of the same item',M(v.a*f),1),S('Value of today\'s amount in the future',M(v.a/f)),S('Total price rise',N((f-1)*100,1)+'%')],
 note:'Shows what '+M(v.a)+' will cost in '+v.y+' years, and how much it will be able to buy.'}};
C.save=function(v){var m=Math.round(v.y*12),i=v.r/1200;if(v.g<=0||m<1||v.r<0||v.c<0)return bad();
 var need=v.g-v.c*Math.pow(1+i,m);if(need<=0)return{stats:[S('Monthly saving needed',M(0),1)],note:'Your current savings alone will reach the goal.'};
 var P=i===0?need/m:need*i/((Math.pow(1+i,m)-1)*(1+i));
 return{stats:[S('Monthly saving needed',M(P),1),S('Total you will deposit',M(P*m)),S('Growth from interest',M(v.g-v.c-P*m))]}};
C.roi=function(v){if(v.a<=0||v.b<0)return bad();var r=(v.b-v.a)/v.a*100,st=[S('ROI',N(r,2)+'%',1),S('Net profit / loss',M(v.b-v.a))];
 if(v.y>0&&v.b>0)st.push(S('Annualized return',N((Math.pow(v.b/v.a,1/v.y)-1)*100,2)+'%'));return{stats:st}};

/* ---------------- Tax, salary & business ---------------- */
C.gst=function(v){var rt=v.rate==='c'?v.cr:+v.rate;if(v.a<=0||rt<0)return bad('Enter an amount greater than zero.');
 var base,g,tot;if(v.mode==='add'){base=v.a;g=v.a*rt/100;tot=v.a+g}else{tot=v.a;base=v.a*100/(100+rt);g=tot-base}
 return{stats:[S('Net amount (without tax)',M(base,2)),S('Tax amount',M(g,2),1),S('Gross amount (with tax)',M(tot,2)),S('CGST ('+N(rt/2,2)+'%)',M(g/2,2)),S('SGST ('+N(rt/2,2)+'%)',M(g/2,2))]}};
C.hra=function(v){var b=v.b+v.da;if(b<=0||v.hra<0||v.rent<0)return bad();var pct=+v.city,A=v.hra,Bv=Math.max(0,v.rent-0.1*b),Cv=pct/100*b,ex=Math.max(0,Math.min(A,Bv,Cv));
 return{stats:[S('Monthly HRA exemption',M(ex),1),S('Taxable HRA (monthly)',M(A-ex)),S('Annual exemption',M(ex*12))],
 table:{head:['Rule','Monthly amount'],rows:[['Actual HRA received',M(A)],['Rent paid minus 10% of salary',M(Bv)],[pct+'% of salary',M(Cv)]]},note:'The exemption is the lowest of the three amounts. It applies only under the old tax regime.'}};
C.grat=function(v){if(v.sal<=0||v.yr<0||v.mo<0)return bad();var yrs=Math.floor(v.yr)+(v.mo>=6?1:0),g=v.sal*15/26*yrs;
 return{stats:[S('Gratuity amount',M(g),1),S('Years counted',yrs+' years'),S('Last drawn salary (Basic + DA)',M(v.sal))],note:(v.yr<5?'Gratuity is generally payable only after 5 years of continuous service. ':'')+'A tax-free limit applies to the gratuity amount. Check the current limit.'}};
C.hour=function(v){if(v.rate<=0||v.hrs<=0||v.wks<=0)return bad();var a=v.rate*v.hrs*v.wks;
 return{stats:[S('Annual salary',M(a,0),1),S('Monthly salary',M(a/12,0)),S('Weekly salary',M(v.rate*v.hrs,0)),S('Daily (5-day week)',M(v.rate*v.hrs/5,0))]}};
C.disc=function(v){if(v.a<=0||v.d1<0||v.d2<0||v.d1>100||v.d2>100)return bad();var f=v.a*(1-v.d1/100)*(1-v.d2/100);
 return{stats:[S('Final price',M(f,2),1),S('You save',M(v.a-f,2)),S('Effective discount',N((1-f/v.a)*100,2)+'%')]}};
C.tip=function(v){if(v.a<=0||v.t<0||v.n<1)return bad();var t=v.a*v.t/100,tot=v.a+t;
 return{stats:[S('Tip amount',M(t,2)),S('Total bill',M(tot,2),1),S('Each person pays',M(tot/Math.round(v.n),2))]}};
C.marg=function(v){if(v.sp<=0||v.cost<0)return bad();var p=v.sp-v.cost;
 return{stats:[S('Profit',M(p,2),1),S('Profit margin',N(p/v.sp*100,2)+'%'),S('Markup',v.cost>0?N(p/v.cost*100,2)+'%':'—')]}};
C.be=function(v){var cm=v.price-v.vc;if(v.fc<0||v.price<=0||v.vc<0)return bad();if(cm<=0)return bad('The selling price must be higher than the variable cost per unit.');
 var u=v.fc/cm;return{stats:[S('Break-even units',N(Math.ceil(u),0),1),S('Break-even revenue',M(Math.ceil(u)*v.price)),S('Contribution margin per unit',M(cm,2)),S('Contribution margin ratio',N(cm/v.price*100,1)+'%')]}};
C.comm=function(v){if(v.a<=0||v.r<0)return bad();var c=v.a*v.r/100;return{stats:[S('Commission',M(c,2),1),S('Sale amount after commission',M(v.a-c,2))]}};

/* ---------------- Health ---------------- */
C.bmi=function(v){var kg,m;if(v.u==='m'){kg=v.kg;m=v.cm/100}else{kg=v.lb*0.45359237;m=(v.ft*12+v.inch)*0.0254}
 if(kg<=0||m<=0)return bad('Enter your weight and height.');var b=kg/(m*m),c=b<18.5?'Underweight':b<25?'Normal weight':b<30?'Overweight':'Obese',lo=18.5*m*m,hi=24.9*m*m,u=v.u==='m';
 return{stats:[S('Your BMI',N(b,1),1),S('Category',c),S('Healthy weight range',u?N(lo,1)+' – '+N(hi,1)+' kg':N(lo/0.45359237,0)+' – '+N(hi/0.45359237,0)+' lb')],
 note:'BMI is a screening tool and does not measure body fat. Some health bodies use lower cut-offs for South Asian populations. Talk to a doctor for personal advice.'}};
C.bmr=function(v){if(v.age<=0||v.kg<=0||v.cm<=0)return bad();var b=10*v.kg+6.25*v.cm-5*v.age+(v.sex==='m'?5:-161);
 return{stats:[S('BMR (calories at rest)',N(b,0)+' kcal/day',1),S('Daily calories to maintain weight',N(b*(+v.act),0)+' kcal/day')],note:'Uses the Mifflin-St Jeor equation. Results are estimates, not medical advice.'}};
C.ideal=function(v){if(v.cm<=0)return bad();var inch=Math.max(0,v.cm/2.54-60),m=v.sex==='m',
 dev=(m?50:45.5)+2.3*inch,rob=(m?52:49)+(m?1.9:1.7)*inch,mil=(m?56.2:53.1)+(m?1.41:1.36)*inch,mm=v.cm/100;
 return{stats:[S('Devine formula',N(dev,1)+' kg',1),S('Robinson formula',N(rob,1)+' kg'),S('Miller formula',N(mil,1)+' kg'),S('Healthy BMI range (18.5–24.9)',N(18.5*mm*mm,1)+' – '+N(24.9*mm*mm,1)+' kg')],
 note:'Ideal weight formulas are rough guides. A healthy weight depends on age, muscle mass and overall health.'}};
C.bf=function(v){if(v.cm<=0||v.neck<=0||v.waist<=0)return bad();var f=v.sex==='f',bf;
 if(f){if(v.hip<=0||v.waist+v.hip<=v.neck)return bad('Check your measurements.');bf=495/(1.29579-0.35004*Math.log10(v.waist+v.hip-v.neck)+0.221*Math.log10(v.cm))-450}
 else{if(v.waist<=v.neck)return bad('Waist must be larger than neck.');bf=495/(1.0324-0.19077*Math.log10(v.waist-v.neck)+0.15456*Math.log10(v.cm))-450}
 var cat=f?(bf<14?'Essential fat':bf<21?'Athletic':bf<25?'Fitness':bf<32?'Average':'Above average'):(bf<6?'Essential fat':bf<14?'Athletic':bf<18?'Fitness':bf<25?'Average':'Above average');
 return{stats:[S('Body fat',N(bf,1)+'%',1),S('Category',cat)],note:'Uses the U.S. Navy method with measurements in cm. It is an estimate.'}};
C.preg=function(v){if(!v.lmp)return bad('Choose the first day of your last period.');var lmp=pd(v.lmp),cyc=v.cyc||28,edd=addDays(lmp,280+(cyc-28)),t=new Date();t=new Date(t.getFullYear(),t.getMonth(),t.getDate());
 var d=Math.floor((t-lmp)/864e5),st=[S('Estimated due date',fdate(edd),1)];
 if(d>=0&&d<=300)st.push(S('Pregnancy progress today',Math.floor(d/7)+' weeks '+(d%7)+' days'));
 st.push(S('Second trimester starts',fdate(addDays(lmp,98))),S('Third trimester starts',fdate(addDays(lmp,196))));
 return{stats:st,note:'Only about 5% of babies arrive on the due date. This is an estimate. Please consult your doctor.'}};

/* ---------------- Math & everyday ---------------- */
C.pct=function(v){var x=v.x,y=v.y;
 if(v.mode==='a')return{stats:[S(N(x,2)+'% of '+N(y,2)+' is',N(x*y/100,4),1)]};
 if(v.mode==='b'){if(y===0)return bad('The second value cannot be zero.');return{stats:[S(N(x,2)+' is what percent of '+N(y,2),N(x/y*100,4)+'%',1)]}}
 if(v.mode==='c'){if(x===0)return bad('The first value cannot be zero.');var c=(y-x)/Math.abs(x)*100;return{stats:[S('Percentage '+(c>=0?'increase':'decrease'),N(Math.abs(c),4)+'%',1),S('Difference',N(y-x,4))]}}
 return{stats:[S('After increasing '+N(y,2)+' by '+N(x,2)+'%',N(y*(1+x/100),4),1),S('After decreasing '+N(y,2)+' by '+N(x,2)+'%',N(y*(1-x/100),4))]}};
C.avg=function(v){var a=nums(v.nums);if(!a||!a.length)return bad('Enter numbers separated by commas, spaces or new lines.');
 var n=a.length,s=a.reduce(function(p,c){return p+c},0),so=a.slice().sort(function(p,c){return p-c}),med=n%2?so[(n-1)/2]:(so[n/2-1]+so[n/2])/2,cnt={},mx=0;
 a.forEach(function(x){cnt[x]=(cnt[x]||0)+1;if(cnt[x]>mx)mx=cnt[x]});var modes=Object.keys(cnt).filter(function(k){return cnt[k]===mx});
 return{stats:[S('Mean (average)',N(s/n,4),1),S('Median',N(med,4)),S('Mode',mx>1?modes.join(', '):'No repeating value'),S('Count',n),S('Sum',N(s,4)),S('Minimum',N(so[0],4)),S('Maximum',N(so[n-1],4)),S('Range',N(so[n-1]-so[0],4))]}};
C.sd=function(v){var a=nums(v.nums);if(!a||a.length<2)return bad('Enter at least two numbers separated by commas, spaces or new lines.');
 var n=a.length,m=a.reduce(function(p,c){return p+c},0)/n,ss=a.reduce(function(p,c){return p+(c-m)*(c-m)},0);
 return{stats:[S('Sample standard deviation',N(Math.sqrt(ss/(n-1)),4),1),S('Population standard deviation',N(Math.sqrt(ss/n),4)),S('Sample variance',N(ss/(n-1),4)),S('Population variance',N(ss/n,4)),S('Mean',N(m,4)),S('Count',n)]}};
C.age=function(v){if(!v.dob||!v.to)return bad('Choose your date of birth.');var a=pd(v.dob),b=pd(v.to);if(a>b)return bad('Date of birth must be before the second date.');
 var r=ymd(a,b),days=Math.floor((b-a)/864e5),nb=new Date(b.getFullYear(),a.getMonth(),a.getDate());if(nb<=b)nb=new Date(b.getFullYear()+1,a.getMonth(),a.getDate());
 return{stats:[S('Your age',r[0]+' years, '+r[1]+' months, '+r[2]+' days',1),S('Total months',N(r[0]*12+r[1],0)),S('Total weeks',N(days/7,0)),S('Total days',N(days,0)),S('Next birthday in',Math.ceil((nb-b)/864e5)+' days'),S('Born on a',['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'][a.getDay()])]}};
C.dd=function(v){if(!v.s||!v.e)return bad('Choose both dates.');var a=pd(v.s),b=pd(v.e);if(a>b){var t=a;a=b;b=t}
 var days=Math.round((b-a)/864e5),r=ymd(a,b),bd=0,c=new Date(a.getTime());for(var i=0;i<days;i++){var w=c.getDay();if(w!==0&&w!==6)bd++;c.setDate(c.getDate()+1)}
 return{stats:[S('Difference',N(days,0)+' days',1),S('In years, months, days',r[0]+' y, '+r[1]+' m, '+r[2]+' d'),S('In weeks',Math.floor(days/7)+' weeks '+(days%7)+' days'),S('Working days (Mon–Fri)',N(bd,0))]}};
C.cgpa=function(v){if(v.val<=0)return bad();var m=+v.mult;if(v.mode==='a')return{stats:[S('Percentage',N(v.val*m,2)+'%',1)],note:'Uses the multiplier '+m+'. Check which formula your board or university accepts.'};
 return{stats:[S('CGPA',N(v.val/m,2),1)],note:'Uses the multiplier '+m+'. Check which formula your board or university accepts.'}};
C.pyth=function(v){var a=v.a,b,c;if(v.mode==='h'){b=v.b;if(a<=0||b<=0)return bad();c=Math.sqrt(a*a+b*b)}else{c=v.c;if(a<=0||c<=a)return bad('The hypotenuse must be longer than the other side.');b=Math.sqrt(c*c-a*a)}
 var d=function(x){return N(x*180/Math.PI,2)+'°'};
 return{stats:[S(v.mode==='h'?'Hypotenuse (c)':'Missing side (b)',N(v.mode==='h'?c:b,4),1),S('Area',N(a*b/2,4)),S('Perimeter',N(a+b+c,4)),S('Angle opposite side a',d(Math.atan(a/b))),S('Angle opposite side b',d(Math.atan(b/a)))]}};
C.area=function(v){var s=v.shape,A,P=null;
 if(s==='rect'){if(v.l<=0||v.w<=0)return bad();A=v.l*v.w;P=2*(v.l+v.w)}
 else if(s==='sq'){if(v.s<=0)return bad();A=v.s*v.s;P=4*v.s}
 else if(s==='circ'){if(v.r<=0)return bad();A=Math.PI*v.r*v.r;P=2*Math.PI*v.r}
 else if(s==='tri'){if(v.tb<=0||v.th<=0)return bad();A=v.tb*v.th/2}
 else if(s==='para'){if(v.tb<=0||v.th<=0)return bad();A=v.tb*v.th}
 else{if(v.pa<=0||v.pb<=0||v.ph<=0)return bad();A=(v.pa+v.pb)/2*v.ph}
 var st=[S('Area',N(A,4)+' (square units)',1)];if(P!==null)st.push(S(s==='circ'?'Circumference':'Perimeter',N(P,4)+' (units)'));return{stats:st,note:'Use the same unit for every measurement.'}};
C.sdt=function(v){var m=v.mode;if(m==='s'){if(v.dist<=0||v.time<=0)return bad();return{stats:[S('Speed',N(v.dist/v.time,3)+' per hour',1)]}}
 if(m==='d'){if(v.spd<=0||v.time<=0)return bad();return{stats:[S('Distance',N(v.spd*v.time,3),1)]}}
 if(v.dist<=0||v.spd<=0)return bad();var t=v.dist/v.spd,h=Math.floor(t),mi=Math.round((t-h)*60);if(mi===60){h++;mi=0}
 return{stats:[S('Time',N(t,3)+' hours',1),S('In hours and minutes',h+' h '+mi+' min')]}};
C.fuel=function(v){if(v.dist<=0||v.mil<=0||v.price<=0)return bad();var l=v.dist/v.mil,c=l*v.price;
 return{stats:[S('Fuel cost',M(c,2),1),S('Fuel needed',N(l,2)+' litres'),S('Cost per km',M(c/v.dist,2))]}};
C.elec=function(v){if(v.w<=0||v.h<=0||v.days<=0||v.rate<0)return bad();var k=v.w*v.h*v.days/1000;
 return{stats:[S('Electricity cost',M(k*v.rate,2),1),S('Energy used',N(k,2)+' kWh'),S('Cost per day',M(k*v.rate/v.days,2))]}};

/* ---------------- Unit converters ---------------- */
function unitCalc(v){var U=window.UNITS||[],f=null,t=null;U.forEach(function(u){if(u[0]===v.from)f=u;if(u[0]===v.to)t=u});if(!f||!t)return bad();
 var base=v.val*f[2],out=base/t[2],rows=U.map(function(u){return [u[1],N(base/u[2],8)]});
 return{stats:[S(N(v.val,6)+' '+f[1]+' =',N(out,8)+' '+t[1],1)],table:{head:['Unit','Value'],rows:rows}}}
C.conv=unitCalc;
C.temp=function(v){var x=v.val,k;if(v.from==='c')k=x+273.15;else if(v.from==='f')k=(x-32)*5/9+273.15;else k=x;
 if(k<0)return bad('That is below absolute zero.');var c=k-273.15,out={c:c,f:c*9/5+32,k:k},nm={c:'°C',f:'°F',k:' K'};
 return{stats:[S(N(x,4)+nm[v.from]+' =',N(out[v.to],4)+nm[v.to],1)],table:{head:['Scale','Value'],rows:[['Celsius',N(c,4)+' °C'],['Fahrenheit',N(out.f,4)+' °F'],['Kelvin',N(k,4)+' K']]}}};

/* ---------------- Engine ---------------- */
var calcName=B.dataset.calc;
if(calcName&&C[calcName]){
 var box=byId('calc'),out=byId('out');
 var fields=box.querySelectorAll('input,select,textarea');
 var today=new Date().toISOString().slice(0,10);
 box.querySelectorAll('[data-today]').forEach(function(e){e.value=today});
 function read(){var v={};fields.forEach(function(e){if(!e.id)return;v[e.id]=e.type==='number'?(parseFloat(e.value)||0):e.value});return v}
 function toggle(v){box.querySelectorAll('[data-when]').forEach(function(w){var p=w.dataset.when.split('='),ok=p[1].split('|').indexOf(String(v[p[0]]))>-1;w.classList.toggle('hidden',!ok)})}
 function render(r){
  if(r.err){out.innerHTML='<div class="note">'+r.err+'</div>';return}
  var h='<div class="stats">'+r.stats.map(function(s){return '<div class="stat'+(s[2]?' hi':'')+'"><small>'+s[0]+'</small><b>'+s[1]+'</b></div>'}).join('')+'</div>';
  if(r.bar){var a=r.bar[0],b=r.bar[1],p=a+b>0?Math.max(0,Math.min(100,a/(a+b)*100)):0;
   h+='<div class="bar"><i style="width:'+p.toFixed(1)+'%"></i></div><div class="legend"><span><s style="background:#8bb494"></s>'+r.bar[2]+' '+p.toFixed(0)+'%</span><span><s style="background:#ffe066"></s>'+r.bar[3]+' '+(100-p).toFixed(0)+'%</span></div>'}
  if(r.table){h+='<div class="tblwrap"><table><tr>'+r.table.head.map(function(x){return '<th>'+x+'</th>'}).join('')+'</tr>'+r.table.rows.map(function(row){return '<tr>'+row.map(function(c){return '<td>'+c+'</td>'}).join('')+'</tr>'}).join('')+'</table></div>'}
  if(r.note)h+='<p class="note">'+r.note+'</p>';
  out.innerHTML=h}
 function run(){var v=read();toggle(v);try{render(C[calcName](v))}catch(e){render(bad())}}
 fields.forEach(function(e){e.addEventListener('input',run);e.addEventListener('change',run)});
 run()}

var q=byId('q');
if(q)q.addEventListener('input',function(){var s=q.value.toLowerCase().trim();
 document.querySelectorAll('.tcard').forEach(function(c){c.classList.toggle('hidden',!!s&&c.textContent.toLowerCase().indexOf(s)<0)});
 document.querySelectorAll('.catsec').forEach(function(sec){sec.classList.toggle('hidden',!sec.querySelector('.tcard:not(.hidden)'))})});
var qp=byId('qp');
if(qp){var qf=function(){var P=parseFloat(byId('qp').value)||0,r=parseFloat(byId('qr').value)||0,m=Math.round((parseFloat(byId('qy').value)||0)*12),o=byId('qout');
 if(P<=0||m<1||r<0){o.innerHTML='<div class="note">Enter valid values.</div>';return}
 var e=emiOf(P,r/1200,m);o.innerHTML='<div class="stats">'+[['Monthly EMI',M(e),1],['Total interest',M(e*m-P)],['Total payment',M(e*m)]].map(function(s){return '<div class="stat'+(s[2]?' hi':'')+'"><small>'+s[0]+'</small><b>'+s[1]+'</b></div>'}).join('')+'</div>'};
 ['qp','qr','qy'].forEach(function(i){byId(i).addEventListener('input',qf)});qf()}
var cr=byId('catRow');
if(cr){byId('catPrev').addEventListener('click',function(){cr.scrollBy({left:-420,behavior:'smooth'})});byId('catNext').addEventListener('click',function(){cr.scrollBy({left:420,behavior:'smooth'})})}
})();

