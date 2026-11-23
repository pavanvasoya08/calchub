(function(){
var f=document.getElementById('ask-form');if(!f)return;
var ENDPOINT=f.dataset.endpoint,msg=document.getElementById('ask-msg'),btn=f.querySelector('button[type=submit]'),q=document.getElementById('ask-question'),cnt=document.getElementById('ask-count');
var started=Date.now(),busy=false;
function uuid(){try{return crypto.randomUUID()}catch(e){return 'x'+Date.now().toString(36)+Math.random().toString(36).slice(2,12)}}
var token=uuid();
function show(kind,text){msg.className='msg '+kind;msg.hidden=false;msg.innerHTML=kind==='load'?'<span class="spin"></span>':'';msg.appendChild(document.createTextNode(text))}
function val(id){return (document.getElementById(id).value||'').replace(/\s+/g,' ').trim()}
q.addEventListener('input',function(){cnt.textContent=q.value.length+' / 1000'});
f.addEventListener('submit',function(ev){
 ev.preventDefault();if(busy)return;
 var name=val('ask-name'),email=val('ask-email').toLowerCase(),cat=document.getElementById('ask-cat').value,question=q.value.trim();
 if(name.length<2)return show('err','Please enter your name.');
 if(!/^[^\s@]+@[^\s@]+\.[A-Za-z]{2,}$/.test(email))return show('err','Please enter a valid email address.');
 if(!cat)return show('err','Please choose a question category.');
 if(question.length<10)return show('err','Please write your question (at least 10 characters).');
 if(question.length>1000)return show('err','Your question is too long (maximum 1000 characters).');
 if(!ENDPOINT||ENDPOINT.indexOf('PASTE_')>-1)return show('err','This form is not connected yet. Please try again later.');
 busy=true;btn.disabled=true;btn.textContent='Sending...';show('load','Sending your question...');
 var payload=JSON.stringify({name:name,email:email,category:cat,question:question,calculator:f.dataset.calc,url:f.dataset.url,website:document.getElementById('ask-web').value,elapsed:Math.round((Date.now()-started)/1000),token:token});
 function fail(t){show('err',t);btn.textContent='Send question';btn.disabled=false}
 function done(text){show('ok',text);f.reset();cnt.textContent='0 / 1000';token=uuid();started=Date.now();btn.textContent='Question sent';setTimeout(function(){btn.textContent='Send question';btn.disabled=false},8000)}
 function post(opts){var ctl=window.AbortController?new AbortController():null,t=setTimeout(function(){if(ctl)ctl.abort()},20000);
  opts.method='POST';opts.headers={'Content-Type':'text/plain;charset=utf-8'};opts.body=payload;opts.redirect='follow';if(ctl)opts.signal=ctl.signal;
  return fetch(ENDPOINT,opts).then(function(r){clearTimeout(t);return r},function(e){clearTimeout(t);throw e})}
 post({}).then(function(r){return r.json()}).then(function(d){
   if(d&&d.ok)done(d.message||'Thank you! Your question has been received.');else fail((d&&d.error)||'Something went wrong. Please try again.')
  },function(){
   /* the reply could not be read (browser CORS/redirect quirk). Send once more without reading the reply; the server ignores repeats of the same submit token. */
   post({mode:'no-cors'}).then(function(){done('Thank you! Your question has been sent.')},function(){fail('Could not send your question. Please check your connection and try again.')})
  }).then(function(){busy=false});
});
})();
