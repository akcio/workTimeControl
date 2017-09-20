from django.conf.urls import url

from . import views

urlpatterns = [
    #url(r'^$', views.index, name='index'),
    url(r'^$', views.getAllInfo, name='AllInfo'),
    url(r'^(?P<startWith>\d+)/$', views.getAllInfo, name='AllInfo'),
    url(r'^(?P<userName>\w+)/start/$', views.startWork, name='startWork'),
    url(r'^(?P<userName>\w+)/$', views.indexUser, name='userIndex'),
    url(r'^(?P<userName>\w+)/end/$', views.endWork, name='endWork'),
    url(r'^(?P<userName>\w+)/stata/$', views.getStatistic, name='userStata'),
]
