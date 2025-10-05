@echo off
echo Stopping Flask server...

REM Kill python processes running app.py
taskkill /F /IM python.exe /FI "WINDOWTITLE eq C:\Users\lyjia\Desktop\FOOD\food_ordering_app\food_ordering_app\app.py*" >nul 2>&1

REM If above doesn't work, kill any python.exe listening on port 5000
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :5000 ^| findstr LISTENING') do taskkill /F /PID %%a

echo Flask server stopped.
pause
