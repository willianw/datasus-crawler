from datasus.download_manager import start
from datasus.treatment import get_ftp_start_node
from datasus.utils import get_metadata

from ftplib import FTP, error_perm
from tqdm import tqdm
import re
import os


def ftp_login(ftp_config):
    ftp = FTP(ftp_config['ftp_host'])
    ftp.login()
    return ftp

def start_download(CONFIG):
    ''' Start downloading files from ftp connection.
        - CONFIG: (dict) data from config.json
    '''

    ftp_config = {
        'ftp_host': CONFIG['ftp_host'],
        'port': CONFIG['ftp_port'],
        'login': 'anonymous',
        'password': 'anonymous@'
    }

    download_list = []
    filters = CONFIG['filters']
    start_url = CONFIG['root_directory']
    for database in filters['databases']:
        download_list += file_tree(
            ftp_config,
            get_ftp_start_node(database, None, start_url),
            filters
        )
    file_path = os.path.abspath(CONFIG['download_folder'])
    os.makedirs(file_path, exist_ok=True)
    start(ftp_config, download_list, file_path)
    
def ftp_line_parse(line, data_list):
    data = re.search(
        r'\d\d-\d\d-\d\d  \d\d:\d\d[AP]M +(<DIR>|\d+) +([\w \.]+)', line)
    if data:
        folder = data.group(1) == '<DIR>'
        filename = data.group(2)
        data_list.append((folder, filename))
    else:
        raise IOError(f'Incorrect line "{line}"')

def file_tree(ftp_config, url_path, filters):
    ''' Downloads files from DATASUS FTP System recursively
        - ftp_config: data for FTP connection.
        - url_path: current ftp path for file extraction
        - filters: (dict) restrict which files to download:
            - databases: list of database names to select, e.g.: ['SIASUS', 'SIHSUS', 'SIM']
            - uf: list of national states, e.g.: ['PB', 'TO', 'RS']
            - date: tuple (start date, end date). They must be year or a string in format "MM/YYYY"
    '''

    ftp = ftp_login(ftp_config)
    folder_content = []
    
    try:
        ftp.retrlines(
            f'LIST {url_path}',
            lambda line: ftp_line_parse(
                                        line,
                                        folder_content))
    except error_perm:
        print(f"ERROR: LIST {url_path}")
    
    download_list = []
    for folder, filename in folder_content:
        #new_url_path = f"{url_path}{filename}{'/' if folder else ''}"
        new_url_path = os.path.join(url_path, filename)
        if folder:
            download_list += file_tree(ftp_config, new_url_path, filters)
        else:
            # Filter files to download
            metadata = get_metadata(filename)
            reject_criteria = [
                filters.get('uf',    False) and metadata['uf']    not in filters['uf'],
                filters.get('year',  False) and metadata['year']  not in filters['year'],
                filters.get('month', False) and metadata['month'] not in filters['month'],
            ]
            if any(reject_criteria):
                continue
            download_list.append(new_url_path)

    ftp.quit()
    return download_list
    