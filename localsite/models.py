from product.models import Product
from django.db import models
from satchmo_utils.thumbnail.field import ImageWithThumbnailField
from django.core.urlresolvers import reverse


class Fournisseur(models.Model):
    product = models.ManyToManyField(Product, blank=True, null=True)
    name = models.CharField("Nom", max_length=200)
    slug = models.SlugField("Slug", blank=True, unique=True)
    description = models.TextField("Description", blank=True)
    picture = ImageWithThumbnailField('Logo', blank=True, null=True,
        upload_to="logos",
        name_field="name",
        max_length=200)  # Media root is automatically prepended

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('fournisseur_list', args=[self.slug])  

    class Meta:
        ordering = ['name']
