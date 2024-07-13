from django.db import models


class Like(models.Model):

    label = models.IntegerField(default=True)
