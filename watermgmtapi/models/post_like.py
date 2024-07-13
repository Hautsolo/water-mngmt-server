from django.db import models
from .user import User
from .post import Post
from .like import Like

class PostLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    like = models.ForeignKey(Like, on_delete=models.CASCADE)
