import json

# Load the data from a file
with open('avgsenti_suburb_centre.json', 'r') as f:
    data = json.load(f)

new_data = {}
for key, value in data.items():
    new_data[key.upper()] = value

# Save the result to a file
with open('avgsenti_suburb_centre_new.json', 'w') as f:
    json.dump(new_data, f, indent=4)