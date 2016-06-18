# -*- coding: utf-8 -*-
from webapp.core import search_engine
from webapp.core import scraper
from webapp.public import core_interface
from webapp.user.models import ArticleRelation


def get_relations_by_id(id):
    """ Returns a list of all associated News/Archive IDs """

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

    def get_system_recommendations(self):
        return [
            Archive(id='archive$$JDG_1981_12_12$$7', metadata={
                u'title': u"CONVENTIONS EN FAVEUR DE L'INDUSTRIE " \
                           u"D'EXPORTATION La BNS n'accédera certainement pas à la requete des horlogers suisses",
                u'meta_year_i': 1981,
                u'meta_publisher_s': 'JDG',
            })
        ]
        articles = core_interface.get_archives_from_news(self)
        print articles
        ids = ["archive$$" + article[u'id'] for article in articles]
        return [
            get_article(
                "archive$$" + article[u'doc_s'] + "$$" + str(article[u'page_i']),
                article,
            ) for article in articles]

    def get_user_recommendations(self):
        return get_relations_by_id(self.id)

class Archive:
    def __init__(self, id, metadata={u'title': 'Titre'}):
        parts = id.split(separator)
        self.id = id
        self.type = parts[0]
        self.url = "http://www.letempsarchives.ch/page/%s/%s" % (parts[0], parts[1])
        self.title = metadata[u'title']

        self.date = metadata[u'meta_year_i']
        self.newspaper = metadata[u'meta_publisher_s']

def get_article(id, metadata={}):
    parts = id.split(separator)
    article_type = parts[0]

    if article_type=="news":
        return News(id)
    elif article_type=="archive":
        return Archive(id, metadata)
    else:
        return News("news$$%s" % id)
