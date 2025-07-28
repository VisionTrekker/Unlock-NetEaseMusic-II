# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "008776F2D3B0F3B6ED29F2EFDCEDE63867C374C77F2FA386E9AF272A3F6D7211FBECFBC18DBF4BD3E6263FB6C251BBF16DCA787CD4C88EB2D921D25DC8D0F8D4854655ABD3212E46C3156E334BBFEA1CD503CD04C143AECC0D7AF29A08A119CDE3D63446E958D7D139C7CBDEF428FCF3E5C2580034C32F979466F97F99FC45B4ACF90B3340BE7FA5022420D5224D8AD4DF527E00C97FB06BA0B0611A40DEF97CC105C0C61A25F5E5DFE5C4252C5DF82D62B8DC5AA3E050FB521A36B166501D42FBC2FFAD65EDF3F8712C21C7F172CBFE688F4D52F010C7AF7BB1EED30B1E9C35EBF8CA40B19573DB587C5A643B82ECB4B06067B6AFE7BFB15A49C61C4696302CFCCB7EBDE1A2F9A71957B36A34A7C34A63FE5B8E8428AB8B53F66A071F3D0454185A3AA7B35344246024AEC60995147E45BE90FC874FB28778AEA8AC9D2D74FE9BC393A614DA3CEEDE40E2603EE8CD72911BCEE0236C05D18DC2EBE90AA960404BCF9349A910B3B2F5873C4D693FF4A2270C193729B3803A18A8006EDA943DB5B75C708DBA3E0E7DFDA93FF8BB00D29478"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
