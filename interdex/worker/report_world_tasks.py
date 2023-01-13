from bs4 import BeautifulSoup
from interdex import tor, utils
from interdex.database import db
from interdex.worker import app


@app.task
def report_world():
    print("Getting selenium driver")
    driver = tor.get_chrome_driver()
    try:
        print("Getting url https://bgp.he.net/report/world")
        driver = tor.get_url("https://bgp.he.net/report/world", driver)
        data = driver.page_source
        if not data:
            raise Exception("No data returned")

        print("Parsing data for report_world")
        soup = BeautifulSoup(data, "html.parser")
        footer = soup.find("div", id="footer")
        date = utils.date_to_json(utils.convert_footer_to_date(str(footer.text).strip()))
        print(f"Last page update {date}")

        table = soup.find("table", id="table_countries")
        cols = [utils.sanitize_string(th.get_text()) for th in table.find("tr").find_all("th")]

        data = []

        for tr in table.find_all("tr")[1:]:
            tds = tr.find_all("td")
            row = {cols[i]: utils.sanitize_string(tds[i].get_text()) for i in range(len(cols))}
            row["country"] = row.pop("description")  # rename key "description" to "country"
            row["asns"] = int(row["asns"].replace(",", ""))  # remove comma and convert to number
            del row["report"]  # remove useless column
            row["details"] = tds[-1].find("a")["href"]  # get link for more details
            row["last_source_page_update"] = date
            if len(row) > 0:
                data.append(row)

        print(f"Saving {len(data)} rows to database")

        db.country.create_index("cc", unique=True)
        for row in data:
            row["last_scrape_at"] = utils.get_current_time()
            del row["details"]
            row["last_source_page_update"] = utils.json_date_to_datetime(row["last_source_page_update"])

            # check if country already exists
            on_db = db.country.find_one({"cc": row["cc"]})
            if on_db:
                # check if last_source_page_update is > last_scrape_at
                if on_db["last_source_page_update"] < row["last_scrape_at"]:
                    print(f"Skipping {row['cc']} because last_source_page_update is > last_scrape_at")
                    continue
                db.country.update_one({"cc": row["cc"]}, {"$set": row})
                print(f"Updated country {row['cc']}")
            else:
                db.country.insert_one(row)
                print(f"Inserted {row['cc']}")

        print("Done with report_world")

    except Exception as e:
        print(e)
    driver.quit()
