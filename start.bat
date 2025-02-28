@echo off
echo Starting Python server...
start /B python flask1.py
timeout /t 20 /nobreak >nul 2>&1
start http://127.0.0.1:5000
