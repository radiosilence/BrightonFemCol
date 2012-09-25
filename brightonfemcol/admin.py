from django.contrib import admin
from .models import (TwitterAccount, Tweet,)


class TweetInline(admin.TabularInline):
    model = Tweet


class TwitterAccountAdmin(admin.ModelAdmin):
    inlines = (TweetInline,)


admin.site.register(TwitterAccount, TwitterAccountAdmin)
