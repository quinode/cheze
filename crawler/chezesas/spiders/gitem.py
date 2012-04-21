# -*- coding: utf-8 -*-

from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.spiders import Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from chezesas.items import ChezesasItem
from scrapy.conf import settings
from chezesas.spiders.base import BaseSpider


class GitemSpider(BaseSpider):
    name = "gitem"
    allowed_domains = ["gitem.fr"]
    start_urls = [
        "http://www.gitem.fr/"
    ]
    breadcrumb_current_item_is_a_link = False
    root_category_slug = 'accueil'
    skip_cats = ['a-poser', 'encastrable', 'informatique']

    rules = (
        
        Rule(SgmlLinkExtractor(allow='www\.gitem\.fr/.+$', deny='product_compare', restrict_xpaths='//div[@id="menu"]'),
            'change_page', follow=True,
        ),
        Rule(SgmlLinkExtractor(allow='www\.gitem\.fr/.+$', deny='product_compare', restrict_xpaths='//div[@class="accueil-categ"]'),
            'change_page', follow=True,
        ),
        Rule(SgmlLinkExtractor(allow='www\.gitem\.fr/.+$', deny='product_compare', restrict_xpaths='//ul[@class="products-grid"]'),
            'parse_product', follow=True,
        ),
    )

    def change_page(self, response):
        self.parse(response)

    def parse_product(self, response):
        hxs = HtmlXPathSelector(response)
        i = ChezesasItem()
        i[settings['FIELD_MANUFACTURER']] = self.extract(hxs.select('//div[@class="product-manufacturer"]/h2/text()'))
        i[settings['FIELD_REFERENCE']] = self.extract(hxs.select('//div[@class="sku"]/text()'))
        i[settings['FIELD_TITLE']] = self.extract(hxs.select('//div[@class="product-name"]/h1/text()'))
        i[settings['FIELD_SHORT_DESCRIPTION']] = self.extract(hxs.select('//div[@class="short-description"]/div[@class="std"]/text()'))
        i[settings['FIELD_DESCRIPTION']] = self.extract(hxs.select('//div[@id="product_tabs_description_contents"]/div[@class="std"]/text()'))
        i[settings['FIELD_PRICE']] = self.get_price(self.extract(hxs.select('//div[@class="price-box"]/p/span[@class="price"]/text()')))
        i[settings['FIELD_CATEGORY']] = self.get_category(hxs.select('//div[@class="searchBar"]/div/div[@class="breadcrumbs"]/ul/li/a/text()'), 
                                                            {'name': 'Electro-ménager', 'slug': 'electro-menager'})
        i[settings['FIELD_PRODUCT_URL']] = response.url
        i[settings['FIELD_IMAGE_URL']] = self.extract(hxs.select('//img[@id="image"]/@src'))

        return i
