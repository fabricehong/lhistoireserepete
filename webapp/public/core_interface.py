# -*- coding: utf-8 -*-

from webapp.core import scraper
from webapp.core import search_engine

def get_news_metadata(url):

    mock = {
            "title" : "Mon titre",
            "subtitle" : "la police qui refuse de donner des précisions sur la nature de l'enquête",
            "article_body" : "Après rénovation, certains ont la capacité d'accueillir 50% d’habitants supplémentaires. Nous sommes prêts à accueillir la croissance là où il existe déjà un bon réseau de transports, c’est-à-dire, dans les zones construites, à condition de ne pas dénaturer les quartiers existants. Et, dans notre système démocratique, cela ne peut pas se faire sans l’approbation de la population"
        }
    real = scraper.scrape_article(url)
    return real


def get_archives_from_news(news):
    mock_archives = [
            {
             "date" : "date",
             "newspaper" : "newspaper",
             "title" : "title",
             "tags" : "termes en relation"
         },
        ]

    #keywords = get_keywords_from_news(news)
    #archives = search_engine.find_articles(keywords, 10)
    return mock_archives

def get_keywords_from_news(news):
    keywords = search_engine.get_keywords(news.title, news.subtitle, news.body)
    return keywords