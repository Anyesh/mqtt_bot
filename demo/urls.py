from django.urls import path, include
from django.conf.urls import url
from . import views


urlpatterns = [
    url('', views.home, name="home"),
    url('bot/', views.IndexView.as_view(), name="index")
]
