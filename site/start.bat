@echo off
rem Starts the quiz on http://localhost:8000 and opens it in your browser.
rem Close this window to stop the server.
cd /d "%~dp0"
echo Quiz running at http://localhost:8000  (close this window to stop)
start "" cmd /c "timeout /t 1 >nul & start http://localhost:8000"
python -m http.server 8000
