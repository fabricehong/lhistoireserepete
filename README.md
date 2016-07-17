# lhistoireserepete

## installer les dependances
```
pip install -r requirements/dev.txt
```

```
sudo apt-get install python-numpy python-scipy python-matplotlib ipython ipython-notebook python-pandas python-sympy python-nose
```

## Lancer le serveur
```
python manage.py runserver
```

activate mock mode:
```
. /mock.sh
```

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

Pour se connecter depuis l'outil ligne de commande:

  mongo ds011442.mlab.com:11442/archives -u hack2016 -p hack2016
  
  collection : titles