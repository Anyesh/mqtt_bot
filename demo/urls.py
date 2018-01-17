from django.urls import path, include
from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.home, name="home"),
    url(r'^bot/$', views.IndexView.as_view(), name="index")
]
