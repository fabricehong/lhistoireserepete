# -*- coding: utf-8 -*-
from webapp.core import search_engine
from webapp.core import scraper
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
        #self.article_metadata = scraper.scrape_article(self.url)
        self.article_metadata = {
            "title" : "Mon titre",
            "subtitle" : "la police qui refuse de donner des précisions sur la nature de l'enquête",
            "article_body" : "Après rénovation, certains ont la capacité d'accueillir 50% d’habitants supplémentaires. Nous sommes prêts à accueillir la croissance là où il existe déjà un bon réseau de transports, c’est-à-dire, dans les zones construites, à condition de ne pas dénaturer les quartiers existants. Et, dans notre système démocratique, cela ne peut pas se faire sans l’approbation de la population"
        }

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
        #articles = search_engine.find_articles("accidents")
        articles = [
            {
             "date" : "date",
             "newspaper" : "newspaper",
             "title" : "title",
             "tags" : "termes en relation",
             "type": "news",
         },
        ]
        return articles

    def get_user_recommendations(self):
        return get_relations_by_id(self.id)

class Archive:
    def __init__(self, id):
        parts = id.split(separator)
        self.id = id
        self.type = parts[0]
        self.url = "http://www.letempsarchives.ch/page/%s/%s/%s" % (parts[1], parts[2], parts[3])

def get_article(id):
    parts = id.split(separator)
    article_type = parts[0]

    if article_type=="news":
        return News(id)
    elif article_type=="archive":
        return Archive(id)
    else:
        return News("news$$%s" % id)
