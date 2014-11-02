from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'codebook.views.front', name='front'),
    url(r'^news$', 'codebook.views.news', name='news'),
    url(r'^watching$', 'codebook.views.watching', name='watching'),
    url(r'^starred$', 'codebook.views.starred', name='starred'),
    url(r'^following$', 'codebook.views.following', name='following'),

)