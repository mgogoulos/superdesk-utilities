# -*- coding: utf-8; -*-

import os
import time
import subprocess
import shlex
from superdesk.utc import utcnow
from uuid import uuid4

from superdesk.io.registry import register_feed_parser
from superdesk.io.feed_parsers import FeedParser

# simple video parser, to be used along with the
# Superdesk's file feeding service

# While Superdesk can ingest video items, they need to
# be specified somehow (as part of RSS or NewsML files).
# Moreover they end up being stored in MongoDB, as GridFS
# objects, and get served by the python app. This script
# provides an easy way to constantly ingest video files without writing
# XML files and serves them on a folder through nginx

# Will consider as valid only files with video types
# on VALID_VIDEO_FILES
# For each file, create a news item with file's name as
# the headline, and current datetime as date created (in utc)
# Then move original file to VIDEO_FOLDER , to be served by nginx.
# Nginx settings need be able to serve videos, with an entry similar
# to
# location /auto_import_media {
#    alias /var/www/auto_import/media;
# }

# Superdesk checks file dates so if it finds them to be
# older than 2 days, it ignores them - keep in mind in case
# timestamps are not correct when saving files to the file
# folder used for Ingestion.

# Superdesk needs to move the original file onto the _PROCESSED
# or _ERROR folders, so once we move the file to the VIDEO_FOLDER
# to be served by nginx, we create an empty file for Superdesk to
# move, otherwise it breaks. We don't want to copy files, since they could
# be big files, move works fine as well specially if the filesystem is
# the same (Superdesk ingest folder and VIDEO_FOLDER for files to be served)

# video folder to be served by nginx
VIDEO_FOLDER = '/var/www/auto_import/media'

VALID_VIDEO_FILES = ['mp4', 'mpg', 'ogv', 'flv', 'webm', 'mp3']


class SimpleVideoParser(FeedParser):
    NAME = 'simplevideo'

    label = 'Simple Video Parser'

    def can_parse(self, file_path):
        try:
            if file_path.split('.')[-1].lower() in VALID_VIDEO_FILES:
                return True
            else:
                return False
        except:
            return False

    def parse(self, file_path, provider):
        file_name = file_path.split('/')[-1]
        headline = file_name
        new_path = os.path.join(VIDEO_FOLDER, file_name)
        cmd = 'mv %s %s' % (file_path, new_path)
        cmd = shlex.split(cmd)
        output = subprocess.check_output(cmd)
        time.sleep(1)
        video_path = 'auto_import_media/' + file_name
        # this is the body for the news item, which is
        # just the video html tag with the source as the
        # video file path
        body = '''

<br>
<video controls="" height=400 width=500 src="%s"></video>
<br>

''' % video_path

        # create new file so that the file feeding service won't complain
        cmd = 'touch %s' % file_path
        cmd = shlex.split(cmd)
        output = subprocess.check_output(cmd)

        item = {}
        guid = str(uuid4())

        item = {
            'body_html': body,
            'headline': headline,
            'type': 'text',
            'versioncreated': utcnow(),
            'guid': guid
        }

        return item


register_feed_parser(SimpleVideoParser.NAME, SimpleVideoParser())
