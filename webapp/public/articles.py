from webapp.scraperletemps import scraperletemps

separator = "$$"
class News:
    def __init__(self, id):
        split_index = id.index(separator)
        self.type = id[:split_index]
        self.url = id[split_index+2:]
        #self.url = "http://www.letemps.ch/economie/2016/06/16/bns-ne-croit-brexit-s-y-prepare"
        self.article_metadata = None

    def init_news_metadata(self):
        self.article_metadata = scraperletemps.scrape_article(self.url)

    @property
    def title(self):
        if (self.article_metadata is None):
            self.init_news_metadata()
        return self.article_metadata["title"]

    @property
    def subtitle(self):
        if (self.article_metadata is None):
            self.init_news_metadata()
        return self.article_metadata["subtitle"]

    @property
    def body(self):
        if (self.article_metadata is None):
            self.init_news_metadata()
        return self.article_metadata["article_body"]

class Archive:
    def __init__(self, id):
        parts = id.split(separator)
        self.type = parts[0]
        self.url = "http://www.letempsarchives.ch/page/%s/%s/%s" % (parts[1], parts[2], parts[3])

def get_article(id):
    parts = id.split(separator)
    article_type = parts[0]

    if article_type=="news":
        return News(id)
    elif article_type=="archive":
        return Archive(id)
    else:
        return News("news$$%s" % id)
