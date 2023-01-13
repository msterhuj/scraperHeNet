import json
import os
from glob import glob
from multiprocessing import Pool, current_process
from os.path import basename

from rich import print
from rich.progress import open as ropen
from rich.progress import track
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By

from scraperHeNet import tor, utils
from scraperHeNet.mongo import db


def __scrap_pool__(doc: dict):
    pname = current_process().name
    print(f"{pname} - booting up")
    driver = tor.get_chrome_driver()
    print(f"{pname} - driver ready")
    failed = []

    try:
        for asn in doc:
            file_path = f"data/html/range/{asn['asn']}.html"
            # check if file exists
            if os.path.isfile(file_path):
                print(f"{pname} - {asn['asn']} - already exists")
                continue
            url = f"https://bgp.he.net{asn['details']}"
            driver = tor.get_url(url, driver, lambda driver: driver.find_elements(By.ID, "table_peers4") or driver.find_elements(By.ID, "table_peers6"))
            if "page_source" in dir(driver):
                data = driver.page_source
                with open(file_path, "w") as f:
                    f.write(data)
                print(f"{pname} {asn['asn']} scraped")
            else:
                print(f"{pname} {asn['asn']} not scraped")
                failed.append(asn)
    except Exception as e:
        print(e)
    driver.quit()
    print(f"{pname} - finished")
    return failed


def scrap():
    data = []
    with open("data/json/asn.json", "r") as f:
        print("removing early exist file scrap")
        for item in track(json.load(f)):
            if os.path.isfile(f"data/html/range/{item['asn']}.html"):
                continue
            data.append(item)
    print("total asn to scrap: ", len(data))
    chunk_size = 15  # todo change this to a config variable
    urls = list(utils.split(data, chunk_size))
    pool = Pool(processes=chunk_size)
    failed = pool.map(__scrap_pool__, urls)
    print(failed)


def to_json():
    files = glob("data/html/range/*.html")
    data = []
    for file in track(files, "Converting range html to json..."):
        with open(file, 'r', encoding="utf-8") as f:
            print(file)
            soup = BeautifulSoup(f.read(), "html.parser")
            an_name = os.path.basename(file).replace(".html", "")
            table_to_parse = {}
            table_to_parse["v4"] = soup.find("table", id="table_prefixes4")
            table_to_parse["v6"] = soup.find("table", id="table_prefixes6")

            for ver, table in table_to_parse.items():
                if table is None:
                    continue
                cols = [th.get_text() for th in table.find("tr").find_all("th")]

                for tr in table.find_all("tr")[1:]:
                    tds = tr.find_all("td")
                    row = {utils.sanitize_string(cols[i]): utils.sanitize_string(tds[i].get_text()) for i in range(len(cols))}
                    row["details"] = tds[0].find("a")["href"]
                    row["asn"] = an_name
                    row["version"] = ver
                    if len(row) > 0:
                        data.append(row)
    utils.save_to_json(data, "data/json/range.json")

def import_to_mongo():
    db.range.create_index("prefix")
    db.range.delete_many({})
    with ropen("data/json/range.json", "r") as f:
        data = json.load(f)
    for item in track(data, "Importing range to db..."):
        del item["details"]
        item["created_at"] = utils.get_current_time()
        item["updated_at"] = item["created_at"]
        db.range.insert_one(item)