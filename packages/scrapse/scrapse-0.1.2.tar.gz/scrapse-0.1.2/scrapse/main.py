import typer
from typing import Optional

from scrapse.leggitalia import leggitalia_app

__version__ = "0.1.2"

app = typer.Typer()
app.add_typer(leggitalia_app, name='leggitalia')


def version_callback(value: bool):
    if value:
        print(f"ScrapSE {__version__}")
        raise typer.Exit()


@app.callback()
def main(
        version: Optional[bool] = typer.Option(
            None, "--version", callback=version_callback
        )):
    """
        Package created for the extraction of judgments.
    """


if __name__ == "__main__":
    app()
