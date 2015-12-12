from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.AnimalList.as_view(), name='list'),
    url(r'^(?P<pk>\d+)/$', views.AnimalDetail.as_view(), name='detail'),
]