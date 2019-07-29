from django.urls import path, re_path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    re_path(r'^(?P<new_url_id>\w{6})$', views.redirect_original, name='redirectoriginal'),
    re_path(r'^makeshort/$', views.shorten_url, name='shortenurl'),
]