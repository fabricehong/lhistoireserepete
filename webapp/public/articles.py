
separator = "$$"
class News:
    def __init__(self, id):
        split_index = id.index(separator)
        self.type = id[:split_index]
        self.url = id[split_index+2:]
        self.url = "http://www.letemps.ch/economie/2016/06/16/bns-ne-croit-brexit-s-y-prepare"

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
