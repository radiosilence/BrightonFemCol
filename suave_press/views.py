from django.http import Http404
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.core.urlresolvers import reverse_lazy as reverse
from mptt.templatetags.mptt_tags import cache_tree_children
from suave.shortcuts import get_page_or_404


from .models import Category, Article


def category(request, category=None):
    category = get_object_or_404(Category, slug=category)
    return TemplateResponse(request, 'suave_press/category.html', dict(
        category=category,
        url=reverse('suave_press:category', kwargs={
            'category': category.slug
        })
    ))


def article(request, category=None, article=None):
    category = get_object_or_404(Category, slug=category)
    article = get_object_or_404(Article, slug=article, category=category)

    if article.status != Article.STATUS.live \
        and not request.user.has_perm('suave_press.view_article'):
        raise Http404

    posts = article.posts.all()
    cache_tree_children(posts)
    return TemplateResponse(request, 'suave_press/article.html', dict(
        category=category,
        article=article,
        posts=posts
    ))


def home(request):
    try:
        page = get_page_or_404(request)
    except Http404:
        page = None
    articles = Article.objects.published().order_by('-published')[:7]
    try:
        first = articles[0]
    except IndexError:
        first = None
    return TemplateResponse(request, 'suave_press/home.html', {
        'title': 'Latest Articles',
        'page': page,
        'articles': articles,
        'first': first,
        'url': reverse('suave_press:home'),
    })
