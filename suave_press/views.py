from django.http import Http404
from django.template.response import TemplateResponse

from .models import Category, Article

from .utils import get_category_from_slug, get_article_from_slug


def view_category(request, category_slug=None):
    category = get_category_from_slug(category_slug)

    return TemplateResponse('suave_press/category.html', dict(
        category=category
    ))

def view_article(request, category_slug=None, article_slug=None):
    category = get_category_from_slug(category_slug)
    article = get_article_from_slug(article_slug)

    return TemplateResponse('suave_press/article.html', dict(
        category=category,
        article=article
    ))
