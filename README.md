# superdesk-utilities

A collection of Superdesk utilities.


## simple_video.py
A simple video parser, to be used along with the Superdesk's file feeding service.

While Superdesk can ingest video items, they need to be specified somehow (as part of RSS or NewsML files).
Moreover they end up being stored in MongoDB, as GridFS objects, and get served by the python app.
This script provides an easy way to constantly ingest video files without writing XML files and serves them on a folder through nginx

To use::

Edit file and specify VALID_VIDEO_FILES plus VIDEO_FOLDER, as the folder video files will be moved and be served by nginx.

Then make sure nginx can serve video files for that folder, eg:

```
location /auto_import_media {
    alias /var/www/auto_import/media;
}
```
copy file simple_video.py to /opt/superdesk/env/src/superdesk-core/superdesk/io/feed_parsers/simplevideo.py
then edit /opt/superdesk/env/src/superdesk-core/superdesk/io/feed_parsers/__init__.py and append

```
from superdesk.io.feed_parsers.simplevideo import SimpleVideoParser
```

Superdesk needs restart

```
root@sd-primary:~# systemctl restart superdesk
```

Now enter the Ingest settings, select 'file feeding service', 'Simple Video Parser' as the parser, and specify the local directory where video files are initially stored. Superdesk will move these files to the VIDEO_FOLDER specified on the script


## simple_text.py

A simple text parser, to be used along with Superdesk's file feeding service. In case you have text files that need to be imported.


To use::

copy file simple_video.py to /opt/superdesk/env/src/superdesk-core/superdesk/io/feed_parsers/simpletext.py
then edit /opt/superdesk/env/src/superdesk-core/superdesk/io/feed_parsers/__init__.py and append

```
from superdesk.io.feed_parsers.simplevideo import SimpleTextParser
```

Superdesk needs restart

```
root@sd-primary:~# systemctl restart superdesk
```

Now enter the Ingest settings, select 'file feeding service', 'Simple Text Parser' as the parser, and specify the local directory where text files are initially stored.


## ftp_to_local_dir.py

This script can be set using crontab to check every X minutes on remote ftp server and fetch files
so that Superdesk can ingest them using file feed service.
Useful in cases where Superdesk's ftp service cannot be used,
 eg on older ftp servers that do not support MLST (as Microsoft Ftp server)


To use::

edit ftp_to_local_dir.py and set credentials to communicate with the ftp server (FTP_USERNAME/PASSWORD/HOST/PATHS)

Then add a crontab entry for the script to run every X minutes. Eg to run every 5 minutes, add this entry through `crontab -e`

```
*/5 * * * * /opt/superdesk/ftp_to_local_dir.py
```

Every time script runs it fetches files on WRITE_DIR dir, which is `/root/ftp_ingest_stuff` by default.


## image_sample.xml

This is just a sample image NewsML2 file that can be used to generate images found on a directory. Superdesk file feed service along with the NewsML 2 parser will ingest it and create a news item. Using a script we can create a similar xml file for all images located on a directory.
Image import can take place either specifying a remote url (as in the case of this sample file) or by specifying the path on the filesystem.
