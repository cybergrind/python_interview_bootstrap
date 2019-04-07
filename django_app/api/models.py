from django.db import models
from django.contrib.postgres.indexes import GistIndex

# Create your models here.


class Author(models.Model):
    name = models.CharField(max_length=255, null=False)

    def __str__(self):
        return f'{self.name}'


class Book(models.Model):
    title = models.CharField(max_length=255, null=False)
    author = models.ForeignKey(Author, related_name='books', on_delete=models.CASCADE)

    class Meta:
        indexes = [
            GistIndex(name='title_gist', fields=['title'], opclasses=['gist_trgm_ops'])
        ]
