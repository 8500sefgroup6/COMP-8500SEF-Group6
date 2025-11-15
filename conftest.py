import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from app import app, db, MenuItem
import os
import subprocess
from datetime import datetime
import time

if not os.path.exists("screenshots"):
    os.makedirs("screenshots")

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    driver = item.funcargs.get("selenium_driver")
    if driver:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"screenshots/{item.name}_{timestamp}.png"
        for _ in range(3):  
            try:
                driver.save_screenshot(screenshot_path)
                break
            except Exception:
                time.sleep(1)
        if os.path.exists(screenshot_path):
            try:
                from pytest_html import extras
                if hasattr(outcome.get_result(), 'extra'):
                    outcome.get_result().extra.append(extras.image(screenshot_path, mime_type='image/png'))
            except ImportError:
                pass
            try:
                from allure import attach, attachment_type
                with open(screenshot_path, "rb") as f:
                    attach(f.read(), name=f"{item.name}_{timestamp}", attachment_type=attachment_type.PNG)
            except ImportError:
                pass

@pytest.fixture(scope="session")
def flask_server():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['SERVER_NAME'] = '127.0.0.1:5000'
    process = subprocess.Popen(
        ["flask", "run", "--host=127.0.0.1", "--port=5000"],
        env={**os.environ, "FLASK_APP": "app.py"},
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    yield
    process.terminate()

@pytest.fixture(scope="session")
def selenium_driver(flask_server):
    chrome_options = Options()
    chrome_options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(10)
    driver.get("http://127.0.0.1:5000")
    yield driver
    driver.quit()

@pytest.fixture
def init_db(flask_server):
    with app.app_context():
        db.create_all()
        sample_menu = [
            {"name": "Margherita Pizza", "description": "Classic tomato, mozzarella, basil", "price_cents": 8800, "image_url": "images/pizza.jpg"},
            {"name": "Pepperoni Pizza", "description": "Pepperoni, mozzarella, tomato", "price_cents": 9800, "image_url": "images/pepperoni.jpg"},
            {"name": "Chicken Katsu Bento", "description": "Crispy chicken, rice, salad", "price_cents": 10500, "image_url": "images/bento.jpg"},
            {"name": "Sushi Set", "description": "Assorted nigiri & rolls", "price_cents": 12800, "image_url": "images/sushi.jpg"},
            {"name": "Ramen Tonkotsu", "description": "Pork broth, chashu, egg", "price_cents": 9200, "image_url": "images/ramen.jpg"},
            {"name": "Curry Rice", "description": "Japanese curry with veggies", "price_cents": 7800, "image_url": "images/curry.jpg"},
        ]
        if not MenuItem.query.first():
            for m in sample_menu:
                db.session.add(MenuItem(**m))
            db.session.commit()
        yield
        db.drop_all()