import requests
import pandas as pd
import numpy as np
import string
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon


def geoBarrios(obj_returned = "dict"): 

    url = "https://cdn.buenosaires.gob.ar/datosabiertos/datasets/barrios/barrios.geojson"
    r = requests.get(url)
    js = r.json()

    keys = list(js['features'][0]['properties'].keys())[1:]
    geoBarrios = pd.DataFrame()
    for i in range(len(js['features'])): 
        properties = js['features'][i]['properties']
        datos = {k:properties[k] for k in keys}
        datos['coordinates'] = js['features'][i]['geometry']['coordinates']
        df_temp = pd.DataFrame(datos, index=[i])
        geoBarrios = geoBarrios.append(df_temp, ignore_index=True)

    geoBarrios.columns = [x.lower() for x in geoBarrios.columns]
    geoBarrios['barrio'] = geoBarrios['barrio'].apply(lambda x: x.lower())
    
    if obj_returned == 'dataframe': 
        return geoBarrios
    elif obj_returned == 'dict': 
        return geoBarrios[['barrio','coordinates']].set_index('barrio').to_dict()['coordinates']
    else: 
        print("Define returned object type")

def point_in_polygon(point, polygon): 
    """point: tuple
       polygon: list of tuples
       return: bool (True/False)
    """
    point = Point(point) #shapley object
    #print(polygon)
    polygon = Polygon(polygon) #shapley object
    return polygon.contains(point)

def coord_to_nbhd(coord, polygons_dict, est_nbhd = None):
    """ coord: tuple with lon & lat coordinates
        polygons_dict: key, value dict with k: neighborhood, v: polygon
        return: string. It may be a concatenated string if more than one neighborhood is matched"""
    if coord==np.nan:
        return np.nan
    matches = []
    if isinstance(est_nbhd, str) and est_nbhd.lower() in polygons_dict:
            if point_in_polygon(coord, polygons_dict[est_nbhd.lower()][0]):
                return est_nbhd
            else: 
                for nbhd in polygons_dict.keys(): 
                    if point_in_polygon(coord, polygons_dict[nbhd][0]):
                        matches.append(string.capwords(nbhd)) 
                    if matches!=[]:
                        return ",".join(matches)
                    else:
                        return np.nan
    else: 
        for nbhd in polygons_dict.keys(): 
            if point_in_polygon(coord, polygons_dict[nbhd][0]):
                matches.append(string.capwords(nbhd)) 
        if matches!=[]:
            return ",".join(matches)
        else:
            return np.nan