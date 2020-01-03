from ftplib import FTP
import re
import os


def start_download(CONFIG):
    ''' Start downloading files from ftp connection.
        - CONFIG: (dict) data from config.json
    '''
    os.makedirs(CONFIG['download_folder'], exist_ok=True)
    ftp = FTP(CONFIG['root_url'])
    ftp.login()
    start_url = CONFIG['root_directory']
    file_tree(
        ftp,
        start_url,
        os.path.abspath(CONFIG['download_folder']),
        CONFIG['filters']
    )
    ftp.quit()
    
def ftp_line_parse(line, data_list):
    data = re.search(
        r'\d\d-\d\d-\d\d  \d\d:\d\d[AP]M +(<DIR>|\d+) +([\w \.]+)', line)
    if data:
        folder = data.group(1) == '<DIR>'
        filename = data.group(2)
        data_list.append((folder, filename))
    else:
        raise SyntaxException(f'Incorrect line "{line}"')
    
def download_file(ftp, url, path):
    print(f"RETR {url}")
    with open(path, 'wb') as f:
        ftp.retrbinary(f'RETR {url}', f.write)

def file_tree(ftp, url_path, file_path, filters):
    ''' Downloads files from DATASUS FTP System recursively
        - ftp: FTP connection. Must be initialized before.
        - url_path: current ftp path for file extraction
        - file_path: current disk folder for download files
        - filters: (dict) restrict which files to download:
            - databases: list of database names to select, e.g.: ['SIASUS', 'SIHSUS', 'SIM']
            - states: list of national states, e.g.: ['PB', 'TO', 'RS']
            - date: tuple (start date, end date). They must be year or a string in format "MM/YYYY"
    '''
    
    os.makedirs(file_path, exist_ok=True)
    folder_content = []
    ftp.retrlines(
        f'LIST {url_path}',
        lambda line: ftp_line_parse(
                                    line,
                                    folder_content))
    for folder, filename in folder_content:
        new_url_path = f"{url_path}{filename}/"
        new_file_path = os.path.join(file_path, filename)
        if folder:
            print(f"Searching {new_file_path}")
            file_tree(ftp, new_url_path, new_file_path, filters)
        else:
            print(f"Downloading {new_file_path}")
            download_file(ftp, new_url_path, new_file_path)
    