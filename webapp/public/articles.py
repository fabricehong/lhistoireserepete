# -*- coding: utf-8 -*-
import os
import datetime

from webapp.core import search_engine
from webapp.core import scraper
from webapp.public import core_interface
from webapp.user.models import ArticleRelation

MOCK = True if os.environ.get("WEBAPP_MOCK_RELATIONS") == 'True' else False


def get_relations_by_id(id):
    """ Returns a list of all associated News/Archive IDs """

    if MOCK:
        ids = [
            'news$$http://www.letemps.ch/sciences/2016/06/18/traversee-atlantique-bertrand-piccard',
            'news$$http://www.letemps.ch/monde/2016/06/18/vaste-coup-filet'
            '-haute-tension-belgique',
            'archive$$JDG_1998_01_30#16#Ar01600',
            'archive$$JDG_1993_05_06#17#Ar01701',
            'archive$$JDG_1992_11_24#19#Ar01907',
        ]
        return [get_article(id) for id in ids]

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
            search_id = metadata["id"]
            our_id = "archive$${}".format(search_id)
            archive = Archive(our_id)
            archive.populate_from_metadata(metadata)
            archives.append(archive)
        return archives

    def get_user_recommendations(self):
        # For now just return a bunch of news:
        return get_relations_by_id(self.id)


class Archive:
    """
    Archive id format:

        archive$${id_solr}

    Where id_solr is the ID used for an archive in Solr. For example:

        archive$$JDG_1910_06_25#1#Ar00107

    From this ID we can lookup all the article metadata in Solr, and we can
    rebuild the webviewer URL on letempsarchive.ch.


    Two ways to initialize this class (after instantiation):

    1) If you already have metadata from the search engine:

        archive.populate_from_metadata(metadata)

    2) If you do not, you only have the ID:

        archive.populate_from_solr()

    """
    def __init__(self, id):
        parts = id.split(separator)
        self.id = id
        self.type = parts[0]
        self.id_solr = parts[1]
        self.doc_id, self.page, _ = self.id_solr.split('#')
        self.url = "http://www.letempsarchives.ch/page/%s/%s" % (
            self.doc_id, self.page)

        # TODO: replace these by properties, like in News
        self.title = ''
        self.date = ''
        self.newspaper = ''
        self.metadata = None

    def init_metadata(self):
        return self.populate_from_solr()

    def populate_from_metadata(self, metadata):
        """ Populate attributes from search engine's output metadata """
        self.title = metadata[u'title']
        self.date = metadata[u'meta_year_i']
        self.newspaper = metadata[u'meta_publisher_s']
        self.metadata = metadata

    def populate_from_solr(self):
        metadata = core_interface.get_archives_from_ids([self.id])[0]
        self.populate_from_metadata(metadata)

    def get_system_recommendations(self):
        # Get huge list of archive metadata from search engine
        archives_json = core_interface.get_archives_from_archive(self)

        # Convert to articles objects
        archives = []
        for metadata in archives_json:
            search_id = metadata["id"]
            our_id = "archive$${}".format(search_id)
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
        a = Archive(id)
        a.init_metadata()
        return a
    else:
        return News("news$$%s" % id)
