from django.contrib import admin

from suave.admin import (DisplayableAdmin, ImageInline, OrderedInline,
    AttachmentInline)

from .models import Event, EventImage, EventLink, Category, EventAttachment


class CategoryAdmin(DisplayableAdmin):
    pass


class EventImageInline(ImageInline):
    model = EventImage


class EventAttachmentInline(AttachmentInline):
    model = EventAttachment


class EventLinkInline(OrderedInline):
    model = EventLink


class EventAdmin(DisplayableAdmin):
    inlines = (
        EventImageInline,
        EventLinkInline,
        EventAttachmentInline,
    )


admin.site.register(Category, CategoryAdmin)
admin.site.register(Event, EventAdmin)
