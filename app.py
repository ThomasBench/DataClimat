# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import pandas as pd
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import xarray as xr
import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_daq as daq
import dash_html_components as html
from dash.dependencies import Input, Output, State , MATCH , ALL
import dash_leaflet as dl
from dash_extensions.javascript import assign, arrow_function
import dash_leaflet.express as dlx
from pathlib import Path
import json
import os
import plotly.graph_objects as go
from ipcc_helpers import *
ROOT_DIR = str(Path().resolve()) + '/data'


chroma = "https://cdnjs.cloudflare.com/ajax/libs/chroma-js/2.1.0/chroma.min.js"
app = dash.Dash(__name__, external_scripts=[chroma], external_stylesheets=[dbc.themes.LUMEN], update_title=None, meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}
    ])
###########Load the data

###### GIEC
liste_scenar_giec = ['ssp119','ssp126','ssp585']

df_dict_temp  = {
    'ssp119' : treat_nc(ROOT_DIR + '/temprec' + '/Panel_b1_Simulated_temperature_change_at_1_5C.nc'),
    'ssp126' : treat_nc(ROOT_DIR + '/temprec' + '/Panel_b2_Simulated_temperature_change_at_2C.nc'),
    'ssp585' : treat_nc(ROOT_DIR + '/temprec' + '/Panel_b3_Simulated_temperature_change_at_4C.nc')
    }
dict_temp = {'ssp119' : '+1.5°C','ssp126' : '+2°C','ssp585' : '+4°C'}
df_dict_prec = {
    'ssp119' : treat_nc(ROOT_DIR + '/temprec' + '/Panel_c1_Simulated_precipitation_change_at_1_5C.nc', pluie = True),
    'ssp126' : treat_nc(ROOT_DIR + '/temprec' + '/Panel_c2_Simulated_precipitation_change_at_2C.nc', pluie = True),
    'ssp585' : treat_nc(ROOT_DIR + '/temprec' + '/Panel_c3_Simulated_precipitation_change_at_4C.nc', pluie = True),
}
#### Source drias : http://www.drias-climat.fr/accompagnement/sections/174
#### Source Giec : https://fr.wikipedia.org/wiki/Trajectoires_socio%C3%A9conomiques_partag%C3%A9es
source_dict = {
    'giec' : '- Données : https://www.ipcc.ch/report/ar6/wg1/  \n -Texte : https://fr.wikipedia.org/wiki/Trajectoires_socio%C3%A9conomiques_partag%C3%A9es',
    'drias' : '- Données : http://www.drias-climat.fr/ \n - Texte : http://www.drias-climat.fr/accompagnement/sections/174'
}
co2_df = pd.read_csv(ROOT_DIR + r'/co2/aggregated.csv')
liste_scenarios = co2_df.columns.tolist()[1:]

##### Drias
url_dict_feux = {
    'refREF' : 'https://api.mapbox.com/styles/v1/fechie/ckt08ixj9073w18rxpb982i0q/tiles/256/{z}/{x}/{y}@2x?access_token=pk.eyJ1IjoiZmVjaGllIiwiYSI6ImNrdDA3bTltYTMwd2UycXRmOTN6NzJ1d3YifQ.UTZ9mF-EsqXZDBbtrAl85A',
    'optiH1' : 'https://api.mapbox.com/styles/v1/fechie/ckt08f77a0ht217ngzlzvmi5t/tiles/256/{z}/{x}/{y}@2x?access_token=pk.eyJ1IjoiZmVjaGllIiwiYSI6ImNrdDA3bTltYTMwd2UycXRmOTN6NzJ1d3YifQ.UTZ9mF-EsqXZDBbtrAl85A',
    'optiH2' : 'https://api.mapbox.com/styles/v1/fechie/ckt08fkuaaqec17qhimo15t32/tiles/256/{z}/{x}/{y}@2x?access_token=pk.eyJ1IjoiZmVjaGllIiwiYSI6ImNrdDA3bTltYTMwd2UycXRmOTN6NzJ1d3YifQ.UTZ9mF-EsqXZDBbtrAl85A',
    'optiH3' : 'https://api.mapbox.com/styles/v1/fechie/ckt08gy4paquo17qi6wjjrdp3/tiles/256/{z}/{x}/{y}@2x?access_token=pk.eyJ1IjoiZmVjaGllIiwiYSI6ImNrdDA3bTltYTMwd2UycXRmOTN6NzJ1d3YifQ.UTZ9mF-EsqXZDBbtrAl85A',
    'interH1' : 'https://api.mapbox.com/styles/v1/fechie/ckt08cp8gaqbr17qhkn1ki47z/tiles/256/{z}/{x}/{y}@2x?access_token=pk.eyJ1IjoiZmVjaGllIiwiYSI6ImNrdDA3bTltYTMwd2UycXRmOTN6NzJ1d3YifQ.UTZ9mF-EsqXZDBbtrAl85A',
    'interH2' : 'https://api.mapbox.com/styles/v1/fechie/ckt08dmsp7h9o17qnmedqxj7m/tiles/256/{z}/{x}/{y}@2x?access_token=pk.eyJ1IjoiZmVjaGllIiwiYSI6ImNrdDA3bTltYTMwd2UycXRmOTN6NzJ1d3YifQ.UTZ9mF-EsqXZDBbtrAl85A',
    'interH3' : 'https://api.mapbox.com/styles/v1/fechie/ckt08dzht3wxj18ql3dcj1ocm/tiles/256/{z}/{x}/{y}@2x?access_token=pk.eyJ1IjoiZmVjaGllIiwiYSI6ImNrdDA3bTltYTMwd2UycXRmOTN6NzJ1d3YifQ.UTZ9mF-EsqXZDBbtrAl85A',
    'pessH1' : 'https://api.mapbox.com/styles/v1/fechie/ckt08hcpgaq1h17tcof317orr/tiles/256/{z}/{x}/{y}@2x?access_token=pk.eyJ1IjoiZmVjaGllIiwiYSI6ImNrdDA3bTltYTMwd2UycXRmOTN6NzJ1d3YifQ.UTZ9mF-EsqXZDBbtrAl85A',
    'pessH2' : 'https://api.mapbox.com/styles/v1/fechie/ckt08hv0u7hdv17qnamd8rajb/tiles/256/{z}/{x}/{y}@2x?access_token=pk.eyJ1IjoiZmVjaGllIiwiYSI6ImNrdDA3bTltYTMwd2UycXRmOTN6NzJ1d3YifQ.UTZ9mF-EsqXZDBbtrAl85A',
    'pessH3' : 'https://api.mapbox.com/styles/v1/fechie/ckt08idlh7hf818qmb7c9ww5d/tiles/256/{z}/{x}/{y}@2x?access_token=pk.eyJ1IjoiZmVjaGllIiwiYSI6ImNrdDA3bTltYTMwd2UycXRmOTN6NzJ1d3YifQ.UTZ9mF-EsqXZDBbtrAl85A',
}

url_dict_sech = {
    'refREF' : 'https://api.mapbox.com/styles/v1/fechie2/ckt1q2deh18t017mmuz5mtahl/tiles/256/{z}/{x}/{y}@2x?access_token=pk.eyJ1IjoiZmVjaGllMiIsImEiOiJja3QxcTE4bXEwY3ZpMnBzMjZ1cjRldzluIn0.nEBWPCGTioiCE_h9T1kUOQ',
    'optiH1' : 'https://api.mapbox.com/styles/v1/fechie2/ckt1s877b1b8h17njcv98foik/tiles/256/{z}/{x}/{y}@2x?access_token=pk.eyJ1IjoiZmVjaGllMiIsImEiOiJja3QxcTE4bXEwY3ZpMnBzMjZ1cjRldzluIn0.nEBWPCGTioiCE_h9T1kUOQ',
    'optiH2' : 'https://api.mapbox.com/styles/v1/fechie2/ckt1s95dt0qai17q9haznh8wu/tiles/256/{z}/{x}/{y}@2x?access_token=pk.eyJ1IjoiZmVjaGllMiIsImEiOiJja3QxcTE4bXEwY3ZpMnBzMjZ1cjRldzluIn0.nEBWPCGTioiCE_h9T1kUOQ',
    'optiH3' : 'https://api.mapbox.com/styles/v1/fechie2/ckt1saelx1axh17mmzbovlupd/tiles/256/{z}/{x}/{y}@2x?access_token=pk.eyJ1IjoiZmVjaGllMiIsImEiOiJja3QxcTE4bXEwY3ZpMnBzMjZ1cjRldzluIn0.nEBWPCGTioiCE_h9T1kUOQ',
    'interH1' : 'https://api.mapbox.com/styles/v1/fechie2/ckt1s671u1bcd17o1hs6124yy/tiles/256/{z}/{x}/{y}@2x?access_token=pk.eyJ1IjoiZmVjaGllMiIsImEiOiJja3QxcTE4bXEwY3ZpMnBzMjZ1cjRldzluIn0.nEBWPCGTioiCE_h9T1kUOQ',
    'interH2' : 'https://api.mapbox.com/styles/v1/fechie2/ckt1s6xis0q8f17q9bud8fvu5/tiles/256/{z}/{x}/{y}@2x?access_token=pk.eyJ1IjoiZmVjaGllMiIsImEiOiJja3QxcTE4bXEwY3ZpMnBzMjZ1cjRldzluIn0.nEBWPCGTioiCE_h9T1kUOQ',
    'interH3' : 'https://api.mapbox.com/styles/v1/fechie2/ckt1s7lnq1av017mmo1qcsm3t/tiles/256/{z}/{x}/{y}@2x?access_token=pk.eyJ1IjoiZmVjaGllMiIsImEiOiJja3QxcTE4bXEwY3ZpMnBzMjZ1cjRldzluIn0.nEBWPCGTioiCE_h9T1kUOQ',
    'pessH1' : 'https://api.mapbox.com/styles/v1/fechie2/ckt1sb1ih1b2p17mctjhx11pa/tiles/256/{z}/{x}/{y}@2x?access_token=pk.eyJ1IjoiZmVjaGllMiIsImEiOiJja3QxcTE4bXEwY3ZpMnBzMjZ1cjRldzluIn0.nEBWPCGTioiCE_h9T1kUOQ',
    'pessH2' : 'https://api.mapbox.com/styles/v1/fechie2/ckt1sbwps1b1x17r8gef9p8dx/tiles/256/{z}/{x}/{y}@2x?access_token=pk.eyJ1IjoiZmVjaGllMiIsImEiOiJja3QxcTE4bXEwY3ZpMnBzMjZ1cjRldzluIn0.nEBWPCGTioiCE_h9T1kUOQ',
    'pessH3' : 'https://api.mapbox.com/styles/v1/fechie2/ckt1scj1h1bs718msmpz1sdjd/tiles/256/{z}/{x}/{y}@2x?access_token=pk.eyJ1IjoiZmVjaGllMiIsImEiOiJja3QxcTE4bXEwY3ZpMnBzMjZ1cjRldzluIn0.nEBWPCGTioiCE_h9T1kUOQ',
}
liste_scenar_feu = ['Référence' , 'Optimiste', 'Intermédiaire', 'Pessimiste']
dict_range = {2008 : 'REF', 2060: 'H1',2060: 'H2', 2100: 'H3'}
dict_scenar_feux ={liste_scenar_feu[0]:'ref', liste_scenar_feu[1]:'opti', liste_scenar_feu[2]:'inter', liste_scenar_feu[3]:'pess'}

### France + big cities
with open(ROOT_DIR + '/france.geojson','r') as f:
    france_geo = json.loads(f.read())
cities = [dict(tooltip="Paris", lat=48.86, lon=2.33),
          dict(tooltip="Lyon", lat=45.75, lon=4.83),
          dict(tooltip="Lille", lat=50.63, lon=3.06),
          dict(tooltip="Toulouse", lat=43.6, lon=1.44),
          dict(tooltip="Bordeaux ", lat=44.837, lon=-0.579),
          dict(tooltip="Rennes ", lat=48.083, lon=-1.683),
          dict(tooltip="Strasbourg ", lat=48.583, lon=7.75),
          dict(tooltip="Marseille ", lat=43.296, lon=5.36)
          ]
cities_geo = dlx.dicts_to_geojson(cities)

## The texts

text_dict = {
    'ssp119' :dcc.Markdown(
        '''
        Le scénario SSP1 est initialement intitulé *La route verte* par le GIEC. Dans celui-ci, le monde s'oriente progressivement, 
        mais de manière généralisée, vers une voie plus durable, en mettant l'accent sur un développement plus inclusif qui respecte 
        les limites environnementales perçues. La gestion des biens communs mondiaux s'améliore lentement, les investissements dans 
        l'éducation et la santé accélèrent la transition démographique, et l'accent mis sur la croissance économique se transforme en un 
        accent plus large sur le bien-être humain. Sous l'impulsion d'un engagement croissant en faveur de la réalisation des objectifs de 
        développement, les inégalités se réduisent tant entre les pays qu'à l'intérieur de ceux-ci. La consommation est orientée vers une 
        faible croissance matérielle et une moindre intensité en ressources et en énergie.** Ce scénario prévoit un arrêt total des émissions 
        de CO2 aux alentours de 2050.** '''),
    'ssp126' :dcc.Markdown(
        '''Ce scénario est similaire au scénario précédent SSP1 - 1.9 à une différence près : 
        **l’arrêt total des émissions de CO2 est ici prévu aux alentours de 2075**.'''),
    'ssp585' :dcc.Markdown(
        '''
            Ce scénario est initialement intitulé *L’autoroute* par le GIEC. Dans celui-ci, le monde fait de plus en plus confiance aux marchés 
            compétitifs, à l'innovation et aux sociétés participatives pour produire des progrès technologiques rapides et développer le 
            capital humain comme voie vers le développement durable. Les marchés mondiaux sont de plus en plus intégrés. Il y a également de 
            forts investissements dans la santé, l'éducation et les institutions pour améliorer le capital humain et social. Dans le même temps, 
            la poussée du développement économique et social va de pair avec l'exploitation d'abondantes ressources en combustibles fossiles et 
            l'adoption de modes de vie à forte intensité de ressources et d'énergie dans le monde entier. Tous ces facteurs entraînent une croissance 
            rapide de l'économie mondiale, tandis que la population mondiale atteint un pic et décline au cours du 21e siècle. Les problèmes 
            environnementaux locaux, comme la pollution atmosphérique, sont gérés avec succès. On croit en la capacité de gérer efficacement les 
            systèmes sociaux et écologiques, y compris par la géo-ingénierie si nécessaire. **Ce scénario prévoit un triplement des émissions de CO2 
            d’ici 2075. **'''),
    'Pessimiste' :dcc.Markdown(
        """
        Le scénario pessimiste décrit un monde très hétérogène. Le thème sous-jacent est l'autosuffisance et la préservation des identités 
        locales. Les schémas de fécondité entre régions convergent très lentement, avec pour résultat un accroissement continu de la 
        population mondiale. Le développement économique a une orientation principalement régionale, et la croissance économique par habitant 
        et l'évolution technologique sont plus fragmentées et plus lentes que dans les autres scénarios. """),
    'Optimiste' :dcc.Markdown(
        ''' 
        Le scénario optimiste décrit un monde convergent avec la même population mondiale culminant au milieu du siècle et déclinant ensuite, 
        comme dans le scénario pessimiste, mais avec des changements rapides dans les structures économiques vers une économie de services et 
        d'information, avec des réductions dans l'intensité des matériaux et l'introduction de technologies propres et utilisant les ressources 
        de manière efficiente. L'accent est placé sur des solutions mondiales orientées vers une viabilité économique, sociale et 
        environnementale, y compris une meilleure équité, mais sans initiatives supplémentaires pour gérer le climat.'''),
    'Intermédiaire' :dcc.Markdown(
        '''Le scénario intermédiaire
            décrit un monde futur dans lequel la croissance économique est très rapide, la population mondiale atteint un maximum au milieu du 
            siècle pour décliner ensuite et de nouvelles technologies plus efficaces sont introduites rapidement. Les principaux thèmes sous-jacents
             sont la convergence entre régions, le renforcement des capacités et des interactions culturelles et sociales accrues, avec une 
             réduction substantielle des différences régionales dans le revenu par habitant. Les sources d'énergies utilisées sont à l'équilibre 
             entre les énergies fossiles et renouvelables. '''),
    'Référence' :dcc.Markdown(
    ''' Le scénario de référence
        représente l'état de la France en 2008 par rapport à l'indicateur choisi. 
        Une description de l'indicateur peut être lu en survolant le bouton "Unité" ci-dessous''')
    }

unit_text_dict = {
    'spi' : html.P(
        '''Le SPI est un indice permettant de mesurer la sécheresse météorologique. Il s’agit d’un indice de probabilité qui repose 
            seulement sur les précipitations. Les probabilités sont standardisées de sorte qu’un SPI de 0 indique une quantité de 
            précipitation médiane . L’indice est négatif pour les sécheresses, et positif pour les conditions humides.'''),
    'ifm' : html.P(
        '''
    Cet indice, développé par le Centre de recherches forestières du Pacifique au Canada, se base sur différents indicateurs météorologiques 
    tels que la vitesse du vent, la température, l'humidité et les précipitations, et est corrélé au nombre de feux de forêt en un lieu donné. 
    Ainsi, un doublement de l'IFM présage un doublement des risques de départ de feux. Cet indice est entre autres utilisé aujourd'hui 
    préventivement pour positionner des canadairs près des lieux à haut risque.
        ''')

}

text_en_tete =  html.Div([html.P('''
    Au mois d’août 2021, le GIEC a présenté la première partie de son sixième et dernier rapport au sein duquel il dresse
    un constat sans appel : les effets du réchauffement climatique vont s'accélérer et ce, quel que soit le rythme de baisse
    des émissions de gaz à effet de serre.'''), html.P('''
    Face à cette urgence écologique, la députée indépendante Paula Forteza lance le site DataClimat. Ce projet de vulgarisation de
    données climatiques permet de visualiser de manière interactive certaines simulations du Groupe d’experts intergouvernemental sur
    l’évolution du climat (GIEC) et de Drias, les futurs du climat, à l’échelle du territoire français.'''),html.P('''
    Vous disposez ci-dessous d’un outil de sélection du type de données que vous souhaitez visualiser :
    ''')])

liste_texte = html.Li(
    children = [
        html.Ul("Feux de forêts et sécheresses → Vous pouvez choisir de visualiser quatre scénarios issus de Drias, les futurs du climat. Pour chacun d’entre eux, vous pouvez choisir une date de projection afin de constater l’évolution des différents scénarios dans le temps. "),
        html.Ul("Précipitations et températures → Vous pouvez choisir de visualiser six scénarios issus du dernier rapport du GIEC. Pour chacun d’entre eux, vous disposez d’une projection des émissions de CO2 en fonction du scénario choisi ; il est possible de zoomer sur cette projection grâce à un clic droit (et de revenir à un affichage normal grâce à un double clic).")
    ],
    style = {'list-style-type': 'none'}
)
texte_fin = html.P("Une fois votre sélection effectuée, la visualisation des indicateurs choisis s’affichera sur la carte à droite.")



#### Create the Viz


##For the map :
color_prop  = 'tooltip'
colorscale = ['#ffbaba','#ff7b7b','#ff5252','#ff0000','#a70000']
vmin, vmax = 1 , 2
colorbar = dl.Colorbar(colorscale=colorscale, width=20, height=150, min=vmin, max=vmax, unit = '°C')
style_assign = assign("""function(feature, context){
    const {min, max, colorscale, colorProp, style} = context.props.hideout;
    const csc = chroma.scale(colorscale).domain([min, max])  // chroma lib to construct colorscale
    var color = csc(feature.properties[colorProp])
    style.fillColor = color // set color based on color prop.
    return style  // send back the style
}""")

point_style = assign(
    """function(feature, latlng){
return L.circleMarker(latlng, {color: 'black', fillOpacity : 1, radius : 4, fillColor : 'black' })}"""
)

france_contour = dl.GeoJSON(data = france_geo, options =dict(style = {'fill' : False, 'color' : 'black', 'weight' : 1} ) )
cities_point = dl.GeoJSON(data = cities_geo, options = dict(pointToLayer = point_style))




element = dl.Map(
    children=[
        dl.TileLayer(),
        dl.TileLayer(id = 'coucou', url = ''),
        html.Div(id = 'colorbar', children = colorbar)
        ],
    id = 'map',
    center=(46, 2),
    zoom=6,
    style={'width': '100%', 'height': '100vh', 'margin': "auto",'z-index' : '300', "display": "block"},
    scrollWheelZoom = False
    )

### Functions to create reused elements
def create_texte(index = 0):
    Id = {'type' :'text-indic' , 'index' : index }
    return dbc.Row(id = Id, style = { 'text-justify' : 'auto' ,'border-radius' : '5px' ,'overflow' : 'auto'})

def create_source_button(index, source_text):
    popover_children = [
        dbc.PopoverHeader("Source : "),
        dbc.PopoverBody(source_text)
    ]
    element = html.Div(
        children = [
            dbc.Button("Source", id='source-' + str(index), color="info", n_clicks=0,outline = True,size = 'sm'),
            dbc.Popover(
                children = popover_children,
                target='source-' + str(index),
                trigger="hover",
            )
        ]
    )
    return element

def create_unit_button(index, source_text):
    popover_children = [
        dbc.PopoverHeader("Unité : "),
        dbc.PopoverBody(source_text)
    ]
    element = html.Div(
        children = [
            dbc.Button("Unité", id='unit-' + str(index), color="warning", n_clicks=0,outline = True,size = 'sm'),
            dbc.Popover(
                children = popover_children,
                target='unit-' + str(index),
                trigger="hover",
            )
        ]
    )
    return element

def create_selector_scenar(liste_scenar, index = 0 ):
    options = [{'label' : scenar, 'value' : scenar} for scenar in liste_scenar]
    select_scenar = dbc.Row(dcc.Dropdown(
        id={'type' :'scenar-dropdown' , 'index' : index },
        options=options,
        value=liste_scenar[0],
        clearable = False,
        multi =False,
        style = {'width':'80%'}
        ),
        justify = 'center',
        align = 'center',
    )
    texte = create_texte(index = index)
    SELECTOR_scenar = dbc.Card( children =[
    dbc.CardHeader(
        children = ["Choisissez le scénario :", select_scenar]
    ),
    dbc.CardBody(texte)
    ])
    return SELECTOR_scenar

def create_map_giec(data,temp = True):
    colorscale = ['#ffffcc','#ffeda0','#fed976','#feb24c','#fd8d3c','#fc4e2a','#e31a1c','#bd0026','#800026']
    vmin = 0.5
    vmax = 4.8
    color_prop = 'tooltip'
    unit = '°C'
    Id = 'temp'
    if not temp:
        colorscale =['#a16928', '#bd925a', '#d6bd8d', '#edeac2', '#b5c8b8', '#79a7ac', '#2887a1']
        vmin =-15
        vmax = 15
        color_prop = 'tooltip'
        Id = 'temp'
        unit = ''
    geojson = dl.GeoJSON(data=data,
        zoomToBounds=True,  # when true, zooms to bounds when data changes
        options=dict(style=style_assign ),
        hideout=dict(
        colorProp=color_prop,
        min=vmin,
        max=vmax,
        colorscale=colorscale,
        style = dict(weight=0, fillOpacity=0.75 , fillColor ='white')
        ),
    id = Id
    )
    colorbar = dl.Colorbar(colorscale=colorscale, width=20, height=150,min = vmin, max = vmax, unit = unit)
    return geojson, colorbar

def create_graph_giec(index):
    element = dcc.Graph(id = {'type' : 'co2fig', 'index' : index}, config =dict(displayModeBar = False))
    return element

slider_feux = dcc.Slider(
        id = 'slider-feux',
        step = None,
        min=2000,
        max=2110,
        marks = {
            2008: '2008' ,
            2030: '2030',
            2060: '2060',
            2100: '2100'
            },
        value = 2008,
        persistence = False
    )
slider_sech = dcc.Slider(
        id = 'slider-sech',
        step = None,
        min=2000,
        max=2110,
        marks = {
            2008: '2008' ,
            2030: '2030',
            2060: '2060',
            2100: '2100'
            },
        value = 2008,
        persistence = False
    )
dict_range = {2008 : 'REF', 2030: 'H1',2060: 'H2', 2100: 'H3'}
## Create content + Tabs
temp_content = dbc.Card([
    create_selector_scenar( liste_scenar_giec,0),
    create_graph_giec(0), 
    create_source_button(0, source_dict['giec']) 
    ])

prec_content = dbc.Card([
    create_selector_scenar( liste_scenar_giec,1),
    create_graph_giec(1), 
    create_source_button(1, source_dict['giec'])
    ])

feux_content = dbc.Card([
    create_selector_scenar(liste_scenar_feu,2),
    dbc.Card(id = {'type' : 'feux-dates', 'index' : 2},children = [html.Div('Choisir une date de projection : '), html.Br(),slider_feux], className  ='border-0'),
    dbc.Row(children = [dbc.Col(create_source_button(2, source_dict['drias'])),dbc.Col(create_unit_button(2,unit_text_dict['ifm']))], no_gutters = True)
    ])
sech_content = dbc.Card([
    create_selector_scenar(liste_scenar_feu,3),
    dbc.Card(id = {'type' : 'feux-dates', 'index' : 3},children = [html.Div('Choisir une date de projection : '), html.Br(),slider_sech], className  ='border-0'), 
    dbc.Row(children = [dbc.Col(create_source_button(3, source_dict['drias'])),dbc.Col(create_unit_button(3,unit_text_dict['spi']))], no_gutters = True)
    ])

active_style = {'color' : 'red'}

TAB_TEMP = dbc.Tab(label = 'Température', tab_id = 't', children = temp_content, active_label_style = active_style)
TAB_PREC = dbc.Tab(label = 'Précipitations', tab_id = 'p', children = prec_content, active_label_style = active_style)
TAB_FEU = dbc.Tab(label  = 'Feux de forêt', tab_id = 'f', children = feux_content, active_label_style = active_style)
TAB_SEC = dbc.Tab(label  = 'Sécheresse', tab_id = 's', children = sech_content, active_label_style = active_style)
TABS = dbc.Tabs([TAB_FEU,TAB_PREC,TAB_TEMP, TAB_SEC], id = 'tab', active_tab = '')
#### Page d'acceuil

TITRE = dbc.CardHeader(
    children = dbc.Row([
        html.Img(src=app.get_asset_url('logo.jpeg'), height = 130),
        html.H1('DataClimat', style = {'margin' : 'auto', 'margin-left' : '0.5em', 'font-size' : '10vh'}),
        #html.P('Par Paula Forteza et son équipe.', style = {'position' : 'absolute', 'bottom' : '0', 'right' : '0'})
        ], no_gutters = True),
    style = {'position' : 'relative'},
    className = 'mt-0'
    )

COLLAPSE_BUTTON =  dbc.Row(dbc.Button(
            "A vous de jouer ! ",
            id="collapse-button",
            className="mb-3",
            color="success",
            n_clicks=0,
            size ='lg'
        ),
        justify = 'center'
        )

COLLAPSE_TEXT = html.Div([text_en_tete,liste_texte,texte_fin], style = {'text-justify' : 'justify'})
COLLAPSE_BODY = dbc.Collapse(
    [dbc.CardBody(COLLAPSE_TEXT), COLLAPSE_BUTTON],
    id = 'collapse',
    is_open = True
)



EN_TETE = dbc.Card([TITRE,COLLAPSE_BODY], style = {'width' : '100%'}, className="border-bottom-0")
FOOTER = dbc.CardFooter(children = dbc.Row(['Produit par Paula Forteza et son équipe',dbc.NavLink("Dépôt de code", active=True, href="https://github.com/ThomasBench/DataClimat")]))
###
content = dbc.Row(
    children = [
        dbc.Col(
            children = [
                EN_TETE,
                dbc.Collapse(TABS, id = 'collapse-2', is_open = False),
                FOOTER
                    ],
                md =6,
                style = {'height' : '99.9%', 'overflow-y' : 'auto', 'overflow-x' : 'hidden'},
                align = 'center'
            ),
        dbc.Col(element, md = 6)
        ],
    no_gutters = True,
    style = {'height' : '100vh'}
    )

### Render the app

app.layout = html.Div(children = [content])
app.title = 'DataClimat'

### Pour le bouton
# app.clientside_callback(
#     """
#     function(click, open) {
#         if (click){
#             return !open
#         } else {
#             return open
#         }
#     }
#     """,
#     Output('collapse', 'is_open'),
#     Input('collapse-button', 'n_clicks'),
#     State('collapse', 'is_open')
# )
app.clientside_callback(
    """
    function(click, open) {
        if (click){
            return !open
        } else {
            return open
        }
    }
    """,
    Output('collapse-2', 'is_open'),
    Input('collapse-button', 'n_clicks'),
    State('collapse-2', 'is_open')
)

app.clientside_callback(
    """
    function(click) {
        if (click){
            return 'f'
        } else {
            return ''
        }
    }
    """,
    Output('tab', 'active_tab'),
    Input('collapse-button', 'n_clicks'),
)

@app.callback(
[Output({'type' : 'feux-dates', 'index' : MATCH},'children')],
[Input({'type' :'scenar-dropdown' , 'index' : MATCH}, 'value')],
State({'type' :'scenar-dropdown' , 'index' : MATCH}, 'id')
)
def modify_slider(scenario,Id):
    new_id = ''
    if Id['index'] == 2:
        new_id = 'slider-feux'
    if Id['index'] == 3:
        new_id = 'slider-sech'
    if scenario != 'Référence':
        horizon_range = dcc.Slider(
        id = new_id,
        step = None,
        min=2015,
        max=2110,
        marks = {
            2008: '2008' ,
            2030: '2030',
            2060: '2060',
            2100: '2100'
            },
        value = 2030
        )
        children = [[html.Div('Choisir une date de projection : '), html.Br(),horizon_range]]
        return children
    else :
        horizon_range = dcc.Slider(
        id = new_id,
        step = None,
        min=2007,
        max=2009,
        marks = {
            2008: '2008'
            },
        value = 2008
        )
        element= dcc.Input(value = 2008, id = new_id, readOnly  =True, style ={'border-style' : 'none', 'width' : '4vw'} )
        children = [[html.P('Date de référence : '), element]]
        return children


@app.callback(
    Output({'type' :'text-indic' , 'index' : MATCH },'children'),
    Input({'type' :'scenar-dropdown' , 'index' : MATCH } , 'value')
)
def change_text(value):

    return text_dict[value]

@app.callback(
    [Output('map', 'children'),Output('colorbar','children' ), Output('coucou', 'url')],
    [Input({'type' :'scenar-dropdown' , 'index' : ALL }, 'value'),Input("tab", "active_tab"), Input('slider-feux', 'value'), Input('slider-sech', 'value')],
    State('map','children')
)
def change_map(scenar, active_tab,slider_feux,slider_sech, childs):
    while len(childs) > 3:
        childs.pop()
    childs += [dl.GestureHandling()]
    if active_tab == '':
        return childs, {}, ''
    if active_tab == 't':

        geo_map , colorbar = create_map_giec(df_dict_temp[scenar[2]])
        childs += [geo_map, france_contour,cities_point]
        return childs, colorbar, ''

    elif active_tab == 'p' :

        geo_map , colorbar = create_map_giec(df_dict_prec[scenar[1]], temp = False)
        childs += [geo_map, france_contour,cities_point]

        return childs, colorbar, ''

    elif active_tab == 'f':
        colorscale =["#ED2938", "#FF8C01","#FFAA1C","#FFE733","#006B3E","#024E1B"]
        nom = dict_scenar_feux[scenar[0]] + dict_range[slider_feux]
        colorscale.reverse()
        colorbar = dl.Colorbar(colorscale=colorscale, width=20, height=150,min = 0, max = 30, unit = 'IFM')
        chosen_url = url_dict_feux[nom]
        childs += [france_contour,cities_point]
        return childs,colorbar, chosen_url
    elif active_tab == 's':
        colorscale =['#a16928', '#bd925a', '#d6bd8d', '#edeac2', '#b5c8b8', '#79a7ac', '#2887a1']
        nom = dict_scenar_feux[scenar[3]] + dict_range[slider_sech]
        colorbar = dl.Colorbar(colorscale=colorscale, width=20, height=150,min = -2, max = 0.6, unit = 'SPI')
        chosen_url = url_dict_sech[nom]
        childs += [france_contour,cities_point]
        return childs,colorbar, chosen_url


#### The callbacks

@app.callback(
    Output({'type' : 'co2fig', 'index' : MATCH}, 'figure'),
    Input({'type' :'scenar-dropdown' , 'index' : MATCH}, 'value')
)
def modify_fig(scenar):
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x = co2_df['years'],
            y = co2_df[scenar],
            mode = 'lines',
            line = dict(
                color = 'red',
                shape = 'spline',
                width = 2
            ),
            fill='tozeroy',
            hovertemplate = '%{y} kT <extra></extra>'
        )
    )

    fig.update_layout(template = 'none', title = 'Projection des émissions de CO2 selon le scénario ' + scenar)
    fig.update_yaxes(title = 'kT')
    fig.add_vline(x =2015,
                annotation_text="Début de la projection ", annotation_position="top left",
                fillcolor="gray", opacity=1, line_width=3)

    return fig

