from django.contrib import admin

from suave.admin import DisplayableAdmin

from .models import Category, Article


class ArticleAdmin(DisplayableAdmin):
    exclude = ('sort_index',)


class CategoryAdmin(DisplayableAdmin):
    pass


admin.site.register(Category, CategoryAdmin)
admin.site.register(Article, ArticleAdmin)
