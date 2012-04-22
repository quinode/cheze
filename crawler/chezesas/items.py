# -*- coding: utf-8 -*-
from scrapy.conf import settings
from scrapy.contrib_exp.djangoitem import DjangoItem
from scrapy.item import Field
from product.models import ProductImage, AttributeOption, ProductAttribute
from django.core.files import File
import urllib
import urllib2
from django.core.files.temp import NamedTemporaryFile
from django.utils.encoding import smart_str
from django.template.defaultfilters import slugify
from localsite.models import Fournisseur


class ChezesasItem(DjangoItem):
    django_model = settings['DJANGO_MODEL']
    price = Field()
    category = Field()
    images = Field()
    product_url = Field()
    reference = Field()
    manufacturer = Field()

    def save(self, commit=True):
        #import pdb; pdb.set_trace()
        django_item = super(ChezesasItem, self).save(commit=False)

        try:
            # on tente de retrouver le meme item
            productattribute = ProductAttribute.objects.get(value=self[settings['FIELD_PRODUCT_URL']])
            older_item = productattribute.product         
            # reprise de la meme PK
            django_item.pk = older_item.pk
            # nettoyage des données reliées
            older_item.category.clear()
            older_item.price_set.all().delete()
            older_item.productimage_set.all().delete()
            older_item.productattribute_set.all().delete()
            fournisseur = older_item.fournisseur_set.all()
            if len(fournisseur) > 0:
                fournisseur[0].product.remove(older_item)
            # effacement de l'ancienne fiche    
            older_item.delete()    
            # sauver en DB la nouvelle fiche
            django_item.save()
            self.save_related_data(django_item)

        except ProductAttribute.DoesNotExist:
            # l'article n'est pas encore en base
            if commit:  # donc on commence par le sauver
                django_item.save()
            self.save_related_data(django_item)

        return django_item

    def save_image(self, django_item):
        try:
            url = smart_str(self[settings['FIELD_IMAGE_URL']])
            img_temp = NamedTemporaryFile()
            img_temp.write(urllib2.urlopen(urllib.quote(url, safe=':/')).read())
            img_temp.flush()
            filename = url.split('/')[-1]
            image = ProductImage(product=django_item)
            image.picture.save(filename, File(img_temp), save=True)
            image.save()
        except:
            pass

    def save_related_data(self, django_item):
        if settings['FIELD_CATEGORY'] in self.keys() and self[settings['FIELD_CATEGORY']] != None:
            django_item.category.add(self[settings['FIELD_CATEGORY']])  # on lui adjoint une catégorie
        if settings['FIELD_PRICE'] in self.keys() and self[settings['FIELD_PRICE']] != None:
            django_item.price_set.add(self[settings['FIELD_PRICE']])
        if settings['FIELD_MANUFACTURER'] in self.keys() and self[settings['FIELD_MANUFACTURER']] != None: 
            brand_name = self[settings['FIELD_MANUFACTURER']]
            brand, created = Fournisseur.objects.get_or_create(name=brand_name, slug=slugify(brand_name))
            django_item.fournisseur_set.add(brand)
        # attributs optionnels
        for field in ('FIELD_REFERENCE', 'FIELD_PRODUCT_URL'):  # permet d'ajouter d'autres attributs si besoin
            if settings[field] in self.keys() and self[settings[field]] != None:
                self.save_product_attribute(settings[field], django_item)
        #self.save_product_url(django_item)
        self.save_image(django_item)

    def save_product_attribute(self, att_name, django_item):
        # print 'getting ' + att_name
        option, created = AttributeOption.objects.get_or_create(name=att_name, defaults={'description': att_name, 'validation': "product.utils.validation_simple"})
        ProductAttribute(product=django_item, option=option, value=self[att_name], languagecode='fr').save()

    # def save_product_url(self, django_item):
    #     option, created = AttributeOption.objects.get_or_create(name="product_url", defaults={'description': "URL", 'validation': "product.utils.validation_simple"})
    #     ProductAttribute(product=django_item, option=option, value=self[settings['FIELD_PRODUCT_URL']]).save()

