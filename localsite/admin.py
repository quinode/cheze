# -*- coding: utf-8 -*-

from django.contrib import admin
from product.models import Product, Category
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _

from localsite.models import Fournisseur
from product.admin import CategoryOptions, ProductOptions, ProductAttribute_Inline, ProductImage_Inline, Price_Inline


from django.contrib.admin.widgets import FilteredSelectMultiple

from tinymce.widgets import AdminTinyMCE
from django import forms


class SortedQueryset:
    def __init__(self, qs):
        self.qs = qs
        
    def all(self):
        #Permet de trier les catégories par le chemin complet (parents inclus)
        items = list(self.qs.all())

        def sort_by_unicode(x): 
            return unicode(x)
        items.sort(key=sort_by_unicode)
        for i in items:
            yield i

    def __getattr__(self, name):
        #Pour toutes les autres méthodes que all : appelle la méthode du queryset
        return getattr(self.qs, name)


## Pour django 1.4
# from cheze.utils import SimpleListFilter
# 
# 
# class Catlevel(SimpleListFilter):
#     title = _('Catégorie niveau 1')
#     parameter_name = 'parent'
#     def lookups(self, request, model_admin):
#         return tuple(('1','truc'),('2','machin'))
#         #Category.objects.filter(parent=None).values_list('id','name')
#     def queryset(self, request, queryset):
#         return queryset.filter(parent=value)


class FournisseurAdmin(admin.ModelAdmin):
    filter_horizontal = ('product',)
admin.site.register(Fournisseur, FournisseurAdmin)
  

class FournisseurInline(admin.TabularInline):
    model = Fournisseur.product.through
    extra = 1


class ProductAdminForm(forms.ModelForm):
    category = forms.ModelMultipleChoiceField(
        queryset=SortedQueryset(Category.objects),
        widget=FilteredSelectMultiple('category', False)
    )
    description = forms.CharField(widget=AdminTinyMCE(attrs={'cols': 80, 'rows': 20}))

    class Meta:
        model = Product


class ProductAdmin(ProductOptions):
    form = ProductAdminForm
    list_display = ('main_category', 'name', 'active', 'featured',)
    list_display_links = ('name',)
    list_filter = ('category', 'date_added', 'active', 'featured')
    inlines = [FournisseurInline, 
               ProductAttribute_Inline, 
               Price_Inline,
               ProductImage_Inline,
               ]
    fieldsets = (
            (None, {'fields': ('site', 'category', 'name', 'description', 
                    'short_description', 'active', 'featured', 'ordering')}), 
            (_('Meta Data'), {'fields': ('meta',), 'classes': ('collapse',)}),
            (_('Related Products'), {'fields': ('related_items',)}), 
            )
    filter_horizontal = ('category', 'related_items')
    ordering = ['category', 'ordering']
            

admin.site.unregister(Product)
admin.site.register(Product, ProductAdmin)


class CategoryAdminForm(forms.ModelForm):
    description = forms.CharField(widget=AdminTinyMCE(attrs={'cols': 80, 'rows': 20}))

    class Meta:
        model = Category


class CategoryAdmin(CategoryOptions):
    form = CategoryAdminForm
    list_display = ('name', '_parents_repr', 'is_active')
    list_display_links = ('name',)
    ordering = ['parent__id', 'ordering']
    search_fields = ['name', 'slug']
#    list_filter = (Catlevel,)
    
    filter_horizontal = ('related_categories',)
    
    def mark_active(self, request, queryset):
        queryset.update(is_active=True)
        return HttpResponseRedirect('')

    def mark_inactive(self, request, queryset):
        queryset.update(is_active=False)
        return HttpResponseRedirect('')
        
    mark_active.short_description = u"Activer les catégories sélectionnées"  
    mark_inactive.short_description = u"Désactiver les catégories sélectionnées" 

admin.site.unregister(Category)
admin.site.register(Category, CategoryAdmin)
