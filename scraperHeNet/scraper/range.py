import json
from glob import glob
from multiprocessing import Pool, current_process
from os.path import basename

from rich import print
from rich.progress import open as ropen
from rich.progress import track
from bs4 import BeautifulSoup

from scraperHeNet import tor, utils


def __scrap_pool__(doc: dict):
    pname = current_process().name
    print(f"{pname} - booting up")
    driver = tor.get_chrome_driver()
    failed = []

    try:
        for asn in doc:
            url = f"https://bgp.he.net{asn['details']}"
            driver = tor.get_url(url, driver)
            data = driver.page_source
            if data:
                with open(f"data/html/range/{asn['ASN']}.html", "w") as f:
                    f.write(data)
                print(f"{pname} {asn['ASN']} scraped")
            else:
                print(f"{pname} {asn['ASN']} not scraped")
                failed.append(asn)
    except Exception as e:
        print(e)
    driver.quit()
    print(f"{pname} - finished")
    return failed


def scrap():
    with ropen("data/json/asn.json", "r") as f:
        data = json.load(f)
    chunk_size = 10  # todo change this to a config variable
    urls = list(utils.split(data, chunk_size))
    pool = Pool(processes=chunk_size)
    failed = pool.map(__scrap_pool__, urls)
    print(failed)



def to_json():
    pass
