import json

from bs4 import BeautifulSoup

from scraperHeNet import tor, utils
from scraperHeNet.mongo import db


def scrap(file_path):
    driver = tor.get_chrome_driver()
    driver = tor.get_url("https://bgp.he.net/report/world", driver)
    data = driver.page_source
    if data:
        with open(file_path, "w") as f:
            f.write(data)
    driver.quit()


def to_json(file_path):
    data = []
    with open(file_path, "r") as f:
        soup = BeautifulSoup(f.read(), "html.parser")
        footer = soup.find("div", id="footer")

        date = utils.date_to_json(utils.convert_footer_to_date(str(footer.text).strip()))
        print(f"Last page update {date}")

        table = soup.find("table", id="table_countries")
        cols = [utils.sanitize_string(th.get_text()) for th in table.find("tr").find_all("th")]

        for tr in table.find_all("tr")[1:]:
            tds = tr.find_all("td")
            row = {cols[i]: utils.sanitize_string(tds[i].get_text()) for i in range(len(cols))}
            row["country"] = row.pop("description")  # rename key "description" to "country"
            row["asns"] = int(row["asns"].replace(",", ""))  # remove comma and convert to number
            del row["report"]  # remove useless column
            row["details"] = tds[-1].find("a")["href"]  # get link for more details
            row["last_page_update"] = date
            if len(row) > 0:
                data.append(row)
    utils.save_to_json(data, "data/json/report_world.json")
    return data


def import_to_mongo():
    db.country.create_index("cc", unique=True)
    db.country.delete_many({})
    with open("data/json/report_world.json", "r") as f:
        data = json.load(f)
    for row in data:
        row["created_at"] = utils.get_current_time()
        row["updated_at"] = row["created_at"]
        del row["details"]
        row["last_page_update"] = utils.json_date_to_datetime(row["last_page_update"])
    db.country.insert_many(data)
