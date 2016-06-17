#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import date
from bs4 import BeautifulSoup
import requests

#################################################
# ----------------- Functions ----------------- #
#################################################

def get_todays_news():
	return scrapeArticle("http://www.letemps.ch/economie/2016/06/16/bns-ne-croit-brexit-s-y-prepare")

# Scrape an article from Le Temps, starting from a URL
# exemple de input: http://www.letemps.ch/opinions/2016/06/16/histoire-une-bretelle-soutien-gorge
# balises d'intérêt:
# - div with class=article_body -> texte de l'article
# - p with class=lead -> sous-titre
# - balise span dans balise h1 -> titre de l'article
def scrapeArticle(source_url):
	sample_date = str(date.today())

	response = requests.get(source_url)
	html = response.text
	doc = BeautifulSoup(html)

	title = doc.find('h1')
	subtitle = doc.find('p', class_='lead')
	article_body = doc.find('div', class_='article_body').findChildren(recursive=False)[1]

	themes = doc.find('a', href_='/theme/*')

	article = {
			'source_url': source_url,
			'sample_date': sample_date,
			'title': title,		
			'subtitle': subtitle,
			'article_body': article_body
		}

	return article

#################################################
# ------------------ Script ------------------- #
#################################################

