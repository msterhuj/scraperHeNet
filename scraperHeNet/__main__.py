from os import path

import typer

from . import scraper

app = typer.Typer()


@app.command()
def report_world(scrap: bool = False, convert: bool = False, import_mongo: bool = False):
    if not scrap and not convert and not import_mongo:
        print("You must specify at least one of the following options: --scrap or --convert or  --import-mongo")
        return

    file_path = "data/html/report_world/report_world.html"

    if scrap:
        print("Scraping report world")
        scraper.report_world.scrap(file_path)
        print("Done")

    if convert:
        print("Converting report world")
        scraper.report_world.to_json(file_path)

    if import_mongo:
        print("Importing report world")
        scraper.report_world.import_to_mongo()
        print("Done")


@app.command()
def report_dns(scrap: bool = False, convert: bool = False, ):
    if not scrap and not convert:
        print("You must specify at least one of the following options: --scrap or --convert")
        return

    if scrap:
        print("Scraping report dns")
        scraper.report_dns.scrap()
        print("Done")

    if convert:
        print("Converting report dns")
        scraper.report_dns.to_json()


@app.command()
def tld(scrap: bool = False, convert: bool = False, import_mongo: bool = False):
    if not scrap and not convert and not import_mongo:
        print("You must specify at least one of the following options: --scrap or --convert or  --import-mongo")
        return

    if scrap:
        scraper.tld_info.scrap()

    if convert:
        scraper.tld_info.to_json()

    if import_mongo:
        scraper.tld_info.import_to_mongo()


@app.command()
def asn(scrap: bool = False, convert: bool = False, import_mongo: bool = False):
    if not scrap and not convert and not import_mongo:
        print("You must specify at least one of the following options: --scrap or --convert or  --import-mongo")
        return

    if scrap:
        scraper.asn.scrap()

    if convert:
        scraper.asn.to_json()

    if import_mongo:
        scraper.asn.import_to_mongo()


@app.command(name="range")
def range_cmd(scrap: bool = False, convert: bool = False, import_mongo: bool = False):
    if not scrap and not convert and not import_mongo:
        print("You must specify at least one of the following options: --scrap or --convert or  --import-mongo")
        return

    if scrap:
        scraper.range.scrap()

    if convert:
        scraper.range.to_json()

    if import_mongo:
        scraper.range.import_to_mongo()


if __name__ == "__main__":
    app()
