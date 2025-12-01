import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pytest

@pytest.fixture(scope='module')
def driver():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()

def test_submit_message(driver):
    driver.get("http://host.docker.internal:5000/")
    username = driver.find_element(By.NAME, "username")
    message = driver.find_element(By.NAME, "message")
    username.clear(); username.send_keys("selenium")
    message.clear(); message.send_keys("hello from selenium")
    message.submit()
    time.sleep(1)
    assert "Message submitted" in driver.page_source or "hello from selenium" in driver.page_source
