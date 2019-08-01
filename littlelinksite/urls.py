from django.urls import path, re_path

from . import views

urlpatterns = [
    path('', views.IndexView.as_view() ),
    path('mylittlelinks', views.LinksView.as_view(), name='mylittlelinks' ),
    path('signup/', views.SignUp.as_view(), name='signup'),
    re_path(r'^(?P<new_url_id>[-\w]+)/delete/$', views.DeleteURLView.as_view(), name='url-delete'),
    re_path(r'^(?P<new_url_id>[-\w]+)$', views.redirect_original, name='redirectoriginal')
]