import multiprocessing
from os import path

import typer
from . import scraper

app = typer.Typer()


@app.command()
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


@app.command()
def report_world(scrap: bool = False, convert: bool = False, force: bool = False):
    if not scrap and not convert:
        print("You must specify at least one of the following options: --scrap or --convert")
        return

    file_path = "data/html/report_world/report_world.html"

    if scrap:
        if not path.isfile(file_path) or force:
            print("Scraping report world")
            scraper.report_world.scrap(file_path)
            print("Done")
        else:
            print("File already exists use --force to override")

    if convert:
        if not path.isfile(file_path):
            print("File does not exist use --scrap to scrap it first")
            return
        print("Converting report world")
        scraper.report_world.to_json(file_path)


if __name__ == "__main__":
    app()
