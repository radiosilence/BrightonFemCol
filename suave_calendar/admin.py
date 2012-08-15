from django.contrib import admin

from suave.admin import DisplayableAdmin, ImageInline, OrderedInline

from .models import Event, EventImage, EventLink, Category


class CategoryAdmin(DisplayableAdmin):
    pass


class EventImageInline(ImageInline):
    model = EventImage


class EventLinkInline(OrderedInline):
    model = EventLink


class EventAdmin(DisplayableAdmin):
    inlines = (
        EventImageInline,
        EventLinkInline,
    )


admin.site.register(Category, CategoryAdmin)
admin.site.register(Event, EventAdmin)
