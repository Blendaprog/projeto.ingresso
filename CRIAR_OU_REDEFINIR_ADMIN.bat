@echo off
setlocal
cd /d "%~dp0"
title TicketShow - configurar administrador
echo Pasta: %CD%
if exist ".venv\Scripts\python.exe" (
  ".venv\Scripts\python.exe" -m flask --app app criar-admin
) else (
  python -m flask --app app criar-admin
)
if errorlevel 1 echo Se houver erro, instale as dependencias com INICIAR_TICKETSHOW.bat primeiro.
pause
endlocal
