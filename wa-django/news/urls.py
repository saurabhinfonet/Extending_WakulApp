from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.news_feed, name='front_page'),
    url(r'^news/$', views.news_feed, name='news'),
    url(r'^news/(?P<category>[\w-]+)/$', views.news_feed, name="news_feed"),
    url(r'^(?P<slug>feed|rss)', views.rss, name="rss"),
    url(r'^news/(?P<category>[\w-]+)/(?P<slug>feed|rss)', views.rss, name="rss"),
    url(r'^map/$', views.map, name='map'),
    url(r'^map/(?P<map_view>[\w-]+)', views.map, name='map'),
    url(r'^twitter/topic/(?P<topic>[\w-]+)/$', views.twitter_topic, name="twitter_topic"),
    url(r'^about/', views.about, name="about"),
    url(r'^directory/$', views.directory, name="directory"),
    url(r'^directory/(?P<outlet>[\w-]+)', views.directory, name="outlet"),
    url(r'^training/', views.training, name="training"),

# url added for sentimens
    url(r'^sentiment/topic/$', views.sentiment, name="sentiment"), 

# url added for first nation
    url(r'^firstnations/$', views.firstnation, name="firstnation"),

]
