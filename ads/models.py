from django.db import models

from users.models import User


class Category(models.Model):
    name = models.CharField(max_length=50, default='')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']

    def __str__(self):
        return self.name


class Ad(models.Model):
    name = models.CharField(max_length=60, default='')
    author = models.ForeignKey(User, on_delete=models.CASCADE, default='')
    price = models.PositiveIntegerField(default=0)
    description = models.TextField(max_length=300, default='')
    is_published = models.BooleanField(default=False)
    image = models.ImageField(upload_to='images/', null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'
        ordering = ['-price']

    def __str__(self):
        return self.name






