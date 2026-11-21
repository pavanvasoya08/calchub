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
