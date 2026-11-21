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
