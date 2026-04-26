import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


@pytest.fixture
def driver():
    chrome_options = Options()
    chrome_options.add_argument("--window-size=1920,1080")
    try:
        driver = webdriver.Chrome(options=chrome_options)
    except Exception:
        chrome_options.add_argument("--headless=new")
        driver = webdriver.Chrome(options=chrome_options)
    driver.get('https://automationteststore.com/')
    yield driver
    driver.quit()