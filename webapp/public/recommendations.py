from webapp.arnaud import hackathon


def get_recommendations(article):
    if article.type=="news":
        keywords = hackathon.get_keywords(article.title, article.subtitle, article.body)
        articles = hackathon.find_articles(keywords)
        return articles
    elif article.type=="archive":
        return None
    else:
        return None
