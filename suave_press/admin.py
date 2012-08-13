from django.contrib import admin

from suave.admin import DisplayableAdmin, ImageInline

from .models import Category, Article, ArticleImage


class ArticleImageInline(ImageInline):
    model = ArticleImage


class ArticleAdmin(DisplayableAdmin):
    inlines = (
        ArticleImageInline,
    )


class CategoryAdmin(DisplayableAdmin):
    pass


admin.site.register(Category, CategoryAdmin)
admin.site.register(Article, ArticleAdmin)
