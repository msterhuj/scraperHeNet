import json
from multiprocessing import Pool, current_process

from rich import print
from rich.progress import open as ropen
from bs4 import BeautifulSoup

from scaperHeNet import tor, utils


def __scrap_pool__(doc: dict):
    pname = current_process().name
    print(f"{pname} - booting up")
    driver = tor.get_chrome_driver()
    failed = []
    try:
        for country in doc:
            pass
            url = f"https://bgp.he.net{country['details']}"
            data = tor.get_url(url, driver)
            if data:
                with open(f"data/html/asn/{country['CC']}.html", "w") as f:
                    f.write(data)
                print(f"{pname} {country['CC']} scraped")
            else:
                print(f"{pname} {country['CC']} not scraped")
                failed.append(country)
    except Exception as e:
        print(e)
    driver.quit()
    print(f"{pname} - finished")
    return failed


def scrap():
    with ropen("data/json/report_world/report_world.json", "r") as f:
        data = json.load(f)
    chunk_size = 5
    urls = list(utils.split(data, chunk_size))
    pool = Pool(processes=chunk_size)
    failed = pool.map(__scrap_pool__, urls)
    print(failed)


def to_json(file_path):
    pass
