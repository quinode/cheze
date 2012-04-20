# -*- coding: utf-8 -*-
from scrapy.contrib.spiders import CrawlSpider
from django.template.defaultfilters import slugify
from product.models import Category
from django.contrib.sites.models import Site
import re


def name_slug_from_nth(categories, pos):
    # print categories
    cats = list(categories)
    cats.reverse()
    # return slug from the nth *link* counting from the right of breadcrumb (starting with 1)
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
        #try:
        categories = elt.extract()
        if len(categories) > 0:
            print 'get_category: ', categories 

            if self.breadcrumb_current_item_is_a_link:
                startpos = 2
            else:
                startpos = 1

            item_cat = name_slug_from_nth(categories, startpos)
            name = item_cat['name']
            slug = item_cat['slug']

            print 'item_cat: ', item_cat
          
            current_slug = slug
            parents = [item_cat]

            loop_counter, pos_counter = 1, 1

            while(current_slug != self.root_category_slug):  # on s'arrete avant la categorie racine du site
            #for x in range(0, 10):
                #print 'current_slug:', current_slug
                pos = int(startpos + pos_counter)
                #print 'index:', pos, categories
                current_cat = name_slug_from_nth(categories, pos)
                #print 'current_cat : ', current_cat
                print 'previous slug : ', parents[pos_counter - 1]['slug']
                if not current_cat['slug'] in self.skip_cats and \
                   current_cat['slug'] != self.root_category_slug and \
                   current_cat['slug'] != parents[pos_counter - 1]['slug']:  # cas des catégories avec le meme nom qui se suivent
                    
                    parents.append(current_cat)
                    current_slug = current_cat['slug']
                    pos_counter += 1
                    #print 'parent added : ', parents
                #print pos_counter
                loop_counter += 1    
                if loop_counter > 20: 
                    break    
            parents.append(root_cat)  # on termine en ajoutant NOTRE catégorie racine
            parents.reverse()
            print 'parents final : ',parents
            current_parent = Category.objects.get(slug=root_cat['slug'])
            for parent_cat in parents[1:-1]:  # on ne va pas recréer notre catégorie racine , 
                                              # et notre catégorie parent de base sera créée à la fin
                current_parent, created = Category.objects.get_or_create(slug=parent_cat['slug'], 
                                                                parent=current_parent, 
                                                                defaults={'site': Site.objects.get_current(), 'name': parent_cat['name']})
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
