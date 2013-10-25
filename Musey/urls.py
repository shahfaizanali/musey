from django.conf.urls import patterns, include, url
from museyapp import views
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'Musey.views.home', name='home'),
    # url(r'^Musey/', include('Musey.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    #url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
     url(r'^$', views.index, name='index'),
     url(r'^musey/', include('museyapp.urls')),
     url(r'^admin/', include(admin.site.urls)),
     url(r'^signup', views.signup, name='signup'),
     url(r'^login', views.login, name='login'),
     url(r'^something/hard/to/guess/', include('paypal.standard.ipn.urls')),
) 
)
