from scrapy.conf import settings
from scrapy.contrib_exp.djangoitem import DjangoItem
from scrapy.item import Field
from product.models import ProductImage, AttributeOption, ProductAttribute
from django.core.files import File
import urllib
import urllib2
from django.core.files.temp import NamedTemporaryFile
from django.utils.encoding import smart_str


class ChezesasItem(DjangoItem):
    django_model = settings['DJANGO_MODEL']
    price = Field()
    category = Field()
    images = Field()
    product_url = Field()

    def save(self, commit=True):
        django_item = super(ChezesasItem, self).save(commit=False)

        try:
            productattribute = django_item.productattribute_set.get(value=self[settings['FIELD_PRODUCT_URL']])
            older_item = productattribute.product
            django_item.pk = older_item.pk
            django_item.category.clear()
            django_item.price_set.clear()
            django_item.productimage_set.clear()
            django_item.productattribute_set.clear()
            django_item.save()
        except ProductAttribute.DoesNotExist:
            if commit:
                django_item.save()
            django_item.category.add(self[settings['FIELD_CATEGORY']])
            if self[settings['FIELD_PRICE']]:
                django_item.price_set.add(self[settings['FIELD_PRICE']])
            self.save_image(django_item)
            self.save_product_url(django_item)
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

    def save_product_url(self, django_item):
        option, created = AttributeOption.objects.get_or_create(name="product_url", defaults={'description': "Product url", 'validation': "product.utils.validation_simple"})
        ProductAttribute(product=django_item, option=option, value=self[settings['FIELD_PRODUCT_URL']]).save()
