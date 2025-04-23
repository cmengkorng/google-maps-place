
from src import utils
import pandas as pd
from src import settings
import argparse
import os
import logging
from logging.handlers import RotatingFileHandler

# Set up root logger for the application
logger = logging.getLogger(__name__)
logger.propagate = False
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(filename)s - %(levelname)s - %(message)s"
)

formatter = logging.Formatter("%(asctime)s - %(filename)s - %(levelname)s - %(message)s")

# Set up StreamHandler (for logging to console)
stream_handler = logging.StreamHandler()
file_handler = RotatingFileHandler("logs/app.log", maxBytes=1024 * 1024, backupCount=3, encoding='utf-8')

stream_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

# Add the StreamHandler to the root logger
logger.addHandler(stream_handler)
logger.addHandler(file_handler)


def main(search_keywords:list, scan_file:str, outlet_check, outlet_file):
    os.makedirs(f"{settings.output_folder}/{scan_file}", exist_ok=True)
    output_raw = f'{settings.output_folder}/{scan_file}/raw_gmaps_extraction.csv'
    output = f'{settings.output_folder}/{scan_file}_output.xlsx'

    logger.info('search keywords')
    for k in search_keywords:
        logger.info(f"    {k}")

    logger.info(f"scanning file: {scan_file}.csv")
    areas = pd.read_csv(f"{settings.SCAN_AREA}/{scan_file}.csv")
    logger.info(f"scanning location total: {areas.shape[0]}")
    all_places = []
    logger.info('fetch location from google maps')
    for i in areas.index:
        bounary = {
            'high': (float(areas.loc[i, 'high_lat']), float(areas.loc[i, 'high_long'])),
            'low': (float(areas.loc[i, 'low_lat']), float(areas.loc[i, 'low_long']))}
        logger.info(bounary)
        places = utils.fetch_location(search_list=search_keywords, area=areas.loc[i, 'area'], bounary=bounary)
        all_places.extend(places)
    pd.DataFrame(all_places).to_csv(output_raw, index=False)
    logger.info(f'saved file: {output_raw}')
    logger.info(f'clean: {output_raw}')
    df = utils.clean_data(output_raw)

    if outlet_check:
        outlets = pd.read_excel(outlet_file)
        logger.info('outlet check enable')
        df_reverse_geo = utils.nearest_point_v2(
                df_points=df,
                df_location=outlets,
                location_col="Outlet Code",
                df_point_coords_col=["latitude", "longitude"],
                df_location_coords_col=["latitude", "longitude"],
                output_col=["outlet", "outlet_distance_m"],
            )
        
        df_reverse_geo.rename(columns={"outlet": "nearest_outlet"}, inplace=True)
        cols = ['name', 'telephone', 'area', 'category', 'rating',
        'latitude', 'longitude', 'photo_link', 'google_maps_link', 'nearest_outlet',
        'outlet_distance_m']
        df_reverse_geo[cols].to_excel(output, index=False)
    else:
        df.to_excel(output, index=False)

    logger.info(f"saved output file: {output}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scan a file for given keywords.")
    parser.add_argument('--keywords', nargs='+', required=True, help='List of keywords to search for')
    parser.add_argument('--file', required=True, help='Path to the file to scan')
    parser.add_argument('--outlet-check', action='store_true', help='Include this flag to enable outlet logic')
    parser.add_argument('--outlet-file', help='File path for outlet data (required if --outlet is set)')

    args = parser.parse_args()

    # Conditional validation
    if args.outlet_check and not args.outlet_file:
        parser.error("--outlet-file is required when --outlet is set")

    main(args.keywords, args.file, args.outlet_check, args.outlet_file)
