import datetime

from django.template.response import TemplateResponse
from django.shortcuts import get_object_or_404

from .models import Event


def calendar(request):
    return TemplateResponse(request, 'suave_calendar/calendar.html', {

    })


def event(request, year, month, day, slug):
    start = datetime.date(int(year), int(month), int(day))
    event = get_object_or_404(Event, slug=slug, start_date=start)

    return TemplateResponse(request, 'suave_calendar/event.html', {
        'event': event,    
    })