@echo off
TITLE IntelliCourse AI Platform Launcher
COLOR 0A

echo ===================================================
echo        INTELLICOURSE AI PLATFORM LAUNCHER          
echo ===================================================
echo.

cd /d "%~dp0"

IF EXIST "venv\Scripts\activate.bat" (
    echo Activating Python Virtual Environment...
    call venv\Scripts\activate.bat
) ELSE (
    echo [INFO] Virtual environment not found, using global Python installation...
)

echo.
echo Launching Web Browser at http://127.0.0.1:8000/ ...
start "" "http://127.0.0.1:8000/"

echo.
echo Starting Django REST Framework Backend Server...
echo Press Ctrl+C in this window to stop the server.
echo.

python manage.py runserver 127.0.0.1:8000

pause
