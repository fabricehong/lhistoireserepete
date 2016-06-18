# -*- coding: utf-8 -*-
# !/usr/bin/env python3

import requests
from nltk.tokenize import WordPunctTokenizer
import codecs


# Trouver les keywords à partir d'un article input
# TODO : fonction qui trouve les mots clés dans un article
def get_keywords(input_article):
    stop_words = codecs.open('stopwords_fr.txt', "r", "utf-8").read().split('\n')
    wpt = WordPunctTokenizer()

    def reduce_words(string_input):
        tokens = wpt.tokenize(string_input)
        return [t for t in tokens if t.lower() not in stop_words]

    title = input_article['title']
    subtitle = input_article['subtitle']
    article_body = input_article['article_body']
    key_words_output = []
    if title:
        key_words_output = reduce_words(title)
    elif subtitle:
        key_words_output = reduce_words(subtitle)
    elif article_body:
        key_words_output = reduce_words(article_body)
    return key_words_output


# Trouver les articles dans lesquels les mots apparaissent
def find_articles(key_words_input):
    root_url = 'http://dhlabsrv8.epfl.ch:8983/solr/letemps_article/select?q='
    url = (root_url + ' OR '.join(key_words_input)).replace(' ', '%20') + '&wt=json'
    page = requests.get(url)
    json_page = page.json()
    response = json_page['response']
    docs = response['docs']
    # TODO : remove duplicates [dict(t) for t in set([tuple(d.items()) for d in l])]
    return docs


# Rank articles using TF-IDF weights
def rank_articles(input_article, query_result_articles):

    # Keep only the article' full text
    article_list = [doc['content_txt_fr'] for doc in query_result_articles]

    # Compute TF-IDF sur ces articles
    wpt = WordPunctTokenizer()
    from sklearn.feature_extraction.text import TfidfVectorizer
    vectorizer = TfidfVectorizer(tokenizer=wpt.tokenize, ngram_range=range(1,3))

    def cosine_sim(text1, text2):
        tfidf = vectorizer.fit_transform([text1, text2])
        return (tfidf * tfidf.T).A[0, 1]

    for query_result_article in article_list:
        query_result_article['score'] = cosine_sim(input_article, query_result_article)


if __name__ == '__main__':

    article = {}
    article['title'] = u"La suspension de la Fédération russe d'athlétisme est maintenue"
    article['subtitle'] = u'Depuis une vingtaine d’années, les confrontations sportives entre la Suisse et la France sont le reflet des tensions croissantes entre les deux pays. Le match de football, dimanche à Lille (21h), n’échappe pas à la règle'
    article['article_body'] = u'Sur Twitter, Pierre Ménès et Granit Xhaka ont déjà lancé le match. «Les Suisses n’ont aucun talent. Si, en tennis», a ironisé le chroniqueur français, connu pour ses avis tranchés et ses jugements à l’emporte-pièce. «Nous parlerons après le match», lui a répondu, toujours sur Twitter, le milieu de terrain de l’équipe de Suisse Granit Xhaka.'

    key_words = get_keywords(article)
    print(u'Key words deduced are {kw}'.format(kw=key_words))
    articles = find_articles(key_words)
    print(u'{narticles} were found'.format(narticles=len(articles)))
    for a in articles:
       print(a['content_txt_fr'][0:100])

    article_input = u'{title} {subtitle} {article_body}'.format(title=article['title'],
                                                                subtitle=article['subtitle'],
                                                                article_body=article['article_body'])
    rank_articles(article_input, articles)


