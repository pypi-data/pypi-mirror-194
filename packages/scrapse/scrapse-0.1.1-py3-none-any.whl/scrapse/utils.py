from pathlib import Path
import typer
from rich.console import Console

LOCATIONS = ['asti', 'alessandria', 'cuneo', 'ivrea', 'novara', 'torino']

SECTIONS = [
    'Sez. Unite', '(Ad. Plen.)', 'Sez. I', 'Sez. I bis', 'Sez. I ter', 'Sez. I quater', 'Sez. II',
    'Sez. II bis', 'Sez. II ter', 'Sez. II quater', 'Sez. III', 'Sez. III bis', 'Sez. III ter',
    'Sez. III quater', 'Sez. IV', 'Sez. IV bis', 'Sez. IV ter', 'Sez. IV quater', 'Sez. V', 'Sez. V bis',
    'Sez. VI', 'Sez. VI - 1', 'Sez. VI - 2', 'Sez. VI - 3', 'Sez. VI - Lavoro', 'Sez. VI - 5', 'Sez. VII',
    'Sez. VIII', 'Sez. IX', 'Sez. X', 'Sez. XI', 'Sez. XII', 'Sez. XIII', 'Sez. XIV', 'Sez. XV', 'Sez. XVI',
    'Sez. XVII', 'Sez. XVIII', 'Sez. XIX', 'Sez. XX', 'Sez. XXI', 'Sez. XXII', 'Sez. XXIII', 'Sez. XXIV',
    'Sez. XXV', 'Sez. XXVI', 'Sez. XXVII', 'Sez. XXVIII', 'Sez. XXIX', 'Sez. XXX', 'Sez. XXXI', 'Sez. XXXII',
    'Sez. XXXIII', 'Sez. XXXIV', 'Sez. XXXV', 'Sez. XXXVI', 'Sez. XXXVII', 'Sez. XXXVIII', 'Sez. XXXIX',
    'Sez. XL', 'Sez. XLI', 'Sez. XLII', 'Sez. XLIII', 'Sez. XLIV', 'Sez. XLV', 'Sez. XLVI', 'Sez. XLVII',
    'Sez. XLVIII', 'Sez. XLIX', 'Sez. L', 'Sez. LI', 'Sez. LII', 'Sez. LIII', 'Sez. LIV', 'Sez. LV', 'Sez. LVI',
    'Sez. LVII', 'Sez. LVIII', 'Sez. LIX', 'Sez. LX', 'Sez. LXI', 'Sez. LXII', 'Sez. LXIII', 'Sez. LXIV',
    'Sez. LXV', 'Sez. LXVI', 'Sez. LXVII', '(Ad. Gen.)', 'Grande Sez.', 'Sez. App.', 'Sez. I App.',
    'Sez. II App.', 'Sez. III App.', 'Sez. agraria', 'Sez. atti norm.', 'Sez. Autonomie', 'Sez. comm. spec.',
    'Sez. consult.', 'Sez. contr.', 'Sez. contr. enti', 'Sez. Contr. gestione', "Sez. Contr. Legittimita'",
    'Sez. Contr. Stato', 'Sez. disciplinare', 'Sez. enti loc.', 'Sez. fall.', 'Sez. feriale', 'Sez. giurisdiz.',
    'Sez. lavoro', 'Sez. minori', 'Sez. riunite', 'Sez. Riunite cons.', 'Sez. Riunite contr.',
    'Sez. spec. in materia di imprese', 'Sez. spec. propr. industr. ed intell.', 'Sez. stralcio', 'II Stralcio',
    'Sez. uff. elettorale', 'Sez. Unica', 'Sez. I ampliata', 'Sez. II ampliata', 'Sez. III ampliata',
    'Sez. IV ampliata', 'Sez. V ampliata', 'VIII ampliata', 'Sez. VI ampliata', 'Sez. VII ampliata',
    'Grande Cam.', 'Sez. Spec. Immigr., Prot. Inter. e Libera circ. UE',
    'Sez. delle persone, dei minori e della fam.']

JUDICIAL_BODIES = [
    'Corte Costituzionale', 'Cassazione Civile', 'Cassazione Penale', 'Consiglio di Stato',
    'Collegio arbitrale', 'Corte di giustizia tributaria di primo grado',
    'Corte di giustizia tributaria di secondo grado', 'Commiss. Trib. I grado',
    'Commiss. Trib. II grado', 'Commissione Tributaria Centrale', 'Commissione tributaria provinciale',
    'Comm.Tributaria regionale', 'Commiss. usi civici', 'C.G.A. della Regione Siciliana',
    "Corte d'Appello", "Corte d'Appello militare", "Corte d'Assise", "Corte europea diritti dell'uomo",
    "Corte d'Assise d'Appello", 'Corte dei Conti', 'Corte di Giustizia CE',
    'Corte giustizia Unione Europea', "Autorita' Garante per la concorrenza", 'Giudice Istruttore',
    'Giudice di Pace', 'Giudice tutelare', 'T.A.R.', 'T.R.G.A.', 'Tribunale', "Trib. liberta'",
    'Tribunale Militare', 'Tribunale Minorenni', 'Trib. Reg. acque', 'Trib. Sorveglianza',
    'Tribunale Superiore delle Acque Pubbliche', 'Tribunale di Primo Grado CE',
    'Trib. I Grado Unione Europea', 'Uff. indagini preliminari']


class LeggiDiItalia:
    baseurl = 'https://pa.leggiditalia.it/rest'
    headers = {
        'Accept': 'application/json',
        'Content-type': 'application/x-www-form-urlencoded',
    }

    search_params = {
        'core': 'giuryPEL',
        'start': '0',
        'method': 'solr.search',
        'sort': 'docorder asc:titolo asc:elemorder asc:_is_parent desc',
        'facet_name': 'mask-sentenze',
        'reload': 'false',
        'fields': 'risultato:score:estrcomp',
        'score': 'true',
        'highlight': 'document_text',
        'filters': '{"mode":"AND","items":[{"field":"operasez","mode":"IN","value":["01","05","44","46","47","55",'
                   '"59","60","78","07","20","15","42","66","70","88","K0","K1","K3","K5","DA","DB","DC","DD","0H",'
                   '"2H","9H","90","41","43","H0","06","68","WT","WZ","86","QN","QP","Q6","W3","V3","WH","QE","WO",'
                   '"QK","WQ","VZ","WF","QC","W7","V7","WV","QO","XM","VD","WX","VV","WK","VW","WP","QL","WD","QA",'
                   '"WL","QH","WT","QN","X3","QS","86","Q6","XC","QZ","WM","QI","WS","QJ","WG","QD","XF","VI","WR",'
                   '"QM","X8","VA","WU","QW","X9","VB","WY","QX","WE","XA","VC","QB","XB","QY","X1","QR","WZ","QP",'
                   '"XU","VX","S7","Q7","AP"]}]}',
    }

    export_params = {
        'method': 'print.doc',
        'reload': '1',
        'mode': 'print',
        'FORMATO': 'HTM',
        'PAGINA': 'P',
        'NOMEEXPORT': 'Salva_documenti',
    }

    chunk_size = 100

    directory = None

    def __init__(self, judicial_bodies=None, sections=None, location=None, rows='100000000', extension=None,
                 path=Path.home()) -> None:
        super().__init__()
        self.judicial_bodies = judicial_bodies
        self.sections = sections
        self.location = location
        self.rows = rows
        self.path = str(path)
        self.extension = extension
        self.check_filters()
        self.build_directory()

    def check_filters(self):
        if self.judicial_bodies is None and self.sections is None and self.location is None:
            Console(stderr=True).print('No filter was provided.\nUse --help for more info.')
            raise typer.Exit()

    def build_search_query(self):
        base_query = """{"mode":"AND","items":[{"mode":"AND","items":[{"field":"operasez","mode":"IN","value":["60","46","47","55","78","59","07"]},{"field":"tipo","mode":"EQUAL","value":"giurisprudenza/sentenze"}]}]}"""
        if self.judicial_bodies is not None:
            base_query = base_query[
                         :-2] + ''',{"field":"giuri_ente","mode":"IN","value":[''' + ','.join(
                f'"{item}"' for item in self.judicial_bodies.split(",")) + ''']}''' + base_query[
                                                                                      -2:]
        if self.sections is not None:
            base_query = base_query[
                         :-2] + ''',{"field":"giuri_sezione","mode":"IN","value":[''' + ','.join(
                f'"{item}"' for item in self.sections.split(",")) + ''']}''' + base_query[
                                                                               -2:]
        if self.location is not None:
            base_query = base_query[
                         :-2] + ''',{"field":"localita_ft","mode":"EQUAL","value":"''' + self.location + '''"}''' + base_query[
                                                                                                                    -2:]
        self.search_params['query'] = base_query
        self.search_params['rows'] = str(self.rows)
        return self.search_params

    def build_export_query(self, ids):
        self.export_params['ids'] = ids
        return self.export_params

    def build_directory(self):
        filters_to_join = [self.judicial_bodies, self.sections, self.location]
        self.directory = '_'.join(
            ['&'.join(filter.split(',')).replace(' ', '').lower() for filter in filters_to_join if filter is not None])

    def build_headers(self):
        path = Path('ldi_cookie.txt')
        if path.is_file():
            self.headers['Cookie'] = path.open(mode='r').read()
