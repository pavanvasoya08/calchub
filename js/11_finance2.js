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
