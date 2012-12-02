from django.contrib import admin

from suave.admin import DisplayableAdmin, ImageInline, AttachmentInline

from .models import Category, Article, ArticleImage, ArticleAttachment


class ArticleAttachmentInline(AttachmentInline):
    model = ArticleAttachment


class ArticleImageInline(ImageInline):
    model = ArticleImage


class ArticleAdmin(DisplayableAdmin):
    inlines = (
        ArticleImageInline,
        ArticleAttachmentInline,
    )
    list_display = ('__unicode__', 'published', 'subtitle', 'status', 'category',)
    list_editable = ('published', 'status', 'category')

class CategoryAdmin(DisplayableAdmin):
    pass


admin.site.register(Category, CategoryAdmin)
admin.site.register(Article, ArticleAdmin)
