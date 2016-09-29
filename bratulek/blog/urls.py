from django.conf.urls import include, url
from . import views


urlpatterns = [
	url(r'^$', views.board_list, name='board_list'),
	url(r'^board/(?P<pk>[0-9]+)/$', views.board_detail, name='board_detail'),
	url(r'^post/(?P<pk>[0-9]+)/$', views.post_detail, name='post_detail'),
	url(r'^post/new/board/(?P<bd>[0-9]+)$', views.post_new, name='post_new'),
	]

