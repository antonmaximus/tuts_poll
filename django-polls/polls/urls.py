from django.conf.urls import patterns, url

from polls import views

#1: urlpatterns = patterns('',
#     url(r'^$', views.index, name='index'), #ex: /polls/
#     url(r'^(?P<poll_id>\d+)/$', views.detail, name='detail'), #ex: /polls/5/
#     url(r'^(?P<poll_id>\d+)/results/$', views.results, name='results'), #ex: /polls/5/results/
#     url(r'^(?P<poll_id>\d+)/vote/$', views.vote, name='vote'), #ex: /polls/5/vote/
# )


urlpatterns = patterns('',
  url(r'^$', views.IndexView.as_view(), name='index'),
  url(r'^(?P<pk>\d+)/$', views.DetailView.as_view(), name='detail'),
  url(r'^(?P<pk>\d+)/results/$', views.ResultsView.as_view(), name='results'),
  url(r'^(?P<poll_id>\d+)/vote/$', views.vote, name='vote'), #ex: /polls/5/vote/

)