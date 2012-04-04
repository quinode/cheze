# -*- coding:utf-8 -*-
#source http://djangosnippets.org/snippets/1197/
#from django.contrib.sites.models import RequestSite
#from product.models import AttributeOption
#from django.contrib.sites.models import Site
#from django.contrib.auth.models import User
from localsite.models import Fournisseur


def footer(request):
    links = {}
    links['fournisseurs'] = Fournisseur.objects.all()
    return links
