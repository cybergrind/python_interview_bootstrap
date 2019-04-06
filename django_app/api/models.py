from django.db import models

# Create your models here.


class Author(models.Model):
    name = models.CharField(max_length=255, null=False)

    def __str__(self):
        return f'{self.name}'


class Book(models.Model):
    title = models.CharField(max_length=255, null=False)
    author = models.ForeignKey(Author, related_name='books', on_delete=models.CASCADE)
