from models import Article, Category
from django.http import Http404


def get_category_from_slug(category_slug=None):
    if category_slug:
        try:
            category = Category.objects.live().get(slug=category_slug)
        except Category.DoesNotExist:
            raise Http404
    else:
        category = Category.object.live()[0]
    return category


def get_article_from_slug(article_slug):
    try:
        article = Article.objects.published().get(slug=article_slug)
    except Article.DoesNotExist:
        raise Http404
    return article
