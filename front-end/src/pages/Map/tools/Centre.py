import json

def calculate_geometric_center(coordinates):
    # Calculate the average of latitude and longitude values
    num_points = len(coordinates)
    sum_lat, sum_lon = 0, 0

    for coord in coordinates:
        sum_lat += coord[1]
        sum_lon += coord[0]

    center_lat = sum_lat / num_points
    center_lon = sum_lon / num_points
    return [center_lat, center_lon]  # Return as [longitude, latitude]

# Load the JSON file
with open('suburbsData.json', 'r') as json_file:
    data = json.load(json_file)

output_data = {}

# Iterate through each suburb
for suburb in data['features']:
    name = suburb['properties']['vic_loca_2']
    loc_pid = suburb['properties']['loc_pid']
    coordinates = suburb['geometry']['coordinates'][0][0]  # Assuming polygon coordinates are in the first element
    center_coordinates = calculate_geometric_center(coordinates)

    # Store the information in the output dictionary
    output_data[name] = {
        'loc_pid(not postcode?)': loc_pid,
        'center_coordinates': center_coordinates
    }

# Write the output data to a new JSON file
with open('suburb_centre.json', 'w') as json_output_file:
    json.dump(output_data, json_output_file, indent=2)
