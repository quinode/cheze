from django.conf.urls.defaults import *

handler404 = 'localsite.views.my404view'
# from django.views.generic.simple import direct_to_template

urlpatterns = patterns('',
    url(r"^$", 'localsite.views.home', name="home"),
)
