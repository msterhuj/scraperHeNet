import os.path

from selenium import webdriver

import json
import socks
import socket
from urllib.request import Request, urlopen
from time import sleep
from stem import Signal
from stem.control import Controller

controller_ip = "172.0.0.1"
controller_port = 9051
controller_pass = "admin"
url_test = "https://check.torproject.org/api/ip"


def get_chrome_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--proxy-server=socks5://tor:9050')
    driver = webdriver.Remote("http://127.0.0.1:4444/wd/hub", options=options)
    return driver


def get_new_tor_ip(controller: Controller):
    """
    Get a new IP address from Tor and re ask utils ip is never seen in the past
    :param controller: connection to tor manager
    :return str: ip for proxy
    """
    controller.signal(Signal.NEWNYM)


def get_tor_controller():
    controller = Controller.from_port(port=9051)
    controller.authenticate(password=controller_pass)
    print("Tor version " + str(controller.get_version()) + " connected")
    return controller


def close_tor_controller(controller: Controller):
    controller.close()
