(function(){
"use strict";
var B=document.body,CUR=B.dataset.cur||'₹',LOC=B.dataset.loc||'en-IN';
var byId=function(i){return document.getElementById(i)};

/* ============ helpers available to every calculator function (C.<name>) ============
 M(n,d)    money   "₹1,23,456"        N(n,d) plain number "1,234.56" (d = max decimals, default 2)
 S(label,value,highlight)  one result tile      bad(msg)  validation error {err}
 emiOf(P,i,m)  EMI for principal P, monthly rate i (decimal), m months
 pd('YYYY-MM-DD') -> local Date     fdate(Date) -> "20 November 2026"     addDays(Date,n)
 ymd(a,b) -> [years,months,days] between two Dates      nums(text) -> array of numbers or null
 pad(n) -> two digits      esc(s) -> html-escaped text
 A calculator function receives v (values by field id: number inputs -> numbers (empty = 0),
 checkbox -> true/false, everything else -> string) and returns ONE of:
   {err:'message'}  or  {stats:[S(..),..], bar:[a,b,'labelA','labelB'], table:{head:[..],rows:[[..]]},
                         note:'text', blocks:[['Label','text to show in a copyable box'],..]}
 Optional properties on the function: C.x.tick=true (re-run every second), C.x.init=function(box,run){...}
*/
function M(n,d){d=d||0;return isFinite(n)?CUR+n.toLocaleString(LOC,{minimumFractionDigits:d,maximumFractionDigits:d}):'—'}
function N(n,d){d=d==null?2:d;return isFinite(n)?n.toLocaleString(LOC,{maximumFractionDigits:d}):'—'}
function S(l,v,h){return [l,v,!!h]}
function bad(m){return {err:m||'Please enter valid values.'}}
function emiOf(P,i,m){return i===0?P/m:P*i*Math.pow(1+i,m)/(Math.pow(1+i,m)-1)}
function pd(s){return new Date(s+'T00:00:00')}
function pad(n){return (n<10?'0':'')+n}
function esc(s){return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;')}
function fdate(d){return d.toLocaleDateString('en-GB',{day:'numeric',month:'long',year:'numeric'})}
function addDays(d,n){var x=new Date(d.getTime());x.setDate(x.getDate()+n);return x}
function nums(s){var a=(s||'').split(/[\s,;]+/).filter(Boolean).map(Number);return a.some(isNaN)?null:a}
function ymd(a,b){var y=b.getFullYear()-a.getFullYear(),m=b.getMonth()-a.getMonth(),d=b.getDate()-a.getDate();
 if(d<0){m--;d+=new Date(b.getFullYear(),b.getMonth(),0).getDate()}if(m<0){y--;m+=12}return [y,m,d]}

var C={};
