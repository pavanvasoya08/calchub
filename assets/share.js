(function(){
var box=document.querySelector('.share');if(!box)return;
var msg=box.querySelector('.msg'),url=box.dataset.url,title=box.dataset.title,text=box.dataset.text;
function say(t){msg.textContent=t;clearTimeout(say.t);say.t=setTimeout(function(){msg.textContent=''},2500)}
var ns=box.querySelector('.ns');
if(navigator.share){ns.hidden=false;ns.addEventListener('click',function(){navigator.share({title:title,text:text,url:url}).catch(function(){})})}
box.querySelector('.cp').addEventListener('click',function(){
 function fb(){var ta=document.createElement('textarea');ta.value=url;ta.style.position='fixed';ta.style.opacity='0';document.body.appendChild(ta);ta.select();var ok=false;try{ok=document.execCommand('copy')}catch(e){}ta.remove();say(ok?'Link copied to clipboard':'Could not copy. Please copy the address bar link.')}
 if(navigator.clipboard&&window.isSecureContext)navigator.clipboard.writeText(url).then(function(){say('Link copied to clipboard')},fb);else fb()});
})();
