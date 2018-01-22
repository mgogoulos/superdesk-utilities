# -*- coding: utf-8; -*-
#!/usr/bin/env python

import ftplib
import os.path

# This script can be set using crontab to check
# every X minutes on remote ftp server and fetch files
# so that Superdesk can ingest them using file feed service
# Useful in cases where Superdesk's ftp service cannot be used,
# eg on older ftp servers that do not support MLST

# connects to an ftp server, provided that
# credentials are correct. Then check into folders
# specified on FTP_PATHS and fetches files to
# WRITE_DIR. There's a check if files are already
# existing on DUPLICATES_DIR, meaning that Superdesk
# has already ingested them, in this case don't fetch them.
# files from the ftp server are saved to WRITE_DIR

WRITE_DIR = '/root/ftp_ingest_stuff'
DUPLICATES_DIR = '/root/ftp_ingest_stuff/_PROCESSED'
FTP_PATHS = ['project/folder1', 'project/folder2']
FTP_USERNAME = 'username'
FTP_PASSWORD = 'password'
FTP_HOST = 'ftp.example.com'

config = {
    'dest_path': '/tmp/',
    'password': FTP_PASSWORD,
    'field_aliases': [],
    'username': FTP_USERNAME,
    'passive': True,
    'host': FTP_HOST
}


ftp = ftplib.FTP(config.get('host'), timeout=300)
ftp.login(config.get('username'), config.get('password'))
# this will be the list of files to fetch
get_items = []

for ftp_path in FTP_PATHS:
    ftp_items = []
    ftp_path = '/%s/%s' % (FTP_USERNAME, ftp_path)
    ftp.cwd(ftp_path)
    # get files listing on list ftp_items
    ftp.retrlines('LIST', ftp_items.append)
    for item in ftp_items:
        # don't fetch empty files
        if item.split()[2] != '0':
            get_items.append(ftp_path+item.split()[3])

for i in get_items:
    file_name = i.split('/')[-1]
    out = os.path.join(WRITE_DIR, file_name)
    dup = os.path.join(DUPLICATES_DIR, file_name)

    try:
        # if file already fetched on WRITE_DIR, or in DUPLICATES_DIR
        # don't fetch
        if not (os.path.isfile(out) or os.path.isfile(dup)):
            with open(out, 'wb') as f:
                ftp.retrbinary('RETR ' + i, f.write)
    except:
        pass
