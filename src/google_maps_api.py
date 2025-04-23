import logging
from src import settings
import requests

logger = logging.getLogger(__name__)


def get_place(search_text, location:dict, nextPageToken):
    # Define the search parameters
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": settings.GMAPS_TOKEN,
        "X-Goog-FieldMask": "places.id,places.accessibilityOptions,places.addressComponents,places.adrFormatAddress,places.businessStatus,places.containingPlaces,places.displayName,places.formattedAddress,places.googleMapsUri,places.iconBackgroundColor,places.iconMaskBaseUri,places.location,places.photos,places.plusCode,places.primaryType,places.primaryTypeDisplayName,places.pureServiceAreaBusiness,places.shortFormattedAddress,places.subDestinations,places.types,places.utcOffsetMinutes,places.viewport,places.currentOpeningHours,places.currentSecondaryOpeningHours,places.internationalPhoneNumber,places.nationalPhoneNumber,places.priceLevel,places.priceRange,places.rating,places.regularOpeningHours,places.regularSecondaryOpeningHours,places.userRatingCount,places.websiteUri,nextPageToken"
    }

    data = {
        "textQuery": search_text,
        "locationRestriction": {
            "rectangle": {
                "high": {
                    "latitude": location['high_lat'],
                    "longitude": location['high_long']
                    },
                "low": {
                    "latitude": location['low_lat'], 
                    "longitude": location['low_long']
                    }
                }
            }
        }
    
    if nextPageToken:
        data['pageToken'] = nextPageToken
    response = requests.post(settings.PLACE_URL, headers=headers, json=data)
    if response.status_code == 200:
        return response.json().get('places', []), response.json().get('nextPageToken')

    else:
        logger.error(response.status_code)
        return None