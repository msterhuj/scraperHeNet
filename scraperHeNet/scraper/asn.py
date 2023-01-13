import json
from glob import glob
from multiprocessing import Pool, current_process
from os.path import basename

from rich import print
from rich.progress import open as ropen
from rich.progress import track
from bs4 import BeautifulSoup

from scraperHeNet import tor, utils
from scraperHeNet.mongo import db


def __scrap_pool__(doc: dict):
    pname = current_process().name
    print(f"{pname} - booting up")
    driver = tor.get_chrome_driver()
    failed = []
    try:
        for country in doc:
            url = f"https://bgp.he.net{country['details']}"
            driver = tor.get_url(url, driver)
            data = driver.page_source
            if data:
                with open(f"data/html/asn/{country['cc']}.html", "w") as f:
                    f.write(data)
                print(f"{pname} {country['cc']} scraped")
            else:
                print(f"{pname} {country['cc']} not scraped")
                failed.append(country)
    except Exception as e:
        print(e)
    driver.quit()
    print(f"{pname} - finished")
    return failed


def scrap():
    with ropen("data/json/report_world.json", "r") as f:
        data = json.load(f)
    chunk_size = 10
    urls = list(utils.split(data, chunk_size))
    pool = Pool(processes=chunk_size)
    failed = pool.map(__scrap_pool__, urls)
    print(failed)


def to_json():
    files = glob("data/html/asn/*.html")
    data = []
    for file in track(files, description="Converting ans html to json..."):
        with open(file, 'r', encoding='utf-8', errors='ignore') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')
            try:
                table = soup.find('table', id='asns')
                cols = [utils.sanitize_string(th.get_text()) for th in table.find('tr').find_all('th')]

                footer = soup.find("div", id="footer")
                date = utils.date_to_json(utils.convert_footer_to_date(str(footer.text).strip()))

                for tr in table.find_all('tr')[1:]:
                    tds = tr.find_all('td')
                    row = {cols[i]: utils.sanitize_string(tds[i].get_text()) for i in range(len(cols))}
                    row["details"] = tds[0].find('a')['href']
                    row["cc"] = basename(file).split(".")[0].lower()
                    row["adjacencies_v4"] = int(row.pop("adjacencies-v4").replace(",", ""))
                    row["routes_v4"] = int(row.pop("routes-v4").replace(",", ""))
                    row["adjacencies_v6"] = int(row.pop("adjacencies-v6").replace(",", ""))
                    row["routes_v6"] = int(row.pop("routes-v6").replace(",", ""))
                    row["last_page_update"] = date
                    if len(row) > 0:
                        data.append(row)
            except AttributeError as e:
                print(f"Error parsing {basename(file)} no table found")
    utils.save_to_json(data, "data/json/asn.json")


def import_to_mongo():
    db.asn.create_index("asn", unique=True)
    db.asn.delete_many({})
    with ropen("data/json/asn.json", "r") as f:
        data = json.load(f)
    for row in track(data):
        del row["details"]
        row["created_at"] = utils.get_current_time()
        row["updated_at"] = row["created_at"]
        row["last_page_update"] = utils.json_date_to_datetime(row["last_page_update"])
    db.asn.insert_many(data)
