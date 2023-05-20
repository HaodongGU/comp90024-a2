import json

def load_and_parse_json(filename):
    with open(filename, 'r') as f:
        data = json.load(f)

    avgsenti_values = []

    for location in data.values():
        if "avgsenti" in location:
            avgsenti_values.append(location["avgsenti"])

    return avgsenti_values

def main():
    filename = 'avgsenti_suburb_centre.json'  # Replace with your actual JSON file name
    avgsenti_values = load_and_parse_json(filename)
    print(f'Total occurrences of "avgsenti": {len(avgsenti_values)}')

    avgsenti_values.sort(reverse=True)
    # print(f'Sorted "avgsenti" values: {avgsenti_values}')
    print("tier 0: ", avgsenti_values[0])
    print("tier 1: ", avgsenti_values[int(len(avgsenti_values)/5) * 1])
    print("tier 2: ", avgsenti_values[int(len(avgsenti_values)/5) * 2])
    print("tier 3: ", avgsenti_values[int(len(avgsenti_values)/5) * 3])
    print("tier 4: ", avgsenti_values[int(len(avgsenti_values)/5) * 4])

if __name__ == "__main__":
    main()
