import babylon

from .models import Article

class ArticleCache(babylon.Cache):
    model = Article

babylon.register(ArticleCache, parents=['PageCache'])