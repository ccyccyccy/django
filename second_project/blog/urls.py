from django.conf.urls import url
from blog import views

urlpatterns = [
    url(r'^$', views.index, name='blog_index'),
    url(r'^time/$', views.today_is, name='blog_time')
]
