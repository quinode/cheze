from scrapy.contrib.spiders import CrawlSpider
from django.template.defaultfilters import slugify
from product.models import Category
from django.contrib.sites.models import Site
import re


class BaseSpider(CrawlSpider):
    def extract(slef, elt, index=0):
        try:
            return elt.extract()[index]
        except:
            return None

    def get_category(self, elt, parent_slug):
        try:
            categories = elt.extract()
            name = categories[len(categories) - 2]
            name = name.lower().capitalize()
            slug = slugify(name)
            length = len(slug)
            if length > 50:
                slug = '%s-%s' % (length, slug)
                slug = slug[0:50]
            parent = Category.objects.get(slug=parent_slug)
            cat, created = Category.objects.get_or_create(slug=slug, parent=parent, defaults={'site': Site.objects.get_current(), 'name': name})
            return cat
        except Exception, e:
            raise e
            return None

    def get_price(self, price):
        if price is None:
            return None
        try:
            expr = re.search(r'\d+\,?\d+', price)
            price = expr.group(0)
            return price.replace(',', '.')
        except:
            return None
