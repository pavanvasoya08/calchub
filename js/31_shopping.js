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
