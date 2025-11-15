@echo off
cd /d C:\Users\lyjia\Desktop\FOOD\food_ordering_app\food_ordering_app

REM Create virtual environment if not exists
if not exist .venv (
    echo Creating virtual environment...
    python -m venv .venv
)

REM Activate virtual environment
call .venv\Scripts\activate

REM Install required packages
pip install flask flask-sqlalchemy

REM Install other dependencies if requirements.txt exists
if exist requirements.txt (
    pip install -r requirements.txt
)

REM Initialize database if not exists
if not exist food.db (
    python db_init.py
)

REM Start Flask app
start "" http://127.0.0.1:5000
python app.py

pause
