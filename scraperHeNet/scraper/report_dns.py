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
 

def scrap():
    driver = tor.get_chrome_driver()
    driver = tor.get_url("https://bgp.he.net/report/dns", driver)
    data = driver.page_source
    if data:
        with open("data/html/report_dns/report_dns.html", "w") as f:
            f.write(data)
    driver.quit()


def to_json():
    data = []
    with open("data/html/report_dns/report_dns.html", "r") as f:
        soup = BeautifulSoup(f.read(), "html.parser")

        table = soup.find("table", id="table_dnsall")
        cols = [utils.sanitize_string(th.get_text()) for th in table.find('tr').find_all('th')]
        
        for tr in table.find_all('tr')[1:]:
            tds = tr.find_all('td')
            row= {}
            row["tld"] = utils.sanitize_string(tds[0].get_text())
            row["description"] = utils.sanitize_string(tds[1].get_text())
            row["up"] = utils.get_dns_status(tds[2].find_all("img"))
            row["v4_glue"] = utils.get_dns_status(tds[3].find_all("img"))
            row["v4_ns"] = utils.get_dns_status(tds[4].find_all("img"))
            row["v6_glue"] = utils.get_dns_status(tds[5].find_all("img"))
            row["v6_ns"] = utils.get_dns_status(tds[6].find_all("img"))
            row["details"] = tds[-1].find("a")["href"]
            data.append(row)
    utils.save_to_json(data, "data/json/report_dns.json")


def import_to_mongo():
    pass
