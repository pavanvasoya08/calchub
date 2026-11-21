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
