from scaperHeNet import tor


def scrap_report_world(file_path):
    driver = tor.get_chrome_driver()
    try:
        driver.get("https://bgp.he.net/report/world")
        with open(file_path, "w") as f:
            f.write(driver.page_source)
        driver.quit()
    except Exception as e:
        print(e)
        driver.quit()
