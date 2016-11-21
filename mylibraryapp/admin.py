from django.contrib import admin

from mylibraryapp import models

# Register your models here.

admin.site.register(models.Book)
admin.site.register(models.Author)
