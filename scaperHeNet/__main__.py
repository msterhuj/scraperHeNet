import time
import multiprocessing

from rich import print
from selenium import webdriver

import tor

def get(url: str):
    driver = tor.get_chrome_driver()
    try:
        driver.get(url)
        data = driver.page_source
        driver.quit()
        return data
    except Exception as e:
        print(e)
        driver.quit()

if __name__ == '__main__':
    
    chrome_driver_total = 4

    p = multiprocessing.Pool(processes=chrome_driver_total)

    urls = [
        "https://check.torproject.org/api/ip",
        "https://ifconfig.me/ip"
    ]

    result = p.map(get, urls)
    print(result)
    p.close()
    p.join()