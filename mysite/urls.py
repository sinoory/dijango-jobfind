from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^jobfind/', include('jobfind.urls')),
    url(r'^polls/', include('polls.urls')),
    url(r'^shoplist/', include('shoplist.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
