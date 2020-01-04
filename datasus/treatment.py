# Methods to work with datasets specifitivities.
# For instance, the root folder for each dataset is different. There isn't any general rule
# If needed, it must implement class heritage to treat different datasets.

import os

def get_ftp_start_node(dataset, table, start_url):
    """ Get path for data in DATASUS FTP system
    """
    if   dataset in ['SIASUS', 'SIHSUS']:
        url = os.path.join('200801_', 'Dados')
    elif dataset in ['SIM']:
        suffix = 'DORES' if table == 'DO' else 'DOFET'
        url = os.path.join('CID10', suffix)
    elif dataset in ['CMD']:
        url = os.path.join('DadosSISAB')
    elif dataset in ['SINAN']:
        url = os.path.join('DADOS', 'FINAIS')
    elif dataset in ['SINASC']:
        url = os.path.join('NOV', 'DNRES')
    else:
        url = os.path.join('Dados')

    return os.path.join(start_url, dataset, url)