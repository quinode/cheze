from product.models import Price
from django.contrib.sites.models import Site
from livesettings import config_value
from scrapy.conf import settings

# from scrapy.exceptions import DropItem

# class GitemAccueil(object):

#     def process_item(self, item, spider):
#         if item['price']:
#             if item['price_excludes_vat']:
#                 item['price'] = item['price'] * self.vat_factor
#             return item
#         else:
#             raise DropItem("Missing price in %s" % item)

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
        #     item[settings['FIELD_MANUFACTURER']] = item[settings['FIELD_MANUFACTURER']].lower().capitalize()
        if item[settings['FIELD_TITLE']]:
            item[settings['FIELD_TITLE']] = item[settings['FIELD_TITLE']].lower().capitalize()
        if item[settings['FIELD_PRICE']]:
            item[settings['FIELD_PRICE']] = Price(price=item[settings['FIELD_PRICE']], quantity=1)
        if not item[settings['FIELD_DESCRIPTION']]:
            item[settings['FIELD_DESCRIPTION']] = '-'
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
