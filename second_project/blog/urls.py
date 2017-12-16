from django.conf.urls import url
from django.contrib.flatpages import views as flat_views
from blog import views

urlpatterns = [
	url(r'^category/(?P<category_slug>[\w-]+)/$', views.post_by_category, name='post_by_category'),
	url(r'^tag/(?P<tag_slug>[\w-]+)/$', views.post_by_tag, name='post_by_tag'),
	url(r'^author/(?P<author_name>[\w]+)/$', views.post_by_author, name='post_by_author'),
	url(r'^feedback/$', views.feedback, name='feedback'),
	url(r'^(?P<pk>\d+)/(?P<post_slug>[\w\d-]+)$', views.post_detail, name='post_detail'),
	url(r'^$', views.post_list, name='post_list'),
	url(r'^login/$', views.login, name='blog_login'),
	url(r'^logout/$', views.logout, name='blog_logout'),
	url(r'^admin-page/$', views.admin_page, name='admin_page'),	
	url(r'^about/$', flat_views.flatpage, {'url': '/about/'}, name='about'),
	url(r'^eula/$', flat_views.flatpage, {'url': '/eula/'}, name='eula'),
]