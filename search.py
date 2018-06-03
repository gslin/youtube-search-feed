#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import feedgen.feed
import html
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

    body = lxml.html.fromstring(r.text)

    for item in body.cssselect('ol.item-section div.yt-lockup-video'):
        try:
            a = item.cssselect('a[title].spf-link')[0]

            # link
            link = a.get('href')
            if '/' == link[0]:
                link = 'https://www.youtube.com' + link

            # img
            link_tuple = urllib.parse.urlparse(link)
            d = urllib.parse.parse_qs(link_tuple[4])
            img = 'https://i.ytimg.com/vi/' + d['v'][0] + '/hqdefault.jpg'

            # title
            title = a.get('title')

            # content
            content = '%s<br/><img alt="%s" src="%s"/>' % (html.escape(title), html.escape(title), html.escape(img))

            entry = feed.add_entry()
            entry.content(content, type='xhtml')
            entry.id(link)
            entry.title(title)
            entry.link(href=link)

        except IndexError:
            pass

    print(str(feed.atom_str(), 'utf-8'))

if __name__ == '__main__':
    magic(sys.argv[1])
