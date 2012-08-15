from django.http import Http404
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse

from suave.utils import get_page_from_url

from .models import Category, Article


def category(request, category=None):
    category = get_object_or_404(Category, slug=category)
    print category
    print category.articles.live().all()
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
    try:
        page = get_page_from_url(request.path)
    except Http404:
        page = None
    articles = Article.objects.published()[:7]
    return TemplateResponse(request, 'suave_press/home.html', {
        'title': 'Latest Articles',
        'page': page,
        'articles': articles,
        'first': articles[0]
    })
