# -*- coding: utf-8 -*-
# !/usr/bin/env python3

from lxml import html
import requests
import BeautifulSoup

# Gestion de l'input
class InputArticle:
    def __init__(self, title, subtitle, full_text, keywords):
        self.title = title
        self.subtitle = subtitle
        self.full_text = full_text
        self.keywords = keywords

    def get_keywords(self):
        pass


# Trouver les articles dans lesquels les mots apparaissent (par la' (get_context))

def find_articles(query):

    root_url = 'http://www.letempsarchives.ch/recherche?q='
    url = root_url + query.replace(' ', '+')
    page = requests.get(url)
    html = page.text
    doc = BeautifulSoup(html)
    dates = doc.findAll('article-headliner')
    #tree = html.fromstring(page.content)
    #dates = tree.xpath("//h4[@class='article-headliner']/small/b/text()")
    print(dates)


# Compute TF-IDF sur ces articles


# from sklearn.feature_extraction.text import TfidfVectorizer
# corpus = ["This is very strange",
#           "This is very nice and nice but very nice"]
# vectorizer = TfidfVectorizer(min_df=1)
# X = vectorizer.fit_transform(corpus)
# idf = vectorizer.idf_
# print(dict(zip(vectorizer.get_feature_names(), idf)))

if __name__ == '__main__':
    find_articles('attentat paris')