import subprocess
import pdb
import re
import os


_EXT = {
    'dbc': 'Baixados',
    'dbf': 'Extraídos',
}

def _inv(date):
    return '/'.join(date.split('/')[::-1])

def _set_path(dict, hierarchy):
    for i, item in enumerate(hierarchy):
        if not item in dict:
            dict[item] = {} if i < len(hierarchy) -1 else []
        dict = dict[item]
    return dict

def list_all(CONFIG):
    stats = {}
    FILE_REGEX = r'^([A-Z]{2,3})([A-Z]{2})([0-9]{2})([0-9]{2})\.([a-z]{3})$'
    for filename in os.listdir(f"{CONFIG['download_folder']}"):
        if not filename.startswith('.'):
            try:
                db, uf, yr, mt, ext = re.search(
                    FILE_REGEX, filename, re.IGNORECASE).groups()
                _set_path(stats, [ext, db, uf]).append(f'{yr}/{mt}')
            except AttributeError:
                pdb.set_trace()
    for ext, dbs in stats.items():
        print(f"{_EXT.get(ext, 'Outros')}")
        for db, ufs in dbs.items():
            print(f"\t{db}")
            for uf, dates in ufs.items():
                print(f"\t\t{uf}:\t{len(dates)}"
                    + f" Registros de {_inv(min(dates))} a {_inv(max(dates))}")
