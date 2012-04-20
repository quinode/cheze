from django.conf.urls.defaults import *
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

#from localsite.urls import urlpatterns

from satchmo_store.urls import urlpatterns

#from autocomplete.views import autocomplete

urlpatterns += patterns('',
    #url(r'^autocomplete/', include(autocomplete.urls)),
    url(r'^admin_tools/', include('admin_tools.urls')),    
    #url(r'^fournisseur/([\w-]+)/$', 'localsite.views.fournisseur_list', {}, name="fabricant_list"),
    url(r'^tinymce/', include('tinymce.urls')),
)

from satchmo_utils import urlhelper

urlhelper.replace_urlpatterns(
    urlpatterns,
    [
        #add override urls here (match the name from satchmo's url files)
        url(r'^$', 'localsite.views.home', {}, name='satchmo_shop_home'),
    ]
)


if settings.DEBUG or ('test' in sys.argv):
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes':True}),
    )
