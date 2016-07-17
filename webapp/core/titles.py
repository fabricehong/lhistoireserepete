#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pymongo import MongoClient

import requests
from bs4 import BeautifulSoup


mongo_client = MongoClient('mongodb://hack2016:hack2016@ds011442.mlab.com:11442/archives')
db = mongo_client.archives
titles_collection = db.titles
#mongo_client = MongoClient('mongodb://hack2016:hack2016@ds011442.mlab.com:11442/archives')

def scrape_title_sparql_from_solr_doc(doc):
    article_id = get_article_id_from_solr_doc(doc)
    return scrape_title_sparql(article_id["journal"], article_id["date"], article_id["articlesubid"])

def get_archive_title(id):
    # mongodb://hack2016:hack2016@ds011442.mlab.com:11442/archives
    archive = titles_collection.find_one({'id': id})
    return archive

def get_article_id_from_solr_doc(doc):
    temp = doc["doc_s"].split("_")
    article_id = {
        "date": temp[1] + "-" + temp[2] + "-" + temp[3],  # "1991-04-22"#
        "journal": doc["meta_publisher_s"],  # "JDG"
        "articlesubid": doc["ar_s"]  # "Ar02302"
    }
    return article_id


# gets a title from the sparql endpoint using the three specified informations
# date format: "1991-04-22"
# journal is either "JDG" or "GDL"
# articlesubid must be of the form "Ar02302"
# !!! URL AND SPARQL REQUEST ARE HARDCODED: TEMPORARY IP-ADRESS -> to be improved, but works for hackathon
def scrape_title_sparql(journal, date, articlesubid):
    # !!! URL AND SPARQL REQUEST ARE HARDCODED: TEMPORARY IP-ADRESS -> to be improved, but works for hackathon
    # works, but gives html: article_url 	 = "http://159.100.249.152:8890/sparql?default-graph-uri=http%3A%2F%2F159.100.249.152%3A8080%2Fletemps-data&query=SELECT+STR%28%3Ftitle%29+AS+%3Ftitle+STR%28%3Fid%29+AS+%3Fid_article%0D%0AWHERE%7B%0D%0A%3Fp+a+lt-owl%3AArticleComponent+.%0D%0A%3Fp+dct%3Atitle+%3Ftitle+.%0D%0A%3Fp+lt-owl%3AinhouseId+%3Fid+.%0D%0A%3Fp+lt-owl%3AissueDate+%22"+ date+"T05%3A00%3A00%22%5E%5Exsd%3AdateTime+.%0D%0A%3Fp+lt-owl%3Apublication+%22"+journal+"%22%5E%5Exsd%3Astring+.%0D%0AFILTER%28regex%28str%28%3Fid%29%2C+%22"+articlesubid+"%22%29%29%0D%0A%7D%0D%0ALIMIT+10&format=text%2Fhtml&timeout=0&debug=on"
    # works, but gives title and id: article_url 	 = "http://159.100.249.152:8890/sparql?default-graph-uri=http%3A%2F%2F159.100.249.152%3A8080%2Fletemps-data&query=SELECT+STR%28%3Ftitle%29+AS+%3Ftitle+STR%28%3Fid%29+AS+%3Fid_article%0D%0AWHERE%7B%0D%0A%3Fp+a+lt-owl%3AArticleComponent+.%0D%0A%3Fp+dct%3Atitle+%3Ftitle+.%0D%0A%3Fp+lt-owl%3AinhouseId+%3Fid+.%0D%0A%3Fp+lt-owl%3AissueDate+%22"+ date+"T05%3A00%3A00%22%5E%5Exsd%3AdateTime+.%0D%0A%3Fp+lt-owl%3Apublication+%22"+journal+"%22%5E%5Exsd%3Astring+.%0D%0AFILTER%28regex%28str%28%3Fid%29%2C+%22"+articlesubid+"%22%29%29%0D%0A%7D%0D%0ALIMIT+10&timeout=0&debug=on"
    article_url = "http://159.100.249.152:8890/sparql?default-graph-uri=http%3A%2F%2F159.100.249.152%3A8080%2Fletemps-data&query=SELECT+STR%28%3Ftitle%29+AS+%3Ftitle%0D%0AWHERE%7B%0D%0A%3Fp+a+lt-owl%3AArticleComponent+.%0D%0A%3Fp+dct%3Atitle+%3Ftitle+.%0D%0A%3Fp+lt-owl%3AinhouseId+%3Fid+.%0D%0A%3Fp+lt-owl%3AissueDate+%22" + date + "T05%3A00%3A00%22%5E%5Exsd%3AdateTime+.%0D%0A%3Fp+lt-owl%3Apublication+%22" + journal + "%22%5E%5Exsd%3Astring+.%0D%0AFILTER%28regex%28str%28%3Fid%29%2C+%22" + articlesubid + "%22%29%29%0D%0A%7D%0D%0ALIMIT+10&timeout=0&debug=on"

    # The actual request
    # query = """SELECT STR(?title) AS ?title
    # WHERE{
    # ?p a lt-owl:ArticleComponent .
    # ?p dct:title ?title .
    # ?p lt-owl:inhouseId ?id .
    # ?p lt-owl:issueDate "1991-04-22T05:00:00"^^xsd:dateTime .
    # ?p lt-owl:publication "JDG"^^xsd:string .
    # FILTER(regex(str(?id), "Ar02302"))
    # }
    # LIMIT 10
    # """

    r = requests.get(article_url)

    bs = BeautifulSoup(r.text, "lxml")

    try:
        title = bs.find('literal').text
    except:
        title = ''

    return title

get_archive_title('JDG_1897_10_08#2#Ar00213')