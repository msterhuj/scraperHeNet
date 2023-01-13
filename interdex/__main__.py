from typer import Typer
from interdex import commands

app = Typer()

app.add_typer(commands.henet.app, name="henet")


@app.command()
def hello(name: str):
    print(f"Hello {name}")


if __name__ == "__main__":
    app()
