# DataClimat

Bienvenu sur le dépôt GitHub du site [DataClimat](https://www.dataclimat.fr/), réalisé par Thomas Benchetrit au sein de l'équipe de la députée Paula Forteza, 
députée de la deuxième cironscription des français de l'étranger (Amérique latine et Caraïbes).

DataClimat a pour vocation de vulgariser des données climatiques issus du [GIEC](https://www.ipcc.ch/report/ar6/wg1/) et du [DRIAS](http://www.drias-climat.fr/).

Le site est réalisé en [Python 3.7.1+](https://www.python.org/downloads/release/python-370/) sur la base de la librairie [Dash](https://plotly.com/dash/) qui permet de créer des webapps.

Sont aussi utilisées des librairies de cartographie comme [Leaflet](https://leafletjs.com/) pour la visualisation des cartes, et les [tiles](https://docs.mapbox.com/vector-tiles/reference/) des indicateurs de feux de forêts et des sécheresses sont hébergées sur [Mapbox](https://www.mapbox.com/).

## Organisation

Le dépôt s'organise comme suit : 

* [app.py](app.py) / [app_creator.ipynb](app_creator.ipynb) permet de créer la webapp, d'effectuer tout les traitements et de gérer l'architecture de l'affichage ;
* [assets/][assets] contient le logo et les fichiers css/js nécessaires à la stylisation du site et à son interactivité, bien qu'une grande partie soit gérée par le framework en python ;
* [data/](data) contient l'ensemble des données nécessaires à la création des visualisations, et les fichiers geojson nécessaires à la géolocalisation des données sur la carte.

## Installation

Plateformes supportées :

- distributions GNU/Linux (en particulier Debian and Ubuntu) ;
- Mac OS X ;
- Windows (nous recommandons d'utiliser [ConEmu](https://conemu.github.io/) à la place de la console par défaut) ;

Pour les autres OS : si vous pouvez exécuter Python, Numpy, Pandas, et Dash, l'installation devrait fonctionner.

### Installez un gestionnaire d'environnement virtuel

Nous recommandons l'utilisation d'un [environnement virtuel](https://virtualenv.pypa.io/en/stable/) (_virtualenv_) avec un gestionnaire de _virtualenv_ tel que [poetry](https://python-poetry.org/).

- Un _[virtualenv](https://virtualenv.pypa.io/en/stable/)_ crée un environnement pour les besoins spécifiques du projet sur lequel vous travaillez.
- Un gestionnaire de _virtualenv_, tel que [poetry](https://python-poetry.org/), vous permet de facilement créer, supprimer et naviguer entre différents projets.

Pour installer `poetry`, lancez une fenêtre de terminal et suivez ces instructions :

```
python --version # Doit être Python 3.7.1 ou une version supérieure.
pip install --upgrade pip
pip install poetry
```

Bravo :tada: Vous êtes prêt·e à installer DataClimat !

### Installez DataClimat

Pour installer `DataClimat`, dans la même fenêtre de terminal qu'avant :

```
git clone git@github.com:ThomasBench/DataClimat.git
cd DataClimat
poetry install
```

Félicitations :tada: DataClimat est prêt à être utilisé !

## Servez l'application web DataClimat

Pour lancer l'application dans votre ordinateur, dans la même fenêtre de terminal lancez :

```
poetry run python app.py # Devrait afficher `Dash is running on http://127.0.0.1:8050/`.
# Si non, n'hesitez pas à nous contacter, ou à ouvrir un [issue](https://github.com/ThomasBench/DataClimat/issues/new).
```

:tada: Vous servez DataClimat, vous pouvez d'ores et déjà visiter l'adresse `http://127.0.0.1:8050/` avec votre navigateur web !

## Contact

De part sa nature en construction, le site est ammené a être modifé dans son contenu et dans son organisation régulièrement au cours des prochaines semaines.
Si vous souhaitez nous contacter pour une modification, une question, ou une remarque, vous êtes prié de le faire par mail à <paula.forteza@assemblee-nationale.fr>, 
ou directement sur <benchetritthomas@gmail.com>.
