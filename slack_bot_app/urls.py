from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.index),
    url(r'^slack/oauth/$', views.slack_oauth),
    url(r'^register/$', views.Registration.as_view(), name='register'),
    url(r'^login/$', views.Login.as_view(), name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^statistics/$', views.statistics, name='statistics'),

]

