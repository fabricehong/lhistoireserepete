# lhistoireserepete

## installer les dependances
pip install -r requirements/dev.txt

## Lancer le serveur
python manage.py runserver

exemple ids:

pour news:
news$$http://www.letempsarchives.ch/page/JDG_1923_07_08/10/conference%20de%20lausanne

pour archive:
archive$$JDG_1923_07_08$$10$$conference%20de%20lausanne


exemple url de comparaison avec les ids:
http://127.0.0.1:5000/compare?source_id=news$$http://www.letempsarchives.ch/page/JDG_1923_07_08/10/conference%20de%20lausanne&destination_id=archive$$JDG_1923_07_08$$10$$conference%20de%20lausanne

## Base de données des titres

Pour remplacer le serveur sparql, on héberge temporairement la liste de titres d'archives dans une base de donnée mongodb à l'adresse suivante:

mongodb://hack2016:hack2016@ds011442.mlab.com:11442/archives