# DataClimat
Bienvenue sur le dépôt GitHub du site [DataClimat](https://www.dataclimat.fr/), réalisé par Thomas Benchetrit au sein de l'équipe de la députée Paula Forteza, 
députée de la deuxième cironscription des français de l'étranger (Amérique latine et Caraïbes).
DataClimat a pour vocation de vulgariser des données climatiques issus du [GIEC](https://www.ipcc.ch/report/ar6/wg1/) et du [DRIAS](http://www.drias-climat.fr/).
Le site est codée en Python sur la base de la librairie [Dash](https://plotly.com/dash/) qui permet de créer des webapp. 
Sont aussi utilisées des librairies de cartographie comme [Leaflet](https://leafletjs.com/) pour la visualisation des cartes, et les Tiles des indicateurs de feux de forêts et des
sécheresses sont hébergés sur [Mapbox](https://www.mapbox.com/)
### Organisation
Le dépôt s'organise comme suit : 
<ul>
<li>app.py / app_creator.ipynb permet de créer la webapp et d'effectuer tout les traitements et de gérer l'architecture de l'affichage </li>
<li>assets/ contient le logo et les fichiers css/js nécessaires à la stylisation du site et à son interactivité, bien qu'une grande partie soit géré par le framework en python </li>
<li> data/ contient l'ensemble des données nécessaires à la création des visualisations, et le fichiers geojson nécessaires à la géolocalisation des données sur la carte </li>
</ul>

 Contact

De part sa nature en construction, le site est ammené a être modifé dans son contenu et dans son organisation régulièrement au cours des prochaines semaines.
Si vous souhaitez nous contactez pour une modification, une question, ou une remarque, vous êtes prié de le faire par mail à <paula.forteza@assemblee-nationale.fr>, 
ou directement sur <benchetritthomas@gmail.com>.
