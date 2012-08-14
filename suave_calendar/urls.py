from django.conf.urls.defaults import patterns, include, url

EVENT_PART = r'(?P<year>[\d]{4})/(?P<month>[\d]{2})/(?P<day>[\d]{2})/(?P<slug>[-\w]+)/'

urlpatterns = patterns('suave_press.views',
    url(r'^' + EVENT_PART + r'$', 'event',
        name='article'),
    url(r'^$', 'calendar', name='calendar'),
)