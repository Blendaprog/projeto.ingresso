"use strict";
async function carregarClima(){
 const cidade=document.getElementById("climaCidade"), temp=document.getElementById("climaTemperatura"), desc=document.getElementById("climaDescricao");
 if(!cidade||!temp||!desc)return;
 desc.textContent="Consultando...";
 try{
   const resposta=await fetch("/api/clima",{headers:{"Accept":"application/json"}});
   if(!resposta.ok)throw new Error("Serviço indisponível");
   const dados=await resposta.json();
   cidade.textContent=dados.cidade;
   temp.textContent=Number(dados.temperatura).toFixed(1).replace(".",",")+" °C";
   desc.textContent=dados.descricao+" · vento "+Number(dados.vento).toFixed(0)+" km/h";
 }catch(_){temp.textContent="-- °C";desc.textContent="Clima indisponível no momento.";}
}
function configurarCep(){
 const form=document.getElementById("formCep");if(!form)return;
 const campo=document.getElementById("cepInput"), status=document.getElementById("cepStatus"), resultado=document.getElementById("cepResultado");
 campo.addEventListener("input",()=>{let v=campo.value.replace(/\D/g,"").slice(0,8);campo.value=v.length>5?v.slice(0,5)+"-"+v.slice(5):v;});
 form.addEventListener("submit",async e=>{
  e.preventDefault();resultado.hidden=true;
  const cep=campo.value.replace(/\D/g,"");
  if(cep.length!==8){status.textContent="Digite um CEP com exatamente 8 números.";return;}
  status.textContent="Buscando endereço...";
  try{
    const r=await fetch("/api/cep/"+cep,{headers:{"Accept":"application/json"}});
    const d=await r.json();
    if(!r.ok){status.textContent=d.erro||"Não foi possível consultar o CEP.";return;}
    for(const [id,key] of [["rCep","cep"],["rRua","logradouro"],["rBairro","bairro"],["rCidade","cidade"],["rUf","uf"]])document.getElementById(id).textContent=d[key]||"Não informado";
    resultado.hidden=false;status.textContent="Endereço encontrado com sucesso.";
  }catch(_){status.textContent="Serviço indisponível. Tente novamente mais tarde.";}
 });
}
document.addEventListener("DOMContentLoaded",()=>{
 carregarClima();configurarCep();
 document.getElementById("atualizarClima")?.addEventListener("click",carregarClima);
});
