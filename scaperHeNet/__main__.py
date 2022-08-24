import multiprocessing

import typer

from .scraper import app as scraper_app


def dev():
    chrome_driver_total = 4

    p = multiprocessing.Pool(processes=chrome_driver_total)

    urls = [
        "https://check.torproject.org/api/ip",
        "https://ifconfig.me/ip"
    ]
    get = None

    result = p.map(get, urls)
    print(result)
    p.close()
    p.join()


app = typer.Typer()

app.add_typer(scraper_app, name="scrap")

if __name__ == "__main__":
    app()
