Prérequis :
-----------
 - scrapy en version 0.14 (sudo pip install Scrapy)
 - Django


Architecture :
--------------
 - Le dossier chezesas contient le projet scrapy


Explications :
--------------
Le projet scrapy utilise le package "scrapy.contrib_exp.djangoitem.DjangoItem" (contenu dans l'installation de scrapy 0.14) permettant de faire le lien entre les Items de scrapy et les Models de Django.

Le projet scrapy se configure grâce au fichier chesessas/settings.py. Le fichier est documenté.


Lancer le crawl :
-----------------
Pour lancer le crawl, il faut se placer dans le dossier crawler et utiliser la commande suivante :
scrapy crawl <nom_du_spider>

Exemples:
 scrapy crawl gitem
 scrapy crawl toutfaire
 scrapy crawl yvanbeal



