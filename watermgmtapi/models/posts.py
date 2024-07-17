from django.db import models
from .user import User
from .category import Category
from .like import Like
from .tag import Tag
from django.utils import timezone


class Post(models.Model):

    title = models.CharField(max_length=150)
    image_url = models.URLField(max_length=200)
    description = models.CharField(max_length=150)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    # likes = models.ManyToManyField(Like, through='PostLike', related_name='posts')
    tags = models.ManyToManyField(Tag, through='PostTag', related_name="posts")
    created_on = models.DateTimeField(default=timezone.now)

    @property
    def user_id(self):
        return self.user.id
