from django.conf.urls import patterns, url
from museyapp import views
from django.conf import settings
urlpatterns = patterns('',
url(r'^events/(?P<event_id>\d+)|/$', views.events, name='events'),
url(r'^projects/(?P<prjct_id>\d+)|/$', views.projects, name='projects'),
url(r'^artists/(?P<artist_id>\d+)|/$', views.artist, name='artist'),
url(r'^events/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT}),
url(r'^charge/$', views.charge, name="charge"),
url(r'projects/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT}),

url(r'^paypal/$', views.paypal, name='paypal'), 

)

