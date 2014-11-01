from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'codebook.views.front', name='front'),

)