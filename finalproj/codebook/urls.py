from django.conf.urls import patterns, include, url

urlpatterns = patterns('',

	# Loading Content
    url(r'^$', 'codebook.content_views.front', name='front'),
    url(r'^news$', 'codebook.content_views.news', name='news'),
    url(r'^watching$', 'codebook.content_views.watching', name='watching'),
    url(r'^starred$', 'codebook.content_views.starred', name='starred'),
    url(r'^following$', 'codebook.content_views.following', name='following'),

    # User Actions 
    url(r'^like_comment/(?P<comment_id>\d+)$', 'codebook.user_action_views.like_comment', name='like_comment'),
    url(r'^watch_repo/(?P<repo_id>\d+)$', 'codebook.user_action_views.watch_repo', name='watch_repo'),
    url(r'^save_post/(?P<post_id>\d+)$', 'codebook.user_action_views.save_post', name='save_post'),
    url(r'^search_results$', 'codebook.user_action_views.search', name='search'),
    url(r'^repo_comment/(?P<repo_id>\d+)$', 'codebook.user_action_views.repo_comment', name='repo_comment'),
)