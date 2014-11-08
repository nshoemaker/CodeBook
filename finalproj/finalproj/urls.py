from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'finalproj.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^codebook/', include('codebook.urls')),
    url(r'^$', 'codebook.views.front'),
    url(r'^admin/', include(admin.site.urls)),
    url('', include('social.apps.django_app.urls', namespace='social')),
    url('', include('django.contrib.auth.urls', namespace='auth')),
    
)
