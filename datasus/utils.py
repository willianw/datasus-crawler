import os
import re

def get_metadata(filename):
    """ Files are in format <DATABASE><UF><YEAR><MONTH>.dbc
    """
    path, _ = os.path.splitext(filename)
    parser = re.search(
        r'(?P<database>[A-Z]+)(?P<uf>[A-Z]{2})(?P<year>\d{2})(?P<month>\d{2})',
        os.path.basename(path).upper())
    if not parser:
        raise FileNotFoundError(f'Invalid file name format: {filename}')
    metadata = {
        field: parser.group(field)
        for field in ['database', 'uf', 'year', 'month']
    }
    metadata['filename'] = filename
    metadata['path'] = path
    return metadata