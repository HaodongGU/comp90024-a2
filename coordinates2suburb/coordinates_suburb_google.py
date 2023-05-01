# Import necessary libraries
import requests

# Define a function to get suburb name from a location coordinate using the Google Maps API
def get_suburb_name(latitude, longitude, api_key):
    # Define the API endpoint
    endpoint = 'https://maps.googleapis.com/maps/api/geocode/json'
    # Define the API parameters
    params = {'latlng': f'{latitude},{longitude}', 'key': api_key}
    # Send a GET request to the API endpoint with the parameters
    response = requests.get(endpoint, params=params)
    # Parse the JSON response
    json_data = response.json()
    # Extract the suburb name from the response
    results = json_data.get('results', [])
    if len(results) > 0:
        address_components = results[0].get('address_components', [])
        for component in address_components:
            if 'locality' in component['types'] and 'political' in component['types']:
                return component['long_name']
    # If no suburb name is found, return None
    return None

# Example usage
latitude = -37.802047
longitude = 144.969512
api_key = 'AIzaSyAPcUQ65PDtiTToBTVgXF9uMRTiu5orEyU'
suburb_name = get_suburb_name(latitude, longitude, api_key)
print(suburb_name) # Output: 'Sydney'

