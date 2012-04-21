# -*- coding: utf-8 -*-
from scrapy.contrib.spiders import CrawlSpider
from django.template.defaultfilters import slugify
from product.models import Category
from django.contrib.sites.models import Site
import re
from scrapy import log


def name_slug_from_nth(categories, pos):
    '''
    returns a dict with the current category name and a re-created slug 
    from the Nth link counting from the right of breadcrumb (starting with 1)
    '''
    cats = list(categories)  # **COPIE** de notre liste de catégories
    cats.reverse()
    name = cats[int(pos - 1)]  # position de départ en partant de la droite - 1 (pour index=0)
    name = name.lower().capitalize()
    slug = slugify(name)
    length = len(slug)
    if length > 50:
        slug = '%s-%s' % (length, slug)
        slug = slug[0:50]
    return {'name': name, 'slug': slug}


class BaseSpider(CrawlSpider):

    breadcrumb_current_item_is_a_link = False
    root_category_slug = u'Accueil'   # ce n'est qu'un exemple
    skip_cats = []

    def extract(self, elt, index=0):
        try:
            return elt.extract()[index]
        except:
            return None

    def get_category(self, elt, root_cat):
        
        categories = elt.extract()
        if len(categories) > 0:
            #try:
            log.msg(u"scraped breadcrumb : %s" % categories, level=log.DEBUG)

            if self.breadcrumb_current_item_is_a_link:
                startpos = 2
            else:
                startpos = 1

            item_cat = name_slug_from_nth(categories, startpos)
            name = item_cat['name']
            slug = item_cat['slug']
            log.msg(u"Current item category : %s" % item_cat, level=log.DEBUG)
            current_slug = slug
            parents = [item_cat]
            loop_counter, pos_counter = 1, 1

            while(current_slug != self.root_category_slug):  # on s'arrete avant la categorie racine du site
                pos = int(startpos + pos_counter)
                current_cat = name_slug_from_nth(categories, pos)
                log.msg(u'current_cat (index=%s) : %s' % (pos, current_cat), level=log.DEBUG)
                current_slug = current_cat['slug']
                log.msg(u'current slug (looking for "%s" to stop loop): %s' % (self.root_category_slug, current_cat['slug']), level=log.DEBUG)

                if not current_slug in self.skip_cats and \
                   current_slug != self.root_category_slug and \
                   current_slug != parents[len(parents) - 1]['slug']:  # cas des catégories avec le meme nom qui se suivent
                    
                    parents.append(current_cat)
                    log.msg(u"parents added : %s" % parents, level=log.DEBUG)
                    
                else:
                    log.msg('skipped = %s ' % current_slug, level=log.DEBUG)
                pos_counter += 1
                # prevent infinite loop
                loop_counter += 1    
                if loop_counter > 20: 
                    break    
            parents.append(root_cat)  # on termine en ajoutant NOTRE catégorie racine
            parents.reverse()
            log.msg(u"parents final : %s" % parents, level=log.DEBUG)

            current_parent = Category.objects.get(slug=root_cat['slug'])
            for parent_cat in parents[1:-1]:  # on ne va pas recréer notre catégorie racine , 
                                              # et notre catégorie parent de base sera créée à la fin
                current_parent, created = Category.objects.get_or_create(slug=parent_cat['slug'], 
                                                                parent=current_parent, 
                                                                defaults={'site': Site.objects.get_current(), 'name': parent_cat['name'],
                                                                'meta':'', 'description':' '})
            cat, created = Category.objects.get_or_create(slug=slug, parent=current_parent, defaults={'site': Site.objects.get_current(), 'name': name})
            return cat
            # return None
            # except Exception, e:
            #     raise e
            #     return None
        else:
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
