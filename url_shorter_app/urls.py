from django.urls import path, re_path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('makeshort/', views.shorten_url, name='shortenurl'),
    re_path('(?P<short_id>\w{6})', views.redirect_original, name='redirectoriginal'),
]