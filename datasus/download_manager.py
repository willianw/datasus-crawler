from tqdm import tqdm as tqdm
import aiofiles
import asyncio
import ftplib
import os


def start(ftp_config: dict, urls: list, path: str):
    errors = []
    for url in tqdm(urls,
                    desc="Download do DATASUS",
                    total=len(urls),
                    unit="Arquivos"):
        try:
            download_file(ftp_config, url, path)
        except Exception as exc:
            errors.append(urls)
    return errors

def download_file(ftp_config: dict, url: str, path: str):
    filename = os.path.join(path, os.path.basename(url))
    if not os.path.exists(filename):
        try:
            ftp = ftplib.FTP(ftp_config['ftp_host'])
            ftp.login()
            with open(filename, 'wb') as f:
                ftp.retrbinary(f'RETR {url}', f.write)
            ftp.quit()
        except Exception as e:
            print(e)
    return url