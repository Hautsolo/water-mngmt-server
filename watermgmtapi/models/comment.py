from django.db import models
from .user import User
from .post import Post
from django.utils import timezone


class Comment(models.Model):

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.CharField(max_length=150)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_on = models.DateTimeField(default=timezone.now)
