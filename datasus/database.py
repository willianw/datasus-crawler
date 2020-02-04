from datasus.utils import get_metadata

from dbfread import DBF
from tqdm import tqdm

import pandas as pd
import subprocess
import glob
import os
import re

def prepare_environment():
    dbc2dbf_filename = os.path.join("datasus", "scripts", "dbc2dbf")
    if not os.path.exists(dbc2dbf_filename):
        subprocess.run([
            "gcc", "-o", dbc2dbf_filename,
            os.path.join("datasus", "scripts", "dbc2dbf.c"),
            os.path.join("datasus", "scripts", "blast.c")])

def dbc2dbf_single(filename):
    metadata = get_metadata(filename)
    converted_file = f'{metadata["path"]}.bdf'
    try:
        subprocess.Popen([
            os.path.join('datasus', 'scripts', 'dbc2bdf'),
            filename,
            converted_file
        ])
    except OSError:
        print(f"Too big {filename}")
        return False
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
        if not converted:
            continue
        db = converted['database']
        database = os.path.join(database_folder, db)
        try:
            bdf = DBF(converted['filename'])
        except ValueError:
            corrupted_files.append(converted['filename'])
        except Exception:
            print(f"Problem file {filename}")
            continue
        if not bdf:
            continue
        df = pd.DataFrame(bdf, columns=bdf.field_names)
        df['month'] = converted['month']
        df['year'] = converted['year']
        df['uf'] = converted['uf']
        with pd.HDFStore(database) as hdf:
            if db in hdf.keys():
                hdf.append(db, df, data_columns=True)
            else:
                hdf.put(db, df, data_columns=True)