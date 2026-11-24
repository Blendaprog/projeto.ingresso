'use strict';
(function(){
const sidebar=document.getElementById('admSidebar'),menu=document.getElementById('admMenu');
menu?.addEventListener('click',()=>{const opened=sidebar?.classList.toggle('opened');menu.setAttribute('aria-expanded',String(!!opened));});
const list=document.getElementById('admEventList'),search=document.getElementById('adminSearch'),category=document.getElementById('adminCategory'),sort=document.getElementById('adminSort'),counter=document.getElementById('admCount'),empty=document.getElementById('admEmpty');
function applyFilters(){if(!list)return;const q=(search?.value||'').toLocaleLowerCase('pt-BR').trim(),cat=(category?.value||'').toLocaleLowerCase('pt-BR');const rows=Array.from(list.querySelectorAll('.adm-event-row'));const method=sort?.value||'recente';rows.sort((a,b)=>method==='nome'?a.dataset.name.localeCompare(b.dataset.name,'pt-BR'):method==='data'?a.dataset.date.localeCompare(b.dataset.date):method==='estoque'?Number(a.dataset.stock)-Number(b.dataset.stock):Number(b.dataset.id)-Number(a.dataset.id));let visible=0;rows.forEach(row=>{const show=(!q||(row.dataset.search||'').includes(q))&&(!cat||row.dataset.category===cat);row.hidden=!show;if(show)visible++;list.appendChild(row);});if(counter)counter.textContent=`${visible} evento${visible===1?'':'s'} encontrado${visible===1?'':'s'}`;if(empty)empty.hidden=visible!==0;}
[search,category,sort].forEach(el=>el?.addEventListener(el===search?'input':'change',applyFilters));applyFilters();
document.addEventListener('click',ev=>{if(!ev.target.closest('.adm-row-menu'))document.querySelectorAll('.adm-row-menu[open]').forEach(el=>el.open=false);});
})();
