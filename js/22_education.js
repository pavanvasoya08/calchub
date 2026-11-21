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
