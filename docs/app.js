(function(){
"use strict";
var B=document.body,CUR=B.dataset.cur||'₹',LOC=B.dataset.loc||'en-IN';
var byId=function(i){return document.getElementById(i)};

/* ============ helpers available to every calculator function (C.<name>) ============
 M(n,d)    money   "₹1,23,456"        N(n,d) plain number "1,234.56" (d = max decimals, default 2)
 S(label,value,highlight)  one result tile      bad(msg)  validation error {err}
 emiOf(P,i,m)  EMI for principal P, monthly rate i (decimal), m months
 pd('YYYY-MM-DD') -> local Date     fdate(Date) -> "20 November 2026"     addDays(Date,n)
 ymd(a,b) -> [years,months,days] between two Dates      nums(text) -> array of numbers or null
 pad(n) -> two digits      esc(s) -> html-escaped text
 A calculator function receives v (values by field id: number inputs -> numbers (empty = 0),
 checkbox -> true/false, everything else -> string) and returns ONE of:
   {err:'message'}  or  {stats:[S(..),..], bar:[a,b,'labelA','labelB'], table:{head:[..],rows:[[..]]},
                         note:'text', blocks:[['Label','text to show in a copyable box'],..]}
 Optional properties on the function: C.x.tick=true (re-run every second), C.x.init=function(box,run){...}
*/
function M(n,d){d=d||0;return isFinite(n)?CUR+n.toLocaleString(LOC,{minimumFractionDigits:d,maximumFractionDigits:d}):'—'}
function N(n,d){d=d==null?2:d;return isFinite(n)?n.toLocaleString(LOC,{maximumFractionDigits:d}):'—'}
function S(l,v,h){return [l,v,!!h]}
function bad(m){return {err:m||'Please enter valid values.'}}
function emiOf(P,i,m){return i===0?P/m:P*i*Math.pow(1+i,m)/(Math.pow(1+i,m)-1)}
function pd(s){return new Date(s+'T00:00:00')}
function pad(n){return (n<10?'0':'')+n}
function esc(s){return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;')}
function fdate(d){return d.toLocaleDateString('en-GB',{day:'numeric',month:'long',year:'numeric'})}
function addDays(d,n){var x=new Date(d.getTime());x.setDate(x.getDate()+n);return x}
function nums(s){var a=(s||'').split(/[\s,;]+/).filter(Boolean).map(Number);return a.some(isNaN)?null:a}
function ymd(a,b){var y=b.getFullYear()-a.getFullYear(),m=b.getMonth()-a.getMonth(),d=b.getDate()-a.getDate();
 if(d<0){m--;d+=new Date(b.getFullYear(),b.getMonth(),0).getDate()}if(m<0){y--;m+=12}return [y,m,d]}

var C={};

/* ---- finance ---- */
C.loan=function(v){var P=v.p,m=Math.round(v.y*12);if(P<=0||m<1||v.r<0||m>600)return bad('Enter a loan amount, a rate and a tenure up to 50 years.');
 var i=v.r/1200,e=emiOf(P,i,m),tot=e*m,bal=P,rows=[],yi=0,yp=0;
 for(var k=1;k<=m;k++){var it=bal*i,pr=e-it;bal=Math.max(0,bal-pr);yi+=it;yp+=pr;
  if(k%12===0||k===m){rows.push([Math.ceil(k/12),M(yp),M(yi),M(bal)]);yi=0;yp=0}}
 return{stats:[S('Monthly EMI',M(e),1),S('Total interest',M(tot-P)),S('Total payment',M(tot))],bar:[P,tot-P,'Principal','Interest'],
 table:{head:['Year','Principal paid','Interest paid','Balance'],rows:rows}}};
C.elig=function(v){var m=Math.round(v.y*12),f=+v.f/100;if(v.inc<=0||m<1||v.r<0||v.emi<0)return bad();
 var maxE=v.inc*f-v.emi;if(maxE<=0)return{stats:[S('Maximum new EMI',M(0),1),S('Eligible loan amount',M(0))],note:'Your existing EMIs already use up the limit of '+(f*100)+'% of income. Lenders may not offer a new loan.'};
 var i=v.r/1200,L=i===0?maxE*m:maxE*(1-Math.pow(1+i,-m))/i;
 return{stats:[S('Eligible loan amount',M(L),1),S('Maximum new EMI',M(maxE)),S('Total EMI limit ('+(f*100)+'%)',M(v.inc*f))],bar:[L,maxE*m-L,'Loan amount','Interest'],
 note:'An estimate only. Banks also check your credit score, age, job stability and the property or vehicle value.'}};
C.interest=function(v){if(v.p<=0||v.y<=0||v.r<0)return bad();var n=+v.n,A,t=v.type==='simple';
 A=t?v.p*(1+v.r*v.y/100):v.p*Math.pow(1+v.r/(100*n),n*v.y);
 return{stats:[S('Interest earned',M(A-v.p,2),1),S('Principal',M(v.p,2)),S('Total amount',M(A,2))],bar:[v.p,A-v.p,'Principal','Interest']}};
C.ci=function(v){var n=+v.n;if(v.p<=0||v.y<=0||v.r<0||v.y>100)return bad();var A=v.p*Math.pow(1+v.r/(100*n),n*v.y),rows=[],yrs=Math.min(Math.ceil(v.y),50);
 for(var y=1;y<=yrs;y++){var t=Math.min(y,v.y),a=v.p*Math.pow(1+v.r/(100*n),n*t);rows.push([y>v.y?N(v.y,2):y,M(a-v.p),M(a)])}
 return{stats:[S('Final amount',M(A,2),1),S('Principal',M(v.p,2)),S('Compound interest',M(A-v.p,2))],bar:[v.p,A-v.p,'Principal','Interest'],table:{head:['Year','Interest so far','Balance'],rows:rows}}};
C.si=function(v){if(v.p<=0||v.y<=0||v.r<0)return bad();var I=v.p*v.r*v.y/100;
 return{stats:[S('Simple interest',M(I,2),1),S('Principal',M(v.p,2)),S('Total amount',M(v.p+I,2))],bar:[v.p,I,'Principal','Interest']}};
C.sip=function(v){var m=Math.round(v.y*12),i=v.r/1200,g=v.step/100;if(v.p<=0||m<1||v.r<0||v.step<0||m>600)return bad();
 var bal=0,inv=0,pay=v.p,rows=[],ys=0;
 for(var k=1;k<=m;k++){if(k>1&&(k-1)%12===0)pay*=1+g;bal=(bal+pay)*(1+i);inv+=pay;
  if(k%12===0||k===m)rows.push([Math.ceil(k/12),M(inv),M(bal-inv),M(bal)])}
 return{stats:[S('Maturity value',M(bal),1),S('Amount invested',M(inv)),S('Estimated returns',M(bal-inv))],bar:[inv,bal-inv,'Invested','Returns'],
 table:{head:['Year','Invested so far','Returns','Value'],rows:rows},note:'Returns are not guaranteed. Market-linked investments can gain or lose value.'}};
C.swp=function(v){var B0=v.p,W=v.w,m=Math.round(v.y*12),i=v.r/1200;if(B0<=0||W<=0||m<1||v.r<0)return bad();
 var bal=B0,tw=0,rows=[],dep=false,last=m,yw=0,ys=B0;
 for(var k=1;k<=m;k++){var w=Math.min(W,bal);bal=(bal-w)*(1+i);tw+=w;yw+=w;if(bal<=0.005){dep=true;last=k;bal=0}
  if(k%12===0||k===m||dep){rows.push([Math.ceil(k/12),M(ys),M(yw),M(bal)]);ys=bal;yw=0;if(dep)break}}
 var ly=Math.floor(last/12),lm=last%12,lasts=dep?((ly?ly+(ly>1?' years':' year'):'')+(ly&&lm?' ':'')+(lm?lm+(lm>1?' months':' month'):'')):'Entire period';
 return{stats:[S('Final balance',M(bal),1),S('Total withdrawn',M(tw)),S('Money lasts',lasts)],table:{head:['Year','Opening balance','Withdrawn','Closing balance'],rows:rows},
 note:dep?'Your money runs out before the period ends. Try a smaller withdrawal.':''}};
C.fd=function(v){var n=+v.n;if(v.p<=0||v.y<=0||v.r<0)return bad();var A=v.p*Math.pow(1+v.r/(100*n),n*v.y);
 return{stats:[S('Maturity amount',M(A),1),S('Amount invested',M(v.p)),S('Total interest',M(A-v.p))],bar:[v.p,A-v.p,'Principal','Interest']}};
C.rd=function(v){if(v.p<=0||v.y<=0||v.r<0)return bad();var i=v.r/400,n=v.y*4,mat=i===0?v.p*12*v.y:v.p*(Math.pow(1+i,n)-1)/(1-Math.pow(1+i,-1/3)),dep=v.p*12*v.y;
 return{stats:[S('Maturity amount',M(mat),1),S('Total deposited',M(dep)),S('Interest earned',M(mat-dep))],bar:[dep,mat-dep,'Deposited','Interest']}};

/* ===== finance2 ===== */
function _tbl(h,r){return {head:h,rows:r}}
C.ppf=function(v){var a=Math.min(v.dep,150000),n=Math.round(v.yrs),r=v.rate/100;
 if(a<=0||n<15||n>60||r<0)return bad('Enter a yearly deposit above 0, a rate of 0 or more, and at least 15 years.');
 var bal=0,rows=[],tot=0;
 for(var y=1;y<=n;y++){var op=bal;tot+=a;var it=(bal+a)*r;bal=bal+a+it;rows.push([y,M(op),M(a),M(it),M(bal)])}
 var capNote=v.dep>150000?' The yearly limit of '+M(150000)+' was applied to your deposit.':'';
 return {stats:[S('Maturity value',M(bal),1),S('Total invested',M(tot)),S('Total interest',M(bal-tot))],bar:[tot,bal-tot,'Invested','Interest'],
  table:_tbl(['Year','Opening balance','Deposit','Interest','Closing balance'],rows),note:'Assumes the full deposit is made before the 5th of April each year and the rate stays constant. PPF rates are set by the government every quarter.'+capNote}};

C.gst=function(v){var r=parseFloat(v.rate);if(v.amt<=0||isNaN(r))return bad('Enter an amount above 0.');
 var net,gst,gross;
 if(v.mode==='add'){net=v.amt;gst=net*r/100;gross=net+gst}else{gross=v.amt;net=gross/(1+r/100);gst=gross-net}
 var st=r>0?[S('CGST ('+N(r/2,2)+'%)',M(gst/2,2)),S('SGST / UTGST ('+N(r/2,2)+'%)',M(gst/2,2))]:[];
 return {stats:[S('GST amount',M(gst,2),1),S('Price before GST',M(net,2)),S('Price including GST',M(gross,2))].concat(st),bar:[net,gst,'Base price','GST'],
  note:'For sales within one state GST is split equally into CGST and SGST. For sales between states the whole amount is charged as IGST.'}};

function _slab(ti,sl){var t=0;for(var i=0;i<sl.length;i++){var lo=sl[i][0],hi=sl[i][1],p=sl[i][2];if(ti>lo)t+=(Math.min(ti,hi)-lo)*p}return t}
var NEW_SL=[[0,400000,0],[400000,800000,.05],[800000,1200000,.10],[1200000,1600000,.15],[1600000,2000000,.20],[2000000,2400000,.25],[2400000,1e18,.30]];
function newTax(ti){var t=_slab(ti,NEW_SL);if(ti<=1200000)t=0;else t=Math.min(t,ti-1200000);return t}
function oldTax(ti,age){var ex=age==='80'?500000:age==='60'?300000:250000,sl;
 if(age==='80')sl=[[0,500000,0],[500000,1000000,.2],[1000000,1e18,.3]];
 else sl=[[0,ex,0],[ex,500000,.05],[500000,1000000,.2],[1000000,1e18,.3]];
 var t=_slab(ti,sl);if(ti<=500000)t=Math.max(0,t-12500);return t}
C.itax=function(v){if(v.inc<=0)return bad('Enter your annual income.');
 var d80c=Math.min(v.c80,150000),d80d=Math.min(v.d80,100000),nps=Math.min(v.nps,50000),hl=Math.min(v.hl,200000);
 var nti=Math.max(0,v.inc-75000),nt=newTax(nti),ncess=nt*.04,ntot=nt+ncess;
 var ded=d80c+d80d+nps+hl+v.hra+v.oth,oti=Math.max(0,v.inc-50000-ded),ot=oldTax(oti,v.age),ocess=ot*.04,otot=ot+ocess;
 var best=ntot<=otot?'New regime':'Old regime',save=Math.abs(ntot-otot);
 return {stats:[S('Tax: new regime',M(ntot),ntot<=otot),S('Tax: old regime',M(otot),otot<ntot),S('Better option',best+' (saves '+M(save)+')')],
  table:_tbl(['Item','New regime','Old regime'],[['Gross income',M(v.inc),M(v.inc)],['Standard deduction',M(75000),M(50000)],['Other deductions','-',M(ded)],['Taxable income',M(nti),M(oti)],['Tax on slabs (after rebate)',M(nt),M(ot)],['Health and education cess (4%)',M(ncess),M(ocess)],['Total tax',M(ntot),M(otot)],['Monthly tax',M(ntot/12),M(otot/12)],['Effective tax rate',N(ntot/v.inc*100)+'%',N(otot/v.inc*100)+'%']]),
  note:'Estimate for FY 2026-27 (AY 2027-28) for a resident individual. Surcharge is not included. Rates and limits can change, so please verify with the Income Tax Department before filing.'}};

C.salary=function(v){if(v.ctc<=0||v.basic<=0||v.basic>100)return bad('Enter your annual CTC and a basic salary percentage between 1 and 100.');
 var basic=v.ctc*v.basic/100,hra=basic*v.hra/100,epf=Math.min(basic,v.ctc)*.12,
  gross=v.ctc-epf,special=gross-basic-hra;
 if(special<0)return bad('Basic and HRA are more than the CTC allows. Lower the basic % or HRA %.');
 var ti=Math.max(0,gross-75000),tax=newTax(ti)*1.04,pt=v.pt*12,
  net=gross-epf-pt-tax;
 return {stats:[S('Monthly in-hand',M(net/12),1),S('Annual in-hand',M(net)),S('Monthly gross',M(gross/12))],bar:[net,v.ctc-net,'Take-home','Deductions and PF'],
  table:_tbl(['Component','Monthly','Annual'],[['Basic salary',M(basic/12),M(basic)],['HRA',M(hra/12),M(hra)],['Special / other allowance',M(special/12),M(special)],['Gross salary',M(gross/12),M(gross)],['Employer PF (part of CTC)',M(epf/12),M(epf)],['Employee PF (12% of basic)',M(-epf/12),M(-epf)],['Professional tax',M(-pt/12),M(-pt)],['Income tax (new regime estimate)',M(-tax/12),M(-tax)],['Net take-home',M(net/12),M(net)]]),
  note:'Assumes the employer PF contribution is included in CTC and equals the employee PF. Tax is a simple new-regime estimate with the standard deduction only.'}};

C.infl=function(v){var n=Math.round(v.yrs);if(v.amt<=0||v.rate<0||n<1||n>100)return bad('Enter an amount above 0, a rate of 0 or more, and years between 1 and 100.');
 var r=v.rate/100,f=v.amt*Math.pow(1+r,n),p=v.amt/Math.pow(1+r,n),rows=[];
 for(var y=1;y<=Math.min(n,30);y++)rows.push([y,M(v.amt*Math.pow(1+r,y)),M(v.amt/Math.pow(1+r,y))]);
 return {stats:[S('Cost after '+n+' years',M(f),1),S('Value of '+M(v.amt)+' then',M(p)),S('Loss of purchasing power',N((1-1/Math.pow(1+r,n))*100)+'%')],
  table:_tbl(['Year','Cost of the same goods','Buying power of your money'],rows),note:'Assumes a constant inflation rate every year.'}};

C.pl=function(v){if(v.cp<=0||v.sp<0)return bad('Enter a cost price above 0.');
 var d=(v.sp-v.cp)*Math.max(1,v.qty),w=d>=0?'Profit':'Loss',pc=(v.sp-v.cp)/v.cp*100;
 if(d===0)return {stats:[S('Result','No profit, no loss',1)],note:'Selling price equals cost price.'};
 return {stats:[S(w,M(Math.abs(d),2),1),S(w+' %',N(Math.abs(pc))+'%'),S('Margin on selling price',v.sp>0?N(Math.abs(pc)*v.cp/v.sp)+'%':'—'),S('Total cost',M(v.cp*Math.max(1,v.qty),2)),S('Total sales',M(v.sp*Math.max(1,v.qty),2))]}};

C.disc=function(v){if(v.price<=0||v.d<0||v.d>100)return bad('Enter a price above 0 and a discount between 0 and 100.');
 var s=v.price*v.d/100,f=v.price-s,x=v.d2>0?f*(1-v.d2/100):f;
 var st=[S('Final price',M(x,2),1),S('You save',M(v.price-x,2)),S('Total discount',N((v.price-x)/v.price*100)+'%')];
 return {stats:st,bar:[x,v.price-x,'You pay','You save'],note:v.d2>0?'The extra discount is applied on the already discounted price.':''}};

C.brk=function(v){if(v.buy<=0||v.sell<=0||v.qty<=0)return bad('Enter buy price, sell price and quantity above 0.');
 var intra=v.type==='intra';
 function charges(b,s){var bt=b*v.qty,st=s*v.qty,tt=bt+st,brk=intra?Math.min(bt*v.brk/100,v.cap)+Math.min(st*v.brk/100,v.cap):bt*v.brk/100+st*v.brk/100;
  var stt=intra?st*.00025:tt*.001,ex=tt*v.ex/100,sebi=tt*.000001,stamp=bt*(intra?.00003:.00015),gst=(brk+ex+sebi)*.18;
  return {brk:brk,stt:stt,ex:ex,sebi:sebi,stamp:stamp,gst:gst,tot:brk+stt+ex+sebi+stamp+gst}}
 var c=charges(v.buy,v.sell),gp=(v.sell-v.buy)*v.qty,net=gp-c.tot;
 var lo=v.buy,hi=v.buy*2;for(var i=0;i<60;i++){var m=(lo+hi)/2;if((m-v.buy)*v.qty-charges(v.buy,m).tot>=0)hi=m;else lo=m}
 return {stats:[S('Net profit / loss',M(net,2),1),S('Gross profit / loss',M(gp,2)),S('Total charges',M(c.tot,2)),S('Breakeven sell price',M(hi,2))],
  table:_tbl(['Charge','Amount'],[['Brokerage',M(c.brk,2)],['STT',M(c.stt,2)],['Exchange transaction charges',M(c.ex,2)],['GST (18%)',M(c.gst,2)],['SEBI charges',M(c.sebi,2)],['Stamp duty',M(c.stamp,2)],['Total',M(c.tot,2)]]),
  note:'STT: 0.1% on buy and sell for delivery, 0.025% on sell for intraday. Stamp duty: 0.015% on buy for delivery, 0.003% for intraday. Rates differ by broker and exchange, so check your contract note.'}};

C.savg=function(v){var tq=0,tv=0,i,p,q;
 for(i=1;i<=5;i++){p=v['p'+i];q=v['q'+i];if(p>0&&q>0){tq+=q;tv+=p*q}}
 if(tq<=0)return bad('Enter at least one purchase with price and quantity.');
 var avg=tv/tq,st=[S('Current average price',M(avg,2),!(v.np>0&&v.nq>0)),S('Total quantity',N(tq,0)),S('Total invested',M(tv,2))];
 if(v.np>0&&v.nq>0){var a2=(tv+v.np*v.nq)/(tq+v.nq);st=[S('New average price',M(a2,2),1),S('Current average price',M(avg,2)),S('Total quantity',N(tq+v.nq,0)),S('Total invested',M(tv+v.np*v.nq,2))];
  return {stats:st,note:'Your average price changes by '+M(a2-avg,2)+' per share after the new purchase.'}}
 return {stats:st}};

C.sprofit=function(v){if(v.buy<=0||v.sell<=0||v.qty<=0)return bad('Enter buy price, sell price and quantity above 0.');
 var inv=v.buy*v.qty,rev=v.sell*v.qty,ch=(inv+rev)*v.ch/100,gp=rev-inv,np=gp-ch;
 return {stats:[S('Net profit / loss',M(np,2),1),S('Return',N(np/inv*100)+'%'),S('Invested',M(inv,2)),S('Sale value',M(rev,2)),S('Gross profit / loss',M(gp,2)),S('Charges',M(ch,2))],bar:[inv,Math.max(0,np),'Invested','Profit'],
  note:'Charges are taken as a percentage of buy value plus sell value.'}};

C.mfr=function(v){var y=v.yrs,r=v.rate/100;
 if(v.mode==='lump'){if(v.amt<=0||y<=0||r<-.99)return bad();var f=v.amt*Math.pow(1+r,y);
  return {stats:[S('Maturity value',M(f),1),S('Invested',M(v.amt)),S('Gain',M(f-v.amt)),S('Absolute return',N((f/v.amt-1)*100)+'%')],bar:[v.amt,f-v.amt,'Invested','Gain']}}
 if(v.mode==='sip'){var n=Math.round(y*12);if(v.amt<=0||n<1||r<-.99)return bad();var i=Math.pow(1+r,1/12)-1,f2=i===0?v.amt*n:v.amt*((Math.pow(1+i,n)-1)/i)*(1+i),inv=v.amt*n;
  return {stats:[S('Maturity value',M(f2),1),S('Invested',M(inv)),S('Gain',M(f2-inv)),S('Absolute return',N((f2/inv-1)*100)+'%')],bar:[inv,f2-inv,'Invested','Gain'],note:'Monthly instalments are assumed at the start of each month with an effective yearly return equal to the rate entered.'}}
 if(v.inv<=0||v.fv<=0||y<=0)return bad('Enter invested amount, current value and years above 0.');
 var cg=(Math.pow(v.fv/v.inv,1/y)-1)*100;
 return {stats:[S('CAGR',N(cg)+'%',1),S('Absolute return',N((v.fv/v.inv-1)*100)+'%'),S('Gain',M(v.fv-v.inv))],bar:[v.inv,Math.max(0,v.fv-v.inv),'Invested','Gain'],note:'CAGR suits a single lump sum. For SIPs, use XIRR from your fund statement.'}};

(function(){
function actF(a){return parseFloat(a)}
function bmiCat(b){return b<18.5?'Underweight':b<25?'Normal weight':b<30?'Overweight':'Obese'}
function mifflin(v){return 10*v.kg+6.25*v.cm-5*v.age+(v.sex==='m'?5:-161)}
function okBody(v){return v.age>0&&v.age<120&&v.kg>0&&v.cm>0}
var MED='This is a general estimate and not medical advice. Please talk to a doctor or a registered dietitian for personal guidance.';

C.bmi=function(v){var kg,m;
 if(v.u==='m'){kg=v.kg;m=v.cm/100}else{kg=v.lb*0.45359237;m=(v.ft*12+v.inch)*0.0254}
 if(!(kg>0&&m>0))return bad('Enter a valid weight and height.');
 var b=kg/(m*m),lo=18.5*m*m,hi=24.9*m*m;
 var rng=v.u==='m'?N(lo,1)+' to '+N(hi,1)+' kg':N(lo/0.45359237,1)+' to '+N(hi/0.45359237,1)+' lb';
 return {stats:[S('Your BMI',N(b,1),1),S('Category',bmiCat(b)),S('Healthy weight range',rng)],note:'BMI is a screening tool and does not measure body fat directly. '+MED}};

C.bmr=function(v){if(!okBody(v))return bad('Enter valid age, weight and height.');
 var m=mifflin(v),hb=v.sex==='m'?88.362+13.397*v.kg+4.799*v.cm-5.677*v.age:447.593+9.247*v.kg+3.098*v.cm-4.33*v.age;
 return {stats:[S('BMR (Mifflin-St Jeor)',N(m,0)+' kcal/day',1),S('BMR (Harris-Benedict)',N(hb,0)+' kcal/day'),S('Per hour',N(m/24,0)+' kcal')],note:'BMR is the energy your body burns at complete rest. '+MED}};

C.tdee=function(v){if(!okBody(v))return bad('Enter valid age, weight and height.');
 var b=mifflin(v),t=b*actF(v.act);
 return {stats:[S('Daily calories (TDEE)',N(t,0)+' kcal',1),S('BMR',N(b,0)+' kcal'),S('Activity multiplier','x '+actF(v.act))],note:MED}};

C.ideal=function(v){if(!(v.cm>0))return bad('Enter a valid height.');
 var inch=v.cm/2.54,over=Math.max(0,inch-60),m=v.sex==='m',
 d=(m?50:45.5)+2.3*over,r=(m?52:49)+(m?1.9:1.7)*over,mi=(m?56.2:53.1)+(m?1.41:1.36)*over,h=(m?48:45.5)+(m?2.7:2.2)*over;
 var av=(d+r+mi+h)/4;
 return {stats:[S('Average of formulas',N(av,1)+' kg',1),S('Devine',N(d,1)+' kg'),S('Robinson',N(r,1)+' kg'),S('Miller',N(mi,1)+' kg'),S('Hamwi',N(h,1)+' kg')],
  note:'These formulas were designed for adults and give a rough target only. '+MED}};

C.bodyfat=function(v){var f=v.sex==='f',x,lg=Math.log10;
 if(!(v.cm>0&&v.neck>0&&v.waist>0))return bad('Enter valid measurements.');
 if(f){if(!(v.hip>0))return bad('Enter your hip measurement.');if(v.waist+v.hip-v.neck<=0)return bad('Check your measurements.');
  x=163.205*lg(v.waist+v.hip-v.neck)-97.684*lg(v.cm)-78.387}
 else{if(v.waist<=v.neck)return bad('Waist must be larger than neck.');x=86.010*lg(v.waist-v.neck)-70.041*lg(v.cm)+36.76}
 if(!(x>0&&x<70))return bad('These measurements give an unrealistic result. Please check them.');
 var cat=f?(x<14?'Essential fat':x<21?'Athletes':x<25?'Fitness':x<32?'Average':'Above average'):(x<6?'Essential fat':x<14?'Athletes':x<18?'Fitness':x<25?'Average':'Above average');
 var fat=v.kg>0?v.kg*x/100:0;
 var st=[S('Body fat',N(x,1)+' %',1),S('Category',cat)];
 if(v.kg>0)st.push(S('Fat mass',N(fat,1)+' kg'),S('Lean mass',N(v.kg-fat,1)+' kg'));
 return {stats:st,note:'Uses the US Navy circumference method, accurate to a few percent. '+MED}};

C.calorie=function(v){if(!okBody(v))return bad('Enter valid age, weight and height.');
 var t=mifflin(v)*actF(v.act),floor=v.sex==='m'?1500:1200;
 function r(d){return N(Math.max(floor,t+d),0)+' kcal'}
 return {stats:[S('Maintain weight',N(t,0)+' kcal',1),S('Lose 0.25 kg / week',r(-275)),S('Lose 0.5 kg / week',r(-550)),S('Gain 0.25 kg / week',r(275)),S('Gain 0.5 kg / week',r(550))],
  note:'About 7,700 kcal equals 1 kg of body weight. Targets below '+floor+' kcal are not shown; very low intakes should only be followed under medical supervision. '+MED}};

C.protein=function(v){if(!(v.kg>0))return bad('Enter a valid weight.');
 var g=actF(v.goal),lo=g*0.9,hi=g*1.1;
 return {stats:[S('Protein per day',N(v.kg*g,0)+' g',1),S('Range',N(v.kg*lo,0)+' to '+N(v.kg*hi,0)+' g'),S('Per meal (4 meals)',N(v.kg*g/4,0)+' g'),S('Calories from protein',N(v.kg*g*4,0)+' kcal')],
  note:'Based on grams of protein per kg of body weight ('+g+' g/kg). People with kidney disease should follow their doctor\'s advice.'}};

C.water=function(v){if(!(v.kg>0))return bad('Enter a valid weight.');
 var base=v.kg*0.033,ex=Math.max(0,v.min)/30*0.35,cl=actF(v.clim),t=base+ex+cl;
 return {stats:[S('Water per day',N(t,1)+' litres',1),S('Glasses (250 ml)',N(t*4,0)),S('Base need',N(base,1)+' L'),S('Extra for exercise and heat',N(ex+cl,1)+' L')],
  note:'Roughly 33 ml per kg plus extra for exercise and hot weather. Food and other drinks also contribute. '+MED}};

C.preg=function(v){if(!v.lmp)return bad('Select the first day of your last period.');
 var l=pd(v.lmp),cyc=v.cycle>=20&&v.cycle<=45?v.cycle:28,due=addDays(l,280+(cyc-28)),now=new Date();now.setHours(0,0,0,0);
 var d=Math.round((now-l)/864e5),w=Math.floor(d/7),dd=d%7,left=Math.round((due-now)/864e5);
 var st=[S('Estimated due date',fdate(due),1)];
 if(d<0)st.push(S('Status','Last period date is in the future'));
 else if(d>300)st.push(S('Status','Past the expected pregnancy length'));
 else st.push(S('Pregnancy now',w+' weeks '+dd+' days'),S('Days left',String(Math.max(0,left))),S('Trimester',w<13?'First':w<27?'Second':'Third'));
 return {stats:st,note:'Calculated with Naegele\'s rule (LMP + 280 days). Only about 4% of babies arrive on the due date. '+MED}};

C.ovul=function(v){if(!v.lmp)return bad('Select the first day of your last period.');
 var l=pd(v.lmp),c=v.cycle>=20&&v.cycle<=45?v.cycle:28,ov=addDays(l,c-14);
 return {stats:[S('Ovulation day',fdate(ov),1),S('Fertile window',fdate(addDays(ov,-5))+' to '+fdate(addDays(ov,1))),S('Next period expected',fdate(addDays(l,c))),S('Pregnancy test from',fdate(addDays(l,c+1)))],
  note:'Ovulation is assumed 14 days before the next period. Cycles vary, so treat this as an estimate. '+MED}};

C.whtr=function(v){if(!(v.cm>0&&v.waist>0))return bad('Enter valid height and waist.');
 var r=v.waist/v.cm,c=r<0.4?'Underweight range':r<0.5?'Healthy':r<0.6?'Increased health risk':'High health risk';
 return {stats:[S('Waist-to-height ratio',N(r,2),1),S('Category',c),S('Keep waist below',N(v.cm/2,1)+' cm')],note:'A ratio below 0.5 is generally considered healthy. '+MED}};

var SPL={bal:[40,30,30],low:[25,35,40],high:[35,40,25],keto:[5,25,70],end:[55,20,25]};
C.macro=function(v){if(!(v.cal>0))return bad('Enter your daily calories.');
 var k=v.cal+actF(v.goal),s=SPL[v.split];if(k<=0)return bad('Calories too low.');
 var c=k*s[0]/100/4,p=k*s[1]/100/4,f=k*s[2]/100/9;
 return {stats:[S('Target calories',N(k,0)+' kcal',1),S('Carbohydrates',N(c,0)+' g ('+s[0]+'%)'),S('Protein',N(p,0)+' g ('+s[1]+'%)'),S('Fat',N(f,0)+' g ('+s[2]+'%)')],
  bar:[c*4,p*4+f*9,'Carbs','Protein and fat'],note:'Carbs and protein give 4 kcal per gram; fat gives 9. '+MED}};

C.age=function(v){if(!v.dob||!v.on)return bad('Select both dates.');
 var a=pd(v.dob),b=pd(v.on);if(a>b)return bad('Date of birth must be before the other date.');
 var t=ymd(a,b),days=Math.round((b-a)/864e5),nb=new Date(b.getFullYear(),a.getMonth(),a.getDate());
 if(nb<b)nb.setFullYear(nb.getFullYear()+1);
 var left=Math.round((nb-b)/864e5);
 return {stats:[S('Age',t[0]+' years, '+t[1]+' months, '+t[2]+' days',1),S('Total months',N(t[0]*12+t[1],0)),S('Total weeks',N(Math.floor(days/7),0)),S('Total days',N(days,0)),S('Total hours',N(days*24,0)),
  S('Next birthday',left===0?'Today':'In '+left+' days'),S('Born on a',a.toLocaleDateString('en-GB',{weekday:'long'}))]}};

C.dob=function(v){if(!v.on)return bad('Select a date.');if(!(v.age>=0&&v.age<=120))return bad('Enter a valid age.');
 var on=pd(v.on),age=Math.floor(v.age),late=new Date(on.getTime()),early=new Date(on.getTime());
 late.setFullYear(on.getFullYear()-age);early.setFullYear(on.getFullYear()-age-1);early=addDays(early,1);
 return {stats:[S('Born between',fdate(early)+' and '+fdate(late),1),S('Possible birth year',early.getFullYear()===late.getFullYear()?String(late.getFullYear()):early.getFullYear()+' or '+late.getFullYear()),S('Age on',fdate(on)+': '+age+' years')],
  note:'Without the exact month the date can only be narrowed to a one-year window.'}};

C.sleep=function(v){if(!v.t)return bad('Select a time.');
 var p=v.t.split(':'),m=(+p[0])*60+(+p[1]),rows=[],fall=14;
 function f(x){x=((x%1440)+1440)%1440;var h=Math.floor(x/60),mm=x%60,ap=h>=12?'PM':'AM';h=h%12||12;return h+':'+pad(mm)+' '+ap}
 if(v.mode==='w'){[6,5,4,3].forEach(function(c){rows.push([f(m-c*90-fall),c+' cycles',N(c*1.5,1)+' hours'])})}
 else{[3,4,5,6].forEach(function(c){rows.push([f(m+fall+c*90),c+' cycles',N(c*1.5,1)+' hours'])})}
 return {table:{head:[v.mode==='w'?'Go to bed at':'Wake up at','Sleep cycles','Total sleep'],rows:rows},note:'Based on 90-minute sleep cycles and about 14 minutes to fall asleep. Most adults need 5 to 6 cycles (7.5 to 9 hours). '+MED}};
})();

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

(function(){
function P(x){return N(x,2)}
function grades(p){return p>=90?['A+','Outstanding']:p>=80?['A','Excellent']:p>=70?['B','Very good']:p>=60?['C','Good']:p>=50?['D','Satisfactory']:p>=40?['E','Pass']:['F','Fail']}

C.e_cgpa=function(v){var a=nums(v.sg);if(!a||!a.length)return bad('Enter your semester grade points separated by commas.');
 if(a.some(function(x){return x<0||x>v.scale}))return bad('Every grade point must be between 0 and '+v.scale+'.');
 var w=nums(v.cr),cg,mode='Simple average';
 if(w&&w.length){if(w.length!==a.length||w.some(function(x){return x<=0}))return bad('Enter one credit value for each semester, or leave credits empty.');
  var tw=w.reduce(function(x,y){return x+y},0);cg=a.reduce(function(s,x,i){return s+x*w[i]},0)/tw;mode='Credit-weighted'}
 else cg=a.reduce(function(x,y){return x+y},0)/a.length;
 return {stats:[S('CGPA',N(cg,2),1),S('Percentage',P(cg*v.mult)+' %'),S('Semesters counted',String(a.length)),S('Method',mode)],note:'Percentage = CGPA x '+v.mult+'. Confirm the multiplier your university uses.'}};

C.e_cgpap=function(v){if(v.cgpa<0||v.cgpa>10||!(v.mult>0))return bad('Enter a CGPA between 0 and 10 and a valid multiplier.');
 var p=v.cgpa*v.mult;if(p>100)return bad('The result is above 100 %. Check the multiplier.');
 return {stats:[S('Percentage',P(p)+' %',1),S('CGPA',N(v.cgpa,2)),S('Multiplier','x '+v.mult)],note:'Percentage = CGPA x multiplier. CBSE uses 9.5.'}};

C.e_pcgpa=function(v){if(v.pct<0||v.pct>100||!(v.mult>0))return bad('Enter a percentage between 0 and 100 and a valid multiplier.');
 var c=v.pct/v.mult;if(c>10)return bad('The result is above 10. Check the multiplier.');
 return {stats:[S('CGPA',N(c,2),1),S('Percentage',P(v.pct)+' %'),S('Multiplier','/ '+v.mult)],note:'CGPA = percentage / multiplier. CBSE uses 9.5.'}};

C.e_gpa=function(v){var pts=0,cr=0,n=0,rows=[];
 for(var i=1;i<=6;i++){var g=v['g'+i],c=v['c'+i];if(g==='x'||!(c>0))continue;var gp=parseFloat(g);pts+=gp*c;cr+=c;n++;rows.push(['Course '+i,N(gp,1),N(c,1),N(gp*c,1)])}
 if(!cr)return bad('Add at least one course with a grade and credits.');
 return {stats:[S('GPA',N(pts/cr,2),1),S('Total credits',N(cr,1)),S('Courses',String(n)),S('Quality points',N(pts,1))],table:{head:['Course','Grade points','Credits','Quality points'],rows:rows},note:'GPA = total quality points / total credits on the standard 4.0 scale.'}};

C.e_marks=function(v){var o=0,m=0,rows=[];
 for(var i=1;i<=6;i++){var a=v['o'+i],b=v['m'+i];if(!(b>0))continue;if(a<0||a>b)return bad('Marks obtained in subject '+i+' must be between 0 and the maximum.');o+=a;m+=b;rows.push(['Subject '+i,N(a,2)+' / '+N(b,2),P(a/b*100)+' %'])}
 if(!m)return bad('Enter maximum marks for at least one subject.');var p=o/m*100,g=grades(p);
 return {stats:[S('Percentage',P(p)+' %',1),S('Total marks',N(o,2)+' / '+N(m,2)),S('Grade',g[0]+' ('+g[1]+')'),S('Division',p>=60?'First division':p>=45?'Second division':p>=33?'Third division':'Fail')],table:{head:['Subject','Marks','Percentage'],rows:rows}}};

C.e_grade=function(v){if(v.pct<0||v.pct>100)return bad('Enter a percentage between 0 and 100.');
 var g=grades(v.pct),st=[S('Grade',g[0],1),S('Remark',g[1]),S('Result',v.pct>=40?'Pass':'Fail')],note='Grade bands: A+ 90 and above, A 80, B 70, C 60, D 50, E 40, F below 40. Your institution may use different bands.';
 if(v.w>0&&v.w<=100){var need=(v.tgt-v.cur*(1-v.w/100))/(v.w/100);
  st.push(S('Needed on the final exam',need>100?'Not possible ('+P(need)+' %)':need<=0?'Already achieved':P(need)+' %'))}
 return {stats:st,note:note}};

C.e_agediff=function(v){if(!v.d1||!v.d2)return bad('Select both dates.');
 var a=pd(v.d1),b=pd(v.d2),older=a<=b?'Person 1':'Person 2',lo=a<=b?a:b,hi=a<=b?b:a,t=ymd(lo,hi),days=Math.round((hi-lo)/864e5);
 if(days===0)return {stats:[S('Age difference','Same birth date',1)]};
 return {stats:[S('Age difference',t[0]+' years, '+t[1]+' months, '+t[2]+' days',1),S('Older person',older),S('Total days',N(days,0)),S('Total months',N(t[0]*12+t[1],0))]}};

C.e_datediff=function(v){if(!v.d1||!v.d2)return bad('Select both dates.');
 var a=pd(v.d1),b=pd(v.d2),sw=a>b;if(sw){var x=a;a=b;b=x}
 var t=ymd(a,b),days=Math.round((b-a)/864e5)+(v.inc?1:0);
 return {stats:[S('Difference',t[0]+' years, '+t[1]+' months, '+t[2]+' days',1),S('Total days',N(days,0)),S('Total weeks',N(Math.floor(days/7),0)+' weeks '+(days%7)+' days'),S('Total months',N(t[0]*12+t[1],0)),S('Total hours',N(days*24,0))],note:(sw?'The dates were swapped so the earlier one comes first. ':'')+(v.inc?'The end date is counted too (+1 day).':'')}};

function hms(s){var neg=s<0;s=Math.abs(Math.round(s));return (neg?'-':'')+Math.floor(s/3600)+':'+pad(Math.floor(s%3600/60))+':'+pad(s%60)}
C.e_time=function(v){var a=v.h1*3600+v.m1*60+v.s1,b=v.h2*3600+v.m2*60+v.s2,r=v.op==='+'?a+b:a-b;
 return {stats:[S('Result (h:mm:ss)',hms(r),1),S('Total seconds',N(r,0)),S('Total minutes',N(r/60,2)),S('Decimal hours',N(r/3600,4))],note:r<0?'The result is negative because the second time is larger.':''}};
})();

/* ===== Business & E-commerce ===== */
function pc(x){return N(x,2)+'%'}
C.margin=function(v){if(v.price<=0||v.cost<0)return bad('Enter a selling price above zero and a valid cost.');
 var p=v.price-v.cost;return {stats:[S('Profit',M(p,2),1),S('Profit margin',v.price?pc(p/v.price*100):'—'),S('Markup',v.cost>0?pc(p/v.cost*100):'—')],bar:[Math.max(p,0),v.cost,'Profit','Cost'],note:'Margin = profit / selling price. Markup = profit / cost.'}};
C.markup=function(v){if(v.cost<=0)return bad('Enter a cost above zero.');
 var price=v.cost*(1+v.mk/100),p=price-v.cost;return {stats:[S('Selling price',M(price,2),1),S('Profit',M(p,2)),S('Equivalent margin',pc(p/price*100))],bar:[p,v.cost,'Profit','Cost']}};
C.selling=function(v){if(v.cost<=0||v.pct<0)return bad('Enter a cost above zero and a valid percentage.');
 var price;if(v.mode==='margin'){if(v.pct>=100)return bad('Margin must be below 100%.');price=v.cost/(1-v.pct/100)}else price=v.cost*(1+v.pct/100);
 var p=price-v.cost;return {stats:[S('Selling price',M(price,2),1),S('Profit per unit',M(p,2)),S('Margin',pc(p/price*100)),S('Markup',pc(p/v.cost*100))],bar:[p,v.cost,'Profit','Cost']}};
C.costprice=function(v){if(v.sp<=0||v.pct<=-100)return bad('Enter a selling price and a valid profit percentage.');
 var cp=v.base==='cost'?v.sp/(1+v.pct/100):v.sp*(1-v.pct/100);if(cp<0)return bad('Profit percentage is too high.');
 var p=v.sp-cp;return {stats:[S('Cost price',M(cp,2),1),S('Profit',M(p,2)),S('Profit on cost',cp>0?pc(p/cp*100):'—'),S('Profit on selling price',pc(p/v.sp*100))],bar:[p,cp,'Profit','Cost']}};
C.vat=function(v){if(v.amt<=0||v.rate<0)return bad();var r=v.rate/100,net,gross;
 if(v.mode==='add'){net=v.amt;gross=net*(1+r)}else{gross=v.amt;net=gross/(1+r)}
 return {stats:[S('Price excluding VAT',M(net,2)),S('VAT amount',M(gross-net,2),1),S('Price including VAT',M(gross,2))],bar:[net,gross-net,'Net price','VAT']}};
C.gstie=function(v){if(v.amt<=0||v.rate<0)return bad();var r=parseFloat(v.rate)/100,net,gross;
 if(v.mode==='excl'){net=v.amt;gross=net*(1+r)}else{gross=v.amt;net=gross/(1+r)}var g=gross-net;
 var st=[S('Base price',M(net,2)),S('Total GST',M(g,2),1),S('Final price',M(gross,2))];
 if(v.supply==='intra'){st.push(S('CGST ('+N(r*50,2)+'%)',M(g/2,2)));st.push(S('SGST ('+N(r*50,2)+'%)',M(g/2,2)))}else st.push(S('IGST ('+N(r*100,2)+'%)',M(g,2)));
 return {stats:st,bar:[net,g,'Base price','GST']}};
C.breakeven=function(v){var cm=v.price-v.vc;if(v.price<=0||v.vc<0||v.fixed<0)return bad();if(cm<=0)return bad('Selling price must be higher than variable cost per unit.');
 var u=Math.ceil(v.fixed/cm),t=Math.ceil((v.fixed+v.target)/cm);
 var st=[S('Break-even units',N(u,0),1),S('Break-even revenue',M(u*v.price,0)),S('Contribution per unit',M(cm,2)),S('Contribution margin',pc(cm/v.price*100))];
 if(v.target>0)st.push(S('Units for target profit',N(t,0)));
 return {stats:st,bar:[v.fixed,u*v.vc,'Fixed costs','Variable costs']}};
C.revenue=function(v){if(v.price<0||v.units<0)return bad();var g=v.price*v.units,d=g*v.disc/100,r=(g-d)*v.ret/100,n=g-d-r;
 return {stats:[S('Gross revenue',M(g,0)),S('Discounts',M(d,0)),S('Returns',M(r,0)),S('Net revenue',M(n,0),1),S('Revenue per month x12',M(n*12,0))],bar:[n,d+r,'Net revenue','Discounts and returns']}};
C.commission=function(v){if(v.sales<=0)return bad('Enter the sales amount.');var c;
 if(v.mode==='flat')c=v.sales*v.r1/100;else c=Math.min(v.sales,v.limit)*v.r1/100+Math.max(v.sales-v.limit,0)*v.r2/100;
 return {stats:[S('Commission',M(c,2),1),S('Effective rate',pc(c/v.sales*100)),S('Sales after commission',M(v.sales-c,2))],bar:[c,v.sales-c,'Commission','Remaining']}};
C.roas=function(v){if(v.spend<=0||v.rev<0)return bad('Ad spend must be above zero.');var ro=v.rev/v.spend,st=[S('ROAS',N(ro,2)+'x',1),S('Revenue per '+CUR+'1 spent',M(ro,2)),S('ACOS',pc(v.spend/v.rev*100))];
 if(v.margin>0&&v.margin<=100){var be=100/v.margin;st.push(S('Break-even ROAS',N(be,2)+'x'));st.push(S('Profit after ad spend',M(v.rev*v.margin/100-v.spend,0)))}
 return {stats:st,note:'Break-even ROAS = 1 / profit margin. Above it, your ads make a profit.'}};
C.roi=function(v){if(v.cost<=0)return bad('Enter the amount invested.');var g=v.ret-v.cost,roi=g/v.cost*100,st=[S('Net gain',M(g,0),1),S('ROI',pc(roi))];
 if(v.years>0&&v.ret>0)st.push(S('Annualised ROI (CAGR)',pc((Math.pow(v.ret/v.cost,1/v.years)-1)*100)));
 return {stats:st,bar:[Math.max(g,0),v.cost,'Gain','Invested']}};
C.shipping=function(v){if(v.l<=0||v.w<=0||v.h<=0||v.wt<0)return bad('Enter the package size and weight.');var vol=v.l*v.w*v.h/v.div,ch=Math.max(vol,v.wt),slabs=Math.max(1,Math.ceil(ch/v.slab-1e-9)),c=v.first+(slabs-1)*v.extra;
 return {stats:[S('Volumetric weight',N(vol,2)+' kg'),S('Actual weight',N(v.wt,2)+' kg'),S('Chargeable weight',N(ch,2)+' kg',1),S('Shipping cost',M(c,2),1)],note:'Chargeable weight is the higher of actual and volumetric weight. Courier slab rates differ, so edit the rates to match your courier.'}};
C.amazon=function(v){if(v.price<=0)return bad('Enter the selling price.');var ref=v.price*v.ref/100,fees=ref+v.close+v.ship,gst=fees*v.gst/100,tot=fees+gst,net=v.price-tot,prof=net-v.cost;
 return {stats:[S('Referral fee',M(ref,2)),S('Closing + shipping fees',M(v.close+v.ship,2)),S('GST on fees',M(gst,2)),S('Total Amazon fees',M(tot,2)),S('Net payout',M(net,2),1),S('Profit after product cost',M(prof,2),1)],bar:[Math.max(net,0),tot,'Payout','Fees'],note:'Referral fee, closing fee and FBA fees vary by category and price band. Check the current rate card on Amazon Seller Central and edit the rates above.'}};
C.flipkart=function(v){if(v.price<=0)return bad('Enter the selling price.');var com=v.price*v.com/100,fees=com+v.fixed+v.ship+v.coll,gst=fees*v.gst/100,tot=fees+gst,net=v.price-tot,prof=net-v.cost;
 return {stats:[S('Commission',M(com,2)),S('Fixed + collection fee',M(v.fixed+v.coll,2)),S('Shipping fee',M(v.ship,2)),S('GST on fees',M(gst,2)),S('Total Flipkart fees',M(tot,2)),S('Settlement amount',M(net,2),1),S('Profit after product cost',M(prof,2),1)],bar:[Math.max(net,0),tot,'Settlement','Fees'],note:'Commission, fixed and shipping fees vary by category and price. Check the current rate card in Flipkart Seller Hub and edit the rates above.'}};
C.ecom=function(v){if(v.price<=0)return bad('Enter the selling price.');var pf=v.price*v.fee/100,rr=Math.min(Math.max(v.ret,0),100)/100,
 ok=v.price-v.cost-pf-v.ship-v.pack-v.ads,lost=-(v.ship+v.pack+v.ads),prof=(1-rr)*ok+rr*lost;
 /* a returned order: product comes back (cost recovered), shipping and packaging are lost, ad cost is lost */
 return {stats:[S('Platform fee',M(pf,2)),S('Profit if delivered',M(ok,2)),S('Expected profit per order',M(prof,2),1),S('Net margin',pc(prof/v.price*100)),S('Profit on '+N(v.orders,0)+' orders',M(prof*v.orders,0))],bar:[Math.max(prof,0),v.price-Math.max(prof,0),'Profit','Costs and fees'],note:'Returned orders are assumed to lose the shipping, packaging and ad cost, while the product returns to stock.'}};

/* ===== Shopping & Everyday ===== */
function shp(x){return N(x,2)+'%'}
C.discpct=function(v){if(v.orig<=0)return bad('Enter the original price.');var sale,pct;
 if(v.mode==='price'){if(v.sale<0||v.sale>v.orig*1000)return bad();sale=v.sale;pct=(v.orig-sale)/v.orig*100}else{if(v.pct<0||v.pct>100)return bad('Discount must be between 0 and 100%.');pct=v.pct;sale=v.orig*(1-pct/100)}
 return {stats:[S('Discount',shp(pct),1),S('You save',M(v.orig-sale,2)),S('Final price',M(sale,2),1)],bar:[sale,Math.max(v.orig-sale,0),'You pay','You save']}};
C.finalprice=function(v){if(v.price<=0)return bad('Enter the price.');var ds=[v.d1,v.d2,v.d3],p=v.price,rows=[];
 for(var i=0;i<3;i++){if(ds[i]<0||ds[i]>100)return bad('Discounts must be between 0 and 100%.');if(ds[i]>0){var off=p*ds[i]/100;p-=off;rows.push(['Discount '+(i+1)+' ('+ds[i]+'%)','-'+M(off,2),M(p,2)])}}
 var tx=p*v.tax/100,fin=p+tx,tot=v.price-p;
 return {stats:[S('Price after discounts',M(p,2)),S('Tax',M(tx,2)),S('Final price',M(fin,2),1),S('Total saved',M(tot,2)),S('Effective discount',shp(tot/v.price*100))],bar:[p,tot,'You pay','You save'],table:rows.length?{head:['Step','Amount off','Price'],rows:rows}:null}};
C.unitprice=function(v){if(v.p1<=0||v.q1<=0||v.p2<=0||v.q2<=0)return bad('Enter price and quantity for both products.');var a=v.p1/v.q1,b=v.p2/v.q2,w=a<=b?'Product A':'Product B',cheap=Math.min(a,b),dear=Math.max(a,b);
 return {stats:[S('Product A per unit',M(a,4)),S('Product B per unit',M(b,4)),S('Better value',a===b?'Same price':w,1),S('Saving per unit',M(dear-cheap,4)),S('Cheaper by',shp((dear-cheap)/dear*100))],note:'Use the same unit for both quantities, for example grams or millilitres.'}};
C.compare=function(v){var rows=[];for(var i=1;i<=4;i++){if(v['p'+i]>0&&v['q'+i]>0)rows.push({n:i,u:v['p'+i]/v['q'+i],p:v['p'+i],q:v['q'+i]})}
 if(rows.length<2)return bad('Enter price and quantity for at least two products.');var best=rows.slice().sort(function(a,b){return a.u-b.u})[0],worst=rows.slice().sort(function(a,b){return b.u-a.u})[0];
 return {stats:[S('Best value','Product '+best.n,1),S('Lowest price per unit',M(best.u,4)),S('Highest price per unit',M(worst.u,4)),S('Saving vs dearest',shp((worst.u-best.u)/worst.u*100))],
  table:{head:['Product','Price','Quantity','Price per unit','Rank'],rows:rows.map(function(r){var rank=rows.filter(function(x){return x.u<r.u}).length+1;return ['Product '+r.n,M(r.p,2),N(r.q,2),M(r.u,4),String(rank)]})}}};
C.cashback=function(v){if(v.amt<=0||v.pct<0)return bad();var raw=v.amt*v.pct/100,cb=v.cap>0?Math.min(raw,v.cap):raw;
 return {stats:[S('Cashback',M(cb,2),1),S('Effective price',M(v.amt-cb,2)),S('Effective discount',shp(cb/v.amt*100))],note:raw>cb?'The cashback cap limits your reward. Uncapped it would be '+M(raw,2)+'.':''}};
C.tip=function(v){if(v.bill<=0||v.people<1||v.tip<0)return bad('Enter the bill and number of people.');var t=v.bill*v.tip/100,tot=v.bill+t;
 return {stats:[S('Tip',M(t,2)),S('Total bill',M(tot,2),1),S('Per person',M(tot/v.people,2),1),S('Tip per person',M(t/v.people,2))],bar:[v.bill,t,'Bill','Tip']}};
C.split=function(v){if(v.bill<=0||v.people<1)return bad('Enter the bill and number of people.');var tx=v.bill*v.tax/100,tp=v.bill*v.tip/100,tot=v.bill+tx+tp;
 return {stats:[S('Total with tax and tip',M(tot,2)),S('Each person pays',M(tot/v.people,2),1),S('Tax',M(tx,2)),S('Tip',M(tp,2))],bar:[v.bill,tx+tp,'Bill','Tax and tip']}};
C.salestax=function(v){if(v.amt<=0||v.rate<0)return bad();var r=v.rate/100,net,gross;if(v.mode==='add'){net=v.amt;gross=net*(1+r)}else{gross=v.amt;net=gross/(1+r)}
 return {stats:[S('Price before tax',M(net,2)),S('Tax',M(gross-net,2),1),S('Price with tax',M(gross,2),1)],bar:[net,gross-net,'Price','Tax']}};
C.electricity=function(v){var units,rows=[],e;
 if(v.mode==='app'){if(v.watts<=0||v.hrs<=0||v.days<=0)return bad('Enter the appliance power and usage.');units=v.watts*v.hrs*v.days*Math.max(v.qty,1)/1000;e=units*v.rate;
  return {stats:[S('Energy used',N(units,2)+' kWh'),S('Cost',M(e,2),1),S('Cost per day',M(e/v.days,2))]}}
 units=v.units;if(units<=0)return bad('Enter the units consumed.');var s1=v.l1,s2=v.l2,u1=Math.min(units,s1),u2=Math.max(Math.min(units,s2)-s1,0),u3=Math.max(units-s2,0);
 var c1=u1*v.r1,c2=u2*v.r2,c3=u3*v.r3;e=c1+c2+c3;var duty=(e+v.fixed)*v.duty/100,tot=e+v.fixed+duty;
 rows=[['First '+N(s1,0)+' units',N(u1,0),M(v.r1,2),M(c1,2)],['Next '+N(s2-s1,0)+' units',N(u2,0),M(v.r2,2),M(c2,2)],['Above '+N(s2,0),N(u3,0),M(v.r3,2),M(c3,2)]];
 return {stats:[S('Energy charge',M(e,2)),S('Fixed charge',M(v.fixed,2)),S('Duty / tax',M(duty,2)),S('Total bill',M(tot,2),1),S('Average per unit',M(tot/units,2))],table:{head:['Slab','Units','Rate','Amount'],rows:rows},note:'Slab rates differ by state and provider. Edit the rates to match your electricity bill.'}};
C.water=function(v){if(v.kl<=0)return bad('Enter the water used.');var u1=Math.min(v.kl,v.l1),u2=Math.max(Math.min(v.kl,v.l2)-v.l1,0),u3=Math.max(v.kl-v.l2,0),w=u1*v.r1+u2*v.r2+u3*v.r3,sw=w*v.sew/100,tot=w+sw+v.fixed;
 return {stats:[S('Water charge',M(w,2)),S('Sewage charge',M(sw,2)),S('Fixed charge',M(v.fixed,2)),S('Total bill',M(tot,2),1),S('Per kilolitre',M(tot/v.kl,2))],note:'1 kilolitre = 1,000 litres. Rates differ by city, so edit them to match your water bill.'}};
C.fuelcost=function(v){if(v.dist<=0||v.mil<=0||v.price<0)return bad('Enter distance, mileage and fuel price.');var l=v.dist/v.mil,c=l*v.price;
 return {stats:[S('Fuel needed',N(l,2)+' litres'),S('Fuel cost',M(c,2),1),S('Cost per km',M(c/v.dist,2))]}};
C.mileage=function(v){if(v.dist<=0||v.lit<=0)return bad('Enter the distance and fuel used.');var m=v.dist/v.lit,st=[S('Mileage',N(m,2)+' km/l',1),S('Fuel per 100 km',N(100/m,2)+' litres')];
 if(v.price>0){st.push(S('Cost per km',M(v.price*v.lit/v.dist,2)));st.push(S('Cost per 100 km',M(v.price*100/m,2)))}return {stats:st}};
C.travel=function(v){if(v.dist<=0||v.mil<=0)return bad('Enter the distance and mileage.');var f=v.dist/v.mil*v.price,tot=f+v.tolls+v.other,pp=tot/Math.max(v.people,1);
 return {stats:[S('Fuel cost',M(f,2)),S('Tolls and other',M(v.tolls+v.other,2)),S('Total trip cost',M(tot,2),1),S('Per person',M(pp,2),1)],bar:[f,v.tolls+v.other,'Fuel','Tolls and other']}};
var COOK={flour:['All-purpose flour',125],sugar:['Granulated sugar',200],rice:['Rice (uncooked)',185],butter:['Butter',227],milk:['Milk',245],water:['Water',237],oil:['Cooking oil',218],honey:['Honey',340]};
var CU={cup:['cup',236.588],tbsp:['tablespoon',14.787],tsp:['teaspoon',4.929],ml:['millilitre',1],g:['gram',0],oz:['ounce (weight)',0]};
C.cooking=function(v){if(v.amt<=0)return bad('Enter an amount.');var gpc=COOK[v.ing][1],dens=gpc/236.588,toml=function(u,a){return u==='g'?a/dens:u==='oz'?a*28.3495/dens:a*CU[u][1]},ml=toml(v.from,v.amt),
 conv=function(u){return u==='g'?ml*dens:u==='oz'?ml*dens/28.3495:ml/CU[u][1]},out=conv(v.to);
 var rows=['cup','tbsp','tsp','ml','g','oz'].map(function(u){return [CU[u][0],N(conv(u),2)]});
 return {stats:[S(N(v.amt,2)+' '+CU[v.from][0]+' of '+COOK[v.ing][0].toLowerCase(),N(out,2)+' '+CU[v.to][0],1)],table:{head:['Unit','Amount'],rows:rows},note:'Weights are approximate (1 cup of '+COOK[v.ing][0].toLowerCase()+' is about '+gpc+' g) and vary with how the ingredient is packed.'}};

/* ===== Date & Time ===== */
var WD=['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'];
function fdw(d){return WD[d.getDay()]+', '+fdate(d)}
function addMonths(d,n){var y=d.getFullYear(),m=d.getMonth()+n,day=d.getDate();var t=new Date(y,m,1);var last=new Date(t.getFullYear(),t.getMonth()+1,0).getDate();return new Date(t.getFullYear(),t.getMonth(),Math.min(day,last))}
function isoWeek(d){var t=new Date(Date.UTC(d.getFullYear(),d.getMonth(),d.getDate()));var n=t.getUTCDay()||7;t.setUTCDate(t.getUTCDate()+4-n);var y0=new Date(Date.UTC(t.getUTCFullYear(),0,1));return Math.ceil(((t-y0)/864e5+1)/7)}
function dayOfYear(d){return Math.round((new Date(d.getFullYear(),d.getMonth(),d.getDate())-new Date(d.getFullYear(),0,1))/864e5)+1}
function dd(a,b){return Math.round((Date.UTC(b.getFullYear(),b.getMonth(),b.getDate())-Date.UTC(a.getFullYear(),a.getMonth(),a.getDate()))/864e5)}
function vd(s){return s&&!isNaN(pd(s).getTime())}
function plural(n,w){return n+' '+w+(n===1?'':'s')}

C.dcalc=function(v){
 if(!vd(v.s))return bad('Please choose a start date.');
 var sg=v.op==='sub'?-1:1,d=pd(v.s);
 d=addMonths(d,sg*(Math.round(v.y)*12+Math.round(v.m)));d=addDays(d,sg*Math.round(v.d));
 return {stats:[S('Result date',fdate(d),1),S('Weekday',WD[d.getDay()]),S('ISO week number','Week '+isoWeek(d)),S('Day of the year',dayOfYear(d)+' of '+((new Date(d.getFullYear(),1,29).getMonth()===1)?366:365))],
  note:'Start date: '+fdw(pd(v.s))+'.'}};

C.between=function(v){
 if(!vd(v.a)||!vd(v.b))return bad('Please choose both dates.');
 var a=pd(v.a),b=pd(v.b);if(b<a){var t=a;a=b;b=t}
 var days=dd(a,b)+(v.inc?1:0),p=ymd(a,b);
 return {stats:[S('Total days',N(days,0),1),S('Weeks',N(Math.floor(days/7),0)+' weeks '+(days%7)+' days'),S('Years, months, days',p[0]+' y '+p[1]+' m '+p[2]+' d'),S('Total hours',N(days*24,0)),S('Approx. months',N(days/30.4375,1)),S('Weekdays',WD[a.getDay()]+' to '+WD[b.getDay()])],
  note:fdate(a)+' to '+fdate(b)+(v.inc?' (end date included).':'.')}};

function countWork(a,b,weekend){var c=0,d=new Date(a.getTime());while(d<=b){var w=d.getDay(),off=weekend==='ss'?(w===0||w===6):weekend==='s'?w===0:false;if(!off)c++;d.setDate(d.getDate()+1)}return c}
C.working=function(v){
 if(!vd(v.a)||!vd(v.b))return bad('Please choose both dates.');
 var a=pd(v.a),b=pd(v.b);if(b<a){var t=a;a=b;b=t}
 var total=dd(a,b)+1,w=countWork(a,b,v.wk),h=Math.max(0,Math.round(v.h)),net=Math.max(0,w-h);
 return {stats:[S('Working days',N(net,0),1),S('Total days in range',N(total,0)),S('Weekend days',N(total-w,0)),S('Holidays subtracted',N(h,0))],bar:[net,total-net,'Working','Off days'],
  note:fdate(a)+' to '+fdate(b)+', both dates included.'}};

C.bizdays=function(v){
 if(!vd(v.a))return bad('Please choose a start date.');
 var a=pd(v.a);
 if(v.mode==='between'){if(!vd(v.b))return bad('Please choose an end date.');var b=pd(v.b);if(b<a){var t=a;a=b;b=t}
  var w=countWork(a,b,'ss'),h=Math.max(0,Math.round(v.h));
  return {stats:[S('Business days',N(Math.max(0,w-h),0),1),S('Calendar days',N(dd(a,b)+1,0)),S('Weekdays before holidays',N(w,0))],note:fdate(a)+' to '+fdate(b)+', Monday to Friday, both dates included.'}}
 var n=Math.max(0,Math.round(v.n)),sg=v.mode==='sub'?-1:1,d=new Date(a.getTime()),c=0;
 if(n>100000)return bad('Please enter a smaller number.');
 while(c<n){d.setDate(d.getDate()+sg);var w2=d.getDay();if(w2!==0&&w2!==6)c++}
 return {stats:[S('Result date',fdate(d),1),S('Weekday',WD[d.getDay()]),S('Calendar days',N(Math.abs(dd(a,d)),0))],note:plural(n,'business day')+(sg>0?' after ':' before ')+fdate(a)+'.'}};

C.cd=function(v){
 if(!v.t)return bad('Please choose a date and time.');
 var t=new Date(v.t);if(isNaN(t.getTime()))return bad('Please choose a valid date and time.');
 var diff=t-new Date(),past=diff<0;diff=Math.abs(diff);
 var s=Math.floor(diff/1000),d=Math.floor(s/86400),h=Math.floor(s%86400/3600),m=Math.floor(s%3600/60),sec=s%60;
 return {stats:[S('Days',N(d,0),1),S('Hours',h),S('Minutes',m),S('Seconds',sec)],note:past?'This moment passed '+d+' days ago.':'Time remaining until '+t.toLocaleString('en-GB',{dateStyle:'long',timeStyle:'short'})+'.'}};
C.cd.tick=true;

function tmin(s){var p=(s||'').split(':');return (+p[0])*60+(+p[1]||0)}
function hm(m){return Math.floor(m/60)+' h '+pad(m%60)+' min'}
C.dur=function(v){
 if(!v.s||!v.e)return bad('Please enter both times.');
 var a=tmin(v.s),b=tmin(v.e),m=b-a;if(m<0)m+=1440;
 return {stats:[S('Duration',hm(m),1),S('Decimal hours',N(m/60,2)),S('Total minutes',N(m,0))],note:b<a?'The end time is treated as the next day.':''}};

C.hours=function(v){
 if(!v.i||!v.o)return bad('Please enter both times.');
 var a=tmin(v.i),b=tmin(v.o),m=b-a;if(m<0)m+=1440;m-=Math.max(0,v.b);
 if(m<0)return bad('The break is longer than the shift.');
 var d=Math.max(0,v.d),wk=m*d,r=v.r;
 var st=[S('Daily hours',hm(m)+' ('+N(m/60,2)+')',1),S('Weekly hours',hm(wk)+' ('+N(wk/60,2)+')'),S('Monthly (4.33 weeks)',N(wk/60*4.33,1)+' h')];
 if(r>0){st.push(S('Daily pay',M(m/60*r,2)));st.push(S('Weekly pay',M(wk/60*r,2)))}
 return {stats:st}};

C.addsub=function(v){
 if(!vd(v.s))return bad('Please choose a start date.');
 var n=Math.round(v.n)*(v.op==='sub'?-1:1),d=pd(v.s);
 d=v.u==='d'?addDays(d,n):v.u==='w'?addDays(d,7*n):v.u==='m'?addMonths(d,n):addMonths(d,12*n);
 return {stats:[S('New date',fdate(d),1),S('Weekday',WD[d.getDay()]),S('Days from start',N(Math.abs(dd(pd(v.s),d)),0))],note:'Start date: '+fdw(pd(v.s))+'.'}};

function tzOff(tz,utc){var f=new Intl.DateTimeFormat('en-US',{timeZone:tz,hour12:false,year:'numeric',month:'numeric',day:'numeric',hour:'numeric',minute:'numeric',second:'numeric'}).formatToParts(utc),o={};f.forEach(function(p){o[p.type]=+p.value});
 var asUtc=Date.UTC(o.year,o.month-1,o.day,o.hour%24,o.minute,o.second);return asUtc-Math.floor(utc.getTime()/1000)*1000}
function offLabel(ms){var m=Math.round(ms/60000),s=m<0?'-':'+';m=Math.abs(m);return 'UTC'+s+pad(Math.floor(m/60))+':'+pad(m%60)}
function fromZone(dateStr,timeStr,tz){var p=dateStr.split('-'),t=timeStr.split(':'),guess=Date.UTC(+p[0],+p[1]-1,+p[2],+t[0],+t[1]||0);
 var u=new Date(guess-tzOff(tz,new Date(guess)));u=new Date(guess-tzOff(tz,u));return u}
C.tz=function(v){
 if(!vd(v.d)||!v.t)return bad('Please choose a date and time.');
 var u;try{u=fromZone(v.d,v.t,v.f)}catch(e){return bad('This time zone is not supported by your browser.')}
 function show(tz){var o=tzOff(tz,u),loc=new Date(u.getTime()+o);return loc}
 function fmt2(tz){var l=show(tz);return l.getUTCDate()+' '+['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'][l.getUTCMonth()]+' '+l.getUTCFullYear()+', '+pad(l.getUTCHours())+':'+pad(l.getUTCMinutes())}
 var l=show(v.to),sd=pd(v.d),ld=new Date(Date.UTC(l.getUTCFullYear(),l.getUTCMonth(),l.getUTCDate())),dayDiff=Math.round((ld-Date.UTC(sd.getFullYear(),sd.getMonth(),sd.getDate()))/864e5);
 var rows=[['India','Asia/Kolkata'],['UTC','UTC'],['London','Europe/London'],['Dubai','Asia/Dubai'],['Singapore','Asia/Singapore'],['Tokyo','Asia/Tokyo'],['Sydney','Australia/Sydney'],['New York','America/New_York'],['Los Angeles','America/Los_Angeles']].map(function(z){return [z[0],fmt2(z[1]),offLabel(tzOff(z[1],u))]});
 return {stats:[S('Converted time',pad(l.getUTCHours())+':'+pad(l.getUTCMinutes()),1),S('Converted date',fmt2(v.to).split(',')[0]),S('Offset',offLabel(tzOff(v.f,u))+' to '+offLabel(tzOff(v.to,u)))],
  table:{head:['City','Date and time','Offset'],rows:rows},note:dayDiff===0?'Same date in both zones.':dayDiff>0?'The converted time falls on the next day.':'The converted time falls on the previous day.'}};

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

/* ---- construction & property ---- */
var CN_F={ft:1,m:3.280839895,'in':1/12,yd:3},CN_SQM=0.09290304;
function cnArea(sqft){return [S('Square feet',N(sqft),1),S('Square metres',N(sqft*CN_SQM)),S('Square yards (gaj)',N(sqft/9))]}
C.sqft=function(v){var f=CN_F[v.unit],tot=0,rows=[];
 for(var i=1;i<=4;i++){var l=v['l'+i],w=v['w'+i];if(l<0||w<0)return bad();var a=l*f*w*f;tot+=a;if(a>0)rows.push(['Room '+i,N(l)+' x '+N(w),N(a)+' sq ft'])}
 if(tot<=0)return bad('Enter the length and width of at least one room.');
 return {stats:cnArea(tot),table:{head:['Room','Size','Area'],rows:rows}}};
function cnLand(sq){return [S('Square feet',N(sq),1),S('Square metres',N(sq*CN_SQM)),S('Square yards (gaj)',N(sq/9)),S('Acres',N(sq/43560,4)),S('Hectares',N(sq*CN_SQM/10000,4)),S('Guntha',N(sq/1089))]}
C.land=function(v){var u=CN_F[v.unit],a;
 if(v.shape==='rect')a=v.rl*v.rw;else if(v.shape==='tri')a=0.5*v.tb*v.th;else if(v.shape==='trap')a=(v.pa+v.pb)/2*v.ph;else a=Math.PI*v.cr*v.cr;
 var sq=a*u*u;if(!(sq>0))return bad('Enter positive dimensions.');return {stats:cnLand(sq)}};
C.plot=function(v){var u=CN_F[v.unit],sq=v.l*v.w*u*u;if(!(sq>0))return bad('Enter positive dimensions.');
 return {stats:cnArea(sq).concat([S('Cents',N(sq/435.6)),S('Guntha',N(sq/1089)),S('Acres',N(sq/43560,4)),S('Hectares',N(sq*CN_SQM/10000,4))])}};
C.carpet=function(v){if(v.area<=0||v.load<0||v.wall<0)return bad();
 var b,s;if(v.type==='super'){s=v.area;b=s/(1+v.load/100)}else{b=v.area;s=b*(1+v.load/100)}
 var c=b/(1+v.wall/100);
 return {stats:[S('Carpet area',N(c)+' sq ft',1),S('Built-up area',N(b)+' sq ft'),S('Super built-up area',N(s)+' sq ft'),S('Carpet / super built-up',N(c/s*100,1)+'%')],bar:[c,s-c,'Carpet area','Walls and common area'],
  note:'Percentages vary by project. Check the carpet area stated in your sale agreement (RERA).'}};
C.builtup=function(v){if(v.carpet<=0||v.wall<0||v.bal<0||v.load<0)return bad();
 var b=v.carpet*(1+v.wall/100)+v.bal,s=b*(1+v.load/100);
 return {stats:[S('Built-up area',N(b)+' sq ft',1),S('Super built-up area',N(s)+' sq ft'),S('Carpet area',N(v.carpet)+' sq ft'),S('Built-up in sq m',N(b*CN_SQM))]}};
function cnMats(vol,c,s,a,dry,waste){var wv=vol*(1+waste/100),dv=wv*dry,p=c+s+a,cem=dv*c/p,bags=cem*1440/50;
 var st=[S('Wet volume (with wastage)',N(wv)+' m3 ('+N(wv*35.3147)+' cu ft)'),S('Cement',N(Math.ceil(bags))+' bags of 50 kg',1),S('Cement weight',N(cem*1440,0)+' kg'),S('Sand',N(dv*s/p)+' m3 ('+N(dv*s/p*35.3147)+' cu ft)')];
 if(a>0)st.push(S('Aggregate',N(dv*a/p)+' m3 ('+N(dv*a/p*35.3147)+' cu ft)'));return st}
C.cement=function(v){if(v.l<=0||v.w<=0||v.d<=0||v.waste<0)return bad();var m=v.mix.split('|');
 return {stats:cnMats(v.l*v.w*v.d,+m[0],+m[1],+m[2]*(m[2]>0?1:0)||0,+m[3],v.waste),note:'Mix: '+m[4]+'. Dry volume factor '+m[3]+'. Use only as an estimate.'}};
var CN_G={m15:[1,2,4],m20:[1,1.5,3],m25:[1,1,2]};
C.conc=function(v){if(v.l<=0||v.w<=0||v.t<=0||v.n<1||v.waste<0)return bad();var g=CN_G[v.grade];
 return {stats:cnMats(v.l*v.w*v.t*v.n,g[0],g[1],g[2],1.54,v.waste),note:'Nominal mix. Structural work should follow an engineer’s design mix.'}};
C.brick=function(v){var na=v.len*v.ht-v.open;if(v.len<=0||v.ht<=0||na<=0||v.waste<0)return bad('Check the wall size and openings.');
 var k=+v.th,thick=[0,0.09,0.19,0.29][k],bricks=na*50*k,bw=Math.ceil(bricks*(1+v.waste/100)),mortar=na*thick-bricks*0.19*0.09*0.09;
 return {stats:[S('Net wall area',N(na)+' m2'),S('Bricks',N(Math.ceil(bricks),0)),S('Bricks with wastage',N(bw,0),1),S('Wet mortar',N(mortar)+' m3'),S('Cement for 1:4 mortar',N(Math.ceil(mortar*1.33*1/5*1440/50),0)+' bags')]}};
C.paint=function(v){var wall=2*(v.l+v.w)*v.h-v.doors*1.9-v.wins*1.2;if(v.l<=0||v.w<=0||v.h<=0||wall<=0||v.coats<1||v.cov<=0)return bad();
 var area=wall+(v.ceil?v.l*v.w:0),lt=area*v.coats/v.cov;
 return {stats:[S('Paintable area',N(area)+' m2 ('+N(area/CN_SQM)+' sq ft)'),S('Paint needed',N(lt)+' litres',1),S('Suggested (4 L cans)',Math.ceil(lt/4)+' cans'),S('With 5% extra',N(lt*1.05)+' litres')]}};
var CN_T=[];
C.tile=function(v){var d=v.size.split('x'),ta=d[0]*d[1]/92903.04,fa=v.l*v.w;if(fa<=0||v.waste<0||v.box<1)return bad();
 var t=Math.ceil(fa*(1+v.waste/100)/ta);return {stats:[S('Floor area',N(fa)+' sq ft'),S('Tile area',N(ta,3)+' sq ft'),S('Tiles needed',N(t,0),1),S('Boxes',N(Math.ceil(t/v.box),0))]}};
C.floorcost=function(v){if(v.area<=0||v.mat<0||v.lab<0||v.waste<0||v.other<0)return bad();
 var m=v.area*(1+v.waste/100)*v.mat,l=v.area*v.lab,t=m+l+v.other;
 return {stats:[S('Material cost',M(m)),S('Labour cost',M(l)),S('Other costs',M(v.other)),S('Total cost',M(t),1),S('Cost per sq ft',M(t/v.area,2))],bar:[m,l+v.other,'Material','Labour and other']}};
C.cc=function(v){if(v.area<=0||v.floors<1||v.rate<0)return bad();var r=v.rate>0?v.rate:+v.q,t=v.area*v.floors*r;
 var sh=[['Foundation and structure',0.35],['Masonry and plaster',0.15],['Flooring and finishing',0.30],['Electrical and plumbing',0.15],['Other and contingency',0.05]];
 return {stats:[S('Total built-up area',N(v.area*v.floors)+' sq ft'),S('Rate used',M(r)+' per sq ft'),S('Estimated cost',M(t),1),S('Materials (about 60%)',M(t*0.6)),S('Labour (about 40%)',M(t*0.4))],bar:[t*0.6,t*0.4,'Materials','Labour'],
  table:{head:['Stage','Share','Cost'],rows:sh.map(function(x){return [x[0],(x[1]*100)+'%',M(t*x[1])]})},note:'Indicative breakdown only. Excludes land, approvals and interiors.'}};
function cnDuty(v,female){var p=v.state.split('|'),isC=p[0]==='Custom',m=isC?v.cs:+p[1],f=isC?v.cs:+p[2];return {name:p[0],rate:female?f:m,reg:isC?v.cr:+p[3]}}
C.reg=function(v){if(v.val<=0)return bad();var s=cnDuty(v,false),sd=v.val*s.rate/100,rf=v.val*s.reg/100;
 return {stats:[S('Stamp duty ('+N(s.rate)+'%)',M(sd)),S('Registration fee ('+N(s.reg)+'%)',M(rf)),S('Total government cost',M(sd+rf),1),S('As % of property value',N((sd+rf)/v.val*100)+'%')],bar:[sd,rf,'Stamp duty','Registration'],
  note:'Indicative rates for '+esc(s.name)+'. States revise rates and caps often, so confirm with the sub-registrar office.'}};
C.stamp=function(v){if(v.val<=0)return bad();var s=cnDuty(v,v.buyer==='f'),m=cnDuty(v,false),sd=v.val*s.rate/100;
 return {stats:[S('Stamp duty rate',N(s.rate)+'%'),S('Stamp duty',M(sd),1),S('Total with property value',M(v.val+sd)),S('Saving vs male buyer',M(v.val*m.rate/100-sd))],
  note:'Indicative rates for '+esc(s.name)+'. Verify the current rate and any surcharge on the official state website.'}};
C.rent=function(v){
 if(v.mode==='hra'){if(v.basic<=0||v.hra<0||v.paid<0)return bad();var a=v.hra,b=v.paid-0.1*v.basic,c=v.metro*v.basic,e=Math.max(0,Math.min(a,b,c));
  return {stats:[S('Monthly HRA exemption',M(e),1),S('Yearly HRA exemption',M(e*12)),S('Taxable HRA per month',M(Math.max(0,v.hra-e)))],table:{head:['Rule','Monthly amount'],rows:[['HRA received',M(a)],['Rent paid - 10% of basic',M(Math.max(0,b))],[(v.metro==0.5?'50%':'40%')+' of basic',M(c)]]},note:'Applies to the old tax regime only. The lowest of the three amounts is exempt.'}}
 if(v.rent<=0||v.yrs<1||v.inc<0||v.maint<0||v.dep<0)return bad();var rows=[],tr=0,tm=0,r=v.rent,n=Math.min(40,Math.round(v.yrs));
 for(var y=1;y<=n;y++){var yr=r*12;tr+=yr;tm+=v.maint*12;rows.push([y,M(r),M(yr)]);r=r*(1+v.inc/100)}
 return {stats:[S('Total rent over '+n+' years',M(tr),1),S('Total maintenance',M(tm)),S('Rent + maintenance',M(tr+tm)),S('Average per month',M((tr+tm)/(n*12))),S('Refundable deposit',M(v.dep))],table:{head:['Year','Monthly rent','Rent for the year'],rows:rows}}};

/* ---- technology & digital ---- */
function tkTime(sec){sec=Math.round(sec);if(sec<1)return 'under 1 second';var d=Math.floor(sec/86400),h=Math.floor(sec%86400/3600),m=Math.floor(sec%3600/60),s=sec%60,p=[];
 if(d)p.push(d+' d');if(h)p.push(h+' h');if(m&&d<1)p.push(m+' min');if(s&&!d&&!h)p.push(s+' s');return p.join(' ')}
C.inet=function(v){var bps=v.speed*parseFloat(v.u);if(!(bps>0)||v.eff<=0||v.eff>100)return bad('Enter a speed and an efficiency between 1 and 100.');
 var eff=v.eff/100,rows=[['100 MB',100],['1 GB',1000],['4 GB (HD movie)',4000],['50 GB (game)',50000],['1 TB',1e6]].map(function(x){return [x[0],tkTime(x[1]*8e6/(bps*eff))]});
 return {stats:[S('Megabits per second',N(bps/1e6)+' Mbps',1),S('Megabytes per second',N(bps/8e6)+' MB/s'),S('Kilobytes per second',N(bps/8e3,0)+' KB/s'),S('Real-world speed',N(bps*eff/8e6)+' MB/s')],table:{head:['File','Download time'],rows:rows}}};
C.xfer=function(v){var bits=v.size*parseFloat(v.su)*8e6,bps=v.speed*parseFloat(v.u);if(!(bits>0)||!(bps>0)||v.eff<=0||v.eff>100)return bad('Enter a file size, a speed and an efficiency between 1 and 100.');
 return {stats:[S('Estimated time',tkTime(bits/(bps*v.eff/100)),1),S('Ideal time (100%)',tkTime(bits/bps)),S('Effective speed',N(bps*v.eff/100/8e6)+' MB/s'),S('File size',N(v.size*parseFloat(v.su))+' MB')]}};
C.data=function(v){var a=[['Video streaming',v.h1,v.g1],['Video calls',v.h2,v.g2],['Music streaming',v.h3,v.g3],['Browsing and social',v.h4,v.g4]],tot=0,rows=[];
 for(var i=0;i<a.length;i++){if(a[i][1]<0||a[i][2]<0||v.days<1)return bad();var g=a[i][1]*a[i][2]*v.days;tot+=g;rows.push([a[i][0],N(a[i][1]*a[i][2])+' GB / day',N(g)+' GB'])}
 if(tot<=0)return bad('Enter at least one activity.');
 return {stats:[S('Total for '+v.days+' days',N(tot)+' GB',1),S('Per day',N(tot/v.days)+' GB'),S('Suggested plan',tot<=1.5*30?'1.5 GB/day or more':Math.ceil(tot/v.days*10)/10+' GB/day or more')],table:{head:['Activity','Daily','Total'],rows:rows}}};
C.stor=function(v){var b=+v.mode,cap=v.cap*Math.pow(b,v.cu==='2'?2:1),mb=b;if(!(v.cap>0)||v.custom<=0)return bad();
 var capMB=cap*(v.cu==='2'?1:1);if(v.cu==='1')capMB=v.cap*b;else capMB=v.cap*b*b;
 var items=[['Photos (4 MB)',4],['Songs (5 MB)',5],['HD video, 1 hour (3,000 MB)',3000],['4K video, 1 hour (7,000 MB)',7000],['Your files ('+N(v.custom)+' MB)',v.custom]];
 var bytes=capMB*b*b,decGB=bytes/1e9,binGB=bytes/Math.pow(1024,3);
 return {stats:[S('Capacity in MB',N(capMB,0),1),S('In decimal GB',N(decGB)+' GB'),S('In binary GB (GiB)',N(binGB)+' GiB')],table:{head:['Item','How many fit'],rows:items.map(function(x){return [x[0],N(Math.floor(capMB/x[1]),0)]})}}};
function tkParse(s,b){s=String(s).trim().replace(/[\s_,]/g,'');var neg=false;if(s[0]==='-'){neg=true;s=s.slice(1)}
 var re={2:/^(0b)?[01]+$/i,8:/^(0o)?[0-7]+$/i,10:/^\d+$/,16:/^(0x)?[0-9a-f]+$/i}[b];if(!s||!re.test(s))return null;
 var pre={2:'0b',8:'0o',16:'0x'}[b];s=s.replace(/^0[box]/i,'');var n=b===10?BigInt(s):BigInt(pre+s);return neg?-n:n}
function tkGroup(s,n){var neg=s[0]==='-';if(neg)s=s.slice(1);var o=[];for(var i=s.length;i>0;i-=n)o.unshift(s.slice(Math.max(0,i-n),i));return (neg?'-':'')+o.join(' ')}
function tkBases(n){return [S('Decimal',n.toString(10),1),S('Binary',tkGroup(n.toString(2),4)),S('Hexadecimal',n.toString(16).toUpperCase()),S('Octal',n.toString(8))]}
C.b2d=function(v){var n=tkParse(v.val,2);if(n===null)return bad('Enter a binary number using only 0 and 1.');var res={stats:tkBases(n)};
 var s=n.toString(2).replace('-','');if(s.length<=16){var rows=[];for(var i=0;i<s.length;i++){var p=s.length-1-i;rows.push([s[i],'2^'+p,s[i]==='1'?Math.pow(2,p):0])}res.table={head:['Bit','Place value','Adds'],rows:rows}}return res};
C.d2b=function(v){var n=tkParse(v.val,10);if(n===null)return bad('Enter a whole number (digits only, optional minus sign).');var res={stats:tkBases(n)};
 var a=n<0n?-n:n;if(a>0n&&a<4294967296n){var rows=[],q=a;while(q>0n){rows.push([q.toString()+' / 2',(q/2n).toString(),(q%2n).toString()]);q=q/2n}res.table={head:['Division','Quotient','Remainder'],rows:rows}}return res};
C.hexc=function(v){var n=tkParse(v.val,+v.from);if(n===null)return bad('That is not a valid number in the selected base.');return {stats:tkBases(n)}};
C.pw=function(v){var len=Math.max(4,Math.min(128,Math.round(v.len))),sets=[];
 if(v.up)sets.push('ABCDEFGHIJKLMNOPQRSTUVWXYZ');if(v.lo)sets.push('abcdefghijklmnopqrstuvwxyz');if(v.di)sets.push('0123456789');if(v.sy)sets.push('!@#$%^&*()-_=+[]{};:,.?/');
 if(!sets.length)return bad('Select at least one character type.');
 function rnd(n){var lim=Math.floor(4294967296/n)*n,x;do{x=crypto.getRandomValues(new Uint32Array(1))[0]}while(x>=lim);return x%n}
 var pool=sets.join(''),out=[];sets.forEach(function(s){out.push(s[rnd(s.length)])});while(out.length<len)out.push(pool[rnd(pool.length)]);out=out.slice(0,Math.max(len,sets.length));
 for(var i=out.length-1;i>0;i--){var j=rnd(i+1),t=out[i];out[i]=out[j];out[j]=t}
 var bits=out.length*Math.log2(pool.length),label=bits<40?'Weak':bits<60?'Fair':bits<80?'Strong':'Very strong';
 return {stats:[S('Length',out.length+' characters'),S('Entropy',N(bits,0)+' bits'),S('Strength',label,1),S('Character pool',pool.length+' symbols')],blocks:[['Your password',out.join('')]],note:'Generated in your browser. Click the button for a new one.'}};
function tkWords(t){return (t.trim().match(/\S+/g)||[]).length}
function tkMin(w,wpm){var s=Math.round(w/wpm*60);return s<60?s+' sec':Math.floor(s/60)+' min '+(s%60?s%60+' sec':'')}
C.words=function(v){var t=v.t,w=tkWords(t),sent=(t.match(/[^.!?]+[.!?]+(\s|$)|[^.!?]+$/g)||[]).filter(function(x){return /\S/.test(x)}).length,para=t.split(/\n\s*\n/).filter(function(x){return /\S/.test(x)}).length;
 return {stats:[S('Words',N(w,0),1),S('Characters',N(t.length,0)),S('Characters (no spaces)',N(t.replace(/\s/g,'').length,0)),S('Sentences',N(sent,0)),S('Paragraphs',N(para,0)),S('Reading time',tkMin(w,200)),S('Speaking time',tkMin(w,130))]}};
C.chars=function(v){var t=v.t,L=(t.match(/[A-Za-z]/g)||[]),D=(t.match(/\d/g)||[]),cnt={};L.forEach(function(c){c=c.toLowerCase();cnt[c]=(cnt[c]||0)+1});
 var top=Object.keys(cnt).sort(function(a,b){return cnt[b]-cnt[a]}).slice(0,5);
 return {stats:[S('Characters with spaces',N(t.length,0),1),S('Characters without spaces',N(t.replace(/\s/g,'').length,0)),S('Letters',N(L.length,0)),S('Digits',N(D.length,0)),S('Spaces',N((t.match(/ /g)||[]).length,0)),S('Lines',N(t?t.split('\n').length:0,0))],
  table:top.length?{head:['Letter','Count'],rows:top.map(function(c){return [c.toUpperCase(),cnt[c]]})}:null}};
C.read=function(v){var w=v.wc>0?Math.round(v.wc):tkWords(v.t);if(v.wpm<=0)return bad('Enter a reading speed.');if(w<1)return bad('Enter some text or a word count.');
 return {stats:[S('Words',N(w,0)),S('Reading time',tkMin(w,v.wpm),1),S('Speaking time',tkMin(w,130)),S('Pages (about 300 words)',N(w/300,1))]}};
C.tcase=function(v){var t=v.t;if(!t.trim())return bad('Enter some text.');
 var w=t.replace(/([a-z0-9])([A-Z])/g,'$1 $2').split(/[^A-Za-z0-9]+/).filter(Boolean),cap=function(x){return x.charAt(0).toUpperCase()+x.slice(1).toLowerCase()};
 var lower=t.toLowerCase();
 return {blocks:[['UPPERCASE',t.toUpperCase()],['lowercase',lower],['Title Case',lower.replace(/(^|\s)(\S)/g,function(m,a,b){return a+b.toUpperCase()})],['Sentence case',lower.replace(/(^\s*|[.!?]\s+)([a-z])/g,function(m,a,b){return a+b.toUpperCase()})],
  ['camelCase',w.map(function(x,i){return i?cap(x):x.toLowerCase()}).join('')],['PascalCase',w.map(cap).join('')],['snake_case',w.map(function(x){return x.toLowerCase()}).join('_')],['kebab-case',w.map(function(x){return x.toLowerCase()}).join('-')],['CONSTANT_CASE',w.map(function(x){return x.toUpperCase()}).join('_')]]}};
function tkGcd(a,b){return b?tkGcd(b,a%b):a}
C.img=function(v){var w=Math.round(v.w),h=Math.round(v.h);if(w<1||h<1||v.dpi<=0)return bad('Enter positive dimensions and DPI.');var g=tkGcd(w,h),px=w*h,bytes=px*(+v.bpp)/8;
 return {stats:[S('Megapixels',N(px/1e6)+' MP',1),S('Total pixels',N(px,0)),S('Uncompressed size',N(bytes/1e6)+' MB ('+N(bytes/1048576)+' MiB)'),S('Aspect ratio',(w/g)+':'+(h/g)+' ('+N(w/h)+')'),S('Print size',N(w/v.dpi)+' x '+N(h/v.dpi)+' in'),S('Print size (cm)',N(w/v.dpi*2.54)+' x '+N(h/v.dpi*2.54)+' cm')]}};
C.screen=function(v){var w,h;if(v.pre!=='custom'){var p=v.pre.split('x');w=+p[0];h=+p[1]}else{w=Math.round(v.w);h=Math.round(v.h)}if(w<1||h<1||v.diag<=0)return bad('Enter positive values.');
 var g=tkGcd(w,h),d=Math.sqrt(w*w+h*h),ppi=d/v.diag,pw=v.diag*w/d,ph=v.diag*h/d;
 return {stats:[S('Resolution',w+' x '+h),S('Aspect ratio',(w/g)+':'+(h/g)+' ('+N(w/h)+')'),S('Megapixels',N(w*h/1e6)+' MP'),S('Pixel density',N(ppi,1)+' PPI',1),S('Physical size',N(pw)+' x '+N(ph)+' in'),S('Physical size (cm)',N(pw*2.54)+' x '+N(ph*2.54)+' cm'),S('Pixel pitch',N(25.4/ppi,3)+' mm')]}};

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

