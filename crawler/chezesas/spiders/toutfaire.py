# -*- coding: utf-8 -*-

from chezesas.spiders.base import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.spiders import Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.conf import settings
from chezesas.items import ChezesasItem
from product.models import Category


class ToutfaireSpider(BaseSpider):
    name = "toutfaire"
    allowed_domains = ["toutfaire.fr"]
    start_urls = [
        "http://toutfaire.fr/liste-produits"
    ]
    breadcrumb_current_item_is_a_link = False
    root_category_slug = 'accueil'

    if settings['DEBUG'] == True:
        rules = (
            Rule(SgmlLinkExtractor(allow='toutfaire\.fr/liste-produits\?&page=[0-1]$'),
                'change_page', follow=True,
            ),
        )
    else:
        rules = (
            Rule(SgmlLinkExtractor(allow='toutfaire\.fr/liste-produits\?&page=[0-9]+$'),
               'change_page', follow=True,
            ),
        )

    rules += (
        Rule(SgmlLinkExtractor(allow='toutfaire\.fr/produits/.+$'),
            'parse_product', follow=True,
        ),
    )

    def change_page(self, response):
        self.parse(response)

    def parse_product(self, response):
        hxs = HtmlXPathSelector(response)
        i = ChezesasItem()
        i[settings['FIELD_TITLE']] = self.extract(hxs.select('//div[@id="block-product"]/div[@class="content"]/h2/text()'))
        i[settings["FIELD_DESCRIPTION"]] = self.extract(hxs.select('//div[@id="block-product"]/div[@class="content"]/div[@class="desc"]/div[@class="first"]/p/text()'))
        i[settings['FIELD_SHORT_DESCRIPTION']] = None
        i[settings["FIELD_PRICE"]] = self.get_price(hxs.select('//div[@id="block-product"]/div[@class="content"]/div[@class="desc"]/div[@class="last"]/div[@class="price"]/strong'))
        i[settings["FIELD_CATEGORY"]] = self.get_category(hxs.select('//div[@id="breadcrumb"]/ul/li/a/text()'), 
                                                                        {'name': 'Matériaux', 'slug': 'materiaux'})
        i[settings['FIELD_PRODUCT_URL']] = response.url
        i[settings["FIELD_IMAGE_URL"]] = self.extract(hxs.select('//div[@id="block-product"]/div[@class="picture"]/div[@class="thumbs-images"]/div[@id="thumb_01"]/a/img/@src'))
        i[settings['FIELD_REFERENCE']] = None
        i[settings['FIELD_MANUFACTURER']] = None

        return i

    def get_price(self, elt):
        try:
            decimal = self.extract(elt.select('text()'), 1).replace(' ', '')
            befor_decimal = self.extract(elt.select('big/text()'))
            price = '%s%s' % (befor_decimal, decimal)
            return super(ToutfaireSpider, self).get_price(price)
        except:
            return None
