from django.conf.urls import patterns, url

import views

urlpatterns = patterns('',
    url(r'^$', views.Index, name='Index'),
    url(r'^index/$', views.Index, name='Index'),
    url(r'^upload/$', views.UploadAPK, name='UploadAPK'),
    url(r'^chart/$', views.IndexChart, name='IndexChart'),
    )