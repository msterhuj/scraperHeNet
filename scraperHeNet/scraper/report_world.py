from bs4 import BeautifulSoup

from scraperHeNet import tor, utils


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
        table = soup.find("table", id="table_countries")
        cols = [utils.sanitize_string(th.get_text()) for th in table.find("tr").find_all("th")]

        for tr in table.find_all("tr")[1:]:
            tds = tr.find_all("td")
            row = {cols[i]: utils.sanitize_string(tds[i].get_text()) for i in range(len(cols))}
            del row["Report"]
            row["details"] = tds[-1].find("a")["href"]
            if len(row) > 0:
                data.append(row)
    utils.save_to_json(data, "data/json/report_world.json")
    return data
