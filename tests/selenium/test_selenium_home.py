import time
from selenium import webdriver
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

def test_homepage_loads(driver):
    driver.get("http://host.docker.internal:5000/")  # in Docker use host.docker.internal; Jenkins host may differ
    assert "Submit a Message" in driver.page_source
