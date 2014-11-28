from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
	# Loading Content
    url(r'^$', 'codebook.content_views.front', name='front'),
    url(r'^news$', 'codebook.content_views.news', name='news'),
    url(r'^watching$', 'codebook.content_views.watching', name='watching'),
    url(r'^saved$', 'codebook.content_views.saved', name='saved'),
    url(r'^sandbox$', 'codebook.content_views.sandbox', name='sandbox'),
    url(r'^profile/(?P<username>\w+)/$', 'codebook.content_views.profile_view', name = 'profile'),
    url(r'^profile$', 'codebook.content_views.my_profile_view', name = 'view_my_profile'),
    url(r'^sort_lang_stream_recent$', 'codebook.ajax_views.sort_lang_stream_recent', name='sort_lang_stream_recent'),
    url(r'^sort_lang_stream_popular$', 'codebook.ajax_views.sort_lang_stream_popular', name='sort_lang_stream_popular'),
    url(r'^expand_folder$', 'codebook.ajax_views.expand_folder', name='expand_folder'),
    url(r'^get_top_level$', 'codebook.ajax_views.get_top_level', name='get_top_level'),
    url(r'^get_file_contents$', 'codebook.ajax_views.get_file_contents', name='get_file_contents'),

    # User Actions
    url(r'^comment_repo/(?P<id>\d+)$', 'codebook.ajax_views.post_repo_comment', name='comment_repo'),
    url(r'^search_results$', 'codebook.user_action_views.new_search', name='search'),
    url(r'^search/(?P<language>\w+)/$', 'codebook.user_action_views.new_quick_search', name='quick_search'),
    url(r'^repo_search_list$', 'codebook.ajax_views.repo_search_list', name='repo_search_list'),
    url(r'^signin', 'codebook.user_action_views.signin', name="signin"),
    url(r'^comment_file/(?P<id>\d+)$', 'codebook.ajax_views.post_file_comment', name='comment_file'),
    url(r'^rate_credibility$', 'codebook.ajax_views.rate_credibility', name='rate_credibility'),
    url(r'^star_repo/(?P<id>\d+)$', 'codebook.ajax_views.star_repo', name='star_repo'),
    url(r'^unstar_repo/(?P<id>\d+)$', 'codebook.ajax_views.unstar_repo', name='unstar_repo'),
    url(r'^watch_repo/(?P<id>\d+)$', 'codebook.ajax_views.watch_repo', name='watch_repo'),
    url(r'^unwatch_repo/(?P<id>\d+)$', 'codebook.ajax_views.unwatch_repo', name='unwatch_repo'),
    url(r'^like_comment/(?P<id>\d+)$', 'codebook.ajax_views.like_comment', name='like_comment'),
    url(r'^unlike_comment/(?P<id>\d+)$', 'codebook.ajax_views.unlike_comment', name='unlike_comment'),
    url(r'^save_file/(?P<id>\d+)$', 'codebook.ajax_views.save_file', name='save_file'),
    url(r'^unsave_file/(?P<id>\d+)$', 'codebook.ajax_views.unsave_file', name='unsave_file'),
    url(r'^add_proficiency$', 'codebook.ajax_views.add_proficiency', name='add_proficiency'),
    url(r'^watch_list$', 'codebook.ajax_views.watch_list', name='watch_list'),
    url(r'^save_file_from_repo$', 'codebook.ajax_views.save_file_from_repo', name='save_file_from_repo'),
    url(r'^rate_difficulty$', 'codebook.ajax_views.rate_difficulty', name='rate_difficulty'),
    url(r'^rate_documentation$', 'codebook.ajax_views.rate_documentation', name='rate_documentation'),
)
