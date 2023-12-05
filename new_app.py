# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import pandas as pd
import sys 
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import xarray as xr
import dash
from dash import dcc
import dash_bootstrap_components as dbc
import dash_daq as daq
from dash import html
from dash.dependencies import Input, Output, State , MATCH , ALL
import dash_leaflet as dl
from dash_extensions.javascript import assign, arrow_function
import dash_leaflet.express as dlx
from pathlib import Path
import json
import os
from collections import ChainMap
import plotly.graph_objects as go
from ipcc_helpers import *
ROOT_DIR = str(Path().resolve()) + '/data'
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

chroma = "https://cdnjs.cloudflare.com/ajax/libs/chroma-js/2.1.0/chroma.min.js"
app = dash.Dash(__name__, external_scripts=[chroma], external_stylesheets=[dbc.themes.LUMEN], update_title=None, meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1, minimum-scale=1,maximum-scale= 1"}
    ])
###########Load the data
def create_co2fig(scenar):
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
    fig.update_layout(dragmode=False,template = 'none', title = 'Emissions de CO2,<br> scénario ' + scenar)
    fig.update_yaxes(title = 'kT')
    fig.add_vline(x =2015,
                annotation_text="Début de la projection ", annotation_position="top left",
                fillcolor="gray", opacity=1, line_width=3)
    return fig

def create_map_giec(data,temp = True):
    colorscale = ['#ffffcc','#ffeda0','#fed976','#feb24c','#fd8d3c','#fc4e2a','#e31a1c','#bd0026','#800026']
    vmin = 0.5
    vmax = 4.8
    color_prop = 'tooltip'
    Id = 'temp'
    if not temp:
        colorscale =['#a16928', '#bd925a', '#d6bd8d', '#edeac2', '#b5c8b8', '#79a7ac', '#2887a1']
        vmin =-15
        vmax = 15
        color_prop = 'tooltip'
        Id = 'temp'
    geojson = dl.GeoJSON(data=data, format = 'geojson',
        # zoomToBounds=True,  # when true, zooms to bounds when data changes
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
    return geojson



###### GIEC
liste_scenar_giec = ['ssp119','ssp126','ssp585']
df_dict_temp  = {
    'ssp119' : create_map_giec(data = treat_nc(ROOT_DIR + '/temprec' + '/Panel_b1_Simulated_temperature_change_at_1_5C.nc')),
    'ssp126' : create_map_giec(data =treat_nc(ROOT_DIR + '/temprec' + '/Panel_b2_Simulated_temperature_change_at_2C.nc')),
    'ssp585' : create_map_giec(data =treat_nc(ROOT_DIR + '/temprec' + '/Panel_b3_Simulated_temperature_change_at_4C.nc'))
    }
dict_temp = {'ssp119' : '+1.5°C','ssp126' : '+2°C','ssp585' : '+4°C'}
df_dict_prec = {
    'ssp119' : create_map_giec(data = treat_nc(ROOT_DIR + '/temprec' + '/Panel_c1_Simulated_precipitation_change_at_1_5C.nc',pluie = True),  temp = False),
    'ssp126' : create_map_giec(data = treat_nc(ROOT_DIR + '/temprec' + '/Panel_c2_Simulated_precipitation_change_at_2C.nc', pluie = True), temp = False),
    'ssp585' : create_map_giec(data = treat_nc(ROOT_DIR + '/temprec' + '/Panel_c3_Simulated_precipitation_change_at_4C.nc', pluie = True), temp = False)
}
#### Source drias : http://www.drias-climat.fr/accompagnement/sections/174
#### Source Giec : https://fr.wikipedia.org/wiki/Trajectoires_socio%C3%A9conomiques_partag%C3%A9es
source_dict = {
    'giec' : '- Données : https://www.ipcc.ch/report/ar6/wg1/  \n -Texte : https://fr.wikipedia.org/wiki/Trajectoires_socio%C3%A9conomiques_partag%C3%A9es',
    'drias' : '- Données : http://www.drias-climat.fr/ \n - Texte : http://www.drias-climat.fr/accompagnement/sections/174'
}
co2_df = pd.read_csv(ROOT_DIR + r'/co2/aggregated.csv')
liste_scenarios = co2_df.columns.tolist()[1:]
dict_fig = dict(ChainMap(*[{scenar : create_co2fig(scenar)} for scenar in liste_scenar_giec]))

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
dict_scenar ={liste_scenar_feu[0]:'ref', liste_scenar_feu[1]:'opti', liste_scenar_feu[2]:'inter', liste_scenar_feu[3]:'pess'}

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
    'ssp119' :html.Div([dcc.Graph(figure = dict_fig['ssp119'] , config  = dict(scrollZoom = False,responsive = True,displayModeBar = False)),dcc.Markdown(
        '''
        Le scénario SSP1 est initialement intitulé *La route verte* par le GIEC. Dans celui-ci, le monde s'oriente progressivement, 
        mais de manière généralisée, vers une voie plus durable, en mettant l'accent sur un développement plus inclusif qui respecte 
        les limites environnementales perçues. La gestion des biens communs mondiaux s'améliore lentement, les investissements dans 
        l'éducation et la santé accélèrent la transition démographique, et l'accent mis sur la croissance économique se transforme en un 
        accent plus large sur le bien-être humain. Sous l'impulsion d'un engagement croissant en faveur de la réalisation des objectifs de 
        développement, les inégalités se réduisent tant entre les pays qu'à l'intérieur de ceux-ci. La consommation est orientée vers une 
        faible croissance matérielle et une moindre intensité en ressources et en énergie.** Ce scénario prévoit un arrêt total des émissions 
        de CO2 aux alentours de 2050.** ''')], style  = {'width' : '99%', 'overflow' : 'auto'}),
    'ssp126' :html.Div([dcc.Graph(figure = dict_fig['ssp126'] , config  = dict(scrollZoom = False,responsive = True,displayModeBar = False)),dcc.Markdown(
        '''Ce scénario est similaire au scénario précédent SSP1 - 1.9 à une différence près : 
        **l’arrêt total des émissions de CO2 est ici prévu aux alentours de 2075**.''')], style = {'margin': 'auto'}),
    'ssp585' :html.Div([dcc.Graph(figure = dict_fig['ssp585'] , config  = dict(scrollZoom = False,responsive = True,displayModeBar = False)),dcc.Markdown(
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
            d’ici 2075. **''')]),
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
        html.Ul("Précipitations et températures → Vous pouvez choisir de visualiser six scénarios issus du dernier rapport du GIEC. Pour chacun d’entre eux, vous disposez d’une projection des émissions de CO2 en fonction du scénario choisi.")
    ],
    style = {'list-style-type': 'none'}
)
texte_fin = html.P("Une fois votre sélection effectuée, la visualisation des indicateurs choisis s’affichera sur la carte.")



#### Create the Viz


##For the map :
color_prop  = 'tooltip'
colorscale = ['#ffbaba','#ff7b7b','#ff5252','#ff0000','#a70000']
vmin, vmax = 1 , 2
colorbar = dl.Colorbar(colorscale=colorscale, width=20, height=150, min=vmin, max=vmax, unit = '°C')


france_contour = dl.GeoJSON(data = france_geo, options =dict(style = {'fill' : False, 'color' : 'black', 'weight' : 1} ) )
cities_point = dl.GeoJSON(data = cities_geo, options = dict(pointToLayer = point_style))



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
        dbc.PopoverBody(source_text ,className = 'unitbutton')
    ]
    element = html.Div(
        children = [
            dbc.Button("Unité", id='unit-' + str(index), color="warning", n_clicks=0,outline = True,size = 'sm'),
            dbc.Popover(
                children = popover_children,
                target='unit-' + str(index),
                trigger="hover"

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
        searchable = False,
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
    dbc.CardBody(texte, style = {'padding' : '17px'})
    ])
    return SELECTOR_scenar


def create_colorbar(indicateur):
    if indicateur == 'prec' : 
        colorscale =['#a16928', '#bd925a', '#d6bd8d', '#edeac2', '#b5c8b8', '#79a7ac', '#2887a1']
        vmin =-15
        vmax = 15
        unit = ''
        colorbar = dl.Colorbar(colorscale=colorscale, width=20, height=150,min = vmin, max = vmax, unit = unit)
        return colorbar
    if indicateur == 'temp' : 
        colorscale = ['#ffffcc','#ffeda0','#fed976','#feb24c','#fd8d3c','#fc4e2a','#e31a1c','#bd0026','#800026']
        vmin = 0.5
        vmax = 4.8
        unit = '°C'
        colorbar = dl.Colorbar(colorscale=colorscale, width=20, height=150,min = vmin, max = vmax, unit = unit)
        return colorbar
    if indicateur == 'feux' : 
        colorscale = ["#ED2938", "#FF8C01","#FFAA1C","#FFE733","#006B3E","#024E1B"]
        colorscale.reverse()
        colorbar = dl.Colorbar(colorscale=colorscale, width=20, height=150,min = 0, max = 30, unit = 'IFM')
        return colorbar
    if indicateur == 'sech' : 
        colorscale =['#a16928', '#bd925a', '#d6bd8d', '#edeac2', '#b5c8b8', '#79a7ac', '#2887a1']
        colorbar = dl.Colorbar(colorscale=colorscale, width=20, height=150,min = -2, max = 0.6, unit = 'SPI')
        return colorbar

def create_graph_giec(index):
    element = dcc.Graph(id = {'type' : 'co2fig', 'index' : index}, config =dict(scrollZoom = False,responsive = True,displayModeBar = False))
    return element

def create_visu_button(index) : 
    element =dbc.Button(
        id = {'type' : 'visu-button', 'index' :index},
        children = 'Voir la carte',
        color = 'success',
        size = 'lg'
    )

    return element

def create_slider(indic, index):
    new_id = f'slider-{indic}'
    if index != 'ref':
        horizon_range = dcc.Slider(
        id = new_id,
        step = None,
        min=2015,
        max=2110,
        marks = {
            2030: '2030',
            2060: '2060',
            2100: '2100'
            },
        value = 2030
        )
        children = [html.Div('Choisir une date de projection : '), html.Br(),horizon_range]
        return [children]
    else :
        element= dcc.Input(value = 2008, id = new_id, readOnly  =True, style ={'border-style' : 'none', 'width' : '50%'} )
        children = [html.P('Date de référence : '), element]
        return [children]


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
    # create_graph_giec(0), 
    create_visu_button(0),
    create_source_button(0, source_dict['giec']) 
    ])

prec_content = dbc.Card([
    create_selector_scenar( liste_scenar_giec,1),
    # create_graph_giec(1), 
    create_visu_button(1),
    create_source_button(1, source_dict['giec'])
    ])

feux_content = dbc.Card([
    create_selector_scenar(liste_scenar_feu,2),
    dbc.Card(id = {'type' : 'feux-dates', 'index' : 2},children = [html.Div('Choisir une date de projection : '), html.Br(),slider_feux], className  ='border-0'),
    create_visu_button(2),
    dbc.Row(children = [dbc.Col(create_source_button(2, source_dict['drias'])),dbc.Col(create_unit_button(2,unit_text_dict['ifm']))])
    ])
sech_content = dbc.Card([
    create_selector_scenar(liste_scenar_feu,3),
    dbc.Card(id = {'type' : 'feux-dates', 'index' : 3},children = [html.Div('Choisir une date de projection : '), html.Br(),slider_sech], className  ='border-0'), 
    create_visu_button(3),
    dbc.Row(children = [dbc.Col(create_source_button(3, source_dict['drias'])),dbc.Col(create_unit_button(3,unit_text_dict['spi']))])
    ])


#### Page d'acceuil

map_dict = {
    'giec': {
        'temp' : {
            'map_dict' : df_dict_temp,
            'colorbar'  : create_colorbar('temp')
        },
        'prec' : {
            'map_dict' : df_dict_prec,
            'colorbar'  : create_colorbar('prec')

        },
    },
    'drias' : {
        'indic' : {
            'scenar_dict' : dict_scenar,
            'range_dict' : dict_range,
        },
        'feux' : {
            'url_dict' : url_dict_feux,
            'colorbar' : create_colorbar('feux')
        },
        'sech' : {
            'url_dict' : url_dict_sech,
            'colorbar' : create_colorbar('sech')
        }
    },
    'autre': {
        'france' : france_contour,
        'villes' : cities_point
    }
}

content_dict = {
    'text' :text_dict,
    'fig' : dict_fig,
    'sliders':{
        'ref' : {
            'feux' : create_slider('feux', 'ref'),
            'sech' : create_slider('sech', 'ref')
        },
        'other' : {
            'feux' : create_slider('feux', 'other'),
            'sech' : create_slider('sech', 'other')
        }
    }
}
###

BUTTON_TEMP = dbc.Button('Températures', id = 'b-temp',color = 'warning',n_clicks = 0, className = 'btn-block')
BUTTON_PREC = dbc.Button('Précipitations', id = 'b-prec',color = 'primary',n_clicks = 0)
BUTTON_FEUX = dbc.Button('Feux de Forêts', id = 'b-feux',color = 'danger',n_clicks = 0)
BUTTON_SECH = dbc.Button('Sécheresses', id = 'b-sech',color = 'secondary',n_clicks = 0)
INFO_BUTTON = dbc.Button(
        "i ",
        id="b-accu",
        className="mb-3",
        color="success",
        n_clicks=0,
        size ='lg',
        style = {
            'font-family' : 'Alice',
            'text-transform': 'lowercase',
            'border-radius' : '100%'
            }
            )


JOUER_BUTTON = dbc.Button(
            "A vous de jouer ! ",
            id="b-accu",
            className="mb-3",
            color="success",
            n_clicks=0,
            size ='lg'
        )


COLLAPSE_CONTAINER =  dbc.Row(id = 'button-container-row', children = [JOUER_BUTTON],justify = 'center')
INFO_CONTAINER = dbc.Row(
    id = 'button-container-info', 
    children = [],
    style = {
        'position' : 'absolute' ,
        'top' : '2em', 
        'z-index' : '50', 
        'left': '50%',
        'width' : '10%',
        'transform': 'translateX(-50%)',
        },
    justify = 'center')


BUTTON_STORE = dcc.Store(id = 'store-button' , data = {'accueil' : JOUER_BUTTON, 'info' : INFO_BUTTON})

COLLAPSE_TEXT = html.Div([text_en_tete,liste_texte,texte_fin], style = {'text-justify' : 'justify'})
CORPS = dbc.CardBody([COLLAPSE_TEXT, COLLAPSE_CONTAINER])

EN_TETE = dbc.CardHeader(
    children = dbc.Row([
        html.Img(src=app.get_asset_url('logo.jpeg'), height = 50),
        html.H1('DataClimat', style = {'margin' : 'auto', 'margin-left' : '0.5em', 'font-size' : '3vh'})
        ]), 
    className = 'mt-0'
    )
FOOTER = dbc.CardFooter(children = dbc.Row(align = 'center', children = ['Produit par Paula Forteza et son équipe',dbc.NavLink("Dépôt de code", active=True, href="https://github.com/ThomasBench/DataClimat")]))
ACCUEIL = dbc.Card(
    children = [
        EN_TETE,
        CORPS,FOOTER
        ], 
    style = {'overflow-y' : 'auto'}
    )


BOUTONS = dbc.ButtonGroup(
            [BUTTON_FEUX,BUTTON_PREC,BUTTON_SECH,BUTTON_TEMP],
            className="mr-1",
            size = 'sm',
            style=  {'position' : 'absolute', 'z-index' : '50', 'bottom' : '1em','left': '50%','transform': 'translateX(-50%)'}
        )


style_collapse = {'position' : 'absolute', 'top' : '1em','z-index' : '100', 'min-height' : '20%','max-height' :'80%', 'width' : '90%', 'overflow-y' : 'auto','left': '50%','transform': 'translateX(-50%)'}

COLLAPSABLE_ACCUEIL = dbc.Collapse(
    id = 'collapse-accueil',
    children = ACCUEIL,
    style =style_collapse,
    is_open = True
    )
COLLAPSABLE_TEMP = dbc.Collapse(
    id = 'collapse-temp',
    children = temp_content,
    style = style_collapse,
    is_open = False
    )
COLLAPSABLE_PREC = dbc.Collapse(
    id = 'collapse-prec',
    children = prec_content,
    style = style_collapse,
    is_open = False
    )
COLLAPSABLE_FEUX = dbc.Collapse(
    id = 'collapse-feux',
    children = feux_content,
    style = style_collapse,
    is_open = False
    )
COLLAPSABLE_SECH = dbc.Collapse(
    id = 'collapse-sech',
    children = sech_content,
    style = style_collapse,
    is_open = False
    )

collapse_store = dcc.Store(id = 'store-collapse', data = {'open' : True, 'content_id' : 'b-accu'} )
content_store = dcc.Store(id= 'store-content', data = content_dict)
map_store = dcc.Store(id = 'store-map', data = map_dict)
### 
MAP = dl.Map(
    children=[
        dl.TileLayer(attribution = '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'),
        dl.TileLayer(id = 'drias', url = ''),
        html.Div(id = 'colorbar', children = [])
        ],
    id = 'map',
    center=(46, 2),
    zoom=6,
    style={'width': '100%', 'height': '100vh', 'margin': "auto",'z-index' : '1', "display": "block"}, 
    scrollWheelZoom = False
    )
CONTENT = [MAP,COLLAPSABLE_ACCUEIL,COLLAPSABLE_TEMP, COLLAPSABLE_PREC, COLLAPSABLE_FEUX,COLLAPSABLE_SECH]
CONTROLS = [ BOUTONS, INFO_CONTAINER]
STORES = [collapse_store, BUTTON_STORE, map_store, content_store]
### Render the app

app.layout = html.Div(children = CONTENT + CONTROLS + STORES)
app.title = 'DataClimat'



#### The callbacks
def apply_clientside_callbacks(app):

    ### Update slider 
    app.clientside_callback(
        '''
        function update_slider(horizon, index, data){

            if(horizon != 'Référence'){
                horizon = 'other'
            } else {
                horizon = 'ref'
            }
            indic = ''

            index = index['index']
            if (index == 3){
                indic = 'sech'
            }
            if (index == 2){
                indic = 'feux'
            }
            child = data['sliders'][horizon][indic]
            return child
        }
        ''',
        [Output({'type' : 'feux-dates', 'index' : MATCH},'children')],
        [Input({'type' :'scenar-dropdown' , 'index' : MATCH}, 'value')],
        State({'type' :'scenar-dropdown' , 'index' : MATCH}, 'id'), State('store-content', 'data')
    )

    ### Select fig
    app.clientside_callback(
        '''
        function select_fig(scenar,dico){
            console.log(dash_clientside.callback_context.triggered.map(t => t.prop_id))
            return dico['fig'][scenar]
        }
        ''',
        Output({'type' : 'co2fig', 'index' : MATCH}, 'figure'),
        Input({'type' :'scenar-dropdown' , 'index' : MATCH}, 'value'),
        State('store-content','data' )
    )

    ### Update accueil bouton
    app.clientside_callback(
        '''
        function update_accueil_button(dico,bouttons){
            const is_open = dico['open'];
            const accueil = dico['content_id'];
            if (is_open && accueil == 'b-accu') {
                return [[bouttons['accueil']],[]]
            }
            else {
                return [[] , bouttons['info']]
            }
        }
        ''',
        Output('button-container-row','children'), Output('button-container-info', 'children'),
        Input('store-collapse' , 'data'), State('store-button', 'data')
    )

    ### Update texte 
    app.clientside_callback(
        '''
        function change_text(value, dico){
            return dico['text'][value]
        }
        ''',
        Output({'type' :'text-indic' , 'index' : MATCH },'children'),
        Input({'type' :'scenar-dropdown' , 'index' : MATCH } , 'value'), State('store-content', 'data')
    )

    ### Big click dispatcher
    app.clientside_callback(
        """
        function big_dispatcher_2(accueil_b,temp,prec,feux,sech,map_click,visu_b,collapse_data) {
            trigger_id = dash_clientside.callback_context.triggered.map(t => t.prop_id);
            if (trigger_id.length == 0) {return collapse_data};
            trigger_id = trigger_id[0].substring(0,6);
            collapse_open = collapse_data['open'];
            new_content_id = collapse_data['content_id'];
            if (trigger_id == 'map.cl' || trigger_id == '{"inde') {return {'open' : false, 'content_id' : new_content_id} }
            if (trigger_id == new_content_id){
                collapse_open = !collapse_open;
            } else {
                collapse_open = true;
                new_content_id = trigger_id
            }
            return {'open' : collapse_open, 'content_id' : new_content_id} 
        }
        
        """,
        Output('store-collapse', 'data'),
        Input('b-accu', 'n_clicks'),Input('b-temp', 'n_clicks'),Input('b-prec', 'n_clicks'),Input('b-feux', 'n_clicks'),Input('b-sech', 'n_clicks'),Input('map' , 'click_lat_lng'),Input({'type' : 'visu-button', 'index' : ALL}, 'n_clicks'),
        State('store-collapse', 'data')
    )

    # Render collapse
    app.clientside_callback(
        '''
        function collapse_renderer(collapse_data){
            content_id = collapse_data['content_id'];
            is_open = collapse_data['open'];
            if (is_open){
                switch (content_id){
                    case 'b-accu':
                        return [false, false, false, false,true]
                    case 'b-temp':
                        return [true, false, false, false,false]
                    case 'b-prec':
                        return [false, true, false, false,false]   
                    case 'b-feux':
                        return [false, false, true, false,false]   
                    case 'b-sech':
                        return [false, false, false, true,false]        
                }
            } else { return [false, false, false, false,false]  }
        }
        ''',
        [
            Output('collapse-temp','is_open'),
            Output('collapse-prec','is_open'),
            Output('collapse-feux','is_open'),
            Output('collapse-sech','is_open'),
            Output('collapse-accueil','is_open')
            ],
        Input('store-collapse', 'data'),
    )

    # Update the map 
    app.clientside_callback(
        '''
        function update_map(scenars, indicateur, slider_feux, slider_sech, childs, map_store ){
            while(childs.length > 3 ) {
                childs.pop()
            }
            active_tab = indicateur['content_id']
            switch (active_tab){
                case '':
                    return [childs, {}, '']
                case 'b-accu':
                    return [childs, {},'']
                case 'b-temp':
                    scenar = scenars[0];
                    dico = map_store['giec']['temp'];
                    colorbar = dico['colorbar'];
                    geomap = dico['map_dict'][scenar];
                    console.log(geomap)
                    france = map_store['autre']['france'];
                    villes = map_store['autre']['villes'];
                    ajout_child = [geomap,france,villes];
                    childs = childs.concat(ajout_child);
                    return [childs,colorbar, 'coucou.com']
                case 'b-prec':
                    scenar = scenars[1];
                    dico = map_store['giec']['prec'];
                    colorbar = dico['colorbar'];
                    geomap = dico['map_dict'][scenar];
                    france = map_store['autre']['france'];
                    villes = map_store['autre']['villes'];
                    ajout_child = [geomap,france,villes];
                    childs = childs.concat(ajout_child);
                    return [childs,colorbar, 'coucou.com']
                case 'b-feux':
                    scenar = scenars[2];
                    dico = map_store['drias']['feux'];
                    helpers = map_store['drias']['indic'];
                    dict_scenar = helpers['scenar_dict'];
                    dict_range = helpers['range_dict'];
                    nom = dict_scenar[scenar] + dict_range[slider_feux]
                    colorbar = dico['colorbar'];
                    url = dico['url_dict'][nom];
                    france = map_store['autre']['france'];
                    villes = map_store['autre']['villes'];
                    ajout_child = [france,villes];
                    childs = childs.concat(ajout_child);
                    return [childs,colorbar, url]
                case 'b-sech':
                    scenar = scenars[3];
                    dico = map_store['drias']['sech'];
                    helpers = map_store['drias']['indic'];
                    dict_scenar = helpers['scenar_dict'];
                    dict_range = helpers['range_dict'];
                    nom = dict_scenar[scenar] + dict_range[slider_sech]
                    colorbar = dico['colorbar'];
                    url = dico['url_dict'][nom];
                    france = map_store['autre']['france'];
                    villes = map_store['autre']['villes'];
                    ajout_child = [france,villes];
                    childs = childs.concat(ajout_child);
                    return [childs,colorbar, url]

            }
        }
        ''',
        [Output('map', 'children'),Output('colorbar','children' ), Output('drias', 'url')],
        [Input({'type' :'scenar-dropdown' , 'index' : ALL }, 'value'),Input("store-collapse", "data"), Input('slider-feux', 'value'), Input('slider-sech', 'value')],
        State('map','children'), State('store-map', 'data')
    )

apply_clientside_callbacks(app)


app.run_server(debug = True, use_reloader = True)