# -*- coding: utf-8 -*-

from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.spiders import Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from chezesas.items import ChezesasItem
from scrapy.conf import settings
from chezesas.spiders.base import BaseSpider
from scrapy import log


class GitemSpider(BaseSpider):
    name = "bricopro"
    allowed_domains = ["bricopro.fr"]
    start_urls = [
        "http://www.bricopro.fr/nos-produits/catalogue/62/liste.html",
        "http://www.bricopro.fr/nos-produits/catalogue/64/liste.html",
        "http://www.bricopro.fr/nos-produits/catalogue/83/liste.html",
        "http://www.bricopro.fr/nos-produits/catalogue/84/liste.html",
    ]
    breadcrumb_current_item_is_a_link = False
    root_category_slug = 'nos-produits'
    skip_cats = []
    
    if settings['DEBUG'] == True:
        rules = (
            Rule(SgmlLinkExtractor(allow='bricopro\.fr/nos-produits/catalogue/\d+/liste.html$', 
                                    restrict_xpaths=['//nav[@class="pagination"]', '//h3[@class="fn"]']),
                'change_page', follow=True,
            ),
        )
    else:
        rules = (
            Rule(SgmlLinkExtractor(allow='bricopro\.fr/nos-produits/catalogue/\d+/liste.html?page=[0-9]+$', 
                                    restrict_xpaths=['//nav[@class="pagination"]', '//h3[@class="fn"]']),
                'change_page', follow=True,
            ),  
        )
    rules += (
        Rule(SgmlLinkExtractor(allow='bricopro\.fr/nos-produits/\d+/fiche.html\?id_catalogue\=\d+', 
                                restrict_xpaths=['//h3[@class="fn"]', '//div[@class="similaries"]']),
            'parse_product', follow=True,
        ),
    )

    def change_page(self, response):
        self.parse(response)

    def parse_product(self, response):
        self.log('PARSING %s' % response.url, level=log.DEBUG)
        hxs = HtmlXPathSelector(response)
        i = ChezesasItem()
        i[settings['FIELD_MANUFACTURER']] = self.extract(hxs.select('//p[@class="brand"]/a/img/@alt'))
        i[settings['FIELD_REFERENCE']] = self.extract(hxs.select('//div[@class="hproduct"]/div[@class="price"]/p[@class="reference"]/text()'))
        i[settings['FIELD_TITLE']] = self.extract(hxs.select('//div[@class="hproduct"]/h2[@class="fn"]/text()'))
        i[settings['FIELD_DESCRIPTION']] = self.extract(hxs.select('//div[@class="hproduct"]/div[@class="description"]/p/text()'))
        i[settings['FIELD_SHORT_DESCRIPTION']] = None
        i[settings['FIELD_PRICE']] = self.get_price(self.extract(hxs.select('//div[@class="hproduct"]/div[@class="price"]/p/span/strong/text()')))
        i[settings['FIELD_CATEGORY']] = self.get_category(hxs.select('//ul[@id="ariane"]/li/a/text()'), 
                                                            {'name': 'Bricolage', 'slug': 'bricolage'})
        i[settings['FIELD_PRODUCT_URL']] = response.url
        i[settings['FIELD_IMAGE_URL']] = self.extract(hxs.select('//div[@class="photo"]/figure/a/@href'))

        return i
