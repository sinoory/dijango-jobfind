from django.conf.urls import patterns, url

from shoplist import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    )
