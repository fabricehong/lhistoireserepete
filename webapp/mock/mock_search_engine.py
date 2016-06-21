# -*- coding: utf-8 -*-

import os
import json

BASEDIR = os.path.abspath(os.path.dirname(__file__))


def find_articles():
    """ Return a previously acquired dump from the search engine """
    with open(os.path.join(BASEDIR, 'archive_recommendations.json'), 'r') as fo:
        archives = json.load(fo)
    return archives


def get_news():
    """ Return a bunch of scraped news metadata """
    with open(os.path.join(BASEDIR, 'news_dump.json'), 'r') as fo:
        news = json.load(fo)
    return news


def get_news_by_url(url):
    """ Return corresponding news metadata, or random one otherwise"""

    news = get_news()
    url_lookup = dict((entry['source_url'], entry) for entry in news)

    if url in url_lookup.keys():
        return url_lookup[url]
    else:
        import random
        return random.choice(news)
