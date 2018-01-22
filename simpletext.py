# -*- coding: utf-8; -*-

import io
import hashlib

from superdesk.utc import utcnow
from superdesk.io.registry import register_feed_parser
from superdesk.io.feed_parsers import FeedParser

# Simple text parser, to be used along with
# Superdesk's file feeding service

# Opens a file, sets it's title
# as the first sentence, and then as body the
# whole text file
# date created is set as now - in utc time
# encoding is expected to be ISO-8859-1
# depending on the file format, regular expressions
# can be used to set a different title, or body


class SimpleTextParser(FeedParser):
    NAME = 'simptetext'

    label = 'Simple Text Parser'

    def can_parse(self, file_path):
        # this can be set to check file extention, eg only txt
        return True

    def parse(self, file_path, provider):
        f = io.open(file_path, mode="r", encoding="ISO-8859-1")
        txt = f.read()
        guid = hashlib.sha1(txt.encode('ISO-8859-1')).hexdigest()

        txt = txt.split('\n')
        headline = "%s" % txt[0]
        body = '<br>'.join(txt)

        item = {}

        item = {
            'body_html': body,
            'headline': headline,
            'type': 'text',
            'versioncreated': utcnow(),
            'guid': guid
            }

        return item


register_feed_parser(SimpleTextParser.NAME, SimpleTextParser())
