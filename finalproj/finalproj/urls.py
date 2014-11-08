from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^codebook/', include('codebook.urls')),
    url(r'^$', 'codebook.content_views.front'),
    url(r'^admin/', include(admin.site.urls)),
)
