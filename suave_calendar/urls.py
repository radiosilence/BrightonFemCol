from django.conf.urls.defaults import patterns, include, url

EVENT_PART = r'(?P<slug>[-\w]+)-(?P<month>[\w]+)-(?P<day>[\d]{2})-(?P<year>[\d]{4})/'

urlpatterns = patterns('suave_calendar.views',
    url(r'^' + EVENT_PART + r'$', 'event',
        name='event'),
    url(r'^archive/$', 'archive', name='archive'),
    url(r'^$', 'home', name='home'),
)