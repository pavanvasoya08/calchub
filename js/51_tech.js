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
