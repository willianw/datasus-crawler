# To-do:
# - Expand database exploration

from datasus import download

import json
import os

MODULE_PATH = os.path.dirname(__file__)

with open(os.path.join(MODULE_PATH, 'config.json'), 'r') as f:
    CONFIG = json.load(f)
    
if __name__ == "__main__":
    # TO-DO: Implement filters logic based on CLI parameters
    CONFIG['filters'] = {}
    download.start_download(CONFIG)

