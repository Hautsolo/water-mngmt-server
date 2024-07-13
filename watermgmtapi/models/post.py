from django.db import models
from .user import User
from .category import Category
from .like import Like
from .tag import Tag
from django.utils import timezone


class Post(models.Model):

    title = models.CharField(max_length=150)
    image_url = models.CharField(max_length=150)
    description = models.CharField(max_length=150)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name='posts')
    tags = models.ForeignKey(Tag, on_delete=models.CASCADE)
    created_on = models.DateTimeField(default=timezone.now)

    @property
    def user_id(self):
        return self.user.id
