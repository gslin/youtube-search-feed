#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import feedgen.feed
import lxml.html
import requests
import sys
import urllib

def magic(keyword):
    url = 'https://www.youtube.com/results?sp=CAI%%253D&search_query=%s' % (urllib.parse.quote_plus(keyword))

    r = requests.get(url);

    title = 'YouTube Search - %s' % (keyword)

    feed = feedgen.feed.FeedGenerator()
    feed.author({'name': 'YouTube Search Feed Generator'})
    feed.id(url)
    feed.link(href=url, rel='alternate')
    feed.title(title)

    html = lxml.html.fromstring(r.text)

    # FIXME

    print(str(feed.atom_str(), 'utf-8'))

if __name__ == '__main__':
    magic(sys.argv[1])
