from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^library/$', views.library, name='library'),
    url(r'^book/$', views.book, name='book'),
    url(r'^book/(?P<bid>\d+)/$', views.book, name='book_with_pid'),
    url(r'^author/$', views.author, name='author'),
    url(r'^author/(?P<bid>\d+)/$', views.author, name='author'),
]
