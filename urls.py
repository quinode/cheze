from django.conf.urls.defaults import *

from django.contrib import admin
admin.autodiscover()

#from localsite.urls import urlpatterns

from satchmo_store.urls import urlpatterns

#from autocomplete.views import autocomplete

urlpatterns += patterns('',
    #url(r'^autocomplete/', include(autocomplete.urls)),
    url(r'^admin_tools/', include('admin_tools.urls')),    
    #url(r'^fournisseur/([\w-]+)/$', 'localsite.views.fournisseur_list', {}, name="fabricant_list"),
)

from satchmo_utils import urlhelper

urlhelper.replace_urlpatterns(
    urlpatterns,
    [
        #add override urls here (match the name from satchmo's url files)
        url(r'^$', 'localsite.views.home', {}, name='satchmo_shop_home'),
    ]
)
