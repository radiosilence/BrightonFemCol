from django.contrib import admin

import reversion

from suave.admin import DatedAdmin
from mptt.admin import MPTTModelAdmin

from .models import Post

class PostAdmin(MPTTModelAdmin, DatedAdmin, reversion.VersionAdmin):
    pass

class PostInline(admin.TabularInline):
    model = Post
    extra = 0


admin.site.register(Post, PostAdmin)