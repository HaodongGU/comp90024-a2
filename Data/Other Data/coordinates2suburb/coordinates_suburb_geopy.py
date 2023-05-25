# Import necessary libraries
from geopy.geocoders import Nominatim

# Define a function to get suburb name from a location coordinate
def get_suburb_name(latitude, longitude):
    # Create a geolocator object using Nominatim API
    geolocator = Nominatim(user_agent='my_application')
    # Reverse geocode the location coordinate to get the address
    location = geolocator.reverse(f'{latitude}, {longitude}')
    # Extract the suburb name from the address
    address = location.raw['address']
    suburb_name = address.get('suburb', None)
    # Return the suburb name, or None if not found
    return suburb_name

# Example usage
latitude = -37.802047
longitude = 144.969512
suburb_name = get_suburb_name(latitude, longitude)
print(suburb_name) # Output: 'Sydney'


# lat = centroid(coordinates)[0]
# lon = centroid(coordinates)[1]
lat = -38.6829
lon = 145.6424
# lat = -33.8671
# lon = 151.2071
# print(lat)
# print(lon)
