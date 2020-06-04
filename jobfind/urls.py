from django.conf.urls import patterns, url

from jobfind import views
from django.contrib.auth.views import login, logout
urlpatterns = patterns('',
    url(r'^index$', views.index, name='index'),
    url(r'^querry$', views.querry, name='querry'),
    url(r'^login51$', views.login51, name='index'),
    url(r'^(?P<poll_id>\d+)/$', views.detail, name='detail'),
    url(r'^modify/(?P<rcdid>\d+)/$', views.modify),
    url(r'^submitstatus$', views.submitstatus),
    url(r'^viewljobs$', views.viewljobs),#view local jobs whith get or water status
    url(r'^accounts/login/$',  login),
    url(r'^accounts/logout/$', logout),
    )
