from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

driver.get("http://127.0.0.1:5000/login")

driver.find_element(By.NAME, "username").send_keys("testuser")
driver.find_element(By.NAME, "password").send_keys("password123")
driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

time.sleep(1)

assert "Dashboard" in driver.page_source

print("Login test passed!")

driver.quit()
