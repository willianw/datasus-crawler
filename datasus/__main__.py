# To-do:
# - Expand database exploration

from datasus import download
from datasus import database
from datasus import list_all

import subprocess
import argparse
import json
import sys
import os

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Ferramentas para o DATASUS')
    parser.add_argument('-f', '--config_file', nargs=1, metavar='<FILE>',
                        help='Arquivo de configurações')
                        
    parser.add_argument('subcommand', choices=['download', 'list', 'extract', 'load', 'get'],
                        help='Subcomandos')

    parser.add_argument('-o', '--output_file', nargs=1,
                        help='Arquivo de saída')
    parser.add_argument('-base', type=str,
                        help='Bases de dados separadas por vírgula, ex.: SIASUS,SIHSUS,...')
    parser.add_argument('-ufs', type=str, help='UFs separadas por vírgula')
    parser.add_argument('-ano', type=str, help='Anos separados por vírgula ou em intervalo, ex.: 2014-2019')

    args = vars(parser.parse_args())


    if (args['output_file']):
        sys.stdout = open('stdout_file', 'w')
    
    if args['config_file']:
        with open(args['config-file'], 'r') as f:
            CONFIG = json.load(f)
    else:
        CONFIG = {
            "root_url":"ftp.datasus.gov.br",
            "root_directory":"dissemin/publicos/",			
            "download_folder":"data"
        }

    # TO-DO: Implement filters logic based on CLI parameters
    CONFIG['filters'] = {'databases': ['SIHSUS']}
    CONFIG['filters'] = {'databases': ['SIHSUS', 'SIASUS'], 'ufs': ['SP', 'RJ', 'MG', 'ES']}
    
    # Switch Commands
    if args['subcommand'] == 'download':
        download.start_download(CONFIG) # Gather below function in a single process
    elif args['subcommand'] == 'extract':
        database.extract_files('data', CONFIG['filters'])
    elif args['subcommand'] == 'list':
        list_all.list_all(CONFIG)
