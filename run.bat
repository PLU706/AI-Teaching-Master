@echo off
title AI Teaching Program - Server Running
color 0A
echo ========================================
echo    DO NOT CLOSE THIS WINDOW
echo    The server is running on localhost:5000
echo ========================================

start http://localhost:5000/login

python app.py

if %errorlevel% neq 0 (
    echo An error occurred while running the server.
    echo Error code: %errorlevel%
    pause
    exit /b %errorlevel%
)

pause
