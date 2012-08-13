from django.conf.urls.defaults import patterns, include, url

CATEGORY_PART = r'(?P<category>[-\w]+)/'
ARTICLE_PART = r'(?P<article>[-\w]+)/'

urlpatterns = patterns('suave_press.views',
    url(r'^' + CATEGORY_PART + ARTICLE_PART + r'$', 'article',
        name='article'),
    url(r'^' + CATEGORY_PART + r'$', 'category',
        name='category'),
    url(r'^$', 'home', name='home'),
)