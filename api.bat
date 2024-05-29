@echo off

rem Starten Sie die Docker-Container
:start
if "%1"=="start" (
    docker compose up -d
    exit /b
)

rem Stoppen Sie die Docker-Container
:stop
if "%1"=="stop" (
    docker compose down
    docker rmi imagename
    exit /b
)

rem Fehlermeldung für ungültige Befehle
echo Ungültiger Befehl: Verwenden Sie 'api start' oder 'api stop'
