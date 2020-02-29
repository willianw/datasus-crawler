from tqdm import tqdm as tqdm
import aiofiles
import asyncio
import ftplib
import os

class Worker:

    def __init__(self, func, n=3):
        self.func = func
        self.queue = asyncio.Queue()
        self.semaphore = asyncio.Semaphore(n)

    def put(self, *args):
        self.queue.put_nowait(args)

    async def run(self):
        while True:
            args = await self._get()
            if args is None:
                return
            asyncio.ensure_future(self._target(args))

    async def _get(self):
        get_task = asyncio.ensure_future(self.queue.get())
        join_task = asyncio.ensure_future(self.queue.join())
        await asyncio.wait([get_task, join_task], return_when='FIRST_COMPLETED')
        if get_task.done():
            return get_task.result()

    async def _target(self, args):
        try:
            async with self.semaphore:
                return await self.func(*args)
        finally:
            self.queue.task_done()


def start(ftp_config: dict, urls: list, path: str):
    worker = Worker(download_file, 10)
    for url in urls:
        worker.put(ftp_config, url, path)
    worker.run()
    
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
                await ftp.retrbinary(f'RETR {url}', lambda c: chunk(c, f))
            ftp.quit()
        except Exception as e:
            print(e)
    return url