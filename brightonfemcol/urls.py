from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
admin.autodiscover()
from django.views.generic.simple import direct_to_template

from suave.sitemap import PageSitemap
from suave_press.sitemap import PressSitemap
from suave_calendar.sitemap import CalendarSitemap

sitemaps = {
    'pages': PageSitemap(),
    'calendar': CalendarSitemap(),
    'press': PressSitemap(),
}
urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^articles/', include('suave_press.urls',
        namespace='suave_press')),
    url(r'^events/', include('suave_calendar.urls',
        namespace='suave_calendar')),
    (r'^tinymce/', include('tinymce.urls')),

    (r'^favicon\.ico$', 'django.views.generic.simple.redirect_to', {
        'url': settings.STATIC_URL + 'images/favicon.ico'
    }),

    (r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {
        'sitemaps': sitemaps
    }),
    
    (r'^robots\.txt$', direct_to_template,
     {'template': 'robots.txt', 'mimetype': 'text/plain'}),
    url(r'^', include('suave.urls', namespace='suave', app_name='suave')),
    (r'^grappelli/', include('grappelli.urls')),
)


if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
   )
