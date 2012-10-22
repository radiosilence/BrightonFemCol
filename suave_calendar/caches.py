import babylon

from .models import Event

class EventCache(babylon.Cache):
    model = Event

babylon.register(EventCache, parents=['PageCache'])