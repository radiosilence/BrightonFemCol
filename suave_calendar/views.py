import datetime
import calendar

from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.core.urlresolvers import reverse_lazy as reverse

from jimmypage.cache import cache_page
from suave.models import Page
from .models import Event


@cache_page
def home(request):
    try:
        page = get_object_or_404(Page, url=request.path)
    except Http404:
        page = None
    return render(request, 'suave_calendar/calendar.html', {
        'title': 'Upcoming Events',
        'page': page,
        'events': Event.objects.future().order_by('start_date', 'start_time'),
        'url': reverse('suave_calendar:home'),
    })


@cache_page
def archive(request):
    try:
        page = get_object_or_404(Page, url=request.path)
    except Http404:
        page = None

    return render(request, 'suave_calendar/calendar.html', {
        'title': 'Archived Events',
        'page': page,
        'events': Event.objects.past().order_by('-start_date', '-start_time'),
        'url': reverse('suave_calendar:archive'),
    })


@cache_page
def event(request, year, month, day, slug):
    try:
        month = dict(
            (v.lower(),k) for k,v in enumerate(calendar.month_name))[month]
    except KeyError:
        raise Http404
    start = datetime.date(int(year), month, int(day))
    event = get_object_or_404(Event, slug=slug, start_date=start)
    if event.status != Event.STATUS.live \
        and not request.user.has_perm('suave_calendar.view_event'):
        raise Http404

    return render(request, 'suave_calendar/event.html', {
        'event': event,    
    })