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
