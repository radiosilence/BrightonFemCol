import datetime
import calendar

from django.http import Http404
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse

from .models import Event


def home(request):
    return TemplateResponse(request, 'suave_calendar/calendar.html', {

    })


def event(request, year, month, day, slug):
    try:
        month = dict(
            (v.lower(),k) for k,v in enumerate(calendar.month_name))[month]
    except KeyError:
        raise Http404
    start = datetime.date(int(year), month, int(day))
    event = get_object_or_404(Event, slug=slug, start_date=start)

    return TemplateResponse(request, 'suave_calendar/event.html', {
        'event': event,    
    })