from django.urls import path, re_path

from . import views

urlpatterns = [
    path('', views.IndexView.as_view() ),
    re_path(r'^(?P<new_url_id>[-\w]+)$', views.redirect_original, name='redirectoriginal')
]