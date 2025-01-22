from geopy.geocoders import Nominatim


def get_address(latitude, longitude, language='en'):
    geolocator = Nominatim(user_agent="Sonni topchi")
    location = geolocator.reverse((latitude, longitude), language=language)

    if location:
        return location.address
    else:
        return "Address not found"
