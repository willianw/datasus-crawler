from ftplib import FTP
ftp = FTP('ftp.datasus.org', timeout=3600000)
ftp.login()
ftp.cwd('dissemin/publicos/SIASUS/200801_/Dados/')
a = ftp.nlst()
print(len(a))
ftp.quit()