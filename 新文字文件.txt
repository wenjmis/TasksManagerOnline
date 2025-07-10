@echo off

echo activating Flask backend
start "Flask Backend" cmd /k "CALL C:\Users\32919\Anaconda3\Scripts\activate.bat && conda activate vue-flask-env && cd /d %~dp0backend && python app.py"

echo Activating NPM frontend
start "Vue Frontend" cmd /k "cd /d %~dp0frontend && npm run serve"

echo Services Activated...
pause