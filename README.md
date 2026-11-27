# TicketShow — Projeto Final (versão de evolução)

Projeto Flask de venda demonstrativa de ingressos, desenvolvido a partir do PP3.

## O que foi acrescentado nesta versão

* Tema visual escuro em preto/grafite com cartões e sombras.
* Fluxo de recuperação de senha com token assinado e validade de 15 minutos.
* Envio do link por Flask-Mail (requer configuração de e-mail no `.env`).
* Página de clima que exibe dados da API Open-Meteo e trata indisponibilidade.
* Arquivo `.env.example` e configuração inicial do Flake8.

## Executar localmente

1. Crie e ative um ambiente virtual.
2. Instale as dependências: `pip install -r requirements.txt`.
3. Copie `.env.example` para `.env` e preencha as variáveis.
4. Execute `python app.py`.

## Configuração de e-mail

Use uma conta Gmail com senha de app em `MAIL\\\_USERNAME` e `MAIL\\\_PASSWORD`. Nunca envie o `.env` ao GitHub.
Sem essas variáveis, o fluxo de recuperação não conseguirá enviar mensagens.

## API externa

A página `/clima` usa a API Open-Meteo, sem chave, com `requests`, timeout e tratamento de falhas.

## Atenção — pendências obrigatórias antes da entrega

Esta versão ainda utiliza arquivos JSON para usuários e ingressos. O enunciado do Projeto Final exige
Flask-SQLAlchemy; portanto, a migração do armazenamento para banco SQLAlchemy ainda precisa ser feita
antes de considerar o projeto pronto para avaliação.

Também é necessário executar os testes completos, revisar todos os acessos por usuário (incluindo
retornos 403/404), rodar `flake8`, configurar `SECRET\\\_KEY` no PythonAnywhere, publicar o site e criar
uma conta de teste. Não publique dados pessoais ou o arquivo `.env`.

## API permitida pelo enunciado

Open-Meteo (clima), listada na tabela do enunciado do professor.



