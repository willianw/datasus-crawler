# To-do:
# - Expand database exploration

from datasus import download
from datasus import database

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
                        
    parser.add_argument('subcommand', choices=['download', 'list', 'load', 'get'],
                        help='Subcomandos')

    #sub = parser.add_subparsers(help='Subcomandos')
    #sub.add_parser('download', help='obtém arquivos brutos da internet')
    #sub.add_parser('list', help='exibe informações sobre os arquivos brutos presentes')
    #sub.add_parser('load', help='converte os arquivos brutos para um formato desejado')
    #sub.add_parser('get', help='obtém arquivos e converte-os para o formato desejado.\n'
    #                          +'Equivalente a chamar "download" e "load" em sequência')

    parser.add_argument('-o', '--output_file', nargs=1,
                        help='Arquivo de saída')
    parser.add_argument('-base', type=str,
                        help='Bases de dados separadas por vírgula, ex.: SIASUS,SIHSUS,...')
    parser.add_argument('-ufs', type=str, help='UFs separadas por vírgula')
    parser.add_argument('-ano', type=str, help='Anos separados por vírgula ou em intervalo, ex.: 2014-2019')

    args = vars(parser.parse_args())


    
    print(args)

    if (args['output']):
        sys.stdout = open('stdout_file', 'w')

    
    if args['config-file']:
        with open(args['config-file'], 'r') as f:
            CONFIG = json.load(f)
    else:
        CONFIG = {
            "root_url":"ftp.datasus.gov.br",
            "root_directory":"dissemin/publicos/",			
            "download_folder":"data"
        }

    if False:
        # TO-DO: Implement filters logic based on CLI parameters
        CONFIG['filters'] = {'databases': ['SIHSUS'], 'uf':['SP']}
        download.start_download(CONFIG) # Gather below function in a single process
        database.extract_files('data', CONFIG['filters'])
