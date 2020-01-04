from datasus.utils import get_metadata

from dbfread import DBF
from tqdm import tqdm

import pandas as pd
import subprocess
import glob
import os
import re


def dbc2bdf_single(filename):
    metadata = get_metadata(filename)
    converted_file = f'{metadata["path"]}.bdf'
    subprocess.run([
        os.path.join('datasus', 'scripts', 'dbc2bdf'),
        filename,
        converted_file
    ])
    metadata['filename'] = converted_file
    return metadata

def extract_files(data_folder, filters):
    corrupted_files = []
    database_folder = os.path.join(data_folder, '.database')
    os.makedirs(database_folder, exist_ok=True)
    data_files = glob.glob(
        os.path.join(data_folder, '*.dbc'))
    for filename in tqdm(data_files):
        converted = dbc2bdf_single(filename)
        db = converted['database']
        database = os.path.join(database_folder, db)
        try:
            bdf = list(DBF(converted['filename']))
        except ValueError:
            corrupted_files.append(converted['filename'])
        if not bdf:
            continue
        df = pd.DataFrame(bdf, columns=bdf[0].keys())
        df['month'] = converted['month']
        df['year'] = converted['year']
        df['uf'] = converted['uf']
        with pd.HDFStore(database) as hdf:
            if db in hdf.keys():
                hdf.append(db, df, data_columns=True)
            else:
                hdf.put(db, df, data_columns=True)