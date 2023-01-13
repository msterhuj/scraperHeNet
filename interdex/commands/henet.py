from typer import Typer

app = Typer()


@app.command()
def report_world():
    from interdex import worker
    worker.report_world.delay()
