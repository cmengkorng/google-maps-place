import pandas as pd
from src import google_maps_api
import ast
import numpy as np

import logging

logger = logging.getLogger(__name__)

def split_rectangle(high, low, split_type='vertical'):
    """
    Split a rectangle into two smaller rectangles.
    
    :param high: Tuple of the high point (lat, long) for top-left corner
    :param low: Tuple of the low point (lat, long) for bottom-right corner
    :param split_type: 'vertical' to split along longitude, 'horizontal' to split along latitude
    :return: Two rectangles, each defined by (lat, long) tuples for high and low points
    """
    
    high_lat, high_long = high
    low_lat, low_long = low
    
    if split_type == 'vertical':
        # Split along longitude
        midpoint_long = (high_long + low_long) / 2
        
        # Rectangle 1
        rec1_high = (high_lat, high_long)
        rec1_low = (low_lat, midpoint_long)
        
        # Rectangle 2
        rec2_high = (high_lat, midpoint_long)
        rec2_low = (low_lat, low_long)
        
    elif split_type == 'horizontal':
        # Split along latitude
        midpoint_lat = (high_lat + low_lat) / 2
        
        # Rectangle 1
        rec1_high = (high_lat, high_long)
        rec1_low = (midpoint_lat, low_long)
        
        # Rectangle 2
        rec2_high = (midpoint_lat, high_long)
        rec2_low = (low_lat, low_long)
        
    else:
        raise ValueError("Invalid split_type. Choose 'vertical' or 'horizontal'.")
    
    return {
        'rec1': {
            'high': rec1_high,
            'low': rec1_low
        },
        'rec2': {
            'high': rec2_high,
            'low': rec2_low
        }
    }

def fetch_location(search_list, area, bounary):
    places = []
    sub_bounary = split_rectangle(high=bounary['high'], low=bounary['low'], split_type='horizontal')
    for rec in ['rec1', 'rec2']:
        for search_text in search_list:
            paginate = True
            nextPageToken = None
            while paginate:
                location = {
                    "high_lat": sub_bounary[rec]['high'][0],
                    "high_long": sub_bounary[rec]['high'][1],
                    "low_lat": sub_bounary[rec]['low'][0],
                    "low_long": sub_bounary[rec]['low'][1],
                }
                logger.info(location)
                result, nextPageToken = google_maps_api.get_place(search_text, location=location, nextPageToken=nextPageToken)
                if result:
                    result = [{**r, "area": area, "category": search_text} for r in result]
                    places.extend(result)
                logger.info(f"{area + rec} - {search_text} - {len(result)}")
                if nextPageToken:
                    continue
                else:
                    paginate = False
    
    return places

def extract_name(x):
    if pd.isna(x):
        return None
    try:
        parsed_list = ast.literal_eval(x)  # Convert string to list
        return parsed_list[0]['googleMapsUri'] if parsed_list else None  # Extract 'name' from first dictionary
    except (ValueError, SyntaxError, IndexError, KeyError):
        return None
    
def clean_data(file:str) -> pd.DataFrame:
    df = pd.read_csv(file)
    df['latitude'] = df['location'].apply(lambda x: ast.literal_eval(x)['latitude'])
    df['longitude'] = df['location'].apply(lambda x: ast.literal_eval(x)['longitude'])
    df['photo_link'] = df['photos'].apply(extract_name)
    df['name'] = df['displayName'].apply(lambda x: ast.literal_eval(x)['text'])

    df['telephone'] = df['nationalPhoneNumber'].copy()
    df['google_maps_link'] = df['googleMapsUri'].copy()
    cols = ['name',
            'telephone', 
            'area',
            'category',
            'rating',
            'latitude',
            'longitude',
            'photo_link',
            'google_maps_link'
            ]
    return df[cols].drop_duplicates()



def nearest_point_v2(df_points:pd.DataFrame, 
                     df_location:pd.DataFrame, 
                     location_col:str, 
                     df_point_coords_col:list=['latitude', 'longitude'], 
                     df_location_coords_col:list=['latitude', 'longitude'],
                     output_col:list=['nearest_location', 'distance_km']
                     )-> pd.DataFrame:
    from scipy.spatial import cKDTree
    points_coords = np.radians(df_points[df_point_coords_col].values)
    location_coords = np.radians(df_location[df_location_coords_col].values)
    tree = cKDTree(location_coords)
    distances, indices = tree.query(points_coords, k=1)
    df_points[output_col[0]] = df_location.iloc[indices][location_col].values
    df_points[output_col[1]] = distances * 6371 *1000
    return df_points