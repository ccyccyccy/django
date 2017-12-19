from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from cadmin import views

urlpatterns = [
	url(r'^$', views.post_list, name='cadmin_post_list'),
	url(r'^post/add/$', views.post_add, name='post_add'),
	url(r'^post/update/(?P<pk>\w+)/$', views.post_update, name='post_update'),
	url(r'^post/delete/(?P<pk>\d+)/$', views.post_delete, name='post_delete'),
	url(r'^category/$', views.category_list, name='category_list'),
	url(r'^category/add/$', views.category_add, name='category_add'),
	url(r'^category/update/(?P<pk>\d+)/$', views.category_update, name='category_update'),
	url(r'^category/delete/(?P<pk>\d+)/$', views.category_delete, name='category_delete'),
	url(r'^tag/$', views.tag_list, name='tag_list'),
	url(r'^tag/add/$', views.tag_add, name='tag_add'),
	url(r'^tag/update/(?P<pk>\d+)/$', views.tag_update, name='tag_update'),
	url(r'^tag/delete/(?P<pk>\d+)/$', views.tag_delete, name='tag_delete'),
	url(r'^login/$', views.login, {'template_name': 'cadmin/login.html'}, name='cadmin_login'),
	url(r'^logout/$', auth_views.logout, {'template_name': 'cadmin/logout.html'}, name='cadmin_logout'),
	url(r'^register/$', views.register, name='register'),
	url(r'^account-info/$', views.account_info, name='account_info'),
	url(r'^activate/account/$', views.activate_account, name='activate_account'),
	url(r'password-change/$', auth_views.password_change,
		{'post_change_redirect': 'password_change_done',
		'template_name': 'cadmin/password_change.html'},
		name='password_change'),
	url(r'^password-change-done/$', auth_views.password_change_done,
		{'template_name': 'cadmin/password_change_done.html'},
		name='password_change_done'),
]
