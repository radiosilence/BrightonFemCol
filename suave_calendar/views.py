import datetime
import calendar

from django.http import Http404
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse

from suave.utils import get_page_from_url

from .models import Event


def home(request):
    try:
        page = get_page_from_url(request.path)
    except Http404:
        page = None
    return TemplateResponse(request, 'suave_calendar/calendar.html', {
        'title': 'Upcoming Events',
        'page': page,
        'events': Event.objects.future().order_by('start_date', 'start_time')
    })


def archive(request):
    try:
        page = get_page_from_url(request.path)
    except Http404:
        page = None

    return TemplateResponse(request, 'suave_calendar/calendar.html', {
        'title': 'Archived Events',
        'page': page,
        'events': Event.objects.past().order_by('-start_date', '-start_time')
    })


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

    return TemplateResponse(request, 'suave_calendar/event.html', {
        'event': event,    
    })