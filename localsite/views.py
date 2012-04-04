# -*- coding: utf-8 -*-
from django.template import RequestContext
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render_to_response
from product.models import Product
from localsite.models import Fournisseur


def my404view(request):
    return redirect('/')

# from product.models import Category


def home(request):
    rdict = {}
    return render_to_response('shop/index.html', rdict, RequestContext(request))


def fabricant_list(request, slug):
    rdict = {}
    fournisseur = Fournisseur.objects.get(slug=slug)
    rdict['category'] = {'name': fournisseur.name, 'description': fournisseur.description}
    rdict['logo'] = fournisseur.picture
    rdict['products'] = Product.objects.filter(fournisseur__slug=slug)
    return render_to_response('product/category.html', rdict, context_instance=RequestContext(request))
