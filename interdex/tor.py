import json
import time

from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from stem import Signal
from stem.control import Controller

from interdex import get_config

config = get_config()

controller_ip = config["tor_control_address"]
controller_port = config["tor_control_port"]
controller_pass = config["tor_control_password"]
url_test = config["tor_url_test"]
selenium_remote_url = config["selenium_remote_url"]


def get_chrome_driver():
    options = webdriver.ChromeOptions()
    args = ["--proxy-server=socks5://tor:9050", "--headless", "--no-sandbox", "--disable-dev-shm-usage"]
    for arg in args:
        options.add_argument(arg)
    driver = webdriver.Remote(selenium_remote_url, options=options)
    return driver


def get_current_tor_ip(driver: webdriver):
    driver.get("https://check.torproject.org/api/ip")

    element: WebElement = driver.find_element(By.TAG_NAME, 'pre')
    return json.loads(element.text)['IP']


def get_url(url: str, driver: webdriver, waiter=None) -> webdriver:
    error_msg_limit = "You have reached your query limit on bgp.he.net."
    error_msg_validate = "Please wait while we validate your browser."
    drv = driver

    drv.get(url)
    if waiter:
        try:
            WebDriverWait(drv, 10).until(waiter)
        except TimeoutException:
            print("Timeout waiting for element")

    if error_msg_limit in drv.page_source:
        print("Reached query limit on bgp.he.net reinit new web driver for ip rotation")
        get_new_tor_ip_path()
        return get_url(url, drv, waiter)

    if error_msg_validate in drv.page_source:
        print("Waiting for validation")
        time.sleep(15)
        if error_msg_validate in drv.page_source:
            print("Validation failed retrying in 15 seconds")
            time.sleep(15)
            return get_url(url, drv, waiter)
    return drv


def get_tor_controller():
    controller = Controller.from_port(address="172.16.1.22", port=9051)
    controller.authenticate(password=controller_pass)
    print("Tor version " + str(controller.get_version()) + " connected")
    return controller


def get_new_tor_ip_path():
    controller = get_tor_controller()
    controller.signal(Signal.NEWNYM)
    controller.close()
