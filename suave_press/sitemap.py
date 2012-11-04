from datetime import date

from django.contrib.sitemaps import Sitemap
from django.core.urlresolvers import reverse
from .models import Article, Category

try:
    LASTMOD = Article.objects.order_by('-updated')[0].updated
except:
    LASTMOD = date.today()


class PressSitemap(Sitemap):
    changefreq = 'daily'
    priority = 0.5

    def items(self):
        return list(Article.objects.published()) \
            + list(Category.objects.all()) \
            + [
                reverse('suave_press:home'),
            ]

    def lastmod(self, obj):
        if isinstance(obj, Article) or isinstance(obj, Category):
            return obj.updated
        else:
            return LASTMOD

    def location(self, obj):
        if isinstance(obj, Article):
            return obj.url
        elif isinstance(obj, Category):
            return reverse('suave_press:category', kwargs={
                'category': obj.slug
            })
        else:
            return obj
