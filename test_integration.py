import pytest
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from app import app, db, MenuItem, Order
import time
import os
from datetime import datetime

@allure.step("將食物加入購物車")
def add_to_cart(selenium_driver, item_to_add, base_url):
    selenium_driver.get(f"{base_url}/menu")
    WebDriverWait(selenium_driver, 15).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "h2"))
    )
    qty_input = selenium_driver.find_element(By.CSS_SELECTOR, f"form[action='/add_to_cart/{item_to_add.id}'] input[name='qty']")
    qty_input.clear()
    qty_input.send_keys("2")
    submit_button = qty_input.find_element(By.XPATH, "./ancestor::form").find_element(By.CSS_SELECTOR, "button[type='submit']")
    submit_button.click()
    WebDriverWait(selenium_driver, 15).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "h2"))
    )
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    screenshot_path = f"screenshots/add_to_cart_{timestamp}.png"
    selenium_driver.save_screenshot(screenshot_path)
    if os.path.exists(screenshot_path):
        with open(screenshot_path, "rb") as f:
            allure.attach(f.read(), name=f"add_to_cart_{timestamp}", attachment_type=allure.attachment_type.PNG)

@allure.step("檢查購物車內容")
def check_cart(selenium_driver, item_to_add, base_url):
    selenium_driver.get(f"{base_url}/cart")
    time.sleep(1)
    WebDriverWait(selenium_driver, 15).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".cart-table td"))
    )
    page_source = selenium_driver.page_source
    assert item_to_add.name in page_source, f"'{item_to_add.name}' not in cart"
    assert "2" in page_source, "Quantity '2' not in cart"
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    screenshot_path = f"screenshots/check_cart_{timestamp}.png"
    selenium_driver.save_screenshot(screenshot_path)
    if os.path.exists(screenshot_path):
        with open(screenshot_path, "rb") as f:
            allure.attach(f.read(), name=f"check_cart_{timestamp}", attachment_type=allure.attachment_type.PNG)

@allure.step("結帳並送出訂單")
def checkout(selenium_driver, base_url):
    selenium_driver.get(f"{base_url}/checkout")
    WebDriverWait(selenium_driver, 15).until(
        EC.presence_of_element_located((By.ID, "customer_name"))
    )
    selenium_driver.find_element(By.ID, "customer_name").send_keys("Test User")
    selenium_driver.find_element(By.ID, "customer_phone").send_keys("1234567890")
    selenium_driver.find_element(By.ID, "customer_address").send_keys("123 Test Street")
    selenium_driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    WebDriverWait(selenium_driver, 15).until(
        EC.url_contains("/my_orders")
    )
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    screenshot_path = f"screenshots/checkout_{timestamp}.png"
    selenium_driver.save_screenshot(screenshot_path)
    if os.path.exists(screenshot_path):
        with open(screenshot_path, "rb") as f:
            allure.attach(f.read(), name=f"checkout_{timestamp}", attachment_type=allure.attachment_type.PNG)

@allure.step("驗證訂單")
def verify_order(selenium_driver, item_to_add, base_url):
    selenium_driver.get(f"{base_url}/my_orders")
    WebDriverWait(selenium_driver, 15).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "td"))
    )
    page_source = selenium_driver.page_source
    assert "Test User" in page_source, "'Test User' not in my orders"
    with app.app_context():
        order = Order.query.filter_by(customer_name='Test User').first()
        assert order, "Order not found in database"
        assert order.total_cents == item_to_add.price_cents * 2, "Order total mismatch"
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    screenshot_path = f"screenshots/verify_order_{timestamp}.png"
    selenium_driver.save_screenshot(screenshot_path)
    if os.path.exists(screenshot_path):
        with open(screenshot_path, "rb") as f:
            allure.attach(f.read(), name=f"verify_order_{timestamp}", attachment_type=allure.attachment_type.PNG)

@allure.step("追蹤訂單")
def track_order(selenium_driver, item_to_add, base_url):
    with app.app_context():
        order = Order.query.filter_by(customer_name='Test User').first()
        assert order, "Order not found for tracking"
        selenium_driver.get(f"{base_url}/order/{order.id}")
        WebDriverWait(selenium_driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "p, h2, li"))
        )
        page_source = selenium_driver.page_source
        assert "Test User" in page_source, "'Test User' not in order tracking page"
        assert order.status.value.replace('_', ' ').title() in page_source, f"Order status '{order.status.value.replace('_', ' ').title()}' not in order tracking page"
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"screenshots/track_order_{timestamp}.png"
        selenium_driver.save_screenshot(screenshot_path)
        if os.path.exists(screenshot_path):
            with open(screenshot_path, "rb") as f:
                allure.attach(f.read(), name=f"track_order_{timestamp}", attachment_type=allure.attachment_type.PNG)

@allure.step("管理員更新訂單狀態並再次追蹤")
def update_and_track_order(selenium_driver, item_to_add, base_url):
    with app.app_context():
        order = Order.query.filter_by(customer_name='Test User').first()
        assert order, "Order not found for status update"
        # 訪問管理員頁面
        selenium_driver.get(f"{base_url}/admin")
        WebDriverWait(selenium_driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "select[name='status']"))
        )
        # 找到對應訂單的狀態選擇框
        status_select = selenium_driver.find_element(By.CSS_SELECTOR, f"form[action='/admin/update_status/{order.id}'] select[name='status']")
        status_select.send_keys("preparing")
        submit_button = status_select.find_element(By.XPATH, "./ancestor::form").find_element(By.CSS_SELECTOR, "button[type='submit']")
        submit_button.click()
        WebDriverWait(selenium_driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "h2"))
        )
        # 再次訪問訂單追蹤頁面
        selenium_driver.get(f"{base_url}/order/{order.id}")
        WebDriverWait(selenium_driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "p, h2, li"))
        )
        page_source = selenium_driver.page_source
        assert "Test User" in page_source, "'Test User' not in order tracking page after status update"
        assert "Preparing" in page_source, "Order status 'Preparing' not in order tracking page after update"
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"screenshots/update_and_track_order_{timestamp}.png"
        selenium_driver.save_screenshot(screenshot_path)
        if os.path.exists(screenshot_path):
            with open(screenshot_path, "rb") as f:
                allure.attach(f.read(), name=f"update_and_track_order_{timestamp}", attachment_type=allure.attachment_type.PNG)

def test_full_order_workflow(selenium_driver, init_db):
    base_url = "http://127.0.0.1:5000"
    with app.app_context():
        item_to_add = MenuItem.query.filter_by(name="Margherita Pizza").first()
        assert item_to_add, "No menu items found"
    add_to_cart(selenium_driver, item_to_add, base_url)
    check_cart(selenium_driver, item_to_add, base_url)
    checkout(selenium_driver, base_url)
    verify_order(selenium_driver, item_to_add, base_url)
    track_order(selenium_driver, item_to_add, base_url)
    update_and_track_order(selenium_driver, item_to_add, base_url)