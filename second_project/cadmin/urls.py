from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from cadmin import views

urlpatterns = [
	url(r'^home/$', views.home, name='home'),
	url(r'^login/$', views.login,
		{'template_name': 'cadmin/login.html'}, name='cadmin_login'
		),
	url(r'^logout/$', auth_views.logout,
		{'template_name': 'cadmin/logout.html'}, name='cadmin_logout'
		),
	url(r'^register/$', views.register, name='register'),
	url(r'^activate/account/$', views.activate_account, name='activate_account'),
	url(r'password-change/$', auth_views.password_change,
		{'post_change_redirect': 'password_change_done',
		'template_name': 'cadmin/password_change.html'},
		name='password_change'
		),
	url(r'^password-change-done/$', auth_views.password_change_done,
		{'template_name': 'cadmin/password_change_done.html'},
		name='password_change_done'
		),
	url(r'^post/add/$', views.post_add, name='post_add'),
	url(r'^post/update/(?P<pk>\w+)/$', views.post_update, name='post_update'),
]
