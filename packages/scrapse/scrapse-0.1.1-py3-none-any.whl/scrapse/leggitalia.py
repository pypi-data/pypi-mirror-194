import typer
import requests
from bs4 import BeautifulSoup
from pathlib import Path
from rich.progress import track, Progress, SpinnerColumn, TextColumn
from rich import print
from scrapse import utils
from scrapse.utils import LeggiDiItalia

leggitalia_app = typer.Typer()


def save_sentences(ldi, current_chunk, request_text):
    soup = BeautifulSoup(request_text, 'html.parser')
    sentences = soup.find_all("div", {"class": "doc_body"})
    for index, sentence in enumerate(sentences):
        output_file = Path(
            '/'.join((ldi.path, ldi.directory, f'{(ldi.chunk_size * current_chunk) + index}.{ldi.extension}')))
        output_file.parent.mkdir(exist_ok=True, parents=True)
        output_file.write_text(str(sentence))


def search_sentences(ldi):
    with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=False,
    ) as progress:
        progress.add_task(description="Searching for sentences...", total=None)
        request = requests.post(url=ldi.baseurl, headers=ldi.headers,
                                params=ldi.build_search_query())

    sentences_found = request.json()['result']['rows']
    progress.console.print(f'\u2713 Found {sentences_found} sentences')

    sentences_id = list()
    for item in request.json()['result']['items']:
        sentences_id.append(item['id'])

    return ['|'.join(sentences_id[i:i + ldi.chunk_size]) for i in
            range(0, len(sentences_id), ldi.chunk_size)], sentences_found


def export_sentences(ldi):
    sentences_id, sentences_found = search_sentences(ldi)

    for current_chunk in track(range(0, len(sentences_id), 1), description='Extraction of sentences...'):
        request = requests.post(url=ldi.baseurl, headers=ldi.headers,
                                params=ldi.build_export_query(sentences_id[current_chunk]))
        # print(request.status_code)
        # print(request.text)
        save_sentences(ldi, current_chunk, request.text)


@leggitalia_app.command()
def save_cookie(cookie: str):
    file_path = '/'.join([str(Path.cwd().absolute()), 'ldi_cookie.txt'])
    output_file = Path(file_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(str(cookie))


@leggitalia_app.command()
def scrap(
        judicial_bodies: str = typer.Option(None, "--judicial-bodies", "-j", help="Filter judging bodies"),
        location: str = typer.Option(None, "--location", "-l", help="Filter location of the court of reference"),
        sections: str = typer.Option(None, "--sections", "-s", help="Reference section filter, may change by location"),
        rows: str = typer.Option('100000000', "--rows", "-r", help="Number of judgments to download"),
        path: Path = typer.Option(Path.home(), "--path", "-p",
                                  help="Path where to save downloaded judgments"),
        extension: str = typer.Option("HTM", "--extension", "-e", help="Desired extension of judgments "),

):
    """
        Download the sentences from the platform https://pa.leggiditalia.it/.

        It is necessary to specify at least one filter among: --adjudicating-bodies, --location and --sections.

        Provide an input list with the following formatting: --sections 'par1, par2, ...'
    """
    ldi = LeggiDiItalia(judicial_bodies=judicial_bodies, location=location, sections=sections, rows=rows,
                        path=path, extension=extension)
    ldi.build_headers()
    export_sentences(ldi)


@leggitalia_app.command()
def show(j: bool = True, s: bool = True, l: bool = True):
    """
        Shows the possible values to be assigned to the respective filters.
    """
    if j:
        print(f'Judicial bodies {utils.JUDICIAL_BODIES}\n')
    if s:
        print(f'Sections {utils.SECTIONS}\n')
    if l:
        print(f'Locations {utils.LOCATIONS}\n')


@leggitalia_app.callback()
def callback():
    """
       Dedicated command to the site LEGGI D'ITALIA PA
    """


if __name__ == "__main__":
    leggitalia_app()
