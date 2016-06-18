# -*- coding: utf-8 -*-
# !/usr/bin/env python3
import os

import requests
from nltk.tokenize import WordPunctTokenizer
import codecs
from titles import scrape_title_sparql_from_solr_doc
from scraper import get_todays_news


def file_full_path(filename):
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), filename)


# Trouver les keywords à partir d'un article input
# TODO : fonction qui trouve les mots clés dans un article
def get_keywords(title, subtitle, article_body):
    path = file_full_path('stopwords_fr.txt')
    stop_words = codecs.open(path, "r", "utf-8").read().split('\n')
    wpt = WordPunctTokenizer()

    def reduce_words(string_input):
        tokens = wpt.tokenize(string_input)
        return [t for t in tokens if t.lower() not in stop_words]

    key_words_output = []
    if title:
        key_words_output = reduce_words(title)
    elif subtitle:
        key_words_output = reduce_words(subtitle)
    elif article_body:
        key_words_output = reduce_words(article_body)
    return key_words_output


# Trouver les articles dans lesquels les mots apparaissent
def find_articles(key_words_input, n_articles):
    root_url = 'http://dhlabsrv8.epfl.ch:8983/solr/letemps_article/select?q='
    url = u"{root}{query}{parameters}".format(root=root_url,
                                              query=' OR '.join(key_words_input).replace(' ', '%20'),
                                              parameters='&wt=json&rows=' + str(n_articles))
    page = requests.get(url)
    json_page = page.json()
    response = json_page['response']
    docs = response['docs']
    for doc in docs:
        found_title = scrape_title_sparql_from_solr_doc(doc)
        if found_title and found_title != 'Untitled Article':
            doc['title'] = found_title
        else:
            doc['title'] = '# ' + ' '.join(doc['content_txt_fr'].split(' ')[0:5])
    return docs


# Rank articles using TF-IDF weights
def rank_articles(input_article, query_result_articles):

    # Define similarity
    def cosine_sim(text1, text2):
        tfidf = vectorizer.fit_transform([text1, text2])
        return (tfidf * tfidf.T).A[0, 1]

    # Compute TF-IDF on the articles
    wpt = WordPunctTokenizer()
    from sklearn.feature_extraction.text import TfidfVectorizer
    vectorizer = TfidfVectorizer(tokenizer=wpt.tokenize, ngram_range=range(1, 3))

    for query_result_article in query_result_articles:
        query_result_article['score'] = cosine_sim(input_article, query_result_article['content_txt_fr'])

    ranked_results = sorted(query_result_articles, key=lambda x: x['score'], reverse=True)

    rank = 0
    print(u'\nRank\tScore\tYear\tArticle title')
    for r in ranked_results:
        rank += 1
        print(u'#{rank}\t\t{score}\t{year}\t{content}'.format(rank=rank,
                                                              year=r['meta_year_i'],
                                                              score=str(r['score'])[0:6],
                                                              content=r['title']))

    return sorted(query_result_articles, key=lambda x: x['score'], reverse=True)

if __name__ == '__main__':

    # article = {}
    # article['title'] = u"La suspension de la Fédération russe d'athlétisme est maintenue"
    # article['subtitle'] = u'Depuis une vingtaine d’années, les confrontations sportives entre la Suisse et la France sont le reflet des tensions croissantes entre les deux pays. Le match de football, dimanche à Lille (21h), n’échappe pas à la règle'
    # article['article_body'] = u'Sur Twitter, Pierre Ménès et Granit Xhaka ont déjà lancé le match. «Les Suisses n’ont aucun talent. Si, en tennis», a ironisé le chroniqueur français, connu pour ses avis tranchés et ses jugements à l’emporte-pièce. «Nous parlerons après le match», lui a répondu, toujours sur Twitter, le milieu de terrain de l’équipe de Suisse Granit Xhaka.'
    #
    #
    # article['title'] = u'Vaste coup de filet et haute tension en Belgique'
    # article['subtitle'] = u"152 boxes de garage ont été vérifiés, 40 personnes interpellées. «Sans incident», dit la police qui refuse de donner des précisions sur la nature de l'enquête, sinon que la situation nécessitait une «intervention immédiate»"
    # article['article_body'] = u"Des dizaines de perquisitions nécessitant une «intervention immédiate» ont été menées dans la nuit de vendredi à samedi en Belgique dans le cadre d'un dossier de terrorisme, au moment où la protection de personnalités a été renforcée sur fond de menace de nouveaux attentats.«Les éléments recueillis dans le cadre de l'instruction nécessitaient d'intervenir immédiatement» explique le parquet fédéral qui centralise les enquêtes antiterroristes en Belgique.Les perquisitions se sont déroulées dans 16 communes principalement à Bruxelles mais aussi en Flandre et en Wallonie. Le parquet n'indique pas pourquoi il a agi si rapidement."

    article = get_todays_news()
    key_words = get_keywords(article['title'], article['subtitle'], article['article_body'])

    print(u'\nKey words deduced are :'.format(kw=key_words))
    for kw in key_words:
        print(kw)
    articles = find_articles(key_words, 14)
    print(u'\n{narticles} were found'.format(narticles=len(articles)))
    # for a in articles:
    #    print(a['content_txt_fr'][0:100])

    article_input = u'{title} {subtitle} {article_body}'.format(title=article['title'],
                                                                subtitle=article['subtitle'],
                                                                article_body=article['article_body'])
    rank_articles(article_input, articles)


