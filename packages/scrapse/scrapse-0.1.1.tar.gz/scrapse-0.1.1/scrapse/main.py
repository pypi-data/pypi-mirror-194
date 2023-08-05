import typer

from scrapse.leggitalia import leggitalia_app

app = typer.Typer()
app.add_typer(leggitalia_app, name='leggitalia')


@app.callback()
def main():
    """
        Package created for the extraction of judgments.
    """


if __name__ == "__main__":
    app()
