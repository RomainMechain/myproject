# Projet Django

## Romain Mechain / Evann YANG

## Présentation du projet. 

Dans ce projet django, nous sommes repartie du code obtenue à la suite des tp et td. Nous avions donc déjà le CRUD sur les produits, les attributs et leurs valeurs, ainsi que sur les items. 

Nous avons rajouté une quantité dans la table item afin de gérer le stock, nous avons trouver cela plus pertinent que de le mettre dans la table Produit car cela rajoute de la précision. On a ensuite rajouté tout ce qui concerne les commandes, à commencer par le CRUD fournisseur, ainsi que la possibilité de lui attribuer un prix pour un produit. Il est ensuite possible de passer une commande, et de lui ajouter des items associé au produits vendue par le fournisseur. On peut enfin faire évoluer l'état de la commande, pour au final mettre à jour le stock. 


## Instalation et lancement 

- Instalation des requirements : 

    `pip install -r requirement.txt`

- Migration manuel : 

    `python3 manage.py makemigrations LesProduits`

    `python3 manage.py sqlmigrate LesProduits 000x`

    `python manage.py migrate`

- Migration avec script : 

    `chmod +x setup_db.sh`

    `./script_bd.sh`

## Lancement des tests

    python manage.py test LesProduits.tests


## Coverage

    coverage run --source='LesProduits' manage.py test LesProduits.tests
    coverage report
    coverage html