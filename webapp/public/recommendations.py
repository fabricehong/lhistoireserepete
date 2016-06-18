from webapp.core import search_engine

def get_recommendations(article):
    if article.type=="news":
        #keywords = search_engine.get_keywords(article.title, article.subtitle, article.body)
        # TODO : change this
        articles = search_engine.find_articles("accidents")
        return articles
    elif article.type=="archive":
        return None
    else:
        return None
