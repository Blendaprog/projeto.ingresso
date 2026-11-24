@echo off
setlocal
cd /d "%~dp0"
title TicketShow VERIFICADO - iniciar
cls
echo ==========================================================
echo TICKETSHOW - CHECKOUT CORRIGIDO - INICIAR
 echo Pasta correta: %CD%
echo ==========================================================
if not exist ".venv\Scripts\python.exe" (
  echo Criando ambiente Python...
  python -m venv .venv
  if errorlevel 1 goto erro
)
if not exist ".venv\dependencias_ok.txt" (
  echo Instalando bibliotecas do projeto...
  ".venv\Scripts\python.exe" -m pip install -r requirements.txt
  if errorlevel 1 goto erro
  echo ok>".venv\dependencias_ok.txt"
)
echo.
echo Conferindo o sistema antes de iniciar...
".venv\Scripts\python.exe" TESTAR_SISTEMA.py
if errorlevel 1 goto erro
echo.
echo Acesse: http://127.0.0.1:5000
".venv\Scripts\python.exe" app.py
if errorlevel 1 goto erro
goto fim
:erro
echo.
echo [ERRO] A inicializacao falhou. Copie o texto acima para verificar.
pause
:fim
endlocal
