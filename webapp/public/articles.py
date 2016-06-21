# -*- coding: utf-8 -*-
import os
import datetime

from webapp.core import search_engine
from webapp.core import scraper
from webapp.public import core_interface
from webapp.user.models import ArticleRelation

MOCK = True if os.environ.get("WEBAPP_MOCK_SEARCH") == 'True' else False

def get_relations_by_id(id):
    """ Returns a list of all associated News/Archive IDs """

    if MOCK:
        # Build some unrelated News articles, mix in some Archives:
        from webapp.mock.mock_search_engine import get_news
        news_metadata = get_news()

        articles = []
        for entry in news_metadata:
            article = News('news$$' + entry['source_url'])
            article.article_metadata = entry
            articles.append(article)

        # TODO: mix in some archives
        return articles

    # id1 -> id2 relations:
    relations = ArticleRelation.query.filter_by(article1_id=id).all()
    print "relations 1", relations
    ids = set(relation.article2_id for relation in relations)

    # id2 -> id1 relations:
    relations = ArticleRelation.query.filter_by(article2_id=id).all()
    print "relations 2", relations
    ids = ids.union(relation.article1_id for relation in relations)

    print ids

    return [get_article(id) for id in ids]


separator = "$$"
class News:
    def __init__(self, id):
        split_index = id.index(separator)
        self.id = id
        self.type = id[:split_index]
        self.url = id[split_index+2:]
        #self.url = "http://www.letemps.ch/economie/2016/06/16/bns-ne-croit-brexit-s-y-prepare"
        self.article_metadata = None

    def init_news_metadata(self):
        self.article_metadata = core_interface.get_news_metadata(self.url)

    @property
    def title(self):
        if (self.article_metadata is None):
            self.init_news_metadata()
        return self.article_metadata["title"]

    @property
    def subtitle(self):
        if (self.article_metadata is None):
            self.init_news_metadata()
        return self.article_metadata["subtitle"]

    @property
    def body(self):
        if (self.article_metadata is None):
            self.init_news_metadata()
        return self.article_metadata["article_body"]

    @property
    def date(self):
        if (self.article_metadata is None):
            self.init_news_metadata()
        return self.article_metadata["publication_date"]

    def get_system_recommendations(self):
        # big ol' JSON dump
        archives_json = core_interface.get_archives_from_news(self)

        # Convert to articles objects
        archives = []
        for metadata in archives_json:
            search_id = metadata["id"].split('#')[0]
            our_id = "archive$${}$${}".format(
                search_id,
                metadata[u'page_i'],
            )
            archive = Archive(our_id)
            archive.populate_from_metadata(metadata)
            archives.append(archive)
        return archives

    def get_user_recommendations(self):
        # For now just return a bunch of news:
        return get_relations_by_id(self.id)


class Archive:
    def __init__(self, id):
        parts = id.split(separator)
        self.id = id
        self.type = parts[0]
        self.url = "http://www.letempsarchives.ch/page/%s/%s" % (parts[1], parts[2])

        self.title = ''
        self.date = ''
        self.newspaper = ''

    def populate_from_metadata(self, metadata):
        """ Populate attributes from search engine's output metadata """
        self.title = metadata[u'title']
        self.date = metadata[u'meta_year_i']
        self.newspaper = metadata[u'meta_publisher_s']

    def get_system_recommendations(self):
        # big ol' JSON dump
        archives_json = core_interface.get_archives_from_archive(self)

        # Convert to articles objects
        archives = []
        for metadata in archives_json:
            search_id = metadata["id"].split('#')[0]
            our_id = "archive$${}$${}".format(
                search_id,
                metadata[u'page_i'],
            )
            archive = Archive(our_id)
            archive.populate_from_metadata(metadata)
            archives.append(archive)
        return archives

    def get_user_recommendations(self):
        return get_relations_by_id(self.id)

def get_article(id):
    parts = id.split(separator)
    article_type = parts[0]

    if article_type=="news":
        return News(id)
    elif article_type=="archive":
        return Archive(id)
    else:
        return News("news$$%s" % id)
