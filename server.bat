@echo off
echo ========================================
echo   SoftDesk API Server
echo ========================================
echo.
echo Starting server at http://127.0.0.1:8000/
echo Press Ctrl+C to stop the server
echo.
echo Opening API interface in browser...
timeout /t 3 /nobreak > nul
start http://127.0.0.1:8000/admin/
poetry run python manage.py runserver
pause
