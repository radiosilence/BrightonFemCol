import datetime
from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse_lazy
from django.utils.timezone import utc

from model_utils import Choices
from model_utils.managers import PassThroughManager
from model_utils.fields import StatusField

from suave.models import Displayable, SiteEntityQuerySet, Image, Attachment
from suave.utils import get_default_image

from suave_discussion.models import Post, DISCUSSION_TYPE


class Category(Displayable):
    @property
    def articles(self):
        return Article.objects.published().filter(
            Q(category=self)
            | Q(categories__in=[self])
        ).order_by('-published')

    class Meta:
        verbose_name_plural = 'categories'


class ArticleQuerySet(SiteEntityQuerySet):
    def by_author(self, user):
        return self.filter(user=user)

    def published(self):
        now = datetime.datetime.utcnow().replace(tzinfo=utc)
        return self.live().filter(published__lte=now)

    def unpublished(self):
        now = datetime.datetime.utcnow().replace(tzinfo=utc)
        return self.filter(published__gte=now)


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
    category = models.ForeignKey(Category, related_name='primary_articles')
    categories = models.ManyToManyField(Category,
        related_name='secondary_articles', null=True, blank=True,
        verbose_name="extra categories")
    posts = models.ManyToManyField(Post, related_name='articles',
        null=True, blank=True)
    discussion_type = models.CharField(max_length=15,
        choices=DISCUSSION_TYPE, default=DISCUSSION_TYPE.open)

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
            return get_default_image()


class ArticleImage(Image):
    article = models.ForeignKey(Article, related_name='images')
    gallery = models.BooleanField(default=True)


class ArticleAttachment(Attachment):
    article = models.ForeignKey(Article, related_name='attachments')
