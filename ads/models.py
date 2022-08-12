from django.db import models


class Ad(models.Model):
    name = models.CharField(max_length=60, default='')
    author = models.CharField(max_length=30, default='')
    price = models.PositiveIntegerField(default=0)
    description = models.CharField(max_length=30, default='')
    address = models.CharField(max_length=200, null=False, default='')
    is_published = models.BooleanField(verbose_name='published', default=False)


class Category(models.Model):
    name = models.CharField(max_length=30, default='')

