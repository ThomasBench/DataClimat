# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import pandas as pd 
import xarray as xr
import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc 
import dash_daq as daq
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_leaflet as dl
from dash_extensions.javascript import assign, arrow_function
import plotly.express as px
import plotly.graph_objects as go 
import dash_leaflet.express as dlx
def point_to_poly(point_geo):
    geometry = point_geo['geometry']
    geometry['type'] = 'Polygon'
    coord = geometry['coordinates']
    list_coord = [[-0.5,-0.5],[0.5,-0.5],[0.5,0.5],[-0.5,0.5]]
    list_coord = [ [coord[0] + a , coord[1] + b] for [a,b] in list_coord]
    list_coord.append(list_coord[0])
    geometry['coordinates'] = [list_coord]
    return point_geo
def treat_nc(path, pluie = False):
    ds = xr.open_dataset(path)
    df = ds.to_dataframe().reset_index().drop(columns = ['panel', 'conflict', 'non_robust', 'model_nr'])
    code = 'tas'
    if pluie:
        code ='pr'
    df.columns = ['tooltip' if x==code else x for x in df.columns]

    df.lon = (df.lon % 360 + 540) % 360 - 180
    df = df[df.lon < 30]
    df = df[df.lon > -20]
    df = df[df.lat< 61.0]
    df = df[df.lat> 32]
    mmax , mmin = df.tooltip.max(), df.tooltip.min()
    dico = df.to_dict('rows')
    geo_json = dlx.dicts_to_geojson(dico)
    for element in geo_json['features'] : 
        element = point_to_poly(element)
    # print(mmax,mmin)
    return geo_json

def rgb_to_hex(rgb):
    return '#'+ '%02x%02x%02x' % rgb

###########Load the data
liste_scenar = ['ssp119','ssp126','ssp585']

df_dict_temp  = {
    'ssp119' : treat_nc('D:\Stage\Climat\Giec\Panel_b1_Simulated_temperature_change_at_1_5C.nc'),
    'ssp126' : treat_nc('D:\Stage\Climat\Giec\Panel_b2_Simulated_temperature_change_at_2C.nc'),
    'ssp585' : treat_nc('D:\Stage\Climat\Giec\Panel_b3_Simulated_temperature_change_at_4C.nc')
    }
dict_temp = {'ssp119' : '+1.5°C','ssp126' : '+2°C','ssp585' : '+4°C'}
df_dict_prec = {
    'ssp119' : treat_nc('D:\Stage\Climat\Giec\Panel_c1_Simulated_precipitation_change_at_1_5C.nc', pluie = True),
    'ssp126' : treat_nc('D:\Stage\Climat\Giec\Panel_c2_Simulated_precipitation_change_at_2C.nc', pluie = True),
    'ssp585' : treat_nc('D:\Stage\Climat\Giec\Panel_c3_Simulated_precipitation_change_at_4C.nc', pluie = True),

}
text_dict = {
    'ssp119' : 
        '''Le monde 
            s'oriente progressivement, mais de manière généralisée, vers une voie plus durable, en mettant l'accent 
            sur un développement plus inclusif qui respecte les limites environnementales perçues. La gestion des biens 
            communs mondiaux s'améliore lentement, les investissements dans l'éducation et la santé accélèrent la 
            transition démographique, et l'accent mis sur la croissance économique se transforme en un accent plus large 
            sur le bien-être humain. Sous l'impulsion d'un engagement croissant en faveur de la réalisation des objectifs 
            de développement, les inégalités se réduisent tant entre les pays qu'à l'intérieur de ceux-ci. La consommation
            est orientée vers une faible croissance matérielle et une moindre intensité en ressources et en énergie. 
            Les émissions de gaz à effet de serre sont restreintes au strict minimum.''',
    'ssp126' : 
        '''Le monde 
            s'oriente progressivement, mais de manière généralisée, vers une voie plus durable, en mettant l'accent 
            sur un développement plus inclusif qui respecte les limites environnementales perçues. La gestion des biens 
            communs mondiaux s'améliore lentement, les investissements dans l'éducation et la santé accélèrent la 
            transition démographique, et l'accent mis sur la croissance économique se transforme en un accent plus large 
            sur le bien-être humain. Sous l'impulsion d'un engagement croissant en faveur de la réalisation des objectifs 
            de développement, les inégalités se réduisent tant entre les pays qu'à l'intérieur de ceux-ci. La consommation
            est orientée vers une faible croissance matérielle et une moindre intensité en ressources et en énergie. 
            Les émissions de gaz à effet de serre sont fortement réduite.''',
    'ssp585' :
        '''Ce monde 
        fait de plus en plus confiance aux marchés compétitifs, à l'innovation et aux sociétés participatives pour produire 
        des progrès technologiques rapides et développer le capital humain comme voie vers le développement durable. Les 
        marchés mondiaux sont de plus en plus intégrés. Il y a également de forts investissements dans la santé, l'éducation 
        et les institutions pour améliorer le capital humain et social. Dans le même temps, la poussée du développement 
        économique et social va de pair avec l'exploitation d'abondantes ressources en combustibles fossiles et l'adoption de 
        modes de vie à forte intensité de ressources et d'énergie dans le monde entier. Tous ces facteurs entraînent une 
        croissance rapide de l'économie mondiale, tandis que la population mondiale atteint un pic et décline au cours du 21e 
        siècle. Les problèmes environnementaux locaux, comme la pollution atmosphérique, sont gérés avec succès. On croit en 
        la capacité de gérer efficacement les systèmes sociaux et écologiques, y compris par la géo-ingénierie si nécessaire.''',
    }





#### Create the Viz

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

geojson = dl.GeoJSON(data={},
                     zoomToBounds=True,  # when true, zooms to bounds when data changes
                     options=dict(style=style_assign ),
                     hideout=dict(
                        colorProp=color_prop,
                        min=vmin,
                        max=vmax,
                        colorscale=colorscale,
                        style = dict(weight=0, fillOpacity=0.75 , fillColor ='white')
                        ),
                    id = 'map'
                    )
options = [{'label' : scenar, 'value' : scenar} for scenar in liste_scenar]
select_scenar = dbc.Row(dcc.Dropdown(
        id='scenar-dropdown',
        options=options,
        value='ssp585',
        clearable = False,
        multi =False,
        style = {'width':'80%'}
        ),
        justify = 'center',
        align = 'center',

    )



toggle = dbc.Row(children= [
    html.Div('Température    '),daq.ToggleSwitch(id = 'temp-toggle', size=  50, value = False ) , html.Div('   Précipitations')
    ],
    justify = 'center', align ='center'
)

texte = dbc.Row(id = 'text-indic', style = { 'text-justify' : 'auto' ,'border-radius' : '5px' ,'overflow' : 'auto'})

SELECTOR_indic = dbc.Card([dbc.CardHeader("Choisissez l'indicateur :"),dbc.CardBody(toggle)])



SELECTOR_scenar = dbc.Card( children =[
    dbc.CardHeader(
        children = ["Choisissez le scénario :", select_scenar]
    ),
    dbc.CardBody(texte)
])


info = dbc.Card(children= dbc.Col([SELECTOR_indic,SELECTOR_scenar]), id='info',
                style={'height' : '50vh', "z-index": "500"})
element = dl.Map(
    children=[dl.TileLayer(),geojson, html.Div(id = 'colorbar', children = colorbar)],
    bounds  = [[32, -20], [61,30]] ,
    style={'width': '100%', 'height': '100vh', 'margin': "auto",'z-index' : '300', "display": "block"} ) 
content = dbc.Row(children = [dbc.Col(info, md =4 ), dbc.Col(dcc.Loading(element), md = 8)], no_gutters = True)

### Render the app
chroma = "https://cdnjs.cloudflare.com/ajax/libs/chroma-js/2.1.0/chroma.min.js"
app = dash.Dash(__name__, external_scripts=[chroma], external_stylesheets=[dbc.themes.SIMPLEX])
app.layout = html.Div(children = [content])
app.title = 'GIEC data'

@app.callback(
    Output('text-indic','children'),
    Input('scenar-dropdown' , 'value')
)
def change_text(value):
    print(value)
    return text_dict[value]

@app.callback(
    [Output('map', 'data'), Output('map','hideout'),Output('colorbar','children' )],
    [Input('scenar-dropdown', 'value'), Input('temp-toggle' , 'value')],
    State('map','hideout')
)
def change_map(scenar, temp, hideout):

    if not temp:
        colorscale = ['#ffffcc',
        '#ffeda0',
        '#fed976',
        '#feb24c',
        '#fd8d3c',
        '#fc4e2a',
        '#e31a1c',
        '#bd0026',
        '#800026']
        vmin = 1
        vmax = 4
        hideout['min']=vmin
        hideout['max']=vmax
        colorbar = dl.Colorbar(colorscale=colorscale, width=20, height=150, min=vmin, max=vmax, unit = '°C')
        hideout['colorscale']=colorscale
        return df_dict_temp[scenar], hideout, colorbar
    else: 
        colorscale =['#a16928', '#bd925a', '#d6bd8d', '#edeac2', '#b5c8b8', '#79a7ac', '#2887a1']
        vmin =-15
        vmax = 15
        hideout['min']=vmin
        hideout['max']=vmax
        hideout['colorscale']=colorscale
        colorbar = dl.Colorbar(colorscale=colorscale, width=20, height=150,min = vmin, max = vmax, unit = 'mm')
        return df_dict_prec[scenar], hideout, colorbar 

#### The callbacks



if __name__ == "__main__":
    app.run_server(debug=True, use_reloader = False)


# %%



