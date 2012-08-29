from django.db import models
from django.contrib.auth.models import User

from model_utils import Choices
from suave.models import Dated
from mptt.models import MPTTModel, TreeForeignKey


DISCUSSION_TYPE = Choices(
    ('open', 'Open (post shown, new posts enabled'),
    ('closed', 'Closed (posts shown, new posts disabled)'),
    ('disabled', 'Disabled (posts not shown)'),
)


class Post(MPTTModel, Dated):
    author = models.ForeignKey(User, related_name='posts')
    topic = models.BooleanField(default=False)
    parent = TreeForeignKey('self', null=True, blank=True,
        related_name='children')
    content = models.TextField()
