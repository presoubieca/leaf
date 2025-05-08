@echo off
echo Starting Python server...
start /B python flask1.py

:wait_loop
timeout /t 1 >nul
curl http://127.0.0.1:5000 >nul 2>&1
if errorlevel 1 (
    goto wait_loop
)

start http://127.0.0.1:5000
