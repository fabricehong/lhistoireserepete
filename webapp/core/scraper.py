#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import date
from bs4 import BeautifulSoup
import requests
import re
from random import randint

# source_url = "http://www.letemps.ch/opinions/2016/06/15/fiscalite-entreprises-force-compromis"
# source_url = "http://www.letemps.ch/sport/2016/06/17/suspension-federation-russe-athletisme-maintenue"

#################################################
# ----------------- Functions ----------------- #
#################################################

def get_articles_en_continu():
	urlencontinu = "http://www.letemps.ch/en-continu/feed"
	sample_date = str(date.today())

	response = requests.get(urlencontinu)
	html = response.text
	doc = BeautifulSoup(html)

	# look for urls in the resulting doc 
	regex = "(http://www.letemps.ch/\w+/\d{4}/\d{2}/\d{2}/[\w-]+)"
	articles_urls = re.compile(regex).findall(doc.text) 

	return articles_urls

def get_random_article():
	articles_urls = get_articles_en_continu()

	return articles_urls[randint(0,len(articles_urls)-1)]

def get_todays_news():
    import random
    urls = ["http://www.letemps.ch/sciences/2016/06/18/traversee-atlantique-bertrand-piccard",
            "http://www.letemps.ch/monde/2016/06/18/vaste-coup-filet-haute-tension-belgique",
            "http://www.letemps.ch/economie/2016/06/17/presidents-grands-groupes-suisses-mieux-payes-monde",
            "http://www.letemps.ch/economie/2016/06/17/suisse-va-reprendre-discussions-inde",
            "http://www.letemps.ch/monde/2016/06/17/politique-migratoire-honteuse-europe-aura-plus-aucune-credibilite",
            "http://www.letemps.ch/sport/2016/06/17/roumanie-albanie-stade-yverdon-euro",
            "https://www.letemps.ch/economie/2016/06/16/bns-ne-croit-brexit-s-y-prepare"]
    url = random.choice(urls)
    return scrape_article(url)


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
