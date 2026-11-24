'use strict';
(function(){
 const menu=document.getElementById('mobileMenu'); const nav=document.getElementById('ts-navigation');
 menu?.addEventListener('click',()=>{const expanded=menu.getAttribute('aria-expanded')==='true';menu.setAttribute('aria-expanded',String(!expanded));nav?.classList.toggle('is-open',!expanded);});
 const trigger=document.getElementById('categoriesTrigger'); const panel=document.getElementById('categoriesMenu');
 trigger?.addEventListener('click',()=>{const isOpen=trigger.getAttribute('aria-expanded')==='true';trigger.setAttribute('aria-expanded',String(!isOpen));panel?.classList.toggle('is-open',!isOpen);});
 document.addEventListener('click',e=>{if(trigger&&!trigger.parentElement.contains(e.target)){panel?.classList.remove('is-open');trigger.setAttribute('aria-expanded','false');}});
 const searchToggle=document.getElementById('searchToggle'), searchForm=document.getElementById('quickSearch'), searchInput=document.getElementById('searchInput'), grid=document.getElementById('eventGrid'), empty=document.getElementById('emptySearch');
 searchToggle?.addEventListener('click',()=>{searchForm.hidden=!searchForm.hidden;if(!searchForm.hidden)searchInput?.focus();});
 function runSearch(){if(!grid)return;const query=(searchInput?.value||'').trim().toLocaleLowerCase('pt-BR');const cards=Array.from(grid.querySelectorAll('.ts-event-card'));let count=0;cards.forEach(card=>{const match=!query||(card.dataset.search||'').includes(query);card.hidden=!match;if(match)count++;});if(empty)empty.hidden=count!==0||!cards.length;}
 searchInput?.addEventListener('input',runSearch);searchForm?.addEventListener('submit',e=>{e.preventDefault();runSearch();document.getElementById('eventos')?.scrollIntoView({behavior:'smooth'});});
})();
