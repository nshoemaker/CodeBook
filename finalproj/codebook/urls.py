from django.conf.urls import patterns, include, url

urlpatterns = patterns('',

	# Loading Content
    url(r'^$', 'codebook.views.front', name='front'),
    url(r'^news$', 'codebook.views.news', name='news'),
    url(r'^watching$', 'codebook.views.watching', name='watching'),
    url(r'^starred$', 'codebook.views.starred', name='starred'),
    url(r'^following$', 'codebook.views.following', name='following'),
    url(r'^signin$', 'codebook.views.signin', name='signin'),
    url(r'^signup$', 'codebook.views.signup', name='signup'),


    # User Actions 
    url(r'^like_comment/(?P<comment_id>\d+)$', 'codebook.user_action_views.like_comment', name='like_comment'),
    url(r'^watch_repo/(?P<repo_id>\d+)$', 'codebook.user_action_views.watch_repo', name='watch_repo'),
    url(r'^save_post/(?P<post_id>\d+)$', 'codebook.user_action_views.save_post', name='save_post'),
)