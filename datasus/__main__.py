# To-do:
# - Expand database exploration

from datasus import download
from datasus import database

import subprocess
import json
import os

MODULE_PATH = os.path.dirname(__file__)

with open(os.path.join(MODULE_PATH, 'config.json'), 'r') as f:
    CONFIG = json.load(f)

def prepare_environment():
    # Scripts
    dbc2bdf_filename = os.path.join("datasus", "scripts", "dbc2bdf")
    if not os.path.exists(dbc2bdf_filename):
        subprocess.run([
            "gcc", "-o", dbc2bdf_filename,
            os.path.join("datasus", "scripts", "dbc2dbf.c"),
            os.path.join("datasus", "scripts", "blast.c")])

if __name__ == "__main__":
    # TO-DO: Implement filters logic based on CLI parameters
    CONFIG['filters'] = {'databases': ['SIHSUS'], 'uf':['RJ']}
    prepare_environment()
    download.start_download(CONFIG) # Gather below function in a single process
    #database.extract_files('data', CONFIG['filters'])
