import multiprocessing
from os import path

import typer
from . import scraper

app = typer.Typer()


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


@app.command()
def asn(scrap: bool = False, convert: bool = False):
    if not scrap and not convert:
        print("You must specify at least one of the following options: --scrap or --convert")
        return

    if scrap:
        scraper.asn.scrap()

    if convert:
        scraper.asn.to_json()


@app.command(name="range")
def range_cmd(scrap: bool = False, convert: bool = False):
    if not scrap and not convert:
        print("You must specify at least one of the following options: --scrap or --convert")
        return

    if scrap:
        scraper.range.scrap()

    if convert:
        scraper.range.to_json()


if __name__ == "__main__":
    app()
    # todo tester le switch d'ip
    #pass