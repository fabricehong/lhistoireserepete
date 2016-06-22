# -*- coding: utf-8 -*-

import os
import json
import random

BASEDIR = os.path.abspath(os.path.dirname(__file__))


def find_articles():
    """ Return a previously acquired dump from the search engine """
    with open(os.path.join(BASEDIR, 'archive_recommendations.json'), 'r') as fo:
        archives = json.load(fo)
    return archives

def find_articles_by_ids(ids):
    """ Return a previoulsy acquired list of articles.

    ID is the Solr archive ID, not webapp ID. If ID doesn't match in the mock
    database, return a random article instead.
    """

    with open(os.path.join(BASEDIR, 'archive_recommendations.json'), 'r') as fo:
        archives = json.load(fo)

    id_lookup = dict((entry['id'], entry) for entry in archives)

    metadata = []
    for id in ids:
        if id in id_lookup:
            metadata.append(id_lookup[id])
        else:
            metadata.append(random.choice(archives))
    return metadata


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
        return random.choice(news)
