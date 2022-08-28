import json
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from stem import Signal
from stem.control import Controller

controller_ip = "172.0.0.1"
controller_port = 9051
controller_pass = "admin"
url_test = "https://check.torproject.org/api/ip"
selenium_remote_url = "http://127.0.0.1:4444/wd/hub"


def get_chrome_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--proxy-server=socks5://tor:9050')
    driver = webdriver.Remote(selenium_remote_url, options=options)
    return driver


def get_url(url: str, driver: webdriver) -> webdriver:
    error_msg = "You have reached your query limit on bgp.he.net."
    try:
        driver.get(url)
        data = driver.page_source

        if error_msg in data:
            # get_new_tor_ip(driver)
            driver.quit()
            driver = get_chrome_driver()
            return get_url(url, driver)

        return driver
    except Exception as e:
        print(e)


def get_tor_controller():
    controller = Controller.from_port(port=9051)
    controller.authenticate(password=controller_pass)
    print("Tor version " + str(controller.get_version()) + " connected")
    return controller


def get_current_tor_ip(driver: webdriver):
    driver.get("https://check.torproject.org/api/ip")

    element: WebElement = driver.find_element(By.TAG_NAME, 'pre')
    return json.loads(element.text)['IP']


def get_new_tor_ip(driver: webdriver):
    controller = get_tor_controller()
    current_ip = get_current_tor_ip(driver)
    controller.signal(Signal.NEWNYM)
    new_ip = get_current_tor_ip(driver)
    if current_ip == new_ip:
        print("Fail to get new ip retrying in 15 seconds")
        time.sleep(15)
        get_new_tor_ip(driver)
    controller.close()
