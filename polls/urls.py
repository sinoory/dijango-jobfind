from django.conf.urls import patterns, url

from polls import views


urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url( r'^static/(?P<path>.*)$', 'django.views.static.serve',{ 'document_root':'/home/sin/wkspace/webserver/django/mysite/static' }),
    url(r'^(?P<poll_id>\d+)/$', views.detail, name='detail'),
    url(r'^(?P<poll_id>\d+)/results/$', views.results, name='results'),
    url(r'^(?P<poll_id>\d+)/vote/$', views.vote, name='vote'),
    )
