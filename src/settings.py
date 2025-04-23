from dotenv import load_dotenv
import os

load_dotenv('.env')

PLACE_URL="https://places.googleapis.com/v1/places:searchText"
GMAPS_TOKEN=os.getenv('GMAPS_TOKEN')
SCAN_AREA='data/scan_area'
output_folder='data/output'