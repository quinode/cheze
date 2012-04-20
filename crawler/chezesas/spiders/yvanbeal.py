# -*- coding: utf-8 -*-

from chezesas.spiders.base import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.spiders import Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from chezesas.items import ChezesasItem
from scrapy.conf import settings
from product.models import Category


class YvanbealSpider(BaseSpider):
    name = "yvanbeal"
    allowed_domains = ["yvanbeal.com"]
    start_urls = [
        "http://www.yvanbeal.com/recherche.html?p=1&d=Beal_Catalog_Product&"
    ]

    if settings['DEBUG']:
        rules = (
            Rule(SgmlLinkExtractor(allow='www\.yvanbeal\.com/recherche\.html\?p=[1-2]&d=Beal_Catalog_Product$'),
                'change_page', follow=True,
            ),
        )
    else:
        rules = (
            Rule(SgmlLinkExtractor(allow='www\.yvanbeal\.com/recherche\.html\?p=[1-9]+&d=Beal_Catalog_Product$'),
               'change_page', follow=True,
            ),
        )

    rules += (
        Rule(SgmlLinkExtractor(allow='www\.yvanbeal\.com/catalogue/.+$', restrict_xpaths='//div[@id="colG"]'),
            'parse_product', follow=True,
        ),
    )

    breadcrumb_current_item_is_a_link = True
    root_category_slug = 'catalogue'

    def change_page(self, response):
        self.parse(response)

    def parse_product(self, response):
        hxs = HtmlXPathSelector(response)
        i = ChezesasItem()
        i[settings['FIELD_TITLE']] = self.extract(hxs.select('//div[@class="product"]/div[@class="fiche"]/h2/text()'))
        i[settings['FIELD_DESCRIPTION']] = self.extract(hxs.select('//div[@class="product"]/div[@class="fiche"]/div[@class="text"]/p/text()'))
        i[settings['FIELD_MANUFACTURER']] = self.extract(hxs.select('//div[@class="product"]/div[@class="fiche"]/img[@class="log"]/@alt'))
        i[settings['FIELD_SHORT_DESCRIPTION']] = None
        i[settings['FIELD_PRICE']] = None
        # i[settings['FIELD_CATEGORY']] = self.get_category(hxs.select('//div[@class="product"]/div[@class="fiche"]/h1/text()'), 
        i[settings['FIELD_CATEGORY']] = self.get_category(hxs.select('//div[@class="chemin"]/ul/li/a/b/text()'), 
                                                                        {'name': 'Motoculture', 'slug': 'motoculture'})
        i[settings['FIELD_PRODUCT_URL']] = response.url
        i[settings["FIELD_IMAGE_URL"]] = self.extract(hxs.select('//div[@id="gallery"]/div[@class="affiche"]/a/img/@src'))
        return i

    def get_price(self, elt):
        try:
            print self.extract(elt, len(elt) - 1)
        except:
            return None
