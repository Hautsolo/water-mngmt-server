from django.db import models
from .user import User
from .categories import Category
class Post(models.Model):
  title = models.CharField(max_length=50)
  image_url=models.CharField(max_length=100)
  description = models.CharField(max_length=200)
  user_id= models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
  category = models.ForeignKey(Category, on_delete=models.CASCADE)
