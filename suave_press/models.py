from datetime import datetime
from django.db import models
from django.contrib.auth.models import User

from model_utils.managers import PassThroughManager

from suave.models import Displayable, SiteEntityQuerySet


class Category(Displayable):
    pass


class ArticleQuerySet(SiteEntityQuerySet):
    def by_author(self, user):
        return self.filter(user=user)

    def published(self):
        return self.live().filter(published__lte=datetime.now())

    def unpublished(self):
        return self.filter(published__gte=datetime.now())


class Article(Displayable):
    published = models.DateTimeField()
    subtitle = models.CharField(max_length=255, null=True, blank=True)
    author = models.ForeignKey(User, related_name='articles')

    objects = PassThroughManager.for_queryset_class(ArticleQuerySet)()
