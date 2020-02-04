from tqdm import tqdm as tqdm
import aiofiles
import asyncio
import ftplib
import os


def start(ftp_config: dict, urls: list, path: str):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(download_files(ftp_config, urls[:100], path))
    loop.close()

async def download_files(ftp_config: dict, urls: list, path: str):
    errors = []
    downloads = [
        asyncio.create_task(download_file(ftp_config, url, path))
        for url in urls
    ]
    for download in tqdm(asyncio.as_completed(downloads),
                         desc="Download do DATASUS",
                         total=len(downloads),
                         unit="Arquivos"):
        try:
            url = await download
        except Exception as exc:
            errors.append(urls)
    return errors

async def download_file(ftp_config: dict, url: str, path: str):
    filename = os.path.join(path, os.path.basename(url))
    if not os.path.exists(filename):
        def chunk(chk, fp):
            fp.write(chk)
            fp.flush()
        try:
            ftp = ftplib.FTP(ftp_config['ftp_host'])
            ftp.login()
            async with aiofiles.open(filename, 'wb') as f:
                ftp.retrbinary(f'RETR {url}', lambda c: chunk(c, f))
            ftp.quit()
        except Exception as e:
            print(e)
    return url