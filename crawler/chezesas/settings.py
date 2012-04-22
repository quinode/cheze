# -*- coding: utf-8 -*-
############## CONFIG DE BASE DE SCRAPY ##############
BOT_NAME = 'chezesas'
BOT_VERSION = '1.0'

SPIDER_MODULES = ['chezesas.spiders']
NEWSPIDER_MODULE = 'chezesas.spiders'
USER_AGENT = '%s/%s' % (BOT_NAME, BOT_VERSION)
ITEM_PIPELINES = [
    'chezesas.pipelines.NoRootURL',
    'chezesas.pipelines.CleanPipeline',
    'chezesas.pipelines.DBWriterPipeline',
]

LOG_LEVEL = 'ERROR'
######################################################


############## CONFIG AJOUTER POUR LE LIEN AVEC DJANGO ##############
# La valeur de debug permet de limiter le nombre de pages parsées lors du crawl
#DEBUG = False     # Valeur pour la production. Parse toute les pages pour récupérer tous les items
DEBUG = True      # Valeur pour les tests. Récupère qu'1 ou 2 pages pour permettre les tests

SITE_ID = 1

#Importation de l'environnement de Django
import os
PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))
SITE_PATH = '%s/../..' % PROJECT_PATH  # chemin vers le projet Django


def setup_django_env(path):
    import imp
    from django.core.management import setup_environ
    abs_path = os.path.abspath(path)
    f, filename, desc = imp.find_module('settings', [abs_path])
    os.sys.path.append(filename)
    os.sys.path.append(abs_path)
    project = imp.load_module('settings', f, filename, desc)
    setup_environ(project)

setup_django_env(SITE_PATH)

#Configuration pour le lien avec les models Django
from product.models import Product

# Model Django
DJANGO_MODEL = Product

# FIELD_*, représente le nom des champs du model Django
FIELD_TITLE = "name"
FIELD_MANUFACTURER = "manufacturer"
FIELD_REFERENCE = "reference"
FIELD_SHORT_DESCRIPTION = "short_description"
FIELD_DESCRIPTION = "description"
FIELD_PRICE = "price"
FIELD_CATEGORY = "category"
FIELD_PRODUCT_URL = "product_url"
FIELD_IMAGE_URL = "images"
FIELD_SHOP = "shop"

# Constantes permettant d'identifier les boutiques
GITEM = 0
TOUTAFAIRE = 1
YVANBEAL = 2
BRICOPRO = 3
#####################################################################
