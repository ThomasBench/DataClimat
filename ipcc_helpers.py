import pandas as pd 
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import xarray as xr
import dash_leaflet.express as dlx
import os



def treat_fire(path):
    dict_df = {}
    for file in os.scandir(path):
        df = pd.read_csv(file.path,comment = '#', encoding= 'ISO-8859-1', delimiter = ';').drop(columns = ['Point', 'Unnamed: 9','Contexte', 'NORIFM20','NORIFM40','NORIFM60'])
        horizons = list(df.iloc[:,2].drop_duplicates())

        for horizon in horizons:
            nom = file.name[5:-4] + horizon
            code = 'NORIFM' 
            temp_df = df[df.iloc[:,2] == horizon]
            temp_df = temp_df[temp_df.index % 2 == 0]
            temp_df.columns = ['tooltip' if x==code else x for x in df.columns]
            dico = temp_df.to_dict('rows')
            geo_json = dlx.dicts_to_geojson(dico, lon = 'Longitude', lat = 'Latitude')

            for element in geo_json['features'] : 
                element = point_to_poly(element, scale = 0.031,xscale = 3)
            geobuf =  dlx.geojson_to_geobuf(geo_json)
            dict_df.update({nom:geobuf})
    return dict_df


def point_to_poly(point_geo,scale = 0.5, xscale = 1):
    geometry = point_geo['geometry']
    geometry['type'] = 'Polygon'
    coord = geometry['coordinates']
    list_coord = [[-scale*xscale,-scale],[scale*xscale,-scale],[scale*xscale,scale],[-scale*xscale,scale]]
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
    geo_json = dlx.geojson_to_geobuf(geo_json)
    return geo_json
def rgb_to_hex(rgb):
    return '#'+ '%02x%02x%02x' % rgb
