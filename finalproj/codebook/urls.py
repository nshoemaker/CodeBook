from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
	# Loading Content
    url(r'^$', 'codebook.content_views.front', name='front'),
    url(r'^news$', 'codebook.content_views.news', name='news'),
    url(r'^watching$', 'codebook.content_views.watching', name='watching'),
    url(r'^following$', 'codebook.content_views.following', name='following'),
    url(r'^saved$', 'codebook.content_views.saved', name='saved'),
    url(r'^sandbox$', 'codebook.content_views.sandbox', name='sandbox'),

    # User Actions
    url(r'^comment_repo/(?P<id>\d+)$', 'codebook.ajax_views.post_repo_comment', name='comment_repo'),
    #url(r'^like_comment/(?P<source>\d+)/(?P<comment_id>\d+)$', 'codebook.user_action_views.like_comment', name='like_comment'),
    #url(r'^watch_repo/(?P<source>\D+)/(?P<repo_id>\d+)$', 'codebook.user_action_views.watch_repo', name='watch_repo'),
    #url(r'^star_repo/(?P<source>\D+)/(?P<repo_id>\d+)$', 'codebook.user_action_views.star_repo', name='star_repo'),
    #url(r'^save_file/(?P<source>\D+)/(?P<file_id>\d+)$', 'codebook.user_action_views.save_file', name='save_file'),
    url(r'^search_results$', 'codebook.user_action_views.search', name='search'),
    url(r'^comment/(?P<comment_type>[^/]+)/(?P<source>\D+)/(?P<id>\d+)$', 'codebook.user_action_views.comment', name='comment'),
    url(r'^signin', 'codebook.user_action_views.signin', name="signin"),

    url(r'^comment_file/(?P<id>\d+)$', 'codebook.ajax_views.post_file_comment', name='comment_file'),
    url(r'^star_repo/(?P<id>\d+)$', 'codebook.ajax_views.star_repo', name='star_repo'),
    url(r'^unstar_repo/(?P<id>\d+)$', 'codebook.ajax_views.unstar_repo', name='unstar_repo'),
    url(r'^watch_repo/(?P<id>\d+)$', 'codebook.ajax_views.watch_repo', name='watch_repo'),
    url(r'^unwatch_repo/(?P<id>\d+)$', 'codebook.ajax_views.unwatch_repo', name='unwatch_repo'),
    url(r'^like_comment/(?P<id>\d+)$', 'codebook.ajax_views.like_comment', name='like_comment'),
    url(r'^save_file/(?P<id>\d+)$', 'codebook.ajax_views.save_file', name='save_file'),
)
