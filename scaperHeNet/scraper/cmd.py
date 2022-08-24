from os import path

import typer

from . import scrap_report_world

app = typer.Typer()


@app.command()
def report_world(redownload: bool = False):
    file_path = "data/html/report_world/report_world.html"
    if not path.isfile(file_path) or redownload:
        print("Scraping report world")
        scrap_report_world(file_path)
        print("Done")
    else:
        print("File already exists")
