from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse_lazy

from model_utils import Choices
from model_utils.managers import PassThroughManager
from model_utils.fields import StatusField

from suave.models import Displayable, SiteEntityQuerySet, Image


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
    STATUS = Choices(
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('live', 'Live'),
        ('deleted', 'Deleted')
    )

    subtitle = models.CharField(max_length=255, null=True, blank=True)
    published = models.DateTimeField()
    author = models.ForeignKey(User, related_name='articles')
    category = models.ForeignKey(Category, related_name='category')
    categories = models.ManyToManyField(Category, related_name='articles',
        null=True, blank=True, verbose_name="extra categories")

    objects = PassThroughManager.for_queryset_class(ArticleQuerySet)()

    @property
    def url(self):
        return self.get_absolute_url()

    def get_absolute_url(self):
        return reverse_lazy('suave_press:article', kwargs={
            'article': self.slug,
            'category': self.category.slug,
        })

    @property
    def image(self):
        try:
            return self.images.all()[0]
        except IndexError:
            return None


class ArticleImage(Image):
    article = models.ForeignKey(Article, related_name='images')
    gallery = models.BooleanField(default=True)
