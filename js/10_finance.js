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
