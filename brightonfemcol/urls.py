from django.conf import settings
from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.views.generic.base import TemplateView, RedirectView
admin.autodiscover()

from suave.sitemap import PageSitemap
from suave_press.sitemap import PressSitemap
from suave_calendar.sitemap import CalendarSitemap

class TextResponse(TemplateResponse):
    def __init__(self, *args, **kwargs):
        kwargs['mimetype'] = 'text/plain'
        return super(TextResponse, self).__init__(*args, **kwargs)

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
    (r'^accounts/', include('allauth.urls')),
    (r'^tinymce/', include('tinymce.urls')),

    (r'^favicon\.ico$', RedirectView.as_view(
        url=settings.STATIC_URL + 'images/favicon.ico'
    )),

    (r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {
        'sitemaps': sitemaps
    }),
    (r'^google38834dce68fed27f\.html$',
        lambda r: HttpResponse(
            'google-site-verification: google38834dce68fed27f.html'
        )
    ),
    
    (r'^robots\.txt$', TemplateView.as_view(
        template_name='robots.txt',
        response_class=TextResponse
    )),
    url(r'^', include('suave.urls', namespace='suave', app_name='suave')),
    (r'^grappelli/', include('grappelli.urls')),
)


if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
   )
