from django.contrib import admin

import reversion
from suave.admin import DatedAdmin
from .models import Post

class PostAdmin(DatedAdmin, reversion.VersionAdmin):
    pass

class PostInline(models.TabbedInline):
    model = Post
    extra = 0


admin.site.register(Post, PostAdmin)