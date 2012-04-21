# -*- coding: utf-8 -*-
from product.models import Price
from django.contrib.sites.models import Site
from livesettings import config_value
from scrapy.conf import settings
from scrapy.exceptions import DropItem
from scrapy import log


class NoRootURL(object):
    def process_item(self, item, spider):
        if item['product_url'].count('/') > 3:
            return item
        else:
            # import pdb; pdb.set_trace()
            raise DropItem(u'A root (fashionable) URL')
            log.msg(u" **** Skipping root URL: %s" % item['product_url'], level=log.DEBUG)


class CleanPipeline(object):
    def process_item(self, item, spider):
        item['site'] = Site.objects.get_current()
        item['items_in_stock'] = '0'
        item['active'] = True
        item['featured'] = False
        item['ordering'] = 0
        item['total_sold'] = '0'
        item['taxable'] = lambda: config_value('TAX', 'PRODUCTS_TAXABLE_BY_DEFAULT')
        item['shipclass'] = "DEFAULT"

        # if item[settings['FIELD_MANUFACTURER']]:
        #     item[settings['FIELD_MANUFACTURER']] = item[settings['FIELD_MANUFACTURER']].upper()
        
        if item[settings['FIELD_REFERENCE']]:
            if spider.name == "bricopro":
                ref = u' '.join([x.strip() for x in item[settings['FIELD_REFERENCE']].splitlines()])
                item[settings['FIELD_REFERENCE']] = ref.replace(u'Réf.', u'')
            else:
                item[settings['FIELD_REFERENCE']] = item[settings['FIELD_REFERENCE']].strip()

        if item[settings['FIELD_TITLE']]:
            if spider.name == 'gitem':
                item[settings['FIELD_TITLE']] = item[settings['FIELD_TITLE']].lower().capitalize() \
                    + u' ' + item[settings['FIELD_MANUFACTURER']] + u' (' + item[settings['FIELD_REFERENCE']] + u')'
            elif spider.name in ['yvanbeal', 'bricopro']:
                pass
            else:
                item[settings['FIELD_TITLE']] = item[settings['FIELD_TITLE']].lower().capitalize()
          
        if item[settings['FIELD_PRICE']]:
            item[settings['FIELD_PRICE']] = Price(price=item[settings['FIELD_PRICE']], quantity=1)
        if not item[settings['FIELD_DESCRIPTION']]:
            item[settings['FIELD_DESCRIPTION']] = '-'
        # if not settings['FIELD_SHORT_DESCRIPTION'] in item.keys() or not item[settings['FIELD_SHORT_DESCRIPTION']]:
        if not item[settings['FIELD_SHORT_DESCRIPTION']]:
            description = item[settings['FIELD_DESCRIPTION']]
            if len(item[settings['FIELD_DESCRIPTION']]) <= 100:
                item[settings['FIELD_SHORT_DESCRIPTION']] = description
            else:
                item[settings['FIELD_SHORT_DESCRIPTION']] = '%s...' % description[0:100]
        return item


class DBWriterPipeline(object):
    def process_item(self, item, spider):
        if item[settings['FIELD_TITLE']] and item[settings['FIELD_DESCRIPTION']] != '':
            return item.save()
