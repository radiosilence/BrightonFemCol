from django.contrib import admin

from suave.admin import DisplayableAdmin, ImageInline, OrderedInline

from .models import Event, EventImage, EventLink


class EventImageInline(ImageInline):
    model = EventImage


class EventLinkInline(OrderedInline):
    model = EventLink


class EventAdmin(DisplayableAdmin):
    inlines = (
        EventImageInline,
        EventLinkInline,
    )


admin.site.register(Event, EventAdmin)
