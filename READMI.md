# Projet Django

## Romain Mechain / Evann YANG


### Bien installer

    pip install -r requirement.txt

### Commande migrate

    python3 manage.py makemigrations LesProduits
    python3 manage.py sqlmigrate LesProduits 000x
    python manage.py migrate

### Commande pour init la BD

    chmod +x setup_db.sh
    ./script_bd.sh


### Commande pour les tests

    python manage.py test LesProduits.tests


### Coverage

    coverage run --source='LesProduits' manage.py test LesProduits.tests
    coverage report
    coverage html