from django.http import Http404
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse

from .models import Category, Article


def category(request, category=None):
    category = get_object_or_404(Category, slug=category)

    return TemplateResponse(request, 'suave_press/category.html', dict(
        category=category
    ))

def article(request, category=None, article=None):
    category = get_object_or_404(Category, slug=category)
    article = get_object_or_404(Article, slug=article, category=category)

    if article.status != Article.STATUS.live \
        and not request.user.is_staff:

        raise Http404

    return TemplateResponse(request, 'suave_press/article.html', dict(
        category=category,
        article=article
    ))

def home(request):
    return TemplateResponse(request, 'suave_press/home.html', {})
