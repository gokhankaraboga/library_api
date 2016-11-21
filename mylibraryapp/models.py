from __future__ import unicode_literals
from django.db import models


# import django.contrib.auth.models as auth_models

class Author(models.Model):
    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    date_of_birth = models.DateField()

    def __unicode__(self):
        return 'Author %d: ' % self.id + self.name + ' ' + self.surname


class Book(models.Model):
    authors = models.ManyToManyField(Author)
    title = models.CharField(max_length=255)
    lc_classification = models.CharField(max_length=255)

    def __unicode__(self):
        return 'Book %d: ' % self.id + self.title
