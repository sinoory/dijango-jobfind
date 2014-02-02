from django.conf.urls import patterns, url

from jobfind import views

urlpatterns = patterns('',
    url(r'^index$', views.index, name='index'),
    url(r'^querry$', views.querry, name='querry'),
    url(r'^(?P<poll_id>\d+)/$', views.detail, name='detail'),
    url(r'^modify/(?P<rcdid>\d+)/$', views.modify),
    url(r'^submitstatus$', views.submitstatus),
    )
