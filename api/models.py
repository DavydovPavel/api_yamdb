from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Title(models.Model):
    name = models.CharField(max_length=100)
    year = models.PositiveSmallIntegerField()
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True)
    genre = models.ManyToManyField('Genre', blank=True, null=True)
    description = models.TextField(null=True, blank=True)
    rating = models.PositiveIntegerField(null=True, blank=True)
    
    class Meta:        
        ordering = ('-id',)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length = 20)
    slug = models.SlugField(max_length = 20, unique=True)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length = 20)
    slug = models.SlugField(max_length = 20, unique=True)

    def __str__(self):
        return self.name
