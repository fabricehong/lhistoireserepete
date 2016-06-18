#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import date
from bs4 import BeautifulSoup
import requests
import re


# source_url = "http://www.letemps.ch/opinions/2016/06/15/fiscalite-entreprises-force-compromis"
# source_url = "http://www.letemps.ch/sport/2016/06/17/suspension-federation-russe-athletisme-maintenue"

#################################################
# ----------------- Functions ----------------- #
#################################################

def get_todays_news():
	return scrape_article("http://www.letemps.ch/economie/2016/06/16/bns-ne-croit-brexit-s-y-prepare")


# Scrape an article from Le Temps, starting from a URL
# exemple de input: http://www.letemps.ch/opinions/2016/06/16/histoire-une-bretelle-soutien-gorge
# balises d'interet:
# - div with class=article_body -> texte de l'article
# - p with class=lead -> sous-titre
# - balise span dans balise h1 -> titre de l'article


def scrape_article(source_url):
    sample_date = str(date.today())

    response = requests.get(source_url)
    html = response.text
    doc = BeautifulSoup(html)

    title = doc.find('h1').text
    subtitle = doc.find('p', class_='lead', text=True).text
    # article_body = doc.find('div', class_='article_body').findChildren(recursive=False)[1]
    article_body = doc.find('div', class_='article_body').findChildren(recursive=False)[1].findAll(text=True)
    article_body = ' '.join(article_body)
    article_info = doc.find('section', class_='article-info')

    # reading_time
    reading_time = "unknown"
    try:
        reading_time = article_info.find('p', class_='reading-time', text=True).strip()
    except:
        reading_time = "unknown"

    # author
    author = "unknown"
    try:
        author = article_info.find('a', class_='article-author', text=True).strip()
    except:
        author = "unknown"

    # themes
    themes = []

    def get_text(a):
        return a.getText()

    try:
        da = article_info.findAll('b')
        themes = []
        for d in da:
            themes.append(d)
    except:
        themes = []

    # publication date
    publication_date = "unknown"
    try:
        ai_children = article_info.findChildren(recursive=False)
        m = re.search(u".*Publi\xe9 (.*)", ai_children[2].text)
        if m:
            publication_date = m.group(1)
    except:
        publication_date = "unknown"

    article = {
        'source_url': source_url,
        'sample_date': sample_date,
        'title': title,
        'subtitle': subtitle,
        'article_body': article_body,
        'reading_time': reading_time,  # not present on all articles, default: "unknown"
        'themes': themes,  # not present on all articles, default: []
        'author': author,  # not present on all articles, default: "unknown"
        'publication_date': publication_date  # not present on all articles, default: "unknown"
    }

    return article

#################################################
# ------------------ Script ------------------- #
#################################################
