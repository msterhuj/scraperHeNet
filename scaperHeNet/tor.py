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


def get_output_ip() -> dict:
    try:
        soc = tor_proxy.split(":")
        socks.set_default_proxy(socks.SOCKS5, soc[0], int(soc[1]))
        socket.socket = socks.socksocket
        req = Request(url_test, headers={'User-Agent': 'Mozilla/5.0', })
        return json.loads(urlopen(req).read())
    except Exception:
        print("Error when check new ip retry in 10s")
        sleep(5)
        return get_output_ip()


def get_new_tor_ip(controller: Controller):
    """
    Get a new IP address from Tor and re ask utils ip is never seen in the past
    :param controller: connection to tor manager
    :return str: ip for proxy
    """
    old_ips_path = "json/used_tor_ips.json"
    used_tor_ips = []
    if os.path.isfile(old_ips_path):
        with open(old_ips_path, 'r') as f:
            used_tor_ips = json.load(f)
    print("Request new tor path")
    controller.signal(Signal.NEWNYM)
    print("Getting new ip address")
    new_ip = get_output_ip()
    if not new_ip.get("IsTor"):
        print("Not a tor ip obtained")
        exit(-1)
    ip = new_ip.get("IP")
    if ip in used_tor_ips:
        print("IP already used as tor for new ip in 10s")
        sleep(5)
        get_new_tor_ip(controller)

    print("New ip obtained: " + ip)
    used_tor_ips.append(ip)
    with open(old_ips_path, 'w') as f:
        print("Writing new ip to used_tor_ips.json")
        json.dump(used_tor_ips, f)
    return ip


def get_tor_controller():
    controller = Controller.from_port(port=9051)
    controller.authenticate(password=controller_pass)
    print("Tor version " + str(controller.get_version()) + " connected")
    return controller


def close_tor_controller(controller: Controller):
    controller.close()
