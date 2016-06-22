# -*- coding: utf-8 -*-

import os

from webapp.core import scraper
from webapp.core import search_engine
from webapp.mock import mock_search_engine

MOCK = True if os.environ.get("WEBAPP_MOCK_SEARCH") == 'True' else False

def get_news_metadata(url):
    if MOCK:
        return mock_search_engine.get_news_by_url(url)

    real = scraper.scrape_article(url)
    return real

def get_archives_from_news(news):
    """ Return search engine matches (metadata dict) for a News article """
    if MOCK:
        return mock_search_engine.find_articles()

    article = scraper.scrape_article(news.url)
    keywords = search_engine.get_keywords(article['title'], article['subtitle'],
                                  article['article_body'])
    archives = search_engine.find_articles(keywords, 10)
    return archives

def get_archives_from_archive(archive):
    """ Return list search engine matches (metadata dict) for an Archive """
    if MOCK:
        return mock_search_engine.find_articles()

    # TODO!
    # - fetch metadata
    # - extract keywords
    # - search_engine.find_articles(keywords)
    return []

def get_keywords_from_news(news):
    keywords = search_engine.get_keywords(news.title, news.subtitle, news.body)
    return keywords


def get_archives_from_ids(ids):
    """ According to ID of archive, find its metadata

    :arg list ids: list of ids (our ids, prefixed with archive$$)

        can also be a single string.

    """
    if type(ids) == str:
        ids = [ids]

    ids_solr = [ id.partition("$$")[2] for id in ids ]

    if MOCK:
        return mock_search_engine.find_articles_by_ids(ids_solr)

    return search_engine.find_articles_by_id(ids_solr)

